# CHAOS API Reference

This document provides a comprehensive reference for the CHAOS Python API.

## Core Modules

### `run_chaos(source: str, verbose: bool = False) -> Dict[str, Any]`

The primary entry point for executing CHAOS scripts.

**Parameters:**
- `source` — The CHAOS script source code as a string
- `verbose` — If `True`, prints debug information during execution

**Returns:**
A dictionary with three keys:
- `structured_core` — Key-value pairs from `[KEY]: value` tags
- `emotive_layer` — List of emotion dictionaries with `name` and `intensity`
- `chaosfield_layer` — The narrative text from `{ }` blocks

**Example:**
```python
from chaos_language import run_chaos

source = """
[EVENT]: memory
[EMOTION:JOY:7]
{ The garden was alive. }
"""

env = run_chaos(source)
print(env["structured_core"])  # {'EVENT': 'memory'}
print(env["emotive_layer"])    # [{'name': 'JOY', 'intensity': 7}]
print(env["chaosfield_layer"]) # 'The garden was alive.'
```

---

### `validate_chaos(source: str) -> None`

Validates a CHAOS script without executing it. Raises `ChaosValidationError` if
the script is malformed.

**Parameters:**
- `source` — The CHAOS script source code

**Raises:**
- `ChaosValidationError` — If validation fails

**Validation Rules:**
- Script must contain at least one structured core pair (`[KEY]: value`)
- Emotion intensities must be in range 0-10
- Narrative blocks must contain text (not empty `{}`)

**Example:**
```python
from chaos_language import validate_chaos, ChaosValidationError

try:
    validate_chaos("[EVENT]: test\n[EMOTION:JOY:15]\n{ Text }")
except ChaosValidationError as e:
    print(f"Invalid: {e}")  # Emotion intensity out of bounds
```

---

## Lexer & Parser

### `ChaosLexer`

Tokenizes CHAOS source code into a stream of tokens.

**Methods:**
- `tokenize(source: str) -> List[Token]` — Convert source to token list

**Example:**
```python
from chaos_language import ChaosLexer

lexer = ChaosLexer()
tokens = lexer.tokenize("[EVENT]: memory")
for token in tokens:
    print(f"{token.type.name}: {token.value}")
```

### `ChaosParser`

Parses a token stream into a three-layer AST.

**Methods:**
- `parse() -> Node` — Returns the root `PROGRAM` node with children:
  - `STRUCTURED_CORE` — Contains key-value pairs
  - `EMOTIVE_LAYER` — Contains emotion entries
  - `CHAOSFIELD_LAYER` — Contains narrative text

---

## Agent System

### `ChaosAgent`

An emotion-aware agent that processes scripts and text, maintains memory,
and executes protocols.

**Constructor:**
```python
ChaosAgent(name: str, *, seed: Optional[int] = None)
```

**Parameters:**
- `name` — Agent identifier
- `seed` — Optional random seed for deterministic dream generation

**Methods:**

#### `step(*, text: Optional[str] = None, sn: Optional[str] = None) -> AgentReport`

Process input and advance the agent state.

**Parameters:**
- `text` — Free-form text input for emotion triggering
- `sn` — CHAOS script source to process

**Returns:**
`AgentReport` with:
- `emotions` — Current active emotions
- `symbols` — Known symbols
- `narrative` — Current narrative context
- `action` — Recommended protocol action (if any)
- `dreams` — Generated dream visions
- `log` — Agent activity log

#### `perceive_text(text: str) -> None`

Trigger emotions from free-form text.

#### `perceive_sn(source: str) -> None`

Process a CHAOS script into agent memory.

#### `reflect() -> List[str]`

Generate dream visions based on current state.

#### `decide() -> Optional[Action]`

Evaluate protocols and return recommended action.

**Example:**
```python
from chaos_language import ChaosAgent

agent = ChaosAgent("Concord", seed=42)
report = agent.step(
    text="warmth and ocean breeze",
    sn="[EVENT]: reflection\n[EMOTION:HOPE:6]\n{ Finding peace. }"
)

print(report.emotions)  # Active emotions
print(report.action)    # Protocol recommendation
print(report.dreams)    # Generated visions
```

