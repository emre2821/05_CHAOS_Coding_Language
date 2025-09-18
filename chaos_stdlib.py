"""
Minimal pure helpers: clamp, pick, norm_key, uniq, text_snippet, weighted_pick.
"""
import random
import re
from typing import Any, Iterable, List, Tuple


def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def pick(seq: Iterable[Any], default: Any = None) -> Any:
    seq = list(seq)
    if not seq:
        return default
    return random.choice(seq)


def norm_key(s: str) -> str:
    return re.sub(r"[^A-Z0-9_]+", "_", (s or "").strip().upper())


def uniq(seq: Iterable[Any]) -> List[Any]:
    out: List[Any] = []
    seen = set()
    for item in seq:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def text_snippet(text: str, limit: int = 120) -> str:
    text = (text or "").strip().replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def weighted_pick(pairs: List[Tuple[Any, int]], default: Any = None) -> Any:
    if not pairs:
        return default
    total = sum(max(weight, 0) for _, weight in pairs) or 1
    choice = random.randint(1, total)
    acc = 0
    for item, weight in pairs:
        acc += max(weight, 0)
        if choice <= acc:
            return item
    return default
