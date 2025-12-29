"""
Minimal pure helpers: clamp, pick, norm_key, uniq, text_snippet, weighted_pick.

The sacred utilities of CHAOS - small functions that carry great meaning,
providing the elemental operations that support the larger ritual of
symbolic-emotional computation.
"""

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import random
import re


def clamp(value: int, minimum: int, maximum: int) -> int:
    """
    Constrain a value within sacred bounds.
    
    Args:
        value: The value to constrain
        minimum: The lower sacred bound
        maximum: The upper sacred bound
        
    Returns:
        The value constrained within the sacred bounds
    """
    return max(minimum, min(maximum, value))


def pick(sequence: Iterable[Any], default: Any = None) -> Any:
    """
    Choose an element from a sequence with sacred randomness.
    
    Args:
        sequence: The collection to choose from
        default: Value to return if sequence is empty
        
    Returns:
        A randomly chosen element, or the default
    """
    seq_list = list(sequence)
    if not seq_list:
        return default
    return random.choice(seq_list)


def norm_key(text: str) -> str:
    """
    Normalize a string into a sacred symbolic key.
    
    Converts to uppercase, replaces non-alphanumeric characters with underscores,
    ensuring the result is suitable for symbolic identification.
    
    Args:
        text: The text to normalize
        
    Returns:
        A normalized symbolic key
    """
    cleaned = re.sub(r"[^A-Z0-9_]+", "_", (text or "").strip().upper())
    return cleaned.strip("_")  # Remove leading/trailing underscores


def uniq(sequence: Iterable[Any]) -> List[Any]:
    """
    Remove duplicates while preserving sacred order.
    
    Args:
        sequence: The collection to deduplicate
        
    Returns:
        List with duplicates removed, in original order
    """
    seen = set()
    result = []
    
    for item in sequence:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result


def text_snippet(text: str, max_length: int = 120) -> str:
    """
    Extract a meaningful snippet from sacred text.
    
    Args:
        text: The text to snippet
        max_length: Maximum length of the snippet
        
    Returns:
        The snippet, truncated with ellipsis if necessary
    """
    if not text:
        return ""
    
    cleaned = text.strip().replace("\n", " ")
    
    if len(cleaned) <= max_length:
        return cleaned
    
    return cleaned[:max_length - 1] + "…"


def weighted_pick(weighted_items: Sequence[Tuple[Any, int]], default: Any = None) -> Any:
    """
    Choose an element based on sacred weights.
    
    Args:
        weighted_items: Sequence of (item, weight) tuples
        default: Value to return if no items or all weights zero
        
    Returns:
        The chosen item, weighted by its sacred significance
    """
    if not weighted_items:
        return default
    
    # Calculate total weight, ensuring all weights are non-negative
    total_weight = sum(max(weight, 0) for _, weight in weighted_items)
    
    if total_weight <= 0:
        return default
    
    # Choose based on weighted probability
    selection = random.randint(1, total_weight)
    cumulative = 0
    
    for item, weight in weighted_items:
        cumulative += max(weight, 0)
        if selection <= cumulative:
            return item
    
    return default


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries with sacred precedence.
    
    Later dictionaries override earlier ones in case of key conflicts.
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        The merged dictionary
    """
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


def deep_get(dictionary: Dict[str, Any], path: str, default: Any = None, separator: str = ".") -> Any:
    """
    Retrieve a value from nested dictionaries using dot notation.
    
    Args:
        dictionary: The dictionary to search
        path: Dot-separated path to the value
        default: Value to return if path not found
        separator: Path separator (default: ".")
        
    Returns:
        The value at the path, or default if not found
    """
    keys = path.split(separator)
    current = dictionary
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to an integer.
    
    Args:
        value: The value to convert
        default: Value to return if conversion fails
        
    Returns:
        The integer value, or default if conversion fails
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_str(value: Any, default: str = "") -> str:
    """
    Safely convert a value to a string.
    
    Args:
        value: The value to convert
        default: Value to return if conversion fails
        
    Returns:
        The string value, or default if conversion fails
    """
    try:
        return str(value)
    except (ValueError, TypeError):
        return default


class SacredTimer:
    """A simple timer for measuring sacred durations."""
    
    def __init__(self) -> None:
        """Initialize the timer."""
        self.start_time = None
        self.end_time = None
    
    def start(self) -> None:
        """Start the timer."""
        self.start_time = random.time.time()
        self.end_time = None
    
    def stop(self) -> float:
        """Stop the timer and return duration."""
        self.end_time = random.time.time()
        return self.duration()
    
    def duration(self) -> float:
        """Get the current duration."""
        if self.start_time is None:
            return 0.0
        
        end = self.end_time or random.time.time()
        return end - self.start_time
    
    def reset(self) -> None:
        """Reset the timer."""
        self.start_time = None
        self.end_time = None
