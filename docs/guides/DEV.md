# CHAOS Developer Guide

**Last Updated:** 2025-12-18

Welcome to the CHAOS developer guide. This document provides detailed information about the architecture, development workflow, and technical patterns used in the CHAOS language implementation.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Development Workflow](#development-workflow)
- [Testing Strategy](#testing-strategy)
- [Code Style & Conventions](#code-style--conventions)
- [Debugging & Troubleshooting](#debugging--troubleshooting)
- [Performance Considerations](#performance-considerations)
- [Release Process](#release-process)

## Architecture Overview

CHAOS is built as a **three-layer architecture** that separates structure, emotion, and narrative:

```
┌─────────────────────────────────────────┐
│     Structured Core (Metadata)          │
│   [KEY]: value pairs, [EMOTION:*]       │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      Emotive Layer (Emotions)            │
│   Emotion names, intensities, context    │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Chaosfield Layer (Narrative)           │
│   Free-form text in { } blocks           │
└─────────────────────────────────────────┘
```

### Processing Pipeline

```
.sn file → Lexer → Tokens → Parser → AST → Interpreter → Environment
```

1. **Lexer** (`chaos_lexer.py`) — Tokenizes CHAOS source into structured tokens
2. **Parser** (`chaos_parser.py`) — Builds three-layer AST from tokens
3. **Interpreter** (`chaos_interpreter.py`) — Walks AST, populates environment
4. **Runtime** (`chaos_runtime.py`) — High-level API that orchestrates the pipeline

### Key Design Principles

- **Meaning First** — Structure preserves intent; execution is secondary
- **Ethics Embedded** — Boundaries and consent are first-class concepts
- **Symbolic Preservation** — Motifs, roles, and relationships travel with data
- **Emotion-Aware** — Emotional context isn't metadata—it's structural
- **Human-Readable** — Every artifact must make sense to humans before machines

## Development Environment Setup

### Prerequisites

- **Python 3.9+** (tested on 3.9, 3.10, 3.11, 3.12)
- **pip** (Python package installer)
- **git** (version control)
- **make** (optional, for convenience commands)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language.git
cd 05_CHAOS_Coding_Language

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify installation
pytest -v
make lint
```

### Recommended Tools

- **IDE:** VS Code, PyCharm, or your preferred editor
- **Extensions:** Python, Pylint, pytest
- **Terminal:** Any terminal with UTF-8 support

## Project Structure

```
/
├── src/
│   └── chaos_language/           # Core package
│       ├── __init__.py           # Public API exports
│       ├── chaos_lexer.py        # Tokenization
│       ├── chaos_parser.py       # AST construction
│       ├── chaos_interpreter.py  # AST walking
│       ├── chaos_runtime.py      # High-level runtime
│       ├── chaos_validator.py    # Validation rules
│       ├── chaos_agent.py        # Agent runtime
│       ├── chaos_emotion.py      # Emotion stack management
│       ├── chaos_errors.py       # Custom exceptions
│       ├── chaos_stdlib.py       # Standard library functions
│       └── cli/                  # Command-line interfaces
│           ├── chaos_cli.py      # Interactive shell
│           ├── chaos_exec.py     # Script executor
│           └── chaos_agent_cli.py # Agent REPL
│
├── tests/                        # Test suite
│   ├── test_lexer.py             # Lexer tests
│   ├── test_parser.py            # Parser tests
│   ├── test_interpreter.py       # Interpreter tests
│   ├── test_agent.py             # Agent tests
│   ├── test_integration.py       # End-to-end tests
│   └── conftest.py               # Pytest fixtures
│
├── chaos_corpus/                 # Example .sn artifacts
│   ├── memory_garden.sn
│   ├── stability_call.sn
│   └── ...
│
├── tools/cli_shims/                      # Utility scripts
│   ├── chaos_fuzz.py             # Corpus validation
│   └── README.md
│
├── docs/                         # Documentation
│   ├── API_REFERENCE.md
│   ├── DEBUGGING.md
│   └── ...
│
├── .github/
│   └── workflows/                # CI/CD
│       ├── tests.yml
│       ├── pylint.yml
│       └── codecov.yml
│
├── pyproject.toml                # Project configuration
├── requirements.txt              # Runtime dependencies
├── requirements-dev.txt          # Dev dependencies
├── Makefile                      # Convenience commands
└── README.md                     # Project overview
```

## Core Components

### Lexer (`chaos_lexer.py`)

**Responsibility:** Convert raw CHAOS source text into tokens

**Key classes:**
- `Token` — Data class holding token type and value
- `Lexer` — Main lexer class with tokenization logic

**Token types:**
- `TAG_KEY` — `[KEY]:` format
- `TAG_EMOTION` — `[EMOTION:NAME:INTENSITY]` format
- `TAG_SYMBOL` — `[SYMBOL:...]` format
- `LBRACE`, `RBRACE` — `{` and `}` for narrative blocks
- `TEXT` — Free-form text content

**Usage:**
```python
from chaos_language.chaos_lexer import Lexer

lexer = Lexer(source_code)
tokens = lexer.tokenize()
```

### Parser (`chaos_parser.py`)

**Responsibility:** Build three-layer AST from tokens

**Key classes:**
- `Parser` — Main parser class
- `ASTNode` — Base class for AST nodes
- Various node types for different constructs

**Three layers:**
1. **Structured Core** — Metadata tags
2. **Emotive Layer** — Emotion entries
3. **Chaosfield Layer** — Narrative text

**Usage:**
```python
from chaos_language.chaos_parser import Parser

parser = Parser(tokens)
ast = parser.parse()
```

### Interpreter (`chaos_interpreter.py`)

**Responsibility:** Walk AST and populate runtime environment

**Key classes:**
- `Interpreter` — AST walker
- `Environment` — Runtime state container

**Environment structure:**
```python
{
    'structured_core': {'KEY': 'value', ...},
    'emotive_layer': [{'name': 'JOY', 'intensity': 7}, ...],
    'chaosfield_layer': 'Narrative text content...'
}
```

**Usage:**
```python
from chaos_language.chaos_interpreter import Interpreter

interpreter = Interpreter(ast)
env = interpreter.interpret()
```

### Runtime (`chaos_runtime.py`)

**Responsibility:** High-level API orchestrating lexer → parser → interpreter

**Main function:**
```python
def run_chaos(source: str, verbose: bool = False) -> dict:
    """Execute CHAOS source and return environment."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    return interpreter.interpret()
```

### Validator (`chaos_validator.py`)

**Responsibility:** Preflight checks for CHAOS artifacts

**Validation rules:**
- Required fields present
- Emotion intensity in valid range (0-10)
- Narrative blocks properly closed
- Tag syntax correctness

**Usage:**
```python
from chaos_language.chaos_validator import validate_chaos

validate_chaos(source)  # Raises ChaosValidationError if invalid
```

### Agent (`chaos_agent.py`)

**Responsibility:** Emotion-aware agent runtime with memory and protocol

**Key classes:**
- `ChaosAgent` — Main agent class
- `EmotionStack` — Emotion state management
- `SymbolicMemory` — Memory and context preservation

**Features:**
- Emotional state tracking
- Protocol execution with boundaries
- Consent/refusal handling
- Symbolic memory preservation

## Development Workflow

### 1. Start a Feature

```bash
# Create branch
git checkout -b feature/your-feature-name

# Make sure tests pass before changes
pytest -v
```

### 2. Make Changes

- Edit code in `src/chaos_language/`
- Add/update tests in `tests/`
- Update documentation if needed

### 3. Test Locally

```bash
# Run tests
pytest -v

# Run specific test file
pytest tests/test_lexer.py -v

# Run with coverage
pytest --cov=chaos_language --cov-report=term-missing

# Validate corpus
python tools/cli_shims/chaos_fuzz.py
```

### 4. Lint Code

```bash
# Run linter
make lint

# Or manually
pylint src/chaos_language/ tests/ tools/cli_shims/
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "Add feature: describe what you did"
```

### 6. Push & PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Open pull request on GitHub
# Fill out PR template
```

## Testing Strategy

### Test Categories

1. **Unit Tests** — Test individual components in isolation
   - `test_lexer.py` — Tokenization logic
   - `test_parser.py` — AST construction
   - `test_interpreter.py` — Environment population

2. **Integration Tests** — Test components working together
   - `test_integration.py` — End-to-end script execution
   - `test_agent.py` — Agent with emotion and memory

3. **Corpus Tests** — Validate example artifacts
   - `tools/cli_shims/chaos_fuzz.py` — Ensure all `.sn` files are valid

### Writing Tests

```python
import pytest
from chaos_language import run_chaos

def test_emotion_parsing():
    """Test that emotion tags are correctly parsed."""
    source = "[EMOTION:JOY:7]\n{ Happy text }"
    env = run_chaos(source)
    
    assert len(env['emotive_layer']) == 1
    assert env['emotive_layer'][0]['name'] == 'JOY'
    assert env['emotive_layer'][0]['intensity'] == 7
```

### Test Fixtures

Common fixtures are defined in `conftest.py`:
```python
@pytest.fixture
def sample_artifact():
    """Provide a sample CHAOS artifact for testing."""
    return """
    [EVENT]: memory
    [EMOTION:JOY:7]
    { The garden was alive. }
    """
```

### Coverage Goals

- **Minimum:** 80% code coverage
- **Target:** 90%+ for core modules (lexer, parser, interpreter)

## Code Style & Conventions

### Python Style

Follow **PEP 8** with these adjustments:

- **Line length:** 100 characters (not 79)
- **Docstrings:** Required for public APIs, optional for internals
- **Type hints:** Encouraged for function signatures

### Naming Conventions

- **Functions/methods:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private:** `_leading_underscore`

### CHAOS-Specific Conventions

- **Emotional terms:** Keep as written (`dream`, `ritual`, `stability`)
- **Narrative names:** Prefer clarity over brevity
- **Comments:** Add context, not obvious statements

### Example

```python
from typing import Dict, List, Any

def parse_emotion_tag(tag: str) -> Dict[str, Any]:
    """
    Parse an emotion tag into name and intensity.
    
    Args:
        tag: Emotion tag string like "EMOTION:JOY:7"
        
    Returns:
        Dictionary with 'name' and 'intensity' keys
        
    Raises:
        ValueError: If tag format is invalid
    """
    parts = tag.split(':')
    if len(parts) != 3 or parts[0] != 'EMOTION':
        raise ValueError(f"Invalid emotion tag: {tag}")
        
    return {
        'name': parts[1],
        'intensity': int(parts[2])
    }
```

## Debugging & Troubleshooting

### Common Issues

**Problem:** Import errors after installation  
**Solution:** Ensure you installed in editable mode: `pip install -e .`

**Problem:** Tests fail with module not found  
**Solution:** Check `pythonpath` in `pyproject.toml` and verify virtual env is active

**Problem:** Linter fails on narrative content  
**Solution:** Some linter rules are disabled for CHAOS-specific patterns in `pyproject.toml`

### Debugging Techniques

**1. Verbose mode**
```python
from chaos_language import run_chaos

env = run_chaos(source, verbose=True)  # Prints debug info
```

**2. Interactive debugging**
```python
import pdb; pdb.set_trace()  # Insert breakpoint
```

**3. Token inspection**
```python
from chaos_language.chaos_lexer import Lexer

lexer = Lexer(source)
tokens = lexer.tokenize()
for token in tokens:
    print(f"{token.type}: {token.value}")
```

**4. AST visualization**
```python
from chaos_language.chaos_parser import Parser

parser = Parser(tokens)
ast = parser.parse()
print(ast)  # Pretty-print AST structure
```

See [DEBUGGING.md](docs/DEBUGGING.md) for more detailed debugging guides.

## Performance Considerations

### Design Trade-offs

CHAOS prioritizes **meaning preservation** over execution speed. Performance optimizations are welcome but must not:

- Erase symbolic context
- Skip consent checks
- Obscure emotional intent
- Remove narrative clarity

### Acceptable Optimizations

✅ Caching parsed ASTs  
✅ Efficient token scanning  
✅ Lazy evaluation of optional features  
✅ Memory pooling for large artifacts  

### Unacceptable Optimizations

❌ Skipping validation for "known safe" inputs  
❌ Removing emotion tracking for speed  
❌ Compressing narrative text  
❌ Parallel execution that breaks consent flows  

## Release Process

### Version Numbering

CHAOS follows **Semantic Versioning**:
- **MAJOR** — Breaking changes to syntax or API
- **MINOR** — New features, backward compatible
- **PATCH** — Bug fixes, no new features

### Release Checklist

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with changes
3. **Run full test suite:** `pytest -v`
4. **Run linter:** `make lint`
5. **Validate corpus:** `python tools/cli_shims/chaos_fuzz.py`
6. **Update documentation** if needed
7. **Create git tag:** `git tag -a v0.1.0 -m "Release 0.1.0"`
8. **Push tag:** `git push origin v0.1.0`
9. **Create GitHub release** with notes
10. **Build package:** `python -m build`
11. **Publish** (if applicable)

### Pre-release Testing

- Run on multiple Python versions (3.9, 3.10, 3.11, 3.12)
- Test in clean virtual environment
- Verify Docker build works
- Check CI passes on all platforms

---

## Getting Help

- **Technical questions:** Open an issue on GitHub
- **Design discussions:** Use GitHub Discussions
- **Bugs:** File detailed bug reports with reproduction steps
- **Documentation:** Check `docs/` directory

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for detailed contribution guidelines.

---

**Happy coding!** Remember: meaning first, execution second. 💜
