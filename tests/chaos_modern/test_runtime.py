"""Tests for the CHAOS runtime and execution engine."""

import pytest
from chaos_legacy.chaos_runtime import run_chaos
from chaos_legacy.chaos_errors import ChaosSyntaxError, ChaosRuntimeError


class TestChaosRuntime:
    """Test the sacred execution of CHAOS programs."""
    
    def test_empty_program(self):
        """Test execution of empty program."""
        result = run_chaos("")
        
        assert "structured_core" in result
        assert "emotive_layer" in result
        assert "chaosfield_layer" in result
        assert result["structured_core"] == {}
        assert result["emotive_layer"] == []
        assert result["chaosfield_layer"] == ""
    
    def test_simple_symbol_program(self):
        """Test execution with simple symbols."""
        source = """
        [NAME]: "Concord"
        [TYPE]: "Agent"
        [VERSION]: "2.0"
        """
        result = run_chaos(source)
        
        assert result["structured_core"]["NAME"] == "Concord"
        assert result["structured_core"]["TYPE"] == "Agent"
        assert result["structured_core"]["VERSION"] == "2.0"
        assert result["emotive_layer"] == []
        assert result["chaosfield_layer"] == ""
    
    def test_emotion_program(self):
        """Test execution with emotions."""
        source = """
        [EMOTION:JOY:8]
        [EMOTION:WONDER:6]
        [EMOTION:KINDNESS:9]
        """
        result = run_chaos(source)
        
        assert result["structured_core"] == {}
        assert len(result["emotive_layer"]) == 3
        
        emotions = {e["name"]: e["intensity"] for e in result["emotive_layer"]}
        assert emotions["JOY"] == 8
        assert emotions["WONDER"] == 6
        assert emotions["KINDNESS"] == 9
    
    def test_chaosfield_program(self):
        """Test execution with narrative text."""
        source = """
        {
        In the realm of symbolic computation,
        where meaning flows like water through the channels of syntax,
        we find that code and poetry are not so different.
        }
        """
        result = run_chaos(source)
        
        assert result["structured_core"] == {}
        assert result["emotive_layer"] == []
        assert "symbolic computation" in result["chaosfield_layer"]
        assert "code and poetry" in result["chaosfield_layer"]
    
    def test_complete_program(self):
        """Test execution of complete three-layer program."""
        source = """
        [EVENT]: memory
        [CONTEXT]: garden
        [SYMBOL:GROWTH:PRESENT]
        [EMOTION:JOY:7]
        [EMOTION:HOPE:5]
        {
        The garden was alive with color and quiet courage.
        Every bloom held a story, every leaf a whisper of wisdom.
        In this sacred space, growth was not just possible—it was inevitable.
        }
        """
        result = run_chaos(source)
        
        # Verify structured core
        assert result["structured_core"]["EVENT"] == "memory"
        assert result["structured_core"]["CONTEXT"] == "garden"
        
        # Verify emotive layer
        assert len(result["emotive_layer"]) == 2
        emotions = {e["name"]: e["intensity"] for e in result["emotive_layer"]}
        assert emotions["JOY"] == 7
        assert emotions["HOPE"] == 5
        
        # Verify chaosfield
        assert "garden was alive" in result["chaosfield_layer"]
        assert "sacred space" in result["chaosfield_layer"]
    
    def test_invalid_syntax(self):
        """Test handling of invalid syntax."""
        source = "[UNCLOSED"
        
        with pytest.raises(ChaosSyntaxError):
            run_chaos(source)
    
    def test_mixed_complexity(self):
        """Test program with mixed symbolic and emotional complexity."""
        source = """
        [PERSONA]: "Seeker"
        [JOURNEY]: "beginning"
        [EMOTION:WONDER:9]
        [EMOTION:CURIOSITY:7]
        [SYMBOL:PATH:UNCERTAIN]
        [RELATIONSHIP:GUIDE:TRUST:8]
        {
        Every journey begins with a single step into the unknown.
        The path reveals itself to those who dare to walk it.
        }
        """
        result = run_chaos(source)
        
        # Should have symbols, emotions, and narrative
        assert len(result["structured_core"]) >= 2
        assert len(result["emotive_layer"]) >= 2
        assert len(result["chaosfield_layer"]) > 0
        
        # Check specific values
        assert result["structured_core"]["PERSONA"] == "Seeker"
        assert result["structured_core"]["JOURNEY"] == "beginning"
    
    def test_verbose_execution(self):
        """Test verbose execution mode."""
        source = '[TEST]: "verbose"'
        
        # Should not raise any errors in verbose mode
        result = run_chaos(source, verbose=True)
        
        assert result["structured_core"]["TEST"] == "verbose"
    
    def test_unicode_handling(self):
        """Test handling of unicode characters in CHAOS programs."""
        source = """
        [MESSAGE]: "Welcome to CHAOS 🌌"
        [EMOTION:JOY:8]
        {
        The universe speaks in many languages: 中文, العربية, Русский
        All are welcome in the realm of symbolic computation.
        }
        """
        result = run_chaos(source)
        
        assert "🌌" in result["structured_core"]["MESSAGE"]
        assert "中文" in result["chaosfield_layer"]
        assert "العربية" in result["chaosfield_layer"]
