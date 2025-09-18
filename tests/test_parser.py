from chaos_lexer import ChaosLexer
from chaos_parser import ChaosParser, NodeType


def test_parse_three_layers():
    src = """
    [EVENT]: memory
    [EMOTION:JOY:7]
    { The garden was alive. }
    """
    ast = ChaosParser(ChaosLexer().tokenize(src)).parse()
    assert ast.type == NodeType.PROGRAM
    assert len(ast.children) == 3
