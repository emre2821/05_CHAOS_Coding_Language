"""CHAOS language support package.

CHAOS (Contextual Harmonics and Operational Stories) is a narrative-first scripting
language for organizations that want to capture structured telemetry, emotional
signals, and qualitative story fragments in a single artifact.
"""

from .chaos_lexer import ChaosLexer, TokenType, Token
from .chaos_parser import ChaosParser
from .chaos_interpreter import ChaosInterpreter
from .chaos_runtime import run_chaos
from .chaos_validator import validate_chaos
from .chaos_agent import ChaosAgent
from .chaos_reports import generate_business_report, render_report_lines
from .chaos_emotion import ChaosEmotionStack
from .chaos_context import ChaosContext
from .chaos_errors import ChaosError, ChaosSyntaxError, ChaosValidationError

__version__ = "0.1.0"

__all__ = [
    "ChaosLexer",
    "TokenType",
    "Token",
    "ChaosParser",
    "ChaosInterpreter",
    "run_chaos",
    "validate_chaos",
    "ChaosAgent",
    "generate_business_report",
    "render_report_lines",
    "ChaosEmotionStack",
    "ChaosContext",
    "ChaosError",
    "ChaosSyntaxError",
    "ChaosValidationError",
]
