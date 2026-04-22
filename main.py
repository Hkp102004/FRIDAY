from brain import chat
from speak import speak
from listen import listen
from skills.apps import open_app, close_app
from skills.system import set_volume, get_volume, set_brightness, get_brightness, get_battery, take_screenshot, get_system_info
from skills.search import search_web, search_youtube, open_website
from skills.news import get_full_briefing, get_gaming_news, get_ai_news, get_world_news
from skills.tasks import add_task, get_tasks, complete_task, clear_tasks
from skills.spotify import play_song, pause_music, next_song, previous_song, toggle_playback, get_current_song, play_playlist, play_my_playlist, get_my_playlists
import re
import subprocess
import time
import threading
import keyboard  # pip install keyboard

# ── How long Friday waits for follow-up before going back to sleep ─────────
CONVERSATION_TIMEOUT = 30  # seconds

# ── F4 hotkey flag ─────────────────────────────────────────────────────────
_f4_pressed = threading.Event()
_friday_awake = threading.Event()  # tracks whether Friday is in conversation mode

def _on_f4():
    if _friday_awake.is_set():
        print("[Hotkey] F4 pressed — sending Friday to sleep!")
    else:
        print("[Hotkey] F4 pressed — waking Friday up!")
    _f4_pressed.set()

keyboard.add_hotkey('f4', _on_f4)

def _flush_audio_queue():
    """Throw away all stale audio chunks sitting in the wake word queue."""
    from wakeword import _audio_queue
    flushed = 0
    while not _audio_queue.empty():
        try:
            _audio_queue.get_nowait()
            flushed += 1
        except Exception:
            break
    if flushed:
        print(f"[Queue] Flushed {flushed} stale audio chunk(s)")

def extract_number(text):
    numbers = re.findall(r'\d+', text)
    return numbers[0] if numbers else None

def extract_song(text):
    song = text
    for phrase in [
        "play the song called", "play the song", "play song called",
        "play song", "play the track", "play track", "on spotify",
        "from spotify", "can you", "please", "for me", "resume music",
        "resume the song", "resume song", "resume",
        "start music", "put on", "i want to hear", "i want to listen to"
    ]:
        song = song.replace(phrase, "")
    song = song.strip()
    if song.startswith("play "):
        song = song[5:]
    return song.strip()

def handle_command(user_input):
    text = user_input.lower()

    # --- NEWS ---
    if "news briefing" in text or "morning briefing" in text or "all news" in text:
        return get_full_briefing()
    elif "gaming news" in text or "game news" in text:
        return get_gaming_news()
    elif "ai news" in text or "tech news" in text:
        return get_ai_news()
    elif "world news" in text:
        return get_world_news()

    # --- TASKS ---
    elif "add task" in text or "add to my list" in text or "remind me to" in text:
        task = text.replace("add task", "").replace("add to my list", "").replace("remind me to", "").strip()
        return add_task(task)
    elif "my tasks" in text or "my list" in text or "what do i have to do" in text:
        return get_tasks()
    elif "complete task" in text or "mark done" in text or "finished" in text:
        task = text.replace("complete task", "").replace("mark done", "").replace("finished", "").strip()
        return complete_task(task)
    elif "clear tasks" in text or "clear my list" in text:
        return clear_tasks()

    # --- APPS ---
    elif "open" in text and any(app in text for app in ["steam", "spotify", "discord", "vs code", "vscode", "opera", "brave", "github", "unity", "notepad", "calculator", "explorer", "claude"]):
        app = text.replace("open", "").strip()
        return open_app(app)
    elif "close" in text and any(app in text for app in ["steam", "spotify", "discord", "vs code", "opera", "brave", "github", "unity"]):
        for app in ["steam", "spotify", "discord", "vs code", "opera", "brave", "github", "unity"]:
            if app in text:
                return close_app(app)
        return "Which app do you want me to close?"

    # --- SPOTIFY ---
    elif "what song" in text or "current song" in text or "what's playing" in text or "whats playing" in text:
        return get_current_song()
    elif "pause" in text or "stop music" in text:
        return pause_music()
    elif "next song" in text or "skip song" in text or "next track" in text or "skip" in text:
        return next_song()
    elif "previous song" in text or "last song" in text or "previous track" in text or "go back" in text:
        return previous_song()
    # resume/start with no song name = always toggle, never search
    elif ("resume" in text or "start music" in text) and "open" not in text and "youtube" not in text:
        return toggle_playback()
    elif "my playlists" in text or "show playlists" in text or "list playlists" in text:
        return get_my_playlists()
    elif ("play playlist" in text or "play my playlist" in text) and "open" not in text:
        playlist = text.replace("play my playlist", "").replace("play playlist", "").replace("can you", "").replace("please", "").strip()
        return play_my_playlist(playlist)
    elif "play" in text and "open" not in text and "youtube" not in text:
        song = extract_song(text)
        if not song or song in ["", "music", "it", "the song", "a song", "the", "song"]:
            return toggle_playback()
        else:
            return play_song(song)

    # --- SYSTEM ---
    elif "set volume" in text or "volume to" in text:
        num = extract_number(text)
        if num:
            return set_volume(num)
        return "What volume level do you want?"
    elif "volume up" in text:
        return set_volume(80)
    elif "volume down" in text:
        return set_volume(30)
    elif "mute" in text:
        return set_volume(0)
    elif "what's the volume" in text or "current volume" in text:
        return get_volume()
    elif "set brightness" in text or "brightness to" in text:
        num = extract_number(text)
        if num:
            return set_brightness(num)
        return "What brightness level do you want?"
    elif "brightness up" in text:
        return set_brightness(80)
    elif "brightness down" in text:
        return set_brightness(30)
    elif "what's the brightness" in text or "current brightness" in text:
        return get_brightness()
    elif "battery" in text:
        return get_battery()
    elif "screenshot" in text:
        return take_screenshot()
    elif "system info" in text or "cpu" in text or "ram usage" in text:
        return get_system_info()

    # --- SEARCH ---
    elif "search for" in text or "look up" in text or "google" in text:
        query = text.replace("search for", "").replace("look up", "").replace("google", "").strip()
        return search_web(query)
    elif "youtube" in text and "search" in text:
        query = text.replace("search youtube for", "").replace("youtube", "").replace("search", "").strip()
        return search_youtube(query)
    elif "open website" in text or "go to" in text:
        url = text.replace("open website", "").replace("go to", "").strip()
        return open_website(url)

    # --- FALLBACK TO BRAIN ---
    else:
        return chat(user_input)


