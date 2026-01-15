"""Tests for the CHAOS lexical analyzer."""

import pytest
from chaos_legacy.chaos_lexer import ChaosLexer, TokenType, Token


class TestChaosLexer:
    """Test the sacred token recognition patterns."""
    
    def test_empty_source(self):
        """Test tokenization of empty source."""
        lexer = ChaosLexer()
        tokens = lexer.tokenize("")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_simple_symbol(self):
        """Test tokenization of a simple symbol definition."""
        source = '[NAME]: "value"'
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        
        assert len(tokens) == 6
        assert tokens[0].type == TokenType.LEFT_BRACKET
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "NAME"
        assert tokens[2].type == TokenType.RIGHT_BRACKET
        assert tokens[3].type == TokenType.COLON
        assert tokens[4].type == TokenType.STRING
        assert tokens[4].value == "value"
        assert tokens[5].type == TokenType.EOF
    
    def test_emotion_triplet(self):
        """Test tokenization of emotion triplets."""
        source = "[EMOTION:JOY:7]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        
        expected_types = [
            TokenType.LEFT_BRACKET,
            TokenType.IDENTIFIER,  # EMOTION
            TokenType.COLON,
            TokenType.IDENTIFIER,  # JOY
            TokenType.COLON,
            TokenType.NUMBER,      # 7
            TokenType.RIGHT_BRACKET,
            TokenType.EOF
        ]
        
        assert len(tokens) == len(expected_types)
        for i, expected_type in enumerate(expected_types):
            assert tokens[i].type == expected_type
    
    def test_chaosfield_text(self):
        """Test tokenization of chaosfield narrative text."""
        source = '{ "Sacred text" }'
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        
        assert tokens[0].type == TokenType.LEFT_BRACE
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "Sacred text"
        assert tokens[2].type == TokenType.RIGHT_BRACE
        assert tokens[3].type == TokenType.EOF
    
    def test_keywords(self):
        """Test recognition of CHAOS keywords."""
        source = "TRUE FALSE NULL"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        
        assert tokens[0].type == TokenType.BOOLEAN
        assert tokens[0].value is True
        assert tokens[1].type == TokenType.BOOLEAN
        assert tokens[1].value is False
        assert tokens[2].type == TokenType.NULL
        assert tokens[2].value is None
    
    def test_comments(self):
        """Test that comments are ignored."""
        source = """
        # This is a sacred comment
        [SYMBOL]: "value"  # Another comment
        """
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        
        # Should only have the meaningful tokens
        meaningful_tokens = [t for t in tokens if t.type != TokenType.EOF]
        assert len(meaningful_tokens) == 5  # [, SYMBOL, ], :, "value"
    
    def test_complex_program(self):
        """Test tokenization of a complete CHAOS program."""
        source = """
        [EVENT]: memory
        [SYMBOL:GROWTH:PRESENT]
        [EMOTION:JOY:7]
        {
        The garden was alive with color and quiet courage.
        }
        """
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        
        # Verify we have the expected structure
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        
        # Should have brackets, identifiers, colons, strings, braces
        assert TokenType.LEFT_BRACKET in token_types
        assert TokenType.RIGHT_BRACKET in token_types
        assert TokenType.IDENTIFIER in token_types
        assert TokenType.COLON in token_types
        assert TokenType.STRING in token_types
        assert TokenType.LEFT_BRACE in token_types
        assert TokenType.RIGHT_BRACE in token_types
