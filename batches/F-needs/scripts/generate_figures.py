"""
Universal Needs Graph (UNeedG) - Figure generation
Batch F: Needs paper (UPG series)
Reproducible: python3 generate_figures.py

Inputs : ../data/uneedg_nodes.csv, ../data/uneedg_edges.csv
Outputs: ../figures/figF1_universal_needs_graph.png
         ../figures/figF2_theory_domain_mapping.png
         ../figures/figF3_dual_channel_and_prepotency.png
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
nodes = pd.read_csv(os.path.join(DATA, "uneedg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "uneedg_edges.csv"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

SHORT = {
    "N": "Needs system\n(global)",
    "NEED_PHY": "Physiological /\nexistence", "NEED_SAF": "Safety /\nself-protection",
    "NEED_REL": "Relatedness /\nbelonging", "NEED_EST": "Esteem /\nstatus",
    "NEED_COM": "Competence", "NEED_AUT": "Autonomy", "NEED_MEA": "Meaning /\ngrowth",
    "SAT": "Satisfaction\nchannel", "FRU": "Frustration\nchannel",
    "CTX_ENV": "Environmental\nsupports/thwarts", "OUT_WB": "Wellbeing /\nflourishing",
    "OUT_IB": "Ill-being /\ndefensiveness", "MOT_IF": "Motivation &\ngoal layer",
    "PERS_IF": "Personality\nlayer",
    "MECH_PRI": "Dynamic\nprioritization", "MECH_STR": "Need\nstrength",
    "MECH_SUB": "Substitution /\ncompensation",
}

# ---------------------------------------------------------------- Figure F1
def figF1_uneedg():
    pos = {
        "N": (0, 6.0),
        "NEED_PHY": (-7.6, 4.0), "NEED_SAF": (-5.1, 4.4), "NEED_REL": (-2.6, 4.0),
        "NEED_EST": (-0.1, 4.4), "NEED_COM": (2.4, 4.0), "NEED_AUT": (4.9, 4.4),
        "NEED_MEA": (7.4, 4.0),
        "SAT": (-3.4, 1.2), "FRU": (2.6, 1.2),
        "CTX_ENV": (-7.6, 0.6), "MECH_PRI": (7.2, 1.6), "MECH_STR": (7.4, -0.8),
        "MECH_SUB": (4.9, -1.2),
        "OUT_WB": (-5.2, -2.2), "OUT_IB": (0.2, -2.4), "MOT_IF": (2.6, -3.4),
        "PERS_IF": (7.4, -3.0),
    }
    fig, ax = plt.subplots(figsize=(14, 9))
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
        if r.sign == "-":
            col = "#16a085"
        gated = isinstance(r.gate, str) and r.gate not in ("none",)
        rad = 0.0 if r.type == "hierarchical" else 0.16
        ax.add_patch(mpatches.FancyArrowPatch(
            pos[r.source], pos[r.target], connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>" if r.type != "hierarchical" else "-",
            mutation_scale=11, lw=0.6 + 2.6 * abs(r.weight), alpha=0.65,
            shrinkA=28, shrinkB=28, color=col, ls=ls, zorder=2))
        if gated and r.type != "hierarchical":
            mx = (pos[r.source][0] + pos[r.target][0]) / 2
            my = (pos[r.source][1] + pos[r.target][1]) / 2 + (0.35 if rad else 0.2)
            ax.plot(mx, my, marker="D", ms=5.5, color="#f1c40f",
                    mec="#7f6000", mew=0.8, zorder=8)
    for n, (x, y) in pos.items():
        lvl = int(nodes.loc[nodes.node_id == n, "level"].iloc[0])
        fc = {0: "#1a1a2e"}.get(lvl, "#2e86ab")
        if n in ("CTX_ENV", "OUT_WB", "OUT_IB", "MOT_IF", "PERS_IF"):
            fc = "#7f8c8d"
        if n.startswith("MECH"):
            fc = "#a0522d"
        if n in ("SAT",):
            fc = "#27ae60"
        if n in ("FRU",):
            fc = "#c0392b"
        ax.add_patch(mpatches.Circle((x, y), 0.92, fc=fc, ec="white", lw=2, zorder=5))
        ax.annotate(SHORT[n], (x, y), ha="center", va="center", color="white",
                    fontsize=7.0, weight="bold", zorder=6)
    handles = [
        Line2D([0], [0], color="#555555", lw=2, label="Hierarchical edge"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Cascade edge (directed)"),
        Line2D([0], [0], color="#2980b9", lw=2, ls="-.", label="Transactional edge (reciprocal)"),
        Line2D([0], [0], color="#16a085", lw=2, ls="--", label="Negative (signed) edge (Axiom 5)"),
        Line2D([0], [0], color="#8e44ad", lw=1.5, label="Self-loop (Axiom 4)"),
        Line2D([0], [0], marker="D", color="w", mfc="#f1c40f", mec="#7f6000",
               ms=7, label="Gated weight w(t) (situational / life-stage)"),
        mpatches.Patch(color="#27ae60", label="Satisfaction channel"),
        mpatches.Patch(color="#c0392b", label="Frustration channel"),
        mpatches.Patch(color="#7f8c8d", label="Interface node (Systems / Disorder / Motivation / Personality)"),
        mpatches.Patch(color="#a0522d", label="Mechanism node"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=7.4,
              frameon=False, bbox_to_anchor=(0.5, -0.06))
    ax.set_xlim(-9.4, 9.6); ax.set_ylim(-4.9, 7.2)
    ax.set_title("Universal Needs Graph: seven domains, dual channels, and priority dynamics\n"
                 "(edge thickness " + r"$\propto$" + " provisional consensus weight; diamonds mark gated edges)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figF1_universal_needs_graph.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure F2
def figF2_mapping():
    rows = [
        ("Murray (1938)", ["viscerogenic\nneeds", "affiliation,\nsuccorance", "dominance,\nrecognition", "achievement", "autonomy", "(implicit in\nplay/understanding)"]),
        ("Maslow (1943)", ["physiological;\nsafety", "love /\nbelonging", "esteem", "(within esteem:\ncompetence)", "(precondition\nfor all)", "self-\nactualization"]),
        ("Alderfer (ERG)", ["existence", "relatedness", "(within\nrelatedness)", "growth", "(within\ngrowth)", "growth"]),
        ("Herzberg", ["hygiene\nfactors", "hygiene\n(relations)", "recognition\n(motivator)", "achievement\n(motivator)", "responsibility\n(motivator)", "growth\n(motivator)"]),
        ("McClelland", ["(assumed\nbaseline)", "need for\naffiliation", "need for\npower", "need for\nachievement", "(not\nrepresented)", "(not\nrepresented)"]),
        ("SDT (Ryan & Deci)", ["(precondition,\nnot core need)", "relatedness", "(derivative,\nnot basic)", "competence", "autonomy", "(candidate 4th:\nmeaning)"]),
        ("Dweck (2017)", ["(predictability\nas basic)", "acceptance", "status", "competence", "(composite of\nbasic needs)", "(via self-\ncoherence)"]),
        ("Kenrick et al. (2010)", ["physiological;\nself-protection", "affiliation;\nmate/care line", "status /\nesteem", "(within\nstatus)", "(not\nrepresented)", "(subsumed in\nmating/status)"]),
        ("Tønnesvang (MARC)", ["(background\ncondition)", "relatedness", "(derivative)", "competence", "autonomy", "meaning"]),
    ]
    cols = ["Existence / safety", "Relatedness", "Esteem / status", "Competence", "Autonomy", "Meaning / growth"]
    col_colors = ["#8e6d3a", "#c0392b", "#e67e22", "#2980b9", "#27ae60", "#8e44ad"]
    fig, ax = plt.subplots(figsize=(13.5, 8.2))
    ax.axis("off")
    x0, y0, cw, rh = 3.0, 7.6, 1.95, 0.86
    for j, (c, cc) in enumerate(zip(cols, col_colors)):
        ax.add_patch(mpatches.FancyBboxPatch((x0 + j * cw - 0.88, y0 + 0.55), 1.76, 0.56,
                     boxstyle="round,pad=0.05", fc=cc, ec="white", lw=1.2))
        ax.annotate(c, (x0 + j * cw, y0 + 0.83), ha="center", va="center",
                    color="white", fontsize=6.9, weight="bold")
    for i, (model, cells) in enumerate(rows):
        y = y0 - i * rh
        ax.annotate(model, (0.05, y), ha="left", va="center", fontsize=7.8, weight="bold")
        for j, cell in enumerate(cells):
            fc = "#f2f2f2" if cell.startswith("(") else "white"
            ax.add_patch(mpatches.FancyBboxPatch((x0 + j * cw - 0.88, y - 0.36), 1.76, 0.72,
                         boxstyle="round,pad=0.04", fc=fc, ec=col_colors[j], lw=1.0))
            ax.annotate(cell, (x0 + j * cw, y), ha="center", va="center", fontsize=6.2,
                        color="#333")
    ax.set_xlim(-0.4, 14.6); ax.set_ylim(-0.9, 9.0)
    ax.set_title("Convergence across needs theories: constructs mapped onto the seven-domain consensus core\n"
                 "(existence and safety displayed as one column; after Sohrabi et al., 2021; Szalma, 2020; "
                 "Kenrick et al., 2010; Tønnesvang, 2025; grey cells: derivative, implicit, or absent)", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figF2_theory_domain_mapping.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------------- Figure F3
def figF3_channels_prepotency():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    # Panel A: dual-channel asymmetry
    x = np.linspace(0, 1, 200)
    ax1.plot(x, 0.15 + 0.75 * x, lw=2.4, color="#27ae60",
             label="Satisfaction " + r"$\rightarrow$" + " wellbeing (+0.70)")
    ax1.plot(x, 0.72 - 0.30 * x, lw=2.0, ls="--", color="#27ae60",
             label="Satisfaction " + r"$\rightarrow$" + " ill-being (−0.35)")
    ax1.plot(x, 0.12 + 0.78 * x, lw=2.4, color="#c0392b",
             label="Frustration " + r"$\rightarrow$" + " ill-being (+0.70)")
    ax1.plot(x, 0.70 - 0.32 * x, lw=2.0, ls="--", color="#c0392b",
             label="Frustration " + r"$\rightarrow$" + " wellbeing (−0.35)")
    ax1.set_xlabel("Channel state (satisfaction or frustration)")
    ax1.set_ylabel("Outcome level (illustrative)")
    ax1.set_title("A. Dual-channel asymmetry: frustration is not\nmerely low satisfaction "
                  "(Vansteenkiste & Ryan, 2013)", fontsize=9.5)
    ax1.legend(fontsize=7.2, frameon=False)
    ax1.spines[["top", "right"]].set_visible(False)
    # Panel B: dynamic prepotency
    t = np.linspace(0, 24, 600)  # hours
    base = {"Existence (hunger cycle)": 0.25 + 0.35 * (1 + np.sin(t / 24 * 2 * np.pi * 3 - 1.2)) / 2,
            "Safety (threat cue at 14h)": 0.15 + 0.75 * np.exp(-((t - 14) ** 2) / 1.2),
            "Relatedness (evening rise)": 0.25 + 0.35 * np.exp(-((t - 20) ** 2) / 14),
            "Competence (workday arc)": 0.2 + 0.35 * np.exp(-((t - 10.5) ** 2) / 22)}
    colors = ["#8e6d3a", "#e74c3c", "#2980b9", "#27ae60"]
    for (lab, y), c in zip(base.items(), colors):
        ax2.plot(t, y, lw=2.0, color=c, label=lab)
    ax2.set_xlabel("Time of day (h) — illustrative")
    ax2.set_ylabel("Need salience (priority weight)")
    ax2.set_ylim(0, 1.05)
    ax2.set_title("B. Dynamic prepotency: salience from deficit +\nsituational triggers, no fixed ladder "
                  "(Kenrick et al., 2010)", fontsize=9.5)
    ax2.legend(fontsize=7.2, frameon=False, loc="upper left")
    ax2.spines[["top", "right"]].set_visible(False)
    plt.suptitle("The two dynamics the UNeedG carries as edges (illustrative shapes, not fitted functions)",
                 fontsize=10.5, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figF3_dual_channel_and_prepotency.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    figF1_uneedg()
    figF2_mapping()
    figF3_channels_prepotency()
    print("Figures written to", os.path.abspath(FIGS))
