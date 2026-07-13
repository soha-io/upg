"""
Universal Systems Graph (USysG) - Figure generation
Batch H: Systems models paper (UPG series)
Reproducible: python3 generate_figures.py

Inputs : ../data/usysg_nodes.csv, ../data/usysg_edges.csv
Outputs: ../figures/figH1_universal_systems_graph.png
         ../figures/figH2_theory_construct_mapping.png
         ../figures/figH3_social_determinant_cascade.png
         ../figures/figH4_nested_ecological_topology.png
All weights are consensus priors with cited provenance (see CSVs).
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIGS = os.path.join(HERE, "..", "figures")
os.makedirs(FIGS, exist_ok=True)
nodes = pd.read_csv(os.path.join(DATA, "usysg_nodes.csv"))
edges = pd.read_csv(os.path.join(DATA, "usysg_edges.csv"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

POS_C = "#2c6e8f"   # positive / support edge
NEG_C = "#c0392b"   # negative / thwart edge
NODE_FILL = {
    "eco": "#dbe9f1", "mech": "#e8e2f0", "iface": "#f3e6d6",
    "person": "#f6d4d0", "root": "#cfe3d6",
}

SHORT = {
    "SYS": "Systems /\nenvironment",
    "MICRO": "Micro-\nsystem", "MESO": "Meso-\nsystem", "EXO": "Exo-\nsystem",
    "MACRO": "Macro-\nsystem", "CHRONO": "Chrono-\nsystem",
    "BOUNDARY": "Person-env.\nboundary",
    "FAM": "Family /\nhousehold", "SCHWORK": "School /\nwork", "PEER": "Peer /\ncommunity",
    "LINK_XS": "Cross-setting\nlinkages",
    "ECON_LOCAL": "Caregiver\neconomy", "SERV": "Service &\nhealth systems",
    "MEDIA": "Media /\ninformation", "GOV_LOCAL": "Local\ngovernance",
    "STATE": "State / law\n& policy", "MAC_ECON": "Economic\nsystem",
    "INEQ": "Socioeconomic\ninequality", "CULT": "Culture /\nideology",
    "FEEDBACK": "Feedback /\ncircular\ncausality", "COUPLING": "Structural\ncoupling",
    "PROX_PROC": "Proximal\nprocesses", "SOC_DETERM": "Social-determinant\ntransduction",
    "LEVERAGE": "Leverage\npoints",
    "PERSON_IF": "PERSON\n(mother node)", "NEEDS_IF": "Needs\ninterface",
    "ME_IF": "Motivation-\nemotion iface", "DEV_IF": "Development\ninterface",
    "DIS_IF": "Psychopathology\ninterface", "THER_IF": "Therapy\ninterface",
}


def _class(nid):
    if nid == "PERSON_IF":
        return "person"
    if nid == "SYS":
        return "root"
    if nid.endswith("_IF"):
        return "iface"
    if nid in ("FEEDBACK", "COUPLING", "PROX_PROC", "SOC_DETERM", "LEVERAGE"):
        return "mech"
    return "eco"


def _arrow(ax, p0, p1, color, lw, ls="-", rad=0.12, alpha=0.9, z=1):
    a = FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                        arrowstyle="-|>", mutation_scale=11, lw=lw,
                        color=color, ls=ls, alpha=alpha, zorder=z,
                        shrinkA=17, shrinkB=17)
    ax.add_patch(a)


def _node(ax, xy, nid, w=1.35, h=0.9, fs=8):
    fc = NODE_FILL[_class(nid)]
    box = mpatches.FancyBboxPatch((xy[0] - w / 2, xy[1] - h / 2), w, h,
                                  boxstyle="round,pad=0.02,rounding_size=0.14",
                                  fc=fc, ec="#333333", lw=1.1, zorder=5)
    ax.add_patch(box)
    ax.text(xy[0], xy[1], SHORT.get(nid, nid), ha="center", va="center",
            fontsize=fs, zorder=6)


# --------------------------------------------------------------- Figure H1
def figH1():
    pos = {
        "SYS": (0.0, 8.4),
        "MACRO": (-7.6, 6.2), "EXO": (-7.6, 3.2), "MESO": (-7.6, 0.3),
        "MICRO": (-3.4, 0.3),
        "CHRONO": (7.6, 6.2), "BOUNDARY": (3.6, 2.0),
        # macro facets
        "STATE": (-11.0, 8.0), "MAC_ECON": (-11.0, 6.2),
        "INEQ": (-11.0, 4.4), "CULT": (-11.0, 2.6),
        # exo facets
        "ECON_LOCAL": (-11.0, 0.9), "SERV": (-8.9, -1.7),
        "MEDIA": (-11.0, -0.9), "GOV_LOCAL": (-6.6, -1.9),
        # micro facets
        "FAM": (-3.4, -2.2), "SCHWORK": (-0.7, -2.2), "PEER": (-5.9, -2.4),
        "LINK_XS": (-7.6, -2.2),
        # mechanisms
        "FEEDBACK": (-1.2, 1.9), "COUPLING": (3.9, -0.6),
        "PROX_PROC": (0.6, 0.4), "SOC_DETERM": (-4.6, 3.6), "LEVERAGE": (-2.4, 5.2),
        # interfaces / person
        "PERSON_IF": (2.0, -3.0),
        "NEEDS_IF": (6.6, -2.6), "ME_IF": (8.7, -0.7), "DEV_IF": (9.2, 2.2),
        "DIS_IF": (-1.2, -4.4), "THER_IF": (3.2, 6.6),
    }
    fig, ax = plt.subplots(figsize=(15.5, 12.0))
    wmax = edges.weight.max()
    for _, e in edges.iterrows():
        s, t = e["source"], e["target"]
        if s not in pos or t not in pos:
            continue
        color = POS_C if e["sign"] == "+" else NEG_C
        lw = 0.8 + 3.0 * (e["weight"] / wmax)
        ls = "-" if e["gate"] == "none" else (0, (5, 2))
        if s == t:  # self-loop
            x, y = pos[s]
            loop = mpatches.FancyArrowPatch(
                (x - 0.35, y + 0.45), (x + 0.35, y + 0.45),
                connectionstyle="arc3,rad=3.4", arrowstyle="-|>",
                mutation_scale=10, lw=lw, color=color, zorder=2)
            ax.add_patch(loop)
            continue
        rad = 0.14
        _arrow(ax, pos[s], pos[t], color, lw, ls=ls, rad=rad, alpha=0.85)
    for nid, xy in pos.items():
        big = nid in ("PERSON_IF", "SYS")
        _node(ax, xy, nid, w=1.7 if big else 1.42, h=1.02 if big else 0.92,
              fs=8.5 if big else 7.7)
    # legend
    leg = [
        Line2D([0], [0], color=POS_C, lw=3, label="Supporting / positive edge"),
        Line2D([0], [0], color=NEG_C, lw=3, label="Thwarting / negative edge"),
        Line2D([0], [0], color="#555", lw=2, ls=(0, (5, 2)), label="Gated edge (developmental / situational / historical)"),
        mpatches.Patch(fc=NODE_FILL["eco"], ec="#333", label="Ecological system / setting"),
        mpatches.Patch(fc=NODE_FILL["mech"], ec="#333", label="Systemic mechanism"),
        mpatches.Patch(fc=NODE_FILL["iface"], ec="#333", label="Interface to another stratum"),
        mpatches.Patch(fc=NODE_FILL["person"], ec="#333", label="Person (mother node)"),
    ]
    ax.legend(handles=leg, loc="lower left", fontsize=8.5, framealpha=0.95,
              bbox_to_anchor=(0.005, 0.005))
    ax.set_xlim(-12.6, 10.6)
    ax.set_ylim(-5.6, 9.4)
    ax.axis("off")
    ax.set_title("Figure H1. The Universal Systems Graph (USysG): the person as an autopoietic unity "
                 "nested in coupled environmental systems",
                 fontsize=11.5, pad=10)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "figH1_universal_systems_graph.png"), dpi=200,
                bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------- Figure H2
def figH2():
    theories = [
        "General Systems Theory\n(von Bertalanffy; Laszlo)",
        "Cybernetics\n(Wiener; Lalande)",
        "Autopoiesis\n(Maturana & Varela)",
        "Ecological systems\n(Bronfenbrenner)",
        "Family systems / Milan\n(Selvini Palazzoli)",
        "Structural-strategic\n(Szapocznik BSFT)",
        "Systems for global MH\n(Jordans)",
        "Social determinants\n(Mani; Siegel; Dickerson)",
    ]
    comps = ["Nested\nhierarchy", "Feedback /\ncircularity", "Autopoietic\nboundary",
             "Proximal\nprocesses", "Homeostasis /\nprior", "Leverage /\nintervention",
             "Social-determinant\ntransduction"]
    # 1 = central, 0.5 = partial/implicit, 0 = absent
    M = np.array([
        [1.0, 1.0, 0.5, 0.0, 0.5, 0.5, 0.0],  # GST
        [0.5, 1.0, 0.5, 0.0, 1.0, 0.0, 0.0],  # cybernetics
        [0.5, 0.5, 1.0, 0.5, 0.5, 0.0, 0.0],  # autopoiesis
        [1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5],  # ecological
        [0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.0],  # Milan
        [0.5, 1.0, 0.0, 0.5, 1.0, 1.0, 0.0],  # BSFT
        [1.0, 1.0, 0.0, 0.0, 0.5, 1.0, 0.5],  # Jordans
        [0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 1.0],  # social determinants
    ])
    fig, ax = plt.subplots(figsize=(11.5, 8.2))
    ax.imshow(M, cmap="BuPu", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(comps)))
    ax.set_xticklabels(comps, fontsize=8.2)
    ax.set_yticks(range(len(theories)))
    ax.set_yticklabels(theories, fontsize=8.4)
    for i in range(len(theories)):
        for j in range(len(comps)):
            v = M[i, j]
            lab = {1.0: "●", 0.5: "◐", 0.0: "–"}[v]
            ax.text(j, i, lab, ha="center", va="center",
                    color="#222" if v < 0.75 else "white", fontsize=12)
    ax.set_xticks(np.arange(-.5, len(comps), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(theories), 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.5)
    ax.tick_params(which="minor", length=0)
    ax.set_title("Figure H2. Convergence across systems theories: each theory's constructs mapped onto "
                 "the seven USysG components\n(● central   ◐ partial/implicit   – absent)",
                 fontsize=10.5, pad=10)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "figH2_theory_construct_mapping.png"), dpi=200,
                bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------- Figure H3
def figH3():
    """The social-determinant cascade: how macro structure becomes individual outcome."""
    fig, ax = plt.subplots(figsize=(13.0, 7.4))
    layers = {
        "STATE": (1.2, 6.0, "State policy\n(police & parens patriae)"),
        "MAC_ECON": (1.2, 3.4, "Economic system /\nresource distribution"),
        "INEQ": (1.2, 0.8, "Socioeconomic\ninequality gradient"),
        "SOC_DETERM": (5.6, 3.4, "Social-determinant\ntransduction\n(scarcity, cognitive load,\nfood insecurity, stress)"),
        "PERSON_IF": (10.4, 5.2, "Cognitive function\n(≈ 13 IQ-equiv. points;\ncumulative in early childhood)"),
        "ME_IF": (10.4, 3.4, "Appraisal / attention\ncaptured by scarcity"),
        "NEEDS_IF": (10.4, 1.6, "Existence & safety\nneeds frustrated"),
        "DIS_IF": (10.4, -0.4, "Environmental\ndisorder prior"),
    }
    for nid, (x, y, lab) in layers.items():
        cls = _class(nid)
        fc = NODE_FILL[cls]
        w, h = (2.5, 1.5) if nid in ("SOC_DETERM",) else (2.4, 1.2)
        if nid == "PERSON_IF":
            w, h = 2.7, 1.4
        box = mpatches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                      boxstyle="round,pad=0.03,rounding_size=0.12",
                                      fc=fc, ec="#333", lw=1.2, zorder=5)
        ax.add_patch(box)
        ax.text(x, y, lab, ha="center", va="center", fontsize=8.2, zorder=6)
    cascade = [
        ("STATE", "INEQ", NEG_C, "policy raises/\nlowers gradient"),
        ("STATE", "SOC_DETERM", POS_C, ""),
        ("MAC_ECON", "SOC_DETERM", POS_C, ""),
        ("INEQ", "SOC_DETERM", POS_C, ""),
        ("SOC_DETERM", "PERSON_IF", NEG_C, "impedes\ncognition"),
        ("SOC_DETERM", "ME_IF", NEG_C, "captures\nappraisal"),
        ("SOC_DETERM", "NEEDS_IF", NEG_C, "frustrates\nneeds"),
        ("SOC_DETERM", "DIS_IF", NEG_C, "disorder\nprior"),
    ]
    for s, t, c, lab in cascade:
        x0, y0 = layers[s][0], layers[s][1]
        x1, y1 = layers[t][0], layers[t][1]
        _arrow(ax, (x0, y0), (x1, y1), c, 2.4, rad=0.06, alpha=0.9)
    # buffering annotation
    ax.annotate("Supportive lower systems (family, peers, services) enter PERSON with a positive sign\n"
                "and sum against these negative edges (signed superposition — Axiom 5): the model of resilience.",
                xy=(6.2, -1.6), ha="center", fontsize=8.4, style="italic",
                bbox=dict(boxstyle="round,pad=0.4", fc="#eef4ee", ec="#88a"))
    ax.set_xlim(-0.4, 12.3)
    ax.set_ylim(-2.6, 7.3)
    ax.axis("off")
    ax.set_title("Figure H3. The social-determinant cascade: how macro-structural conditions are transduced "
                 "into individual functioning",
                 fontsize=11, pad=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "figH3_social_determinant_cascade.png"), dpi=200,
                bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------- Figure H4
def figH4():
    """Nested ecological topology: concentric systems around the person."""
    fig, ax = plt.subplots(figsize=(10.5, 10.5))
    rings = [
        (9.2, "#eef3f7", "MACROSYSTEM  —  economy, state & law, inequality, culture"),
        (7.1, "#dce8f0", "EXOSYSTEM  —  caregiver economy, services, media, governance"),
        (5.1, "#c4d9e6", "MESOSYSTEM  —  linkages among settings"),
        (3.2, "#a9c9dc", "MICROSYSTEM  —  family, school/work, peers"),
    ]
    for r, c, lab in rings:
        ax.add_patch(Circle((0, 0), r, fc=c, ec="#4a6b82", lw=1.3, zorder=1))
        ax.text(0, r - 0.42, lab, ha="center", va="center", fontsize=8.3,
                color="#20303a", zorder=3)
    # person core
    ax.add_patch(Circle((0, 0), 1.5, fc=NODE_FILL["person"], ec="#333", lw=1.6, zorder=4))
    ax.text(0, 0, "PERSON\n(autopoietic\nunity)", ha="center", va="center",
            fontsize=9.5, zorder=5)
    # microsystem settings as small nodes
    micro = {"Family": (-1.7, 1.7), "School /\nwork": (1.9, 1.5), "Peers": (0.0, -2.4)}
    for lab, (x, y) in micro.items():
        ax.add_patch(Circle((x, y), 0.72, fc="#f4ede2", ec="#555", lw=1.0, zorder=6))
        ax.text(x, y, lab, ha="center", va="center", fontsize=7.3, zorder=7)
    # chronosystem arrow (time)
    ax.annotate("", xy=(9.6, -8.6), xytext=(-9.6, -8.6),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#666"))
    ax.text(0, -9.35, "CHRONOSYSTEM  —  ecological transitions, life-course and historical time",
            ha="center", fontsize=8.5, color="#444")
    # structural-coupling double arrow through the rings
    ax.annotate("", xy=(0.0, 1.55), xytext=(0.0, 9.1),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.8, color=NEG_C, alpha=0.55))
    ax.text(0.35, 6.0, "structural\ncoupling\n(bidirectional)", fontsize=7.6,
            color=NEG_C, rotation=90, va="center")
    ax.set_xlim(-10.2, 10.2)
    ax.set_ylim(-10.0, 10.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Figure H4. The nested ecological topology: the person at the centre of concentric, "
                 "mutually coupled systems in time",
                 fontsize=10.8, pad=6)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "figH4_nested_ecological_topology.png"), dpi=200,
                bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    figH1()
    figH2()
    figH3()
    figH4()
    print("Figures written to", FIGS)
