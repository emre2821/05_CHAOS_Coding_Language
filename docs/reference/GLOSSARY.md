# CHAOS Glossary

**Last Updated:** 2025-12-18

This glossary defines key terms, concepts, and terminology used throughout the CHAOS language and its ecosystem. Terms are organized alphabetically within categories for easy reference.

## Core Concepts

### Artifact
A CHAOS `.sn` document that combines symbolic, emotional, and ethical context with optional execution hooks. Artifacts are the primary unit of work in CHAOS—they are meant to be read by humans first, interpreted by agents second, and optionally executed by tooling.

**Example:** `memory_garden.sn` is an artifact.

### Bounded Execution
Execution that is constrained by declared ethical boundaries, consent flows, and refusal paths. In CHAOS, execution is never automatic or unconstrained—it must honor the governance layer of the artifact.

**Related:** Governance Layer, Boundaries

### CHAOS
**Contextual Harmonics and Operational Stories.** A symbolic-operational language that carries meaning, emotion, ethics, and executable logic together. Used within the Echolace/EdenOS ecosystem.

**Pronunciation:** "kay-oss"

### Chaosfield Layer
The third layer of a CHAOS artifact containing free-form narrative text enclosed in `{ }` braces. This layer holds meaning that cannot be reduced to structured data or emotions—it is prose, poetry, context, and story.

**Example:**
```chaos
{
The garden was alive with color and quiet courage.
Each plant held a story, each bloom a promise kept.
}
```

**Related:** Three-Layer Architecture, Narrative

### Consent Flow
The explicit declaration of how consent is obtained, maintained, and revoked within a CHAOS artifact or protocol. Consent flows ensure that automation defers to human agency.

**Example:**
```chaos
[PERMISSION:READ:PUBLIC]
[PERMISSION:WRITE:AUTHENTICATED]
[REFUSAL:HALT_ON_REQUEST]
```

**Related:** Refusal Path, Boundaries

### Dignity-First Design
A core CHAOS principle stating that the dignity of human subjects, users, and contributors must be preserved above all other concerns—including performance, convenience, or automation.

**Implications:**
- Personal data requires explicit consent
- Context is never erased for efficiency
- Automation defers to human judgment
- Refusal is always honored

### Echolace
The broader ecosystem within which CHAOS operates. Echolace is the context, platform, or environment where CHAOS artifacts are created, interpreted, and honored.

**Related:** EdenOS

### EdenOS
The operating system or substrate that uses CHAOS as a governance and operational language. CHAOS binds rituals, ethics, and executable logic within EdenOS.

**Related:** Echolace

### Emotive Layer
The second layer of a CHAOS artifact containing emotional tags with names and intensities. Emotions are first-class data in CHAOS, traveling alongside structured metadata and narrative.

**Format:** `[EMOTION:NAME:INTENSITY]` where intensity is 0-10

**Example:**
```chaos
[EMOTION:JOY:7]
[EMOTION:HOPE:5]
```

**Related:** Three-Layer Architecture, Emotion Stack

### Governance Layer
The portion of a CHAOS artifact that encodes consent flows, boundaries, permissions, and decision rights. The governance layer ensures tooling can align with declared ethics before any action is attempted.

