"""
Universal Therapy Graph (UTG) - Figure generation
Batch B: Psychotherapy & Psychiatry paper
Reproducible: python3 generate_figures.py

Inputs : ../data/utg_nodes.csv, ../data/utg_edges.csv
Outputs: ../figures/figB1_universal_therapy_graph.png
         ../figures/figB2_formulation_subgraph.png
         ../figures/figB3_evidence_process_weights.png
Weights are evidence/process ratings synthesized from the cited literature
(see CSV provenance columns); they are consensus priors, not measurements.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIGS = os.path.join(HERE, "..", "figures")
os.makedirs(FIGS, exist_ok=True)

nodes = pd.read_csv(os.path.join(DATA, "utg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "utg_edges.csv"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

SHORT = {
    "N01": "Entry /\nTriage", "N02": "Safety +\nEthics", "N03": "Alliance",
    "N04": "Assessment", "N05": "Case\nFormulation", "N06": "Goal\nAgreement",
    "N07": "Change\nWork", "N08": "Practice +\nGeneraliz.", "N09": "Outcome\nMonitoring",
    "N10": "Review +\nAdaptation", "N11": "Consolidation /\nTermination",
}

# ---------------------------------------------------------------- Figure B1
def figB1_utg():
    """Circular workflow layout with feedback and cross-cutting edges."""
    main = [f"N{i:02d}" for i in range(1, 12)]
    n = len(main)
    # ellipse layout, clockwise from top-left
    angles = np.linspace(110, 110 + 360, n, endpoint=False) * np.pi / 180
    pos = {m: (5.6 * np.cos(-a), 3.6 * np.sin(-a)) for m, a in zip(main, angles)}

    fig, ax = plt.subplots(figsize=(12.5, 8.5))
    ax.axis("off")

    styles = {
        "sequential": dict(color="#2c3e50", ls="-"),
        "feedback": dict(color="#c0392b", ls="--"),
        "cross-cutting": dict(color="#e67e22", ls=":"),
    }
    for _, r in edges.iterrows():
        if r.source not in pos or r.target not in pos:
            continue
        if r.source == r.target:  # self-loop
            x, y = pos[r.source]
            out = np.array([x, y]) * 1.16
            ax.add_patch(mpatches.FancyArrowPatch(
                (x - 0.3, out[1] + (0.42 if y >= 0 else -0.42)),
                (x + 0.3, out[1] + (0.45 if y >= 0 else -0.45)),
                connectionstyle="arc3,rad=1.5", arrowstyle="-|>",
                mutation_scale=10, color="#8e44ad", lw=1.4, zorder=7))
            continue
        st = styles.get(r.type, dict(color="#e67e22", ls=":"))
        col = "#16a085" if r.sign == "-" else st["color"]
        rad = 0.12 if r.type == "sequential" else 0.35
        ax.add_patch(mpatches.FancyArrowPatch(
            pos[r.source], pos[r.target], connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>", mutation_scale=11,
            lw=0.6 + 2.6 * abs(r.weight), alpha=0.75, shrinkA=24, shrinkB=24,
            color=col, ls=st["ls"], zorder=2))

    for m in main:
        ew = int(nodes.loc[nodes.node_id == m, "evidence_weight"].iloc[0])
        pw = int(nodes.loc[nodes.node_id == m, "process_weight"].iloc[0])
        core = ew == 5 and pw == 5
        ax.add_patch(mpatches.Circle(pos[m], 0.78, fc="#16537e" if core else "#5b8db8",
                                     ec="white", lw=2, zorder=5))
        ax.annotate(SHORT[m] + f"\nE{ew}/P{pw}", pos[m], ha="center", va="center",
                    color="white", fontsize=7.0, weight="bold", zorder=6)

    handles = [
        Line2D([0], [0], color="#2c3e50", lw=2, label="Sequential workflow edge"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Feedback edge (recursion)"),
        Line2D([0], [0], color="#e67e22", lw=2, ls=":", label="Cross-cutting edge"),
        Line2D([0], [0], color="#16a085", lw=2, label="Inhibitory edge (Axiom 5)"),
        Line2D([0], [0], color="#8e44ad", lw=1.5, label="Self-loop (Axiom 4)"),
        mpatches.Patch(color="#16537e", label="Core node (Evidence 5 / Process 5)"),
        mpatches.Patch(color="#5b8db8", label="Standard node"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=4, fontsize=7.4,
              frameon=False, bbox_to_anchor=(0.5, -0.08))
    ax.set_xlim(-7.6, 7.6); ax.set_ylim(-5.6, 5.4)
    ax.set_title("Universal Therapy Graph: the recursive clinical control loop\n"
                 "(E = evidence weight, P = process weight, 1–5; edge thickness "
                 r"$\propto$" + " weight; all weights are consensus priors)", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figB1_universal_therapy_graph.png"), dpi=300,
                bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure B2
def figB2_formulation_subgraph():
    lay = {
        "S0501": (5.0, 5.2, "Presenting\nProblem"),
        "S0502": (8.2, 4.0, "Triggers"),
        "S0503": (8.6, 1.8, "Emotion /\nBody State"),
        "S0504": (5.0, 0.7, "Meaning /\nBelief / Schema"),
        "S0505": (1.4, 1.8, "Action /\nAvoidance"),
        "S0506": (1.8, 4.0, "Consequences"),
        "S0507": (10.6, 5.4, "Relationships\n+ Context"),
        "S0508": (-1.0, 5.4, "Protective\nFactors"),
    }
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.axis("off")
    for _, r in edges.iterrows():
        if r.source in lay and r.target in lay and r.source.startswith("S05"):
            (x1, y1, _), (x2, y2, _) = lay[r.source], lay[r.target]
            col = "#16a085" if r.sign == "-" else ("#c0392b" if "feedback" in r.type else "#2c3e50")
            ls = "--" if "feedback" in r.type else ("-." if r.sign == "-" else "-")
            ax.add_patch(mpatches.FancyArrowPatch(
                (x1, y1), (x2, y2), connectionstyle="arc3,rad=0.15",
                arrowstyle="-|>", mutation_scale=12, lw=0.6 + 2.6 * abs(r.weight),
                alpha=0.8, shrinkA=26, shrinkB=26, color=col, ls=ls))
    for k, (x, y, lab) in lay.items():
        aux = k in ("S0507", "S0508")
        ax.add_patch(mpatches.Circle((x, y), 0.85, fc="#7fb3d5" if aux else "#16537e",
                                     ec="white", lw=2, zorder=5))
        ax.annotate(lab, (x, y), ha="center", va="center", color="white",
                    fontsize=7.2, weight="bold", zorder=6)
    ax.annotate("maintaining loop", (4.9, 3.0), ha="center", fontsize=9,
                style="italic", color="#c0392b")
    handles = [
        Line2D([0], [0], color="#2c3e50", lw=2, label="Causal-functional edge"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Loop-closing feedback edge"),
        Line2D([0], [0], color="#16a085", lw=2, ls="-.", label="Inhibitory (protective) edge"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=8, frameon=False)
    ax.set_xlim(-2.6, 12.2); ax.set_ylim(-0.6, 6.6)
    ax.set_title("Case Formulation subgraph (zoom-in): the maintaining loop with contextual inputs and protective inhibition\n"
                 "Subgraph communicates with the workflow level only through its mother node (encapsulation principle)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figB2_formulation_subgraph.png"), dpi=300,
                bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure B3
def figB3_weights():
    main = nodes[nodes.level == 0].copy()
    y = np.arange(len(main))[::-1]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.barh(y + 0.18, main.evidence_weight, height=0.34, color="#16537e", label="Evidence weight")
    ax.barh(y - 0.18, main.process_weight, height=0.34, color="#e67e22", label="Process weight")
    ax.set_yticks(y, [l.replace(" / ", " /\n") for l in main.label])
    ax.set_xlim(0, 5.4); ax.set_xlabel("Weight (1–5)")
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    ax.set_title("Evidence and process weights of the eleven universal nodes\n"
                 "(5 = meta-analytic support / indispensable architecture; see Table 2 for sources)",
                 fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figB3_evidence_process_weights.png"), dpi=300,
                bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    figB1_utg()
    figB2_formulation_subgraph()
    figB3_weights()
    print("Figures written to", os.path.abspath(FIGS))
