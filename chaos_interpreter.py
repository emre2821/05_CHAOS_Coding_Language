"""
Interpreter: walk parse tree -> environment dict.
"""
from typing import Dict, Any

from chaos_parser import NodeType, Node


class ChaosInterpreter:
    def __init__(self):
        self.environment = {}

    def reset(self):
        self.environment = {}

    def interpret(self, node: Node) -> Dict[str, Any]:
        if node.type == NodeType.PROGRAM:
            for child in node.children:
                self.interpret(child)
        elif node.type == NodeType.STRUCTURED_CORE:
            self.environment["structured_core"] = node.value or {}
        elif node.type == NodeType.EMOTIVE_LAYER:
            self.environment["emotive_layer"] = node.value or []
        elif node.type == NodeType.CHAOSFIELD_LAYER:
            self.environment["chaosfield_layer"] = node.value or ""
        else:
            raise ValueError(f"Unknown node: {node.type}")
        return self.environment
