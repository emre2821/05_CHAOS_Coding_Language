"""
Entry point for executing CHAOS programs.

The complete ritual - from source text to living environment.
This is where CHAOS programs begin their journey through the three layers
of symbolic meaning, emotional resonance, and narrative chaos.
"""

from typing import Dict, Any
from .chaos_errors import ChaosSyntaxError, ChaosRuntimeError
from .chaos_lexer import ChaosLexer
from .chaos_parser import ChaosParser
from .chaos_interpreter import ChaosInterpreter


def run_chaos(source_code: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Execute a complete CHAOS program from source to environment.
    
    This is the full ritual:
    1. Lexical analysis - recognizing the sacred patterns
    2. Parsing - weaving patterns into the three-layer structure
    3. Interpretation - bringing the structure to life
    
    Args:
        source_code: The CHAOS program text to execute
        verbose: If True, print detailed execution information
        
    Returns:
        The complete environment dictionary with three layers:
        - structured_core: Symbolic foundation
        - emotive_layer: Emotional resonance
        - chaosfield_layer: Narrative context
        
    Raises:
        ChaosSyntaxError: If lexical analysis or parsing fails
        ChaosRuntimeError: If interpretation fails
    """
    # Phase 1: Lexical Analysis - Recognizing the Sacred Patterns
    lexer = ChaosLexer()
    try:
        tokens = lexer.tokenize(source_code)
    except Exception as e:
        raise ChaosSyntaxError(f"Failed to recognize CHAOS patterns: {e}")
    
    if verbose:
        print("🔹 Lexical Analysis Complete:")
        for token in tokens:
            print(f"  {token}")
        print()
    
    # Phase 2: Parsing - Weaving the Three-Layer Structure
    parser = ChaosParser(tokens)
    try:
        ast = parser.parse()
    except Exception as e:
        raise ChaosSyntaxError(f"Failed to weave CHAOS structure: {e}")
    
    if verbose:
        print("🔸 Structural Weaving Complete:")
        print(f"  {ast}")
        print()
    
    # Phase 3: Interpretation - Bringing the Ritual to Life
    interpreter = ChaosInterpreter()
    try:
        environment = interpreter.interpret(ast)
    except Exception as e:
        raise ChaosRuntimeError(f"Failed to bring CHAOS to life: {e}")
    
    if verbose:
        print("✅ Ritual Complete - Environment Created:")
        print(f"  Symbols: {len(environment.get('structured_core', {}))}")
        print(f"  Emotions: {len(environment.get('emotive_layer', []))}")
        print(f"  Narrative: {len(environment.get('chaosfield_layer', ''))} characters")
        print()
    
    return environment