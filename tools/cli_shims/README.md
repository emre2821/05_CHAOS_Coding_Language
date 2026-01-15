# Scripts

This directory contains CLI entry points and utility scripts for the CHAOS language.
The CLI files are thin shims that delegate to the maintained implementations in
`chaos_language.cli`, keeping the legacy shim paths (formerly `scripts/`) working for tooling and docs.

## CLI Tools

- **chaos_cli.py** - Interactive shell and script runner for CHAOS scripts
- **chaos_exec.py** - Command-line executor with agent mode and business reports
- **chaos_agent_cli.py** - Interactive REPL for the emotion-driven ChaosAgent

## Utility Scripts

- **chaos_fuzz.py** - Validation runner that tests all `.sn` files in `chaos_corpus/`

## Usage

```bash
# Run a CHAOS script
python tools/cli_shims/chaos_cli.py chaos_corpus/memory_garden.sn --json

# Run with business report output
python tools/cli_shims/chaos_exec.py chaos_corpus/stability_call.sn --report

# Open an empathic agent loop
python tools/cli_shims/chaos_agent_cli.py --name Concord

# Run fuzz tests on corpus
python tools/cli_shims/chaos_fuzz.py
```
