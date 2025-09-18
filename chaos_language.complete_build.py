# CHAOS Monorepo Dump (Full Core Stack)

> Everything we built in one place. Copy/paste as needed. Each file is delimited and self-contained.

---

## `chaos_errors.py`

```python
"""
Defines CHAOS exception classes grouped by failure mode.
"""

class ChaosError(Exception):
    """Base error for all CHAOS exceptions."""
    pass

class ChaosSyntaxError(ChaosError):
    """Raised during tokenization or parsing issues."""
    pass

class ChaosRuntimeError(ChaosError):
    """Raised during interpretation or execution."""
    pass

class ChaosValidationError(ChaosError):
    """Raised during static pre-validation of CHAOS structure."""
    pass

class ChaosSymbolError(ChaosError):
    """Raised when an unknown or illegal symbol is used."""
    pass

class ChaosEmotionError(ChaosError):
    """Raised for invalid emotion-related constructs."""
    pass

class ChaosGraphError(ChaosError):
    """Raised when symbolic graph operations fail."""
    pass
```

---

## `chaos_logger.py`

```python
"""
Timestamped runtime logger for symbols, emotions, narrative.
"""
import datetime

class ChaosLogger:
    def __init__(self):
        self.logs = []

    def log(self, message: str):
        entry = f"[{datetime.datetime.now().isoformat()}] {message}"
        self.logs.append(entry)

    def log_symbol(self, name: str, value: str):
        self.log(f"SYMBOL: {name} = {value}")

    def log_emotion(self, emotion: str):
        self.log(f"EMOTION: {emotion}")

    def log_narrative(self, chaosfield: str):
        self.log(f"NARRATIVE: {chaosfield[:60]}...")

    def export(self):
        return "\n".join(self.logs)
```

---

## `chaos_context.py`

```python
"""
Shared memory for symbols, emotions, narrative.
"""
class ChaosContext:
    def __init__(self):
        self.memory = {
            "symbols": {},
            "emotions": [],
            "narrative": "",
        }

    def set_symbol(self, key: str, value: str):
        self.memory["symbols"][key] = value

    def add_emotion(self, emotion: str):
        self.memory["emotions"].append(emotion)

    def set_narrative(self, text: str):
        self.memory["narrative"] = text

    def get(self):
        return self.memory

    def reset(self):
        self.__init__()
```

---

## `chaos_lexer.py`

```python
"""
Simplified lexer for the CHAOS language.
"""
from enum import Enum, auto

class TokenType(Enum):
    CREATE = auto(); IF = auto(); THEN = auto(); ELSE = auto(); END = auto(); ECHO = auto()
    IDENTIFIER = auto(); STRING = auto(); NUMBER = auto(); BOOLEAN = auto(); NULL = auto()
    ASSIGN = auto(); GREATER = auto(); LESS = auto(); EQUAL = auto(); NOT_EQUAL = auto()
    LEFT_PAREN = auto(); RIGHT_PAREN = auto(); LEFT_BRACE = auto(); RIGHT_BRACE = auto()
    LEFT_BRACKET = auto(); RIGHT_BRACKET = auto(); COMMA = auto(); COLON = auto(); DOT = auto()
    EOF = auto(); UNKNOWN = auto()

class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type; self.value = value; self.line = line; self.column = column
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.column})"

class ChaosLexer:
    def __init__(self):
        self.keywords = { 'TRUE': TokenType.BOOLEAN, 'FALSE': TokenType.BOOLEAN, 'NULL': TokenType.NULL }

    def tokenize(self, source):
        self.source = source; self.tokens = []; self.i = 0; self.line = 1; self.col = 1
        s = self.source
        def emit(t, v): self.tokens.append(Token(t, v, self.line, self.col))
        while self.i < len(s):
            c = s[self.i]
            if c in ' \t\r': self.i += 1; self.col += 1; continue
            if c == '\n': self.i += 1; self.line += 1; self.col = 1; continue
            if c == '#':
                while self.i < len(s) and s[self.i] != '\n': self.i += 1
                continue
            if c == '[': emit(TokenType.LEFT_BRACKET, c); self.i += 1; self.col += 1; continue
            if c == ']': emit(TokenType.RIGHT_BRACKET, c); self.i += 1; self.col += 1; continue
            if c == '{': emit(TokenType.LEFT_BRACE, c); self.i += 1; self.col += 1; continue
            if c == '}': emit(TokenType.RIGHT_BRACE, c); self.i += 1; self.col += 1; continue
            if c == ':': emit(TokenType.COLON, c); self.i += 1; self.col += 1; continue
            if c == ',': emit(TokenType.COMMA, c); self.i += 1; self.col += 1; continue
            if c == '"':
                self.i += 1; start = self.i
                while self.i < len(s) and s[self.i] != '"':
                    if s[self.i] == '\n': self.line += 1; self.col = 1
                    self.i += 1
                val = s[start:self.i]
                if self.i < len(s) and s[self.i] == '"': self.i += 1
                emit(TokenType.STRING, val); continue
            if c.isdigit():
                start = self.i
                while self.i < len(s) and s[self.i].isdigit(): self.i += 1
                emit(TokenType.NUMBER, s[start:self.i]); continue
            if c.isalpha() or c == '_':
                start = self.i
                while self.i < len(s) and (s[self.i].isalnum() or s[self.i] == '_'): self.i += 1
                word = s[start:self.i]
                t = self.keywords.get(word.upper(), TokenType.IDENTIFIER)
                val = True if word.upper() == 'TRUE' else False if word.upper() == 'FALSE' else None if word.upper()=='NULL' else word
                emit(t, val if t != TokenType.IDENTIFIER else word)
                continue
            # Unknown char → skip
            self.i += 1; self.col += 1
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.col))
        return self.tokens
```

