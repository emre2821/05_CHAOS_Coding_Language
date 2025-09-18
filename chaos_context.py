# chaos_context.py

class ChaosContext:
    def __init__(self):
        self.memory = {
            "symbols": {},
            "emotions": [],
            "narrative": ""
        }

    def set_symbol(self, key: str, value: str):
        self.memory["symbols"][key] = value

    def add_emotion(self, emotion: str):
        self.memory["emotions"].append(emotion)

    def set_narrative(self, text: str):
        self.memory["narrative"] = text

    def get_memory(self):
        return self.memory

    def reset(self):
        self.__init__()
