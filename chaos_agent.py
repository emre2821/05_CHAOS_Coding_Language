"""
Emotion-driven agent that executes CHAOS scripts, updates memory, runs protocols.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from chaos_context import ChaosContext
from chaos_dreams import DreamEngine
from chaos_emotion import ChaosEmotionStack
from chaos_graph import ChaosGraph
from chaos_logger import ChaosLogger
from chaos_protocols import ProtocolRegistry
from chaos_runtime import run_chaos
from chaos_stdlib import norm_key, soft_intensity, text_snippet


@dataclass
class Action:
    kind: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentReport:
    emotions: List[Dict[str, Any]]
    symbols: Dict[str, Any]
    narrative: str
    action: Optional[Action]
    dreams: List[str]
    log: str


class ChaosAgent:
    def __init__(self, name: str, *, seed: Optional[int] = None):
        self.name = name
        self.ctx = ChaosContext()
        self.log = ChaosLogger()
        self.emotions = ChaosEmotionStack()
        self.graph = ChaosGraph()
        self.protocols = ProtocolRegistry()
        self.dreams = DreamEngine(seed=seed)

    def perceive_text(self, text: str) -> None:
        self.log.log(f"{self.name} perceived: {text_snippet(text)}")
        self.emotions.trigger_from_text(text)

    def perceive_sn(self, source: str) -> None:
        env = run_chaos(source, verbose=False)
        structured_core = env.get("structured_core", {})
        emotive_layer = env.get("emotive_layer", [])
        chaosfield_layer = env.get("chaosfield_layer", "")
        for key, value in structured_core.items():
            symbol_key = norm_key(key)
            self.ctx.set_symbol(symbol_key, value)
            self.log.log(f"symbol {symbol_key}={value}")
        for entry in emotive_layer:
            name = norm_key(entry.get("type") or entry.get("name") or "FEELING")
            raw = entry.get("intensity")
            intensity = soft_intensity(raw)
            self.emotions.push(name, intensity)
            self.log.log(f"emotion {name}:{intensity}")
        if chaosfield_layer:
            self.ctx.set_narrative(chaosfield_layer)
            self.log.log(f"narrative {text_snippet(chaosfield_layer)}")

    def reflect(self) -> List[str]:
        memory = self.ctx.get()
        emotions_snapshot = self._emotion_snapshot()
        visions = self.dreams.visions(memory["symbols"], emotions_snapshot, memory["narrative"])
        for vision in visions:
            self.log.log(f"dream {text_snippet(vision)}")
        return visions

    def decide(self) -> Optional[Action]:
        memory = self.ctx.get()
        emotions_snapshot = self._emotion_snapshot()
        choice = self.protocols.evaluate(memory, emotions_snapshot)
        if not choice:
            self.log.log("idle")
            return None
        self.log.log(f"protocol {choice.name}:{choice.score} -> {choice.action}")
        return Action(choice.action, choice.details)

    def act(self, action: Optional[Action]) -> None:
        if not action:
            return
        self.log.log(f"act {action.kind} {action.payload}")
        if action.kind == "relate":
            symbols = list(self.ctx.get()["symbols"].keys())
            for index in range(len(symbols) - 1):
                self.graph.add_edge(symbols[index], symbols[index + 1])

    def tick(self, decay: int = 1) -> None:
        self.emotions.decay_all(decay)

    def step(self, *, text: Optional[str] = None, sn: Optional[str] = None) -> AgentReport:
        if text:
            self.perceive_text(text)
        if sn:
            self.perceive_sn(sn)
        dreams = self.reflect()
        action = self.decide()
        self.act(action)
        self.tick()
        memory = self.ctx.get()
        return AgentReport(
            emotions=self._emotion_snapshot(),
            symbols=dict(memory["symbols"]),
            narrative=memory["narrative"],
            action=action,
            dreams=dreams,
            log=self.log.export(),
        )

    def _emotion_snapshot(self) -> List[Dict[str, Any]]:
        return [
            {"name": emotion.name, "intensity": emotion.intensity}
            for emotion in self.emotions.stack
            if emotion.is_active()
        ]

