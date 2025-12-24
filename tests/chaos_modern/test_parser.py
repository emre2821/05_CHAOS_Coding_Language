"""Tests for the CHAOS parser and three-layer structure."""

import pytest
from chaos.chaos_parser import ChaosParser, NodeType, Node
from chaos.chaos_lexer import ChaosLexer, TokenType


class TestChaosParser:
    """Test the sacred weaving of tokens into three-layer structure."""
    
    def test_empty_program(self):
        """Test parsing empty source."""
        lexer = ChaosLexer()
        tokens = lexer.tokenize("")
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        assert ast.type == NodeType.PROGRAM
        assert len(ast.children) == 3
        assert ast.children[0].type == NodeType.STRUCTURED_CORE
        assert ast.children[1].type == NodeType.EMOTIVE_LAYER
        assert ast.children[2].type == NodeType.CHAOSFIELD_LAYER
    
    def test_structured_core_only(self):
        """Test parsing structured core layer only."""
        source = '[NAME]: "value"\n[TYPE]: "test"'
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        # Check structure
        assert ast.children[0].type == NodeType.STRUCTURED_CORE
        assert ast.children[0].value == {
            "NAME": "value",
            "TYPE": "test"
        }
        
        # Other layers should be empty
        assert ast.children[1].value == []
        assert ast.children[2].value == ""
    
    def test_emotive_layer_only(self):
        """Test parsing emotive layer only."""
        source = "[EMOTION:JOY:7]\n[EMOTION:HOPE:5]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        # Check emotive layer
        assert ast.children[1].type == NodeType.EMOTIVE_LAYER
        expected_emotions = [
            {"name": "JOY", "intensity": 7},
            {"name": "HOPE", "intensity": 5}
        ]
        assert ast.children[1].value == expected_emotions
        
        # Other layers should be empty
        assert ast.children[0].value == {}
        assert ast.children[2].value == ""
    
    def test_chaosfield_only(self):
        """Test parsing chaosfield layer only."""
        source = '{ "Sacred narrative text" }'
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        # Check chaosfield
        assert ast.children[2].type == NodeType.CHAOSFIELD_LAYER
        assert ast.children[2].value == "Sacred narrative text"
        
        # Other layers should be empty
        assert ast.children[0].value == {}
        assert ast.children[1].value == []
    
    def test_complete_program(self):
        """Test parsing a complete CHAOS program."""
        source = """
        [EVENT]: memory
        [CONTEXT]: garden
        [SYMBOL:GROWTH:PRESENT]
        [EMOTION:JOY:7]
        [EMOTION:HOPE:5]
        {
        The garden was alive with color and quiet courage.
        Every bloom held a story, every leaf a whisper of wisdom.
        }
        """
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        # Verify three-layer structure
        assert len(ast.children) == 3
        
        # Structured core
        structured = ast.children[0]
        assert structured.value["EVENT"] == "memory"
        assert structured.value["CONTEXT"] == "garden"
        
        # Emotive layer
        emotive = ast.children[1]
        assert len(emotive.value) == 2
        assert emotive.value[0]["name"] == "JOY"
        assert emotive.value[0]["intensity"] == 7
        
        # Chaosfield
        chaosfield = ast.children[2]
        assert "garden was alive" in chaosfield.value
        assert "bloom held a story" in chaosfield.value
    
    def test_mixed_tags(self):
        """Test parsing mixed symbol and emotion tags."""
        source = """
        [NAME]: "test"
        [EMOTION:CALM:6]
        [TYPE]: "example"
        [EMOTION:WONDER:8]
        """
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        # Should have two symbols in structured core
        assert len(ast.children[0].value) == 2
        assert ast.children[0].value["NAME"] == "test"
        assert ast.children[0].value["TYPE"] == "example"
        
        # Should have two emotions in emotive layer
        assert len(ast.children[1].value) == 2
        emotions = {e["name"]: e["intensity"] for e in ast.children[1].value}
        assert emotions["CALM"] == 6
        assert emotions["WONDER"] == 8
    
    def test_invalid_emotion_intensity(self):
        """Test handling of invalid emotion intensities."""
        source = "[EMOTION:JOY:invalid]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        # Should default to intensity 5 for invalid values
        assert ast.children[1].value[0]["intensity"] == 5
    
    def test_emotion_intensity_clamping(self):
        """Test that emotion intensities are properly clamped."""
        source = "[EMOTION:JOY:15]\n[EMOTION:SADNESS:-3]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()
        
        emotions = {e["name"]: e["intensity"] for e in ast.children[1].value}
        assert emotions["JOY"] == 10  # Clamped to max
        assert emotions["SADNESS"] == 0  # Clamped to min