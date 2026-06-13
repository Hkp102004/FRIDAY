import os
import re
import subprocess
import time
from rapidfuzz import process, fuzz

STEAM_PATH = r"C:\Program Files (x86)\Steam"
LIBRARY_VDF = os.path.join(STEAM_PATH, "steamapps", "libraryfolders.vdf")

def _normalize(text):
    """Normalize text — lowercase, straight apostrophes, strip punctuation."""
    text = text.lower().strip()
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.rstrip(".,!?")
    return text

def _get_library_paths():
    paths = [os.path.join(STEAM_PATH, "steamapps")]
    if not os.path.exists(LIBRARY_VDF):
        return paths
    try:
        with open(LIBRARY_VDF, "r", encoding="utf-8") as f:
            content = f.read()
        matches = re.findall(r'"path"\s+"([^"]+)"', content)
        for path in matches:
            steamapps = os.path.join(path, "steamapps")
            if os.path.exists(steamapps) and steamapps not in paths:
                paths.append(steamapps)
    except Exception as e:
        print(f"[Steam] Error reading library paths: {e}")
    return paths

def _build_game_library():
    games = {}
    library_paths = _get_library_paths()
    for library in library_paths:
        if not os.path.exists(library):
            continue
        for filename in os.listdir(library):
            if not filename.startswith("appmanifest_") or not filename.endswith(".acf"):
                continue
            acf_path = os.path.join(library, filename)
            try:
                with open(acf_path, "r", encoding="utf-8") as f:
                    content = f.read()
                app_id = re.search(r'"appid"\s+"(\d+)"', content)
                name = re.search(r'"name"\s+"([^"]+)"', content)
                if app_id and name:
                    # Normalize name — straight apostrophes, lowercase
                    normalized = _normalize(name.group(1))
                    games[normalized] = app_id.group(1)
            except Exception:
                continue
    print(f"[Steam] Found {len(games)} games in library")
    return games

_game_library = _build_game_library()

def _find_game(query):
    """Find best matching game using rapidfuzz fuzzy matching."""
    query = _normalize(query)
    print(f"[Steam] Searching for: '{query}'")

    if not _game_library:
        return None, None

    # Use rapidfuzz to find best match
    result = process.extractOne(
        query,
        _game_library.keys(),
        scorer=fuzz.token_sort_ratio,  # handles word order differences
        score_cutoff=50  # minimum 50% match — below this = no match
    )

    if result:
        name, score, _ = result
        print(f"[Steam] Best match: '{name}' (score: {score})")
        return name, _game_library[name]

    return None, None

def launch_game(game_name):
    try:
        name, app_id = _find_game(game_name)
        if not app_id:
            return f"Couldn't find {game_name} in your Steam library!"
        subprocess.Popen(f"start steam://rungameid/{app_id}", shell=True)
        return f"Launching {name.title()}!"
    except Exception as e:
        return f"Couldn't launch {game_name}: {str(e)}"

def get_steam_games():
    if not _game_library:
        return "No Steam games found!"
    names = sorted([name.title() for name in _game_library.keys()])
    return "Your Steam games: " + ", ".join(names)

def refresh_library():
    global _game_library
    _game_library = _build_game_library()
    return f"Library refreshed! Found {len(_game_library)} games."

def restart_steam():
    try:
        subprocess.run(["taskkill", "/f", "/im", "steam.exe"], capture_output=True)
        time.sleep(3)
        subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe")
        return "Restarting Steam!"
    except Exception as e:
        return f"Couldn't restart Steam: {str(e)}"

if __name__ == "__main__":
    print("Steam games found:")
    for name, gid in sorted(_game_library.items()):
        print(f"  {name.title()} (ID: {gid})")