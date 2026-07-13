"""
Spectral graph tools (Batch I 5.3): Laplacian, its spectrum, the Fiedler
vector, and eigenvector centrality.

The functions are generic (they take a symmetric matrix); the convenience
:func:`dimension_spectral_report` wires the 8-node dimension graph through
them and reproduces Batch J Section 6 exactly.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .io import dimension_magnitude_matrix
from .registry import DIMS


def symmetrize_magnitude(W: np.ndarray) -> np.ndarray:
    """|W| with zero diagonal, symmetrized: S = (|W| + |W|^T) / 2."""
    Wm = np.abs(W).copy()
    np.fill_diagonal(Wm, 0.0)
    return (Wm + Wm.T) / 2


def laplacian(S: np.ndarray) -> np.ndarray:
    """Combinatorial Laplacian L = D - S for a symmetric weight matrix S."""
    D = np.diag(S.sum(1))
    return D - S


def normalized_laplacian(S: np.ndarray) -> np.ndarray:
    """Symmetric normalized Laplacian L_sym = I - D^{-1/2} S D^{-1/2}."""
    d = S.sum(1)
    Dinv2 = np.diag(1.0 / np.sqrt(d))
    return np.eye(S.shape[0]) - Dinv2 @ S @ Dinv2


def laplacian_spectrum(S: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Ascending eigenvalues and eigenvectors of the Laplacian of S."""
    return np.linalg.eigh(laplacian(S))


def eigenvector_centrality(S: np.ndarray) -> np.ndarray:
    """|leading eigenvector| of S, scaled so the maximum entry is 1."""
    _ew, ev = np.linalg.eigh(S)
    c = np.abs(ev[:, -1])
    return c / c.max()


@dataclass
class SpectralReport:
    eigenvalues: list[float]
    algebraic_connectivity: float
    fiedler: dict[str, float]
    partition: tuple[list[str], list[str]]
    bridge_ranking: list[tuple[str, float]]
    centrality: dict[str, float]


def dimension_spectral_report() -> SpectralReport:
    """Reproduce the spectral anatomy of the 8-node dimension graph.

    Sign convention: the Fiedler vector is oriented so that SYS is
    non-positive (matches the manuscript's reported orientation).
    """
    S = symmetrize_magnitude(dimension_magnitude_matrix())
    lam, V = laplacian_spectrum(S)
    v2 = V[:, 1]
    if v2[DIMS.index("SYS")] > 0:
        v2 = -v2

    fiedler = {d: float(val) for d, val in zip(DIMS, v2)}
    partition = ([d for d, val in zip(DIMS, v2) if val < 0],
                 [d for d, val in zip(DIMS, v2) if val >= 0])
    order = np.argsort(np.abs(v2))
    bridge = [(DIMS[i], float(abs(v2[i]))) for i in order]

    c = eigenvector_centrality(S)
    centrality = {d: float(round(v, 3))
                  for d, v in sorted(zip(DIMS, c), key=lambda t: -t[1])}

    return SpectralReport(
        eigenvalues=[float(round(x, 3)) for x in lam],
        algebraic_connectivity=float(lam[1]),
        fiedler=fiedler,
        partition=partition,
        bridge_ranking=bridge,
        centrality=centrality,
    )
