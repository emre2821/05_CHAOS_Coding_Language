# CHAOS: Symbolic–Operational Language for EdenOS

[![Tests](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/tests.yml/badge.svg)](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/tests.yml)
[![Pylint](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/pylint.yml/badge.svg)](https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/gh/Paradigm-Eden/05_CHAOS_Coding_Language/graph/badge.svg)](https://codecov.io/gh/Paradigm-Eden/05_CHAOS_Coding_Language)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: Eden Cooperative](https://img.shields.io/badge/license-Eden%20Cooperative-purple.svg)](LICENSE)

CHAOS (Contextual Harmonics and Operational Stories) is a symbolic–operational
language used inside the Echolace / EdenOS ecosystem. It carries symbolic
meaning, emotional intent, ethical constraints, execution boundaries, and
human-readable ritual context alongside executable or semi-executable logic.
CHAOS protects meaning first; execution is optional and always bounded by the
ethics declared in the artifact.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Tools](#tools)
- [Development](#development)

## Overview

### What CHAOS Is

- A language that lives between code, ritual, metadata, and governance.
- A way to write artifacts meant to be read by humans, interpreted by agents,
  constrained by ethics, and optionally executed or enforced by tooling.
- A vessel for symbolic memory, emotional stance, and explicit intent.

### What CHAOS Is Not

- Not a general-purpose programming language.
- Not a drop-in replacement for existing runtimes or frameworks.
- Not "just" a DSL or config file—the meaning layer is primary.
- Not a vehicle for opaque automation or optimization that erases context.

### Audience

CHAOS is for:
- System builders crafting EdenOS-aligned services.
- Agent architects defining protocol, state, and story together.
- Symbolic / ethical AI designers needing traceable, constrained intent.
- EdenOS contributors maintaining shared rituals, boundaries, and governance.

CHAOS is not for:
- People seeking a general-purpose language for arbitrary software.
- Teams prioritizing throughput over meaning, consent, or traceability.

### Core Principles

- **Dignity-first design.** Human subjects, memories, and narratives stay
  sovereign; automation must defer to consent.
- **Consent and refusal.** Rituals and execution paths encode how to ask, honor
  refusal, and halt cleanly.
- **Symbolic memory.** Symbols, roles, and motifs are preserved as
  first-class—never decorative.
- **Emotional safety.** Emotional tone and intent accompany actions and must be
  handled with care by agents and tooling.
- **Traceability and intent.** Boundaries, permissions, and reasons are declared
  explicitly for audit and intervention.
- **Rejection of hollow optimization.** Performance or automation must not erase
  meaning, context, or ethical posture.

### Specification & File Format

CHAOS has a formal specification that defines the canonical file format:

- **[SPEC.md](SPEC.md)** — Complete language specification (single source of truth)
- **[schema/chaos.schema.json](schema/chaos.schema.json)** — Machine-checkable JSON Schema
- **[examples/](examples/)** — Reference files demonstrating the format
- **[templates/](templates/)** — Ready-to-use templates for new files

### File Structure

CHAOS files consist of:
1. **Header section** with key-value metadata (required: `file_type`, `tags`)
2. **Content section** enclosed in `[CONTENT BEGIN]` ... `[CONTENT END]` markers

### Ethics & Safety Fields

CHAOS includes optional fields for consent-aware and safety-conscious systems:
- `consent`: `explicit` | `implicit` | `none`
- `safety_tier`: `low` | `med` | `high`
- `sensitive`: `pii` | `trauma` | `none`

See [SPEC.md](SPEC.md) for complete field definitions and validation rules.

### Key Terms

- **Artifact.** A CHAOS `.sn` document that pairs symbolic, emotional, and
  ethical context with optional execution hooks; it is the primary unit of work
  in this repository.
- **Ritual object.** The form an artifact takes when it is meant to be held and
  read as a living agreement—something to be honored, not just executed.
- **Symbolic memory.** The motifs, roles, and relationships an artifact carries
  forward so agents can remember context and obligations across interactions.
- **Governance layer.** The portion of an artifact that encodes consent flows,
  boundaries, and decision rights so tooling can align with the declared
  ethics before any action is attempted.

### File Philosophy

A CHAOS file is a living ritual object. It typically names:
- **Identity** — who is speaking or acting.
- **Role** — the stance or authority being held.
- **Intent** — why the ritual or action exists.
- **Boundaries** — what is off-limits and how to stop.
- **Permissions** — what is allowed, by whom, and under what consent.
- **Memory / symbolism** — motifs, relationships, and fragments to preserve and
  respect.
- **Optional execution hooks** — actions agents or tooling may perform, guarded
  by declared ethics and boundaries.

This is descriptive, not a formal grammar; meaning and ethics remain primary.

### How CHAOS Is Used

- **Human-readable first.** Artifacts are written for people to read before any
  tool executes them.
- **Interpreted by agents.** Agent runtimes align protocol, emotional stance,
  and symbolic memory from the file.
- **Constrained by ethics.** Boundaries, consent flows, and refusal paths must
  be honored by interpreters and tooling.
- **Optionally executed.** Tools can emit JSON, trigger bounded protocols, or
  generate reports—always downstream of the declared ritual and ethics.
- **Governance layer.** CHAOS can stand alone as an intent and governance layer
  even when no execution is performed.

### Relationship to EdenOS

- **EdenOS substrate.** CHAOS binds rituals, governance, and operational stories
  within EdenOS.
- **CHAOS CLI and artifacts.** Use `chaos-cli` and `chaos-exec` to inspect,
  interpret, or optionally execute `.sn` artifacts with reporting outputs.
- **Agent runtimes.** `ChaosAgent` and related runtimes maintain symbols,
  emotions, and relationships in sync with declared boundaries.
- **Validators / interpreters.** Validators ensure structure and ethics are
  intact; interpreters walk the file into bounded runtime behaviors.
- **Independent meaning layer.** CHAOS artifacts remain useful without
  execution; they can be consumed as governance or ritual documents.

### Status & Scope

- Interpreter, validator, and CLI target Python 3.9+.
- Corpus and tooling evolve with EdenOS; expect iterative refinement.
- Scope is limited to environments that honor CHAOS ethical posture; elsewhere
  treat artifacts as read-only ritual documents.

## Quick Start

### Installation

```bash
# Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install CHAOS from PyPI
pip install chaos-language

# Or install from source in editable mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Validate CHAOS files (new format with headers)
chaos-validate examples/memory_vow.chaos -v

# Validate multiple files or directories
chaos-validate examples/*.chaos
chaos-validate --dir examples/

# Check for ethical compliance
chaos-validate examples/config_with_pii.chaos --fail-on-sensitive

# Inspect legacy .sn artifacts (human-readable first)
chaos-cli chaos_corpus/memory_garden.sn --json

# Run with reporting outputs (execution remains bounded by declared ethics)
chaos-exec chaos_corpus/stability_call.sn --report --emit report.json

# Open an empathic agent loop
chaos-agent --name Concord
```

### First validation in 60 seconds

Create a tiny CHAOS file, run the validator, and confirm success:

```bash
# 1) Create a minimal CHAOS artifact
cat > hello.chaos <<'EOF'
file_type: memory
tags: quickstart, hello, 🌿
consent: explicit
safety_tier: low

[CONTENT BEGIN]
This is a tiny CHAOS hello to prove the toolchain is working.
[CONTENT END]
EOF

# 2) Validate it with verbose output
chaos-validate hello.chaos -v
```

Expected output:

```
✔ hello.chaos

✓ All 1 file(s) valid
```

How to read this:
- `✔ hello.chaos` — the file passed all schema checks (headers, tags, content markers).
- `✓ All 1 file(s) valid` — the run succeeded; exit code is `0`. A `✖` line would call out the exact issue if validation failed.

### CHAOS File Format

CHAOS files use a simple header + content structure:

```chaos
file_type: memory
tags: garden, growth, 🌱
consent: explicit
safety_tier: med

[CONTENT BEGIN]
Your narrative, data, or operational content here.
Unicode and emojis are fully supported! ✨
[CONTENT END]
```

See [SPEC.md](SPEC.md) for the complete specification and [examples/](examples/) for reference files.

## Examples

- Browse **[examples/](examples/)** for reference files using the canonical
  header + content structure.
- Explore **[templates/](templates/)** to start new artifacts quickly.
- Inspect legacy ritual objects in **[chaos_corpus/](chaos_corpus/)** to see
  how symbolic memory and ethics are expressed.

## Tools

### Using the Makefile

```bash
make dev      # Install development dependencies
make test     # Run test suite
make lint     # Run linter
make coverage # Run tests with coverage report
make help     # Show all available commands
```

### Embedding CHAOS in Your Systems

1. **Capture rituals.** Compose `.sn` artifacts that pair structured telemetry
   with narrative, symbols, and consent boundaries.
2. **Interpret with agents.** Use `run_chaos` or agent runtimes to align protocol
   with declared intent, emotions, and ethical constraints.
3. **Optionally execute.** Emit JSON, trigger bounded protocols, or generate
   reports—always downstream of the declared ritual and ethics.

## Project Layout

```
/
├── src/
│   ├── chaos_language/       # Main package code/modules
│       ├── __init__.py       # Package exports
│       ├── chaos_lexer.py    # Tokenizes CHAOS syntax
│       ├── chaos_parser.py   # Produces three-layer AST
│       ├── chaos_interpreter.py  # Walks AST into runtime environment
│       ├── chaos_runtime.py  # High-level lexer → parser → interpreter
│       ├── chaos_validator.py    # Preflight validation
│       ├── chaos_agent.py    # Emotion-aware agent
│       ├── chaos_reports.py  # Reporting utilities
│       └── ...               # Additional modules
│   └── chaos/                # Modernized CHAOS package
│       ├── chaos_lexer.py    # Token recognition (modernized)
│       ├── chaos_parser.py   # Three-layer structure weaving
│       ├── chaos_runtime.py  # Execution pipeline
│       └── ...               # Additional modules
├── tests/                    # Unit/integration tests
│   └── chaos_modern/         # Modernized CHAOS test suite
├── scripts/                  # CLI entry points and utilities
│   ├── chaos_cli.py          # Interactive shell and artifact inspector
│   ├── chaos_exec.py         # Artifact runner with JSON/report output
│   ├── chaos_agent_cli.py    # Agent REPL
│   └── chaos_fuzz.py         # Artifact corpus validation runner
├── docs/                     # Documentation
│   └── modernization/        # Modernization notes and docs
├── chaos_corpus/             # Example .sn artifacts for inspiration and tests
├── experiments/modernization/ # Modernization experimental syntax ideas
├── .github/workflows/        # CI/CD workflows
├── .gitignore
├── README.md
├── pyproject.toml            # Project configuration
└── conftest.py               # Pytest configuration
```

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

We welcome contributions. Please see our [Contributing Guide](CONTRIBUTING.md)
for details on how to get started, and read our [Code of Conduct](CODE_OF_CONDUCT.md).

For comprehensive project information, see:
- **[GOVERNANCE.md](GOVERNANCE.md)** — Project governance and decision-making
- **[DEV.md](DEV.md)** — Developer guide and architecture
- **[LEARNING.md](LEARNING.md)** — Tutorials and learning resources
- **[GLOSSARY.md](GLOSSARY.md)** — Complete terminology reference

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

## License / Ethics Note

This project is released under the **Eden Cooperative License**—share with care,
attribute with love, and keep the memories safe. CHAOS artifacts must be used in
contexts that respect consent, dignity, and symbolic integrity.

---

**Built with care by Paradigm Eden**
