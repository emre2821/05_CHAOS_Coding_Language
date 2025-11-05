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

| Path | Purpose |
| ---- | ------- |
| `chaos_lexer.py` | Tokenizes CHAOS syntax into typed tokens. |
| `chaos_parser.py` | Produces the three-layer abstract syntax tree. |
| `chaos_interpreter.py` | Walks the AST into the runtime environment. |
| `chaos_runtime.py` | High-level helper that runs lexer → parser → interpreter. |
| `chaos_validator.py` | Preflight validation to guarantee all three layers exist. |
| `chaos_exec.py` | Command-line runner with JSON and business report output. |
| `chaos_cli.py` | Interactive shell and script inspector. |
| `chaos_agent.py` | Emotion-aware agent orchestrating dreams and protocols. |
| `chaos_reports.py` | Business-facing environment reporting utilities. |
| `chaos_corpus/` | Example `.sn` scripts for inspiration and tests. |
| `docs/chaos_monorepo.md` | Reference dump of the full CHAOS core stack modules. |

## Embedding CHAOS in Your Systems

1. **Capture rituals.** Compose `.sn` scripts during customer calls, incident
   reviews, or strategic planning. Include structured fields (e.g., `ACCOUNT_ID`,
   `STAGE`) along with emotional annotations.
2. **Automate ingestion.** Use `run_chaos` from `chaos_runtime` or the CLI to
   convert scripts into JSON for data pipelines, or call
   `chaos_reports.generate_business_report` to produce stakeholder-friendly
   snapshots.
3. **Close the loop.** Feed transcripts into `ChaosAgent` to elicit protocol
   recommendations (`stabilize`, `transform`, `relate`) and dream summaries that
   surface hidden connections.

## Testing & Quality

```bash
pytest
python chaos_fuzz.py
```

The `pytest` suite covers lexer, parser, interpreter, emotion stack, agent, CLI
execution, and the reporting utilities. The fuzz harness ensures the sample
corpus stays valid as the language evolves.

## License

This project is released under the **Eden Cooperative License**—share with care,
attribute with love, and keep the memories safe.
