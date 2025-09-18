# chaos_runtime.py

from chaos_lexer import ChaoLexer
from chaos_parser import ChaoParser
from chaos_interpreter import ChaoInterpreter
from chaos_errors import ChaosSyntaxError, ChaosRuntimeError

def run_chaos(source_code: str, verbose=False, return_tokens=False):
    lexer = ChaoLexer()
    try:
        tokens = lexer.tokenize(source_code)
    except Exception as e:
        raise ChaosSyntaxError(f"Lexer error: {e}")

    if verbose:
        print("🔹 Tokens:")
        for t in tokens:
            print(t)

    parser = ChaoParser(tokens)
    try:
        ast = parser.parse()
    except Exception as e:
        raise ChaosSyntaxError(f"Parser error: {e}")

    if verbose:
        print("🔸 AST:")
        print(ast)

    interpreter = ChaoInterpreter()
    try:
        interpreter.interpret(ast)
    except Exception as e:
        raise ChaosRuntimeError(f"Interpreter error: {e}")

    if verbose:
        print("✅ CHAOS Runtime Environment:")
        print(interpreter.environment)

    return (interpreter.environment, tokens) if return_tokens else interpreter.environment
