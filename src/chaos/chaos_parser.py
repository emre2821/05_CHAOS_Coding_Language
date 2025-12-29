"""
Minimal parser: PROGRAM -> [STRUCTURED_CORE, EMOTIVE_LAYER, CHAOSFIELD_LAYER]

The parser weaves the sacred tokens into the three-layer structure that
defines CHAOS. Each layer carries its own symbolic weight and emotional
resonance, creating the mythic architecture of the language.
"""

from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple, NamedTuple
from .chaos_lexer import TokenType, Token
from .chaos_errors import ChaosSyntaxError


class NodeType(Enum):
    """The sacred nodes that form the tree of CHAOS meaning."""
    
    PROGRAM = auto()           # The complete ritual
    STRUCTURED_CORE = auto()   # The bones and architecture
    EMOTIVE_LAYER = auto()     # The heart and emotional weight
    CHAOSFIELD_LAYER = auto()  # The narrative chaos and free text


class Node:
    """A node in the sacred tree of CHAOS meaning."""
    
    def __init__(self, node_type: NodeType, value: Optional[Any] = None, 
                 children: Optional[List['Node']] = None) -> None:
        """Create a node with its sacred properties."""
        self.type = node_type
        self.value = value
        self.children = children or []
    
    def __repr__(self) -> str:
        if self.children:
            return f"Node({self.type}, value={self.value!r}, children={len(self.children)})"
        return f"Node({self.type}, value={self.value!r})"


class TagTriplet(NamedTuple):
    tag: str
    kind: str
    value: Optional[Any]
    value_type: Optional[str]
    has_value: bool


