# CHAOS Templates

Ready-to-use templates for creating new CHAOS files. Each template follows the canonical format specified in [SPEC.md](../docs/reference/SPEC.md).

## Available Templates

### minimal.chaos

The bare minimum required for a valid CHAOS file:
- Required fields: `file_type`, `tags`
- Content block with markers
- Perfect for quick notes or simple artifacts

**Use when:** You need a quick artifact without extra metadata

```bash
cp templates/minimal.chaos my_note.chaos
```

### standard.chaos

Standard template with commonly used optional fields:
- All minimal requirements
- Plus: `classification`, `symbolic_identity`, `author`, `created`, `version`
- Demonstrates field descriptions and examples

**Use when:** Creating a well-documented artifact with metadata

```bash
cp templates/standard.chaos my_artifact.chaos
```

### ethical.chaos

Template emphasizing ethics and safety fields:
- All minimal requirements
- Plus: `consent`, `safety_tier`, `sensitive`
- Includes guidelines for each ethics field
- Best for consent-aware and safety-conscious systems

**Use when:** Building systems that handle sensitive data or require explicit consent

```bash
cp templates/ethical.chaos my_sensitive_artifact.chaos
```

## Quick Start

1. **Choose a template** based on your needs
2. **Copy it** to your workspace
3. **Edit** the placeholder values:
   - Replace `[REQUIRED - ...]` with actual values
   - Replace `[optional]` with your values or remove the line
   - Fill in the content section
4. **Validate** your file:
   ```bash
   chaos-validate your_file.chaos
   ```

## Example Workflow

```bash
# Create a new memory artifact from ethical template
cp templates/ethical.chaos my_memory.chaos

# Edit it (use your preferred editor)
nano my_memory.chaos

# Validate
chaos-validate my_memory.chaos -v

# If valid, you're good to go!
```

## Template Guidelines

### Required Fields

Always include:
- `file_type`: The primary purpose (memory, ritual, vow, protocol, etc.)
- `tags`: Comma-separated keywords for searchability
- `[CONTENT BEGIN]` and `[CONTENT END]` markers
- Non-empty content between markers

### Optional but Recommended

Consider adding:
- `classification`: Hierarchical categorization
- `symbolic_identity`: Who is speaking/acting
- `created`: ISO 8601 timestamp
- `consent`: Consent posture (explicit/implicit/none)

### Ethics Fields

Use when appropriate:
- `consent`: Always specify when handling user data
- `safety_tier`: For risk-sensitive content
- `sensitive`: Flag PII or trauma content

See [SPEC.md](../docs/reference/SPEC.md) for complete field definitions.

## Validation

All templates are valid CHAOS files that can be used as-is or customized:

```bash
# Templates are valid and will pass validation
chaos-validate templates/*.chaos

# After customizing, validate your file
chaos-validate my_file.chaos

# Validate with security checks
chaos-validate my_file.chaos --require-consent
chaos-validate my_file.chaos --fail-on-sensitive
```

## Reference Examples

For real-world examples of valid CHAOS files, see:
- [examples/](../examples/) - Complete, valid reference files
- [SPEC.md](../docs/reference/SPEC.md) - Specification with examples

## Contributing Templates

Have an idea for a new template? Contributions welcome!

1. Create a template following existing patterns
2. Document it in this README
3. Ensure it follows [SPEC.md](../docs/reference/SPEC.md)
4. Submit a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