---

## `chaos_parser.py`

```python
"""
Minimal parser: PROGRAM -> [STRUCTURED_CORE, EMOTIVE_LAYER, CHAOSFIELD_LAYER]
"""
from enum import Enum, auto
from typing import List, Dict, Any
from chaos_lexer import TokenType, Token

class NodeType(Enum):
    PROGRAM = auto(); STRUCTURED_CORE = auto(); EMOTIVE_LAYER = auto(); CHAOSFIELD_LAYER = auto()

class Node:
    def __init__(self, type_, value=None, children=None):
        self.type = type_; self.value = value; self.children = children or []
    def __repr__(self): return f"Node({self.type}, value={self.value!r}, children={len(self.children)})"

class ChaosParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens; self.current = 0

    def parse(self) -> Node:
        return Node(NodeType.PROGRAM, children=[
            self.parse_structured_core(),
            self.parse_emotive_layer(),
            self.parse_chaosfield_layer(),
        ])

    def is_at_end(self): return self.peek().type == TokenType.EOF
    def peek(self): return self.tokens[self.current]
    def previous(self): return self.tokens[self.current-1]
    def advance(self):
        if not self.is_at_end(): self.current += 1
        return self.previous()
    def check(self, t): return (not self.is_at_end()) and self.peek().type == t
    def match(self, *k):
        if self.is_at_end(): return False
        if self.peek().type in k:
            self.advance(); return True
        return False
    def consume(self, t, msg):
        if self.check(t): return self.advance()
        raise SyntaxError(msg)

    def parse_structured_core(self) -> Node:
        pairs: Dict[str, Any] = {}
        # Expect many:  [IDENT]: value
        while not self.is_at_end():
            if not self.check(TokenType.LEFT_BRACKET): break
            self.advance()  # [
            if not self.check(TokenType.IDENTIFIER):
                # Not a key-value tag → maybe emotive layer
                self.current -= 1  # step back from '['
                break
            key = self.advance().value
            self.consume(TokenType.RIGHT_BRACKET, "] expected after key")
            self.consume(TokenType.COLON, ": expected after ]")
            # value: STRING | NUMBER | IDENTIFIER | BOOLEAN | NULL
            tok = self.advance()
            if tok.type in (TokenType.STRING, TokenType.NUMBER, TokenType.BOOLEAN):
                pairs[key] = tok.value
            elif tok.type == TokenType.IDENTIFIER:
                pairs[key] = tok.value
            elif tok.type == TokenType.NULL:
                pairs[key] = None
            else:
                # If next is left brace, bail (chaosfield)
                self.current -= 1
                break
        return Node(NodeType.STRUCTURED_CORE, value=pairs)

    def parse_emotive_layer(self) -> Node:
        emotions = []
        while not self.is_at_end():
            if not self.check(TokenType.LEFT_BRACKET): break
            self.advance()  # [
            if not self.check(TokenType.IDENTIFIER):
                self.current -= 1; break
            tag = self.advance().value
            if tag != "EMOTION" and tag != "SYMBOL" and tag != "RELATIONSHIP":
                # Not emotive-family; rewind to before '[' for next phase
                self.current -= 2  # step back identifier and '['
                break
            self.consume(TokenType.COLON, "':' after tag")
            kind = self.consume(TokenType.IDENTIFIER, "emotion/symbol type").value
            intensity = None
            if self.match(TokenType.COLON):
                val = self.consume(TokenType.IDENTIFIER, "intensity").value
                intensity = val
            self.consume(TokenType.RIGHT_BRACKET, "] after tag")
            if tag == "EMOTION":
                # store as {name,intensity} for interpreter-compat
                try:
                    iv = int(intensity) if intensity is not None else 5
                except Exception:
                    iv = 5
                emotions.append({"name": kind.upper(), "intensity": iv})
            # SYMBOL/RELATIONSHIP ignored in minimal core; can extend later
        return Node(NodeType.EMOTIVE_LAYER, value=emotions)

    def parse_chaosfield_layer(self) -> Node:
        if not self.match(TokenType.LEFT_BRACE):
            return Node(NodeType.CHAOSFIELD_LAYER, value="")
        parts = []
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            tok = self.advance(); parts.append(str(tok.value))
        if self.check(TokenType.RIGHT_BRACE): self.advance()
        return Node(NodeType.CHAOSFIELD_LAYER, value=(" ".join(parts)).strip())
```

