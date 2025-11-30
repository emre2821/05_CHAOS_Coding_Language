import pytest

from chaos_language import ChaosLexer, ChaosParser
from chaos_language.chaos_parser import NodeType


def test_parse_three_layers():
    src = """
    [EVENT]: memory
    [EMOTION:JOY:7]
    { The garden was alive. }
    """
    ast = ChaosParser(ChaosLexer().tokenize(src)).parse()
    assert ast.type == NodeType.PROGRAM
    assert len(ast.children) == 3


def test_chaosfield_requires_closing_brace():
    src = """
    [EVENT]: memory
    [EMOTION:JOY:7]
    { The garden was alive.
    """
    with pytest.raises(SyntaxError):
        ChaosParser(ChaosLexer().tokenize(src)).parse()
