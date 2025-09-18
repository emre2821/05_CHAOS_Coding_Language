"""
Undirected lightweight graph for symbols/entities.
"""
from typing import Any, Dict, Set

from chaos_errors import ChaosGraphError


class ChaosGraph:
    def __init__(self):
        self.nodes: Set[str] = set()
        self.edges: Dict[str, Set[str]] = {}

    def add_node(self, node: str) -> None:
        self.nodes.add(node)
        self.edges.setdefault(node, set())

    def add_edge(self, a: str, b: str) -> None:
        if a == b:
            return
        self.add_node(a)
        self.add_node(b)
        self.edges[a].add(b)
        self.edges[b].add(a)

    def neighbors(self, node: str) -> Set[str]:
        if node not in self.edges:
            raise ChaosGraphError(f"Unknown node: {node}")
        return set(self.edges[node])

    def __repr__(self) -> str:
        return f"CHAOSGraph(nodes={len(self.nodes)}, edges={sum(len(v) for v in self.edges.values())})"