def conversation_loop():
    """
    Friday stays awake and keeps listening for follow-up commands.
    Goes back to sleep if:
      - You say a sleep command ("go to sleep", "that's all", etc.)
      - You say nothing twice in a row (timeout behaviour)
      - F4 is pressed again (toggle)
    """
    sleep_commands = [
        "go to sleep", "go to sleep friday", "that's all",
        "that's all friday", "sleep", "sleep friday",
        "you can sleep", "thanks friday", "thank you friday",
        "that will be all", "that will be all friday"
    ]

    shutdown_commands = [
        "goodbye friday", "bye friday", "shutdown friday", "turn off friday"
    ]

    print(f"Friday: Awake — say 'go to sleep', 'that's all', or press F4 to sleep")
    missed = 0
    _friday_awake.set()    # mark Friday as awake
    _f4_pressed.clear()    # clear any previous F4 press

    while True:
        # Check if F4 was pressed to toggle sleep
        if _f4_pressed.is_set():
            _f4_pressed.clear()
            speak("Going to sleep. Press F4 or say Friday whenever you need me!")
            _friday_awake.clear()
            return

        user_input = listen()

        # Check F4 again after listen() returns (in case pressed during listening)
        if _f4_pressed.is_set():
            _f4_pressed.clear()
            speak("Going to sleep. Press F4 or say Friday whenever you need me!")
            _friday_awake.clear()
            return

        # Nothing heard
        if user_input is None:
            missed += 1
            if missed >= 2:
                speak("Going back to sleep. Say Friday whenever you need me!")
                _friday_awake.clear()
                return
            else:
                speak("Still here, go ahead!")
            continue

        # Reset miss counter on successful input
        missed = 0
        print(f"You: {user_input}")
        text = user_input.lower()

        # Full shutdown
        if any(cmd in text for cmd in shutdown_commands):
            speak("Goodbye Boss! Have a great day!")
            exit()

        # Sleep command — go back to wake word mode
        if any(cmd in text for cmd in sleep_commands):
            speak("Going to sleep. Say Friday whenever you need me!")
            _friday_awake.clear()
            return

        # Handle the command
        response = handle_command(user_input)
        if response:
            speak(response)

        # Short cooldown so Friday's own voice doesn't get picked up
        time.sleep(1.5)


def _wait_for_activation(listen_for_wakeword):
    """
    Blocks until either:
    - The wake word is detected (voice), OR
    - F4 is pressed (hotkey)
    Runs wake word detection in a thread so F4 can interrupt it.
    """
    _f4_pressed.clear()
    wakeword_triggered = threading.Event()

    def _wakeword_thread():
        listen_for_wakeword()
        wakeword_triggered.set()

    t = threading.Thread(target=_wakeword_thread, daemon=True)
    t.start()

    # Wait for whichever comes first
    while not wakeword_triggered.is_set() and not _f4_pressed.is_set():
        time.sleep(0.05)

    if _f4_pressed.is_set():
        print("[Hotkey] Activated via F4")
    else:
        print("[Wake] Activated via wake word")


def run_friday():
    from wakeword import listen_for_wakeword

    speak("Friday is running in the background. Say 'Friday' or press F4 to wake me up!")

    while True:
        try:
            print("Friday: Sleeping... say 'Friday' or press F4 to wake me up!")

            # Wait for wake word OR F4 hotkey
            _wait_for_activation(listen_for_wakeword)

            # Wake up and enter conversation mode
            speak("Yes Boss?")

            # Stay in conversation until sleep command or timeout
            conversation_loop()

            # Flush stale audio so old chunks don't instantly re-trigger
            _flush_audio_queue()

            # Small gap before re-arming wake word
            time.sleep(1)

        except Exception as e:
            print(f"[Error] Something went wrong: {e}")
            time.sleep(1)
            continue


if __name__ == "__main__":
    run_friday()