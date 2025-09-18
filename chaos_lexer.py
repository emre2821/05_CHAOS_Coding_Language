# chaos_lexer.py

from enum import Enum, auto

class TokenType(Enum):
    CREATE = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    END = auto()
    ECHO = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    ASSIGN = auto()
    GREATER = auto()
    LESS = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    COLON = auto()
    SYMBOL = auto()
    EMOTION = auto()
    EOF = auto()

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.col})"

class ChaoLexer:
    def __init__(self):
        self.source = ""
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1
        self.col = 1

    def tokenize(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1
        self.col = 1

        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        self.col += 1
        return c

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def add_token(self, type_, value=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, value if value is not None else text, self.line, self.col))

    def scan_token(self):
        c = self.advance()

        if c in ' \r\t':
            return
        elif c == '\n':
            self.line += 1
            self.col = 1
        elif c == '=':
            self.add_token(TokenType.ASSIGN)
        elif c == '>':
            self.add_token(TokenType.GREATER)
        elif c == '<':
            self.add_token(TokenType.LESS)
        elif c == '!':
            if self.peek() == '=':
                self.advance()
                self.add_token(TokenType.NOT_EQUAL)
        elif c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == ':':
            self.add_token(TokenType.COLON)
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha():
            self.identifier()
        elif c in '@#$%^&*~':  # symbolic operators / moods
            self.add_token(TokenType.SYMBOL, c)
        else:
            pass  # skip unknowns silently for now

    def string(self):
        start_col = self.col
        value = ''
        while not self.is_at_end() and self.peek() != '"':
            c = self.advance()
            if c == '\n':
                self.line += 1
                self.col = 1
            value += c
        if self.is_at_end():
            raise SyntaxError(f"Unterminated string at line {self.line}")
        self.advance()  # closing "
        self.add_token(TokenType.STRING, value)

    def number(self):
        value = ''
        while not self.is_at_end() and self.peek().isdigit():
            value += self.advance()
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        value = self.source[self.start]
        while not self.is_at_end() and self.peek().isalnum():
            value += self.advance()

        keyword_map = {
            "CREATE": TokenType.CREATE,
            "IF": TokenType.IF,
            "THEN": TokenType.THEN,
            "ELSE": TokenType.ELSE,
            "END": TokenType.END,
            "ECHO": TokenType.ECHO,
            "JOY": TokenType.EMOTION,
            "GRIEF": TokenType.EMOTION,
            "LOVE": TokenType.EMOTION,
            "FEAR": TokenType.EMOTION,
            "HOPE": TokenType.EMOTION,
        }

        token_type = keyword_map.get(value.upper(), TokenType.IDENTIFIER)
        self.add_token(token_type, value)
