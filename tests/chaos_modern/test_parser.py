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

    def test_emotion_tag_routed_to_emotive_layer(self):
        """Regression: ensure emotion tags bypass structured core parsing."""
        source = "[EMOTION:JOY:7]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()

        assert ast.children[0].value == {}
        assert ast.children[1].value == [{"name": "JOY", "intensity": 7}]

    def test_emotion_tag_with_structured_core(self):
        """Ensure emotion tags following structured core data are routed correctly."""
        source = "[META] : 1 [EMOTION:JOY:7]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()

        # Structured core layer should capture the META entry
        assert ast.children[0].value == {"META": "1"}
        # Emotive layer should capture the emotion tag
        assert ast.children[1].value == [{"name": "JOY", "intensity": 7}]

    def test_emotion_tag_interleaved_with_text_and_chaosfield(self):
        """
        Ensure emotion tags are detected when interleaved with free text and chaosfield content.

        The parser advances through non-bracket tokens in both the structured and emotive layers,
        so the emotive entry must still be detected and the chaosfield layer must capture the
        block beginning with the first brace.
        """
        source = "intro [EMOTION:JOY:7] middle {chaos} outro"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()

        # Emotive layer should still capture the emotion tag regardless of surrounding text/chaosfield
        emotive_layer = ast.children[1]
        assert emotive_layer.value == [{"name": "JOY", "intensity": 7}]

        # Chaosfield / free-text layer should capture the content inside the braces.
        chaos_layer = ast.children[2]
        assert chaos_layer.value == "chaos"

    def test_symbol_tag_bypasses_structured_core(self):
        """Regression: ensure symbol tags are not consumed as structured keys."""
        source = "[SYMBOL:GROWTH:PRESENT]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()

        assert ast.children[0].value == {}
        assert ast.children[1].value == []

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

    def test_negative_emotion_intensity_is_parsed(self):
        """Ensure negative numeric intensities are processed without disrupting parsing."""
        source = "[EMOTION:SADNESS:-3]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()

        assert ast.children[1].value == [{"name": "SADNESS", "intensity": 0}]

    def test_non_emotive_tag_triplet_is_ignored_by_structured_core(self):
        """Tag-like triplets that are not routed emotions should bypass structured core."""
        source = "[META:FOO:BAR]"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()

        assert ast.children[0].value == {}
        assert ast.children[1].value == []

    def test_malformed_tag_patterns_do_not_pollute_layers(self):
        """Malformed tag triplets should not corrupt structured core or chaosfield parsing."""
        cases = [
            ("[EMOTION::7]", [], ""),
            ("[EMOTION:JOY:]", [{"name": "JOY", "intensity": 5}], ""),
            ("[EMOTION:JOY 7]", [], ""),
            ("prefix [EMOTION:JOY middle {chaos text} end", [], "chaos text"),
        ]

        for source, expected_emotions, expected_chaos in cases:
            lexer = ChaosLexer()
            tokens = lexer.tokenize(source)
            parser = ChaosParser(tokens)
            ast = parser.parse()

            # Structured core should stay empty regardless of malformed tags
            assert ast.children[0].value == {}

            # Emotive layer should reflect any recoverable emotion tags without crashing
            assert ast.children[1].value == expected_emotions

            # Chaosfield should still parse brace-enclosed content when present
            assert ast.children[2].value == expected_chaos

    def test_chaosfield_after_multiple_tags(self):
        """Ensure chaosfield parsing starts at the first brace after tag-like content."""
        source = "[META] : 1 [EMOTION:JOY:2] lead-in {inside chaos} trailing"
        lexer = ChaosLexer()
        tokens = lexer.tokenize(source)
        parser = ChaosParser(tokens)
        ast = parser.parse()

        assert ast.children[0].value == {"META": "1"}
        assert ast.children[1].value == [{"name": "JOY", "intensity": 2}]
        assert ast.children[2].value == "inside chaos"
