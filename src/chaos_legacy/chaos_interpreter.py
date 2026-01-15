"""
Interpreter: walk parse tree -> environment dict.

The heart of CHAOS execution - where the three-layer structure becomes
living memory, where symbols gain emotional weight, and where the
narrative chaos finds its place in the symbolic ecosystem.
"""

from typing import Dict, Any, Optional
from .chaos_parser import NodeType, Node
from .chaos_errors import ChaosRuntimeError


class ChaosInterpreter:
    """Brings the CHAOS ritual to life through execution."""
    
    def __init__(self) -> None:
        """Initialize the interpreter with an empty environment."""
        self.environment: Dict[str, Any] = {}
        self.reset()
    
    def reset(self) -> None:
        """Clear the environment for a new ritual."""
        self.environment = {}
    
    def interpret(self, node: Node) -> Dict[str, Any]:
        """
        Execute the CHAOS parse tree and build the environment.
        
        This is where the three layers become living memory:
        - Structured core becomes symbolic foundation
        - Emotive layer becomes emotional resonance
        - Chaosfield layer becomes narrative context
        
        Args:
            node: The root node of the CHAOS parse tree
            
        Returns:
            The complete environment dictionary with three layers
            
        Raises:
            ChaosRuntimeError: If interpretation fails
        """
        try:
            if node.type == NodeType.PROGRAM:
                # Process each layer in the sacred order
                for child in node.children:
                    self.interpret(child)
            
            elif node.type == NodeType.STRUCTURED_CORE:
                # The bones of the ritual - symbols and their values
                self.environment["structured_core"] = node.value or {}
            
            elif node.type == NodeType.EMOTIVE_LAYER:
                # The heart of the ritual - emotions and their intensities
                self.environment["emotive_layer"] = node.value or []
            
            elif node.type == NodeType.CHAOSFIELD_LAYER:
                # The spirit of the ritual - free narrative text
                self.environment["chaosfield_layer"] = node.value or ""
            
            else:
                raise ChaosRuntimeError(f"Unknown node type: {node.type}")
            
            return self.environment
            
        except Exception as e:
            raise ChaosRuntimeError(f"Failed to interpret CHAOS program: {e}")