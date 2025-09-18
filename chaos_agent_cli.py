"""
Interactive CLI for ChaosAgent.
"""
import argparse
import os
from typing import Optional

from chaos_agent import ChaosAgent

BANNER = """\
CHAOS Agent CLI 🌌
:open <path>   load .sn/.chaos file
:dreams        show visions
:emotions      active emotions
:symbols       known symbols
:action        last action
:clear         clear narrative
:help          help
:quit          exit
"""


def _read(path: str) -> Optional[str]:
    if not os.path.exists(path):
        print("File not found.")
        return None
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def main():
    parser = argparse.ArgumentParser(description="CHAOS Agent REPL")
    parser.add_argument("--name", default="Concord")
    args = parser.parse_args()

    agent = ChaosAgent(args.name)
    print(BANNER)
    buf: list[str] = []
    last = None

    while True:
        try:
            line = input("agent> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break

        if line.startswith(":"):
            cmd, *rest = line[1:].split(maxsplit=1)
            arg = rest[0] if rest else ""
            if cmd == "open":
                src = _read(arg)
                if src:
                    last = agent.step(sn=src)
                    print("✓ merged.")
            elif cmd == "dreams":
                last = agent.step()
                print("\n".join(last.dreams[:5]))
            elif cmd == "emotions":
                last = agent.step()
                print(last.emotions)
            elif cmd == "symbols":
                last = agent.step()
                print(last.symbols)
            elif cmd == "action":
                last = agent.step()
                print(last.action)
            elif cmd == "clear":
                agent.ctx.set_narrative("")
                print("✓ cleared.")
            elif cmd in ("help", "h", "?"):
                print(BANNER)
            elif cmd in ("quit", "exit", "q"):
                print("bye.")
                break
            else:
                print("unknown. :help")
            continue

        if not line:
            text = "\n".join(buf).strip()
            buf.clear()
            if not text and not last:
                continue
            last = agent.step(text=text or None)
            print(f"✓ action: {last.action} | emotions: {last.emotions} | dreams: {last.dreams[:2]}")
            continue

        buf.append(line)


if __name__ == "__main__":
    main()
