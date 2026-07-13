"""
Universal Developmental Graph (UDevG) - Figure generation
Batch C: Developmental Psychology paper (UPG series)
Reproducible: python3 generate_figures.py

Inputs : ../data/udevg_nodes.csv, ../data/udevg_edges.csv
Outputs: ../figures/figC1_universal_developmental_graph.png
         ../figures/figC2_sensitive_period_gating.png
         ../figures/figC3_cascade_example.png
All weights are consensus priors with cited provenance (see CSVs); gating
curves are illustrative shapes of the time-varying weight principle, not
fitted functions.
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
nodes = pd.read_csv(os.path.join(DATA, "udevg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "udevg_edges.csv"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

SHORT = {
    "D": "Development\n(global)", "DOM_PHY": "Physical /\nMotor", "DOM_COG": "Cognitive",
    "DOM_LAN": "Language", "DOM_EMO": "Emotional", "DOM_SOC": "Social /\nRelational",
    "DOM_MOR": "Moral", "DOM_SLF": "Self /\nIdentity", "CTX_CARE": "Caregiving\ncontext",
}

# ---------------------------------------------------------------- Figure C1
def figC1_udevg():
    pos = {
        "D": (0, 4.4),
        "DOM_PHY": (-7.2, 1.6), "DOM_COG": (-4.6, 2.4), "DOM_LAN": (-2.0, 1.4),
        "DOM_EMO": (0.6, 2.4), "DOM_SOC": (3.2, 1.4), "DOM_MOR": (5.8, 2.4),
        "DOM_SLF": (8.2, 1.4), "CTX_CARE": (0.6, -1.6),
    }
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis("off")
    stylemap = {"hierarchical": ("#555555", "-"), "cascade": ("#c0392b", "--"),
                "transactional": ("#2980b9", "-.")}
    for _, r in edges.iterrows():
        if r.source not in pos or r.target not in pos:
            continue
        if r.source == r.target:
            x, y = pos[r.source]
            ax.add_patch(mpatches.FancyArrowPatch((x - 0.35, y + 0.55), (x + 0.35, y + 0.58),
                         connectionstyle="arc3,rad=1.6", arrowstyle="-|>",
                         mutation_scale=10, color="#8e44ad", lw=1.4, zorder=7))
            continue
        col, ls = stylemap.get(r.type, ("#c0392b", "--"))
        gated = isinstance(r.gate, str) and r.gate not in ("none",)
        rad = 0.0 if r.type == "hierarchical" else 0.22
        ax.add_patch(mpatches.FancyArrowPatch(
            pos[r.source], pos[r.target], connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>" if r.type != "hierarchical" else "-",
            mutation_scale=11, lw=0.6 + 2.8 * abs(r.weight), alpha=0.7,
            shrinkA=26, shrinkB=26, color=col, ls=ls, zorder=2))
        if gated and r.type != "hierarchical":
            mx = (pos[r.source][0] + pos[r.target][0]) / 2
            my = (pos[r.source][1] + pos[r.target][1]) / 2 + (0.45 if rad else 0.2)
            ax.plot(mx, my, marker="D", ms=5.5, color="#f1c40f",
                    mec="#7f6000", mew=0.8, zorder=8)
    for n, (x, y) in pos.items():
        lvl = int(nodes.loc[nodes.node_id == n, "level"].iloc[0])
        fc = {0: "#1a1a2e", 1: "#2e86ab"}.get(lvl, "#2e86ab")
        if n == "CTX_CARE":
            fc = "#7f8c8d"
        ax.add_patch(mpatches.Circle((x, y), 0.86, fc=fc, ec="white", lw=2, zorder=5))
        ax.annotate(SHORT[n], (x, y), ha="center", va="center", color="white",
                    fontsize=7.4, weight="bold", zorder=6)
    handles = [
        Line2D([0], [0], color="#555555", lw=2, label="Hierarchical edge"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Cascade edge (directed)"),
        Line2D([0], [0], color="#2980b9", lw=2, ls="-.", label="Transactional edge (reciprocal)"),
        Line2D([0], [0], color="#8e44ad", lw=1.5, label="Self-loop (Axiom 4)"),
        Line2D([0], [0], marker="D", color="w", mfc="#f1c40f", mec="#7f6000",
               ms=7, label="Time-gated weight w(t) (sensitive period)"),
        mpatches.Patch(color="#7f8c8d", label="Interface node (to Systems stratum)"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=7.6,
              frameon=False, bbox_to_anchor=(0.5, -0.05))
    ax.set_xlim(-8.6, 9.6); ax.set_ylim(-3.2, 5.6)
    ax.set_title("Universal Developmental Graph: domains, cascades, transactions, and time-gated weights\n"
                 "(edge thickness " + r"$\propto$" + " provisional consensus weight; diamonds mark edges whose weight varies with developmental time)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figC1_universal_developmental_graph.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure C2
def figC2_gating():
    t = np.linspace(0, 25, 500)  # years
    def bump(t, mu, sig, floor=0.05):
        return floor + (1 - floor) * np.exp(-((t - mu) ** 2) / (2 * sig ** 2))
    curves = {
        "Caregiving → Attachment (infancy-peak)": bump(t, 1.0, 1.4),
        "Input → Language (sensitive period)": bump(t, 3.5, 2.4),
        "Motor → Cognitive exploration (infancy-peak)": bump(t, 1.5, 1.8),
        "Relational feedback → Identity (adolescence-peak)": bump(t, 16.0, 3.2),
    }
    colors = ["#c0392b", "#2980b9", "#27ae60", "#8e44ad"]
    fig, ax = plt.subplots(figsize=(9, 5))
    for (lab, y), c in zip(curves.items(), colors):
        ax.plot(t, y, lw=2.2, color=c, label=lab)
    ax.set_xlabel("Developmental time (years)")
    ax.set_ylabel("Relative edge gain  g(t)")
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Sensitive-period gating: edge weights as functions of developmental time\n"
                 r"$w_{ij}(t) = g_{ij}(t)\,\bar{w}_{ij}$" +
                 "  (curve shapes are illustrative of the principle, not fitted functions)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figC2_sensitive_period_gating.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure C3
def figC3_cascade():
    """Developmental cascade example across strata epochs (Masten-style)."""
    lay = {
        "A": (0.6, 4.2, "Early emotion-\nregulation\ndifficulty"),
        "B": (3.2, 5.2, "Parent-child\ncoercive cycles"),
        "C": (5.8, 4.2, "School-entry\nconduct problems"),
        "D": (5.8, 1.8, "Academic\nfailure"),
        "E": (8.4, 3.2, "Peer\nrejection"),
        "F": (11.0, 4.0, "Deviant peer\naffiliation"),
        "G": (11.0, 1.6, "Adolescent\ninternalizing"),
    }
    arrows = [("A","B",.6), ("B","C",.65), ("C","D",.55), ("C","E",.6),
              ("D","G",.5), ("E","F",.55), ("E","G",.5), ("F","G",.35)]
    fig, ax = plt.subplots(figsize=(11.5, 6))
    ax.axis("off")
    for s, tg, w in arrows:
        ax.add_patch(mpatches.FancyArrowPatch(
            lay[s][:2], lay[tg][:2], connectionstyle="arc3,rad=0.12",
            arrowstyle="-|>", mutation_scale=13, lw=0.8 + 3 * w, alpha=0.75,
            shrinkA=30, shrinkB=30, color="#c0392b"))
    for k, (x, y, lab) in lay.items():
        ax.add_patch(mpatches.FancyBboxPatch((x - 1.05, y - 0.62), 2.1, 1.24,
                     boxstyle="round,pad=0.08", fc="#2e86ab", ec="white", lw=1.5, zorder=5))
        ax.annotate(lab, (x, y), ha="center", va="center", color="white",
                    fontsize=7.6, weight="bold", zorder=6)
    for x, lab in [(0.6, "Infancy /\ntoddlerhood"), (4.5, "Early-middle\nchildhood"),
                   (8.4, "Middle childhood /\nearly adolescence"), (11.0, "Adolescence")]:
        ax.annotate(lab, (x, 0.15), ha="center", fontsize=8, style="italic", color="#555")
    ax.axhline(0.75, color="#bbb", lw=0.8, ls=":")
    ax.set_xlim(-1.2, 12.6); ax.set_ylim(-0.4, 6.2)
    ax.set_title("A developmental cascade rendered as a dated path in the UDevG\n"
                 "(illustrative composite of documented externalizing-to-internalizing cascades; "
                 "each edge is a time-stamped, testable prediction)", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figC3_cascade_example.png"), dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    figC1_udevg()
    figC2_gating()
    figC3_cascade()
    print("Figures written to", os.path.abspath(FIGS))
