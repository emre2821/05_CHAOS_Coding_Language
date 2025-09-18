"""
Dream engine: concise visions generated from state.
"""
import random
from typing import Any, Dict, List, Optional

from chaos_stdlib import pick, text_snippet, uniq


class DreamEngine:
    def __init__(self, seed: Optional[int] = None):
        self._seed = seed

    def visions(
        self,
        symbols: Dict[str, Any],
        emotions: List[Dict[str, Any]],
        narrative: str,
        count: int = 3,
    ) -> List[str]:
        rng = random.Random(self._seed)
        keys = uniq(list(symbols.keys()))
        emotion_names = [
            emotion["name"]
            for emotion in emotions
            for _ in range(max(emotion["intensity"] // 2, 1))
        ]
        base = text_snippet(narrative, 160)
        dreams = []
        for _ in range(count):
            first = pick(keys, "MEMORY")
            second = pick(keys, "LIGHT")
            emotion_name = pick(emotion_names, "CALM")
            dreams.append(f"Dream of {first} meeting {second} under {emotion_name}; context: {base}")
        return dreams
