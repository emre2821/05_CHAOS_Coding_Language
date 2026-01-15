# Debugging & Logging Guide

This guide covers debugging and logging strategies for CHAOS development.

## Verbose Mode

### Runtime Verbose Output

Enable verbose mode when running scripts to see tokens and AST:

```python
from chaos_language import run_chaos

env = run_chaos(source, verbose=True)
```

This outputs:
- 🔹 Tokens — Raw token stream from the lexer
- 🔸 AST — Parsed abstract syntax tree
- ✅ ENV — Final execution environment

### CLI Verbose Options

```bash
# Show tokens during script execution
chaos-cli script.sn --tokens

# Show AST during script execution
chaos-cli script.sn --ast

# Combine options
chaos-cli script.sn --tokens --ast --json
```

## Logging

### Using ChaosLogger

The built-in logger tracks agent activity with timestamps:

```python
from chaos_language.chaos_logger import ChaosLogger

logger = ChaosLogger()
logger.log("Custom message")
logger.log_symbol("KEY", "value")
logger.log_emotion("JOY:8")
logger.log_narrative("The garden bloomed...")

# Export all logs
print(logger.export())
```

### Agent Activity Logs

Access the agent's internal log after operations:

```python
from chaos_language import ChaosAgent

agent = ChaosAgent("Debug")
report = agent.step(sn="[EVENT]: test\n[EMOTION:JOY:5]\n{ Hello }")

# View activity log
print(report.log)
```

## Debugging Strategies

### Isolate Layers

Test each layer independently:

```python
from chaos_language import ChaosLexer, ChaosParser, ChaosInterpreter

# Step 1: Tokenize
lexer = ChaosLexer()
tokens = lexer.tokenize(source)
print("Tokens:", [t.type.name for t in tokens])

# Step 2: Parse
parser = ChaosParser(tokens)
ast = parser.parse()
print("AST children:", len(ast.children))

# Step 3: Interpret
interpreter = ChaosInterpreter()
env = interpreter.interpret(ast)
print("Environment:", env.keys())
```

### Validate Before Execute

Always validate scripts before running them:

```python
from chaos_language import validate_chaos, run_chaos, ChaosValidationError

try:
    validate_chaos(source)
    env = run_chaos(source)
except ChaosValidationError as e:
    print(f"Validation failed: {e}")
```

### Corpus Fuzzing

Run all corpus files through the validator:

```bash
python tools/cli_shims/chaos_fuzz.py
```

## Common Issues

### "Structured core required"
- Ensure your script has at least one `[KEY]: value` pair before emotions

### "Emotion intensity out of bounds"
- Intensity must be between 0 and 10

### "Narrative text required"
- The `{ }` block cannot be empty

### Import Errors
- Ensure PYTHONPATH includes the `src` directory:
  ```bash
  export PYTHONPATH=src:$PYTHONPATH
  ```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CHAOS_LOG_LEVEL` | Log verbosity | INFO |
| `CHAOS_OUTPUT_DIR` | Report output path | ./output |
| `CHAOS_DEBUG` | Enable debug mode | false |

See `.env.example` for all available options.

## IDE Setup

### VS Code

Add to `.vscode/settings.json`:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.envFile": "${workspaceFolder}/.env"
}
```

### Debug Configuration

Add to `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug CHAOS Script",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/tools/cli_shims/chaos_cli.py",
      "args": ["${file}", "--tokens", "--ast"],
      "cwd": "${workspaceFolder}",
      "env": {"PYTHONPATH": "${workspaceFolder}/src"}
    }
  ]
}
```

---

*For additional help, see the [API Reference](API_REFERENCE.md) or open an issue.*
