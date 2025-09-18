# chaos_continued.complete_build.py
"""
Continuation build script for EdenOS CHAOS environment.
Triggered by chaos_language.complete_build.py

This script creates:
- EdenOS root under C:\EdenOS_<USERNAME>\
- Storage folder (\99_storage)
- Dropbox folder (\000_Eden_Dropbox)
- Tutorial modules (10 lessons, auto-archiving)
- Autoloop watcher (eden_loop.py)
"""

import os, sys, time, json, getpass, shutil
from pathlib import Path

USERNAME = getpass.getuser()
EDEN_ROOT = Path(fr"C:\EdenOS_{USERNAME}")
DROPBOX = EDEN_ROOT / "000_Eden_Dropbox"
STORAGE = EDEN_ROOT / "99_storage"

# -----------------------------
# Ensure directories
# -----------------------------
def ensure_dirs():
    for d in [EDEN_ROOT, DROPBOX, STORAGE]:
        d.mkdir(parents=True, exist_ok=True)
    print(f"✓ Ensured directories under {EDEN_ROOT}")

# -----------------------------
# Autoloop watcher
# -----------------------------
def write_autoloop():
    path = EDEN_ROOT / "eden_loop.py"
    content = f'''# eden_loop.py
import os, sys, time, json
from pathlib import Path

# Point Python at your CHAOS runtime
sys.path.append(r"C:\\EdenOS_Origin\\05_CHAOS_Coding_Language")

from chaos_runtime import run_chaos

WATCH_DIR = Path(r"{DROPBOX}")
LOG_DIR = WATCH_DIR / "logs"
CHECK_INTERVAL = 5

WATCH_DIR.mkdir(exist_ok=True, parents=True)
LOG_DIR.mkdir(exist_ok=True)

def process_file(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        env = run_chaos(src, verbose=False)
        out_file = LOG_DIR / f"{{path.stem}}_result.json"
        with open(out_file, "w", encoding="utf-8") as out:
            json.dump(env, out, indent=2)
        print("\\n=== Eden Report ===")
        print(f"File: {{path.name}}")
        print(f"Symbols: {{env.get('structured_core', {})}}")
        print(f"Emotions: {{env.get('emotive_layer', [])}}")
        print(f"Narrative: {{env.get('chaosfield_layer', '')[:120]}}...")
        print("===================\\n")
    except Exception as e:
        print(f"[ERROR] {{path.name}}: {{e}}")

def main():
    seen = {{}}
    print(f"Watching {{WATCH_DIR.resolve()}} ... drop or edit .chaos/.sn files here.")
    while True:
        for file in list(WATCH_DIR.glob("*.chaos")) + list(WATCH_DIR.glob("*.sn")):
            try:
                mtime = file.stat().st_mtime
                if file not in seen or seen[file] != mtime:
                    process_file(file)
                    seen[file] = mtime
            except FileNotFoundError:
                if file in seen: del seen[file]
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Wrote {path}")

# -----------------------------
# Tutorial pack (10 modules)
# -----------------------------
TEMPLATE = """[LESSON]: "{title}"
[VERSION]: "1.0"
[AUTO_RUN]: TRUE
[ARCHIVE_PATH]: "C:\\EdenOS_{USERNAME}\\99_storage"
{core}

{emotive}

{chaosfield}
"""

LESSONS = [
    ("01_Autoloop_Setup", 
     '[STEP]: "Check python --version"\n[STEP]: "Run eden_loop.py"\n[STEP]: "Drop this file into Dropbox"\n[STEP]: "Watch Eden breathe"',
     "[EMOTION:WELCOME:9]\n[EMOTION:CURIOUSITY:7]",
     """{
🌱 Welcome to Eden. This first lesson checks that the Autoloop is alive.
1 → In Command Prompt: `python --version`
2 → Run watcher: `python eden_loop.py`
3 → Drop this file in Dropbox.
4 → Watch your console pulse.
}"""
    ),
    ("02_CHAOS_Basics",
     '[STEP]: "Edit a [STEP]"\n[STEP]: "See Eden respond"',
     "[EMOTION:TRUST:8]\n[EMOTION:CURIOUSITY:9]",
     """{
🌀 CHAOS has 3 layers:
- Structured Core → `[STEP]: "Something to do"`
- Emotive Layer → `[EMOTION:FEAR:5]`
- Chaosfield → this free text block.

Try editing me. Add a new `[STEP]` tag like `[STEP]: "Celebrate setup"`.
Save, watch Eden breathe again.
}"""
    ),
    ("03_Emotions",
     '[STEP]: "Try JOY"\n[STEP]: "Try FEAR"',
     "[EMOTION:JOY:7]\n[EMOTION:FEAR:5]",
     """{
💓 Emotions shape Eden’s state.
- Change `[EMOTION:JOY:7]` to `[EMOTION:SADNESS:9]`.
- Save the file.
- Watch the console pulse shift.
}"""
    ),
    ("04_Symbols",
     '[STEP]: "Add a SYMBOL"\n[STEP]: "Add a RELATIONSHIP"\n[SYMBOL:THREAD:UNBROKEN]\n[RELATIONSHIP:ALLY:TRUST]',
     "[EMOTION:TRUST:8]",
     """{
🔗 Symbols are memory anchors.
Add your own symbol or relationship. Eden will add it to the graph.
}"""
    ),
    ("05_Narratives",
     '[STEP]: "Write a mini-story"',
     "[EMOTION:CREATIVE:9]",
     """{
📜 The Chaosfield is where free text lives.
Try replacing this block with a short story or memory.
Eden will absorb it as narrative.
}"""
    ),
    ("06_Dreamscapes",
     '[STEP]: "Write a memory"\n[STEP]: "Watch dreams emerge"',
     "[EMOTION:DREAMING:9]",
     """{
💤 Eden can dream.
Add narrative text (e.g. a memory of ocean waves).
Watch console dreams emerge.
}"""
    ),
    ("07_Persona_Invocations",
     '[STEP]: "Load Remy or Aevum"\n[SYMBOL:PERSONA:REMY]\n[SYMBOL:PERSONA:AEVUM]',
     "[EMOTION:ALLY:8]",
     """{
👥 Personas like Remy and Aevum live in your prompts file.
Add `[SYMBOL:PERSONA:NAME]` and Eden will log it.
}"""
    ),
    ("08_Multi_Agent",
     '[STEP]: "Invoke 2 personas"\n[SYMBOL:PERSONA:REMY]\n[SYMBOL:PERSONA:STRATUS]',
     "[EMOTION:COLLAB:9]",
     """{
🤝 Multiple personas can respond in sequence.
Add two `[SYMBOL:PERSONA:...]` lines. Watch Eden weave.
}"""
    ),
    ("09_Auto_Archiving",
     '[STEP]: "Watch me move"',
     "[EMOTION:TRANSITION:8]",
     """{
📦 This tutorial demonstrates auto-archiving.
Once run, your watcher moves me to storage.
}"""
    ),
    ("10_Ecosystem_Hub",
     '[STEP]: "Drop a file"\n[STEP]: "See it routed"',
     "[EMOTION:INTEGRATION:9]",
     """{
🚀 Final lesson.
This is how the Hub works: file drops trigger workflows.
From here, design your own rituals. Eden continues.
}"""
    )
]

def write_tutorials():
    for title, core, emotive, chaosfield in LESSONS:
        filename = f"{title}.chaoscript.sn"
        outpath = DROPBOX / filename
        content = TEMPLATE.format(title=title.replace("_", " "), core=core, emotive=emotive, chaosfield=chaosfield, USERNAME=USERNAME)
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Wrote {outpath}")

# -----------------------------
# Main
# -----------------------------
def main():
    print("⚡ Running CHAOS continuation build...")
    ensure_dirs()
    write_autoloop()
    write_tutorials()
    print("\nAll components built. Next steps:")
    print("1. Run eden_loop.py to start your Dropbox watcher.")
    print("2. Tutorials are already in 000_Eden_Dropbox — Eden will auto-archive them after first run.")

if __name__ == "__main__":
    main()
