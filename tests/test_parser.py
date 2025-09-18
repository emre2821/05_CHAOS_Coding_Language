from chaos_lexer import ChaoLexer
from chaos_parser import ChaoParser, NodeType

def test_parse_three_layers():
    src = '''
    [EVENT]: memory
    [EMOTION:JOY:7]
    { The garden was alive. }
    '''
    ast = ChaoParser(ChaoLexer().tokenize(src)).parse()
    assert ast.type == NodeType.PROGRAM
    assert len(ast.children) == 3