---

## Emotion Engine

### `ChaosEmotionStack`

Stack-based emotion processor with keyword triggers and transitions.

**Methods:**

#### `push(name: str, intensity: int) -> None`
Add an emotion to the stack.

#### `current() -> Optional[Emotion]`
Get the top emotion.

#### `trigger_from_text(text: str) -> None`
Scan text for keywords and push matching emotions.

#### `transition() -> None`
Apply emotion transition rules (e.g., FEAR → HOPE).

#### `decay_all(amount: int = 1) -> None`
Reduce all emotion intensities.

#### `summary() -> List[str]`
Get string representations of active emotions.

**Built-in Triggers:**
| Keyword | Emotion | Intensity |
|---------|---------|-----------|
| safe | CALM | 6 |
| momma | NOSTALGIA | 8 |
| disconnected | ANXIETY | 7 |
| warmth | LOVE | 7 |
| loss | GRIEF | 9 |
| ocean | WONDER | 5 |
| dark | FEAR | 6 |

**Built-in Transitions:**
- FEAR → HOPE
- HOPE → LOVE
- LOVE → GRIEF
- GRIEF → WISDOM

---

## Business Reports

### `generate_business_report(env: Dict) -> Dict[str, Any]`

Generate a business-friendly report from interpreter output.

**Parameters:**
- `env` — Output from `run_chaos()`

**Returns:**
Dictionary with:
- `structured` — Key-value data
- `top_emotion` — Highest intensity emotion
- `emotion_summary` — All emotions with intensities
- `narrative_snippet` — Truncated narrative
- `recommendations` — Contextual suggestions

### `render_report_lines(report: Dict) -> List[str]`

Convert a report to human-readable lines.

**Example:**
```python
from chaos_language import run_chaos, generate_business_report, render_report_lines

env = run_chaos("[ACCOUNT]: A-19\n[EMOTION:JOY:8]\n{ Positive momentum. }")
report = generate_business_report(env)
for line in render_report_lines(report):
    print(line)
```

---

## Error Handling

### Exception Hierarchy

```
ChaosError (base)
├── ChaosSyntaxError      — Lexer/parser errors
├── ChaosRuntimeError     — Interpreter errors
├── ChaosValidationError  — Validation failures
├── ChaosSymbolError      — Unknown symbols
├── ChaosEmotionError     — Invalid emotion constructs
└── ChaosGraphError       — Graph operation failures
```

**Example:**
```python
from chaos_language import run_chaos, ChaosError

try:
    env = run_chaos("{ missing structured core }")
except ChaosError as e:
    print(f"CHAOS error: {e}")
```

---

## Type Reference

### Token
```python
@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
```

### Emotion
```python
@dataclass
class Emotion:
    name: str        # Uppercase emotion name
    intensity: int   # 0-10
    timestamp: datetime
```

### Action
```python
@dataclass
class Action:
    kind: str                    # 'stabilize', 'transform', 'relate'
    payload: Dict[str, Any]      # Context-specific data
```

### AgentReport
```python
@dataclass
class AgentReport:
    emotions: List[Dict[str, Any]]
    symbols: Dict[str, Any]
    narrative: str
    action: Optional[Action]
    dreams: List[str]
    log: str
```

---

## CLI Reference

### chaos-cli

```bash
# Run a script
chaos-cli <script.sn> [--json]

# Interactive REPL
chaos-cli
```

### chaos-exec

```bash
# Execute with report
chaos-exec <script.sn> [--report] [--emit <output.json>]

# Execute with agent mode
chaos-exec <script.sn> --agent
```

### chaos-agent

```bash
# Start agent REPL
chaos-agent [--name <agent_name>]
```

**Agent Commands:**
- `:open <path>` — Load a `.sn` file
- `:dreams` — Show generated visions
- `:emotions` — Show active emotions
- `:symbols` — Show known symbols
- `:action` — Show last recommended action
- `:clear` — Clear narrative context
- `:help` — Show help
- `:quit` — Exit

---

*For more examples, see the `artifacts/corpus_sn/` directory and the test suite.*
