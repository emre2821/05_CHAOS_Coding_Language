# CHAOS: Coding Language of Business

[![Tests](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/tests.yml/badge.svg)](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/tests.yml)
[![Pylint](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/pylint.yml/badge.svg)](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/gh/Paradigm-Eden/05_CHAOS_Coding_Language/graph/badge.svg)](https://codecov.io/gh/Paradigm-Eden/05_CHAOS_Coding_Language)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: Eden Cooperative](https://img.shields.io/badge/license-Eden%20Cooperative-purple.svg)](LICENSE)

CHAOS (Contextual Harmonics and Operational Stories) is a narrative-first scripting
language for organizations that want to capture structured telemetry, emotional
signals, and qualitative story fragments in a single artifact. This repository
ships the full interpreter stack, tooling, and agent harness you need to weave
business memories into actionable intelligence.

## Why CHAOS for Business?

* **One ritual, three views.** Every `.sn` script carries a structured core for
  analytics, an emotive layer for sentiment tracking, and a chaosfield narrative
  for qualitative insights. The interpreter preserves each strand so you can feed
  dashboards, CRMs, or knowledge bases without translation loss.
* **Executable knowledge.** Run a script to generate JSON, trigger agentic
  protocols, or stream real-time dreams—perfect for retrospectives, customer
  journeys, and operational storytelling.
* **Agent-ready.** The bundled `ChaosAgent` keeps symbols, emotions, and
  relationships in sync, providing automatic dream synthesis and ritual
  protocols tailored for business stabilization, transformation, and relationship
  mapping.

## Quick Start

### Installation

```bash
# Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install CHAOS in editable mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Inspect a script
chaos-cli chaos_corpus/memory_garden.sn --json

# Run with reporting outputs
chaos-exec chaos_corpus/stability_call.sn --report --emit report.json

# Open an empathic agent loop
chaos-agent --name Concord
```

### Using the Makefile

```bash
make dev      # Install development dependencies
make test     # Run test suite
make lint     # Run linter
make coverage # Run tests with coverage report
make help     # Show all available commands
```

## Project Layout

```
/
├── src/
│   └── chaos_language/       # Main package code/modules
│       ├── __init__.py       # Package exports
│       ├── chaos_lexer.py    # Tokenizes CHAOS syntax
│       ├── chaos_parser.py   # Produces three-layer AST
│       ├── chaos_interpreter.py  # Walks AST into runtime environment
│       ├── chaos_runtime.py  # High-level lexer → parser → interpreter
│       ├── chaos_validator.py    # Preflight validation
│       ├── chaos_agent.py    # Emotion-aware agent
│       ├── chaos_reports.py  # Business-facing reporting utilities
│       └── ...               # Additional modules
├── tests/                    # Unit/integration tests
├── scripts/                  # CLI entry points and utilities
│   ├── chaos_cli.py          # Interactive shell and script inspector
│   ├── chaos_exec.py         # Command-line runner with JSON/report output
│   ├── chaos_agent_cli.py    # Agent REPL
│   └── chaos_fuzz.py         # Corpus validation runner
├── docs/                     # Documentation
├── chaos_corpus/             # Example .sn scripts for inspiration and tests
├── .github/workflows/        # CI/CD workflows
├── .gitignore
├── README.md
├── pyproject.toml            # Project configuration
└── conftest.py               # Pytest configuration
```

## Embedding CHAOS in Your Systems

1. **Capture rituals.** Compose `.sn` scripts during customer calls, incident
   reviews, or strategic planning. Include structured fields (e.g., `ACCOUNT_ID`,
   `STAGE`) along with emotional annotations.
2. **Automate ingestion.** Use `run_chaos` from `chaos_language` or the CLI to
   convert scripts into JSON for data pipelines, or call
   `generate_business_report` to produce stakeholder-friendly snapshots.
3. **Close the loop.** Feed transcripts into `ChaosAgent` to elicit protocol
   recommendations (`stabilize`, `transform`, `relate`) and dream summaries that
   surface hidden connections.

## Testing & Quality

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chaos_language --cov-report=term-missing

# Validate corpus integrity
python scripts/chaos_fuzz.py
```

The `pytest` suite covers lexer, parser, interpreter, emotion stack, agent, CLI
execution, and the reporting utilities. The fuzz harness ensures the sample
corpus stays valid as the language evolves.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md)
for details on how to get started.

Before contributing, please read our [Code of Conduct](CODE_OF_CONDUCT.md).

## Development

### Prerequisites

- Python 3.9 or higher
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language.git
cd 05_CHAOS_Coding_Language

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
make test     # Quick test run
make coverage # With coverage report
make lint     # Code quality check
make check    # All checks
```

## Docker

```bash
# Build the image
docker build -t chaos-language .

# Run the agent
docker run -it chaos-language

# Run a specific command
docker run chaos-language chaos-cli chaos_corpus/memory_garden.sn --json
```

## License

This project is released under the **Eden Cooperative License**—share with care,
attribute with love, and keep the memories safe.

---

**Built with 💜 by Paradigm Eden**
