"""
Universal Disorder Graph (UDG) - Figure generation
Batch A: Psychopathology paper
Reproducible: python3 generate_figures.py  (requires networkx, matplotlib, pandas, numpy)

Inputs : ../data/udg_nodes.csv, ../data/udg_edges.csv
Outputs: ../figures/figA1_three_systems.png
         ../figures/figA2_universal_disorder_graph.png
         ../figures/figA3_internalizing_subgraph.png
         ../figures/figA4_adjacency_heatmap.png
All weights are provisional consensus values synthesized from published
factor-analytic estimates (see edges.csv 'primary_source' column); they are
starting priors W(0) intended for empirical re-estimation, not fixed constants.
"""
import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIGS = os.path.join(HERE, "..", "figures")
os.makedirs(FIGS, exist_ok=True)

nodes = pd.read_csv(os.path.join(DATA, "udg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "udg_edges.csv"))

LEVEL_COLORS = {0: "#1a1a2e", 1: "#16537e", 2: "#2e86ab", 3: "#7fb3d5"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

SHORT = {
    "P": "p\n(general)", "SS_EMO": "Emotional\ndysfunction", "SS_PSY": "Psychosis",
    "SS_EXT": "Externalizing", "SP_INT": "Internalizing", "SP_SOM": "Somatoform",
    "SP_THO": "Thought\ndisorder", "SP_DET": "Detachment", "SP_DIS": "Disinhibited\next.",
    "SP_ANT": "Antagonistic\next.", "SP_NDV": "Neuro-\ndevelopmental",
    "SF_DIST": "Distress", "SF_FEAR": "Fear", "SF_EAT": "Eating", "SF_SEX": "Sexual\nproblems",
    "SF_MAN": "Mania", "SF_SUB": "Substance", "SF_ASB": "Antisocial",
}

# ---------------------------------------------------------------- Figure 1
def figA1_three_systems():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    # DSM: discrete boxes
    ax = axes[0]
    ax.set_title("A. DSM-5-TR: categorical-polythetic", fontsize=10, weight="bold")
    labels = ["MDD", "GAD", "PTSD", "AUD", "BPD", "SSD"]
    pos = [(2, 7.5), (6.5, 7.5), (2, 5), (6.5, 5), (2, 2.5), (6.5, 2.5)]
    for (x, y), lab in zip(pos, labels):
        ax.add_patch(mpatches.FancyBboxPatch((x - 1.2, y - 0.7), 2.9, 1.4,
                     boxstyle="round,pad=0.08", fc="#e8e8e8", ec="#555"))
        ax.text(x + 0.25, y, lab, ha="center", va="center", fontsize=9)
    ax.text(5, 0.6, "Discrete disorders; present/absent;\nno formal between-category structure",
            ha="center", fontsize=8, style="italic")

    # ICD: chapter tree
    ax = axes[1]
    ax.set_title("B. ICD-10/11: clinical-descriptive tree", fontsize=10, weight="bold")
    ax.add_patch(mpatches.FancyBboxPatch((3.4, 8.2), 3.2, 1.2, boxstyle="round,pad=0.08",
                 fc="#dfeeea", ec="#555"))
    ax.text(5, 8.8, "Chapter V / 06", ha="center", va="center", fontsize=9)
    blocks = ["F2x\nPsychotic", "F3x\nMood", "F4x\nNeurotic/\nstress", "F6x\nPersonality"]
    xs = [1.4, 3.8, 6.2, 8.6]
    for x, b in zip(xs, blocks):
        ax.plot([5, x], [8.2, 6.3], color="#777", lw=1)
        ax.add_patch(mpatches.FancyBboxPatch((x - 1.05, 4.8), 2.1, 1.5,
                     boxstyle="round,pad=0.06", fc="#f4f4f4", ec="#666"))
        ax.text(x, 5.55, b, ha="center", va="center", fontsize=7.5)
    ax.text(5, 0.6, "Prototype guidance; flexible clinical\ndescriptions; global public-health mandate",
            ha="center", fontsize=8, style="italic")

    # HiTOP: dimensional hierarchy
    ax = axes[2]
    ax.set_title("C. HiTOP: hierarchical-dimensional", fontsize=10, weight="bold")
    ax.add_patch(mpatches.Circle((5, 9), 0.75, fc="#1a1a2e"))
    ax.text(5, 9, "p", ha="center", va="center", color="w", fontsize=10, weight="bold")
    sxs = [2.2, 5, 7.8]
    for x, lab in zip(sxs, ["Emot.", "Psych.", "Ext."]):
        ax.plot([5, x], [8.4, 6.9], color="#888", lw=1.2)
        ax.add_patch(mpatches.Circle((x, 6.3), 0.68, fc="#16537e"))
        ax.text(x, 6.3, lab, ha="center", va="center", color="w", fontsize=7.5)
    spectra_x = [1.1, 3.3, 4.4, 5.8, 7.0, 8.9]
    for i, x in enumerate(spectra_x):
        parent = sxs[0] if i < 2 else (sxs[1] if i < 4 else sxs[2])
        ax.plot([parent, x], [5.7, 4.2], color="#999", lw=1)
        ax.add_patch(mpatches.Circle((x, 3.7), 0.55, fc="#2e86ab"))
    ax.text(5, 2.2, "spectra " + r"$\rightarrow$" + " subfactors " + r"$\rightarrow$" +
            " syndromes " + r"$\rightarrow$" + " symptoms", ha="center", fontsize=8)
    ax.text(5, 0.6, "Continuous dimensions; comorbidity\nmodeled as shared higher-order liability",
            ha="center", fontsize=8, style="italic")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figA1_three_systems.png"), dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure 2
def figA2_udg():
    G = nx.DiGraph()
    for _, r in nodes.iterrows():
        G.add_node(r.node_id, level=r.level)
    for _, r in edges.iterrows():
        G.add_edge(r.source, r.target, weight=r.weight, etype=r.type)

    # manual layered layout
    pos = {
        "P": (0, 4),
        "SS_EMO": (-5.5, 2.6), "SS_PSY": (0, 2.6), "SS_EXT": (5.5, 2.6),
        "SP_INT": (-7, 1), "SP_SOM": (-4, 1), "SP_THO": (-1.3, 1), "SP_DET": (1.3, 1),
        "SP_DIS": (4, 1), "SP_ANT": (7, 1), "SP_NDV": (9.3, 2.0),
        "SF_DIST": (-9, -1), "SF_FEAR": (-7.4, -1), "SF_EAT": (-5.8, -1), "SF_SEX": (-4.2, -1),
        "SF_MAN": (-1.3, -1), "SF_SUB": (3.3, -1), "SF_ASB": (5.2, -1),
    }
    fig, ax = plt.subplots(figsize=(13.5, 8))
    ax.axis("off")

    for u, v, d in G.edges(data=True):
        if u == v:  # self-loop
            x, y = pos[u]
            ax.add_patch(mpatches.FancyArrowPatch((x - 0.35, y + 0.52), (x + 0.35, y + 0.55),
                         connectionstyle="arc3,rad=1.6", arrowstyle="-|>",
                         mutation_scale=10, color="#c0392b", lw=1.4, alpha=0.95, zorder=7))
            continue
        style = {"hierarchical": dict(color="#555", ls="-"),
                 "cross-spectral": dict(color="#c0392b", ls="--"),
                 "cross-subfactor": dict(color="#e67e22", ls=":")}[d["etype"]] \
                 if d["etype"] in ("hierarchical", "cross-spectral", "cross-subfactor") \
                 else dict(color="#c0392b", ls="--")
        rad = 0.0 if d["etype"] == "hierarchical" else 0.25
        ax.add_patch(mpatches.FancyArrowPatch(pos[u], pos[v],
                     connectionstyle=f"arc3,rad={rad}", arrowstyle="-",
                     lw=0.6 + 3.2 * d["weight"], alpha=0.55, shrinkA=16, shrinkB=16, **style))

    for n in G.nodes():
        lvl = int(nodes.loc[nodes.node_id == n, "level"].iloc[0])
        r = {0: 0.68, 1: 0.66, 2: 0.62, 3: 0.46}[lvl]
        ax.add_patch(mpatches.Circle(pos[n], r, fc=LEVEL_COLORS[lvl], ec="white", lw=1.5, zorder=5))
        ax.annotate(SHORT[n], pos[n], ha="center", va="center", color="white",
                    fontsize=6.4 if lvl == 3 else 6.8, zorder=6, weight="bold")

    handles = [
        Line2D([0], [0], color="#555", lw=2, label="Hierarchical edge (loading)"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Cross-spectral edge (residual covariance)"),
        Line2D([0], [0], color="#e67e22", lw=2, ls=":", label="Cross-subfactor edge"),
        Line2D([0], [0], color="#c0392b", lw=1.2, label="Self-loop (autoregressive; Axiom 4)"),
        mpatches.Patch(color=LEVEL_COLORS[0], label="Level 0: general factor"),
        mpatches.Patch(color=LEVEL_COLORS[1], label="Level 1: superspectra"),
        mpatches.Patch(color=LEVEL_COLORS[2], label="Level 2: spectra"),
        mpatches.Patch(color=LEVEL_COLORS[3], label="Level 3: subfactors"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=4, fontsize=7.5, frameon=False,
              bbox_to_anchor=(0.5, -0.06))
    ax.set_xlim(-10.3, 10.6); ax.set_ylim(-2.3, 5.0)
    ax.set_title("Universal Disorder Graph: weighted hierarchical structure with cross-cutting edges\n"
                 "(edge thickness " + r"$\propto$" + " provisional consensus weight; all weights are priors for empirical re-estimation)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figA2_universal_disorder_graph.png"), dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure 3
def figA3_internalizing_subgraph():
    syndromes = {
        "SF_DIST": ["MDD", "GAD", "Dysthymia", "PTSD"],
        "SF_FEAR": ["Panic", "Agoraphobia", "Social\nanxiety", "Specific\nphobia", "OCD"],
        "SF_EAT": ["Anorexia", "Bulimia", "Binge\neating"],
    }
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.axis("off")
    ax.add_patch(mpatches.Circle((5, 5.6), 0.65, fc="#2e86ab", zorder=5))
    ax.text(5, 5.6, "Internalizing", ha="center", va="center", color="w", fontsize=8,
            weight="bold", zorder=6)
    sf_pos = {"SF_DIST": (1.8, 3.8), "SF_FEAR": (5, 3.8), "SF_EAT": (8.2, 3.8)}
    row_y = {"SF_DIST": 2.35, "SF_FEAR": 1.15, "SF_EAT": 2.35}  # staggered rows
    for sf, (x, y) in sf_pos.items():
        ax.plot([5, x], [5.05, y + 0.45], color="#555", lw=2)
        ax.add_patch(mpatches.Circle((x, y), 0.5, fc="#7fb3d5", zorder=5))
        ax.text(x, y, SHORT[sf], ha="center", va="center", fontsize=7.5, zorder=6, weight="bold")
        n = len(syndromes[sf])
        ry = row_y[sf]
        for i, syn in enumerate(syndromes[sf]):
            sx = x + (i - (n - 1) / 2) * 1.3
            ax.plot([x, sx], [y - 0.45, ry + 0.4], color="#999", lw=1)
            ax.add_patch(mpatches.FancyBboxPatch((sx - 0.55, ry - 0.38), 1.1, 0.75,
                         boxstyle="round,pad=0.05", fc="#eef4f8", ec="#666", zorder=5))
            ax.text(sx, ry, syn, ha="center", va="center", fontsize=6.4, zorder=6)
    # cross-subfactor edge (distress-fear)
    ax.add_patch(mpatches.FancyArrowPatch(sf_pos["SF_DIST"], sf_pos["SF_FEAR"],
                 connectionstyle="arc3,rad=0.3", arrowstyle="-", color="#c0392b",
                 ls="--", lw=2.2, alpha=0.7, shrinkA=16, shrinkB=16))
    ax.text(3.4, 3.15, "w " + r"$\approx$" + " .70", color="#c0392b", fontsize=7.5)
    # bridge symptom examples
    ax.text(5, 0.55, "Example bridge symptoms: insomnia (distress " + r"$\leftrightarrow$" +
            " fear), appetite change (distress " + r"$\leftrightarrow$" + " eating), "
            "panic-type arousal (fear " + r"$\leftrightarrow$" + " somatoform)",
            ha="center", fontsize=8, style="italic")
    ax.set_xlim(-0.5, 10.5); ax.set_ylim(0, 6.6)
    ax.set_title("Internalizing spectrum subgraph (zoom-in): subfactors, representative syndromes, and bridge relations\n"
                 "Subgraphs communicate with other spectra only through their mother node", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figA3_internalizing_subgraph.png"), dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure 4
def figA4_heatmap():
    spectra = ["SP_INT", "SP_SOM", "SP_THO", "SP_DET", "SP_DIS", "SP_ANT", "SP_NDV"]
    labels = ["INT", "SOM", "THO", "DET", "DIS", "ANT", "NDV"]
    n = len(spectra)
    W = np.eye(n)
    for _, r in edges.iterrows():
        if r.source in spectra and r.target in spectra and r.source != r.target:
            i, j = spectra.index(r.source), spectra.index(r.target)
            W[i, j] = W[j, i] = r.weight
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    im = ax.imshow(W, cmap="YlOrRd", vmin=0, vmax=1)
    ax.set_xticks(range(n), labels); ax.set_yticks(range(n), labels)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{W[i,j]:.2f}", ha="center", va="center",
                    color="white" if W[i, j] > 0.55 else "#333", fontsize=8)
    ax.set_title("Provisional spectrum-level adjacency matrix W(0)\n(consensus priors for empirical re-estimation)", fontsize=10)
    fig.colorbar(im, shrink=0.8, label="edge weight")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figA4_adjacency_heatmap.png"), dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    figA1_three_systems()
    figA2_udg()
    figA3_internalizing_subgraph()
    figA4_heatmap()
    print("All figures generated in", os.path.abspath(FIGS))
