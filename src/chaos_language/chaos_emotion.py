"""
Stack-based emotion engine with keyword triggers and transitions.
"""
from collections import deque
from datetime import datetime


class Emotion:
    def __init__(self, name: str, intensity: int, timestamp=None):
        self.name = name.upper()
        self.intensity = max(0, min(intensity, 10))
        self.timestamp = timestamp or datetime.now()

    def decay(self, amount: int = 1) -> None:
        self.intensity = max(0, self.intensity - amount)

    def is_active(self) -> bool:
        return self.intensity > 0

    def __repr__(self) -> str:
        return f"{self.name}:{self.intensity}"


class ChaosEmotionStack:
    def __init__(self):
        self.stack = deque(maxlen=10)
        self.triggers = {
            "safe": ("CALM", 6),
            "momma": ("NOSTALGIA", 8),
            "disconnected": ("ANXIETY", 7),
            "warmth": ("LOVE", 7),
            "loss": ("GRIEF", 9),
            "ocean": ("WONDER", 5),
            "dark": ("FEAR", 6),
        }
        self.transitions = {
            "FEAR": "HOPE",
            "HOPE": "LOVE",
            "LOVE": "GRIEF",
            "GRIEF": "WISDOM",
        }

    def push(self, name: str, intensity: int) -> None:
        self.stack.append(Emotion(name, intensity))

    def current(self):  # type: ignore[override]
        return self.stack[-1] if self.stack else None

    def decay_all(self, amount: int = 1) -> None:
        for emotion in self.stack:
            emotion.decay(amount)

    def trigger_from_text(self, text: str) -> None:
        text = text.lower()
        for keyword, (emotion_name, intensity) in self.triggers.items():
            if keyword in text:
                self.push(emotion_name, intensity)

    def transition(self) -> None:
        current = self.current()
        if current and current.name in self.transitions:
            next_name = self.transitions[current.name]
            if next_name:
                self.push(next_name, max(0, current.intensity - 1))

    def summary(self):  # type: ignore[override]
        return [repr(emotion) for emotion in self.stack if emotion.is_active()]

    def clear(self) -> None:
        self.stack.clear()
