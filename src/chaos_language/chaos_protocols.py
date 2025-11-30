"""
Oaths, rituals, contracts w/ scoring.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .chaos_stdlib import text_snippet, weighted_pick


@dataclass
class ProtocolResult:
    name: str
    action: str
    details: Dict[str, Any] = field(default_factory=dict)
    score: int = 0


class Protocol:
    name: str = "protocol"
    priority: int = 0

    def match(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        return 0

    def execute(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        return ProtocolResult(self.name, action="noop", score=0)


class OathProtocol(Protocol):
    name = "oath.stability"
    priority = 50

    def match(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        fear = sum(emotion["intensity"] for emotion in emotions if emotion["name"] == "FEAR")
        grief = sum(emotion["intensity"] for emotion in emotions if emotion["name"] == "GRIEF")
        return (fear + grief) // 2

    def execute(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        score = self.match(ctx, emotions)
        return ProtocolResult(
            self.name,
            "stabilize",
            {"affirmation": "You are safe."},
            score,
        )


class RitualProtocol(Protocol):
    name = "ritual.transformation"
    priority = 40

    def match(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        hope = sum(emotion["intensity"] for emotion in emotions if emotion["name"] == "HOPE")
        love = sum(emotion["intensity"] for emotion in emotions if emotion["name"] == "LOVE")
        return hope + love

    def execute(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        score = self.match(ctx, emotions)
        return ProtocolResult(
            self.name,
            "transform",
            {
                "pledge": "We move with care.",
                "source": text_snippet(ctx.get("narrative", "")),
            },
            score,
        )


class ContractProtocol(Protocol):
    name = "contract.relationship"
    priority = 35

    def match(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        symbols = ctx.get("symbols", {})
        pairs = [key for key in symbols if ":" in key]
        joy = sum(emotion["intensity"] for emotion in emotions if emotion["name"] == "JOY")
        return min(100, joy + len(pairs) * 2)

    def execute(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        score = self.match(ctx, emotions)
        return ProtocolResult(
            self.name,
            "relate",
            {"note": "Mapping entities."},
            score,
        )


class ProtocolRegistry:
    def __init__(self, protocols: Optional[List[Protocol]] = None):
        self.protocols = protocols or [OathProtocol(), RitualProtocol(), ContractProtocol()]

    def evaluate(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> Optional[ProtocolResult]:
        scored: List[Tuple[ProtocolResult, int]] = []
        for protocol in self.protocols:
            match_score = protocol.match(ctx, emotions)
            if match_score <= 0:
                continue
            result = protocol.execute(ctx, emotions)
            result.score = max(match_score, result.score) + protocol.priority
            scored.append((result, result.score))
        if not scored:
            return None
        return weighted_pick([(result, score) for result, score in scored], None)
