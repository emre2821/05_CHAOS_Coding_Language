"""
Shared memory for symbols, emotions, narrative.
"""


class ChaosContext:
    def __init__(self):
        self.memory = {
            "symbols": {},
            "emotions": [],
            "narrative": "",
        }

    def set_symbol(self, key: str, value: str) -> None:
        self.memory["symbols"][key] = value

    def add_emotion(self, emotion: str) -> None:
        self.memory["emotions"].append(emotion)

    def set_narrative(self, text: str) -> None:
        self.memory["narrative"] = text

    def get(self):  # type: ignore[override]
        return self.memory

    def reset(self) -> None:
        self.__init__()
