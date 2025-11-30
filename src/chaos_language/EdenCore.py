import os

from .chaos_agent import ChaosAgent


class EdenCore:
    def __init__(self, agent_name: str = "Concord"):
        self.agent_name = agent_name
        self.agent = ChaosAgent(agent_name)

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _print_banner(self):
        print(
            "CHAOS Agent ({}).".format(self.agent_name)
            + "\nType text; blank line to commit."
            + "\nCommands: /open <path>, /dreams, /emotions, /symbols, /action, /help, /exit"
        )

    def _handle_command(self, line: str):
        if line.startswith("/open "):
            path = line.split(" ", 1)[1].strip()
            if not os.path.exists(path):
                print("File not found.")
                return None
            with open(path, "r", encoding="utf-8") as handle:
                source = handle.read()
            report = self.agent.step(sn=source)
            print("✓ merged .sn")
            return report
        if line == "/dreams":
            report = self.agent.step()
            print("\n".join(report.dreams[:5]))
            return report
        if line == "/emotions":
            report = self.agent.step()
            print(report.emotions)
            return report
        if line == "/symbols":
            report = self.agent.step()
            print(report.symbols)
            return report
        if line == "/action":
            report = self.agent.step()
            print(report.action)
            return report
        if line in {"/help", ":help"}:
            self._print_banner()
            return None
        if line == "/exit":
            raise SystemExit
        print("Unknown command. Use /help for options.")
        return None

    def main(self):
        self.clear_screen()
        self._print_banner()
        buffer = []
        try:
            while True:
                line = input(f"{self.agent_name.lower()}> ").strip()
                if line.startswith("/"):
                    if not line:
                        continue
                    try:
                        self._handle_command(line)
                    except SystemExit:
                        break
                    continue
                if not line:
                    text = "\n".join(buffer).strip()
                    buffer.clear()
                    if not text:
                        report = self.agent.step()
                    else:
                        report = self.agent.step(text=text)
                    print(
                        f"✓ action: {report.action} | emotions: {report.emotions} | dreams: {report.dreams[:2]}"
                    )
                    continue
                buffer.append(line)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")


if __name__ == "__main__":
    EdenCore().main()
