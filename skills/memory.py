import json
import os
import re

MEMORY_FILE = "data/memory.json"

def ensure_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)

def load_memories():
    ensure_file()
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memories(memories):
    ensure_file()
    with open(MEMORY_FILE, "w") as f:
        json.dump(memories, f, indent=2)

def remember(fact):
    """Manually save a fact to memory."""
    fact = fact.strip()
    if not fact:
        return "What should I remember?"
    memories = load_memories()
    # Avoid exact duplicates
    if fact.lower() in [m["fact"].lower() for m in memories]:
        return "I already know that!"
    memories.append({"fact": fact, "source": "manual"})
    save_memories(memories)
    return f"Got it, I'll remember that!"

def forget(fact):
    """Remove a fact from memory by keyword match."""
    fact = fact.strip().lower()
    memories = load_memories()
    original_count = len(memories)
    memories = [m for m in memories if fact not in m["fact"].lower()]
    if len(memories) < original_count:
        save_memories(memories)
        return "Done, I've forgotten that!"
    return "I don't have anything like that in my memory."

def get_memories():
    """Return all memories as a readable string."""
    memories = load_memories()
    if not memories:
        return "I don't have anything saved in my memory yet!"
    lines = [f"- {m['fact']}" for m in memories]
    return "Here's what I remember:\n" + "\n".join(lines)

def clear_memories():
    """Wipe all memories."""
    save_memories([])
    return "Memory cleared!"

def get_memory_context():
    """
    Returns a short string to inject into the system prompt.
    Called by brain.py on every chat call.
    """
    memories = load_memories()
    if not memories:
        return ""
    lines = [m["fact"] for m in memories]
    return "Things you remember about Hekey:\n" + "\n".join(f"- {l}" for l in lines)

# ── Auto memory extraction ─────────────────────────────────────────────────
# Looks for obvious preference/fact patterns in what the user says
# and saves them automatically without needing an extra Ollama call

AUTO_PATTERNS = [
    # favourite things
    (r"my fav(?:ou?rite)? (\w+) is (.+)", "Hekey's favourite {0} is {1}"),
    (r"i (?:really )?love (.+)", "Hekey loves {0}"),
    (r"i (?:really )?like (.+)", "Hekey likes {0}"),
    (r"i (?:really )?hate (.+)", "Hekey dislikes {0}"),
    (r"i don'?t like (.+)", "Hekey dislikes {0}"),
    # currently playing / doing
    (r"i(?:'m| am) playing (.+)", "Hekey is currently playing {0}"),
    (r"i(?:'m| am) working on (.+)", "Hekey is working on {0}"),
    # personal facts
    (r"my name is (\w+)", "Hekey's preferred name is {0}"),
    (r"i(?:'m| am) (\d+) years old", "Hekey is {0} years old"),
    (r"i(?:'m| am) from (.+)", "Hekey is from {0}"),
    (r"i(?:'m| am) a (?:student|developer|designer|engineer|gamer|programmer) (?:at|from)? ?(.+)?", "Hekey is a {0}"),
]

def auto_extract(user_message):
    """
    Scans user message for obvious facts and saves them automatically.
    Silent — doesn't return anything to the user.
    """
    text = user_message.lower().strip()
    memories = load_memories()
    existing = [m["fact"].lower() for m in memories]

    for pattern, template in AUTO_PATTERNS:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            # Fill template with matched groups
            fact = template
            for i, g in enumerate(groups):
                if g:
                    fact = fact.replace("{" + str(i) + "}", g.strip())
            # Clean up any unfilled placeholders
            fact = re.sub(r"\{.\}", "", fact).strip()
            if fact and fact.lower() not in existing:
                memories.append({"fact": fact, "source": "auto"})
                existing.append(fact.lower())
                print(f"[Memory] Auto-saved: {fact}")

    save_memories(memories)