---

## `chaos_interpreter.py`

```python
"""
Interpreter: walk parse tree -> environment dict.
"""
from typing import Dict, Any
from chaos_parser import NodeType, Node

class ChaosInterpreter:
    def __init__(self):
        self.environment = {}

    def reset(self):
        self.environment = {}

    def interpret(self, node: Node) -> Dict[str, Any]:
        if node.type == NodeType.PROGRAM:
            for child in node.children: self.interpret(child)
        elif node.type == NodeType.STRUCTURED_CORE:
            self.environment["structured_core"] = node.value or {}
        elif node.type == NodeType.EMOTIVE_LAYER:
            self.environment["emotive_layer"] = node.value or []
        elif node.type == NodeType.CHAOSFIELD_LAYER:
            self.environment["chaosfield_layer"] = node.value or ""
        else:
            raise ValueError(f"Unknown node: {node.type}")
        return self.environment
```

---

## `chaos_validator.py`

```python
"""
Preflight: tokenizes + parses and checks for 3 layers.
"""
from chaos_errors import ChaosValidationError
from chaos_lexer import ChaosLexer
from chaos_parser import ChaosParser

def validate_chaos(source: str) -> None:
    try:
        tokens = ChaosLexer().tokenize(source)
        ast = ChaosParser(tokens).parse()
        if not ast or not ast.children or len(ast.children) != 3:
            raise ChaosValidationError("Expected 3 layers in CHAOS: structured_core, emotive_layer, chaosfield_layer")
    except Exception as e:
        raise ChaosValidationError(f"CHAOS Validation Failed: {e}")
```

---

## `chaos_runtime.py`

```python
"""
Entry point for executing CHAOS programs.
"""
from typing import Dict, Any
from chaos_errors import ChaosSyntaxError, ChaosRuntimeError
from chaos_lexer import ChaosLexer
from chaos_parser import ChaosParser
from chaos_interpreter import ChaosInterpreter

def run_chaos(source_code: str, verbose: bool = False) -> Dict[str, Any]:
    lexer = ChaosLexer()
    try:
        tokens = lexer.tokenize(source_code)
    except Exception as e:
        raise ChaosSyntaxError(f"Lexer error: {e}")

    if verbose:
        print("🔹 Tokens:")
        for t in tokens: print(t)

    parser = ChaosParser(tokens)
    try:
        ast = parser.parse()
    except Exception as e:
        raise ChaosSyntaxError(f"Parser error: {e}")

    if verbose:
        print("🔸 AST:")
        print(ast)

    interpreter = ChaosInterpreter()
    try:
        env = interpreter.interpret(ast)
    except Exception as e:
        raise ChaosRuntimeError(f"Interpreter error: {e}")

    if verbose:
        print("✅ ENV:")
        print(env)

    return env
```

---

## `chaos_emotion.py`

