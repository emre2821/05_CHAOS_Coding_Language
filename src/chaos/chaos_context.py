"""
Shared memory for symbols, emotions, narrative.

The living memory of CHAOS - where symbols gain meaning, emotions
leave their traces, and narratives become part of the collective
unconscious of the program.
"""

from typing import Dict, Any, List, Optional


class ChaosContext:
    """The sacred memory space where CHAOS programs store their essence."""
    
    def __init__(self) -> None:
        """Initialize the memory with empty layers."""
        self.memory = {
            "symbols": {},      # The structured core - symbolic foundation
            "emotions": [],     # The emotive layer - traces of feeling
            "narrative": "",    # The chaosfield - free narrative text
        }
    
    def set_symbol(self, key: str, value: str) -> None:
        """
        Add or update a symbol in the structured core.
        
        Args:
            key: The symbolic name
            value: The symbolic value
        """
        self.memory["symbols"][key] = value
    
    def get_symbol(self, key: str) -> Optional[str]:
        """
        Retrieve a symbol from the structured core.
        
        Args:
            key: The symbolic name to retrieve
            
        Returns:
            The symbolic value, or None if not found
        """
        return self.memory["symbols"].get(key)
    
    def add_emotion(self, emotion: str) -> None:
        """
        Add an emotion trace to the emotive layer.
        
        Args:
            emotion: The emotion name to add
        """
        self.memory["emotions"].append(emotion)
    
    def set_narrative(self, text: str) -> None:
        """
        Set the narrative text in the chaosfield layer.
        
        Args:
            text: The narrative text to store
        """
        self.memory["narrative"] = text
    
    def get_narrative(self) -> str:
        """Get the current narrative text."""
        return self.memory["narrative"]
    
    def get_symbols(self) -> Dict[str, str]:
        """Get all symbols from the structured core."""
        return self.memory["symbols"].copy()
    
    def get_emotions(self) -> List[str]:
        """Get all emotion traces from the emotive layer."""
        return self.memory["emotions"].copy()
    
    def get(self) -> Dict[str, Any]:
        """
        Get the complete memory state.
        
        Returns:
            Dictionary with symbols, emotions, and narrative
        """
        return self.memory.copy()
    
    def reset(self) -> None:
        """Clear all memory and start fresh."""
        self.__init__()
    
    def has_symbol(self, key: str) -> bool:
        """Check if a symbol exists in the structured core."""
        return key in self.memory["symbols"]
    
    def remove_symbol(self, key: str) -> bool:
        """
        Remove a symbol from the structured core.
        
        Args:
            key: The symbolic name to remove
            
        Returns:
            True if the symbol was removed, False if it didn't exist
        """
        if key in self.memory["symbols"]:
            del self.memory["symbols"][key]
            return True
        return False
    
    def get_symbol_count(self) -> int:
        """Get the number of symbols in the structured core."""
        return len(self.memory["symbols"])
    
    def get_emotion_count(self) -> int:
        """Get the number of emotion traces in the emotive layer."""
        return len(self.memory["emotions"])
    
    def append_to_narrative(self, text: str) -> None:
        """
        Add text to the existing narrative.
        
        Args:
            text: Text to append to the current narrative
        """
        if self.memory["narrative"]:
            self.memory["narrative"] += " " + text
        else:
            self.memory["narrative"] = text