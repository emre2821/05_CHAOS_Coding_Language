# CHAOS Examples

This directory contains reference implementations of CHAOS files using the canonical format specified in [SPEC.md](../SPEC.md).

## Files

### Memory & Vows

- **memory_vow.chaos** - A personal vow with full ethics metadata
  - Demonstrates: consent, safety_tier, sensitive fields
  - Type: memory/vow
  - Tags: commitment, healing, 💙
  
- **memory_garden.chaos** - A simple memory file
  - Demonstrates: Minimal required fields with emotion
  - Type: memory
  - Tags: garden, growth, 🌱

### Personas & Communication

- **persona_language_flowers.chaos** - Language palette for agent communication
  - Demonstrates: Symbolic identity and communication patterns
  - Type: persona
  - Tags: communication, empathy, 🌸

### Configuration & Data

- **config_with_pii.chaos** - User profile with personal data
  - Demonstrates: PII handling with high safety tier
  - Type: configuration
  - Tags: user, settings, profile
  - ⚠️ Contains PII markers for demonstration

### Protocols & Systems

- **protocol_stability_call.chaos** - Emotional support check-in protocol
  - Demonstrates: System daemon with implicit consent
  - Type: protocol
  - Tags: stability, check-in, emotional-support

## Validation

All example files are validated in CI to ensure they remain compliant with the specification.

To validate these files locally:

```bash
# Validate all examples
chaos-validate artifacts/examples/*.chaos -v

# Or use Make
make validate
```

## Usage as Templates

You can copy any of these files as a starting point for your own CHAOS artifacts:

```bash
# Copy an example
cp artifacts/examples/memory_vow.chaos my_artifact.chaos

# Edit as needed
nano my_artifact.chaos

# Validate
chaos-validate my_artifact.chaos
```

Or use the ready-made templates in [templates/](../templates/).

## Ethics & Safety

Examples demonstrate different ethics postures:

| File | consent | safety_tier | sensitive |
|------|---------|-------------|-----------|
| memory_vow.chaos | explicit | med | none |
| config_with_pii.chaos | explicit | high | pii |
| protocol_stability_call.chaos | implicit | med | none |
| memory_garden.chaos | - | - | - |
| persona_language_flowers.chaos | explicit | low | none |

Use these as reference for your own consent-aware systems.

## Contributing Examples

To add a new example:

1. Create a valid CHAOS file following [SPEC.md](../SPEC.md)
2. Run `chaos-validate your_file.chaos` to verify
3. Document the example in this README
4. Submit a PR with the new file

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full guidelines.
