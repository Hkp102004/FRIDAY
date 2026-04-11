import subprocess
import time
import psutil
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SPOTIFY_PATH = r"C:\Users\Harsh\AppData\Local\Microsoft\WindowsApps\Spotify.exe"

SCOPE = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

def get_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=SCOPE,
        cache_path=".spotify_cache"
    ))
    return sp

def is_spotify_running():
    for proc in psutil.process_iter(['name']):
        try:
            if 'spotify' in proc.info['name'].lower():
                return True
        except:
            pass
    return False

def ensure_spotify_running():
    if not is_spotify_running():
        subprocess.Popen(SPOTIFY_PATH, shell=True)
        time.sleep(5)

def get_active_device(sp):
    devices = sp.devices()
    if devices and devices['devices']:
        for device in devices['devices']:
            if device['is_active']:
                return device['id']
        return devices['devices'][0]['id']
    return None

def toggle_playback():
    try:
        ensure_spotify_running()
        time.sleep(1)
        sp = get_spotify()
        device_id = get_active_device(sp)
        playback = sp.current_playback()
        if playback and playback['is_playing']:
            sp.pause_playback(device_id=device_id)
            return "Music paused!"
        else:
            sp.start_playback(device_id=device_id)
            return "Music playing!"
    except Exception as e:
        return f"Couldn't toggle playback: {str(e)}"

def pause_music():
    try:
        if not is_spotify_running():
            return "Spotify is not running!"
        sp = get_spotify()
        device_id = get_active_device(sp)
        sp.pause_playback(device_id=device_id)
        return "Music paused!"
    except Exception as e:
        return f"Couldn't pause: {str(e)}"

def next_song():
    try:
        if not is_spotify_running():
            return "Spotify is not running!"
        sp = get_spotify()
        device_id = get_active_device(sp)
        sp.next_track(device_id=device_id)
        return "Skipping to next song!"
    except Exception as e:
        return f"Couldn't skip: {str(e)}"

def previous_song():
    try:
        if not is_spotify_running():
            return "Spotify is not running!"
        sp = get_spotify()
        device_id = get_active_device(sp)
        sp.previous_track(device_id=device_id)
        return "Going to previous song!"
    except Exception as e:
        return f"Couldn't go back: {str(e)}"

def play_song(song_name):
    try:
        ensure_spotify_running()
        time.sleep(1)
        sp = get_spotify()
        device_id = get_active_device(sp)
        results = sp.search(q=f"track:{song_name}", type='track', limit=1)
        tracks = results['tracks']['items']
        if tracks:
            track = tracks[0]
            sp.start_playback(device_id=device_id, uris=[track['uri']])
            return f"Playing {track['name']} by {track['artists'][0]['name']}!"
        return f"Couldn't find {song_name} on Spotify!"
    except Exception as e:
        return f"Couldn't play song: {str(e)}"

def get_current_song():
    try:
        sp = get_spotify()
        playback = sp.current_playback()
        if playback and playback['is_playing']:
            track = playback['item']
            return f"Currently playing {track['name']} by {track['artists'][0]['name']}!"
        return "Nothing is playing right now!"
    except Exception as e:
        return f"Couldn't get current song: {str(e)}"

def set_spotify_volume(level):
    try:
        sp = get_spotify()
        device_id = get_active_device(sp)
        sp.volume(int(level), device_id=device_id)
        return f"Spotify volume set to {level}%!"
    except Exception as e:
        return f"Couldn't set volume: {str(e)}"
    
def play_playlist(playlist_name):
    try:
        ensure_spotify_running()
        time.sleep(1)
        sp = get_spotify()
        device_id = get_active_device(sp)
        
        # Search for playlist
        results = sp.search(q=playlist_name, type='playlist', limit=1)
        playlists = results['playlists']['items']
        
        if playlists:
            playlist = playlists[0]
            sp.start_playback(device_id=device_id, context_uri=playlist['uri'])
            return f"Playing playlist {playlist['name']}!"
        return f"Couldn't find playlist {playlist_name}!"
    except Exception as e:
        return f"Couldn't play playlist: {str(e)}"

def play_my_playlist(playlist_name):
    try:
        ensure_spotify_running()
        time.sleep(1)
        sp = get_spotify()
        device_id = get_active_device(sp)
        
        # Get user's own playlists
        playlists = sp.current_user_playlists(limit=50)
        
        for playlist in playlists['items']:
            if playlist_name.lower() in playlist['name'].lower():
                sp.start_playback(device_id=device_id, context_uri=playlist['uri'])
                return f"Playing your playlist {playlist['name']}!"
        
        # If not found in own playlists search globally
        return play_playlist(playlist_name)
    except Exception as e:
        return f"Couldn't play playlist: {str(e)}"

def get_my_playlists():
    try:
        sp = get_spotify()
        playlists = sp.current_user_playlists(limit=20)
        if playlists['items']:
            names = [p['name'] for p in playlists['items']]
            return "Your playlists: " + ", ".join(names)
        return "No playlists found!"
    except Exception as e:
        return f"Couldn't get playlists: {str(e)}"