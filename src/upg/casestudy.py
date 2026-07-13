"""
The worked case (Batch J Section 8): "Sara", a synthetic case at dimension
resolution used to demonstrate Topographic Network Diagnosis end to end.

This module owns the case-specific constants (the problem-frame coupling
matrix B, the treatment gain vector g, the standing-condition vector b, the
global coupling kappa, and the edge-surgery deltas) and provides builders so
the tests and the reproduce script share exactly one definition of the case.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dynamics import (critical_coupling, iterate, jacobian_rho,
                       signed_loops, spectral_radius)
from .registry import ENDO

# Global coupling for the worked case.
KAPPA = 0.42

# Problem-frame couplings B[target][source] (all load-increasing; protective
# content lives inside the strata subgraphs).
B_ROWS: dict[str, dict[str, float]] = {
    "TEM":  {"DEV": 0.45, "TEM": 0.45},
    "DEV":  {"TEM": 0.45, "SYS": 0.70, "DEV": 0.50},
    "PER":  {"TEM": 0.65, "DEV": 0.70, "SYS": 0.50, "PER": 0.70},
    "NEED": {"DEV": 0.50, "PER": 0.60, "ME": 0.50, "DIS": 0.45, "SYS": 0.65,
             "NEED": 0.35},
    "ME":   {"TEM": 0.60, "DEV": 0.50, "PER": 0.55, "NEED": 0.80, "SYS": 0.60,
             "ME": 0.35},
    "DIS":  {"TEM": 0.55, "DEV": 0.55, "PER": 0.60, "NEED": 0.55, "ME": 0.60,
             "SYS": 0.60, "DIS": 0.30},
    "SYS":  {"PER": 0.60, "ME": 0.55, "DIS": 0.45, "SYS": 0.50},
}
# Treatment gain vector (THER -> dims; load-reducing).
G_THER: dict[str, float] = {"DIS": -0.65, "ME": -0.65, "SYS": -0.60,
                            "TEM": -0.45, "PER": -0.40, "NEED": -0.45}
# Standing conditions: constitutionally high NA, adversity history, thwarts.
B_CASE: dict[str, float] = {"TEM": 0.35, "DEV": 0.30, "SYS": 0.30}

# DIS -> THER coupling (treatment seeking) used in the signed-loop matrix.
DIS_TO_THER = 0.70


def build_case_model() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, int]]:
    """Return (B, g, b, idx) over the seven endogenous dimensions."""
    n = len(ENDO)
    idx = {d: i for i, d in enumerate(ENDO)}
    B = np.zeros((n, n))
    for tgt, row in B_ROWS.items():
        for src, w in row.items():
            B[idx[tgt], idx[src]] = w
    g = np.zeros(n)
    for tgt, w in G_THER.items():
        g[idx[tgt]] = w
    b = np.zeros(n)
    for tgt, w in B_CASE.items():
        b[idx[tgt]] = w
    return B, g, b, idx


def effective_signed_matrix() -> tuple[np.ndarray, list[str]]:
    """8x8 case-effective signed matrix (7 endogenous dims + THER) for loops."""
    B, g, _b, idx = build_case_model()
    m = len(ENDO) + 1
    Wc = np.zeros((m, m))
    Wc[:len(ENDO), :len(ENDO)] = B
    ti = len(ENDO)
    Wc[ti, idx["DIS"]] = DIS_TO_THER      # DIS -> THER
    Wc[:len(ENDO), ti] = g                # THER -> dims
    np.fill_diagonal(Wc, 0.0)
    return Wc, ENDO + ["THER"]


def edge_surgery_model() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, int]]:
    """B and b after the consolidated structural changes of successful therapy."""
    B, g, b, idx = build_case_model()
    Bs = B.copy()
    Bs[idx["ME"], idx["NEED"]] = 0.50     # frustration -> appraisal, softened
    Bs[idx["DIS"], idx["ME"]] = 0.35      # regulation acquired
    Bs[idx["DIS"], idx["DIS"]] = 0.20     # symptom self-loop broken
    Bs[idx["NEED"], idx["SYS"]] = 0.40    # environmental thwart reduced
    Bs[idx["ME"], idx["SYS"]] = 0.35      # situational threat reduced
    bs = b.copy()
    bs[idx["SYS"]] = 0.15                 # family intervention lowers thwart
    return Bs, g, bs, idx


@dataclass
class CaseReport:
    untreated: dict[str, float]
    untreated_rho: float
    bistable: bool
    lambda_max_B: float
    kappa_star: float
    treated: dict[float, dict[str, float]]
    relapse_dis: float
    surgery: dict[str, float]
    surgery_maintained: dict[str, float]
    top_amplifying: list[tuple[float, list[str]]]
    top_regulating: list[tuple[float, list[str]]]


def case_report() -> CaseReport:
    """Reproduce the worked-case numbers of Batch J Section 8."""
    B, g, b, idx = build_case_model()
    x_lo = iterate(B, g, b, u=0.0, x0=np.zeros(7), kappa=KAPPA)
    x_hi = iterate(B, g, b, u=0.0, x0=np.ones(7), kappa=KAPPA)
    untreated = {d: float(round(v, 3)) for d, v in zip(ENDO, x_hi)}
    bistable = bool(np.max(np.abs(x_hi - x_lo)) > 1e-3)
    rho_hi = jacobian_rho(B, g, b, 0.0, x_hi, kappa=KAPPA)

    lam_max = float(max(np.real(np.linalg.eigvals(B))))
    k_crit = critical_coupling(B)

    treated: dict[float, dict[str, float]] = {}
    for u in (0.5, 0.8):
        x_tr = iterate(B, g, b, u=u, x0=x_hi, kappa=KAPPA)
        treated[u] = {d: float(round(v, 3)) for d, v in zip(ENDO, x_tr)}
    x_tr8 = iterate(B, g, b, u=0.8, x0=x_hi, kappa=KAPPA)
    x_relapse = iterate(B, g, b, u=0.0, x0=x_tr8, kappa=KAPPA)

    Bs, gs, bs, _ = edge_surgery_model()
    x_surg = iterate(Bs, gs, bs, u=0.0, x0=x_tr8, kappa=KAPPA)
    x_maint = iterate(Bs, gs, bs, u=0.3, x0=x_surg, kappa=KAPPA)

    Wc, names = effective_signed_matrix()
    loops = signed_loops(Wc, names, lengths=(2, 3))
    amp = sorted(loops, key=lambda t: -t[0])[:5]
    reg = sorted(loops, key=lambda t: t[0])[:3]

    return CaseReport(
        untreated=untreated,
        untreated_rho=float(round(rho_hi, 3)),
        bistable=bistable,
        lambda_max_B=float(round(lam_max, 3)),
        kappa_star=float(round(k_crit, 3)),
        treated={u: v for u, v in treated.items()},
        relapse_dis=float(round(x_relapse[idx["DIS"]], 3)),
        surgery={d: float(round(v, 3)) for d, v in zip(ENDO, x_surg)},
        surgery_maintained={d: float(round(v, 3)) for d, v in zip(ENDO, x_maint)},
        top_amplifying=[(round(gp, 3), p) for gp, p in amp],
        top_regulating=[(round(gp, 3), p) for gp, p in reg],
    )
