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
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.column})"


class ChaosLexer:
    def __init__(self):
        self.keywords = {
            "TRUE": TokenType.BOOLEAN,
            "FALSE": TokenType.BOOLEAN,
            "NULL": TokenType.NULL,
        }

    def tokenize(self, source):
        self.source = source
        self.tokens = []
        self.i = 0
        self.line = 1
        self.col = 1
        s = self.source

        def emit(token_type, value):
            self.tokens.append(Token(token_type, value, self.line, self.col))

        while self.i < len(s):
            c = s[self.i]
            if c in " \t\r":
                self.i += 1
                self.col += 1
                continue
            if c == "\n":
                self.i += 1
                self.line += 1
                self.col = 1
                continue
            if c == "#":
                while self.i < len(s) and s[self.i] != "\n":
                    self.i += 1
                continue
            if c == "[":
                emit(TokenType.LEFT_BRACKET, c)
                self.i += 1
                self.col += 1
                continue
            if c == "]":
                emit(TokenType.RIGHT_BRACKET, c)
                self.i += 1
                self.col += 1
                continue
            if c == "{":
                emit(TokenType.LEFT_BRACE, c)
                self.i += 1
                self.col += 1
                continue
            if c == "}":
                emit(TokenType.RIGHT_BRACE, c)
                self.i += 1
                self.col += 1
                continue
            if c == ":":
                emit(TokenType.COLON, c)
                self.i += 1
                self.col += 1
                continue
            if c == ",":
                emit(TokenType.COMMA, c)
                self.i += 1
                self.col += 1
                continue
            if c == '"':
                self.i += 1
                start = self.i
                while self.i < len(s) and s[self.i] != '"':
                    if s[self.i] == "\n":
                        self.line += 1
                        self.col = 1
                    self.i += 1
                val = s[start:self.i]
                if self.i < len(s) and s[self.i] == '"':
                    self.i += 1
                emit(TokenType.STRING, val)
                continue
            if c.isdigit():
                start = self.i
                while self.i < len(s) and s[self.i].isdigit():
                    self.i += 1
                emit(TokenType.NUMBER, s[start:self.i])
                continue
            if c.isalpha() or c == "_":
                start = self.i
                while self.i < len(s) and (
                    s[self.i].isalnum() or s[self.i] in {"_", "-"}
                ):
                    self.i += 1
                word = s[start:self.i]
                token_type = self.keywords.get(word.upper(), TokenType.IDENTIFIER)
                if token_type == TokenType.BOOLEAN:
                    value = word.upper() == "TRUE"
                elif token_type == TokenType.NULL:
                    value = None
                else:
                    value = word
                emit(token_type, value)
                continue
            # Unknown char → skip
            self.i += 1
            self.col += 1

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens
