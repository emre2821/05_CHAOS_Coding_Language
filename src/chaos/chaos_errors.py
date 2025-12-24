"""
Defines CHAOS exception classes grouped by failure mode.

Each error type carries the symbolic weight of CHAOS - not just technical
failures, but moments where the ritual of code encounters resistance.
These exceptions honor the emotional journey of programming.
"""


class ChaosError(Exception):
    """Base error for all CHAOS exceptions.
    
    The root of all CHAOS failures - when the symbolic and emotional
    layers cannot maintain their harmony with the structured core.
    """
    pass


class ChaosSyntaxError(ChaosError):
    """Raised during tokenization or parsing issues.
    
    When the ritual words are spoken incorrectly, when the symbolic
    tags lose their resonance, when the layers cannot be properly
    distinguished from one another.
    """
    pass


class ChaosRuntimeError(ChaosError):
    """Raised during interpretation or execution.
    
    The moment when theory becomes practice and the emotional weight
    becomes too heavy for the current symbolic structure to bear.
    """
    pass


class ChaosValidationError(ChaosError):
    """Raised during static pre-validation of CHAOS structure.
    
    Before the ritual begins, the sacred geometry must be verified.
    This error speaks of incomplete ceremonies and broken patterns.
    """
    pass


class ChaosSymbolError(ChaosError):
    """Raised when an unknown or illegal symbol is used.
    
    When the language of symbols fails, when meaning becomes corrupted,
    when the emotional resonance cannot find its anchor in the structured core.
    """
    pass


class ChaosEmotionError(ChaosError):
    """Raised for invalid emotion-related constructs.
    
    The heart of CHAOS speaks in emotions, but sometimes the emotional
    grammar becomes too complex, too intense, or loses its connection
    to the symbolic foundation.
    """
    pass


class ChaosGraphError(ChaosError):
    """Raised when symbolic graph operations fail.
    
    When the web of relationships between symbols becomes tangled,
    when connections cannot be formed or maintained, when the network
    of meaning begins to unravel.
    """
    pass