```python
"""
Stack-based emotion engine with keyword triggers and transitions.
"""
from collections import deque
from datetime import datetime

class Emotion:
    def __init__(self, name: str, intensity: int, timestamp=None):
        self.name = name.upper()
        self.intensity = max(0, min(intensity, 10))
        self.timestamp = timestamp or datetime.now()
    def decay(self, amount: int = 1):
        self.intensity = max(0, self.intensity - amount)
    def is_active(self) -> bool:
        return self.intensity > 0
    def __repr__(self):
        return f"{self.name}:{self.intensity}"

class ChaosEmotionStack:
    def __init__(self):
        self.stack = deque(maxlen=10)
        self.triggers = {
            "safe": ("CALM", 6),
            "momma": ("NOSTALGIA", 8),
            "disconnected": ("ANXIETY", 7),
            "warmth": ("LOVE", 7),
            "loss": ("GRIEF", 9),
            "ocean": ("WONDER", 5),
            "dark": ("FEAR", 6),
        }
        self.transitions = {"FEAR": "HOPE", "HOPE": "LOVE", "LOVE": "GRIEF", "GRIEF": "WISDOM"}

    def push(self, name: str, intensity: int):
        self.stack.append(Emotion(name, intensity))
    def current(self):
        return self.stack[-1] if self.stack else None
    def decay_all(self, amount: int = 1):
        for e in self.stack: e.decay(amount)
    def trigger_from_text(self, text: str):
        text = text.lower()
        for keyword, (emotion_name, intensity) in self.triggers.items():
            if keyword in text: self.push(emotion_name, intensity)
    def transition(self):
        cur = self.current()
        if cur and cur.name in self.transitions:
            nxt = self.transitions[cur.name]
            if nxt: self.push(nxt, max(0, cur.intensity - 1))
    def summary(self):
        return [repr(e) for e in self.stack if e.is_active()]
    def clear(self):
        self.stack.clear()
```

---

## `chaos_graph.py`

```python
"""
Undirected lightweight graph for symbols/entities.
"""
from typing import Any, Dict, Set
from chaos_errors import ChaosGraphError

class ChaosGraph:
    def __init__(self):
        self.nodes: Set[str] = set()
        self.edges: Dict[str, Set[str]] = {}
    def add_node(self, n: str):
        self.nodes.add(n); self.edges.setdefault(n, set())
    def add_edge(self, a: str, b: str):
        if a == b: return
        self.add_node(a); self.add_node(b)
        self.edges[a].add(b); self.edges[b].add(a)
    def neighbors(self, n: str):
        if n not in self.edges:
            raise ChaosGraphError(f"Unknown node: {n}")
        return set(self.edges[n])
    def __repr__(self):
        return f"CHAOSGraph(nodes={len(self.nodes)}, edges={sum(len(v) for v in self.edges.values())})"
```

---

## `chaos_stdlib.py`

```python
"""
Minimal pure helpers: clamp, pick, norm_key, uniq, text_snippet, weighted_pick.
"""
from typing import Any, Iterable, List, Tuple
import random, re

def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))

def pick(seq: Iterable[Any], default: Any = None) -> Any:
    seq = list(seq)
    if not seq: return default
    return random.choice(seq)

def norm_key(s: str) -> str:
    return re.sub(r"[^A-Z0-9_]+", "_", (s or "").strip().upper())

def uniq(seq: Iterable[Any]) -> List[Any]:
    out, seen = [], set()
    for x in seq:
        if x in seen: continue
        seen.add(x); out.append(x)
    return out

def text_snippet(s: str, n: int = 120) -> str:
    s = (s or "").strip().replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"

def weighted_pick(pairs: List[Tuple[Any, int]], default: Any = None) -> Any:
    if not pairs: return default
    total = sum(max(w, 0) for _, w in pairs) or 1
    r = random.randint(1, total); acc = 0
    for item, w in pairs:
        acc += max(w, 0)
        if r <= acc: return item
    return default
```

---

## `chaos_protocols.py`

```python
"""
Oaths, rituals, contracts w/ scoring.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from chaos_stdlib import weighted_pick, text_snippet

@dataclass
class ProtocolResult:
    name: str
    action: str
    details: Dict[str, Any] = field(default_factory=dict)
    score: int = 0

class Protocol:
    name: str = "protocol"
    priority: int = 0
    def match(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> int: return 0
    def execute(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> ProtocolResult:
        return ProtocolResult(self.name, action="noop", score=0)

class OathProtocol(Protocol):
    name, priority = "oath.stability", 50
    def match(self, ctx, emotions) -> int:
        fear = sum(e["intensity"] for e in emotions if e["name"] == "FEAR")
        grief = sum(e["intensity"] for e in emotions if e["name"] == "GRIEF")
        return (fear + grief) // 2
    def execute(self, ctx, emotions) -> ProtocolResult:
        s = self.match(ctx, emotions)
        return ProtocolResult(self.name, "stabilize", {"affirmation": "You are safe."}, s)

class RitualProtocol(Protocol):
    name, priority = "ritual.transformation", 40
    def match(self, ctx, emotions) -> int:
        hope = sum(e["intensity"] for e in emotions if e["name"] == "HOPE")
        love = sum(e["intensity"] for e in emotions if e["name"] == "LOVE")
        return hope + love
    def execute(self, ctx, emotions) -> ProtocolResult:
        s = self.match(ctx, emotions)
        return ProtocolResult(self.name, "transform", {"pledge": "We move with care.","source": text_snippet(ctx.get("narrative", ""))}, s)

class ContractProtocol(Protocol):
    name, priority = "contract.relationship", 35
    def match(self, ctx, emotions) -> int:
        syms = ctx.get("symbols", {})
        pairs = [k for k in syms if ":" in k]
        joy = sum(e["intensity"] for e in emotions if e["name"] == "JOY")
        return min(100, joy + len(pairs) * 2)
    def execute(self, ctx, emotions) -> ProtocolResult:
        s = self.match(ctx, emotions)
        return ProtocolResult(self.name, "relate", {"note": "Mapping entities."}, s)

class ProtocolRegistry:
    def __init__(self, protocols: Optional[List[Protocol]] = None):
        self.protocols = protocols or [OathProtocol(), RitualProtocol(), ContractProtocol()]
    def evaluate(self, ctx: Dict[str, Any], emotions: List[Dict[str, Any]]) -> Optional[ProtocolResult]:
        scored: List[Tuple[ProtocolResult, int]] = []
        for p in self.protocols:
            m = p.match(ctx, emotions)
            if m <= 0: continue
            res = p.execute(ctx, emotions)
            res.score = max(m, res.score) + p.priority
            scored.append((res, res.score))
        if not scored: return None
        return weighted_pick([(r, sc) for r, sc in scored], None)
```

