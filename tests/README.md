# Tests

This directory contains unit and integration tests for the CHAOS language.

## Test Files

- **test_lexer.py** - Tests for the CHAOS lexer/tokenizer
- **test_parser.py** - Tests for the CHAOS parser
- **test_interpreter.py** - Tests for the CHAOS interpreter
- **test_validator.py** - Tests for script validation
- **test_emotion.py** - Tests for the emotion engine
- **test_agent.py** - Tests for the ChaosAgent
- **test_reports.py** - Tests for business reporting utilities
- **test_cli_execution.py** - Integration tests for CLI execution

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_lexer.py

# Run a specific test
pytest tests/test_lexer.py::test_lex_basic_pairs
```
