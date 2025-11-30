# CHAOS Language Package

This is the main Python package for the CHAOS (Contextual Harmonics and Operational Stories) scripting language.

## Modules

- **chaos_lexer.py** - Tokenizes CHAOS syntax into typed tokens
- **chaos_parser.py** - Produces the three-layer abstract syntax tree
- **chaos_interpreter.py** - Walks the AST into the runtime environment
- **chaos_runtime.py** - High-level helper that runs lexer → parser → interpreter
- **chaos_validator.py** - Preflight validation to guarantee all three layers exist
- **chaos_agent.py** - Emotion-aware agent orchestrating dreams and protocols
- **chaos_reports.py** - Business-facing environment reporting utilities
- **chaos_emotion.py** - Stack-based emotion engine with triggers and transitions
- **chaos_context.py** - Context management for agent state
- **chaos_dreams.py** - Dream engine for generating visions from state
- **chaos_protocols.py** - Oaths, rituals, and contracts with scoring
- **chaos_graph.py** - Undirected lightweight graph for symbols/entities
- **chaos_logger.py** - Logging utilities for CHAOS operations
- **chaos_stdlib.py** - Standard library utilities
- **chaos_errors.py** - Exception classes for CHAOS failures

## Usage

```python
from chaos_language import ChaosLexer, ChaosParser, ChaosInterpreter, run_chaos

# Run a CHAOS script
env = run_chaos(source_code)

# Or use components directly
tokens = ChaosLexer().tokenize(source_code)
ast = ChaosParser(tokens).parse()
env = ChaosInterpreter().interpret(ast)
```
