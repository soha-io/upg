"""
Axiom audit on a composed :class:`~upg.schema.PersonGraph`.

The five axioms become computable properties on the assembled object; this
module reproduces Batch J Section 4.4 exactly and returns the numbers as a
dict so they can be asserted in tests or printed in a report.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .schema import PersonGraph


@dataclass
class AxiomReport:
    weakly_connected: bool
    component_size: int
    n_nodes: int
    isolated_nodes: int
    reachability_fill: float
    self_loops: int
    negative_edges: int

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def axiom_audit(pg: PersonGraph) -> AxiomReport:
    ids = pg.node_ids()
    pos = pg.index()
    n = len(ids)

    A = pg.directed_boolean()          # A[source, target]
    und = A | A.T

    # Axiom 1: weak connectivity via BFS from node 0.
    seen = np.zeros(n, dtype=bool)
    stack = [0]
    seen[0] = True
    while stack:
        v = stack.pop()
        for w in np.nonzero(und[v])[0]:
            if not seen[w]:
                seen[w] = True
                stack.append(w)

    # Axiom 2: no isolated nodes.
    deg = und.sum(1)
    isolated = int((deg == 0).sum())

    # Axiom 3: mediated influence.  Decomposition edges (hierarchical* and
    # binding) also carry aggregation upward, so they count both directions.
    A2 = A.copy()
    for e in pg.edges:
        if "hierarchical" in e.type or e.type == "binding":
            A2[pos[e.target], pos[e.source]] = True
    R = A2.copy()                      # boolean transitive closure
    for k in range(n):
        R = R | np.outer(R[:, k], R[k, :])
    np.fill_diagonal(R, False)
    frac = float(R.sum() / (n * (n - 1)))

    return AxiomReport(
        weakly_connected=bool(seen.all()),
        component_size=int(seen.sum()),
        n_nodes=n,
        isolated_nodes=isolated,
        reachability_fill=frac,
        self_loops=len(pg.self_loops()),
        negative_edges=len(pg.negative_edges()),
    )
