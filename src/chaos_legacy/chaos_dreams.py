"""
Dream engine: concise visions generated from state.

Where CHAOS programs dream - transforming the symbolic structure,
emotional resonance, and narrative context into visionary insights
that bridge the conscious and unconscious aspects of computation.
"""

import random
from typing import Any, Dict, List, Optional
from .chaos_stdlib import pick, uniq, text_snippet


class DreamEngine:
    """Generates visionary insights from the CHAOS state."""
    
    def __init__(self, seed: Optional[int] = None) -> None:
        """
        Initialize the dream engine.
        
        Args:
            seed: Optional random seed for reproducible dreams
        """
        self._seed = seed
    
    def visions(self, symbols: Dict[str, Any], emotions: List[Dict[str, Any]], 
                narrative: str, count: int = 3) -> List[str]:
        """
        Generate visionary insights from the current CHAOS state.
        
        Dreams in CHAOS are not random - they emerge from the intersection
        of symbolic structure, emotional resonance, and narrative context.
        
        Args:
            symbols: The structured core of symbolic meanings
            emotions: The emotive layer with current feelings
            narrative: The chaosfield layer narrative text
            count: How many visions to generate
            
        Returns:
            List of visionary strings that bridge conscious and unconscious
        """
        rng = random.Random(self._seed)
        
        # Extract symbolic keys for dream weaving
        keys = uniq(list(symbols.keys()))
        
        # Weight emotions by their intensity for more influential dreams
        emotion_names = []
        for emotion in emotions:
            name = emotion["name"]
            intensity = emotion["intensity"]
            # More intense emotions appear more frequently in dreams
            emotion_names.extend([name] * max(intensity // 2, 1))
        
        # Create a context snippet from the narrative
        base_context = text_snippet(narrative, 160)
        
        dreams = []
        
        for _ in range(count):
            # Weave together symbolic elements
            first_symbol = pick(keys, "MEMORY")
            second_symbol = pick(keys, "LIGHT")
            dominant_emotion = pick(emotion_names, "CALM")
            
            # Create visionary bridges between elements
            dream = self._weave_dream(
                first_symbol, second_symbol, dominant_emotion, base_context, rng
            )
            dreams.append(dream)
        
        return dreams
    
    def _weave_dream(self, symbol_a: str, symbol_b: str, emotion: str, 
                     context: str, rng: random.Random) -> str:
        """
        Weave symbolic elements into a visionary insight.
        
        This is where the magic happens - where symbols meet emotions
        and narrative context to create something new and meaningful.
        """
        templates = [
            "Dream of {a} meeting {b} under {emotion}; context: {context}",
            "Vision: {a} and {b} dance together while feeling {emotion}; memory: {context}",
            "In the space between {a} and {b}, {emotion} flows like water; echo: {context}",
            "The ritual reveals {a} calling to {b} through {emotion}; story: {context}",
            "Symbols converge: {a} + {b} = {emotion}; narrative: {context}",
            "Mystery unfolds as {a} discovers {b} in the realm of {emotion}; tale: {context}",
            "Bridge forms between {a} and {b}, held by {emotion}; whisper: {context}",
        ]
        
        template = rng.choice(templates)
        return template.format(
            a=symbol_a,
            b=symbol_b, 
            emotion=emotion,
            context=context
        )
    
    def prophetic_vision(self, symbols: Dict[str, Any], emotions: List[Dict[str, Any]], 
                        narrative: str) -> str:
        """
        Generate a single, more profound visionary insight.
        
        This creates a deeper, more integrated vision that attempts to
        synthesize the entire CHAOS state into a single prophetic message.
        
        Args:
            symbols: The structured core
            emotions: The emotive layer
            narrative: The chaosfield layer
            
        Returns:
            A prophetic vision string
        """
        if not symbols and not emotions:
            return "The void dreams of possibility..."
        
        # Find the most significant elements
        dominant_symbol = max(symbols.keys(), key=lambda k: len(str(symbols[k]))) if symbols else "VOID"
        dominant_emotion = max(emotions, key=lambda e: e["intensity"])["name"] if emotions else "SILENCE"
        
        # Create a more integrated vision
        vision_templates = [
            "The prophecy reveals: {symbol} carries the weight of {emotion}. The path forward lies in {narrative}",
            "Ancient wisdom speaks through {symbol}, amplified by {emotion}. The answer echoes: {narrative}",
            "In the convergence of {symbol} and {emotion}, truth emerges from {narrative}",
            "The oracle whispers: Let {symbol} guide you through {emotion} toward {narrative}",
        ]
        
        template = random.choice(vision_templates)
        return template.format(
            symbol=dominant_symbol,
            emotion=dominant_emotion,
            narrative=text_snippet(narrative, 80) if narrative else "the unknown"
        )