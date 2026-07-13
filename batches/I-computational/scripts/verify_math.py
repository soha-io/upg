"""
Batch I — verification of every worked numerical example in the manuscript.
Each block prints the exact numbers quoted in the text so a reviewer can
reproduce them. Run: python3 verify_math.py
"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)

def head(t): print("\n" + "=" * 8 + " " + t + " " + "=" * 8)

# ---------------------------------------------------------------------------
head("EX 1 — signed superposition: influence as a matrix-vector product")
# Three nodes: 1=rumination, 2=insomnia, 3=social contact (protective).
# Row i = influences arriving AT node i from node j (column j).
W = np.array([
    [0.0,  0.6, -0.4],   # rumination gets +0.6 from insomnia, -0.4 from social
    [0.5,  0.0, -0.3],   # insomnia gets +0.5 from rumination, -0.3 from social
    [-0.2, -0.1, 0.0],   # social contact mildly pushed down by rumination/insomnia
])
x = np.array([0.8, 0.6, 0.3])           # current activations
drive = W @ x                            # net incoming drive at each node
print("W =\n", W)
print("x =", x)
print("net drive W@x =", drive)          # signed superposition (Axiom 5)
# contribution of node 2 (insomnia) to node 1 (rumination):
print("p_12 = W[0,1]*x[1] =", W[0,1]*x[1])
print("protective p_13 = W[0,2]*x[2] =", W[0,2]*x[2])

# ---------------------------------------------------------------------------
head("EX 2 — Laplacian & Fiedler vector of an UNDIRECTED weighted graph")
# Symmetrised 6-node graph: two loose communities {0,1,2} and {3,4,5}
# joined by one weak bridge edge (2-3). Positive weights only (couplings).
A = np.zeros((6, 6))
edges = {(0,1):0.9,(0,2):0.8,(1,2):0.7,      # community A
         (3,4):0.9,(4,5):0.8,(3,5):0.7,      # community B
         (2,3):0.2}                          # bridge
for (i,j),w in edges.items():
    A[i,j]=w; A[j,i]=w
D = np.diag(A.sum(1))
L = D - A
print("degree diag(D) =", np.diag(D))
evals, evecs = np.linalg.eigh(L)             # symmetric -> eigh, sorted asc
print("Laplacian eigenvalues =", evals)
print("lambda_1 (should be ~0) =", evals[0])
print("lambda_2 algebraic connectivity =", evals[1])
fiedler = evecs[:,1]
# sign convention: make first entry negative for readability
if fiedler[0] > 0: fiedler = -fiedler
print("Fiedler vector v2 =", fiedler)
print("sign(v2) partition =", np.sign(fiedler).astype(int))
# node with smallest |v2| = closest to the fault line (bridge)
print("|v2| per node =", np.abs(fiedler))
print("bridge node (argmin |v2|) =", int(np.argmin(np.abs(fiedler))))

# normalized Laplacian check
d = A.sum(1); Dinv2 = np.diag(1/np.sqrt(d))
Lsym = np.eye(6) - Dinv2 @ A @ Dinv2
ev_sym = np.linalg.eigvalsh(Lsym)
print("normalized-Laplacian eigenvalues =", ev_sym)

# ---------------------------------------------------------------------------
head("EX 3 — linear dynamical system: fixed point, Jacobian, stability")
# x_{t+1} = B x_t + b   (linear; sigma = identity)
B = np.array([[0.5, 0.4],
              [0.3, 0.2]])
b = np.array([0.1, 0.2])
# fixed point x* = (I-B)^{-1} b
xstar = np.linalg.solve(np.eye(2)-B, b)
print("B =\n", B, "\nb =", b)
print("fixed point x* =", xstar)
# Jacobian of a linear map is B itself; stability <=> spectral radius < 1
eigB = np.linalg.eigvals(B)
rho = max(abs(eigB))
print("eig(B) =", eigB, " spectral radius rho =", round(rho,4),
      "-> stable" if rho < 1 else "-> unstable")
# simulate to confirm convergence
xt = np.array([0.0,0.0])
for _ in range(60):
    xt = B@xt + b
print("simulated limit =", xt, " matches x*?", np.allclose(xt, xstar))

head("EX 3b — a self-sustaining (unstable) coupling -> disorder attractor")
# Strengthen the loop so rho>1: illustrates Borsboom alternative-stable-state
B2 = np.array([[0.7, 0.6],
               [0.7, 0.5]])
eig2 = np.linalg.eigvals(B2); rho2 = max(abs(eig2))
print("eig(B2) =", eig2, " rho =", round(rho2,4),
      "-> runs away (needs saturating sigma to bound)" if rho2>1 else "")
# with a saturating nonlinearity tanh the runaway becomes a bounded attractor
def sigma(v): return np.tanh(v)
xt = np.array([0.05,0.05]); traj=[xt.copy()]
for _ in range(200):
    xt = sigma(B2@xt); traj.append(xt.copy())
print("bounded attractor with tanh =", np.round(xt,4))

# ---------------------------------------------------------------------------
head("EX 4 — Bayesian belief update (behavioural experiment, CBT)")
# Prior belief 'coffee-shop patrons are well-dressed & will mock me'
# Model as Beta prior over p=Pr(mocked); observe casually-dressed, no mockery.
# Beta(a,b): a=prior 'confirmations', b=prior 'disconfirmations'
a0, b0 = 8, 2                 # strong prior p~0.8
# Susie observes 20 patrons, 0 mockery events (all disconfirming)
succ, fail = 0, 20
a1, b1 = a0+succ, b0+fail
mean0 = a0/(a0+b0); mean1 = a1/(a1+b1)
print(f"prior  Beta({a0},{b0}) mean Pr(mock) = {mean0:.3f}")
print(f"posterior Beta({a1},{b1}) mean Pr(mock) = {mean1:.3f}")
print(f"belief shift = {mean0-mean1:.3f}")

# ---------------------------------------------------------------------------
head("EX 5 — temporal-difference (RL) value update (avoidance/exposure)")
# V(s) <- V(s) + alpha * (r + gamma V(s') - V(s))
# Prior avoidance learning has cached a strong NEGATIVE value on the feared
# state s2. Exposure-with-response-prevention repeatedly visits s2 -> safe
# with reward 0 and no harm, so the negative value EXTINGUISHES toward 0.
alpha, gamma = 0.3, 0.9
V_safe = 0.0
V_s2 = -0.8                 # cached fear value from earlier avoidance
vals = []
for k in range(6):
    delta = 0 + gamma*V_safe - V_s2      # prediction error
    V_s2 += alpha*delta
    vals.append(round(V_s2, 4))
print("V(s2) after each exposure trial:", vals)
print("extinction: value moved from -0.8 toward 0")
# Avoidance case: the agent jumps out before reaching s2, so s2 is never
# sampled, its prediction error is never generated, and the fear persists.
print("avoided-state value stays fixed at -0.8 (never sampled -> no extinction)")

# ---------------------------------------------------------------------------
head("EX 6 — spectral embedding coordinates (learned clinical axes)")
# project a synthetic state onto the first two nontrivial Laplacian modes
Vm = evecs[:, 1:3]                        # v2, v3
state = np.array([0.9,0.5,0.7,0.1,0.0,0.2])   # graded, mostly community-A
z = Vm.T @ state
print("state =", state)
print("embedding z = Vm^T x =", z)

print("\nAll blocks executed.")
