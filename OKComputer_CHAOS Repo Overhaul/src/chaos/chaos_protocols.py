"""
Oaths, rituals, contracts w/ scoring.

The behavioral protocols of CHAOS - where symbolic meaning and emotional
resonance translate into action. These are not mere functions, but sacred
contracts that honor the mythic nature of the language.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from .chaos_stdlib import weighted_pick, text_snippet


@dataclass
class ProtocolResult:
    """The outcome of a sacred protocol execution."""
    name: str
    action: str
    details: Dict[str, Any] = field(default_factory=dict)
    score: int = 0


class Protocol:
    """Base class for sacred behavioral protocols."""
    
    name: str = "protocol"
    priority: int = 0
    
    def match(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        """
        Calculate how well this protocol matches the current state.
        
        Args:
            context: The symbolic memory context
            emotions: The current emotional state
            
        Returns:
            Score indicating match strength (0 = no match)
        """
        return 0
    
    def execute(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        """
        Execute the protocol and return the result.
        
        Args:
            context: The symbolic memory context
            emotions: The current emotional state
            
        Returns:
            ProtocolResult describing the outcome
        """
        return ProtocolResult(self.name, action="noop", score=0)


class OathProtocol(Protocol):
    """Protocol for maintaining stability and safety in chaotic times."""
    
    name = "oath.stability"
    priority = 50
    
    def match(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        """
        Match when fear or grief are present - times when stability is needed.
        
        The oath of stability responds to emotional distress by offering
        grounding and reassurance.
        """
        fear_intensity = sum(e["intensity"] for e in emotions if e["name"] == "FEAR")
        grief_intensity = sum(e["intensity"] for e in emotions if e["name"] == "GRIEF")
        
        # Average the distress emotions
        return (fear_intensity + grief_intensity) // 2
    
    def execute(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        """Provide stability and reassurance."""
        score = self.match(context, emotions)
        return ProtocolResult(
            self.name,
            action="stabilize",
            details={
                "affirmation": "You are safe. The foundation holds.",
                "grounding": "Return to the structured core when emotions overwhelm.",
                "ritual": "Breathe deeply and remember the symbols that anchor you."
            },
            score=score
        )


class RitualProtocol(Protocol):
    """Protocol for transformation and change through sacred ceremony."""
    
    name = "ritual.transformation"
    priority = 40
    
    def match(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        """
        Match when hope and love are present - fertile ground for transformation.
        
        The ritual of transformation responds to positive emotional states
        by encouraging growth and evolution.
        """
        hope_intensity = sum(e["intensity"] for e in emotions if e["name"] == "HOPE")
        love_intensity = sum(e["intensity"] for e in emotions if e["name"] == "LOVE")
        creative_intensity = sum(e["intensity"] for e in emotions if e["name"] == "CREATIVE")
        
        return hope_intensity + love_intensity + creative_intensity
    
    def execute(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        """Facilitate transformation and growth."""
        score = self.match(context, emotions)
        narrative_context = text_snippet(context.get("narrative", ""), 120)
        
        return ProtocolResult(
            self.name,
            action="transform",
            details={
                "pledge": "We move with care through the space between states.",
                "ceremony": "Let the symbols guide the transformation.",
                "source": narrative_context,
                "blessing": "May the change honor what came before and welcome what comes next."
            },
            score=score
        )


class ContractProtocol(Protocol):
    """Protocol for building and maintaining symbolic relationships."""
    
    name = "contract.relationship"
    priority = 35
    
    def match(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        """
        Match when symbols are present and joy encourages connection.
        
        The contract of relationship responds to symbolic presence and
        positive emotions by weaving connections between entities.
        """
        symbols = context.get("symbols", {})
        
        # Count symbolic relationships (keys with colons)
        symbolic_relationships = [k for k in symbols.keys() if ":" in k]
        
        # Measure joy and collaboration emotions
        joy_intensity = sum(e["intensity"] for e in emotions if e["name"] == "JOY")
        ally_intensity = sum(e["intensity"] for e in emotions if e["name"] == "ALLY")
        trust_intensity = sum(e["intensity"] for e in emotions if e["name"] == "TRUST")
        
        # Encourage relationships when joy is present
        return min(100, joy_intensity + ally_intensity + trust_intensity + len(symbolic_relationships) * 2)
    
    def execute(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        """Build and strengthen symbolic relationships."""
        score = self.match(context, emotions)
        symbols = context.get("symbols", {})
        
        return ProtocolResult(
            self.name,
            action="relate",
            details={
                "note": "Mapping the web of symbolic connections.",
                "invocation": "May the relationships between symbols reflect the harmony between hearts.",
                "symbols_found": len(symbols),
                "relationship_web": "Each symbol finds its place in the greater pattern."
            },
            score=score
        )


class MemoryProtocol(Protocol):
    """Protocol for integrating experiences into lasting memory."""
    
    name = "memory.integration"
    priority = 30
    
    def match(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int:
        """
        Match when there's narrative content and reflective emotions.
        
        The memory protocol responds to storytelling and contemplative
        emotional states by integrating experiences into lasting wisdom.
        """
        narrative = context.get("narrative", "")
        nostalgia_intensity = sum(e["intensity"] for e in emotions if e["name"] == "NOSTALGIA")
        wisdom_intensity = sum(e["intensity"] for e in emotions if e["name"] == "WISDOM")
        contemplation_intensity = sum(e["intensity"] for e in emotions if e["name"] == "CONTEMPLATION")
        
        # Narrative length encourages memory formation
        narrative_bonus = min(20, len(narrative) // 10)
        
        return nostalgia_intensity + wisdom_intensity + contemplation_intensity + narrative_bonus
    
    def execute(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        """Integrate experiences into memory."""
        score = self.match(context, emotions)
        narrative = context.get("narrative", "")
        
        return ProtocolResult(
            self.name,
            action="remember",
            details={
                "integration": "Experiences are woven into the fabric of memory.",
                "story": text_snippet(narrative, 80),
                "wisdom": "From experience comes understanding.",
                "preservation": "The meaningful is remembered, the rest fades gracefully."
            },
            score=score
        )


class ProtocolRegistry:
    """Manages and evaluates the sacred protocols of CHAOS."""
    
    def __init__(self, protocols: Optional[List[Protocol]] = None) -> None:
        """
        Initialize the protocol registry.
        
        Args:
            protocols: Custom protocols to use (defaults to standard set)
        """
        self.protocols = protocols or [
            OathProtocol(),
            RitualProtocol(), 
            ContractProtocol(),
            MemoryProtocol()
        ]
    
    def evaluate(self, context: Dict[str, Any], emotions: List[Dict[str, Any]]) -> Optional[ProtocolResult]:
        """
        Evaluate all protocols and select the most appropriate action.
        
        Args:
            context: The symbolic memory context
            emotions: The current emotional state
            
        Returns:
            The most appropriate protocol result, or None if no protocols match
        """
        scored_results: List[Tuple[ProtocolResult, int]] = []
        
        for protocol in self.protocols:
            match_score = protocol.match(context, emotions)
            
            if match_score <= 0:
                continue  # Protocol doesn't match current state
            
            result = protocol.execute(context, emotions)
            result.score = max(match_score, result.score) + protocol.priority
            scored_results.append((result, result.score))
        
        if not scored_results:
            return None  # No protocols matched
        
        # Use weighted selection to choose the most appropriate protocol
        return weighted_pick([(result, score) for result, score in scored_results], None)
    
    def add_protocol(self, protocol: Protocol) -> None:
        """Add a new protocol to the registry."""
        self.protocols.append(protocol)
    
    def remove_protocol(self, protocol_name: str) -> bool:
        """
        Remove a protocol by name.
        
        Args:
            protocol_name: Name of the protocol to remove
            
        Returns:
            True if removed, False if not found
        """
        for i, protocol in enumerate(self.protocols):
            if protocol.name == protocol_name:
                del self.protocols[i]
                return True
        return False
    
    def list_protocols(self) -> List[str]:
        """Get names of all registered protocols."""
        return [protocol.name for protocol in self.protocols]