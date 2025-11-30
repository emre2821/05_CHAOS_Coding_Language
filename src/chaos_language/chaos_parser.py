"""
Minimal parser: PROGRAM -> [STRUCTURED_CORE, EMOTIVE_LAYER, CHAOSFIELD_LAYER]
"""
from enum import Enum, auto
from typing import Any, Dict, List

from .chaos_lexer import Token, TokenType
from .chaos_stdlib import soft_intensity


class NodeType(Enum):
    PROGRAM = auto()
    STRUCTURED_CORE = auto()
    EMOTIVE_LAYER = auto()
    CHAOSFIELD_LAYER = auto()


class Node:
    def __init__(self, type_, value=None, children=None):
        self.type = type_
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"Node({self.type}, value={self.value!r}, children={len(self.children)})"


class ChaosParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Node:
        return Node(
            NodeType.PROGRAM,
            children=[
                self.parse_structured_core(),
                self.parse_emotive_layer(),
                self.parse_chaosfield_layer(),
            ],
        )

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type: TokenType) -> bool:
        return (not self.is_at_end()) and self.peek().type == token_type

    def match(self, *token_types: TokenType) -> bool:
        if self.is_at_end():
            return False
        if self.peek().type in token_types:
            self.advance()
            return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise SyntaxError(message)

    def _collect_bracket_contents(self, *, include_brackets: bool = False) -> str:
        depth = 1
        parts: List[str] = ["["] if include_brackets else []
        while not self.is_at_end():
            tok = self.advance()
            if tok.type == TokenType.LEFT_BRACKET:
                depth += 1
                parts.append(str(tok.value))
                continue
            if tok.type == TokenType.RIGHT_BRACKET:
                depth -= 1
                if depth == 0:
                    if include_brackets:
                        parts.append(str(tok.value))
                    break
                parts.append(str(tok.value))
                continue
            parts.append(str(tok.value))
        if depth != 0:
            raise SyntaxError("Unterminated bracket expression")
        return "".join(parts).strip()

    def parse_structured_core(self) -> Node:
        pairs: Dict[str, Any] = {}
        # Expect many:  [IDENT[:...]]: value
        while not self.is_at_end():
            if not self.check(TokenType.LEFT_BRACKET):
                break
            bracket_start = self.current
            self.advance()  # consume '['
            if not self.check(TokenType.IDENTIFIER):
                # Not a key-value tag → maybe emotive layer
                self.current = bracket_start
                break
            key = self._collect_bracket_contents(include_brackets=False)
            if not self.check(TokenType.COLON):
                # Not a structured core pair; rewind for emotive parser
                self.current = bracket_start
                break
            self.advance()  # consume ':'
            tok = self.advance()
            if tok.type in (TokenType.STRING, TokenType.NUMBER, TokenType.BOOLEAN):
                pairs[key] = tok.value
            elif tok.type == TokenType.IDENTIFIER:
                pairs[key] = tok.value
            elif tok.type == TokenType.NULL:
                pairs[key] = None
            elif tok.type == TokenType.LEFT_BRACKET:
                # Capture nested bracketed value like [ATTRIBUTE:WOOD]
                value = self._collect_bracket_contents(include_brackets=False)
                pairs[key] = value
            else:
                # If next is left brace, bail (chaosfield)
                self.current -= 1
                break
        return Node(NodeType.STRUCTURED_CORE, value=pairs)

    def parse_emotive_layer(self) -> Node:
        emotions = []
        while not self.is_at_end():
            if not self.check(TokenType.LEFT_BRACKET):
                break
            self.advance()  # [
            if not self.check(TokenType.IDENTIFIER):
                self.current -= 1
                break
            tag = self.advance().value
            if tag != "EMOTION" and tag != "SYMBOL" and tag != "RELATIONSHIP":
                # Not emotive-family; rewind to before '[' for next phase
                self.current -= 2  # step back identifier and '['
                break
            self.consume(TokenType.COLON, "':' after tag")
            kind = self.consume(TokenType.IDENTIFIER, "emotion/symbol type").value
            extras = []
            while self.match(TokenType.COLON):
                if self.is_at_end():
                    raise SyntaxError(": without value")
                extras.append(self.advance())
            trailing = []
            if tag == "EMOTION":
                while not self.check(TokenType.RIGHT_BRACKET) and not self.is_at_end():
                    trailing.append(self.advance())
            self.consume(TokenType.RIGHT_BRACKET, "] after tag")
            if tag == "EMOTION":
                tokens = extras + trailing
                raw_value = "".join(str(token.value) for token in tokens).strip() if tokens else None
                intensity_value = soft_intensity(raw_value, clamp_result=False)
                emotions.append({"name": kind.upper(), "intensity": intensity_value})
            # SYMBOL/RELATIONSHIP ignored in minimal core; can extend later
        return Node(NodeType.EMOTIVE_LAYER, value=emotions)

    def parse_chaosfield_layer(self) -> Node:
        if not self.match(TokenType.LEFT_BRACE):
            return Node(NodeType.CHAOSFIELD_LAYER, value="")
        parts = []
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            tok = self.advance()
            parts.append(str(tok.value))
        if self.check(TokenType.RIGHT_BRACE):
            self.advance()
            return Node(NodeType.CHAOSFIELD_LAYER, value=(" ".join(parts)).strip())
        raise SyntaxError("Unterminated chaosfield narrative; missing '}'")
