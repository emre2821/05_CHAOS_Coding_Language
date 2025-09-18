"""
Entry point for executing CHAOS programs.
"""
from typing import Dict, Any

from chaos_errors import ChaosSyntaxError, ChaosRuntimeError
from chaos_lexer import ChaosLexer
from chaos_parser import ChaosParser
from chaos_interpreter import ChaosInterpreter


def run_chaos(source_code: str, verbose: bool = False) -> Dict[str, Any]:
    lexer = ChaosLexer()
    try:
        tokens = lexer.tokenize(source_code)
    except Exception as exc:
        raise ChaosSyntaxError(f"Lexer error: {exc}") from exc

    if verbose:
        print("🔹 Tokens:")
        for token in tokens:
            print(token)

    parser = ChaosParser(tokens)
    try:
        ast = parser.parse()
    except Exception as exc:
        raise ChaosSyntaxError(f"Parser error: {exc}") from exc

    if verbose:
        print("🔸 AST:")
        print(ast)

    interpreter = ChaosInterpreter()
    try:
        env = interpreter.interpret(ast)
    except Exception as exc:
        raise ChaosRuntimeError(f"Interpreter error: {exc}") from exc

    if verbose:
        print("✅ ENV:")
        print(env)

    return env
