import subprocess
import psutil
import os

APPS = {
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "spotify": r"C:\Users\Harsh\AppData\Local\Microsoft\WindowsApps\Spotify.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "discord": r"C:\Users\Harsh\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "vs code": r"C:\Users\Harsh\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode": r"C:\Users\Harsh\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "opera": r"C:\Users\Harsh\AppData\Local\Programs\Opera GX\opera.exe",
    "opera gx": r"C:\Users\Harsh\AppData\Local\Programs\Opera GX\opera.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "github desktop": r"C:\Users\Harsh\AppData\Local\GitHubDesktop\GitHubDesktop.exe",
    "github": r"C:\Users\Harsh\AppData\Local\GitHubDesktop\GitHubDesktop.exe",
    "claude": r"C:\Users\Harsh\.local\bin\claude.exe",
    "unity hub": r"C:\Program Files\Unity Hub\Unity Hub.exe",
    "unity": r"C:\Program Files\Unity Hub\Unity Hub.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "settings": "ms-settings:",
}

def open_app(app_name):
    app_name = app_name.lower()
    for key, path in APPS.items():
        if key in app_name:
            try:
                subprocess.Popen(path, shell=True)
                return f"Opening {key} for you!"
            except Exception as e:
                return f"Couldn't open {key}: {str(e)}"
    return f"I don't know how to open {app_name} yet!"

def close_app(app_name):
    app_name = app_name.lower()
    closed = False
    for proc in psutil.process_iter(['name']):
        try:
            if app_name in proc.info['name'].lower():
                proc.kill()
                closed = True
        except:
            pass
    return f"Closed {app_name}!" if closed else f"Couldn't find {app_name} running!"

def get_running_apps():
    apps = []
    for proc in psutil.process_iter(['name']):
        try:
            apps.append(proc.info['name'])
        except:
            pass
    return list(set(apps))

def launch_steam_game(game_id):
    subprocess.Popen(f"start steam://rungameid/{game_id}", shell=True)
    return f"Launching game on Steam!"