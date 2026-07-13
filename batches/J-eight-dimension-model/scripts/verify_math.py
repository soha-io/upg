"""
Batch J — verification code.
Reproduces every numerical claim in the manuscript, in section order.
Requires only numpy (plus the CSVs in ../data). Run: python3 verify_math.py
"""
import csv
import itertools
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

DIMS = ["TEM", "DEV", "PER", "NEED", "ME", "DIS", "THER", "SYS"]
ENDO = ["TEM", "DEV", "PER", "NEED", "ME", "DIS", "SYS"]  # THER = control input


def read_csv(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Dimension-level structural matrix W (8x8, signed, directed)
# Parallel channels (SYS support/thwart) combined by mean magnitude for the
# structural/spectral analysis; the dynamic model uses the case-appropriate
# channel explicitly.
# ---------------------------------------------------------------------------
def dimension_W():
    idx = {d: i for i, d in enumerate(DIMS)}
    mags = {}
    for r in read_csv("upg_dimension_edges.csv"):
        key = (idx[r["source"]], idx[r["target"]])
        mags.setdefault(key, []).append(float(r["weight"]))
    W = np.zeros((8, 8))
    for (j, i), vals in mags.items():   # source j -> target i, W[i,j]
        W[i, j] = np.mean(vals)
    return W


# ---------------------------------------------------------------------------
# Problem-load dynamic model (Section 8 worked case).
# State x in [0,1]^7 over ENDO dims; entries of B are the dimension-edge
# priors mapped into the problem frame (all couplings load-increasing;
# protective content lives inside the strata subgraphs). THER enters as
# exogenous control u with gain vector g (load-reducing).
# x(t+1) = tanh( kappa * (B x + g u) + b ),  b = standing conditions.
# ---------------------------------------------------------------------------
B_ROWS = {  # target: {source: weight}
    "TEM":  {"DEV": 0.45, "TEM": 0.45},
    "DEV":  {"TEM": 0.45, "SYS": 0.70, "DEV": 0.50},
    "PER":  {"TEM": 0.65, "DEV": 0.70, "SYS": 0.50, "PER": 0.70},
    "NEED": {"DEV": 0.50, "PER": 0.60, "ME": 0.50, "DIS": 0.45, "SYS": 0.65,
             "NEED": 0.35},
    "ME":   {"TEM": 0.60, "DEV": 0.50, "PER": 0.55, "NEED": 0.80, "SYS": 0.60,
             "ME": 0.35},
    "DIS":  {"TEM": 0.55, "DEV": 0.55, "PER": 0.60, "NEED": 0.55, "ME": 0.60,
             "SYS": 0.60, "DIS": 0.30},
    "SYS":  {"PER": 0.60, "ME": 0.55, "DIS": 0.45, "SYS": 0.50},
}
G_THER = {"DIS": -0.65, "ME": -0.65, "SYS": -0.60, "TEM": -0.45, "PER": -0.40,
          "NEED": -0.45}
KAPPA = 0.42
# Case "Sara": constitutionally high NA, adversity history, ongoing thwarts
B_CASE = {"TEM": 0.35, "DEV": 0.30, "SYS": 0.30}


def dynamic_model():
    n = len(ENDO)
    idx = {d: i for i, d in enumerate(ENDO)}
    B = np.zeros((n, n))
    for tgt, row in B_ROWS.items():
        for src, w in row.items():
            B[idx[tgt], idx[src]] = w
    g = np.zeros(n)
    for tgt, w in G_THER.items():
        g[idx[tgt]] = w
    b = np.zeros(n)
    for tgt, w in B_CASE.items():
        b[idx[tgt]] = w
    return B, g, b, idx


def iterate(B, g, b, u, x0, kappa=KAPPA, T=400):
    x = x0.copy()
    for _ in range(T):
        x = np.tanh(kappa * (B @ x + g * u) + b)
    return x


def jacobian_rho(B, g, b, u, xstar, kappa=KAPPA):
    pre = kappa * (B @ xstar + g * u) + b
    J = (kappa * B) * (1 - np.tanh(pre) ** 2)[:, None]
    return max(abs(np.linalg.eigvals(J)))


def main():
    np.set_printoptions(precision=3, suppress=True)

    # ---- 1. Composition census -------------------------------------------
    print("=" * 72)
    print("1. COMPOSITION CENSUS")
    dn = read_csv("upg_dimension_nodes.csv")
    de = read_csv("upg_dimension_edges.csv")
    selfloops = [r for r in de if r["source"] == r["target"]]
    signed = [r for r in de if r["sign"] == "-"]
    print(f"dimension nodes: {len(dn)}; edge rows: {len(de)} "
          f"({len(de)-len(selfloops)} inter-dimension + {len(selfloops)} self-loops); "
          f"negative-signed rows: {len(signed)}")
    gn = read_csv("upg_greatgraph_nodes.csv")
    ge = read_csv("upg_greatgraph_edges.csv")
    strat = {r["node_id"]: r["stratum"] for r in gn}
    cross = [e for e in ge if strat[e["source"]] != strat[e["target"]]]
    gself = [e for e in ge if e["source"] == e["target"]]
    gsigned = [e for e in ge if e["sign"] == "-"]
    print(f"great graph: {len(gn)} nodes, {len(ge)} edges "
          f"({len(cross)} cross-stratum, {len(gself)} self-loops, "
          f"{len(gsigned)} negative-signed)")
    per_stratum = {}
    for r in gn:
        per_stratum[r["stratum"]] = per_stratum.get(r["stratum"], 0) + 1
    print("nodes per stratum:", dict(sorted(per_stratum.items())))

    # ---- 2. Axiom audit on the Great Graph -------------------------------
    print("=" * 72)
    print("2. AXIOM AUDIT (computed on upg_greatgraph_*.csv)")
    ids = [r["node_id"] for r in gn]
    pos = {v: k for k, v in enumerate(ids)}
    n = len(ids)
    A = np.zeros((n, n), dtype=bool)      # directed adjacency
    for e in ge:
        A[pos[e["source"]], pos[e["target"]]] = True
    # Axiom 1/3: reachability via BFS on directed graph, and weak connectivity
    und = A | A.T
    seen = np.zeros(n, dtype=bool)
    stack = [0]
    seen[0] = True
    while stack:
        v = stack.pop()
        for w in np.nonzero(und[v])[0]:
            if not seen[w]:
                seen[w] = True
                stack.append(w)
    print(f"Axiom 1 (connectivity): weakly connected = {bool(seen.all())} "
          f"({seen.sum()}/{n} nodes in one component)")
    deg = und.sum(1)
    print(f"Axiom 2 (non-dismissibility): isolated nodes = {(deg == 0).sum()}")
    # Hierarchical and binding edges are decomposition/conduit relations:
    # the mother aggregates its children's states (upward) and broadcasts
    # drive to them (downward), so they carry influence both ways.
    A2 = A.copy()
    for e in ge:
        if "hierarchical" in e["type"] or e["type"] == "binding":
            A2[pos[e["target"]], pos[e["source"]]] = True
    R = A2.copy()                          # transitive closure (Warshall, boolean)
    for k in range(n):
        R = R | (np.outer(R[:, k], R[k, :]))
    np.fill_diagonal(R, False)
    frac = R.sum() / (n * (n - 1))
    print(f"Axiom 3 (mediated influence): reachability fill = {frac:.3f} "
          f"(fraction of ordered node pairs connected by a directed path, "
          f"with decomposition edges carrying aggregation upward)")
    print(f"Axiom 4 (self-loops): {len(gself)} explicit self-loops present")
    print(f"Axiom 5 (signed superposition): {len(gsigned)} negative edges coexist "
          f"with positive edges (net drive = signed sum, cf. Batch I §5.2)")

    # ---- 3. Spectral analysis of the dimension graph ---------------------
    print("=" * 72)
    print("3. SPECTRAL ANALYSIS (8-node dimension graph)")
    W = dimension_W()
    Wm = np.abs(W)
    np.fill_diagonal(Wm, 0.0)
    S = (Wm + Wm.T) / 2
    D = np.diag(S.sum(1))
    L = D - S
    lam, V = np.linalg.eigh(L)
    print("Laplacian eigenvalues:", np.round(lam, 3))
    lam2 = lam[1]
    v2 = V[:, 1]
    if v2[DIMS.index("SYS")] > 0:     # fix sign convention for reporting
        v2 = -v2
    print(f"algebraic connectivity lambda_2 = {lam2:.3f}")
    print("Fiedler vector:")
    for d, val in zip(DIMS, v2):
        print(f"   {d:5s} {val:+.3f}")
    partA = [d for d, val in zip(DIMS, v2) if val < 0]
    partB = [d for d, val in zip(DIMS, v2) if val >= 0]
    print(f"Fiedler partition: {partA} | {partB}")
    order = np.argsort(np.abs(v2))
    print("bridge ranking (smallest |v2| first):",
          [f"{DIMS[i]}={abs(v2[i]):.3f}" for i in order[:3]])
    # eigenvector centrality on symmetrized magnitudes
    ew, ev = np.linalg.eigh(S)
    c = np.abs(ev[:, -1])
    c = c / c.max()
    print("structural centrality (eigenvector, max=1):",
          {d: float(round(v, 3)) for d, v in sorted(zip(DIMS, c), key=lambda t: -t[1])})

    # ---- 4. Signed loops on the case's effective matrix -------------------
    # Signed cycle analysis needs the parallel SYS channels resolved; we use
    # the worked case's effective signed matrix: the problem-frame couplings
    # of Section 5 extended by the treatment loop DIS->THER (+0.70) and the
    # THER-> gains. Positive gain = self-amplifying, negative = regulating.
    print("=" * 72)
    print("4. SIGNED INTER-DIMENSION CYCLES (case-effective matrix)")
    Bc, gc, _, eidx0 = dynamic_model()
    m = len(ENDO) + 1
    Wc = np.zeros((m, m))
    Wc[:len(ENDO), :len(ENDO)] = Bc
    ti = len(ENDO)                          # THER index
    Wc[ti, eidx0["DIS"]] = 0.70             # DIS -> THER (treatment seeking)
    Wc[:len(ENDO), ti] = gc                 # THER -> dims (signed gains)
    np.fill_diagonal(Wc, 0.0)               # cycles = inter-node loops only
    names = ENDO + ["THER"]
    cycles = []
    for k in (2, 3):
        for combo in itertools.permutations(range(m), k):
            if combo[0] != min(combo):
                continue
            gpath, ok = 1.0, True
            for a, bnode in zip(combo, combo[1:] + combo[:1]):
                w = Wc[bnode, a]
                if w == 0:
                    ok = False
                    break
                gpath *= w
            if ok:
                cycles.append((gpath, [names[i] for i in combo]))
    cycles.sort(key=lambda t: -t[0])
    print("top amplifying loops:")
    for gpath, path in cycles[:5]:
        print(f"   gain {gpath:+.3f}: {' -> '.join(path)} -> {path[0]}")
    print("top regulating loops:")
    for gpath, path in sorted(cycles, key=lambda t: t[0])[:3]:
        print(f"   gain {gpath:+.3f}: {' -> '.join(path)} -> {path[0]}")

    # ---- 5. Worked case: fixed points, stability, treatment --------------
    print("=" * 72)
    print("5. WORKED CASE (problem-load dynamics, kappa =", KAPPA, ")")
    B, g, b, eidx = dynamic_model()
    x_lo = iterate(B, g, b, u=0.0, x0=np.zeros(7))
    x_hi = iterate(B, g, b, u=0.0, x0=np.ones(7))
    print("untreated fixed point from x0=0:",
          {d: float(round(v, 3)) for d, v in zip(ENDO, x_lo)})
    print("untreated fixed point from x0=1:",
          {d: float(round(v, 3)) for d, v in zip(ENDO, x_hi)})
    bistable = np.max(np.abs(x_hi - x_lo)) > 1e-3
    print(f"bistable at kappa={KAPPA}: {bistable}")
    rho_hi = jacobian_rho(B, g, b, 0.0, x_hi)
    print(f"disorder attractor: DIS = {x_hi[eidx['DIS']]:.3f}, "
          f"spectral radius rho(J) = {rho_hi:.3f} (<1: locally stable)")
    if bistable:
        rho_lo = jacobian_rho(B, g, b, 0.0, x_lo)
        print(f"healthy attractor:  DIS = {x_lo[eidx['DIS']]:.3f}, "
              f"rho(J) = {rho_lo:.3f}")
    # bifurcation structure of the composed system (cf. Batch I §5.4):
    # at b = 0 the quiescent state x = 0 loses stability when the loop gain
    # kappa * lambda_max(B) crosses 1 (pitchfork); standing input b > 0
    # unfolds the pitchfork, which is why the case is monostable-high.
    lam_max = max(np.real(np.linalg.eigvals(B)))
    k_crit = 1.0 / lam_max
    print(f"lambda_max(B) = {lam_max:.3f} -> critical coupling "
          f"kappa* = 1/lambda_max = {k_crit:.3f}")
    for k in (0.9 * k_crit, 1.3 * k_crit):
        z_lo = iterate(B, g, np.zeros(7), 0.0, np.zeros(7) + 1e-3, kappa=k)
        z_hi = iterate(B, g, np.zeros(7), 0.0, np.ones(7), kappa=k)
        tag = "bistable (quiescent unstable, disorder attractor exists)" \
            if abs(z_hi[eidx["DIS"]]) > 1e-2 else "monostable quiescent"
        print(f"   b=0, kappa={k:.3f}: |x*_DIS| from x0~0 -> "
              f"{abs(z_lo[eidx['DIS']]):.3f}, from x0=1 -> "
              f"{abs(z_hi[eidx['DIS']]):.3f}  [{tag}]")
    print(f"case has b > 0 (constitution + history + ongoing thwarts): "
          f"pitchfork unfolds; untreated system is monostable-high at "
          f"kappa = {KAPPA} = {KAPPA/k_crit:.2f}*kappa*")
    # treatment as state-shifting control: switch u on
    for u in (0.5, 0.8):
        x_tr = iterate(B, g, b, u=u, x0=x_hi)
        print(f"treated (u={u}): fixed point "
              f"{ {d: float(round(v, 3)) for d, v in zip(ENDO, x_tr)} }  "
              f"rho(J) = {jacobian_rho(B, g, b, u, x_tr):.3f}")
    x_tr = iterate(B, g, b, u=0.8, x0=x_hi)
    x_relapse = iterate(B, g, b, u=0.0, x0=x_tr)
    print(f"after withdrawal of treatment (u back to 0): DIS = "
          f"{x_relapse[eidx['DIS']]:.3f} "
          f"({'returns to pre-treatment attractor' if x_relapse[eidx['DIS']] > 0.5 else 'holds in healthy basin'})")
    # structure-changing intervention: edge surgery on W (what successful
    # therapy consolidates: regulation skills, softened frustration->appraisal
    # coupling, family/context change), then withdraw u entirely
    Bs = B.copy()
    Bs[eidx["ME"], eidx["NEED"]] = 0.50    # need-frustration -> appraisal, softened
    Bs[eidx["DIS"], eidx["ME"]] = 0.35     # regulation acquired (Gross; Batch G)
    Bs[eidx["DIS"], eidx["DIS"]] = 0.20    # relapse-prevention breaks symptom loops
    Bs[eidx["NEED"], eidx["SYS"]] = 0.40   # environmental thwart of needs, reduced
    Bs[eidx["ME"], eidx["SYS"]] = 0.35     # situational threat load, reduced
    bs = b.copy()
    bs[eidx["SYS"]] = 0.15                 # family intervention lowers standing thwart
    x_surg = iterate(Bs, g, bs, u=0.0, x0=x_tr)
    print(f"after edge surgery (NEED->ME 0.80->0.50, ME->DIS 0.60->0.35, "
          f"DIS self-loop 0.30->0.20, SYS->NEED 0.65->0.40, SYS->ME "
          f"0.60->0.35, standing SYS input 0.30->0.15), untreated fixed point: "
          f"{ {d: float(round(v, 3)) for d, v in zip(ENDO, x_surg)} }")
    print(f"   DIS without ongoing treatment: {x_hi[eidx['DIS']]:.3f} -> "
          f"{x_surg[eidx['DIS']]:.3f}; residual load persists (constitution "
          f"and history are not erased) -> durable change = rewriting W, "
          f"not only driving x")
    x_maint = iterate(Bs, g, bs, u=0.3, x0=x_surg)
    print(f"edge surgery + maintenance dose (u=0.3): DIS = "
          f"{x_maint[eidx['DIS']]:.3f} "
          f"{ {d: float(round(v, 3)) for d, v in zip(ENDO, x_maint)} }")

    # ---- 6. Node importance in the Great Graph ---------------------------
    print("=" * 72)
    print("6. STRUCTURAL NODE IMPORTANCE (weighted degree, Great Graph)")
    wdeg = {}
    for e in ge:
        w = abs(float(e["weight"]))
        wdeg[e["source"]] = wdeg.get(e["source"], 0) + w
        wdeg[e["target"]] = wdeg.get(e["target"], 0) + w
    top = sorted(wdeg.items(), key=lambda t: -t[1])[:12]
    for nid, w in top:
        print(f"   {nid:18s} {w:6.2f}")


if __name__ == "__main__":
    main()
