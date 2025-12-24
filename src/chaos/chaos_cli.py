"""
CHAOS Shell and script runner - the gateway to symbolic-emotional computation.

This module provides the command-line interface for running CHAOS programs,
offering both interactive shell mode and script execution capabilities.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .chaos_runtime import run_chaos
from .chaos_lexer import ChaosLexer
from .chaos_parser import ChaosParser
from .chaos_interpreter import ChaosInterpreter


def run_chaos_with_options(code: str, show_tokens: bool = False, 
                          show_ast: bool = False, output_json: bool = False) -> None:
    """
    Execute CHAOS code with optional debugging output.
    
    Args:
        code: The CHAOS source code to execute
        show_tokens: If True, display the token stream
        show_ast: If True, display the parse tree
        output_json: If True, output the environment as JSON
    """
    # Tokenization phase
    lexer = ChaosLexer()
    tokens = lexer.tokenize(code)
    
    if show_tokens:
        print("\n🧱 Sacred Tokens:")
        for token in tokens:
            print(f"  {token}")
    
    # Parsing phase
    parser = ChaosParser(tokens)
    ast = parser.parse()
    
    if show_ast:
        print("\n🌳 Parse Tree:")
        print(f"  {ast}")
    
    # Interpretation phase
    interpreter = ChaosInterpreter()
    environment = interpreter.interpret(ast)
    
    # Output results
    print("\n🧠 CHAOS Environment Created:")
    if output_json:
        print(json.dumps(environment, indent=2))
    else:
        for key, value in environment.items():
            print(f"  {key}: {value}")


def main() -> None:
    """Main entry point for the CHAOS CLI."""
    parser = argparse.ArgumentParser(
        description="CHAOS: A Symbolic-Emotional Programming Language",
        epilog="Examples:\n"
               "  chaos script.sn              # Run a CHAOS script\n"
               "  chaos --tokens script.sn     # Run with token display\n"
               "  chaos --ast script.sn        # Run with AST display\n"
               "  chaos                        # Start interactive shell\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "path", 
        nargs="?", 
        help="Path to a CHAOS script (.sn or .chaos)"
    )
    parser.add_argument(
        "--tokens", 
        action="store_true", 
        help="Show the token stream during execution"
    )
    parser.add_argument(
        "--ast", 
        action="store_true", 
        help="Show the parse tree during execution"
    )
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output the environment as JSON"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="CHAOS 2.0.0 - Symbolic-Emotional Programming Language"
    )
    
    args = parser.parse_args()
    
    # Script execution mode
    if args.path:
        script_path = Path(args.path)
        
        # Validate file extension
        if script_path.suffix.lower() not in [".sn", ".chaos"]:
            parser.error("CHAOS scripts must use .sn or .chaos extension")
        
        # Check file existence
        if not script_path.exists():
            print(f"💥 File not found: {script_path}", file=sys.stderr)
            sys.exit(1)
        
        # Read script
        try:
            source = script_path.read_text(encoding="utf-8")
        except OSError as err:
            print(f"💥 Could not read {script_path}: {err}", file=sys.stderr)
            sys.exit(1)
        
        # Execute with options
        try:
            run_chaos_with_options(source, args.tokens, args.ast, args.json)
        except Exception as err:
            print(f"💥 CHAOS execution failed: {err}", file=sys.stderr)
            sys.exit(1)
        
        return
    
    # Interactive shell mode
    print("🌌 CHAOS Interactive Shell (type 'exit' to quit)")
    print("   Enter CHAOS code and press Enter twice to execute")
    print("   Use /help for shell commands")
    print()
    
    buffer = []
    
    while True:
        try:
            line = input("CHAOS> ")
            
            # Shell commands
            if line.strip().startswith("/"):
                command = line.strip()[1:].lower()
                
                if command == "exit" or command == "quit":
                    print("\n✨ Leaving the realm of CHAOS...")
                    break
                elif command == "help":
                    print("\nCHAOS Shell Commands:")
                    print("  /exit, /quit  - Leave the CHAOS shell")
                    print("  /help         - Show this help")
                    print("  /clear        - Clear the current buffer")
                    print("  /tokens       - Toggle token display")
                    print("  /ast          - Toggle AST display")
                    print("  /json         - Toggle JSON output")
                    print()
                    continue
                elif command == "clear":
                    buffer.clear()
                    print("Buffer cleared.")
                    continue
                elif command == "tokens":
                    args.tokens = not args.tokens
                    print(f"Token display: {'ON' if args.tokens else 'OFF'}")
                    continue
                elif command == "ast":
                    args.ast = not args.ast
                    print(f"AST display: {'ON' if args.ast else 'OFF'}")
                    continue
                elif command == "json":
                    args.json = not args.json
                    print(f"JSON output: {'ON' if args.json else 'OFF'}")
                    continue
                else:
                    print(f"Unknown command: {command} (use /help for options)")
                    continue
            
            # Execute buffer on empty line
            if line.strip() == "":
                if buffer:
                    code = "\n".join(buffer)
                    
                    try:
                        run_chaos_with_options(code, args.tokens, args.ast, args.json)
                    except Exception as e:
                        print(f"💥 Error: {e}")
                    
                    buffer.clear()
                    print()  # Extra newline after execution
                continue
            
            # Add line to buffer
            buffer.append(line)
            
        except KeyboardInterrupt:
            print("\n\n✨ CHAOS shell interrupted. Goodbye.")
            break
        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            buffer.clear()


if __name__ == "__main__":
    main()