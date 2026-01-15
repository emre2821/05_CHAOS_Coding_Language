"""
Timestamped runtime logger for symbols, emotions, narrative.

The sacred chronicle of CHAOS execution - where every symbol gained,
every emotion felt, and every narrative woven is recorded with
temporal precision for future reflection and understanding.
"""

import datetime
from typing import List, Optional


class ChaosLogger:
    """Records the sacred history of CHAOS execution."""
    
    def __init__(self) -> None:
        """Initialize an empty chronicle."""
        self.logs: List[str] = []
        self.start_time = datetime.datetime.now()
    
    def log(self, message: str) -> None:
        """
        Record a general event in the sacred chronicle.
        
        Args:
            message: The event to record
        """
        entry = f"[{datetime.datetime.now().isoformat()}] {message}"
        self.logs.append(entry)
    
    def log_symbol(self, name: str, value: str) -> None:
        """
        Record the birth or transformation of a symbol.
        
        Args:
            name: The symbolic name
            value: The symbolic value
        """
        self.log(f"SYMBOL: {name} = {value}")
    
    def log_emotion(self, emotion: str, intensity: int) -> None:
        """
        Record the arising of an emotional state.
        
        Args:
            emotion: The emotion name
            intensity: The emotional intensity (0-10)
        """
        self.log(f"EMOTION: {emotion}:{intensity}")
    
    def log_narrative(self, chaosfield: str) -> None:
        """
        Record the weaving of narrative text.
        
        Args:
            chaosfield: The narrative text (will be truncated for logging)
        """
        truncated = chaosfield[:60] + "..." if len(chaosfield) > 60 else chaosfield
        self.log(f"NARRATIVE: {truncated}")
    
    def log_dream(self, dream: str) -> None:
        """
        Record a visionary insight from the dream engine.
        
        Args:
            dream: The visionary text
        """
        truncated = dream[:80] + "..." if len(dream) > 80 else dream
        self.log(f"DREAM: {truncated}")
    
    def log_protocol(self, protocol_name: str, action: str, score: int) -> None:
        """
        Record the execution of a sacred protocol.
        
        Args:
            protocol_name: Name of the protocol
            action: The action taken
            score: The match score
        """
        self.log(f"PROTOCOL: {protocol_name}:{score} -> {action}")
    
    def log_error(self, error_type: str, message: str) -> None:
        """
        Record an error in the sacred chronicle.
        
        Args:
            error_type: Type of error that occurred
            message: Error description
        """
        self.log(f"ERROR [{error_type}]: {message}")
    
    def export(self) -> str:
        """
        Get the complete sacred chronicle as text.
        
        Returns:
            Complete log history as a string
        """
        header = f"=== CHAOS Execution Chronicle ===\n"
        header += f"Started: {self.start_time.isoformat()}\n"
        header += f"Entries: {len(self.logs)}\n"
        header += "=" * 40 + "\n\n"
        
        return header + "\n".join(self.logs)
    
    def get_recent(self, count: int = 10) -> List[str]:
        """
        Get the most recent log entries.
        
        Args:
            count: How many recent entries to return
            
        Returns:
            List of recent log entries
        """
        return self.logs[-count:] if len(self.logs) >= count else self.logs
    
    def clear(self) -> None:
        """Clear the sacred chronicle (use with caution)."""
        self.logs.clear()
        self.start_time = datetime.datetime.now()
    
    def get_duration(self) -> datetime.timedelta:
        """Get how long the chronicle has been recording."""
        return datetime.datetime.now() - self.start_time
    
    def search(self, keyword: str) -> List[str]:
        """
        Search the chronicle for entries containing a keyword.
        
        Args:
            keyword: The term to search for
            
        Returns:
            List of matching log entries
        """
        keyword_lower = keyword.lower()
        return [entry for entry in self.logs if keyword_lower in entry.lower()]