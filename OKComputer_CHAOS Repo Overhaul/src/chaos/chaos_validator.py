"""
Preflight: tokenizes + parses and checks for 3 layers.

The guardian of CHAOS integrity - ensuring that programs maintain
the sacred three-layer structure before they are brought to life
through execution.
"""

from .chaos_errors import ChaosValidationError
from .chaos_lexer import ChaosLexer
from .chaos_parser import ChaosParser


def validate_chaos(source: str) -> None:
    """
    Validate that source code follows CHAOS sacred structure.
    
    This preflight check ensures that:
    1. The lexical patterns are recognizable
    2. The three-layer structure can be parsed
    3. The program honors the CHAOS architecture
    
    Args:
        source: The CHAOS source code to validate
        
    Raises:
        ChaosValidationError: If the program structure is invalid
    """
    try:
        # Phase 1: Lexical validation
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        
        # Phase 2: Structural validation
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        # Phase 3: Architectural validation
        if not ast or not ast.children or len(ast.children) != 3:
            raise ChaosValidationError(
                "CHAOS programs must have exactly three layers: "
                "structured_core, emotive_layer, and chaosfield_layer"
            )
        
        # Validate layer types
        layers = {
            ast.children[0].type: "structured_core",
            ast.children[1].type: "emotive_layer", 
            ast.children[2].type: "chaosfield_layer"
        }
        
        expected_types = ["STRUCTURED_CORE", "EMOTIVE_LAYER", "CHAOSFIELD_LAYER"]
        actual_types = [layer.name for layer in layers.keys()]
        
        if actual_types != expected_types:
            raise ChaosValidationError(
                f"Invalid layer order. Expected {expected_types}, got {actual_types}"
            )
        
    except Exception as e:
        if isinstance(e, ChaosValidationError):
            raise
        raise ChaosValidationError(f"CHAOS validation failed: {e}")


def validate_symbols(symbols: Dict[str, str]) -> None:
    """
    Validate that symbols follow CHAOS naming conventions.
    
    Args:
        symbols: Dictionary of symbolic names and values
        
    Raises:
        ChaosValidationError: If symbols violate naming conventions
    """
    for name, value in symbols.items():
        # Check for valid symbolic names
        if not name or not name[0].isalpha():
            raise ChaosValidationError(
                f"Symbolic name '{name}' must start with a letter"
            )
        
        # Check for valid characters
        if not all(c.isalnum() or c in "_:-" for c in name):
            raise ChaosValidationError(
                f"Symbolic name '{name}' contains invalid characters"
            )


def validate_emotions(emotions: List[Dict[str, Any]]) -> None:
    """
    Validate that emotions have proper structure and values.
    
    Args:
        emotions: List of emotion dictionaries
        
    Raises:
        ChaosValidationError: If emotions are improperly structured
    """
    for i, emotion in enumerate(emotions):
        if not isinstance(emotion, dict):
            raise ChaosValidationError(f"Emotion {i} must be a dictionary")
        
        if "name" not in emotion or "intensity" not in emotion:
            raise ChaosValidationError(
                f"Emotion {i} must have 'name' and 'intensity' keys"
            )
        
        if not isinstance(emotion["intensity"], (int, float)):
            raise ChaosValidationError(
                f"Emotion {i} intensity must be numeric"
            )
        
        if not (0 <= emotion["intensity"] <= 10):
            raise ChaosValidationError(
                f"Emotion {i} intensity must be between 0 and 10"
            )


def validate_chaos_environment(environment: Dict[str, Any]) -> None:
    """
    Validate a complete CHAOS environment.
    
    Args:
        environment: The environment dictionary to validate
        
    Raises:
        ChaosValidationError: If the environment is invalid
    """
    required_keys = ["structured_core", "emotive_layer", "chaosfield_layer"]
    
    for key in required_keys:
        if key not in environment:
            raise ChaosValidationError(f"Missing required environment key: {key}")
    
    # Validate each layer
    validate_symbols(environment["structured_core"])
    validate_emotions(environment["emotive_layer"])
    
    # Validate chaosfield layer
    if not isinstance(environment["chaosfield_layer"], str):
        raise ChaosValidationError("Chaosfield layer must be a string")