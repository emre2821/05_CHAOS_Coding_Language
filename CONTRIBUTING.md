# Contributing to CHAOS

**Thank you for being here.** 🌱

Whether you're fixing a typo, suggesting a feature, or diving deep into the
interpreter, your contribution matters. CHAOS is a collaborative project, and
every thoughtful change helps the language grow.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Scope Guidelines](#scope-guidelines)
- [Questions?](#questions)

## Ways to Contribute

- **Report bugs** — Found something broken? Let us know.
- **Suggest features** — Have an idea? We'd love to hear it.
- **Improve documentation** — Clarity helps everyone.
- **Write code** — Bug fixes, new features, performance improvements.
- **Review pull requests** — Fresh eyes catch hidden issues.
- **Share knowledge** — Write about CHAOS, create tutorials, spread the word.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/05_CHAOS_Coding_Language.git
   cd 05_CHAOS_Coding_Language
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language.git
   ```

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Or use the Makefile
make dev
```

### Using the Makefile

The project includes a `Makefile` for common tasks:

```bash
make dev      # Install development dependencies
make test     # Run tests
make lint     # Run linter
make format   # Format code (if available)
make clean    # Clean build artifacts
make help     # Show all available commands
```

## Making Changes

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** — Keep commits focused and atomic.

3. **Write tests** — New features need tests. Bug fixes should include regression tests.

4. **Run the test suite** — Ensure all tests pass:
   ```bash
   make test
   # or
   python -m pytest -v
   ```

5. **Run the linter** — Check code quality:
   ```bash
   make lint
   # or
   pylint src/ tests/ scripts/
   ```

## Code Style

CHAOS follows these principles:

- **PEP 8** — Standard Python style guide
- **Clear docstrings** — Document the "why," not just the "what"
- **Type hints** — Preferred for function signatures
- **Meaningful names** — Code should read like prose

### Special Considerations

CHAOS is a narrative-first language. Some patterns that look "wrong" by standard
metrics are intentional:

- **Emotional terminology** — `dream`, `ritual`, `stability` are domain terms
- **Expressive variable names** — We prefer clarity over brevity
- **Narrative comments** — Context matters more than conventional terseness

## Testing

All code changes should include appropriate tests:

```bash
# Run all tests
python -m pytest -v

# Run with coverage
python -m pytest --cov=chaos_language --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_lexer.py -v

# Validate corpus integrity
python scripts/chaos_fuzz.py
```

### Test Guidelines

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what's being tested
- Include both positive and negative test cases

## Pull Request Process

1. **Update your branch** with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub:
   - Fill out the PR template
   - Provide context for your changes
   - Reference any related issues

4. **Respond to feedback** — We review PRs with care. Discussion is welcome.

5. **Celebrate** 🎉 — Once merged, your contribution becomes part of CHAOS!

## Scope Guidelines

### In Scope

- Code in `src/chaos_language/`
- Tests in `tests/`
- CLI scripts in `scripts/`
- Configuration files
- Non-narrative documentation
- CI/CD workflows

### Out of Scope

Please **do not modify** without explicit discussion:

- `.sn` files in `chaos_corpus/` — These are narrative artifacts
- Symbolic or emotional content embedded in the language
- The core aesthetic or voice of CHAOS documentation

If you're unsure whether something is in scope, open an issue first!

## Questions?

- **Open an issue** for bugs or feature discussions
- **Start a discussion** for broader questions
- **Read the docs** in `docs/` for technical details

---

**Welcome to the CHAOS community.** We're grateful you're here. 💜
