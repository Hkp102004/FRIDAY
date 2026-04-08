from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import psutil
import os

def set_volume(level):
    try:
        level = int(level)
        level = max(0, min(100, level))
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return f"Volume set to {level}%!"
    except Exception as e:
        return f"Couldn't set volume: {str(e)}"

def get_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        level = round(volume.GetMasterVolumeLevelScalar() * 100)
        return f"Current volume is {level}%"
    except Exception as e:
        return f"Couldn't get volume: {str(e)}"

def set_brightness(level):
    try:
        level = int(level)
        level = max(0, min(100, level))
        sbc.set_brightness(level)
        return f"Brightness set to {level}%!"
    except Exception as e:
        return f"Couldn't set brightness: {str(e)}"

def get_brightness():
    try:
        level = sbc.get_brightness()[0]
        return f"Current brightness is {level}%"
    except Exception as e:
        return f"Couldn't get brightness: {str(e)}"

def get_battery():
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = "charging" if battery.power_plugged else "not charging"
            return f"Battery is at {round(battery.percent)}% and {status}!"
        return "Couldn't find battery info!"
    except Exception as e:
        return f"Error: {str(e)}"

def take_screenshot():
    try:
        import pyautogui
        import datetime
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
        pyautogui.screenshot(path)
        return f"Screenshot saved to your desktop as {filename}!"
    except Exception as e:
        return f"Couldn't take screenshot: {str(e)}"

def get_system_info():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_used = round(ram.used / (1024**3), 1)
        ram_total = round(ram.total / (1024**3), 1)
        return f"CPU usage is {cpu}% and RAM usage is {ram_used}GB out of {ram_total}GB!"
    except Exception as e:
        return f"Error: {str(e)}"