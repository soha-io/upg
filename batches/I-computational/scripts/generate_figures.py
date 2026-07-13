"""
Batch I — figure generation.
Produces four PNGs used in the manuscript. All numerical content is
reproduced from verify_math.py so figures and text agree.
Run: python3 generate_figures.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                     "axes.titlesize": 12, "figure.dpi": 150})

INK, SUP, THW, MUT = "#1a1a2e", "#1f6f54", "#b02a37", "#8a8a99"
ACC = "#274b8f"

# ---------------------------------------------------------------------------
# FIG I1 — the three-level architecture of computational/mathematical psychology
# ---------------------------------------------------------------------------
def fig1():
    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.set_title("The formal turn: levels of computational & mathematical psychology",
                 weight="bold", pad=12)

    levels = [
        (7.9, "Biophysical / circuit models", SUP,
         "synapses, neurons, microcircuits\n(Anticevic & Murray 2018, ch.1–4)"),
        (5.9, "Connectionist / neural-systems models", ACC,
         "large-scale networks, distributed representation\n(Rumelhart & McClelland; ch.5–7)"),
        (3.9, "Algorithmic / cognitive models", "#7a4fb0",
         "reinforcement learning, Bayesian inference,\ndrift-diffusion (ch.8–11; Moutoussis 2017)"),
        (1.9, "Formal-theory constructions", "#c1622d",
         "stochastic models, axiomatic method,\nfunctional equations (Batchelder 2010)"),
    ]
    for y, name, col, sub in levels:
        box = FancyBboxPatch((0.6, y-0.7), 6.7, 1.4, boxstyle="round,pad=0.05,rounding_size=0.12",
                             fc=col, ec="none", alpha=0.16, zorder=1)
        ax.add_patch(box)
        ax.text(0.95, y+0.28, name, weight="bold", color=col, fontsize=11, va="center")
        ax.text(0.98, y-0.34, sub, fontsize=8.4, color=INK, va="center")

    # vertical "abstraction" axis
    ax.annotate("", xy=(0.35, 8.7), xytext=(0.35, 1.1),
                arrowprops=dict(arrowstyle="-|>", color=MUT, lw=1.6))
    ax.text(0.05, 8.9, "more\nabstract", fontsize=8, color=MUT, ha="center")
    ax.text(0.05, 0.8, "more\nbiophysical", fontsize=8, color=MUT, ha="center")

    # right column: the unifying formal objects
    ax.text(8.7, 8.7, "Shared formal objects", weight="bold", ha="center", color=INK)
    objs = ["state vector  x(t)", "weighted matrix  W", "graph Laplacian  L = D − W",
            "operator / map  x₁ = σ(Bx+…)", "belief / value updates"]
    for i, o in enumerate(objs):
        yy = 7.9 - i*1.15
        b = FancyBboxPatch((7.75, yy-0.36), 1.95, 0.72, boxstyle="round,pad=0.03,rounding_size=0.1",
                           fc="white", ec=ACC, lw=1.3, zorder=2)
        ax.add_patch(b)
        ax.text(8.72, yy, o, fontsize=8.3, ha="center", va="center", color=INK)
    # bracket linking levels to objects
    ax.annotate("", xy=(7.72, 4.55), xytext=(7.5, 4.55),
                arrowprops=dict(arrowstyle="-|>", color=MUT, lw=1.4))
    ax.text(7.32, 5.6, "one\nformalism", fontsize=7.6, color=MUT, ha="center")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figI1_formal_levels.png"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG I2 — worked spectral example: 6-node graph, Fiedler partition + embedding
# ---------------------------------------------------------------------------
def fig2():
    A = np.zeros((6,6))
    edges = {(0,1):0.9,(0,2):0.8,(1,2):0.7,(3,4):0.9,(4,5):0.8,(3,5):0.7,(2,3):0.2}
    for (i,j),w in edges.items(): A[i,j]=w; A[j,i]=w
    D = np.diag(A.sum(1)); L = D - A
    evals, evecs = np.linalg.eigh(L)
    v2 = evecs[:,1];  v2 = -v2 if v2[0]>0 else v2
    v3 = evecs[:,2]

    pos = {0:(-1.6,1.0),1:(-2.1,-0.1),2:(-1.0,-0.9),
           3:(1.0,-0.9),4:(2.1,-0.1),5:(1.6,1.0)}
    labels = {0:"n1",1:"n2",2:"n3",3:"n4",4:"n5",5:"n6"}

    fig, (axg, axe) = plt.subplots(1,2, figsize=(11,4.9),
                                   gridspec_kw={"width_ratios":[1.15,1]})
    axg.set_title("(a) weighted graph, Fiedler partition", weight="bold")
    axg.set_xlim(-3,3); axg.set_ylim(-1.9,1.9); axg.axis("off")
    for (i,j),w in edges.items():
        lw = 1+6*w
        col = MUT if w<0.3 else MUT if (i,j)==(2,3) else "#5a5a6e"
        axg.plot(*zip(pos[i],pos[j]), color=("#c98a2e" if (i,j)==(2,3) else "#8a8a99"),
                 lw=lw, zorder=1, solid_capstyle="round")
    for n,(px,py) in pos.items():
        col = SUP if v2[n]<0 else ACC
        axg.add_patch(Circle((px,py),0.34, fc=col, ec="white", lw=2, zorder=3, alpha=0.9))
        axg.text(px,py,labels[n], color="white", ha="center", va="center",
                 weight="bold", fontsize=10, zorder=4)
    axg.text(-1.55,1.65,"community A", color=SUP, ha="center", fontsize=9, weight="bold")
    axg.text(1.55,1.65,"community B", color=ACC, ha="center", fontsize=9, weight="bold")
    axg.text(0,-1.55,"bridge edge w=0.2 (n3–n4)", color="#c98a2e", ha="center", fontsize=8.5)

    axe.set_title("(b) spectral embedding  φ(i)=(v₂,v₃)", weight="bold")
    for n in range(6):
        col = SUP if v2[n]<0 else ACC
        axe.scatter(v2[n], v3[n], s=180, color=col, zorder=3, edgecolor="white", lw=1.5)
        axe.annotate(labels[n], (v2[n],v3[n]), textcoords="offset points",
                     xytext=(8,4), fontsize=9, color=INK)
    axe.axvline(0, color=MUT, ls="--", lw=1); axe.axhline(0, color=MUT, ls=":", lw=0.8)
    axe.set_xlabel("Fiedler coordinate  v₂  (λ₂ = 0.119)")
    axe.set_ylabel("v₃")
    axe.text(0.02,0.97,"sign(v₂) splits the two communities;\n|v₂| smallest at bridge node n3",
             transform=axe.transAxes, va="top", fontsize=8.2, color=INK,
             bbox=dict(boxstyle="round", fc="white", ec=MUT, alpha=0.9))
    axe.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figI2_spectral_example.png"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG I3 — dynamical systems: phase portrait (stable) + bifurcation of a loop gain
# ---------------------------------------------------------------------------
def fig3():
    fig, (axp, axb) = plt.subplots(1,2, figsize=(11,4.9))

    # (a) phase portrait of x_{t+1}=B x + b  (stable node, rho=0.727)
    B = np.array([[0.5,0.4],[0.3,0.2]]); b=np.array([0.1,0.2])
    xstar = np.linalg.solve(np.eye(2)-B, b)
    xs = np.linspace(-0.4,1.2,18); ys = np.linspace(-0.4,1.0,18)
    X,Y = np.meshgrid(xs,ys)
    U = (B[0,0]-1)*X + B[0,1]*Y + b[0]
    Vv= B[1,0]*X + (B[1,1]-1)*Y + b[1]
    axp.set_title("(a) phase portrait: convergence to a fixed point", weight="bold")
    axp.streamplot(X,Y,U,Vv, color="#8a8a99", density=1.0, linewidth=0.8, arrowsize=0.9)
    for x0 in [(-0.3,0.9),(1.1,-0.3),(1.1,0.9),(-0.3,-0.3)]:
        xt=np.array(x0,float); tr=[xt.copy()]
        for _ in range(40): xt=B@xt+b; tr.append(xt.copy())
        tr=np.array(tr); axp.plot(tr[:,0],tr[:,1], color=ACC, lw=1.5, alpha=0.8)
    axp.scatter(*xstar, s=170, color=MUT, zorder=5, edgecolor="white", lw=1.6)
    axp.annotate("attractor x*=(0.571,0.464)", xstar, textcoords="offset points",
                 xytext=(-30,-22), fontsize=8.6, color=MUT, weight="bold")
    axp.set_xlabel("x₁  (e.g. rumination)"); axp.set_ylabel("x₂  (e.g. insomnia)")

    # (b) bifurcation: as a symmetric loop gain g rises, x*=tanh(g*x*) splits
    axb.set_title("(b) pitchfork bifurcation of a self-maintaining loop", weight="bold")
    gs = np.linspace(0,2.5,400)
    def fixed_pts(g):
        # solve x = tanh(g x); x=0 always; nonzero branch by iteration if g>1
        roots=[0.0]
        if g>1.0:
            x=0.5
            for _ in range(200): x=np.tanh(g*x)
            if x>1e-4: roots += [x,-x]
        return roots
    for g in gs:
        for r in fixed_pts(g):
            stable = (g*(1-np.tanh(g*r)**2) < 1)   # |f'(x*)|<1
            axb.plot(g, r, ".", ms=2.2,
                     color=(SUP if stable else THW))
    axb.axvline(1.0, color=MUT, ls="--", lw=1)
    axb.text(1.03,0.9,"critical gain g=1\n(bifurcation)", fontsize=8.2, color=MUT)
    axb.text(1.7,0.62,"stable 'disorder'\nattractors", fontsize=8.4, color=SUP)
    axb.text(1.35,0.03,"unstable branch", fontsize=8, color=THW)
    axb.set_xlabel("loop gain  g"); axb.set_ylabel("fixed point  x*")
    axb.set_ylim(-1.05,1.05); axb.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figI3_dynamics_bifurcation.png"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG I4 — mapping the toolbox onto the eight-stratum modelling needs
# ---------------------------------------------------------------------------
def fig4():
    tools = ["vector\nx(t)", "signed matrix\nW", "Laplacian\nspectrum", "iterated map\nσ(Bx+…)",
             "Bayesian /\nRL update", "measurement\n& selection"]
    needs = ["encode a person's\nmomentary state",
             "signed, weighted\ninfluence (Axiom 5)",
             "latent axes,\ncommunities, bridges",
             "movement, loops,\nattractors, control",
             "how history &\ntherapy re-weight edges",
             "reliability, validity,\noverfitting control"]
    # which tool primarily serves which need (diagonal) + secondary links
    M = np.array([
        [2,1,0,1,0,0],
        [1,2,1,1,0,0],
        [0,1,2,1,0,0],
        [1,1,1,2,1,0],
        [0,1,0,1,2,1],
        [0,0,1,0,1,2],
    ])
    fig, ax = plt.subplots(figsize=(8.6,6.4))
    im = ax.imshow(M, cmap="BuPu", vmin=0, vmax=2, aspect="auto")
    ax.set_xticks(range(6)); ax.set_yticks(range(6))
    ax.set_xticklabels(needs, fontsize=8.2)
    ax.set_yticklabels(tools, fontsize=8.8, weight="bold")
    ax.set_title("How the mathematical toolbox meets the modelling needs of the UPG",
                 weight="bold", pad=12)
    for i in range(6):
        for j in range(6):
            if M[i,j]==2: ax.text(j,i,"●", ha="center", va="center", color="white", fontsize=11)
            elif M[i,j]==1: ax.text(j,i,"○", ha="center", va="center", color="#4a2d63", fontsize=9)
    ax.set_xlabel("modelling need", fontsize=9)
    ax.set_ylabel("formal tool", fontsize=9)
    plt.setp(ax.get_xticklabels(), rotation=18, ha="right")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03, ticks=[0,1,2])
    cb.ax.set_yticklabels(["none","supporting","primary"], fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figI4_toolbox_mapping.png"), bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    print("wrote:", sorted(os.listdir(OUT)))
