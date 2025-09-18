# chaos_errors.py

class ChaosError(Exception):
    """Base error for all CHAOS exceptions."""
    pass

class ChaosSyntaxError(ChaosError):
    """Raised during tokenization or parsing issues."""
    pass

class ChaosRuntimeError(ChaosError):
    """Raised during interpretation or execution."""
    pass

class ChaosValidationError(ChaosError):
    """Raised during static pre-validation of CHAOS structure."""
    pass

class ChaosSymbolError(ChaosError):
    """Raised when an unknown or illegal symbol is used."""
    pass

class ChaosEmotionError(ChaosError):
    """Raised for invalid emotion-related constructs."""
    pass

class ChaosGraphError(ChaosError):
    """Raised when symbolic graph operations fail."""
    pass
