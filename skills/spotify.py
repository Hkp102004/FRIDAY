import subprocess
import time
import psutil
import ctypes
from ctypes import wintypes

SPOTIFY_PATH = r"C:\Users\Harsh\AppData\Local\Microsoft\WindowsApps\Spotify.exe"

# Windows media key codes
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1

def press_media_key(key_code):
    """Press a media key - works globally without needing window focus!"""
    ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)

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

def get_spotify_window():
    user32 = ctypes.windll.user32
    found = ctypes.c_void_p(0)

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.c_void_p)
    def callback(hwnd, extra):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buffer, length + 1)
                title = buffer.value.lower()
                if 'spotify' in title:
                    nonlocal found
                    found = ctypes.c_void_p(hwnd)
                    return False
        return True

    user32.EnumWindows(callback, ctypes.c_void_p(0))
    return found.value if found.value else None

def focus_spotify():
    hwnd = get_spotify_window()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 9)
        time.sleep(0.2)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        return True
    return False

def toggle_playback():
    try:
        ensure_spotify_running()
        time.sleep(0.5)
        press_media_key(VK_MEDIA_PLAY_PAUSE)
        return "Toggled playback!"
    except Exception as e:
        return f"Couldn't toggle playback: {str(e)}"

def pause_music():
    try:
        if not is_spotify_running():
            return "Spotify is not running!"
        press_media_key(VK_MEDIA_PLAY_PAUSE)
        return "Music paused!"
    except Exception as e:
        return f"Couldn't pause music: {str(e)}"

def next_song():
    try:
        if not is_spotify_running():
            return "Spotify is not running!"
        press_media_key(VK_MEDIA_NEXT_TRACK)
        return "Skipping to next song!"
    except Exception as e:
        return f"Couldn't skip song: {str(e)}"

def previous_song():
    try:
        if not is_spotify_running():
            return "Spotify is not running!"
        press_media_key(VK_MEDIA_PREV_TRACK)
        return "Going to previous song!"
    except Exception as e:
        return f"Couldn't go to previous song: {str(e)}"

def play_song(song_name):
    try:
        import pyautogui
        ensure_spotify_running()
        focus_spotify()
        time.sleep(0.5)

        # Open search
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.8)

        # Clear and type
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.typewrite(f"play {song_name}", interval=0.05)
        time.sleep(2)

        # Select first result and play
        pyautogui.press('down')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)

        return f"Playing {song_name} on Spotify!"
    except Exception as e:
        return f"Couldn't play song: {str(e)}"