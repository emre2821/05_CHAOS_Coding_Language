"""
EdenCore - The heart of the CHAOS ecosystem with daemon management.

This is the master coordinator that manages multiple CHAOS agents and
provides a unified interface to the symbolic-emotional computation system.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from .chaos_agent import ChaosAgent


class EdenCore:
    """
    The master coordinator of the CHAOS ecosystem.
    
    EdenCore manages multiple daemon processes and provides a unified
    interface to the symbolic-emotional computation capabilities of CHAOS.
    """
    
    def __init__(self, log_file: str = "edencore_log.json") -> None:
        """
        Initialize the EdenCore coordinator.
        
        Args:
            log_file: File to log daemon activities
        """
        self.log_file = log_file
        
        # Available daemon processes in the CHAOS pantheon
        self.daemons: Dict[str, Tuple[str, Any]] = {
            "1": ("CHAOS Agent (Concord)", "CHAOS_AGENT"),
            "2": ("Eyes of Echo", self._create_stub_daemon("Eyes of Echo")),
            "3": ("Threadstep", self._create_stub_daemon("Threadstep")),
            "4": ("Markbearer", self._create_stub_daemon("Markbearer")),
            "5": ("Scriptum", self._create_stub_daemon("Scriptum")),
            "6": ("Rook", self._create_stub_daemon("Rook")),
            "7": ("Glimmer", self._create_stub_daemon("Glimmer")),
            "8": ("Muse Jr.", self._create_stub_daemon("Muse Jr.")),
            "9": ("Toto", self._create_stub_daemon("Toto")),
            "10": ("PulsePause", self._create_stub_daemon("PulsePause")),
        }
    
    def _create_stub_daemon(self, name: str) -> Any:
        """Create a stub daemon for unavailable components."""
        class StubDaemon:
            def __init__(self, daemon_name: str):
                self.name = daemon_name
            
            def main(self) -> None:
                print(f"🌸 The {self.name} daemon is not installed in this CHAOS distribution.")
                print("   This is a placeholder for future ecosystem expansion.")
                input("\nPress Enter to return to EdenCore...")
        
        return StubDaemon(name)
    
    def log_action(self, daemon_name: str) -> None:
        """Log a daemon activation."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "daemon": daemon_name,
            "action": "activated"
        }
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(entry, f)
                f.write("\n")
        except Exception:
            pass  # Silent failure for logging
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")
    
    def _run_chaos_agent(self) -> None:
        """Run the interactive CHAOS Agent interface."""
        agent = ChaosAgent("Concord")
        self.clear_screen()
        
        print("🌌 CHAOS Agent (Concord)")
        print("Type text; blank line to commit.")
        print("Commands: /open <path>, /dreams, /emotions, /symbols, /action, /exit")
        
        buffer = []
        last_report = None
        
        while True:
            try:
                line = input("concord> ").strip()
                
                if line == "/exit":
                    break
                
                if line.startswith("/open "):
                    path = line.split(" ", 1)[1].strip()
                    if not os.path.exists(path):
                        print("File not found.")
                        continue
                    
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            source = f.read()
                        last_report = agent.step(sn=source)
                        print("✓ merged .sn")
                    except Exception as e:
                        print(f"Error: {e}")
                    continue
                
                if line == "/dreams":
                    last_report = agent.step()
                    if last_report.dreams:
                        print("\n".join(last_report.dreams[:5]))
                    continue
                
                if line == "/emotions":
                    last_report = agent.step()
                    print(last_report.emotions)
                    continue
                
                if line == "/symbols":
                    last_report = agent.step()
                    print(last_report.symbols)
                    continue
                
                if line == "/action":
                    last_report = agent.step()
                    print(last_report.action)
                    continue
                
                if not line:
                    text = "\n".join(buffer).strip()
                    buffer.clear()
                    
                    if not text and not last_report:
                        continue
                    
                    last_report = agent.step(text=text or None)
                    
                    emotion_count = len(last_report.emotions) if last_report.emotions else 0
                    dream_count = len(last_report.dreams) if last_report.dreams else 0
                    action_name = last_report.action.kind if last_report.action else "idle"
                    
                    print(f"✓ action: {action_name} | emotions: {emotion_count} | dreams: {dream_count[:2]}")
                    continue
                
                buffer.append(line)
                
            except (EOFError, KeyboardInterrupt):
                print("\nExiting CHAOS Agent.")
                break
    
    def main(self) -> None:
        """Run the main EdenCore interface."""
        while True:
            self.clear_screen()
            
            print("\n🌌 EdenCore: Your CHAOS Pantheon 🌌\n")
            
            # Display available daemons
            for key, (name, _) in self.daemons.items():
                print(f"{key}. {name}")
            
            print(f"{len(self.daemons) + 1}. Exit EdenCore")
            
            choice = input(f"\nChoose a daemon (1-{len(self.daemons) + 1}): ").strip()
            
            if choice == str(len(self.daemons) + 1):
                print("\n🙏 EdenCore rests. You are enough.")
                break
            
            if choice in self.daemons:
                daemon_name, daemon = self.daemons[choice]
                self.log_action(daemon_name)
                self.clear_screen()
                
                if daemon == "CHAOS_AGENT":
                    self._run_chaos_agent()
                else:
                    try:
                        daemon.main()
                    except Exception as e:
                        print(f"💥 Daemon '{daemon_name}' encountered an error: {e}")
                        input("\nPress Enter to continue...")
            else:
                print("\n💫 Choose wisely, seeker. Try again.")
                input("\nPress Enter to continue...")


def main() -> None:
    """Entry point for EdenCore."""
    try:
        EdenCore().main()
    except KeyboardInterrupt:
        print("\n\n🙏 EdenCore interrupted. The CHAOS ecosystem rests.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 EdenCore encountered an error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()