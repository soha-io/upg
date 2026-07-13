"""
Universal Temperament Graph (UTempG) - Figure generation
Batch E: Temperament paper (UPG series)
Reproducible: python3 generate_figures.py

Inputs : ../data/utempg_nodes.csv, ../data/utempg_edges.csv
Outputs: ../figures/figE1_universal_temperament_graph.png
         ../figures/figE2_model_dimension_mapping.png
         ../figures/figE3_goodness_of_fit_surface.png
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
nodes = pd.read_csv(os.path.join(DATA, "utempg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "utempg_edges.csv"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

SHORT = {
    "T": "Temperament\n(global)", "BIO_GEN": "Genetic /\nphysiological\nsubstrate",
    "DIM_NA": "Negative\naffectivity", "DIM_SU": "Surgency /\npositive affect",
    "DIM_EC": "Effortful\ncontrol", "TYPE": "Configural\ntypes",
    "FIT": "Goodness\nof fit", "CTX_CARE": "Caregiving /\ndemands",
    "OUT_ADJ": "Maladjustment\nrisk", "PERS_IF": "Personality\ntrait layer",
    "MECH_TXT": "T x T\nmoderation", "MECH_TXE": "T x E\nmoderation",
    "MECH_MAT": "Regulatory\nmaturation",
}

# ---------------------------------------------------------------- Figure E1
def figE1_utempg():
    pos = {
        "T": (0, 5.2),
        "BIO_GEN": (-7.8, 3.4),
        "DIM_NA": (-3.9, 2.9), "DIM_SU": (0.0, 2.9), "DIM_EC": (3.9, 2.9),
        "TYPE": (7.6, 3.4),
        "MECH_MAT": (7.0, 0.9), "MECH_TXT": (4.6, -1.3), "MECH_TXE": (-6.2, -1.3),
        "FIT": (-3.4, -0.9), "CTX_CARE": (-7.4, 0.9),
        "OUT_ADJ": (0.6, -2.6), "PERS_IF": (4.4, -3.2),
    }
    fig, ax = plt.subplots(figsize=(13.5, 8.5))
    ax.axis("off")
    stylemap = {"hierarchical": ("#555555", "-"), "cascade": ("#c0392b", "--"),
                "transactional": ("#2980b9", "-."), "moderation": ("#e67e22", ":")}
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
        if r.sign == "-":
            col = "#16a085"
        gated = isinstance(r.gate, str) and r.gate not in ("none",)
        rad = 0.0 if r.type == "hierarchical" else 0.18
        ax.add_patch(mpatches.FancyArrowPatch(
            pos[r.source], pos[r.target], connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>" if r.type != "hierarchical" else "-",
            mutation_scale=11, lw=0.6 + 2.8 * abs(r.weight), alpha=0.7,
            shrinkA=28, shrinkB=28, color=col, ls=ls, zorder=2))
        if gated and r.type != "hierarchical":
            mx = (pos[r.source][0] + pos[r.target][0]) / 2
            my = (pos[r.source][1] + pos[r.target][1]) / 2 + (0.4 if rad else 0.2)
            ax.plot(mx, my, marker="D", ms=5.5, color="#f1c40f",
                    mec="#7f6000", mew=0.8, zorder=8)
    for n, (x, y) in pos.items():
        lvl = int(nodes.loc[nodes.node_id == n, "level"].iloc[0])
        fc = {0: "#1a1a2e"}.get(lvl, "#2e86ab")
        if n in ("BIO_GEN", "CTX_CARE", "OUT_ADJ", "PERS_IF"):
            fc = "#7f8c8d"
        if n.startswith("MECH"):
            fc = "#a0522d"
        ax.add_patch(mpatches.Circle((x, y), 0.92, fc=fc, ec="white", lw=2, zorder=5))
        ax.annotate(SHORT[n], (x, y), ha="center", va="center", color="white",
                    fontsize=7.2, weight="bold", zorder=6)
    handles = [
        Line2D([0], [0], color="#555555", lw=2, label="Hierarchical edge"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Cascade edge (directed)"),
        Line2D([0], [0], color="#2980b9", lw=2, ls="-.", label="Transactional edge (reciprocal)"),
        Line2D([0], [0], color="#e67e22", lw=2, ls=":", label="Moderation edge"),
        Line2D([0], [0], color="#16a085", lw=2, ls="--", label="Negative (signed) edge (Axiom 5)"),
        Line2D([0], [0], color="#8e44ad", lw=1.5, label="Self-loop (Axiom 4)"),
        Line2D([0], [0], marker="D", color="w", mfc="#f1c40f", mec="#7f6000",
               ms=7, label="Time-gated weight w(t)"),
        mpatches.Patch(color="#7f8c8d", label="Interface node (Biology / Systems / Disorder / Personality)"),
        mpatches.Patch(color="#a0522d", label="Mechanism node"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=7.6,
              frameon=False, bbox_to_anchor=(0.5, -0.07))
    ax.set_xlim(-9.4, 9.4); ax.set_ylim(-4.6, 6.4)
    ax.set_title("Universal Temperament Graph: reactivity, regulation, fit, and their traffic\n"
                 "(edge thickness " + r"$\propto$" + " provisional consensus weight; diamonds mark time-gated edges)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figE1_universal_temperament_graph.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure E2
def figE2_mapping():
    """The four classic models' constructs mapped onto the three convergent dimensions."""
    rows = [
        ("Thomas & Chess (NYLS)", ["mood (negative),\nwithdrawal, intensity", "activity, approach,\nadaptability", "persistence /\nattention span", "9 dimensions;\n3 types"]),
        ("Buss & Plomin (EAS)", ["emotionality", "activity,\nsociability", "(not represented)", "heritability\ncriterion"]),
        ("Goldsmith & Campos", ["fear, anger,\nsadness", "pleasure /\ninterest", "(regulation via\nexpression)", "emotion-centered\ndefinition"]),
        ("Rothbart", ["negative\naffectivity", "surgency /\nextraversion", "effortful\ncontrol", "reactivity +\nself-regulation"]),
        ("Kagan", ["high-reactive /\ninhibited bias", "low-reactive /\nuninhibited bias", "(indirect via\nfrontal maturation)", "categorical\nbiases"]),
    ]
    cols = ["Negative affectivity", "Surgency / positive affectivity", "Effortful control", "Model signature"]
    col_colors = ["#c0392b", "#e67e22", "#2980b9", "#7f8c8d"]
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    ax.axis("off")
    x0, y0, cw, rh = 2.6, 5.4, 2.55, 0.98
    for j, (c, cc) in enumerate(zip(cols, col_colors)):
        ax.add_patch(mpatches.FancyBboxPatch((x0 + j * cw - 1.12, y0 + 0.62), 2.24, 0.62,
                     boxstyle="round,pad=0.06", fc=cc, ec="white", lw=1.2))
        ax.annotate(c, (x0 + j * cw, y0 + 0.93), ha="center", va="center",
                    color="white", fontsize=7.6, weight="bold")
    for i, (model, cells) in enumerate(rows):
        y = y0 - i * rh
        ax.annotate(model, (0.1, y), ha="left", va="center", fontsize=8.4, weight="bold")
        for j, cell in enumerate(cells):
            fc = "#f2f2f2" if "(not" in cell or "(indirect" in cell or "(regulation" in cell else "white"
            ax.add_patch(mpatches.FancyBboxPatch((x0 + j * cw - 1.12, y - 0.40), 2.24, 0.80,
                         boxstyle="round,pad=0.05", fc=fc, ec=col_colors[j], lw=1.1))
            ax.annotate(cell, (x0 + j * cw, y), ha="center", va="center", fontsize=6.9,
                        color="#333")
    ax.annotate("RST mapping (Gomez et al., 2016):  BIS/FFFS " + r"$\rightarrow$" +
                " negative affectivity      BAS " + r"$\rightarrow$" + " surgency      "
                "(effortful control outside RST reactive systems)",
                (x0 + 1.5 * cw, y0 - 4.9), ha="center", fontsize=8, style="italic", color="#555")
    ax.set_xlim(-0.4, 13.0); ax.set_ylim(-0.4, 7.2)
    ax.set_title("Convergence across the classic models: constructs mapped onto the three consensus dimensions\n"
                 "(after Goldsmith et al., 1987; Fu & Pérez-Edgar, 2015; Rettew & McKee, 2005)", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figE2_model_dimension_mapping.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure E3
def figE3_fit_surface():
    """Goodness of fit as an interaction surface: risk = f(temperamental load, environmental support)."""
    t = np.linspace(0, 1, 120)   # temperamental load (e.g., negative reactivity)
    e = np.linspace(0, 1, 120)   # environmental support / fit
    T, E = np.meshgrid(t, e)
    risk = T * (1.15 - E) + 0.08 * (1 - E)
    fig, ax = plt.subplots(figsize=(9.5, 6))
    cf = ax.contourf(T, E, risk, levels=14, cmap="RdYlGn_r")
    cbar = fig.colorbar(cf, ax=ax)
    cbar.set_label("Maladjustment risk (illustrative)")
    ax.plot(t, 0.15 + 0 * t, ls=":", color="k", lw=1.2)
    ax.plot(t, 0.85 + 0 * t, ls="--", color="k", lw=1.2)
    ax.annotate("low-support environment: risk rises steeply with load", (0.03, 0.10),
                fontsize=8, color="k")
    ax.annotate("high-support environment: risk curve flattened", (0.03, 0.88),
                fontsize=8, color="k")
    ax.set_xlabel("Temperamental load (e.g., negative reactivity, low effortful control)")
    ax.set_ylabel("Environmental support / goodness of fit")
    ax.set_title("Goodness of fit as an interaction surface\n"
                 "(illustrative rendering of the T" + r"$\times$" + "E moderation edges; "
                 "after Chess & Thomas, 1989; McClowry et al., 2008; Berdan et al., 2008)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figE3_goodness_of_fit_surface.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    figE1_utempg()
    figE2_mapping()
    figE3_fit_surface()
    print("Figures written to", os.path.abspath(FIGS))
