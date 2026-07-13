#!/usr/bin/env python3
"""
Reproduce every headline number of Batches I and J from the packaged model.

This replaces the two per-batch ``verify_math.py`` scripts with a single
report driven by the ``upg`` package.  Run:

    python scripts/reproduce.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from upg import (axiom_audit, build_person_graph, case_report,  # noqa: E402
                 dimension_spectral_report, encapsulation_violations)


def rule(title: str) -> None:
    print("=" * 72)
    print(title)


def main() -> None:
    pg = build_person_graph()

    rule("1. COMPOSITION CENSUS")
    print(f"great graph: {pg.n} nodes, {len(pg.edges)} edges "
          f"({len(pg.cross_stratum_edges())} cross-stratum, "
          f"{len(pg.self_loops())} self-loops, "
          f"{len(pg.negative_edges())} negative-signed)")
    print("nodes per stratum:", pg.nodes_per_stratum())
    print("encapsulation violations:", encapsulation_violations(pg))

    rule("2. AXIOM AUDIT")
    a = axiom_audit(pg)
    print(f"Axiom 1 (connectivity): weakly connected = {a.weakly_connected} "
          f"({a.component_size}/{a.n_nodes})")
    print(f"Axiom 2 (non-dismissibility): isolated nodes = {a.isolated_nodes}")
    print(f"Axiom 3 (mediated influence): reachability fill = {a.reachability_fill:.3f}")
    print(f"Axiom 4 (self-influence): self-loops = {a.self_loops}")
    print(f"Axiom 5 (signed superposition): negative edges = {a.negative_edges}")

    rule("3. SPECTRAL ANATOMY (dimension graph)")
    sp = dimension_spectral_report()
    print("Laplacian eigenvalues:", sp.eigenvalues)
    print(f"algebraic connectivity lambda_2 = {sp.algebraic_connectivity:.3f}")
    print("Fiedler partition:", sp.partition)
    print("bridge ranking (smallest |v2| first):",
          [f"{d}={m:.3f}" for d, m in sp.bridge_ranking[:3]])
    print("structural centrality:", sp.centrality)

    rule("4. SIGNED INTER-DIMENSION CYCLES")
    cr = case_report()
    print("top amplifying loops:")
    for g, path in cr.top_amplifying[:5]:
        print(f"   gain {g:+.3f}: {' -> '.join(path)} -> {path[0]}")
    print("top regulating loops:")
    for g, path in cr.top_regulating[:3]:
        print(f"   gain {g:+.3f}: {' -> '.join(path)} -> {path[0]}")

    rule("5. WORKED CASE (problem-load dynamics)")
    print("untreated fixed point:", cr.untreated)
    print(f"rho(J) = {cr.untreated_rho:.3f} (<1 stable); bistable = {cr.bistable}")
    print(f"lambda_max(B) = {cr.lambda_max_B:.3f} -> kappa* = {cr.kappa_star:.3f}")
    print("treated u=0.5:", cr.treated[0.5])
    print("treated u=0.8:", cr.treated[0.8])
    print(f"after withdrawal: DIS = {cr.relapse_dis:.3f} (returns to attractor)")
    print("after edge surgery:", cr.surgery)
    print("edge surgery + maintenance:", cr.surgery_maintained)

    rule("6. STRUCTURAL NODE IMPORTANCE (weighted degree)")
    for nid, w in pg.top_weighted_degree(12):
        print(f"   {nid:18s} {w:6.2f}")


if __name__ == "__main__":
    main()
