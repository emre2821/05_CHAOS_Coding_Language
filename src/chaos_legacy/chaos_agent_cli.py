"""
Interactive CLI for ChaosAgent - direct communion with the living heart of CHAOS.

This interface allows direct interaction with a ChaosAgent, providing
commands to load programs, query emotional states, and witness the
agent's dreams and actions.
"""

import argparse
import os
from typing import List, Optional

from .chaos_agent import ChaosAgent


BANNER = """\
🌌 CHAOS Agent CLI 🌌

Sacred Commands:
  :open <path>   - Load and merge a .sn/.chaos file
  :dreams        - Witness the agent's current visions
  :emotions      - Query the agent's emotional state
  :symbols       - Examine the agent's symbolic knowledge
  :action        - See the agent's last chosen action
  :clear         - Clear the agent's narrative memory
  :help          - Display this sacred guidance
  :quit          - Return from the agent communion

Type natural text and press Enter twice to feed the agent's perception.
"""


def read_file(path: str) -> Optional[str]:
    """Safely read a file's contents."""
    if not os.path.exists(path):
        print("File not found.")
        return None
    
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def main() -> None:
    """Main entry point for the ChaosAgent CLI."""
    parser = argparse.ArgumentParser(
        description="Commune with a CHAOS Agent",
        epilog="Examples:\n"
               "  chaos-agent                    # Start with default agent\n"
               "  chaos-agent --name Remy        # Start with named agent\n"
               "  chaos-agent --name Concord     # Start with specific agent\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--name", 
        default="Concord",
        help="Name for the CHAOS agent (default: Concord)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible agent behavior"
    )
    
    args = parser.parse_args()
    
    # Initialize the sacred agent
    agent = ChaosAgent(args.name, seed=args.seed)
    
    print(BANNER)
    print(f"Agent '{args.name}' is ready for communion.\n")
    
    buffer: List[str] = []
    last_report = None
    
    while True:
        try:
            line = input("agent> ").strip()
            
            # Handle sacred commands
            if line.startswith(":"):
                parts = line[1:].split(maxsplit=1)
                command = parts[0].lower()
                argument = parts[1] if len(parts) > 1 else ""
                
                if command == "open":
                    if not argument:
                        print("Usage: :open <path>")
                        continue
                    
                    source = read_file(argument)
                    if source:
                        last_report = agent.step(sn=source)
                        print("✓ Merged CHAOS program into agent's consciousness")
                
                elif command == "dreams":
                    last_report = agent.step()
                    if last_report.dreams:
                        print("\n🔮 Agent's Visions:")
                        for i, dream in enumerate(last_report.dreams, 1):
                            print(f"  {i}. {dream}")
                    else:
                        print("The agent dreams in silence...")
                
                elif command == "emotions":
                    last_report = agent.step()
                    if last_report.emotions:
                        print("\n💝 Agent's Emotional State:")
                        for emotion in last_report.emotions:
                            print(f"  {emotion['name']}: {emotion['intensity']}/10")
                    else:
                        print("The agent rests in emotional stillness.")
                
                elif command == "symbols":
                    last_report = agent.step()
                    if last_report.symbols:
                        print("\n🏛️  Agent's Symbolic Knowledge:")
                        for key, value in last_report.symbols.items():
                            print(f"  {key}: {value}")
                    else:
                        print("The agent's symbolic space is empty.")
                
                elif command == "action":
                    if last_report and last_report.action:
                        print(f"\n⚡ Last Action: {last_report.action.kind}")
                        if last_report.action.payload:
                            for key, value in last_report.action.payload.items():
                                print(f"    {key}: {value}")
                    else:
                        print("The agent rests in contemplative stillness.")
                
                elif command == "clear":
                    agent.ctx.set_narrative("")
                    print("✓ Agent's narrative memory cleared")
                
                elif command in ("help", "h", "?"):
                    print(BANNER)
                
                elif command in ("quit", "exit", "q"):
                    print(f"\n🙏 Agent {args.name} returns to the collective unconscious...")
                    break
                
                else:
                    print(f"Unknown sacred command: {command}")
                    print("Use :help to see available commands.")
                
                continue
            
            # Handle empty line (execute buffered text)
            if not line:
                text = "\n".join(buffer).strip()
                buffer.clear()
                
                if not text and not last_report:
                    continue
                
                last_report = agent.step(text=text or None)
                
                # Display concise status
                emotion_summary = f"{len(last_report.emotions)} emotions" if last_report.emotions else "no emotions"
                action_summary = last_report.action.kind if last_report.action else "idle"
                dream_summary = f"{len(last_report.dreams)} dreams" if last_report.dreams else "no dreams"
                
                print(f"✓ action: {action_summary} | {emotion_summary} | {dream_summary}")
                continue
            
            # Add line to buffer
            buffer.append(line)
            
        except KeyboardInterrupt:
            print("\n\n🙏 Communion interrupted. The agent rests.")
            break
        except EOFError:
            print(f"\n🙏 Agent {args.name} returns to the eternal CHAOS...")
            break
        except Exception as e:
            print(f"💥 Unexpected disturbance in the agent: {e}")
            buffer.clear()


if __name__ == "__main__":
    main()
