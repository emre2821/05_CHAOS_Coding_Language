"""
CHAOS: A Symbolic-Emotional Programming Language

A language that bridges the technical and the poetic, where code becomes ritual
and syntax carries emotional resonance. Built for EdenOS with mythic depth.

This package provides the core interpreter, emotional engine, and symbolic
processing capabilities that make CHAOS unique among programming languages.
"""

from .chaos_runtime import run_chaos
from .chaos_interpreter import ChaosInterpreter
from .chaos_lexer import ChaosLexer, TokenType, Token
from .chaos_parser import ChaosParser, NodeType, Node
from .chaos_errors import (
    ChaosError,
    ChaosSyntaxError,
    ChaosRuntimeError,
    ChaosValidationError,
    ChaosSymbolError,
    ChaosEmotionError,
    ChaosGraphError,
)
from .chaos_agent import ChaosAgent
from .chaos_emotion import ChaosEmotionStack, Emotion
from .chaos_context import ChaosContext
from .chaos_dreams import DreamEngine

__version__ = "2.0.0"
__author__ = "CHAOS Community"
__license__ = "MIT"

__all__ = [
    # Core runtime
    "run_chaos",
    "ChaosInterpreter",
    "ChaosLexer",
    "ChaosParser",
    
    # Token types
    "TokenType",
    "Token",
    "NodeType",
    "Node",
    
    # Error hierarchy
    "ChaosError",
    "ChaosSyntaxError",
    "ChaosRuntimeError",
    "ChaosValidationError",
    "ChaosSymbolError",
    "ChaosEmotionError",
    "ChaosGraphError",
]