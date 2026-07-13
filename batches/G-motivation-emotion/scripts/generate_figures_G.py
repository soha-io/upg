"""
Universal Motivation-Emotion Graph (UMEG) - Figure generation
Batch G: Motivation & Emotion paper (UPG series)
Reproducible: python3 generate_figures.py

Inputs : ../data/umeg_nodes.csv, ../data/umeg_edges.csv
Outputs: ../figures/figG1_universal_motivation_emotion_graph.png
         ../figures/figG2_theory_construct_mapping.png
         ../figures/figG3_wanting_liking_and_dual_readout.png
         ../figures/figG4_affect_circumplex.png
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
nodes = pd.read_csv(os.path.join(DATA, "umeg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "umeg_edges.csv"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

SHORT = {
    "ME": "Motivation-\nEmotion\nsystem",
    "APPR": "Appraisal /\nvaluation core",
    "MOT": "Motivation\nreadout", "EMO": "Emotion\nreadout",
    "BAS": "Approach /\nreward channel", "AVD": "Avoidance /\npunishment channel",
    "OUT_ACT": "Action /\nbehavior",
    "NEEDS_IF": "Needs\ninput layer", "SYS_IF": "Situation /\nenvironment",
    "PERS_IF": "Personality\nlayer", "TEMP_IF": "Temperament\nlayer",
    "DIS_IF": "Psychopathology\ninterface", "THER_IF": "Therapy /\nregulation",
    "MECH_ATTR": "Causal\nattribution", "MECH_SAL": "Incentive\nsalience\n('wanting')",
    "MECH_REG": "Regulation", "MECH_LEARN": "Reinforcement\nlearning",
}

# nodes shown at domain/channel/mechanism resolution (facets live in figG4 / subgraphs)
DISPLAY = ["ME", "APPR", "MOT", "EMO", "BAS", "AVD", "OUT_ACT",
           "NEEDS_IF", "SYS_IF", "PERS_IF", "TEMP_IF", "DIS_IF", "THER_IF",
           "MECH_ATTR", "MECH_SAL", "MECH_REG", "MECH_LEARN"]
PARENT = dict(zip(nodes.node_id, nodes.parent.fillna("")))


def disp(n):
    """Collapse a level-2 facet to its parent for the domain-level figure."""
    if n in DISPLAY:
        return n
    p = PARENT.get(n, "")
    return p if p in DISPLAY else None


# --------------------------------------------------------------- Figure G1
def figG1_umeg():
    pos = {
        "ME": (0.0, 7.2),
        "NEEDS_IF": (-8.6, 5.2), "PERS_IF": (-8.6, 2.9),
        "TEMP_IF": (-8.6, 0.6), "SYS_IF": (-8.6, -1.8),
        "APPR": (-2.6, 4.3),
        "MECH_LEARN": (3.9, 6.2), "MECH_ATTR": (6.7, 3.6),
        "MECH_SAL": (3.1, 1.4), "MECH_REG": (-4.4, 0.7),
        "BAS": (-0.2, 1.9), "AVD": (1.2, -0.4),
        "MOT": (-3.0, -2.2), "EMO": (3.4, -1.7),
        "OUT_ACT": (-0.3, -4.6), "DIS_IF": (6.6, -3.4),
        "THER_IF": (-7.2, -3.1),
    }
    # build collapsed edge list (cascade + transactional; hierarchical only ME->L1)
    drawn = {}
    for _, r in edges.iterrows():
        s, t = disp(r.source), disp(r.target)
        if s is None or t is None:
            continue
        if r.type == "hierarchical" and r.source != "ME":
            continue
        if s == t and not (r.source == r.target):   # facet->sibling collapses; skip spurious loop
            continue
        key = (s, t, r.sign)
        if key not in drawn or abs(r.weight) > abs(drawn[key][0]):
            drawn[key] = (r.weight, r.type, r.gate)

    fig, ax = plt.subplots(figsize=(15, 9.5))
    ax.axis("off")
    stylemap = {"hierarchical": ("#555555", "-"), "cascade": ("#c0392b", "--"),
                "transactional": ("#2980b9", "-.")}
    for (s, t, sign), (w, typ, gate) in drawn.items():
        if s == t:  # self-loop (Axiom 4)
            x, y = pos[s]
            ax.add_patch(mpatches.FancyArrowPatch((x - 0.4, y + 0.6), (x + 0.4, y + 0.62),
                         connectionstyle="arc3,rad=1.7", arrowstyle="-|>",
                         mutation_scale=10, color="#8e44ad", lw=1.5, zorder=7))
            continue
        col, ls = stylemap.get(typ, ("#c0392b", "--"))
        if sign == "-":
            col = "#16a085"
        gated = isinstance(gate, str) and gate not in ("none",)
        rad = 0.0 if typ == "hierarchical" else 0.15
        ax.add_patch(mpatches.FancyArrowPatch(
            pos[s], pos[t], connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>" if typ != "hierarchical" else "-",
            mutation_scale=12, lw=0.6 + 2.6 * abs(w), alpha=0.62,
            shrinkA=30, shrinkB=30, color=col, ls=ls, zorder=2))
        if gated and typ != "hierarchical":
            mx = (pos[s][0] + pos[t][0]) / 2
            my = (pos[s][1] + pos[t][1]) / 2 + (0.32 if rad else 0.2)
            ax.plot(mx, my, marker="D", ms=5.5, color="#f1c40f",
                    mec="#7f6000", mew=0.8, zorder=8)
    for n, (x, y) in pos.items():
        lvl = int(nodes.loc[nodes.node_id == n, "level"].iloc[0])
        fc = {0: "#1a1a2e"}.get(lvl, "#2e86ab")
        if n in ("NEEDS_IF", "SYS_IF", "PERS_IF", "TEMP_IF", "DIS_IF", "THER_IF"):
            fc = "#7f8c8d"
        if n.startswith("MECH"):
            fc = "#a0522d"
        if n == "APPR":
            fc = "#6c3483"
        if n == "BAS":
            fc = "#27ae60"
        if n == "AVD":
            fc = "#c0392b"
        if n == "OUT_ACT":
            fc = "#d68910"
        rad = 1.02 if n == "ME" else 0.95
        ax.add_patch(mpatches.Circle((x, y), rad, fc=fc, ec="white", lw=2, zorder=5))
        ax.annotate(SHORT[n], (x, y), ha="center", va="center", color="white",
                    fontsize=6.8, weight="bold", zorder=6)
    handles = [
        Line2D([0], [0], color="#555555", lw=2, label="Hierarchical edge"),
        Line2D([0], [0], color="#c0392b", lw=2, ls="--", label="Cascade edge (directed)"),
        Line2D([0], [0], color="#2980b9", lw=2, ls="-.", label="Transactional edge (reciprocal)"),
        Line2D([0], [0], color="#16a085", lw=2, ls="--", label="Negative (signed) edge (Axiom 5)"),
        Line2D([0], [0], color="#8e44ad", lw=1.5, label="Self-loop (Axiom 4)"),
        Line2D([0], [0], marker="D", color="w", mfc="#f1c40f", mec="#7f6000",
               ms=7, label="Gated weight w(t) (situational / developmental)"),
        mpatches.Patch(color="#6c3483", label="Appraisal / valuation core"),
        mpatches.Patch(color="#27ae60", label="Approach channel"),
        mpatches.Patch(color="#c0392b", label="Avoidance channel"),
        mpatches.Patch(color="#a0522d", label="Mechanism node"),
        mpatches.Patch(color="#7f8c8d", label="Interface node (Needs / Systems / Personality / Temperament / Disorder / Therapy)"),
        mpatches.Patch(color="#d68910", label="Action output"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=7.3,
              frameon=False, bbox_to_anchor=(0.5, -0.07))
    ax.set_xlim(-10.4, 8.8)
    ax.set_ylim(-6.0, 8.6)
    ax.set_title("Universal Motivation-Emotion Graph: one valuation process, two coupled readouts\n"
                 "(edge thickness " + r"$\propto$" + " provisional consensus weight; diamonds mark gated edges; "
                 "facets shown in Figure G4)", fontsize=10.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figG1_universal_motivation_emotion_graph.png"),
                dpi=300, bbox_inches="tight")
    plt.close()


# --------------------------------------------------------------- Figure G2
def figG2_mapping():
    cols = ["Appraisal /\nvaluation", "Motivation\n(dir/int/pers)", "Core affect\n(dimensional)",
            "Discrete\nemotion", "Wanting /\nliking", "Regulation /\nexpression"]
    col_colors = ["#6c3483", "#2980b9", "#16a085", "#e67e22", "#c0392b", "#8e6d3a"]
    rows = [
        ("Weiner (1985)", ["causal\nattribution", "expectancy →\npersistence", "(implicit\nvalence)", "pride, shame,\nguilt, anger", "(—)", "(—)"]),
        ("Buck (1985) PRIME", ["prime\nreadout", "primes\nenergize", "readout of\nprimes", "primary\naffects", "drive /\nincentive", "display\nrules"]),
        ("Berridge (2018)", ["reward\nvaluation", "incentive\nsalience", "affective\nvalence", "fear,\ndisgust", "wanting vs\nliking", "(—)"]),
        ("Lazarus (1991)", ["primary +\nsecondary", "goal\ncommitment", "(via\nappraisal)", "core relational\nthemes", "(—)", "coping /\nreappraisal"]),
        ("Rolls (2025)", ["reinforcer\nvalue (OFC)", "goal-directed\naction", "reward /\npunisher", "reinforcer-\nlinked states", "reward\nexpectation", "reasoning\noverride"]),
        ("Ekman (1992)", ["auto-\nappraisers", "(—)", "(—)", "6 basic\nemotions", "(—)", "facial\nexpression"]),
        ("Russell (2003)", ["(via\ncategorization)", "(—)", "core affect\n(V x A)", "constructed\ncategories", "(—)", "(—)"]),
        ("Barrett (2017)", ["predictive\ninference", "allostasis\nbudgeting", "interoceptive\naffect", "conceptual\nconstruction", "(—)", "concept\nregulation"]),
        ("Scherer (2009)", ["stimulus-eval.\nchecks (SECs)", "action\ntendency", "feeling\ncomponent", "modal\nemotions", "(—)", "expression\ncomponent"]),
        ("Panksepp (2011)", ["(sub-\ncortical)", "SEEKING\nsystem", "primal\naffect", "7 primary\nsystems", "SEEKING /\nreward", "(—)"]),
        ("Gross (1998)", ["situation\nappraisal", "goal\npursuit", "affect\nmodulation", "(any\nemotion)", "(—)", "5-point\nregulation"]),
        ("Frijda (1986)", ["relevance\nappraisal", "action\nreadiness", "pleasure /\npain", "emotion =\ntendency", "(—)", "regulation /\ncontrol"]),
    ]
    fig, ax = plt.subplots(figsize=(14.5, 9.2))
    ax.axis("off")
    x0, y0, cw, rh = 3.2, 11.6, 1.92, 0.86
    for j, (c, cc) in enumerate(zip(cols, col_colors)):
        ax.add_patch(mpatches.FancyBboxPatch((x0 + j * cw - 0.9, y0 + 0.42), 1.8, 0.72,
                     boxstyle="round,pad=0.04", fc=cc, ec="white", lw=1.2))
        ax.annotate(c, (x0 + j * cw, y0 + 0.78), ha="center", va="center",
                    color="white", fontsize=6.6, weight="bold")
    for i, (model, cells) in enumerate(rows):
        y = y0 - (i + 1) * rh
        ax.annotate(model, (0.02, y), ha="left", va="center", fontsize=7.6, weight="bold")
        for j, cell in enumerate(cells):
            empty = cell.strip().startswith("(")
            fc = "#f2f2f2" if empty else "white"
            ax.add_patch(mpatches.FancyBboxPatch((x0 + j * cw - 0.9, y - 0.37), 1.8, 0.74,
                         boxstyle="round,pad=0.03", fc=fc, ec=col_colors[j], lw=1.0))
            ax.annotate(cell, (x0 + j * cw, y), ha="center", va="center", fontsize=6.1,
                        color="#333")
    ax.set_xlim(-0.4, 15.4)
    ax.set_ylim(0.2, 13.0)
    ax.set_title("Convergence across motivation-emotion theories: constructs mapped onto the UMEG components\n"
                 "(grey cells: derivative, implicit, or absent in the source theory)", fontsize=10.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figG2_theory_construct_mapping.png"),
                dpi=300, bbox_inches="tight")
    plt.close()


# --------------------------------------------------------------- Figure G3
def figG3_dynamics():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    # Panel A: wanting / liking / learning dissociation (Berridge)
    x = np.linspace(0, 1, 200)          # cumulative reward exposure (illustrative)
    wanting = 0.20 + 0.75 * (1 - np.exp(-3.2 * x))          # sensitizes upward
    liking = 0.62 - 0.34 * x                                # habituates / flat-to-down
    learning = 0.15 + 0.80 * (1 - np.exp(-5.0 * x))         # saturates
    ax1.plot(x, wanting, lw=2.6, color="#c0392b", label="'Wanting' (incentive salience)")
    ax1.plot(x, liking, lw=2.4, ls="--", color="#27ae60", label="'Liking' (hedonic impact)")
    ax1.plot(x, learning, lw=2.0, ls=":", color="#2980b9", label="Learning (value update)")
    ax1.annotate("addiction:\nwanting >> liking", (0.83, 0.86), fontsize=7.4, color="#c0392b",
                 ha="center", va="center")
    ax1.set_xlabel("Cumulative reward exposure (illustrative)")
    ax1.set_ylabel("Component strength")
    ax1.set_ylim(0, 1.05)
    ax1.set_title("A. Wanting ≠ liking ≠ learning: three dissociable\nreward components (Berridge, 2018)", fontsize=9.5)
    ax1.legend(fontsize=7.2, frameon=False, loc="center right")
    ax1.spines[["top", "right"]].set_visible(False)
    # Panel B: one appraised-value axis, two readouts (motivation + emotion)
    v = np.linspace(-1, 1, 200)                              # appraised value: punisher -> reward
    approach = 1 / (1 + np.exp(-4.0 * v))                    # motivation: approach tendency
    valence = 0.5 + 0.5 * np.tanh(1.8 * v)                   # emotion: hedonic valence
    arousal = 0.35 + 0.6 * v**2                              # emotion: arousal (U-shaped)
    ax2.plot(v, approach, lw=2.6, color="#2980b9", label="Motivation readout (approach tendency)")
    ax2.plot(v, valence, lw=2.4, color="#16a085", label="Emotion readout (core-affect valence)")
    ax2.plot(v, arousal, lw=2.0, ls="--", color="#e67e22", label="Emotion readout (arousal)")
    ax2.axvline(0, color="#999", lw=0.8, ls=":")
    ax2.set_xlabel("Appraised reward/punisher value (single valuation axis)")
    ax2.set_ylabel("Readout level (illustrative)")
    ax2.set_ylim(0, 1.05)
    ax2.set_title("B. One process, two readouts: motivation and emotion\nco-emerge from appraised value (Buck, 1985; Rolls, 2025)", fontsize=9.5)
    ax2.legend(fontsize=7.2, frameon=False, loc="upper left")
    ax2.spines[["top", "right"]].set_visible(False)
    plt.suptitle("The two signature dynamics the UMEG carries as edges (illustrative shapes, not fitted functions)",
                 fontsize=10.5, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figG3_wanting_liking_and_dual_readout.png"),
                dpi=300, bbox_inches="tight")
    plt.close()


# --------------------------------------------------------------- Figure G4
def figG4_circumplex():
    fig, ax = plt.subplots(figsize=(9.2, 9.2))
    # circle
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color="#333", lw=1.4, zorder=2)
    ax.axhline(0, color="#bbb", lw=1.0, zorder=1)
    ax.axvline(0, color="#bbb", lw=1.0, zorder=1)
    # discrete emotions placed by (valence, arousal) angle on the circumplex
    emos = {
        "excited": 62, "elated": 75, "happy": 30, "delighted": 45,
        "content": 8, "serene": -12, "relaxed": -28, "calm": -42,
        "sleepy": -70, "tired": -88, "bored": -122, "depressed": -108,
        "sad": -140, "gloomy": -158, "miserable": 200, "distressed": 158,
        "frustrated": 143, "afraid": 128, "angry": 118, "tense": 105, "alarmed": 92,
    }
    quad_color = lambda a: ("#27ae60" if -90 < a < 90 and np.sin(np.radians(a)) >= 0 else
                            "#e67e22" if np.sin(np.radians(a)) >= 0 else
                            ("#7f8c8d" if np.cos(np.radians(a)) >= 0 else "#c0392b"))
    for name, ang in emos.items():
        a = np.radians(ang)
        r = 0.86
        x, y = r * np.cos(a), r * np.sin(a)
        vpos = np.cos(a) >= 0
        col = "#27ae60" if (np.cos(a) >= 0 and np.sin(a) >= 0) else \
              "#e67e22" if (np.cos(a) < 0 and np.sin(a) >= 0) else \
              "#c0392b" if (np.cos(a) < 0 and np.sin(a) < 0) else "#2980b9"
        ax.plot(x, y, "o", ms=7, color=col, zorder=4)
        ax.annotate(name, (x * 1.07, y * 1.07), fontsize=7.6,
                    ha="left" if x >= 0 else "right", va="center", color="#222", zorder=5)
    # axes labels
    ax.annotate("HIGH AROUSAL", (0, 1.16), ha="center", fontsize=9.5, weight="bold", color="#555")
    ax.annotate("LOW AROUSAL", (0, -1.18), ha="center", fontsize=9.5, weight="bold", color="#555")
    ax.annotate("UNPLEASANT\n(negative valence)", (-1.2, 0), ha="center", va="center",
                fontsize=9.5, weight="bold", color="#555", rotation=90)
    ax.annotate("PLEASANT\n(positive valence)", (1.2, 0), ha="center", va="center",
                fontsize=9.5, weight="bold", color="#555", rotation=-90)
    # quadrant appraisal annotations
    ax.annotate("goal-congruent +\nhigh control", (0.52, 0.52), fontsize=7.0, color="#1e8449",
                ha="center", style="italic")
    ax.annotate("goal-incongruent +\nother-blame / threat", (-0.55, 0.52), fontsize=7.0, color="#b9770e",
                ha="center", style="italic")
    ax.annotate("goal-incongruent +\nloss / low control", (-0.55, -0.52), fontsize=7.0, color="#a93226",
                ha="center", style="italic")
    ax.annotate("goal-attained +\nlow demand", (0.52, -0.52), fontsize=7.0, color="#21618c",
                ha="center", style="italic")
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("The affect circumplex: discrete emotion as regions of the valence x arousal core-affect plane\n"
                 "(integrating dimensional and categorical accounts; after Russell, 2003; appraisal quadrants "
                 "after Lazarus, 1991 / Weiner, 1985)", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "figG4_affect_circumplex.png"),
                dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    figG1_umeg()
    figG2_mapping()
    figG3_dynamics()
    figG4_circumplex()
    print("Figures written to", os.path.abspath(FIGS))
