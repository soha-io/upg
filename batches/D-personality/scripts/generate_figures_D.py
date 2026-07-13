"""
Universal Personality Graph (UPerG) - Figure generation
Batch D: Personality Psychology paper (UPG series)
Reproducible: python3 generate_figures.py

Inputs : ../data/uperg_nodes.csv, ../data/uperg_edges.csv
Outputs: ../figures/figD1_universal_personality_graph.png
         ../figures/figD2_trait_hierarchy_30_facets.png
         ../figures/figD3_process_loop.png
All weights are consensus priors with cited provenance (see CSVs).
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
nodes = pd.read_csv(os.path.join(DATA, "uperg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "uperg_edges.csv"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

SHORT = {
    "P": "Personality\n(global)", "LAYER_TRT": "Dispositional\ntraits",
    "LAYER_ADP": "Characteristic\nadaptations", "LAYER_NAR": "Narrative\nidentity",
    "ST_STATE": "Momentary\nstates", "CTX_SIT": "Situations /\ncontexts",
    "OUT_LIFE": "Consequential\noutcomes", "TEMP_IN": "Temperament\nsubstrate",
    "MECH_SEL": "Selection", "MECH_EVO": "Evocation", "MECH_REA": "Reactive\nprocesses",
    "MECH_INS": "Instrumental\nmediation", "MECH_CYB": "Cybernetic\ngoal loop",
}

# ---------------------------------------------------------------- Figure D1
def figD1_uperg():
    pos = {
        "P": (0, 5.0),
        "LAYER_TRT": (-4.6, 2.9), "LAYER_ADP": (0.2, 2.9), "LAYER_NAR": (4.6, 2.9),
        "TEMP_IN": (-8.2, 2.9),
        "MECH_SEL": (-6.4, 0.6), "MECH_EVO": (-4.2, 0.6), "MECH_REA": (-2.0, 0.6),
        "MECH_INS": (2.2, 0.6), "MECH_CYB": (4.4, 0.6),
        "ST_STATE": (-2.2, -1.7), "CTX_SIT": (-6.0, -1.7), "OUT_LIFE": (2.4, -1.7),
    }
    fig, ax = plt.subplots(figsize=(13.5, 8.5))
    ax.axis("off")
    stylemap = {"hierarchical": ("#555555", "-"), "cascade": ("#c0392b", "--"),
                "transactional": ("#2980b9", "-."), "feedback": ("#27ae60", ":")}
    # signed domain->outcome edges are drawn from the trait layer at this zoom level
    ALIAS = {"TRT_N": "LAYER_TRT", "TRT_C": "LAYER_TRT"}
    for _, r in edges.iterrows():
        src = ALIAS.get(r.source, r.source) if r.target == "OUT_LIFE" else r.source
        if src not in pos or r.target not in pos:
            continue
        if src == r.target:
            x, y = pos[src]
            ax.add_patch(mpatches.FancyArrowPatch((x - 0.35, y + 0.55), (x + 0.35, y + 0.58),
                         connectionstyle="arc3,rad=1.6", arrowstyle="-|>",
                         mutation_scale=10, color="#8e44ad", lw=1.4, zorder=7))
            continue
        col, ls = stylemap.get(r.type, ("#c0392b", "--"))
        if r.sign == "-":
            col = "#16a085"
        gated = isinstance(r.gate, str) and r.gate not in ("none",)
        rad = 0.0 if r.type == "hierarchical" else (0.30 if r.sign == "-" else 0.18)
        r = r.copy(); r.source = src
        ax.add_patch(mpatches.FancyArrowPatch(
            pos[r.source], pos[r.target], connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>" if r.type != "hierarchical" else "-",
            mutation_scale=11, lw=0.6 + 2.8 * abs(r.weight), alpha=0.7,
            shrinkA=26, shrinkB=26, color=col, ls=ls, zorder=2))
        if gated and r.type != "hierarchical":
            mx = (pos[r.source][0] + pos[r.target][0]) / 2
            my = (pos[r.source][1] + pos[r.target][1]) / 2 + (0.4 if rad else 0.2)
            ax.plot(mx, my, marker="D", ms=5.5, color="#f1c40f",
                    mec="#7f6000", mew=0.8, zorder=8)
    for n, (x, y) in pos.items():
        lvl = int(nodes.loc[nodes.node_id == n, "level"].iloc[0])
        fc = {0: "#1a1a2e"}.get(lvl, "#2e86ab")
        if n in ("TEMP_IN", "CTX_SIT"):
            fc = "#7f8c8d"
        if n.startswith("MECH"):
            fc = "#a0522d"
        ax.add_patch(mpatches.Circle((x, y), 0.88, fc=fc, ec="white", lw=2, zorder=5))
        ax.annotate(SHORT[n], (x, y), ha="center", va="center", color="white",
                    fontsize=7.4, weight="bold", zorder=6)
    handles = [
        Line2D([0], [0], color="#555555", lw=2, label="Hierarchical edge"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Cascade edge (directed)"),
        Line2D([0], [0], color="#2980b9", lw=2, ls="-.", label="Transactional edge (reciprocal)"),
        Line2D([0], [0], color="#27ae60", lw=2, ls=":", label="Feedback edge"),
        Line2D([0], [0], color="#16a085", lw=2, ls="--", label="Negative (signed) edge (Axiom 5)"),
        Line2D([0], [0], color="#8e44ad", lw=1.5, label="Self-loop (Axiom 4)"),
        Line2D([0], [0], marker="D", color="w", mfc="#f1c40f", mec="#7f6000",
               ms=7, label="Time-gated weight w(t)"),
        mpatches.Patch(color="#7f8c8d", label="Interface node (Temperament / Systems strata)"),
        mpatches.Patch(color="#a0522d", label="Process node"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=7.6,
              frameon=False, bbox_to_anchor=(0.5, -0.06))
    ax.set_xlim(-9.6, 9.6); ax.set_ylim(-3.4, 6.2)
    ax.set_title("Universal Personality Graph: three layers, five processes, and their traffic\n"
                 "(edge thickness " + r"$\propto$" + " provisional consensus weight; diamonds mark time-gated edges)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figD1_universal_personality_graph.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure D2
def figD2_hierarchy():
    """Metatraits -> Big Five -> 30 NEO facets (encapsulated trait subgraph)."""
    domains = ["TRT_N", "TRT_E", "TRT_O", "TRT_A", "TRT_C"]
    dom_lab = {"TRT_N": "Neuroticism", "TRT_E": "Extraversion", "TRT_O": "Openness",
               "TRT_A": "Agreeableness", "TRT_C": "Conscientiousness"}
    dom_col = {"TRT_N": "#c0392b", "TRT_E": "#e67e22", "TRT_O": "#8e44ad",
               "TRT_A": "#27ae60", "TRT_C": "#2980b9"}
    facets = nodes[nodes.level == 3]
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis("off")
    # metatraits
    meta = {"Stability\n(shared variance of N–, A, C)": (4.0, 7.2),
            "Plasticity\n(shared variance of E, O)": (10.0, 7.2)}
    meta_map = {"TRT_N": 0, "TRT_A": 0, "TRT_C": 0, "TRT_E": 1, "TRT_O": 1}
    mpos = list(meta.values())
    xs = np.linspace(1.2, 12.8, 5)
    dpos = {d: (x, 4.8) for d, x in zip(domains, xs)}
    for d in domains:
        mx, my = mpos[meta_map[d]]
        ls = "--" if d == "TRT_N" else "-"
        ax.plot([mx, dpos[d][0]], [my - 0.35, dpos[d][1] + 0.42],
                color="#777", lw=1.3, ls=ls, zorder=1)
    for lab, (x, y) in meta.items():
        ax.add_patch(mpatches.FancyBboxPatch((x - 1.55, y - 0.42), 3.1, 0.84,
                     boxstyle="round,pad=0.08", fc="#1a1a2e", ec="white", lw=1.5, zorder=5))
        ax.annotate(lab, (x, y), ha="center", va="center", color="white",
                    fontsize=8, weight="bold", zorder=6)
    for d in domains:
        x, y = dpos[d]
        sub = facets[facets.parent == d].reset_index(drop=True)
        fx = np.linspace(x - 1.15, x + 1.15, 6)
        for i, r in sub.iterrows():
            ax.plot([x, fx[i]], [y - 0.42, 2.6], color=dom_col[d], lw=1.0, alpha=0.7, zorder=1)
            ax.annotate(r.label, (fx[i], 2.45), rotation=60, ha="right", va="top",
                        fontsize=7.2, color=dom_col[d])
        ax.add_patch(mpatches.FancyBboxPatch((x - 1.05, y - 0.42), 2.1, 0.84,
                     boxstyle="round,pad=0.08", fc=dom_col[d], ec="white", lw=1.5, zorder=5))
        ax.annotate(dom_lab[d], (x, y), ha="center", va="center", color="white",
                    fontsize=8, weight="bold", zorder=6)
    ax.annotate("Metatraits\n(Digman, 1997; DeYoung, 2015)", (13.9, 7.2), fontsize=8,
                style="italic", color="#555", ha="right")
    ax.annotate("Domains\n(Big Five)", (13.9, 4.8), fontsize=8, style="italic",
                color="#555", ha="right")
    ax.annotate("30 facets\n(NEO-PI-R)", (13.9, 1.6), fontsize=8, style="italic",
                color="#555", ha="right")
    ax.set_xlim(-0.3, 14.4); ax.set_ylim(-0.4, 8.2)
    ax.set_title("The trait-layer subgraph: metatraits, Big Five domains, and the 30 NEO facets\n"
                 "(dashed metatrait link: Neuroticism loads negatively on Stability; "
                 "subgraph communicates with the rest of the UPerG only through its mother node)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figD2_trait_hierarchy_30_facets.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure D3
def figD3_process_loop():
    """How traits get outside the skin and how life gets back in."""
    lay = {
        "T": (0.8, 3.2, "Trait\n(e.g., Conscien-\ntiousness)"),
        "S": (4.2, 5.0, "Situation\nselection /\nevocation"),
        "X": (7.6, 5.0, "Contexts &\nactivities"),
        "M": (4.2, 1.4, "Mediating\nbehaviors\n(e.g., health)"),
        "O": (7.6, 1.4, "Consequential\noutcomes"),
        "ST": (11.0, 3.2, "Momentary\nstates"),
    }
    arrows = [("T", "S", .6, "#c0392b"), ("S", "X", .6, "#c0392b"),
              ("T", "M", .6, "#c0392b"), ("M", "O", .6, "#c0392b"),
              ("X", "ST", .6, "#c0392b"), ("O", "ST", .4, "#c0392b")]
    fig, ax = plt.subplots(figsize=(11.5, 6))
    ax.axis("off")
    for s, tg, w, c in arrows:
        ax.add_patch(mpatches.FancyArrowPatch(
            lay[s][:2], lay[tg][:2], connectionstyle="arc3,rad=0.12",
            arrowstyle="-|>", mutation_scale=13, lw=0.8 + 3 * w, alpha=0.75,
            shrinkA=32, shrinkB=32, color=c))
    # feedback: outcomes -> trait (corresponsive), states -> trait (whole-trait consolidation)
    ax.add_patch(mpatches.FancyArrowPatch(lay["O"][:2], lay["T"][:2],
                 connectionstyle="arc3,rad=0.35", arrowstyle="-|>", mutation_scale=13,
                 lw=2.0, alpha=0.8, shrinkA=34, shrinkB=34, color="#27ae60", ls=":"))
    ax.add_patch(mpatches.FancyArrowPatch(lay["ST"][:2], lay["T"][:2],
                 connectionstyle="arc3,rad=-0.45", arrowstyle="-|>", mutation_scale=13,
                 lw=1.6, alpha=0.8, shrinkA=34, shrinkB=34, color="#27ae60", ls=":"))
    ax.annotate("corresponsive feedback\n(Caspi et al., 2005)", (4.6, -0.15),
                fontsize=7.6, color="#27ae60", ha="center", style="italic")
    ax.annotate("state-to-trait consolidation\n(Fleeson & Jayawickreme, 2015)", (7.2, 6.6),
                fontsize=7.6, color="#27ae60", ha="center", style="italic")
    for k, (x, y, lab) in lay.items():
        fc = "#2e86ab" if k not in ("T",) else "#1a1a2e"
        ax.add_patch(mpatches.FancyBboxPatch((x - 1.1, y - 0.68), 2.2, 1.36,
                     boxstyle="round,pad=0.08", fc=fc, ec="white", lw=1.5, zorder=5))
        ax.annotate(lab, (x, y), ha="center", va="center", color="white",
                    fontsize=7.6, weight="bold", zorder=6)
    ax.set_xlim(-0.8, 12.6); ax.set_ylim(-0.7, 7.2)
    ax.set_title("How traits get outside the skin — and how life gets back in\n"
                 "(red: instrumental and selective paths, after Hampson, 2012; "
                 "green dotted: the two documented return routes)", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figD3_process_loop.png"), dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    figD1_uperg()
    figD2_hierarchy()
    figD3_process_loop()
    print("Figures written to", os.path.abspath(FIGS))
