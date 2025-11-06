"""
Dream engine: concise visions generated from state.
"""
import random
from typing import Any, Dict, Iterable, List, Optional

from chaos_stdlib import text_snippet, uniq


class DreamEngine:
    def __init__(self, seed: Optional[int] = None):
        self._seed = seed
        self._rng = random.Random(seed)

    def visions(
        self,
        symbols: Dict[str, Any],
        emotions: List[Dict[str, Any]],
        narrative: str,
        count: int = 3,
    ) -> List[str]:
        rng = self._rng
        
        def choose(seq: Iterable[Any], default: str) -> str:
            seq = list(seq)
            if not seq:
                return default
            return self._rng.choice(seq)

        keys = uniq(list(symbols.keys()))
        emotion_names = [
            emotion["name"]
            for emotion in emotions
            for _ in range(max(emotion["intensity"] // 2, 1))
        ]
        base = text_snippet(narrative, 160)
        dreams = []
        for _ in range(count):
            first = choose(keys, "MEMORY")
            second = choose(keys, "LIGHT")
            emotion_name = choose(emotion_names, "CALM")
            dreams.append(f"Dream of {first} meeting {second} under {emotion_name}; context: {base}")
        return dreams