**Components:**
- Boundaries (what's off-limits)
- Permissions (who can do what)
- Refusal paths (how to stop)
- Intent (why this exists)

**Related:** Bounded Execution, Consent Flow

### Ritual
A structured process with symbolic meaning that is meant to be performed with care and attention. In CHAOS, rituals are not just procedures—they carry emotional weight and ethical obligations.

**Example:** A check-in protocol might be described as a ritual.

**Related:** Ritual Object, Protocol

### Ritual Object
The form a CHAOS artifact takes when it is meant to be held and read as a living agreement—something to be honored, not just executed. Ritual objects are read, reflected upon, and respected.

**Example:** A governance artifact declaring community boundaries is a ritual object.

### Structured Core
The first layer of a CHAOS artifact containing key-value metadata tags. This layer provides machine-readable structure for agents and tooling.

**Format:** `[KEY]: value`

**Example:**
```chaos
[EVENT]: memory
[TIME]: 2025-04-30T14:30:00Z
[CONTEXT]: garden
```

**Related:** Three-Layer Architecture, Metadata

### Symbolic Memory
The motifs, roles, relationships, and fragments that a CHAOS artifact carries forward so agents can remember context and obligations across interactions. Symbolic memory ensures continuity of meaning.

**Example:** References to "the garden" might carry symbolic weight across multiple artifacts.

**Related:** Context Preservation, Continuity

### Three-Layer Architecture
The core structure of CHAOS artifacts:
1. **Structured Core** — Key-value metadata
2. **Emotive Layer** — Emotional context
3. **Chaosfield Layer** — Narrative text

Each layer serves a distinct purpose, and all three work together to preserve meaning.

**Related:** Structured Core, Emotive Layer, Chaosfield Layer

## File Formats & Syntax

### .sn Extension
The file extension for CHAOS artifacts. Stands for "**s**tory + **n**arrative" or "**s**ymbolic **n**otation."

**Example:** `memory_garden.sn`

### Tag
A structured element in CHAOS syntax enclosed in square brackets. Tags provide metadata, emotions, symbols, or boundaries.

**Types:**
- **Key-value:** `[EVENT]: memory`
- **Emotion:** `[EMOTION:JOY:7]`
- **Symbol:** `[SYMBOL:GROWTH:PRESENT]`
- **Boundary:** `[BOUNDARY:NO_ANALYTICS]`
- **Permission:** `[PERMISSION:READ:PUBLIC]`

### Narrative Block
Text enclosed in `{ }` braces that forms the Chaosfield layer. Narrative blocks contain human-readable prose that conveys meaning beyond structure.

**Example:**
```chaos
{
The garden was alive.
}
```

### Intensity
A numeric value (0-10) indicating the strength of an emotion in an emotion tag.

**Scale:**
- 0-3: Mild
- 4-6: Moderate
- 7-9: Strong
- 10: Overwhelming

**Example:** `[EMOTION:JOY:7]` — Joy at strong intensity (7/10)

## Runtime & Execution

### Agent
An emotion-aware runtime that interprets CHAOS artifacts, maintains symbolic memory, tracks emotional state, and executes protocols within declared boundaries.

**Implementation:** `ChaosAgent` class

**Related:** Agent Runtime, Emotion Stack

### Agent Runtime
The environment in which a CHAOS agent operates, managing state, memory, emotions, and protocol execution.

**Features:**
- Emotion tracking
- Symbolic memory preservation
- Consent/refusal handling
- Bounded protocol execution

### AST (Abstract Syntax Tree)
An intermediate representation of a CHAOS artifact produced by the parser. The AST represents the three-layer structure in a tree format that can be walked by the interpreter.

**Pipeline:** Source → Tokens → AST → Environment

### Environment
The runtime state produced by executing a CHAOS artifact. Contains the three layers as accessible data structures.

**Structure:**
```python
{
    'structured_core': {'KEY': 'value', ...},
    'emotive_layer': [{'name': 'JOY', 'intensity': 7}, ...],
    'chaosfield_layer': 'Narrative text...'
}
```

### Interpreter
The component that walks the AST and populates the runtime environment. The interpreter translates the parsed structure into executable state.

**Implementation:** `Interpreter` class

**Related:** Parser, Lexer, Runtime

### Lexer
The component that converts raw CHAOS source text into tokens. The lexer is the first stage of the processing pipeline.

**Implementation:** `Lexer` class

**Related:** Tokenization, Parser

### Parser
The component that takes tokens from the lexer and builds a three-layer AST. The parser enforces CHAOS syntax rules.

**Implementation:** `Parser` class

**Related:** AST, Lexer, Interpreter

### Token
A structured unit produced by the lexer, containing a type and value.

**Types:** `TAG_KEY`, `TAG_EMOTION`, `TAG_SYMBOL`, `LBRACE`, `RBRACE`, `TEXT`, etc.

**Example:** `Token(type='TAG_KEY', value='EVENT: memory')`

### Validator
A component that performs preflight checks on CHAOS artifacts to ensure they are well-formed before execution.

**Checks:**
- Required fields present
- Emotion intensities in valid range
- Narrative blocks properly closed
- Tag syntax correctness

**Implementation:** `validate_chaos()` function

## Emotional & Symbolic Concepts

### Emotion Stack
A data structure that tracks emotional states over time within an agent runtime. The emotion stack allows agents to maintain emotional continuity across interactions.

**Operations:**
- Push emotion (add new state)
- Pop emotion (remove state)
- Query current state
- Decay over time

**Implementation:** `EmotionStack` class

### Emotional Safety
The principle that emotional context must be preserved, respected, and handled with care by agents and tooling. Emotional safety means never dismissing, erasing, or trivializing emotional data.

**Practices:**
- Track emotions alongside actions
- Allow complex, contradictory emotions
- Provide space for vulnerability
- Defer to human judgment on emotional matters

### Intent
The declared "why" behind a CHAOS artifact or action. Intent provides traceability and context for future readers and auditors.

**Example:** `[INTENT]: maintain_connection`

**Related:** Traceability

### Motif
A recurring symbolic element that carries meaning across multiple artifacts or interactions. Motifs are part of symbolic memory.

**Example:** "The garden" as a motif representing growth and care.

### Role
A declared stance or authority held by the author or agent in a CHAOS artifact. Roles clarify who is speaking and with what capacity.

**Example:** `[ROLE]: moderator`

**Related:** Identity, Authority

### Symbol
An element carrying meaning beyond its literal value. Symbols are first-class in CHAOS and are preserved through execution.

**Format:** `[SYMBOL:NAME:STATE]`

**Example:** `[SYMBOL:GROWTH:PRESENT]`

## Ethics & Governance

### Boundary
A declared limit on what actions are allowed, what data can be accessed, or what behaviors are acceptable. Boundaries are enforced by the governance layer.

**Format:** `[BOUNDARY:RULE]`

**Examples:**
- `[BOUNDARY:NO_PERSONAL_DATA]`
- `[BOUNDARY:NO_ANALYTICS]`
- `[BOUNDARY:ASK_BEFORE_ACTION]`

**Related:** Governance Layer, Refusal Path

### Permission
A declaration of who can perform what actions under what conditions. Permissions are explicit and auditable.

**Format:** `[PERMISSION:ACTION:SCOPE]`

**Examples:**
- `[PERMISSION:READ:PUBLIC]`
- `[PERMISSION:WRITE:AUTHENTICATED]`
- `[PERMISSION:EXECUTE:OWNER]`

### Refusal Path
An explicit mechanism for stopping, declining, or opting out of an action or protocol. Refusal paths are required in consent-aware systems.

**Format:** `[REFUSAL:METHOD]`

**Examples:**
- `[REFUSAL:HALT_ON_REQUEST]`
- `[REFUSAL:SILENT_EXIT]`
- `[REFUSAL:ASK_FIRST]`

**Related:** Consent Flow, Boundaries

### Traceability
The ability to trace why an action was taken, who authorized it, and what boundaries applied. Traceability enables audit and accountability.

**Components:**
- Intent declarations
- Permission records
- Boundary declarations
- Action logs

**Related:** Intent, Governance Layer

## Tools & Commands

### chaos-agent
A CLI tool that starts an interactive agent REPL for conversational interaction with a CHAOS agent.

**Usage:** `chaos-agent --name AgentName`

### chaos-cli
A CLI tool for inspecting and executing CHAOS artifacts with various output formats.

**Usage:** `chaos-cli artifact.sn [--json] [--verbose]`

### chaos-exec
A CLI tool for running CHAOS artifacts with reporting and JSON output capabilities.

**Usage:** `chaos-exec artifact.sn [--report] [--emit output.json]`

### Corpus
The collection of example CHAOS artifacts in the `chaos_corpus/` directory. The corpus serves as reference, test data, and inspiration.

**Examples:**
- `memory_garden.sn`
- `stability_call.sn`
- `relation_box.sn`

## Development & Technical

### Eden Cooperative License (ECL)
The license under which CHAOS is released. The ECL emphasizes:
- Attribution and lineage
- Sharing with care (no oppressive uses)
- Memory safety (protect sensitive data)

**Full text:** See [LICENSE](LICENSE)

### Pipeline
The processing flow for CHAOS artifacts:
```
Source → Lexer → Tokens → Parser → AST → Interpreter → Environment
```

### Pytest
The testing framework used for CHAOS. Tests are in the `tests/` directory.

**Usage:** `pytest -v`

### Validation Error
An error raised when a CHAOS artifact fails validation checks.

**Type:** `ChaosValidationError`

**Causes:**
- Missing required fields
- Invalid emotion intensity
- Malformed tags
- Unclosed narrative blocks

## Philosophy & Design

### Context Preservation
The principle that context—symbolic, emotional, historical—must be maintained through execution and transformation. Context is never erased for convenience or performance.

### Execution-Optional
The design principle that CHAOS artifacts remain valuable even when not executed. They can be read as ritual objects, governance documents, or symbolic records.

### Human-Readable First
The requirement that CHAOS artifacts must make sense to human readers before being useful to machines. Humans are the primary audience.

### Meaning-First Design
The core philosophy that meaning, context, and intent take priority over execution speed, performance, or optimization. CHAOS protects meaning first.

### Narrative-First
The approach where narrative (story, prose, explanation) is treated as primary, not secondary, to structured data. In CHAOS, the Chaosfield layer is as important as the structured core.

---

## Related Documentation

- [README.md](../../README.md) — Project overview
- [LEARNING.md](../guides/LEARNING.md) — Learning guide and tutorials
- [DEV.md](../guides/DEV.md) — Developer guide and architecture
- [GOVERNANCE.md](../../GOVERNANCE.md) — Project governance
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — Contribution guidelines
- [API_REFERENCE.md](../API_REFERENCE.md) — API documentation

---

**Note:** This glossary is a living document. Terms may be added or refined as CHAOS evolves. If you encounter terminology that needs clarification or addition, please open an issue or pull request.

**For Echolace DI Workspace context:** If you need deeper context about how these terms relate to the broader Echolace ecosystem beyond this repository, see the [GLOSSARY_PROMPT.md](GLOSSARY_PROMPT.md) file for a prompt you can use with workspace-aware tools.
