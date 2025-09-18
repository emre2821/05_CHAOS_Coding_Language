# chaos_validator.py

from chaos_errors import ChaosValidationError
from chaos_lexer import ChaoLexer
from chaos_parser import ChaoParser

def validate_chaos(source: str) -> None:
    """Raises ChaosValidationError if the CHAOS code is invalid."""
    try:
        lexer = ChaoLexer()
        tokens = lexer.tokenize(source)

        parser = ChaoParser(tokens)
        ast = parser.parse()

        if not ast or not ast.children or len(ast.children) != 3:
            raise ChaosValidationError("Expected 3 layers in CHAOS: structured_core, emotive_layer, chaosfield_layer")
    except Exception as e:
        raise ChaosValidationError(f"CHAOS Validation Failed: {e}")
