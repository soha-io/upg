"""
Dynamical-systems tools (Batch I 5.4): the iterated map, fixed points,
Jacobian spectral radius (local stability), the critical coupling of the
loop-gain bifurcation, and signed cycle (loop-gain) analysis.

All matrices follow the influence convention ``M[target, source]`` so that
``M @ x`` is the net drive arriving at each node.
"""
from __future__ import annotations

import itertools

import numpy as np


def spectral_radius(M: np.ndarray) -> float:
    return float(max(abs(np.linalg.eigvals(M))))


def iterate(B: np.ndarray, g: np.ndarray, b: np.ndarray, u: float,
            x0: np.ndarray, kappa: float, T: int = 400) -> np.ndarray:
    """Run x(t+1) = tanh(kappa * (B x + g u) + b) to (near) convergence."""
    x = x0.copy().astype(float)
    for _ in range(T):
        x = np.tanh(kappa * (B @ x + g * u) + b)
    return x


# convenience alias
fixed_point = iterate


def jacobian_rho(B: np.ndarray, g: np.ndarray, b: np.ndarray, u: float,
                 xstar: np.ndarray, kappa: float) -> float:
    """Spectral radius of the Jacobian of the tanh map at ``xstar``.

    < 1 means the fixed point is locally stable.
    """
    pre = kappa * (B @ xstar + g * u) + b
    J = (kappa * B) * (1 - np.tanh(pre) ** 2)[:, None]
    return float(max(abs(np.linalg.eigvals(J))))


def critical_coupling(B: np.ndarray) -> float:
    """kappa* = 1 / lambda_max(B): the loop-gain bifurcation threshold.

    With no standing load, the quiescent state x = 0 of the tanh map loses
    stability (pitchfork) when kappa * lambda_max(B) crosses 1.
    """
    lam_max = max(np.real(np.linalg.eigvals(B)))
    return float(1.0 / lam_max)


def signed_loops(W: np.ndarray, names: list[str],
                 lengths: tuple[int, ...] = (2, 3)) -> list[tuple[float, list[str]]]:
    """Enumerate directed cycles and their loop gains (product of edge weights).

    Positive gain = self-amplifying loop; negative = regulating loop.
    ``W[target, source]`` is the signed weight of edge source -> target.
    Each cycle is reported once (canonical rotation starting at its min index).
    """
    m = len(names)
    cycles: list[tuple[float, list[str]]] = []
    for k in lengths:
        for combo in itertools.permutations(range(m), k):
            if combo[0] != min(combo):
                continue
            gain, ok = 1.0, True
            for a, bnode in zip(combo, combo[1:] + combo[:1]):
                w = W[bnode, a]
                if w == 0:
                    ok = False
                    break
                gain *= w
            if ok:
                cycles.append((float(gain), [names[i] for i in combo]))
    return cycles
