# chaos_cli.py

from chaos_lexer import ChaoLexer
from chaos_parser import ChaoParser
from chaos_interpreter import ChaoInterpreter

import argparse
import json

def run_chaos(code, show_tokens=False, show_ast=False, output_json=False):
    lexer = ChaoLexer()
    tokens = lexer.tokenize(code)

    if show_tokens:
        print("\n🧱 Tokens:")
        for t in tokens:
            print(t)

    parser = ChaoParser(tokens)
    ast = parser.parse()

    if show_ast:
        print("\n🌳 AST:")
        print(ast)

    interpreter = ChaoInterpreter()
    interpreter.interpret(ast)

    print("\n🧠 Final CHAOS Environment:")
    if output_json:
        print(json.dumps(interpreter.environment, indent=2))
    else:
        for k, v in interpreter.environment.items():
            print(f"{k}: {v}")

def main():
    parser = argparse.ArgumentParser(description="CHAOS Interactive Shell")
    parser.add_argument("--tokens", action="store_true", help="Show token list")
    parser.add_argument("--ast", action="store_true", help="Show AST output")
    parser.add_argument("--json", action="store_true", help="Output environment as JSON")
    args = parser.parse_args()

    print("CHAOS Shell 🌌 (type 'exit' to quit)")
    buffer = []

    while True:
        try:
            line = input("CHAOS> ")
            if line.strip().lower() == "exit":
                break
            if line.strip() == "":
                if buffer:
                    code = "\n".join(buffer)
                    run_chaos(code, args.tokens, args.ast, args.json)
                    buffer = []
                continue
            buffer.append(line)
        except KeyboardInterrupt:
            print("\nExiting CHAOS.")
            break
        except Exception as e:
            print(f"💥 Error: {e}")
            buffer = []

if __name__ == "__main__":
    main()
