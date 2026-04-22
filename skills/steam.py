import os
import re
import subprocess

STEAM_PATH = r"C:\Program Files (x86)\Steam"
LIBRARY_VDF = os.path.join(STEAM_PATH, "steamapps", "libraryfolders.vdf")

def _get_library_paths():
    """
    Reads libraryfolders.vdf to find all Steam library locations
    across all drives automatically.
    """
    paths = [os.path.join(STEAM_PATH, "steamapps")]  # default library

    if not os.path.exists(LIBRARY_VDF):
        return paths

    try:
        with open(LIBRARY_VDF, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract all "path" values from the vdf file
        matches = re.findall(r'"path"\s+"([^"]+)"', content)
        for path in matches:
            steamapps = os.path.join(path, "steamapps")
            if os.path.exists(steamapps) and steamapps not in paths:
                paths.append(steamapps)
    except Exception as e:
        print(f"[Steam] Error reading library paths: {e}")

    return paths


def _build_game_library():
    """
    Scans all Steam library folders and builds a dict of
    game_name (lowercase) -> app_id.
    """
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
                # Extract app id and name
                app_id = re.search(r'"appid"\s+"(\d+)"', content)
                name = re.search(r'"name"\s+"([^"]+)"', content)
                if app_id and name:
                    games[name.group(1).lower()] = app_id.group(1)
            except Exception:
                continue

    print(f"[Steam] Found {len(games)} games in library")
    return games


# Build the library once at import time
_game_library = _build_game_library()


def _find_game(query):
    """
    Finds the best matching game from the library for a given query.
    Tries exact match first, then partial match.
    """
    query = query.lower().strip()

    # Exact match
    if query in _game_library:
        return query, _game_library[query]

    # Partial match — query is contained in game name
    matches = [(name, gid) for name, gid in _game_library.items() if query in name]
    if matches:
        # Pick shortest match (closest to what was asked)
        matches.sort(key=lambda x: len(x[0]))
        return matches[0]

    # Partial match — game name is contained in query
    matches = [(name, gid) for name, gid in _game_library.items() if name in query]
    if matches:
        matches.sort(key=lambda x: len(x[0]), reverse=True)
        return matches[0]

    return None, None


def launch_game(game_name):
    """Launch a Steam game by name."""
    try:
        name, app_id = _find_game(game_name)

        if not app_id:
            # Give a helpful hint if no match found
            suggestions = [n for n in _game_library.keys() if any(word in n for word in game_name.lower().split())]
            if suggestions:
                return f"Couldn't find {game_name}. Did you mean: {', '.join(suggestions[:3])}?"
            return f"Couldn't find {game_name} in your Steam library!"

        subprocess.Popen(f"start steam://rungameid/{app_id}", shell=True)
        # Capitalize game name nicely for response
        display_name = name.title()
        return f"Launching {display_name}!"

    except Exception as e:
        return f"Couldn't launch {game_name}: {str(e)}"


def get_steam_games():
    """Returns a list of all installed Steam games."""
    if not _game_library:
        return "No Steam games found!"
    names = sorted([name.title() for name in _game_library.keys()])
    return "Your Steam games: " + ", ".join(names)


def refresh_library():
    """Refreshes the game library cache — call this after installing new games."""
    global _game_library
    _game_library = _build_game_library()
    return f"Library refreshed! Found {len(_game_library)} games."


if __name__ == "__main__":
    print("Steam games found:")
    for name, gid in sorted(_game_library.items()):
        print(f"  {name.title()} (ID: {gid})")