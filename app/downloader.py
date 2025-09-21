
import os
import yt_dlp
import spotipy
import requests
from mutagen.mp3 import MP3
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, APIC, error


load_dotenv()
CLIENT_ID = os.getenv("clientId")
CLIENT_SECRET = os.getenv('clientSecret')
auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def format_duration(ms):

    """
    Function to convert ms to min:sec to display track duration
    """

    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


def get_info(link):

    """
    A function for obtaining track information, such as:
    - track title
    - track length
    - track preview
    - album title
    - release date
    - artists
    - track/album images (often three identical but different sizes)
    """
    data = sp.track(track_id=link[31:link.find('?')])
    artists_data = data.get('artists')
    images_data = data.get('album').get('images')
    artists = []
    for i in range(len(artists_data)):
        artists.append(artists_data[i].get('name'))
    images = []
    for i in range(len(images_data)):
        images.append(images_data[i].get('url'))
    res_Data = {
        'name': data.get('name'),
        'duration': data.get('duration_ms'),
        'preview': data.get('preview_url'),
        'album_name': data.get('album').get('name'),
        'release_date': data.get('album').get('release_date'),
        'artists': artists,
        'images': images,
    }
    return res_Data


def download(data):

    """
    A function for downloading a track. 
    The track is searched for by keywords on YouTube 
    and only the audio is downloaded in mp3 format 
    with the best quality.
    """

    query = f'{data.get("artists")[0]} - {data.get("name")} Official'
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'songs/{data.get("name")} - {data.get("artists")[0]}.%(ext)s',
        'default_search': 'ytsearch',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }]
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([query])

    img_data = requests.get(data.get("images")[0]).content
    audio = MP3(f"songs/{data.get('name')} - {data.get('artists')[0]}.mp3", ID3=ID3)
    try:
        audio.add_tags()
    except error:
        pass
    audio.tags.add(TIT2(encoding=3, text=data.get('name')))
    audio.tags.add(TPE1(encoding=3, text=data.get('artists')[0]))
    audio.tags.add(TALB(encoding=3, text=data.get('album_name')))
    audio.tags.add(TDRC(encoding=3, text=data.get('release_date')))
    audio.tags.add(APIC(encoding=3, mime="image/png", type=3, desc='Cover', data=img_data))
    audio.save(v2_version=3)
