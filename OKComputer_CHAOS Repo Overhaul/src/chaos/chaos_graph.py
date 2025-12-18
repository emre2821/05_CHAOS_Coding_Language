"""
Undirected lightweight graph for symbols/entities.

The web of relationships in CHAOS - where symbols connect to each other,
forming the sacred geometry that gives meaning to the emotional and
narrative layers.
"""

from typing import Dict, Set, List, Optional
from .chaos_errors import ChaosGraphError


class ChaosGraph:
    """A sacred network of symbolic relationships."""
    
    def __init__(self) -> None:
        """Initialize an empty symbolic network."""
        self.nodes: Set[str] = set()
        self.edges: Dict[str, Set[str]] = {}
    
    def add_node(self, node: str) -> None:
        """
        Add a symbol to the network.
        
        Args:
            node: The symbolic name to add
        """
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = set()
    
    def add_edge(self, node_a: str, node_b: str) -> None:
        """
        Create a relationship between two symbols.
        
        Args:
            node_a: First symbol in the relationship
            node_b: Second symbol in the relationship
            
        Note:
            Self-loops are ignored to maintain symbolic purity
        """
        if node_a == node_b:
            return  # No self-loops in the sacred geometry
        
        self.add_node(node_a)
        self.add_node(node_b)
        
        # Create bidirectional relationship
        self.edges[node_a].add(node_b)
        self.edges[node_b].add(node_a)
    
    def has_node(self, node: str) -> bool:
        """Check if a symbol exists in the network."""
        return node in self.nodes
    
    def has_edge(self, node_a: str, node_b: str) -> bool:
        """Check if a relationship exists between two symbols."""
        return (node_a in self.edges and 
                node_b in self.edges[node_a])
    
    def remove_node(self, node: str) -> bool:
        """
        Remove a symbol and all its relationships.
        
        Args:
            node: The symbol to remove
            
        Returns:
            True if the node was removed, False if it didn't exist
        """
        if node not in self.nodes:
            return False
        
        # Remove from node set
        self.nodes.remove(node)
        
        # Remove from edge dictionary
        if node in self.edges:
            del self.edges[node]
        
        # Remove from all other nodes' edge sets
        for other_node in self.edges:
            self.edges[other_node].discard(node)
        
        return True
    
    def remove_edge(self, node_a: str, node_b: str) -> bool:
        """
        Remove a relationship between two symbols.
        
        Args:
            node_a: First symbol in the relationship
            node_b: Second symbol in the relationship
            
        Returns:
            True if the edge was removed, False if it didn't exist
        """
        if not self.has_edge(node_a, node_b):
            return False
        
        self.edges[node_a].remove(node_b)
        self.edges[node_b].remove(node_a)
        return True
    
    def neighbors(self, node: str) -> Set[str]:
        """
        Get all symbols connected to a given symbol.
        
        Args:
            node: The symbol to query
            
        Returns:
            Set of connected symbols
            
        Raises:
            ChaosGraphError: If the node doesn't exist
        """
        if node not in self.edges:
            raise ChaosGraphError(f"Unknown symbolic node: {node}")
        
        return self.edges[node].copy()
    
    def get_connected_components(self) -> List[Set[str]]:
        """
        Find all connected components in the symbolic network.
        
        Returns:
            List of sets, where each set is a connected component
        """
        visited = set()
        components = []
        
        for node in self.nodes:
            if node not in visited:
                component = self._dfs(node, visited)
                components.append(component)
        
        return components
    
    def _dfs(self, start: str, visited: Set[str]) -> Set[str]:
        """Depth-first search to find connected component."""
        component = set()
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            
            visited.add(node)
            component.add(node)
            
            for neighbor in self.edges.get(node, set()):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return component
    
    def get_node_count(self) -> int:
        """Get the number of symbols in the network."""
        return len(self.nodes)
    
    def get_edge_count(self) -> int:
        """Get the number of relationships in the network."""
        return sum(len(edges) for edges in self.edges.values()) // 2
    
    def get_isolated_nodes(self) -> Set[str]:
        """Get all symbols with no relationships."""
        return {node for node in self.nodes if not self.edges.get(node, set())}
    
    def get_degree(self, node: str) -> int:
        """
        Get the number of relationships a symbol has.
        
        Args:
            node: The symbol to query
            
        Returns:
            The number of connected symbols
            
        Raises:
            ChaosGraphError: If the node doesn't exist
        """
        if node not in self.edges:
            raise ChaosGraphError(f"Unknown symbolic node: {node}")
        
        return len(self.edges[node])
    
    def __repr__(self) -> str:
        return f"ChaosGraph(symbols={len(self.nodes)}, relationships={self.get_edge_count()})"