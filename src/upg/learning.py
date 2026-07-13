"""
Learning updates (Batch I 5.5): Bayesian belief update and the
temporal-difference value update.

These are how the developmental stratum writes the weights and the therapy
stratum rewrites them.  Kept deliberately small and exact so the worked
examples in the manuscript reproduce to the printed digits.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BetaUpdate:
    a0: float
    b0: float
    a1: float
    b1: float
    prior_mean: float
    posterior_mean: float
    shift: float


def beta_update(a0: float, b0: float, successes: int, failures: int) -> BetaUpdate:
    """Conjugate Beta update for a probability belief (behavioural experiment).

    ``successes`` are confirming events, ``failures`` disconfirming ones.
    """
    a1, b1 = a0 + successes, b0 + failures
    prior_mean = a0 / (a0 + b0)
    posterior_mean = a1 / (a1 + b1)
    return BetaUpdate(a0, b0, a1, b1, prior_mean, posterior_mean,
                      prior_mean - posterior_mean)


def td_update(v_state: float, v_next: float, alpha: float, gamma: float,
              reward: float = 0.0, trials: int = 6) -> list[float]:
    """Temporal-difference value trajectory over repeated visits.

    V(s) <- V(s) + alpha * (r + gamma V(s') - V(s)).  With ``v_next`` held at
    the safe value, this is extinction of a cached fear value (exposure);
    if the state is never visited (avoidance) the value never updates.
    """
    values: list[float] = []
    v = float(v_state)
    for _ in range(trials):
        delta = reward + gamma * v_next - v
        v += alpha * delta
        values.append(v)
    return values
