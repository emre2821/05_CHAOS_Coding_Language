# chaos_logger.py

import datetime

class ChaosLogger:
    def __init__(self):
        self.logs = []

    def log(self, message: str):
        entry = f"[{datetime.datetime.now().isoformat()}] {message}"
        self.logs.append(entry)

    def log_symbol(self, name: str, value: str):
        self.log(f"SYMBOL: {name} = {value}")

    def log_emotion(self, emotion: str):
        self.log(f"EMOTION: {emotion}")

    def log_narrative(self, chaosfield: str):
        self.log(f"NARRATIVE: {chaosfield[:60]}...")

    def export(self):
        return "\n".join(self.logs)
