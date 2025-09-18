import json
import os
from datetime import datetime

# Existing imports were referencing external daemons; keep if available:
try:
    from Eyes_of_Echo import EyesOfEcho
    from Threadstep import Threadstep
    from Markbearer import Markbearer
    from Scriptum import Scriptum
    from Rook import Rook
    from Glimmer import Glimmer
    from MuseJr import MuseJr
    from Toto import Toto
    from PulsePause import PulsePause
except Exception:
    # Soft-fallback stubs (why: so this menu still runs without those files)
    class _Stub:
        def main(self): print("Stub daemon: not installed.")
    EyesOfEcho = Threadstep = Markbearer = Scriptum = Rook = Glimmer = MuseJr = Toto = PulsePause = _Stub

# NEW: CHAOS Agent integration
from chaos_agent import ChaosAgent

class EdenCore:
    def __init__(self):
        self.log_file = "edencore_log.json"
        self.daemons = {
            "1": ("Eyes of Echo", EyesOfEcho()),
            "2": ("Threadstep", Threadstep()),
            "3": ("Markbearer", Markbearer()),
            "4": ("Scriptum", Scriptum()),
            "5": ("Rook", Rook()),
            "6": ("Glimmer", Glimmer()),
            "7": ("Muse Jr.", MuseJr()),
            "8": ("Toto", Toto()),
            "9": ("PulsePause", PulsePause()),
            "10": ("CHAOS Agent (Concord)", "CHAOS_AGENT"),  # special case
        }

    def log_action(self, daemon_name):
        entry = {"timestamp": str(datetime.now()), "daemon": daemon_name}
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(entry, f)
                f.write("\n")
        except Exception:
            pass

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _run_chaos_agent(self):
        agent = ChaosAgent("Concord")
        self.clear_screen()
        print("CHAOS Agent (Concord)\n")
        print("Type text to influence emotions. Enter blank line to commit.")
        print("Commands: /open <path>, /dreams, /emotions, /symbols, /action, /exit")
        buf = []
        last = None
        while True:
            try:
                line = input("concord> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break

            if line == "/exit":
                break
            if line.startswith("/open "):
                path = line.split(" ", 1)[1].strip()
                if not os.path.exists(path):
                    print("File not found.")
                    continue
                with open(path, "r", encoding="utf-8") as f:
                    src = f.read()
                last = agent.step(sn=src)
                print("✓ merged .sn into context.")
                continue
            if line == "/dreams":
                last = agent.step()
                print("\n".join(last.dreams[:5]))
                continue
            if line == "/emotions":
                last = agent.step()
                print(last.emotions)
                continue
            if line == "/symbols":
                last = agent.step()
                print(last.symbols)
                continue
            if line == "/action":
                last = agent.step()
                print(last.action)
                continue

            if not line:
                text = "\n".join(buf).strip()
                buf.clear()
                last = agent.step(text=text or None)
                print(f"✓ action: {last.action}")
                print(f"✓ emotions: {last.emotions}")
                print(f"✓ dreams: {last.dreams[:2]}")
            else:
                buf.append(line)

    def main(self):
        while True:
            self.clear_screen()
            print("\n🌌 EdenCore: Your CHAOS Pantheon 🌌\n")
            for k, (name, _) in self.daemons.items():
                print(f"{k}. {name}")
            print(f"{len(self.daemons) + 1}. Exit")
            choice = input("\nChoose a daemon (1-{}): ".format(len(self.daemons) + 1)).strip()
            if choice == str(len(self.daemons) + 1):
                print("\nEdenCore rests. You are enough.")
                break
            if choice in self.daemons:
                name, daemon = self.daemons[choice]
                self.log_action(name)
                self.clear_screen()
                if daemon == "CHAOS_AGENT":
                    self._run_chaos_agent()
                else:
                    try:
                        daemon.main()
                    except Exception as e:
                        print(f"Daemon '{name}' failed: {e}")
                        input("\nPress Enter to continue...")
            else:
                print("\nPick a number, love. Try again.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    core = EdenCore()
    core.main()
