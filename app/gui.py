import os
import requests
import threading
from io import BytesIO
import customtkinter as ctk
from PIL import Image, ImageDraw
from downloader import get_info, download, format_duration


def change_theme(new_apperance_mode):
    ctk.set_appearance_mode(new_apperance_mode)
    

def show_status(text, color="white"):
    global status_label
    if status_label is not None:
        status_label.destroy()
    status_label = ctk.CTkLabel(app, text=text, font=("Arial", 18, "bold"), 
                                text_color=color)
    status_label.grid(row=3, column=0, pady=10)


def round_corners(img, radius):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), 
                           radius=radius, fill=255)
    img = img.convert("RGBA")
    img.putalpha(mask)
    return img


def search_and_download():
    def task():
        url = entry.get().strip()
        if not url:
            return
        if url.startswith('https://open.spotify.com/track/'):
            app.after(0, lambda: show_status("", "lightgreen"))
            try:
                data = get_info(url)
                if app.winfo_exists():
                    app.after(0, lambda: update_preview(
                        data.get("name"),
                        data.get("artists")[0],
                        data.get("album_name"),
                        format_duration(data.get("duration")),
                        data.get("release_date"),
                        data.get("images")[0]
                    ))

                if app.winfo_exists():
                    if os.path.exists(f'songs/{data.get("name")} - {data.get("artists")[0]}.mp3'):
                        app.after(0, lambda: show_status(
                            f"✅ {data.get('name')} has already been downloaded!", "green")
                            )
                    else:
                        if app.winfo_exists():
                            app.after(0, lambda: show_status(
                                f"⏳ {data.get('name')} is downloading...", "orange")
                                )
                        download(data)

                        if app.winfo_exists():
                            app.after(0, lambda: show_status(
                                f"✅ {data.get('name')} downloaded!", "green")
                                )

            except Exception as e:
                if app.winfo_exists():
                    print(f"\n\n{e}\n\n")
                    app.after(0, lambda: show_status(f"❌ Error: {e}", "red"))
        else:
            if app.winfo_exists():
                app.after(0, lambda: show_status("❌ Incorrect link!", "red"))
    threading.Thread(target=task).start()


def update_preview(name, artist_name, album_name, duration_str, release_date, cover_url):
    global preview_frame, cover_label, track_title, artist, album, length

    if preview_frame is not None:
        preview_frame.destroy()

    preview_frame = ctk.CTkFrame(app, width=450, height=250, corner_radius=30)
    preview_frame.grid(row=2, column=0, pady=20, padx=20, sticky="n")

    img_data = requests.get(cover_url).content
    img = Image.open(BytesIO(img_data)).resize((250, 250))
    img = round_corners(img, 15)
    cover = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 250))
    cover_label = ctk.CTkLabel(preview_frame, image=cover, text="", width=250, height=250)
    cover_label.grid(row=0, column=0, rowspan=4, padx=(15, 30), pady=15)

    info_frame = ctk.CTkFrame(preview_frame, fg_color="transparent")
    info_frame.grid(row=0, column=1, sticky="nw", padx=(0,50), pady=15)

    track_title = ctk.CTkLabel(info_frame, text=name, font=("Arial", 40, "bold"))
    track_title.grid(row=0, column=1, sticky="w", padx=(0, 50), pady=(0, 20))

    artist = ctk.CTkLabel(info_frame, text=artist_name, font=("Arial", 32, "bold"))
    artist.grid(row=1, column=1, sticky="w", padx=(0, 50), pady=(0, 20))

    album = ctk.CTkLabel(info_frame, text=album_name, font=("Arial", 20))
    album.grid(row=2, column=1, sticky="w", padx=(0, 50), pady=(0, 10))

    length = ctk.CTkLabel(info_frame, text=f"{duration_str} - {release_date}", font=("Arial", 20))
    length.grid(row=3, column=1, sticky="w", padx=(0, 50))


status_label = None
preview_frame = None
cover_label = None
track_title = None
artist = None
album = None
length = None

app = ctk.CTk()
app.title('Spotiloader')
app.geometry('900x750')
app.resizable(False, False)
ctk.set_default_color_theme('lavender.json')

app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=0)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)

logo_img = ctk.CTkImage(light_image=Image.open('logo/logo_d.png'),
                        dark_image=Image.open('logo/logo_l.png'),
                        size=(600, 150))
logo_label = ctk.CTkLabel(app, image=logo_img, text="")
logo_label.grid(row=0, column=0, pady=(50, 20), sticky="n")

frame = ctk.CTkFrame(app, fg_color="transparent")
frame.grid(row=1, column=0, pady=5, padx=5)
frame.grid_columnconfigure(0, weight=2)
frame.grid_columnconfigure(1, weight=1)

entry = ctk.CTkEntry(frame, placeholder_text="Spotify track link...", 
                     width=500, height=40, font=('Arial', 20), corner_radius=25)
entry.grid(row=0, column=0, padx=5, pady=5)

appearance_mode_option_menu = ctk.CTkOptionMenu(app, values=["Dark", "Light"],
                                         command=change_theme)
appearance_mode_option_menu.grid(row=4, column=0, columnspan=4, padx=(0, 0), pady=(0, 50))

button = ctk.CTkButton(frame, text="Download", width=150, height=40, 
                       font=('Arial', 20), corner_radius=25, command=search_and_download)
button.grid(row=0, column=1, padx=5, pady=5)


app.mainloop()
