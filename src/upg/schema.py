"""
Typed graph schema for the Unified Person Graph.

A ``PersonGraph`` is a signed, weighted, (optionally) gated, stratified
directed graph.  It is the single in-memory object that every analysis in
this package consumes: composition produces one, the axiom/encapsulation
audits check one, and the spectral and dynamic tools read matrices off one.

Design choices that matter for reproducibility:
  * Edges are stored source -> target.  The influence matrix returned by
    :meth:`PersonGraph.adjacency` places entry (target, source), so that the
    matrix-vector product ``W @ x`` is exactly the net drive arriving at each
    node (Axiom 5 / Batch I 5.2).
  * ``weight`` is always a non-negative magnitude; ``sign`` carries the
    direction of influence.  ``signed_weight`` combines them.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

Role = str  # one of {"mother", "interface", "internal"}


@dataclass(frozen=True)
class Node:
    node_id: str
    stratum: str
    label: str = ""
    level: str = ""
    parent: str = ""
    role: Role = "internal"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    weight: float          # non-negative magnitude
    sign: str              # "+" or "-"
    type: str
    gate: str = "none"
    origin: str = ""

    @property
    def signed_weight(self) -> float:
        return self.weight if self.sign == "+" else -self.weight

    @property
    def is_self_loop(self) -> bool:
        return self.source == self.target


@dataclass
class PersonGraph:
    """A stratified signed/weighted/gated directed graph."""
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    # ---- indexing -------------------------------------------------------
    def node_ids(self) -> list[str]:
        return [n.node_id for n in self.nodes]

    def index(self) -> dict[str, int]:
        return {n.node_id: i for i, n in enumerate(self.nodes)}

    @property
    def n(self) -> int:
        return len(self.nodes)

    def stratum_of(self) -> dict[str, str]:
        return {n.node_id: n.stratum for n in self.nodes}

    def role_of(self) -> dict[str, str]:
        return {n.node_id: n.role for n in self.nodes}

    # ---- edge subsets ---------------------------------------------------
    def self_loops(self) -> list[Edge]:
        return [e for e in self.edges if e.is_self_loop]

    def negative_edges(self) -> list[Edge]:
        return [e for e in self.edges if e.sign == "-"]

    def cross_stratum_edges(self) -> list[Edge]:
        strat = self.stratum_of()
        return [e for e in self.edges if strat[e.source] != strat[e.target]]

    def nodes_per_stratum(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for nd in self.nodes:
            out[nd.stratum] = out.get(nd.stratum, 0) + 1
        return out

    # ---- matrices -------------------------------------------------------
    def adjacency(self, signed: bool = True) -> np.ndarray:
        """Influence matrix M with M[target, source] = (signed) edge weight.

        ``M @ x`` is the net drive arriving at each node.  Parallel edges
        (same source & target) are summed, which is the correct behaviour
        for signed superposition.
        """
        idx = self.index()
        M = np.zeros((self.n, self.n))
        for e in self.edges:
            w = e.signed_weight if signed else e.weight
            M[idx[e.target], idx[e.source]] += w
        return M

    def directed_boolean(self) -> np.ndarray:
        """Boolean directed adjacency A[source, target] = edge exists."""
        idx = self.index()
        A = np.zeros((self.n, self.n), dtype=bool)
        for e in self.edges:
            A[idx[e.source], idx[e.target]] = True
        return A

    def weighted_degree(self) -> dict[str, float]:
        """Undirected weighted degree: sum of |weight| over incident edges.

        Matches Batch J Section 6 (both endpoints accumulate each edge's
        magnitude).
        """
        wdeg: dict[str, float] = {}
        for e in self.edges:
            wdeg[e.source] = wdeg.get(e.source, 0.0) + abs(e.weight)
            wdeg[e.target] = wdeg.get(e.target, 0.0) + abs(e.weight)
        return wdeg

    def top_weighted_degree(self, k: int = 12) -> list[tuple[str, float]]:
        return sorted(self.weighted_degree().items(), key=lambda t: -t[1])[:k]