class ChaosParser:
    """Weaves tokens into the three-layer structure of CHAOS."""
    _ROUTED_TAGS = {"EMOTION", "SYMBOL"}
    
    _ROUTED_TAGS = {"EMOTION", "SYMBOL"}
    
    def __init__(self, tokens: List[Token]) -> None:
        """Initialize the parser with sacred tokens."""
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Node:
        """
        Transform tokens into the sacred three-layer structure.
        
        This is where the ritual takes shape - where individual tokens
        become part of the greater symbolic whole.
        
        Returns:
            The root node of the CHAOS parse tree
        """
        self.current = 0
        structured_core = self._parse_structured_core()
        
        self.current = 0
        emotive_layer = self._parse_emotive_layer()
        
        self.current = 0
        chaosfield_layer = self._parse_chaosfield_layer()
        
        return Node(NodeType.PROGRAM, children=[
            structured_core,
            emotive_layer,
            chaosfield_layer,
        ])
    
    # ---- Token utilities ----
    
    def _is_at_end(self) -> bool:
        """Check if we've reached the end of the token stream."""
        return self._peek().type == TokenType.EOF
    
    def _peek(self) -> Token:
        """Look at the current token without consuming it."""
        return self.tokens[self.current]
    
    def _previous(self) -> Token:
        """Get the previously consumed token."""
        return self.tokens[self.current - 1]
    
    def _advance(self) -> Token:
        """Consume the current token and move to the next."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if the current token matches the given type."""
        return not self._is_at_end() and self._peek().type == token_type
    
    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        if self._is_at_end():
            return False
        if self._peek().type in types:
            self._advance()
            return True
        return False
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """Consume a token of the expected type or raise an error."""
        if self._check(token_type):
            return self._advance()
        raise ChaosSyntaxError(f"{message} at line {self._peek().line}")
    
    # ---- Layer parsing ----
    
    def _parse_structured_core(self) -> Node:
        """Parse the structured core layer - the bones of the ritual."""
        pairs: Dict[str, Any] = {}
        
        while not self._is_at_end():
            start_index = self.current

            probe = self._peek_tag_triplet(start_index)
            if probe:
                entry, end_index = probe
                if self._should_route_tag_triplet(entry):
                    self.current = end_index
                    continue

            if not self._check(TokenType.LEFT_BRACKET):
                self._advance()
                continue
            
            self._advance()  # Consume [
            
            if not self._check(TokenType.IDENTIFIER):
                # Not a simple key-value pair, move past the bracket
                self.current = start_index + 1
                continue
            
            key = self._advance().value

            if not self._check(TokenType.RIGHT_BRACKET):
                self.current = start_index + 1
                continue
            self._advance()  # Consume ]

            if not self._check(TokenType.COLON):
                self.current = start_index + 1
                continue
            self._advance()  # Consume :
            
            if self._is_at_end():
                break
            value_token = self._advance()  # Consume value token
            
            # Extract the value based on token type
            if value_token.type in (TokenType.STRING, TokenType.NUMBER, TokenType.BOOLEAN):
                pairs[key] = value_token.value
            elif value_token.type == TokenType.IDENTIFIER:
                pairs[key] = value_token.value
            elif value_token.type == TokenType.NULL:
                pairs[key] = None
            else:
                # Not a valid value, move past the current bracket and continue
                self.current = start_index + 1
                continue
        
        return Node(NodeType.STRUCTURED_CORE, value=pairs)

    def _peek_tag_triplet(self, start_index: int) -> Optional[Tuple[TagTriplet, int]]:
        """
        Non-destructively inspect whether a tag triplet starts at ``start_index``.
        
        Returns a tuple of (entry, end_index) if a triplet is found, where
        ``end_index`` is the token position immediately after the triplet.
        ``start_index`` must point to a LEFT_BRACKET token.
        """
        idx = start_index
        tokens = self.tokens

        if idx >= len(tokens) or tokens[idx].type != TokenType.LEFT_BRACKET:
            return None
        idx += 1

        if idx >= len(tokens) or tokens[idx].type != TokenType.IDENTIFIER:
            return None
        tag = tokens[idx].value
        idx += 1

        if idx >= len(tokens) or tokens[idx].type != TokenType.COLON:
            return None
        idx += 1

        if idx >= len(tokens) or tokens[idx].type != TokenType.IDENTIFIER:
            return None
        kind = tokens[idx].value
        idx += 1

        value_token = None
        has_second_colon = False
        if idx < len(tokens) and tokens[idx].type == TokenType.COLON:
            has_second_colon = True
            idx += 1
            if idx < len(tokens) and tokens[idx].type in (TokenType.IDENTIFIER, TokenType.NUMBER):
                value_token = tokens[idx]
                idx += 1

        if idx >= len(tokens) or tokens[idx].type != TokenType.RIGHT_BRACKET:
            return None
        idx += 1

        entry = TagTriplet(
            tag=tag,
            kind=kind,
            value=value_token.value if value_token else None,
            value_type=value_token.type.name if value_token else None,
            has_value=has_second_colon,
        )
        return entry, idx

    def _parse_tag_triplet(self, start_index: int) -> Optional[TagTriplet]:
        """
        Parse a tag triplet like [EMOTION:JOY:7] or [SYMBOL:GROWTH:PRESENT].
        
        Returns:
            A TagTriplet with the parsed components, or None if not a triplet pattern.
        """
        probe = self._peek_tag_triplet(start_index)
        if probe is None:
            return None
        
        entry, end_index = probe
        self.current = end_index
        return entry

    def _should_route_tag_triplet(self, entry: TagTriplet) -> bool:
        """Determine if a tag triplet should bypass structured core parsing."""
        return entry.tag in self._ROUTED_TAGS or entry.has_value
    
    def _parse_emotive_layer(self) -> Node:
        """Parse the emotive layer - the heart of the ritual."""
        emotions: List[Dict[str, Any]] = []
        extras: List[Dict[str, Any]] = []
        
        while not self._is_at_end():
            start_index = self.current

            if not self._check(TokenType.LEFT_BRACKET):
                self._advance()
                continue
            
            entry = self._parse_tag_triplet(self.current)
            if entry is None:
                # Not a tag triplet; ensure forward progress without over-skipping
                if self.current <= start_index:
                    self._advance()
                continue
            
            tag = entry.tag
            kind = entry.kind
            value = entry.value
            value_type = entry.value_type
            
            if tag == "EMOTION":
                # Parse emotion intensity
                try:
                    intensity = int(value) if value_type == "NUMBER" else int(str(value)) if value else 5
                except Exception:
                    intensity = 5
                intensity = max(0, min(intensity, 10))  # Clamp to 0-10
                emotions.append({"name": kind.upper(), "intensity": intensity})
            else:
                # Preserve other tags for agent processing
                extras.append({"tag": tag, "kind": kind, "value": value})
        
        return Node(NodeType.EMOTIVE_LAYER, value=emotions)
    
    def _parse_chaosfield_layer(self) -> Node:
        """Parse the chaosfield layer - the narrative free text."""
        while not self._is_at_end() and not self._match(TokenType.LEFT_BRACE):
            self._advance()
        
        if self._is_at_end():
            return Node(NodeType.CHAOSFIELD_LAYER, value="")
        
        parts = []
        while not self._is_at_end() and not self._check(TokenType.RIGHT_BRACE):
            token = self._advance()
            
            # Keep strings as-is, convert others to text
            if token.type == TokenType.STRING:
                parts.append(token.value)
            elif token.value is not None:
                parts.append(str(token.value))
        
        if self._check(TokenType.RIGHT_BRACE):
            self._advance()
        
        text = " ".join(parts).strip()
        return Node(NodeType.CHAOSFIELD_LAYER, value=text)
