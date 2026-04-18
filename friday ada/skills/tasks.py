import json
import os
from datetime import datetime

TASKS_FILE = "data/tasks.json"

def ensure_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)

def load_tasks():
    ensure_file()
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    ensure_file()
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(task_text):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "task": task_text,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save_tasks(tasks)
    return f"Added to your list: {task_text}!"

def get_tasks():
    tasks = load_tasks()
    if not tasks:
        return "Your to-do list is empty!"
    
    pending = [t for t in tasks if not t["done"]]
    done = [t for t in tasks if t["done"]]
    
    response = ""
    if pending:
        response += f"You have {len(pending)} pending tasks:\n"
        for t in pending:
            response += f"- {t['task']}\n"
    if done:
        response += f"\n{len(done)} completed tasks:\n"
        for t in done:
            response += f"✓ {t['task']}\n"
    return response

def complete_task(task_text):
    tasks = load_tasks()
    for t in tasks:
        if task_text.lower() in t["task"].lower():
            t["done"] = True
            save_tasks(tasks)
            return f"Marked as done: {t['task']}!"
    return f"Couldn't find task: {task_text}"

def clear_tasks():
    save_tasks([])
    return "All tasks cleared!"

if __name__ == "__main__":
    print(add_task("Test Ada's task system"))
    print(get_tasks())