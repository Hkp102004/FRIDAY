from brain import chat
from speak import speak
from listen import listen
from skills.apps import open_app, close_app
from skills.system import set_volume, get_volume, set_brightness, get_brightness, get_battery, take_screenshot, get_system_info
from skills.search import search_web, search_youtube, open_website
from skills.news import get_full_briefing, get_gaming_news, get_ai_news, get_world_news
from skills.tasks import add_task, get_tasks, complete_task, clear_tasks
import re

def extract_number(text):
    numbers = re.findall(r'\d+', text)
    return numbers[0] if numbers else None

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
        app = text.replace("close", "").strip()
        return close_app(app)

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

def run_ada():
    speak("Hello Harsh! Ada is online and ready. How can I help you today?")

    while True:
        user_input = listen()

        if user_input is None:
            continue

        print(f"You: {user_input}")

        # Exit commands
        if any(word in user_input for word in ["goodbye ada", "bye ada", "shutdown ada", "turn off ada"]):
            speak("Goodbye Harsh! Have a great day!")
            break

        # Handle command or chat
        response = handle_command(user_input)
        speak(response)

if __name__ == "__main__":
    run_ada()