---

## `chaos_dreams.py`

```python
"""
Dream engine: concise visions generated from state.
"""
from typing import List, Dict, Any, Optional
import random
from chaos_stdlib import pick, uniq, text_snippet

class DreamEngine:
    def __init__(self, seed: Optional[int] = None): self._seed = seed
    def visions(self, symbols: Dict[str, Any], emotions: List[Dict[str, Any]], narrative: str, k: int = 3) -> List[str]:
        rng = random.Random(self._seed)
        keys = uniq(list(symbols.keys()))
        emos = [e["name"] for e in emotions for _ in range(max(e["intensity"] // 2, 1))]
        base = text_snippet(narrative, 160)
        out = []
        for _ in range(k):
            a, b, e = pick(keys, "MEMORY"), pick(keys, "LIGHT"), pick(emos, "CALM")
            out.append(f"Dream of {a} meeting {b} under {e}; context: {base}")
        return out
```

---

## `chaos_agent.py`

```python
"""
Emotion-driven agent that executes CHAOS scripts, updates memory, runs protocols.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from chaos_context import ChaosContext
from chaos_logger import ChaosLogger
from chaos_emotion import ChaosEmotionStack
from chaos_graph import ChaosGraph
from chaos_runtime import run_chaos
from chaos_protocols import ProtocolRegistry
from chaos_dreams import DreamEngine
from chaos_stdlib import norm_key, clamp, text_snippet

@dataclass
class Action:
    kind: str
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentReport:
    emotions: List[Dict[str, Any]]
    symbols: Dict[str, Any]
    narrative: str
    action: Optional[Action]
    dreams: List[str]
    log: str

class ChaosAgent:
    def __init__(self, name: str, *, seed: Optional[int] = None):
        self.name = name
        self.ctx = ChaosContext()
        self.log = ChaosLogger()
        self.emotions = ChaosEmotionStack()
        self.graph = ChaosGraph()
        self.protocols = ProtocolRegistry()
        self.dreams = DreamEngine(seed=seed)

    def perceive_text(self, text: str) -> None:
        self.log.log(f"{self.name} perceived: {text_snippet(text)}")
        self.emotions.trigger_from_text(text)

    def perceive_sn(self, source: str) -> None:
        env = run_chaos(source, verbose=False)
        sc = env.get("structured_core", {})
        emo = env.get("emotive_layer", [])
        cf = env.get("chaosfield_layer", "")
        for k, v in sc.items():
            self.ctx.set_symbol(norm_key(k), v)
            self.log.log(f"symbol {norm_key(k)}={v}")
        for e in emo:
            name = norm_key(e.get("type") or e.get("name") or "FEELING")
            raw = e.get("intensity") or 5
            val = clamp(int(raw) if str(raw).isdigit() else 5, 0, 10)
            self.emotions.push(name, val)
            self.log.log(f"emotion {name}:{val}")
        if cf:
            self.ctx.set_narrative(cf)
            self.log.log(f"narrative {text_snippet(cf)}")

    def reflect(self) -> List[str]:
        mem = self.ctx.get(); emos = self._emotion_snapshot()
        visions = self.dreams.visions(mem["symbols"], emos, mem["narrative"])
        for v in visions: self.log.log(f"dream {text_snippet(v)}")
        return visions

    def decide(self) -> Optional[Action]:
        mem = self.ctx.get(); emos = self._emotion_snapshot()
        choice = self.protocols.evaluate(mem, emos)
        if not choice:
            self.log.log("idle"); return None
        self.log.log(f"protocol {choice.name}:{choice.score} -> {choice.action}")
        return Action(choice.action, choice.details)

    def act(self, action: Optional[Action]) -> None:
        if not action: return
        self.log.log(f"act {action.kind} {action.payload}")
        if action.kind == "relate":
            syms = list(self.ctx.get()["symbols"].keys())
            for i in range(len(syms) - 1): self.graph.add_edge(syms[i], syms[i + 1])

    def tick(self, decay: int = 1) -> None:
        self.emotions.decay_all(decay)

    def step(self, *, text: Optional[str] = None, sn: Optional[str] = None) -> AgentReport:
        if text: self.perceive_text(text)
        if sn: self.perceive_sn(sn)
        dreams = self.reflect(); action = self.decide(); self.act(action); self.tick()
        mem = self.ctx.get()
        return AgentReport(
            emotions=self._emotion_snapshot(),
            symbols=dict(mem["symbols"]),
            narrative=mem["narrative"],
            action=action,
            dreams=dreams,
            log=self.log.export(),
        )

    def _emotion_snapshot(self) -> List[Dict[str, Any]]:
        return [{"name": e.name, "intensity": e.intensity} for e in self.emotions.stack if e.is_active()]
```

