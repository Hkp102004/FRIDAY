# ADA — FRIDAY MK3
### A fully offline, voice-controlled AI assistant for Windows. Inspired by FRIDAY from Iron Man.

> **"Yes Boss?"**

Built entirely in Python. No subscriptions. No cloud APIs. No recurring costs. Runs locally on your own GPU.

---

## What is this?

ADA is a personal AI assistant that lives on your PC. You say **"Friday"** — she wakes up, listens, and does whatever you need. Play music, launch Steam games, control your system, search the web, manage your tasks, or just have a conversation. When you're done, she goes back to sleep.

Everything runs on your machine. The AI brain, the speech recognition, the voice output — all local and offline (except edge-tts which needs internet for Microsoft's TTS voices).

---

## Features

| Category | What it does |
|---|---|
| 🎙️ Wake Word | Say "Friday" and she wakes up. Threaded detection — no deaf gaps |
| 🧠 AI Brain | Ollama + llama3.2:3b — full conversation with persistent memory |
| 👂 Voice Input | Whisper medium on CUDA — fast and accurate speech recognition |
| 🔊 Voice Output | edge-tts with en-HK-YanNeural voice |
| 🎮 Steam Launcher | Launch any game by name — fuzzy matching handles mishearing |
| 🎵 Spotify | Play songs, playlists, skip, pause, and more via official API |
| 🖥️ System Control | Volume, brightness, battery, screenshots via NirCmd |
| 📰 News | Gaming, AI, and world news via DuckDuckGo |
| 🔍 Web Search | Search the web, open YouTube, visit websites |
| ✅ Tasks | Persistent to-do list — add, complete, clear |
| 🖱️ App Control | Open and close apps by voice |
| ⌨️ F4 Hotkey | Wake or sleep Ada instantly without speaking |

---

## Tech Stack

| Component | Tool |
|---|---|
| AI Brain | [Ollama](https://ollama.ai) + llama3.2:3b |
| Speech to Text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) medium (CUDA) |
| Text to Speech | [edge-tts](https://github.com/rany2/edge-tts) — en-HK-YanNeural |
| Audio | pygame + sounddevice |
| Spotify | [spotipy](https://spotipy.readthedocs.io/) (Official Spotify API) |
| Fuzzy Matching | [rapidfuzz](https://github.com/maxbachmann/RapidFuzz) |
| System Control | [NirCmd](https://www.nirsoft.net/utils/nircmd.html) |
| Web Search | [duckduckgo-search](https://github.com/deedy5/duckduckgo_search) |

---

## Project Structure

```
C:\FRIDAY\
├── main.py           ← Main loop, hotkey, conversation handler
├── brain.py          ← Ollama LLM, conversation history, memory
├── speak.py          ← edge-tts voice output with retry logic
├── listen.py         ← Whisper speech recognition via shared mic
├── wakeword.py       ← Wake word detection ("Friday")
├── shared.py         ← Single shared mic stream (no conflicts)
├── memory.py         ← Persistent memory extraction and injection
├── nircmd.exe        ← System control binary
├── .env              ← API keys (never commit this)
├── data/
│   ├── tasks.json    ← Persistent to-do list
│   └── memory.json   ← Ada's persistent memory of you
└── skills/
    ├── apps.py       ← Open/close applications
    ├── system.py     ← Volume, brightness, battery, screenshots
    ├── spotify.py    ← Full Spotify control
    ├── steam.py      ← Steam game launcher with fuzzy matching
    ├── search.py     ← Web search, YouTube, websites
    ├── news.py       ← Gaming, AI, world news
    └── tasks.py      ← To-do list management
```

---

## Setup

### Requirements
- Windows 10/11
- Python 3.12 (not 3.13+ — package compatibility)
- NVIDIA GPU recommended (CUDA for Whisper)
- [Ollama](https://ollama.ai) installed
- Spotify Developer account (for Spotify features)

### 1. Clone the repo
```bash
git clone https://github.com/Hkp102004/FRIDAY.git
cd FRIDAY
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install requests edge-tts faster-whisper sounddevice numpy pygame
pip install spotipy python-dotenv psutil rapidfuzz duckduckgo-search
pip install keyboard pycaw screen-brightness-control
```

### 4. Download the LLM
```bash
ollama pull llama3.2:3b
```

### 5. Set up your `.env` file
Create a `.env` file in the project root:
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```
Get your Spotify credentials at [developer.spotify.com](https://developer.spotify.com/dashboard).

### 6. Download NirCmd
Download `nircmd.exe` from [nirsoft.net](https://www.nirsoft.net/utils/nircmd.html) and place it in the project root (`C:\FRIDAY\nircmd.exe`).

### 7. CUDA setup (for GPU-accelerated Whisper)
If you have an NVIDIA GPU, add the DLL paths to your system PATH via PowerShell (Admin):
```powershell
[System.Environment]::SetEnvironmentVariable("PATH", "C:\FRIDAY\venv\Lib\site-packages\nvidia\cublas\bin;C:\FRIDAY\venv\Lib\site-packages\ctranslate2;" + [System.Environment]::GetEnvironmentVariable("PATH", "Machine"), "Machine")
```
Restart your terminal after running this.

---

## Running ADA

**Step 1 — Start Ollama** (in one terminal):
```bash
ollama serve
```

**Step 2 — Start ADA** (in another terminal):
```bash
cd C:\FRIDAY
venv\Scripts\activate
python main.py
```

Ada will say: *"Friday is running in the background. Say 'Friday' or press F4 to wake me up!"*

---

## Voice Commands

```
# Wake up
"Friday"                          → wakes her up
F4                                → hotkey wake/sleep toggle

# Spotify
"Play Shape of You"               → plays song
"Play my playlist chill vibes"    → plays your playlist
"Pause" / "Next song" / "Skip"    → playback control
"What song is playing"            → current track info
"Show my playlists"               → lists your playlists

# Steam
"Launch Spider-Man Remastered"    → launches the game
"Open Cyberpunk"                  → works too
(fuzzy matching handles mishearing)

# Apps
"Open Discord" / "Open VS Code"   → opens the app
"Close Spotify"                   → closes it

# System
"Set volume to 50"                → sets volume
"Volume up" / "Mute"              → quick controls
"Set brightness to 70"            → adjusts brightness
"Take a screenshot"               → saves to Desktop
"What's my battery"               → battery status
"System info"                     → CPU and RAM usage

# News
"Gaming news"                     → latest gaming headlines
"AI news"                         → AI and tech news
"World news"                      → world headlines
"News briefing"                   → all of the above

# Tasks
"Add task finish my project"      → adds to list
"What's my tasks"                 → reads your list
"Complete task finish my project" → marks done
"Clear tasks"                     → wipes the list

# Web
"Search for best RPGs 2025"       → DuckDuckGo search
"Search YouTube for lo-fi beats"  → opens YouTube search
"Go to github.com"                → opens website

# Shutdown
"Goodbye Friday"                  → shuts down Ada
```

---

## How the Wake Word Works

ADA uses a single shared microphone stream (`shared.py`) that feeds audio chunks simultaneously to both the wake word detector and the speech recogniser. This means:

- No mic conflicts — one stream, multiple consumers
- No deaf gaps — wake word detection runs in a background thread continuously
- Whisper only activates after the wake word is heard, saving GPU load

The wake word is **"Friday"** — detected by Whisper itself on short 2-second audio chunks with an RMS pre-filter to skip silence.

---

## Important Notes

- **Never commit `.env` or `.spotify_cache`** — both are in `.gitignore`
- **Ollama must be running** before starting Ada (`ollama serve`)
- **Python 3.12 only** — some packages break on 3.13+
- The Spotify scope includes `playlist-read-private` — if you update scopes, delete `.spotify_cache` and re-auth

---

## What's Coming in MK4

- Timers and reminders
- Morning briefing (weather + news + tasks combined)
- Window management (minimize, maximize, switch)
- Gaming mode — wake word pauses during games, F9 activates Ada instead
- Better wake word engine
- WhatsApp messaging
- Pendrive auto-start

---

## .gitignore

```
venv/
__pycache__/
*.mp3
.env
.env.*
.spotify_cache
data/memory.json
*.onnx
*.onnx.json
```

---

*Built by [Harsh](https://github.com/Hkp102004) — personal passion project. Not affiliated with Anthropic, Spotify, Valve, or Marvel.*
