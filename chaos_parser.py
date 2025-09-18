# chaos_parser.py

from enum import Enum, auto

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
        return f"Node({self.type}, {self.value}, children={len(self.children)})"

class ChaoParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return Node(
            NodeType.PROGRAM,
            children=[
                self.parse_structured_core(),
                self.parse_emotive_layer(),
                self.parse_chaosfield_layer()
            ]
        )

    def match(self, *types):
        if self.is_at_end():
            return False
        if self.peek().type in types:
            self.advance()
            return True
        return False

    def consume(self, expected_type, error_msg):
        if self.check(expected_type):
            return self.advance()
        raise SyntaxError(f"{error_msg} at {self.peek()}")

    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def parse_structured_core(self):
        pairs = {}
        while not self.is_at_end() and self.peek().type == TokenType.IDENTIFIER:
            key_token = self.advance()
            self.consume(TokenType.ASSIGN, "Expected '=' after key")
            val_token = self.advance()
            pairs[key_token.value] = val_token.value
        return Node(NodeType.STRUCTURED_CORE, value=pairs)

    def parse_emotive_layer(self):
        emotions = []
        while not self.is_at_end() and self.peek().type == TokenType.EMOTION:
            emotion_token = self.advance()
            emotions.append(emotion_token.value)
        return Node(NodeType.EMOTIVE_LAYER, value=emotions)

    def parse_chaosfield_layer(self):
        lines = []
        while not self.is_at_end() and self.peek().type == TokenType.STRING:
            string_token = self.advance()
            lines.append(string_token.value)
        return Node(NodeType.CHAOSFIELD_LAYER, value="\n".join(lines))
