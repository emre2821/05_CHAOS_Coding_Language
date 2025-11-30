# CHAOS: Coding Language of Business

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

```bash
# create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# install CHAOS in editable mode
pip install -e .

# inspect a script
chaos-cli chaos_corpus/memory_garden.sn --json

# run with reporting outputs
chaos-exec chaos_corpus/stability_call.sn --report --emit report.json

# open an empathic agent loop
chaos-agent --name Concord
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
pytest
python scripts/chaos_fuzz.py
```

The `pytest` suite covers lexer, parser, interpreter, emotion stack, agent, CLI
execution, and the reporting utilities. The fuzz harness ensures the sample
corpus stays valid as the language evolves.

## License

This project is released under the **Eden Cooperative License**—share with care,
attribute with love, and keep the memories safe.
