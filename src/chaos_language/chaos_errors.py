"""
Defines CHAOS exception classes grouped by failure mode.
"""


class ChaosError(Exception):
    """Base error for all CHAOS exceptions."""


class ChaosSyntaxError(ChaosError):
    """Raised during tokenization or parsing issues."""


class ChaosRuntimeError(ChaosError):
    """Raised during interpretation or execution."""


class ChaosValidationError(ChaosError):
    """Raised during static pre-validation of CHAOS structure."""


class ChaosSymbolError(ChaosError):
    """Raised when an unknown or illegal symbol is used."""


class ChaosEmotionError(ChaosError):
    """Raised for invalid emotion-related constructs."""


class ChaosGraphError(ChaosError):
    """Raised when symbolic graph operations fail."""
