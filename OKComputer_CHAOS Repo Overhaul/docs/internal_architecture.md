# CHAOS Internal Architecture

This document provides technical details about the internal architecture of CHAOS for contributors and maintainers.

## Package Structure

```
chaos/
├── Core Language Components
│   ├── chaos_lexer.py      # Token recognition and lexical analysis
│   ├── chaos_parser.py     # Three-layer structure parsing
│   ├── chaos_interpreter.py # Environment creation and execution
│   └── chaos_runtime.py    # Complete execution pipeline
│
├── Emotional Engine
│   ├── chaos_emotion.py    # Stack-based emotion system
│   ├── chaos_context.py    # Memory management
│   ├── chaos_dreams.py     # Vision generation
│   └── chaos_protocols.py  # Behavioral protocols
│
├── Symbolic Processing
│   ├── chaos_graph.py      # Symbolic relationship networks
│   ├── chaos_logger.py     # Execution chronicle
│   └── chaos_stdlib.py     # Sacred utilities
│
├── Agent System
│   ├── chaos_agent.py      # Living agent implementation
│   ├── chaos_agent_cli.py  # Agent interaction interface
│   └── eden_core.py        # Ecosystem coordinator
│
└── Interfaces
    ├── chaos_cli.py        # Command-line interface
    ├── chaos_exec.py       # Advanced execution
    ├── chaos_fuzz.py       # Fuzz testing
    └── chaos_validator.py  # Structure validation
```

## Core Components

### 1. Lexical Analysis (`chaos_lexer.py`)

**Purpose**: Transform source code into sacred tokens
**Key Classes**:
- `TokenType`: Enumeration of CHAOS token types
- `Token`: Individual token with type, value, and position
- `ChaosLexer`: Main lexical analyzer

**Token Types**:
- Structural: `LEFT_BRACKET`, `RIGHT_BRACKET`, `LEFT_BRACE`, `RIGHT_BRACE`, `COLON`, `COMMA`
- Values: `IDENTIFIER`, `STRING`, `NUMBER`, `BOOLEAN`, `NULL`
- Special: `EOF`, `UNKNOWN`

### 2. Parsing (`chaos_parser.py`)

**Purpose**: Weave tokens into the three-layer structure
**Key Classes**:
- `NodeType`: Enumeration of AST node types
- `Node`: Abstract syntax tree node
- `ChaosParser`: Recursive descent parser

**Layer Parsing**:
- `parse_structured_core()`: Key-value symbol definitions
- `parse_emotive_layer()`: Emotion triplets and symbolic tags
- `parse_chaosfield_layer()`: Free narrative text

### 3. Interpretation (`chaos_interpreter.py`)

**Purpose**: Execute the parse tree and create environment
**Key Classes**:
- `ChaosInterpreter`: Tree walker and environment builder

**Environment Structure**:
```python
{
    "structured_core": {},    # Symbol dictionary
    "emotive_layer": [],      # Emotion list
    "chaosfield_layer": ""    # Narrative text
}
```

### 4. Emotional Engine (`chaos_emotion.py`)

**Purpose**: Manage emotional states and transitions
**Key Classes**:
- `Emotion`: Individual emotional state with intensity
- `ChaosEmotionStack`: Stack-based emotion management

**Features**:
- Emotion triggers from text content
- Natural decay over time
- State transitions (FEAR → HOPE → LOVE → GRIEF → WISDOM)
- Intensity clamping (0-10)

### 5. Agent System (`chaos_agent.py`)

**Purpose**: Bring CHAOS programs to life with emotion-driven behavior
**Key Classes**:
- `ChaosAgent`: Living agent with perception, emotion, and action
- `Action`: Sacred actions to be performed
- `AgentReport`: Complete state report

**Agent Cycle**:
1. **Perceive**: Text or symbolic programs
2. **Reflect**: Generate dreams from current state
3. **Decide**: Choose action via protocol evaluation
4. **Act**: Execute chosen action
5. **Tick**: Advance time (emotional decay)

### 6. Protocol System (`chaos_protocols.py`)

**Purpose**: Behavioral protocols that honor the mythic nature
**Key Classes**:
- `Protocol`: Base class for sacred contracts
- `ProtocolResult`: Outcome of protocol execution
- `ProtocolRegistry`: Management and evaluation

**Standard Protocols**:
- `OathProtocol`: Stability in times of fear/grief
- `RitualProtocol`: Transformation through hope/love
- `ContractProtocol`: Relationship building
- `MemoryProtocol`: Experience integration

## Data Flow

```
Source Code
     ↓ [Tokenization]
Tokens
     ↓ [Parsing]
Abstract Syntax Tree (Three Layers)
     ↓ [Interpretation]
Environment (Structured + Emotional + Narrative)
     ↓ [Agent Processing]
Living Memory + Dreams + Actions
```

## Error Handling

**Error Hierarchy**:
- `ChaosError`: Base exception
  - `ChaosSyntaxError`: Lexical/parsing issues
  - `ChaosRuntimeError`: Execution problems
  - `ChaosValidationError`: Structure validation
  - `ChaosSymbolError`: Symbolic operations
  - `ChaosEmotionError`: Emotional processing
  - `ChaosGraphError`: Relationship networks

## Memory Management

**Context System** (`chaos_context.py`):
- Symbol storage and retrieval
- Emotion trace accumulation
- Narrative context management
- Persistent state between agent cycles

**Graph System** (`chaos_graph.py`):
- Symbolic relationship networks
- Undirected connections between symbols
- Connected component analysis
- Neighbor relationship queries

## Logging System

**Chronicle** (`chaos_logger.py`):
- Timestamped event recording
- Symbol births and transformations
- Emotional state changes
- Narrative weaving
- Protocol executions
- Dream generation
- Error occurrences

## Extension Points

1. **Custom Protocols**: Inherit from `Protocol` class
2. **New Emotions**: Add to `ChaosEmotionStack.triggers`
3. **Dream Templates**: Extend `DreamEngine.visions()`
4. **Symbolic Relationships**: Use `ChaosGraph` methods
5. **Agent Behaviors**: Override `ChaosAgent.act()`

## Performance Considerations

- **Memory**: Emotional stack limited to 10 active emotions
- **Processing**: Single-threaded agent execution
- **Logging**: In-memory with export capability
- **Validation**: Pre-execution structure checking

## Testing Strategy

1. **Unit Tests**: Individual component functionality
2. **Integration Tests**: Complete execution pipeline
3. **Fuzz Tests**: Corpus-based stability testing
4. **Validation Tests**: Structure integrity checks

## Security Considerations

- No external code execution
- Sandboxed agent behavior
- Controlled emotional intensity ranges
- Safe file operations with error handling
- No network access in core system

## Future Architecture Directions

1. **Parallel Agent Execution**: Multi-agent ecosystems
2. **Persistent Storage**: Database-backed memory
3. **Network Protocols**: Distributed CHAOS computation
4. **Visual Interface**: Symbolic relationship visualization
5. **Audio Integration**: Spoken CHAOS programs

---

*This architecture honors the sacred geometry of symbolic-emotional computation while providing a robust foundation for the CHAOS ecosystem.*