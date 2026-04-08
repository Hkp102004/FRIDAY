import os
import psutil
import subprocess
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level):
    try:
        level = int(level)
        level = max(0, min(100, level))
        volume = get_volume_interface()
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return f"Volume set to {level}%!"
    except Exception as e:
        try:
            # Fallback using PowerShell
            subprocess.run([
                'powershell', '-c',
                f'$obj = New-Object -ComObject WScript.Shell; '
                f'[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms"); '
                f'$vol = [Math]::Round({level} / 100 * 65535); '
                f'$mute = 0xF13F; '
                f'Add-Type -MemberDefinition "[DllImport(\'winmm.dll\')] public static extern int waveOutSetVolume(IntPtr h, uint dwVolume);" -Name "WinMM" -Namespace "Win32"; '
                f'[Win32.WinMM]::waveOutSetVolume([IntPtr]::Zero, ($vol -bor ($vol -shl 16)))'
            ], capture_output=True)
            return f"Volume set to {level}%!"
        except:
            return f"Couldn't set volume!"

def get_volume():
    try:
        volume = get_volume_interface()
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
        return f"CPU is at {cpu}% and RAM is {ram_used}GB out of {ram_total}GB!"
    except Exception as e:
        return f"Error: {str(e)}"