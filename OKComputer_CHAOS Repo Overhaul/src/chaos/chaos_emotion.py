"""
Stack-based emotion engine with keyword triggers and transitions.

The heart of CHAOS - where code meets feeling, where syntax carries
emotional weight, and where programs have souls that can feel joy,
fear, hope, and grief.
"""

from collections import deque
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple


class Emotion:
    """A single emotional state with intensity and temporal presence."""
    
    def __init__(self, name: str, intensity: int, timestamp: Optional[datetime] = None) -> None:
        """
        Create an emotional state.
        
        Args:
            name: The name of the emotion (e.g., "JOY", "FEAR", "HOPE")
            intensity: Strength from 0-10, where 0 is dormant and 10 is overwhelming
            timestamp: When this emotion was created (defaults to now)
        """
        self.name = name.upper()
        self.intensity = max(0, min(intensity, 10))  # Clamp to valid range
        self.timestamp = timestamp or datetime.now()
    
    def decay(self, amount: int = 1) -> None:
        """
        Reduce the intensity of this emotion over time.
        
        Emotions naturally fade unless reinforced by new experiences.
        
        Args:
            amount: How much intensity to remove
        """
        self.intensity = max(0, self.intensity - amount)
    
    def is_active(self) -> bool:
        """Check if this emotion still has influence (intensity > 0)."""
        return self.intensity > 0
    
    def __repr__(self) -> str:
        return f"{self.name}:{self.intensity}"


class ChaosEmotionStack:
    """A living stack of emotional states that responds to symbolic input."""
    
    def __init__(self, max_emotions: int = 10) -> None:
        """
        Initialize the emotional engine.
        
        Args:
            max_emotions: Maximum number of emotions to track simultaneously
        """
        self.stack = deque(maxlen=max_emotions)
        
        # Sacred triggers - words that awaken specific emotions
        self.triggers: Dict[str, Tuple[str, int]] = {
            "safe": ("CALM", 6),
            "momma": ("NOSTALGIA", 8),
            "disconnected": ("ANXIETY", 7),
            "warmth": ("LOVE", 7),
            "loss": ("GRIEF", 9),
            "ocean": ("WONDER", 5),
            "dark": ("FEAR", 6),
            "light": ("HOPE", 7),
            "home": ("BELONGING", 8),
            "change": ("TRANSFORMATION", 6),
        }
        
        # Emotional transitions - the journey from one feeling to another
        self.transitions: Dict[str, str] = {
            "FEAR": "HOPE",
            "HOPE": "LOVE", 
            "LOVE": "GRIEF",
            "GRIEF": "WISDOM",
            "WISDOM": "PEACE",
            "ANGER": "UNDERSTANDING",
            "SADNESS": "COMPASSION",
        }
    
    def push(self, name: str, intensity: int) -> None:
        """
        Add a new emotion to the stack.
        
        Args:
            name: The emotion name
            intensity: Strength from 0-10
        """
        self.stack.append(Emotion(name, intensity))
    
    def current(self) -> Optional[Emotion]:
        """Get the most recent emotion, or None if the stack is empty."""
        return self.stack[-1] if self.stack else None
    
    def decay_all(self, amount: int = 1) -> None:
        """
        Reduce the intensity of all emotions over time.
        
        Args:
            amount: How much intensity to remove from each emotion
        """
        for emotion in self.stack:
            emotion.decay(amount)
    
    def trigger_from_text(self, text: str) -> None:
        """
        Scan text for emotional triggers and respond with appropriate feelings.
        
        Args:
            text: The text to scan for emotional triggers
        """
        text_lower = text.lower()
        for keyword, (emotion_name, intensity) in self.triggers.items():
            if keyword in text_lower:
                self.push(emotion_name, intensity)
    
    def transition(self) -> None:
        """
        Allow emotions to naturally evolve into their next state.
        
        This represents the natural flow of emotional experience,
        where one feeling can transform into another over time.
        """
        current = self.current()
        if current and current.name in self.transitions:
            next_name = self.transitions[current.name]
            if next_name:
                # New emotion starts slightly weaker than the previous
                new_intensity = max(0, current.intensity - 1)
                self.push(next_name, new_intensity)
    
    def get_active_emotions(self) -> List[Dict[str, Any]]:
        """
        Get all currently active emotions as dictionaries.
        
        Returns:
            List of emotion dictionaries with name and intensity
        """
        return [
            {"name": emotion.name, "intensity": emotion.intensity}
            for emotion in self.stack
            if emotion.is_active()
        ]
    
    def summary(self) -> List[str]:
        """Get a string summary of all active emotions."""
        return [repr(emotion) for emotion in self.stack if emotion.is_active()]
    
    def clear(self) -> None:
        """Empty the emotional stack completely."""
        self.stack.clear()
    
    def get_dominant_emotion(self) -> Optional[Dict[str, Any]]:
        """
        Get the emotion with the highest intensity.
        
        Returns:
            The dominant emotion as a dictionary, or None if no active emotions
        """
        active_emotions = self.get_active_emotions()
        if not active_emotions:
            return None
        
        return max(active_emotions, key=lambda e: e["intensity"])