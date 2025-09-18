# chaos_interpreter.py

from enum import Enum, auto

class ChaoInterpreter:
    def __init__(self):
        self.environment = {}

    def reset(self):
        self.environment = {}

    def interpret(self, node):
        if node.type.name == "PROGRAM":
            for child in node.children:
                self.interpret(child)

        elif node.type.name == "STRUCTURED_CORE":
            self.environment["structured_core"] = node.value

        elif node.type.name == "EMOTIVE_LAYER":
            self.environment["emotive_layer"] = node.value

        elif node.type.name == "CHAOSFIELD_LAYER":
            self.environment["chaosfield_layer"] = node.value

        else:
            raise ValueError(f"Unknown node type: {node.type}")
