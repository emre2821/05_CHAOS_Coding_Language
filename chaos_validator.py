"""
Preflight: tokenizes + parses and checks for 3 layers.
"""
from chaos_errors import ChaosValidationError
from chaos_lexer import ChaosLexer
from chaos_parser import ChaosParser


def validate_chaos(source: str) -> None:
    try:
        tokens = ChaosLexer().tokenize(source)
        ast = ChaosParser(tokens).parse()
        if not ast or not ast.children or len(ast.children) != 3:
            raise ChaosValidationError(
                "Expected 3 layers in CHAOS: structured_core, emotive_layer, chaosfield_layer"
            )
    except Exception as exc:
        raise ChaosValidationError(f"CHAOS Validation Failed: {exc}") from exc
