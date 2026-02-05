# tests/test_chaos_canonical.py
import pytest
from pathlib import Path

# Test canonical imports
from chaos_language import (
    ChaosLexer,
    ChaosParser,
    ChaosInterpreter,
    run_chaos,
    validate_chaos,
    ChaosAgent,
    ChaosEmotionStack,
)


def test_canonical_imports_resolve():
    """Verify canonical package imports work."""
    assert ChaosLexer is not None
    assert ChaosParser is not None
    assert ChaosInterpreter is not None
    assert run_chaos is not None
    assert validate_chaos is not None
    assert ChaosAgent is not None
    assert ChaosEmotionStack is not None


def test_canonical_classes_instantiable():
    """Smoke test that core classes can be instantiated."""
    lexer = ChaosLexer()
    assert lexer is not None
    
    context = ChaosEmotionStack()
    assert context is not Nonedef test_mirror_shims_exist():
    """Verify deprecation shims were created in mirror locations."""
    repo_root = Path(__file__).parent.parent.parent
    
    mirrors = [
        repo_root / "EdenOS_Origin/vaults/EdenOS_Origin/05_CHAOS_Coding_Language",
        repo_root / "EdenOS_Origin/vaults/EdenOS_Origin/000_Eden_Dropbox/EdenOS_Mobile/CHAOS",
    ]
    
    for mirror in mirrors:
        # Check deprecation README exists
        readme = mirror / "README_DEPRECATED.md"
        assert readme.exists(), f"Missing deprecation notice in {mirror}"
        
        # Check key module shims exist
        key_shims = ["chaos_lexer.py", "chaos_parser.py", "chaos_runtime.py"]
        for shim in key_shims:
            shim_path = mirror / shim
            assert shim_path.exists(), f"Missing shim: {shim_path}"
            
            # Verify shim contains deprecation warning
            content = shim_path.read_text()
            assert "DEPRECATED" in content
            assert "DeprecationWarning" in content
