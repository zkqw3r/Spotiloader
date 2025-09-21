# 🎵 Spotiloader
[![CustomTkinter](https://img.shields.io/badge/Custom%20Tkinter%20-EEA8AA?style=for-the-badge&logo=python&logoColor=black)](https://customtkinter.tomschimansky.com/)
[![Spotipy](https://img.shields.io/badge/Spotipy%20-3D7A42?style=for-the-badge&logo=spotify&logoColor=black)](https://spotipy.readthedocs.io/en/2.25.1/)
[![Mutagen](https://img.shields.io/badge/metadata-Mutagen%20-9D77EB?style=for-the-badge&logoColor=black)](https://mutagen.readthedocs.io/en/latest/)
[![yt-dlp](https://img.shields.io/badge/Yt_dlp%20-BAC7CE?style=for-the-badge&logo=youtube&logoColor=red)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/license-MIT%20-333333?style=for-the-badge)](LICENSE)

**Spotiloader** — This is a simple GUI application (written in **CustomTkinter**) that allows you to:
- search for tracks by link from **Spotify**
- display information about the song (title, artist, album, cover, release date)
- download tracks using **yt-dlp**
- save them in a convenient **songs/** folder

<div align="center">
  <img src="screenshots/example1.png" width="1000" alt="Preview">

  *example of work*

  <img src="screenshots/example2.png" width="1000" alt="Preview">

  *example of work*
</div>


## 🚀 Installation and launch

### Option 1: Ready EXE (for Windows)
1. Download the latest release from [Releases section](https://github.com/zkqw3r/Spotiloader/releases/tag/Spotiloader)
2. Unzip the folder
3. Run `Spotiloader.exe`

### Option 2: From source

#### Clone the repository:
   ```bash
   git clone https://github.com/zkqw3r/Spotiloader
   cd spotiloader
   ```
#### Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
```
pip install -r requirements.txt
```
#### Create a .env file in the root of your project and specify your Spotify API keys:

```
clientId=your_client_id
clientSecret=your_client_secret
```

#### ▶️ Start app
```bash
python app/gui.py
```

## ❗Warning❗
### On Linux you may have the error: ModuleNotFoundError: No module named 'tkinter'
### even after installing all dependencies, in which case:
### For Ubuntu or other distros with Apt:
```bash
sudo apt-get install python3-tk
```
### For Fedora:
```bash
sudo dnf install python3-tkinter
```

## 📂 Project structure
```bash
spotiloader/
│── app/
│   ├── gui.py          # GUI application
│   ├── downloader.py   # Download logic
│
│── logo/
│   ├── logo_d.png      # Logo for light theme
│   ├── logo_l.png      # Logo for dark theme
│
│── songs/              # Folder for downloaded tracks
│── lavender.json       # Application theme config
│── .env                # Spotify API Keys
│── requirements.txt    # Dependencies
```

## 📦 Dependencies
#### See requirements.txt for the full list:

- **customtkinter** — GUI

- **spotipy** — working with the Spotify API

- **yt-dlp** — loading tracks

- **mutagen** — tags for audio

- **pillow** — working with covers

- **requests**, dotenv etc.

## 📜 License
This project is licensed under the MIT License.
Feel free to use, modify and share.
