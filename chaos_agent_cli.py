"""
Interactive CLI for ChaosAgent:
- Type free text to affect emotions.
- Load & run a .sn / .chaos file into context.
- View dreams, current emotions, symbols, and last action.
"""

from __future__ import annotations
import argparse
import os
from typing import Optional

from chaos_agent import ChaosAgent

BANNER = """\
CHAOS Agent CLI 🌌
Commands:
  :open <path>     Load a .sn/.chaos file into memory
  :dreams          Show current dream visions
  :emotions        Show active emotions and intensities
  :symbols         Show known symbols
  :action          Show the last action taken
  :clear           Clear narrative memory
  :help            Show this help
  :quit            Exit
Type free text to influence emotions (keyword triggers), Enter to commit.
"""

def read_file(path: str) -> Optional[str]:
    if not os.path.exists(path):
        print("File not found.")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description="CHAOS Agent REPL")
    parser.add_argument("--name", default="Concord")
    args = parser.parse_args()

    agent = ChaosAgent(args.name)
    print(BANNER)

    last_report = None
    buf = []
    while True:
        try:
            line = input("agent> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break

        if not line:
            text = "\n".join(buf).strip()
            buf.clear()
            if not text and not last_report:
                continue
            report = agent.step(text=text or None)
            last_report = report
            print(f"✓ action: {report.action}")
            print(f"✓ emotions: {report.emotions}")
            print(f"✓ dreams: {report.dreams[:2]}")
            continue

        if line.startswith(":"):
            parts = line.split(maxsplit=1)
            cmd = parts[0][1:]
            arg = parts[1] if len(parts) > 1 else ""

            if cmd == "open":
                src = read_file(arg)
                if src:
                    rep = agent.step(sn=src)
                    last_report = rep
                    print("✓ loaded and merged.")
            elif cmd == "dreams":
                rep = agent.step()
                print("\n".join(rep.dreams[:5]))
            elif cmd == "emotions":
                rep = agent.step()
                print(rep.emotions)
            elif cmd == "symbols":
                rep = agent.step()
                print(rep.symbols)
            elif cmd == "action":
                rep = agent.step()
                print(rep.action)
            elif cmd == "clear":
                agent.ctx.set_narrative("")
                print("✓ narrative cleared.")
            elif cmd == "help":
                print(BANNER)
            elif cmd in ("q", "quit", "exit"):
                print("bye.")
                break
            else:
                print("unknown command. try :help")
            continue

            # fallthrough never
        buf.append(line)

if __name__ == "__main__":
    main()
