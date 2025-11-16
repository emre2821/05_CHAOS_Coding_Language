"""
Dream engine: concise visions generated from state.
"""
import random
from typing import Any, Dict, Iterable, List, Optional

from chaos_stdlib import text_snippet, uniq


class DreamEngine:
    def __init__(self, seed: Optional[int] = None):
        self._rng = random.Random(seed)

    def _choose(self, rng: random.Random, seq: Iterable[Any], default: str) -> str:
        seq = list(seq)
        if not seq:
            return default
        return rng.choice(seq)

    def visions(
        self,
        symbols: Dict[str, Any],
        emotions: List[Dict[str, Any]],
        narrative: str,
        count: int = 3,
    ) -> List[str]:
        rng = self._rng

        keys = uniq(list(symbols.keys()))
        emotion_names = [
            emotion["name"]
            for emotion in emotions
            for _ in range(max(emotion["intensity"] // 2, 1))
        ]
        base = text_snippet(narrative, 160)
        dreams = []
        for _ in range(count):
            first = self._choose(rng, keys, "MEMORY")
            second = self._choose(rng, keys, "LIGHT")
            emotion_name = self._choose(rng, emotion_names, "CALM")
            dreams.append(f"Dream of {first} meeting {second} under {emotion_name}; context: {base}")
        return dreams