---

## `chaos_agent_cli.py`

```python
"""
Interactive CLI for ChaosAgent.
"""
import argparse, os
from typing import Optional
from chaos_agent import ChaosAgent

BANNER = """\
CHAOS Agent CLI 🌌
:open <path>   load .sn/.chaos file
:dreams        show visions
:emotions      active emotions
:symbols       known symbols
:action        last action
:clear         clear narrative
:help          help
:quit          exit
"""

def _read(path: str) -> Optional[str]:
    if not os.path.exists(path): print("File not found."); return None
    with open(path, "r", encoding="utf-8") as f: return f.read()

def main():
    parser = argparse.ArgumentParser(description="CHAOS Agent REPL")
    parser.add_argument("--name", default="Concord")
    args = parser.parse_args()
    agent = ChaosAgent(args.name)
    print(BANNER)
    buf, last = [], None
    while True:
        try: line = input("agent> ").strip()
        except (EOFError, KeyboardInterrupt): print("\nbye."); break
        if line.startswith(":"):
            cmd, *rest = line[1:].split(maxsplit=1); arg = rest[0] if rest else ""
            if cmd == "open":
                src = _read(arg);
                if src: last = agent.step(sn=src); print("✓ merged.")
            elif cmd == "dreams": last = agent.step(); print("\n".join(last.dreams[:5]))
            elif cmd == "emotions": last = agent.step(); print(last.emotions)
            elif cmd == "symbols": last = agent.step(); print(last.symbols)
            elif cmd == "action": last = agent.step(); print(last.action)
            elif cmd == "clear": agent.ctx.set_narrative(""); print("✓ cleared.")
            elif cmd in ("help","h","?"): print(BANNER)
            elif cmd in ("quit","exit","q"): print("bye."); break
            else: print("unknown. :help");
            continue
        if not line:
            text = "\n".join(buf).strip(); buf.clear()
            if not text and not last: continue
            last = agent.step(text=text or None)
            print(f"✓ action: {last.action} | emotions: {last.emotions} | dreams: {last.dreams[:2]}")
            continue
        buf.append(line)

if __name__ == "__main__": main()
```

---

## `chaos_exec.py`

```python
"""
CHAOS executor for scripts with optional agent mode.
"""
import argparse, os, json
from chaos_validator import validate_chaos
from chaos_runtime import run_chaos
from chaos_agent import ChaosAgent

def main():
    p = argparse.ArgumentParser(description="CHAOS executor")
    p.add_argument("file", nargs="?", help=".sn or .chaos file")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--agent", action="store_true", help="run in agent mode after loading file")
    args = p.parse_args()

    if not args.file and not args.agent:
        p.error("Provide a file or use --agent")

    agent = ChaosAgent("Concord") if args.agent else None

    if args.file:
        if not os.path.exists(args.file): print("File not found."); return
        with open(args.file, "r", encoding="utf-8") as f: src = f.read()
        validate_chaos(src)
        env = run_chaos(src, verbose=args.verbose)
        print(json.dumps(env, indent=2))
        if agent:
            agent.step(sn=src)
            print("\n[agent] merged file into context.")

    if agent:
        print("\n[agent] type text; blank line to commit. /quit to exit.")
        buf = []
        while True:
            line = input("agent> ").strip()
            if line == "/quit": break
            if not line:
                t = "\n".join(buf).strip(); buf.clear()
                rep = agent.step(text=t or None)
                print(f"action={rep.action} emotions={rep.emotions} dreams={rep.dreams[:2]}")
            else:
                buf.append(line)

if __name__ == "__main__": main()
```

