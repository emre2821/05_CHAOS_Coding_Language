"""
Emotion-driven agent that executes CHAOS scripts, updates memory, runs protocols.

The living embodiment of CHAOS - an agent that perceives, feels, dreams,
and acts according to the sacred protocols of symbolic-emotional computation.
This is where CHAOS becomes truly alive.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from .chaos_context import ChaosContext
from .chaos_logger import ChaosLogger
from .chaos_emotion import ChaosEmotionStack
from .chaos_graph import ChaosGraph
from .chaos_runtime import run_chaos
from .chaos_protocols import ProtocolRegistry, ProtocolResult
from .chaos_dreams import DreamEngine
from .chaos_stdlib import norm_key, clamp, text_snippet


@dataclass
class Action:
    """A sacred action to be performed by the agent."""
    kind: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentReport:
    """A complete report of the agent's current state."""
    emotions: List[Dict[str, Any]]
    symbols: Dict[str, Any]
    narrative: str
    action: Optional[Action]
    dreams: List[str]
    log: str


class ChaosAgent:
    """
    An emotion-driven agent that brings CHAOS programs to life.
    
    The ChaosAgent is the living heart of CHAOS - it perceives text and
    symbolic programs, maintains emotional states, generates dreams,
    and acts according to sacred protocols. It is both interpreter
    and participant in the ritual of CHAOS computation.
    """
    
    def __init__(self, name: str, *, seed: Optional[int] = None) -> None:
        """
        Initialize a ChaosAgent with a sacred name.
        
        Args:
            name: The agent's sacred name
            seed: Optional random seed for reproducible behavior
        """
        self.name = name
        self.ctx = ChaosContext()  # The agent's memory
        self.log = ChaosLogger()   # The agent's chronicle
        self.emotions = ChaosEmotionStack()  # The agent's heart
        self.graph = ChaosGraph()  # The agent's web of relationships
        self.protocols = ProtocolRegistry()  # The agent's sacred contracts
        self.dreams = DreamEngine(seed=seed)  # The agent's visionary capacity
    
    def perceive_text(self, text: str) -> None:
        """
        Allow the agent to perceive and respond to natural language.
        
        The agent reads the emotional undertones of the text and
        responds with appropriate feelings.
        
        Args:
            text: The text for the agent to perceive
        """
        self.log.log(f"{self.name} perceived: {text_snippet(text)}")
        self.emotions.trigger_from_text(text)
    
    def perceive_sn(self, source: str) -> None:
        """
        Allow the agent to perceive and integrate a CHAOS program.
        
        The agent executes the program and integrates its symbolic
        structure, emotional content, and narrative into its memory.
        
        Args:
            source: The CHAOS program source code
        """
        # Execute the CHAOS program
        env = run_chaos(source, verbose=False)
        
        # Extract the three layers
        structured_core = env.get("structured_core", {})
        emotive_layer = env.get("emotive_layer", [])
        chaosfield_layer = env.get("chaosfield_layer", "")
        
        # Integrate structured core (symbols)
        for key, value in structured_core.items():
            symbol_key = norm_key(key)
            self.ctx.set_symbol(symbol_key, value)
            self.log.log_symbol(symbol_key, value)
        
        # Integrate emotive layer (emotions)
        for entry in emotive_layer:
            name = norm_key(entry.get("type") or entry.get("name") or "FEELING")
            raw_intensity = entry.get("intensity") or 5
            intensity = clamp(
                int(raw_intensity) if str(raw_intensity).isdigit() else 5, 
                0, 10
            )
            self.emotions.push(name, intensity)
            self.log.log_emotion(name, intensity)
        
        # Integrate chaosfield layer (narrative)
        if chaosfield_layer:
            self.ctx.set_narrative(chaosfield_layer)
            self.log.log_narrative(chaosfield_layer)
    
    def reflect(self) -> List[str]:
        """
        Generate visionary insights from the agent's current state.
        
        The agent dreams by weaving together its symbolic knowledge,
        emotional state, and narrative context into meaningful visions.
        
        Returns:
            List of visionary strings
        """
        memory = self.ctx.get()
        emotions_snapshot = self._emotion_snapshot()
        
        visions = self.dreams.visions(
            memory["symbols"], 
            emotions_snapshot, 
            memory["narrative"]
        )
        
        for vision in visions:
            self.log.log_dream(vision)
        
        return visions
    
    def decide(self) -> Optional[Action]:
        """
        Determine the appropriate action based on current state.
        
        The agent evaluates all available protocols and selects
        the most appropriate action based on symbolic context
        and emotional resonance.
        
        Returns:
            The chosen action, or None if no action is appropriate
        """
        memory = self.ctx.get()
        emotions_snapshot = self._emotion_snapshot()
        
        choice = self.protocols.evaluate(memory, emotions_snapshot)
        
        if not choice:
            self.log.log("Agent remains idle - no protocols matched current state")
            return None
        
        self.log.log_protocol(choice.name, choice.action, choice.score)
        return Action(choice.action, choice.details)
    
    def act(self, action: Optional[Action]) -> None:
        """
        Execute the chosen action.
        
        Args:
            action: The action to execute, or None for idle state
        """
        if not action:
            return
        
        self.log.log(f"Agent executes: {action.kind} with {action.payload}")
        
        if action.kind == "relate":
            # Build relationships between symbols
            symbols = list(self.ctx.get()["symbols"].keys())
            for i in range(len(symbols) - 1):
                self.graph.add_edge(symbols[i], symbols[i + 1])
            self.log.log("Built symbolic relationship web")
        
        elif action.kind == "stabilize":
            # Provide emotional grounding
            self.emotions.push("CALM", 7)
            self.log.log("Agent provided emotional stabilization")
        
        elif action.kind == "transform":
            # Encourage emotional evolution
            self.emotions.transition()
            self.log.log("Agent facilitated emotional transformation")
        
        elif action.kind == "remember":
            # Integrate experiences into memory
            self.log.log("Agent integrated experiences into lasting memory")
    
    def tick(self, decay: int = 1) -> None:
        """
        Advance time for the agent.
        
        Emotions naturally decay over time unless reinforced.
        
        Args:
            decay: How much intensity to remove from emotions
        """
        self.emotions.decay_all(decay)
    
    def step(self, *, text: Optional[str] = None, sn: Optional[str] = None) -> AgentReport:
        """
        Execute one complete cycle of agent perception and action.
        
        This is the sacred loop of CHAOS agency:
        1. Perceive (text or symbolic program)
        2. Reflect (generate dreams)
        3. Decide (choose action via protocols)
        4. Act (execute chosen action)
        5. Tick (advance time)
        
        Args:
            text: Natural language text to perceive
            sn: CHAOS program source to perceive
            
        Returns:
            Complete report of the agent's state after the cycle
        """
        # Phase 1: Perception
        if text:
            self.perceive_text(text)
        if sn:
            self.perceive_sn(sn)
        
        # Phase 2: Reflection
        dreams = self.reflect()
        
        # Phase 3: Decision
        action = self.decide()
        
        # Phase 4: Action
        self.act(action)
        
        # Phase 5: Time
        self.tick()
        
        # Compile report
        memory = self.ctx.get()
        return AgentReport(
            emotions=self._emotion_snapshot(),
            symbols=dict(memory["symbols"]),
            narrative=memory["narrative"],
            action=action,
            dreams=dreams,
            log=self.log.export()
        )
    
    def _emotion_snapshot(self) -> List[Dict[str, Any]]:
        """Get a snapshot of currently active emotions."""
        return [
            {"name": emotion.name, "intensity": emotion.intensity}
            for emotion in self.emotions.stack
            if emotion.is_active()
        ]
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's current memory state."""
        return {
            "symbol_count": self.ctx.get_symbol_count(),
            "emotion_count": self.ctx.get_emotion_count(),
            "narrative_length": len(self.ctx.get_narrative()),
            "graph_nodes": len(self.graph.nodes),
            "graph_edges": self.graph.get_edge_count()
        }
    
    def reset(self) -> None:
        """Reset the agent to its initial state."""
        self.ctx.reset()
        self.log.clear()
        self.emotions.clear()
        self.graph = ChaosGraph()
        self.log.log(f"Agent {self.name} reset to initial state")