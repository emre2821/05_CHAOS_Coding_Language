# Changelog

All notable changes to CHAOS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **SPEC.md** - Canonical language specification with formal file format definition
- **JSON Schema** (schema/chaos.schema.json) for machine-checkable validation
- **chaos-validate** CLI tool for validating CHAOS files against specification
  - Support for single files, multiple files, and directory validation
  - Human-friendly error messages with line numbers
  - Security flags: `--fail-on-sensitive` and `--require-consent`
- **Examples directory** with reference implementations:
  - memory_vow.chaos - Memory/vow with ethics fields
  - memory_garden.chaos - Simple memory file
  - persona_language_flowers.chaos - Language palette
  - config_with_pii.chaos - Configuration with PII handling
  - protocol_stability_call.chaos - System daemon protocol
- **Templates directory** with ready-to-use templates:
  - minimal.chaos - Bare minimum template
  - standard.chaos - Standard template with common fields
  - ethical.chaos - Template with ethics/consent fields
- **New file format** with header section and content markers:
  - Required fields: file_type, tags
  - Optional ethics fields: consent, safety_tier, sensitive
  - Content enclosure with [CONTENT BEGIN]/[CONTENT END] markers
  - Full Unicode and emoji support
- **Comprehensive test suite** for new validator (23+ tests)
- **Makefile validate target** for quick validation
- **CI validation step** to ensure example files remain valid
- CONTRIBUTING.md with contributor guidelines
- CODE_OF_CONDUCT.md with community standards
- SECURITY.md with vulnerability reporting instructions
- .editorconfig for consistent editor settings
- Makefile with developer commands
- .devcontainer for VS Code development containers
- GitHub issue and PR templates
- CodeQL security scanning workflow
- Test coverage reporting
- Pre-commit hooks configuration
- requirements.txt and requirements-dev.txt
- Dockerfile for containerization
- Development dependencies in pyproject.toml

### Changed
- **README.md** updated with new file format documentation and quickstart
- **CI workflows** enhanced with validation step for example files
- Updated pylint configuration for narrative-first codebase
- Improved CI/CD workflows with coverage reporting

## [0.1.0] - 2024-01-01

### Added
- Initial release of CHAOS interpreter
- Lexer (`chaos_lexer.py`) for tokenizing CHAOS syntax
- Parser (`chaos_parser.py`) for three-layer AST generation
- Interpreter (`chaos_interpreter.py`) for runtime execution
- Runtime (`chaos_runtime.py`) high-level orchestration
- Validator (`chaos_validator.py`) for preflight script validation
- Agent (`chaos_agent.py`) emotion-aware agent system
- Reports (`chaos_reports.py`) business-facing reporting utilities
- CLI tools: `chaos-cli`, `chaos-exec`, `chaos-agent`
- Comprehensive test suite (19 tests)
- Example `.sn` scripts in `artifacts/corpus_sn/`
- GitHub Actions CI/CD workflows
- Basic documentation

### Features
- Three-layer script structure (structured, emotive, chaosfield)
- Emotion stack processing
- Dream synthesis
- Business protocol recommendations
- JSON export capabilities
- Interactive agent REPL

---

[Unreleased]: https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Paradigm-Eden/05_CHAOS_Coding_Language/releases/tag/v0.1.0
