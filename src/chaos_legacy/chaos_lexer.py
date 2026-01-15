"""
Simplified lexer for the CHAOS language.

The lexical analysis phase of CHAOS recognizes the sacred patterns:
- Symbolic tags that carry emotional weight
- Structured tokens that form the ritual syntax
- The three-layer architecture that defines CHAOS programs
"""

from enum import Enum, auto
from typing import List, Optional, Union


class TokenType(Enum):
    """Sacred tokens that form the vocabulary of CHAOS."""
    
    # Structural tokens - the bones of the ritual
    LEFT_BRACKET = auto()    # [ - Opening of symbolic space
    RIGHT_BRACKET = auto()   # ] - Closing of symbolic space
    LEFT_BRACE = auto()      # { - Opening of narrative chaos
    RIGHT_BRACE = auto()     # } - Closing of narrative chaos
    COLON = auto()           # : - The binding between name and meaning
    COMMA = auto()           # , - Separation within symbolic lists
    
    # Value tokens - the flesh of meaning
    IDENTIFIER = auto()      # Symbolic names and emotional states
    STRING = auto()          # Quoted text - the voice of chaos
    NUMBER = auto()          # Numeric intensities and measurements
    BOOLEAN = auto()         # TRUE/FALSE - the binary of being
    NULL = auto()           # NULL - the void where meaning sleeps
    
    # End of the ritual
    EOF = auto()
    UNKNOWN = auto()         # When meaning cannot be parsed


class Token:
    """A single unit of CHAOS meaning, carrying both type and symbolic weight."""
    
    def __init__(self, token_type: TokenType, value: Optional[Union[str, int, float, bool]], 
                 line: int, column: int) -> None:
        """Create a token with its sacred properties."""
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.column})"


class ChaosLexer:
    """Transforms CHAOS source code into a sequence of sacred tokens."""
    
    def __init__(self) -> None:
        """Initialize the lexer with the vocabulary of CHAOS."""
        self.keywords = {
            'TRUE': TokenType.BOOLEAN,
            'FALSE': TokenType.BOOLEAN,
            'NULL': TokenType.NULL
        }
    
    def tokenize(self, source: str) -> List[Token]:
        """
        Transform CHAOS source into tokens.
        
        This is the first step in the ritual - recognizing the patterns
        that will later be woven into the three-layer structure.
        
        Args:
            source: The CHAOS program text to tokenize
            
        Returns:
            List of tokens representing the sacred patterns in the source
        """
        self.source = source
        self.tokens: List[Token] = []
        self.i = 0
        self.line = 1
        self.col = 1
        
        while self.i < len(self.source):
            self._scan_next_character()
        
        # Mark the end of the ritual
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.col))
        return self.tokens
    
    def _scan_next_character(self) -> None:
        """Process the next character in the source stream."""
        c = self.source[self.i]
        
        # Whitespace - the silence between words
        if c in ' \t\r':
            self._advance_simple()
            return
        
        # Newline - the breath of the ritual
        if c == '\n':
            self._advance_newline()
            return
        
        # Comments - the hidden wisdom
        if c == '#':
            self._skip_comment()
            return
        
        # Structural tokens - the architecture of meaning
        if c == '[':
            self._emit(TokenType.LEFT_BRACKET, c)
            return
        if c == ']':
            self._emit(TokenType.RIGHT_BRACKET, c)
            return
        if c == '{':
            self._emit(TokenType.LEFT_BRACE, c)
            return
        if c == '}':
            self._emit(TokenType.RIGHT_BRACE, c)
            return
        if c == ':':
            self._emit(TokenType.COLON, c)
            return
        if c == ',':
            self._emit(TokenType.COMMA, c)
            return
        
        # Strings - the voice of chaos
        if c == '"':
            self._scan_string()
            return
        
        # Numbers - the measurement of intensity
        if c == '-' and self._peek_next().isdigit():
            self._scan_number(allow_negative=True)
            return
        if c.isdigit():
            self._scan_number()
            return
        
        # Identifiers and keywords - the names of symbols
        if c.isalpha() or c == '_':
            self._scan_identifier()
            return
        
        # Unknown character - move past it
        self._advance_simple()
    
    def _emit(self, token_type: TokenType, value: str) -> None:
        """Create and store a token."""
        self.tokens.append(Token(token_type, value, self.line, self.col))
        self._advance_simple()
    
    def _advance_simple(self) -> None:
        """Move to the next character, updating column."""
        self.i += 1
        self.col += 1
    
    def _advance_newline(self) -> None:
        """Move to the next line."""
        self.i += 1
        self.line += 1
        self.col = 1
    
    def _skip_comment(self) -> None:
        """Skip until the end of the current line."""
        while self.i < len(self.source) and self.source[self.i] != '\n':
            self.i += 1
    
    def _scan_string(self) -> None:
        """Extract a quoted string value."""
        self.i += 1  # Skip opening quote
        start = self.i
        
        while self.i < len(self.source) and self.source[self.i] != '"':
            if self.source[self.i] == '\n':
                self.line += 1
                self.col = 1
            self.i += 1
        
        value = self.source[start:self.i]
        if self.i < len(self.source) and self.source[self.i] == '"':
            self.i += 1  # Skip closing quote
        
        self.tokens.append(Token(TokenType.STRING, value, self.line, self.col))
        self.col += len(value) + 2  # Account for quotes
    
    def _peek_next(self) -> str:
        """Look at the next character without consuming it."""
        if self.i + 1 >= len(self.source):
            return '\0'
        return self.source[self.i + 1]

    def _scan_number(self, allow_negative: bool = False) -> None:
        """Extract a numeric value."""
        start = self.i
        if allow_negative and self.source[self.i] == '-':
            self.i += 1
        while self.i < len(self.source) and self.source[self.i].isdigit():
            self.i += 1
        
        value = self.source[start:self.i]
        self.tokens.append(Token(TokenType.NUMBER, value, self.line, self.col))
        self.col += len(value)
    
    def _scan_identifier(self) -> None:
        """Extract an identifier or keyword."""
        start = self.i
        while (self.i < len(self.source) and 
               (self.source[self.i].isalnum() or self.source[self.i] == '_')):
            self.i += 1
        
        word = self.source[start:self.i]
        token_type = self.keywords.get(word.upper(), TokenType.IDENTIFIER)
        
        # Handle boolean and null values
        if token_type == TokenType.BOOLEAN:
            value = word.upper() == 'TRUE'
        elif token_type == TokenType.NULL:
            value = None
        else:
            value = word
        
        self.tokens.append(Token(token_type, value, self.line, self.col))
        self.col += len(word)
