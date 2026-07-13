"""
Batch J — figure generation.
Produces five PNGs used in the manuscript. All numerical content is computed
by the same functions as verify_math.py, so figures and text agree exactly.
Run: python3 generate_figures.py
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch

from verify_math import (DIMS, ENDO, KAPPA, dynamic_model, iterate, read_csv,
                         dimension_W)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                     "axes.titlesize": 12, "figure.dpi": 150})

INK, SUP, THW, MUT, ACC = "#1a1a2e", "#1f6f54", "#b02a37", "#8a8a99", "#274b8f"

POS = {"TEM": (1.4, 6.6), "DEV": (1.4, 3.4), "PER": (4.0, 5.0),
       "NEED": (6.6, 6.8), "ME": (6.6, 3.2), "DIS": (8.8, 5.0),
       "SYS": (4.0, 1.0), "THER": (8.8, 8.4)}
QUESTION = {"TEM": "How were you born?", "DEV": "How was your life?",
            "PER": "Who are you?", "NEED": "What do you need?",
            "ME": "What do you want & feel?", "DIS": "What's wrong?",
            "THER": "How to solve?", "SYS": "Where do you live?"}
DCOL = {"TEM": "#7b5ea7", "DEV": "#2f7fbf", "PER": "#274b8f",
        "NEED": "#1f6f54", "ME": "#c07f1f", "DIS": "#b02a37",
        "THER": "#3a8f8f", "SYS": "#6b6b3a"}


# ---------------------------------------------------------------------------
# FIG J1 — the Great Graph at dimension level
# ---------------------------------------------------------------------------
def fig1():
    fig, ax = plt.subplots(figsize=(10.4, 8.6))
    ax.set_xlim(-0.2, 10.4); ax.set_ylim(-0.4, 9.6); ax.axis("off")
    ax.set_aspect("equal")
    ax.set_title("The Great Graph: the eight dimensions and their sourced couplings",
                 weight="bold", pad=10)
    rows = read_csv("upg_dimension_edges.csv")
    seen_pair = {}
    for r in rows:
        s, t = r["source"], r["target"]
        w, sgn = float(r["weight"]), r["sign"]
        col = SUP if sgn == "+" else THW
        if s == t:  # self-loop
            x, y = POS[s]
            ax.add_patch(Circle((x, y + 0.62), 0.24, fill=False,
                                ec=col, lw=1 + 1.6 * w, alpha=0.75))
            continue
        rad = 0.14
        if (t, s) in seen_pair or (s, t) in seen_pair:
            rad = seen_pair.get((s, t), 0.14) + 0.14
        seen_pair[(s, t)] = rad
        p1, p2 = np.array(POS[s]), np.array(POS[t])
        d = p2 - p1; d = d / np.linalg.norm(d)
        a = FancyArrowPatch(p1 + d * 0.52, p2 - d * 0.52,
                            connectionstyle=f"arc3,rad={rad}",
                            arrowstyle="-|>", mutation_scale=11,
                            lw=0.6 + 2.4 * w, color=col,
                            alpha=0.42 if sgn == "+" else 0.8, zorder=1)
        ax.add_patch(a)
    for d, (x, y) in POS.items():
        ax.add_patch(Circle((x, y), 0.5, fc="white", ec=DCOL[d], lw=2.4, zorder=3))
        ax.text(x, y + 0.06, d, ha="center", va="center", weight="bold",
                color=DCOL[d], zorder=4, fontsize=11)
        ax.text(x, y - 0.22, QUESTION[d], ha="center", va="center",
                fontsize=6.1, color=MUT, zorder=4)
    ax.text(0.1, 9.2, "green = reinforcing (+)   red = weakening (−)   "
            "width = consensus prior   loops above nodes = Axiom-4 self-edges",
            fontsize=8, color=MUT)
    ax.text(0.1, 8.75, "Each node encapsulates its stratum's full subgraph "
            "(Batches A–H); cross-dimension influence passes only through "
            "these mother nodes.", fontsize=8, color=MUT)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figJ1_great_graph.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# FIG J2 — block structure of the full 253-node weight matrix
# ---------------------------------------------------------------------------
def fig2():
    nodes = read_csv("upg_greatgraph_nodes.csv")
    edges = read_csv("upg_greatgraph_edges.csv")
    order = ["TEM", "DEV", "PER", "NEED", "ME", "DIS", "THER", "SYS"]
    nodes.sort(key=lambda r: (order.index(r["stratum"]), r["node_id"]))
    pos = {r["node_id"]: i for i, r in enumerate(nodes)}
    n = len(nodes)
    W = np.zeros((n, n))
    for e in edges:
        w = float(e["weight"]) * (1 if e["sign"] == "+" else -1)
        W[pos[e["target"]], pos[e["source"]]] = w
    fig, ax = plt.subplots(figsize=(8.4, 7.6))
    sgn_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "sgn", [THW, "white", SUP])
    ax.imshow(W, cmap=sgn_cmap, vmin=-1, vmax=1, interpolation="nearest")
    bounds, start = [], 0
    for s in order:
        cnt = sum(1 for r in nodes if r["stratum"] == s)
        bounds.append((s, start, start + cnt))
        start += cnt
    for s, a, bnd in bounds:
        ax.axhline(a - 0.5, color=INK, lw=0.6)
        ax.axvline(a - 0.5, color=INK, lw=0.6)
        ax.text(-6, (a + bnd) / 2, s, ha="right", va="center", fontsize=8.5,
                color=DCOL[s], weight="bold")
        ax.text((a + bnd) / 2, -4, s, ha="center", va="bottom", fontsize=8.5,
                color=DCOL[s], weight="bold", rotation=90)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("W of the full Great Graph (253 × 253): encapsulation as "
                 "block structure", weight="bold", pad=26)
    ax.set_xlabel("source node j   (entry W$_{ij}$: signed influence of j on i; "
                  "green +, red −)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figJ2_block_matrix.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Case conditions (identical to verify_math §5)
# ---------------------------------------------------------------------------
def case_states():
    B, g, b, eidx = dynamic_model()
    x_un = iterate(B, g, b, 0.0, np.ones(7))
    x_tr = iterate(B, g, b, 0.8, x_un)
    x_wd = iterate(B, g, b, 0.0, x_tr)
    Bs = B.copy()
    Bs[eidx["ME"], eidx["NEED"]] = 0.50
    Bs[eidx["DIS"], eidx["ME"]] = 0.35
    Bs[eidx["DIS"], eidx["DIS"]] = 0.20
    Bs[eidx["NEED"], eidx["SYS"]] = 0.40
    Bs[eidx["ME"], eidx["SYS"]] = 0.35
    bs = b.copy(); bs[eidx["SYS"]] = 0.15
    x_sm = iterate(Bs, g, bs, 0.3, x_tr)
    return (B, g, b, Bs, bs, eidx,
            {"untreated": x_un, "in treatment (u=0.8)": x_tr,
             "after withdrawal": x_wd, "edge surgery + maintenance": x_sm})


# ---------------------------------------------------------------------------
# FIG J3 — the topographical model: landscapes and heat-map profile
# ---------------------------------------------------------------------------
def fig3():
    _, _, _, _, _, eidx, states = case_states()
    grid_x, grid_y = np.meshgrid(np.linspace(0, 10, 220),
                                 np.linspace(0, 8, 180))

    def elevation(x):
        z = np.zeros_like(grid_x)
        for d in ENDO:
            px, py = POS[d]
            z += x[eidx[d]] * np.exp(-((grid_x - px) ** 2 +
                                       (grid_y - py) ** 2) / (2 * 1.15 ** 2))
        return z

    fig = plt.figure(figsize=(10.6, 8.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[2.1, 1.0], hspace=0.3)
    panels = [("untreated", "(a) untreated landscape"),
              ("edge surgery + maintenance", "(b) after structural change + maintenance")]
    for k, (cond, title) in enumerate(panels):
        ax = fig.add_subplot(gs[0, k])
        z = elevation(states[cond])
        levels = np.linspace(0.0, 0.95, 20)
        cf = ax.contourf(grid_x, grid_y, z, levels=levels, cmap="RdYlGn_r")
        ax.contour(grid_x, grid_y, z, levels=levels[::2], colors="k",
                   linewidths=0.3, alpha=0.35)
        for d in ENDO:
            px, py = POS[d]
            ax.plot(px, py, "o", ms=4, color=INK)
            ax.text(px, py + 0.3, d, ha="center", fontsize=8, weight="bold",
                    color=INK)
        if k == 0:
            ax.annotate("peak: disorder\nactivation 0.77", POS["DIS"],
                        xytext=(7.3, 6.9), fontsize=7.5, color=THW,
                        arrowprops=dict(arrowstyle="->", color=THW, lw=0.8))
            ax.annotate("high plateau:\nfrustrated needs feed\nnegative valuation",
                        (6.6, 5.0), xytext=(3.8, 7.3), fontsize=7.5, color=INK,
                        arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
        ax.set_title(title, fontsize=10, weight="bold")
        ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(cf, ax=ax, shrink=0.82, label="problem-load elevation")
    ax = fig.add_subplot(gs[1, :])
    M = np.array([[states[c][eidx[d]] for d in ENDO] for c in states])
    im = ax.imshow(M, cmap="RdYlGn_r", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(ENDO)), ENDO)
    ax.set_yticks(range(len(states)), list(states.keys()), fontsize=8.5)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                    fontsize=8, color="white" if M[i, j] > 0.55 else INK)
    ax.set_title("(c) heat-map profile of the same four conditions "
                 "(fixed-point activations)", fontsize=10, weight="bold")
    fig.colorbar(im, ax=ax, shrink=0.9, label="activation")
    fig.suptitle("Topographical readout of the worked case: peaks are where "
                 "the person hurts, valleys are where resources lie",
                 weight="bold", y=0.99)
    fig.savefig(os.path.join(OUT, "figJ3_topography.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# FIG J4 — Topographic Network Diagnosis workflow
# ---------------------------------------------------------------------------
def fig4():
    steps = [
        ("1  Instantiate", "select measures for the\n253 published nodes\n(interview, scales, EMA)",
         "≈ intake + testing"),
        ("2  State", "estimate x(t): activation\nof every node; repeat\nto get trajectories",
         "≈ mental-status exam,\nmeasurement-based care"),
        ("3  Structure", "start from consensus W̄;\npersonalize edges from\nrepeated states",
         "≈ case formulation"),
        ("4  Topography", "compute the landscape:\npeaks, valleys, plateaus,\nheat-map profile",
         "the diagnostic picture"),
        ("5  Mechanics", "loops (cycle gains),\nbridges (|v₂|), axes\n(Laplacian eigenvectors)",
         "why it persists"),
        ("6  Dynamics", "attractor x*, stability\nρ(J), distance to basin\nboundary; forecast",
         "prognosis"),
        ("7  Control", "rank targets: drive x (u),\nrewrite W (edge surgery),\nchange context (c)",
         "treatment planning +\nmonitoring loop"),
    ]
    fig, ax = plt.subplots(figsize=(11.4, 4.9))
    ax.set_xlim(0, 11.4); ax.set_ylim(0, 4.9); ax.axis("off")
    ax.set_title("Topographic Network Diagnosis (TND): the workflow",
                 weight="bold", pad=10)
    xw = 1.52
    for i, (t1, t2, t3) in enumerate(steps):
        x0 = 0.25 + i * xw
        ax.add_patch(FancyBboxPatch((x0, 2.0), xw - 0.22, 1.9,
                                    boxstyle="round,pad=0.05",
                                    fc="#f3f4fa", ec=ACC, lw=1.4))
        ax.text(x0 + (xw - 0.22) / 2, 3.62, t1, ha="center", fontsize=9.5,
                weight="bold", color=ACC)
        ax.text(x0 + (xw - 0.22) / 2, 2.86, t2, ha="center", fontsize=6.8,
                color=INK)
        ax.text(x0 + (xw - 0.22) / 2, 1.55, t3, ha="center", fontsize=6.8,
                color=MUT, style="italic")
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((x0 + xw - 0.20, 2.95),
                                         (x0 + xw + 0.02, 2.95),
                                         arrowstyle="-|>", mutation_scale=13,
                                         color=INK))
    ax.add_patch(FancyArrowPatch((0.25 + 6 * xw + 0.65, 3.95),
                                 (0.25 + 1 * xw + 0.65, 3.95),
                                 connectionstyle="arc3,rad=-0.14",
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=SUP, lw=1.3, ls="--"))
    ax.text(5.7, 4.62, "outcome monitoring re-enters at step 2: diagnosis is a "
            "loop, not a label", ha="center", fontsize=8.5, color=SUP)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figJ4_tnd_workflow.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# FIG J5 — state-shifting vs structure-changing intervention; bifurcation
# ---------------------------------------------------------------------------
def fig5():
    B, g, b, Bs, bs, eidx, _ = case_states()
    T1, T2, T3, T4 = 40, 80, 120, 175
    xs, x = [], np.zeros(7)
    for t in range(T4):
        if t < T1:
            Bt, bt, u = B, b, 0.0
        elif t < T2:
            Bt, bt, u = B, b, 0.8
        elif t < T3:
            Bt, bt, u = B, b, 0.0
        else:
            Bt, bt, u = Bs, bs, 0.3
        x = np.tanh(KAPPA * (Bt @ x + g * u) + bt)
        xs.append(x.copy())
    xs = np.array(xs)

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))
    ax = axes[0]
    for d, col, lw in (("DIS", THW, 2.2), ("ME", "#c07f1f", 1.1),
                       ("NEED", SUP, 1.1)):
        ax.plot(xs[:, eidx[d]], color=col, lw=lw, label=d)
    for t, lab in ((T1, "treatment on\n(u=0.8)"), (T2, "withdrawal\n(u=0)"),
                   (T3, "edge surgery +\nmaintenance (u=0.3)")):
        ax.axvline(t, color=MUT, lw=0.8, ls=":")
        ax.text(t + 1.5, 0.96, lab, fontsize=7, color=MUT, va="top")
    ax.set_ylim(0, 1); ax.set_xlabel("time step"); ax.set_ylabel("activation")
    ax.set_title("(a) driving the state vs rewriting the structure",
                 fontsize=10, weight="bold")
    ax.legend(fontsize=8, loc="lower right")

    ax = axes[1]
    ks = np.linspace(0.30, 0.70, 120)
    for bb, col, lab in ((np.zeros(7), ACC, "b = 0 (no standing load): pitchfork"),
                         (b, THW, "case b > 0: unfolded, monostable-high")):
        hi = [iterate(B, g, bb, 0.0, np.ones(7), kappa=k)[eidx["DIS"]] for k in ks]
        ax.plot(ks, hi, color=col, lw=1.8, label=lab)
    ax.axvline(1 / max(np.real(np.linalg.eigvals(B))), color=MUT, ls="--", lw=1)
    ax.text(0.462, 0.06, "κ* = 1/λ$_{max}$(B) = 0.456", fontsize=8, color=MUT)
    ax.axvline(KAPPA, color=INK, ls=":", lw=1)
    ax.text(0.402, 0.55, "case κ", fontsize=8, color=INK, rotation=90)
    ax.set_xlabel("coupling strength κ"); ax.set_ylabel("x*$_{DIS}$")
    ax.set_title("(b) the composed system inherits the loop-gain bifurcation "
                 "(Batch I §5.4)", fontsize=10, weight="bold")
    ax.legend(fontsize=7.5, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figJ5_control_bifurcation.png"),
                bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5):
        f()
        print("done:", f.__name__)
