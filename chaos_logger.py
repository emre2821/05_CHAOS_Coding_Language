"""
Timestamped runtime logger for symbols, emotions, narrative.
"""
import datetime


class ChaosLogger:
    def __init__(self):
        self.logs = []

    def log(self, message: str) -> None:
        entry = f"[{datetime.datetime.now().isoformat()}] {message}"
        self.logs.append(entry)

    def log_symbol(self, name: str, value: str) -> None:
        self.log(f"SYMBOL: {name} = {value}")

    def log_emotion(self, emotion: str) -> None:
        self.log(f"EMOTION: {emotion}")

    def log_narrative(self, chaosfield: str) -> None:
        self.log(f"NARRATIVE: {chaosfield[:60]}...")

    def export(self) -> str:
        return "\n".join(self.logs)