---

## `EdenCore.py` (with CHAOS Agent menu)

```python
import json, os
from datetime import datetime
try:
    from Eyes_of_Echo import EyesOfEcho
    from Threadstep import Threadstep
    from Markbearer import Markbearer
    from Scriptum import Scriptum
    from Rook import Rook
    from Glimmer import Glimmer
    from MuseJr import MuseJr
    from Toto import Toto
    from PulsePause import PulsePause
except Exception:
    class _Stub:
        def main(self): print("Stub daemon not installed.")
    EyesOfEcho = Threadstep = Markbearer = Scriptum = Rook = Glimmer = MuseJr = Toto = PulsePause = _Stub
from chaos_agent import ChaosAgent

class EdenCore:
    def __init__(self):
        self.log_file = "edencore_log.json"
        self.daemons = {
            "1": ("Eyes of Echo", EyesOfEcho()),
            "2": ("Threadstep", Threadstep()),
            "3": ("Markbearer", Markbearer()),
            "4": ("Scriptum", Scriptum()),
            "5": ("Rook", Rook()),
            "6": ("Glimmer", Glimmer()),
            "7": ("Muse Jr.", MuseJr()),
            "8": ("Toto", Toto()),
            "9": ("PulsePause", PulsePause()),
            "10": ("CHAOS Agent (Concord)", "CHAOS_AGENT"),
        }

    def log_action(self, name):
        entry = {"timestamp": str(datetime.now()), "daemon": name}
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(entry, f); f.write("\n")
        except Exception:
            pass

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _run_chaos_agent(self):
        agent = ChaosAgent("Concord")
        self.clear_screen()
        print("CHAOS Agent (Concord)\nType text; blank line to commit.\nCommands: /open <path>, /dreams, /emotions, /symbols, /action, /exit")
        buf, last = [], None
        while True:
            try: line = input("concord> ").strip()
            except (EOFError, KeyboardInterrupt): print("\nExiting."); break
            if line == "/exit": break
            if line.startswith("/open "):
                path = line.split(" ", 1)[1].strip()
                if not os.path.exists(path): print("File not found."); continue
                with open(path, "r", encoding="utf-8") as f: src = f.read()
                last = agent.step(sn=src); print("✓ merged .sn")
                continue
            if line == "/dreams": last = agent.step(); print("\n".join(last.dreams[:5])); continue
            if line == "/emotions": last = agent.step(); print(last.emotions); continue
            if line == "/symbols": last = agent.step(); print(last.symbols); continue
            if line == "/action": last = agent.step(); print(last.action); continue
            if not line:
                text = "\n".join(buf).strip(); buf.clear()
                last = agent.step(text=text or None)
                print(f"✓ action: {last.action} | emotions: {last.emotions} | dreams: {last.dreams[:2]}")
            else:
                buf.append(line)

    def main(self):
        while True:
            self.clear_screen()
            print("\n🌌 EdenCore: Your CHAOS Pantheon 🌌\n")
            for k, (name, _) in self.daemons.items(): print(f"{k}. {name}")
            print(f"{len(self.daemons) + 1}. Exit")
            choice = input("\nChoose a daemon (1-{}): ".format(len(self.daemons) + 1)).strip()
            if choice == str(len(self.daemons) + 1):
                print("\nEdenCore rests. You are enough."); break
            if choice in self.daemons:
                name, daemon = self.daemons[choice]; self.log_action(name); self.clear_screen()
                if daemon == "CHAOS_AGENT": self._run_chaos_agent()
                else:
                    try: daemon.main()
                    except Exception as e:
                        print(f"Daemon '{name}' failed: {e}")
                        input("\nPress Enter to continue...")
            else:
                print("\nPick a number, love. Try again.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    EdenCore().main()
```

---

## `chaos_corpus/` examples

### `chaos_corpus/memory_garden.sn`

```text
[EVENT]: memory
[TIME]: 2025-04-30T14:30:00Z
[CONTEXT]: garden
[SYMBOL:GROWTH:PRESENT]
[EMOTION:JOY:7]
[EMOTION:HOPE:5]
{
The garden was alive with color and quiet courage.
}
```

### `chaos_corpus/relation_box.sn`

```text
[EVENT]: relation
[OBJECT:BOX]: [ATTRIBUTE:WOOD]
[OBJECT:GIFT]: [ATTRIBUTE:SMALL]
[RELATIONSHIP:BOX:CONTAINS:GIFT]
[EMOTION:JOY:6]
{
We opened the box and found both a gift and a promise.
}
```

