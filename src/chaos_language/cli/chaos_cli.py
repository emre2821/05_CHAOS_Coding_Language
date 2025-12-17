# chaos_cli.py

import argparse
import json
import sys
from pathlib import Path

from chaos_language import ChaosLexer, ChaosParser, ChaosInterpreter
from chaos_language.cli.packaged_scripts import resolve_packaged_script


def run_chaos(code, show_tokens=False, show_ast=False, output_json=False):
    lexer = ChaosLexer()
    tokens = lexer.tokenize(code)

    if show_tokens:
        print("\n🧱 Tokens:")
        for t in tokens:
            print(t)

    parser = ChaosParser(tokens)
    ast = parser.parse()

    if show_ast:
        print("\n🌳 AST:")
        print(ast)

    interpreter = ChaosInterpreter()
    interpreter.interpret(ast)

    print("\n🧠 Final CHAOS Environment:")
    if output_json:
        print(json.dumps(interpreter.environment, indent=2))
    else:
        for k, v in interpreter.environment.items():
            print(f"{k}: {v}")

def main():
    parser = argparse.ArgumentParser(description="CHAOS Shell and script runner")
    parser.add_argument("path", nargs="?", help="Path to a CHAOS script (.sn)")
    parser.add_argument("--tokens", action="store_true", help="Show token list")
    parser.add_argument("--ast", action="store_true", help="Show AST output")
    parser.add_argument("--json", action="store_true", help="Output environment as JSON")
    args = parser.parse_args()

    if args.path:
        script_path = Path(args.path)
        if script_path.suffix.lower() != ".sn":
            parser.error("CHAOS scripts must use the .sn extension")

        resolved_path = script_path
        if not script_path.exists():
            packaged_script = resolve_packaged_script(script_path)
            if packaged_script is None:
                print(f"💥 File not found: {script_path}")
                sys.exit(1)
            resolved_path = packaged_script

        try:
            source = resolved_path.read_text(encoding="utf-8")
        except OSError as err:
            print(f"💥 Could not read {script_path}: {err}")
            sys.exit(1)

        try:
            run_chaos(source, args.tokens, args.ast, args.json)
        except Exception as err:
            print(f"💥 Error: {err}")
            sys.exit(1)
        return

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
