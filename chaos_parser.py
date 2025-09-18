"""
Minimal parser: PROGRAM -> [STRUCTURED_CORE, EMOTIVE_LAYER, CHAOSFIELD_LAYER]
"""
from enum import Enum, auto
from typing import List, Dict, Any

from chaos_lexer import TokenType, Token


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

    def parse_structured_core(self) -> Node:
        pairs: Dict[str, Any] = {}
        # Expect many:  [IDENT]: value
        while not self.is_at_end():
            if not self.check(TokenType.LEFT_BRACKET):
                break
            self.advance()  # [
            if not self.check(TokenType.IDENTIFIER):
                # Not a key-value tag → maybe emotive layer
                self.current -= 1  # step back from '['
                break
            key = self.advance().value
            if self.check(TokenType.COLON):
                # Detected a layered tag like [EMOTION:JOY:7]; rewind for emotive parser
                self.current -= 2
                break
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
            intensity_token = None
            if self.match(TokenType.COLON):
                intensity_token = self.advance()
                if intensity_token.type not in (TokenType.IDENTIFIER, TokenType.NUMBER):
                    raise SyntaxError("intensity")
            self.consume(TokenType.RIGHT_BRACKET, "] after tag")
            if tag == "EMOTION":
                raw_value = intensity_token.value if intensity_token is not None else None
                try:
                    intensity_value = int(raw_value) if raw_value is not None else 5
                except Exception:
                    intensity_value = 5
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