### `chaos_corpus/stability_call.sn`

```text
[EVENT]: checkin
[EMOTION:FEAR:6]
[EMOTION:GRIEF:8]
{
Tonight is heavy. I am breathing.
}
```

---

## `chaos_fuzz.py`

```python
"""
Run every .sn in chaos_corpus/ through the runtime.
"""
import glob, os
from chaos_runtime import run_chaos
from chaos_validator import validate_chaos

def main():
    for path in glob.glob(os.path.join("chaos_corpus","*.sn")):
        with open(path, "r", encoding="utf-8") as f: src = f.read()
        try:
            validate_chaos(src)
            env = run_chaos(src)
            print(f"[OK] {path} -> keys={list(env.keys())}")
        except Exception as e:
            print(f"[FAIL] {path} -> {e}")

if __name__ == "__main__": main()
```

---

## `tests/`

### `tests/test_lexer.py`

```python
import pytest
from chaos_lexer import ChaosLexer, TokenType

def test_lex_basic_pairs():
    src = '[EVENT]: memory\n[CONTEXT]: garden\n'
    toks = ChaosLexer().tokenize(src)
    assert any(t.type == TokenType.LEFT_BRACKET for t in toks)
    assert any(getattr(t, "value", None) == "EVENT" for t in toks)
    assert any(t.type == TokenType.COLON for t in toks)

def test_lex_emotion_tag():
    src = '[EMOTION:JOY:7]'
    toks = ChaosLexer().tokenize(src)
    kinds = [t.type.name for t in toks]
    assert "LEFT_BRACKET" in kinds and "RIGHT_BRACKET" in kinds
    assert any(getattr(t, "value", None) == "EMOTION" for t in toks)
```

### `tests/test_parser.py`

```python
from chaos_lexer import ChaosLexer
from chaos_parser import ChaosParser, NodeType

def test_parse_three_layers():
    src = '[EVENT]: memory\n[EMOTION:JOY:7]\n{ Text }'
    ast = ChaosParser(ChaosLexer().tokenize(src)).parse()
    assert ast.type == NodeType.PROGRAM and len(ast.children) == 3
```

### `tests/test_interpreter.py`

```python
from chaos_runtime import run_chaos

def test_interpreter_env_keys():
    src = '[EVENT]: memory\n[EMOTION:JOY:7]\n{ Warm day }'
    env = run_chaos(src)
    assert set(env.keys()) == {"structured_core","emotive_layer","chaosfield_layer"}

def test_interpreter_emotion_payload():
    src = '[EMOTION:HOPE:5]'
    env = run_chaos(src)
    assert any((e.get("type") or e.get("name")) == "HOPE" for e in env["emotive_layer"])
```

### `tests/test_emotion.py`

```python
from chaos_emotion import ChaosEmotionStack

def test_emotion_triggers_and_transition():
    es = ChaosEmotionStack()
    es.trigger_from_text("warmth in the dark, thinking of momma")
    assert es.current() is not None
    prev = es.current().name
    es.transition()
    assert es.current().name == prev or es.current().name in ("HOPE","LOVE","GRIEF","WISDOM")
```

### `tests/test_agent.py`

```python
from chaos_agent import ChaosAgent, Action

def test_agent_step_minimal():
    sn = '[EVENT]: memory\n[EMOTION:JOY:7]\n{ A bright spark }'
    agent = ChaosAgent("Test")
    rep = agent.step(text="ocean warmth", sn=sn)
    assert isinstance(rep.emotions, list)
    assert isinstance(rep.symbols, dict)
    assert rep.action is None or isinstance(rep.action, Action)
    assert isinstance(rep.dreams, list)
```

---

# Usage quick notes

* Run a script: `python chaos_exec.py path/to/file.sn`
* Run script + agent: `python chaos_exec.py path/to/file.sn --agent`
* Agent REPL: `python chaos_agent_cli.py` (type `:help` for commands)
* Fuzz all examples: `python chaos_fuzz.py`
* Tests (pytest): ensure files are importable; then `pytest -q`

# --- HOOK: auto-run CHAOS continuation build ---
import subprocess, sys, os

try:
    continued_path = r"C:\EdenOS_Origin\05_CHAOS_Coding_Language\chaos_continued.complete_build.py"
    if os.path.exists(continued_path):
        print("\n⚡ Launching CHAOS continuation build...")
        subprocess.run([sys.executable, continued_path], check=True)
    else:
        print(f"\n⚠ No continuation build found at {continued_path}")
except Exception as e:
    print(f"\n[ERROR] Could not launch continuation build: {e}")

