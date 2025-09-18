import pytest
from chaos_lexer import ChaoLexer, TokenType

def test_lex_basic_pairs():
    src = '[EVENT]: memory\n[CONTEXT]: garden\n'
    toks = ChaoLexer().tokenize(src)
    assert any(t.type == TokenType.LEFT_BRACKET for t in toks)
    assert any(t.value == "EVENT" for t in toks)
    assert any(t.type == TokenType.COLON for t in toks)

def test_lex_emotion_tag():
    src = '[EMOTION:JOY:7]'
    toks = ChaoLexer().tokenize(src)
    kinds = [t.type.name for t in toks]
    assert "LEFT_BRACKET" in kinds and "RIGHT_BRACKET" in kinds
    assert any(t.value == "EMOTION" for t in toks)
    assert any(t.value == "JOY" for t in toks)
