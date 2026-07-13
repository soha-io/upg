"""
Step 2 of the estimation roadmap: a generative simulator of synthetic persons.

The simulator is the *ground truth we control*.  It samples a person-specific
structure by perturbing the consensus prior, runs the iterated map with process
noise to produce true latent trajectories, and emits realistic EMA-style
observations (measurement noise, sampling compliance, dropout).  Every
generative quantity — the person's coupling matrix ``B``, standing conditions
``b``, coupling ``kappa``, and the true states — is retained so that Step 3
(method recovery) can score an estimator against known answers.

Design choices that make the output invertible in principle:
  * **Structure is fixed from theory (rule W1).**  Perturbation is
    multiplicative on the *existing* edges only; zero entries stay zero, signs
    are preserved.  A recovered structure can therefore be compared to a known
    sparse ground truth rather than a dense free matrix.
  * **One resolution by default.**  The population is generated at the
    dimension level (7 endogenous dimensions + THER as control), where a 7x7
    ``B`` is identifiable from moderate-length series.  The core functions take
    an arbitrary ``B, g, b, kappa`` and so extend to full resolution.

Map (matching Batch J Section 8):
    x(t+1) = tanh( kappa * (B x(t) + g u(t)) + b + eps(t) )
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field

import numpy as np

from .casestudy import KAPPA, build_case_model
from .dynamics import critical_coupling, iterate, jacobian_rho
from .registry import ENDO

# ==========================================================================
# Ground-truth person and dataset containers
# ==========================================================================


@dataclass
class PersonParams:
    """The generative parameters (ground truth) for one synthetic person."""
    person_id: str
    dims: list[str]
    B: np.ndarray            # (n, n) coupling, B[target, source]
    g: np.ndarray            # (n,) treatment gain vector
    b: np.ndarray            # (n,) standing conditions
    kappa: float
    age: float = 35.0
    # derived labels (filled by characterize)
    kappa_star: float = float("nan")
    regime: str = ""
    attractor_dis: float = float("nan")
    rho: float = float("nan")


@dataclass
class PersonRecord:
    """One simulated person: ground truth + true states + messy observations."""
    params: PersonParams
    states: np.ndarray       # (T, n) true latent states
    observations: np.ndarray  # (T, n) with NaN where missing
    u: np.ndarray            # (T,) treatment intensity applied
    observed: np.ndarray     # (T,) bool, occasion-level compliance
    dropout_time: int | None


@dataclass
class SimConfig:
    """Observation / sampling parameters for the EMA-style measurement model."""
    T: int = 100                 # number of recorded occasions
    burn_in: int = 200           # discarded steps so we start near stationarity
    process_noise: float = 0.05  # sd of eps inside the map
    meas_noise: float = 0.08     # sd of observation noise
    sampling_rate: float = 0.70  # per-occasion compliance probability
    dropout_prob: float = 0.20   # probability a person drops out partway
    item_missing: float = 0.0    # optional extra per-item missingness
    seed: int = 0

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class GeneratorPreset:
    """Named generator configuration for benchmark populations."""
    name: str
    description: str
    config_kwargs: dict[str, float]
    person_kwargs: dict[str, float]
    regime_targets: dict[str, float] | None = None
    regime_person_kwargs: dict[str, dict[str, float]] = field(default_factory=dict)
    u_schedule: str | None = None


REGIME_ORDER = ("quiescent", "pinned_high", "bistable")

# Standing-condition support of the generative family: the correlated
# adversity load enters through constitution (TEM), history (DEV), and
# environment (SYS) — Batch J Section 8's b vector.  Estimators that assume
# this family (e.g. the Step 5 amortized estimator) constrain b_hat to it.
STANDING_NOMINAL: dict[str, float] = {"TEM": 0.35, "DEV": 0.30, "SYS": 0.30}


GENERATOR_PRESETS: dict[str, GeneratorPreset] = {
    "balanced_regimes": GeneratorPreset(
        name="balanced_regimes",
        description=(
            "Quota-sampled population with quiescent, pinned-high, and "
            "bistable persons represented in roughly equal numbers."
        ),
        config_kwargs={
            "T": 120,
            "process_noise": 0.06,
            "meas_noise": 0.06,
            "sampling_rate": 0.80,
            "dropout_prob": 0.10,
        },
        person_kwargs={"edge_sigma": 0.15, "gain_sigma": 0.10},
        regime_targets={"quiescent": 1.0, "pinned_high": 1.0, "bistable": 1.0},
        regime_person_kwargs={
            "quiescent": {
                "kappa_mean": 0.34,
                "kappa_sd": 0.05,
                "adversity_mean": 0.02,
                "adversity_sd": 0.08,
            },
            "pinned_high": {
                "kappa_mean": 0.46,
                "kappa_sd": 0.07,
                "adversity_mean": 0.75,
                "adversity_sd": 0.35,
            },
            "bistable": {
                "kappa_mean": 0.52,
                "kappa_sd": 0.06,
                "adversity_mean": 0.0,
                "adversity_sd": 0.0,
                "standing_noise": 0.0,
            },
        },
    ),
    "clinical_realistic": GeneratorPreset(
        name="clinical_realistic",
        description=(
            "Default EMA-like population: more pinned-high and quiescent "
            "persons, fewer bistable persons, moderate missingness/dropout."
        ),
        config_kwargs={
            "T": 100,
            "process_noise": 0.05,
            "meas_noise": 0.08,
            "sampling_rate": 0.70,
            "dropout_prob": 0.20,
        },
        person_kwargs={
            "kappa_mean": 0.44,
            "kappa_sd": 0.09,
            "adversity_mean": 0.55,
            "adversity_sd": 0.50,
        },
    ),
    "transition_rich": GeneratorPreset(
        name="transition_rich",
        description=(
            "Change-heavy population with over-sampled unstable regimes and "
            "a pulsed treatment schedule to create recovery/relapse movement."
        ),
        config_kwargs={
            "T": 180,
            "process_noise": 0.10,
            "meas_noise": 0.06,
            "sampling_rate": 0.85,
            "dropout_prob": 0.05,
        },
        person_kwargs={"edge_sigma": 0.18, "gain_sigma": 0.12},
        regime_targets={"quiescent": 1.0, "pinned_high": 3.0, "bistable": 2.0},
        regime_person_kwargs={
            "quiescent": {
                "kappa_mean": 0.38,
                "kappa_sd": 0.07,
                "adversity_mean": 0.08,
                "adversity_sd": 0.12,
            },
            "pinned_high": {
                "kappa_mean": 0.48,
                "kappa_sd": 0.08,
                "adversity_mean": 0.62,
                "adversity_sd": 0.35,
            },
            "bistable": {
                "kappa_mean": 0.54,
                "kappa_sd": 0.07,
                "adversity_mean": 0.0,
                "adversity_sd": 0.0,
                "standing_noise": 0.0,
            },
        },
        u_schedule="pulsed_treatment",
    ),
}


def generator_preset_names() -> list[str]:
    return sorted(GENERATOR_PRESETS)


def get_generator_preset(name: str) -> GeneratorPreset:
    try:
        return GENERATOR_PRESETS[name]
    except KeyError as exc:
        known = ", ".join(generator_preset_names())
        raise ValueError(f"unknown generator preset {name!r}; choose one of: {known}") from exc


def pulsed_treatment_schedule(config: SimConfig, params: PersonParams | None = None,
                              rng: np.random.Generator | None = None) -> np.ndarray:
    """Treatment-on, withdrawal, and maintenance phases for transition-rich data."""
    del params, rng
    u = np.zeros(config.T)
    on = max(1, int(round(config.T * 0.25)))
    off = max(on + 1, int(round(config.T * 0.52)))
    maint = max(off + 1, int(round(config.T * 0.72)))
    u[on:off] = 0.85
    u[off:maint] = 0.0
    u[maint:] = 0.35
    return u


def named_u_schedule(name: str | None):
    if name is None:
        return None
    if name == "pulsed_treatment":
        return pulsed_treatment_schedule
    raise ValueError(f"unknown u_schedule {name!r}")


def _quota_counts(n_persons: int, targets: dict[str, float]) -> dict[str, int]:
    total = float(sum(targets.values()))
    raw = {k: (v / total) * n_persons for k, v in targets.items()}
    counts = {k: int(np.floor(v)) for k, v in raw.items()}
    remainder = n_persons - sum(counts.values())
    order = sorted(targets, key=lambda k: (raw[k] - counts[k], -REGIME_ORDER.index(k)), reverse=True)
    for k in order[:remainder]:
        counts[k] += 1
    return counts


def preset_config(name: str, seed: int = 0, T: int | None = None,
                  config_overrides: dict | None = None) -> SimConfig:
    preset = get_generator_preset(name)
    kwargs = dict(preset.config_kwargs)
    kwargs["seed"] = seed
    if T is not None:
        kwargs["T"] = T
    if config_overrides:
        kwargs.update(config_overrides)
    return SimConfig(**kwargs)


# ==========================================================================
# Population sampling: perturb the consensus prior into individuals
# ==========================================================================


def dimension_base() -> tuple[np.ndarray, np.ndarray, list[str], float]:
    """The shared consensus structure at dimension level: (B, g, dims, kappa).

    ``B`` and ``g`` are the problem-frame coupling and treatment-gain of Batch
    J Section 8; the per-person standing conditions ``b`` are sampled, not
    inherited from the worked case.
    """
    B, g, _b_case, _idx = build_case_model()
    return B.copy(), g.copy(), list(ENDO), KAPPA


def characterize(params: PersonParams) -> PersonParams:
    """Fill in the dynamical labels a recovery study will try to predict."""
    B, g, b, kappa = params.B, params.g, params.b, params.kappa
    n = len(params.dims)
    x_lo = iterate(B, g, b, u=0.0, x0=np.zeros(n), kappa=kappa)
    x_hi = iterate(B, g, b, u=0.0, x0=np.ones(n), kappa=kappa)
    bistable = bool(np.max(np.abs(x_hi - x_lo)) > 1e-3)
    dis = ENDO.index("DIS")
    attractor_dis = float(x_hi[dis])
    params.kappa_star = float(critical_coupling(B))
    params.rho = float(jacobian_rho(B, g, b, 0.0, x_hi, kappa=kappa))
    if bistable:
        params.regime = "bistable"
    elif attractor_dis > 0.5:
        params.regime = "pinned_high"
    else:
        params.regime = "quiescent"
    params.attractor_dis = attractor_dis
    return params


def sample_person(rng: np.random.Generator, person_id: str,
                  base: tuple | None = None,
                  edge_sigma: float = 0.15,
                  gain_sigma: float = 0.10,
                  kappa_mean: float = 0.42, kappa_sd: float = 0.07,
                  adversity_mean: float = 0.7, adversity_sd: float = 0.45,
                  standing_noise: float = 0.03,
                  ) -> PersonParams:
    """Draw one person by perturbing the consensus prior.

    * edges: multiplicative log-normal noise on existing entries (zeros and
      signs preserved) -> person-specific structure;
    * standing conditions: a correlated adversity load on TEM/DEV/SYS plus
      idiosyncratic jitter -> heterogeneous constitution/history/environment;
    * coupling: kappa drawn around the population mean, so persons fall on both
      sides of their own bifurcation threshold.
    """
    if base is None:
        base = dimension_base()
    B0, g0, dims, _kappa0 = base
    n = len(dims)

    # --- structure: perturb existing edges only (rule W1) ----------------
    mask = B0 != 0.0
    factors = np.exp(rng.normal(0.0, edge_sigma, size=B0.shape))
    B = np.where(mask, np.clip(B0 * factors, 0.0, 1.5), 0.0)

    # --- treatment responsiveness: perturb gains, preserve sign ----------
    g = g0 * np.exp(rng.normal(0.0, gain_sigma, size=g0.shape))

    # --- standing conditions: correlated adversity on TEM/DEV/SYS --------
    adv = float(np.clip(rng.normal(adversity_mean, adversity_sd), 0.0, 2.0))
    b = np.zeros(n)
    for d, val in STANDING_NOMINAL.items():
        i = dims.index(d)
        b[i] = max(0.0, adv * val + rng.normal(0.0, standing_noise))

    kappa = float(np.clip(rng.normal(kappa_mean, kappa_sd), 0.20, 0.70))
    age = float(np.clip(rng.normal(35, 18), 4, 90))

    params = PersonParams(person_id=person_id, dims=dims, B=B, g=g, b=b,
                          kappa=kappa, age=age)
    return characterize(params)


def sample_population(n_persons: int, seed: int = 0,
                      regime_targets: dict[str, float] | None = None,
                      regime_person_kwargs: dict[str, dict] | None = None,
                      max_draws: int = 20000,
                      **kwargs) -> list[PersonParams]:
    rng = np.random.default_rng(seed)
    if regime_targets is None:
        return [sample_person(rng, person_id=f"P{i:04d}", **kwargs)
                for i in range(n_persons)]

    base = dimension_base()
    regime_person_kwargs = regime_person_kwargs or {}
    wanted = _quota_counts(n_persons, regime_targets)
    people: list[PersonParams] = []
    for regime in REGIME_ORDER:
        target_n = wanted.get(regime, 0)
        regime_kwargs = dict(kwargs)
        regime_kwargs.update(regime_person_kwargs.get(regime, {}))
        accepted = 0
        draws = 0
        while accepted < target_n and draws < max_draws:
            draws += 1
            candidate = sample_person(
                rng, person_id=f"C{len(people):04d}", base=base, **regime_kwargs
            )
            if candidate.regime == regime:
                people.append(candidate)
                accepted += 1
        if accepted < target_n:
            raise RuntimeError(
                f"could not draw {target_n} {regime!r} persons after {draws} attempts"
            )

    rng.shuffle(people)
    for i, person in enumerate(people):
        person.person_id = f"P{i:04d}"
    return people


# ==========================================================================
# Simulation: true trajectories + EMA observations
# ==========================================================================


def _u_schedule(config: SimConfig, u_schedule) -> np.ndarray:
    if u_schedule is None:
        return np.zeros(config.T)
    u = np.asarray(u_schedule, dtype=float)
    if u.shape != (config.T,):
        raise ValueError(f"u_schedule must have shape ({config.T},)")
    return u


def simulate_person(params: PersonParams, config: SimConfig,
                    rng: np.random.Generator,
                    u_schedule=None) -> PersonRecord:
    """Run the noisy iterated map and emit messy observations for one person."""
    B, g, b, kappa = params.B, params.g, params.b, params.kappa
    n = len(params.dims)
    if callable(u_schedule):
        u_schedule = u_schedule(config, params, rng)
    u = _u_schedule(config, u_schedule)

    # burn-in (no treatment) to reach the stationary neighbourhood
    x = np.zeros(n)
    for _ in range(config.burn_in):
        eps = rng.normal(0.0, config.process_noise, n)
        x = np.tanh(kappa * (B @ x) + b + eps)

    states = np.zeros((config.T, n))
    for t in range(config.T):
        eps = rng.normal(0.0, config.process_noise, n)
        x = np.tanh(kappa * (B @ x + g * u[t]) + b + eps)
        states[t] = x

    # observation model
    obs = states + rng.normal(0.0, config.meas_noise, size=states.shape)
    observed = rng.random(config.T) < config.sampling_rate

    dropout_time: int | None = None
    if rng.random() < config.dropout_prob:
        dropout_time = int(rng.integers(config.T // 2, config.T))
        observed[dropout_time:] = False

    mask = np.repeat(observed[:, None], n, axis=1)
    if config.item_missing > 0:
        mask &= rng.random(size=states.shape) >= config.item_missing
    obs = np.where(mask, obs, np.nan)

    return PersonRecord(params=params, states=states, observations=obs, u=u,
                        observed=observed, dropout_time=dropout_time)


@dataclass
class SyntheticDataset:
    """A population of simulated persons with ground truth, saveable to disk."""
    dims: list[str]
    config: SimConfig
    records: list[PersonRecord] = field(default_factory=list)

    # ---- summary --------------------------------------------------------
    def regime_counts(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for r in self.records:
            out[r.params.regime] = out.get(r.params.regime, 0) + 1
        return dict(sorted(out.items()))

    def missing_fraction(self) -> float:
        obs = np.concatenate([r.observations.reshape(-1) for r in self.records])
        return float(np.mean(np.isnan(obs)))

    # ---- persistence ----------------------------------------------------
    def save(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        N = len(self.records)
        n = len(self.dims)
        T = self.config.T
        B = np.stack([r.params.B for r in self.records])
        g = np.stack([r.params.g for r in self.records])
        b = np.stack([r.params.b for r in self.records])
        states = np.stack([r.states for r in self.records])
        obs = np.stack([r.observations for r in self.records])
        u = np.stack([r.u for r in self.records])
        observed = np.stack([r.observed for r in self.records])
        kappa = np.array([r.params.kappa for r in self.records])
        kappa_star = np.array([r.params.kappa_star for r in self.records])
        rho = np.array([r.params.rho for r in self.records])
        attractor = np.array([r.params.attractor_dis for r in self.records])
        age = np.array([r.params.age for r in self.records])
        dropout = np.array([-1 if r.dropout_time is None else r.dropout_time
                            for r in self.records])
        np.savez_compressed(
            os.path.join(path, "population.npz"),
            B=B, g=g, b=b, states=states, observations=obs, u=u,
            observed=observed, kappa=kappa, kappa_star=kappa_star, rho=rho,
            attractor_dis=attractor, age=age, dropout=dropout,
            person_ids=np.array([r.params.person_id for r in self.records]),
            regimes=np.array([r.params.regime for r in self.records]),
        )
        meta = {"dims": self.dims, "config": self.config.as_dict(),
                "n_persons": N, "n_dims": n, "T": T}
        with open(os.path.join(path, "manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2)

    @classmethod
    def load(cls, path: str) -> "SyntheticDataset":
        with open(os.path.join(path, "manifest.json"), encoding="utf-8") as fh:
            meta = json.load(fh)
        z = np.load(os.path.join(path, "population.npz"), allow_pickle=False)
        dims = meta["dims"]
        config = SimConfig(**meta["config"])
        records: list[PersonRecord] = []
        for i in range(meta["n_persons"]):
            p = PersonParams(
                person_id=str(z["person_ids"][i]), dims=dims,
                B=z["B"][i], g=z["g"][i], b=z["b"][i], kappa=float(z["kappa"][i]),
                age=float(z["age"][i]), kappa_star=float(z["kappa_star"][i]),
                regime=str(z["regimes"][i]), attractor_dis=float(z["attractor_dis"][i]),
                rho=float(z["rho"][i]),
            )
            dt = int(z["dropout"][i])
            records.append(PersonRecord(
                params=p, states=z["states"][i], observations=z["observations"][i],
                u=z["u"][i], observed=z["observed"][i],
                dropout_time=None if dt < 0 else dt,
            ))
        return cls(dims=dims, config=config, records=records)


def simulate_population(n_persons: int, config: SimConfig | None = None,
                        pop_seed: int = 0, u_schedule=None,
                        regime_targets: dict[str, float] | None = None,
                        regime_person_kwargs: dict[str, dict] | None = None,
                        **person_kwargs) -> SyntheticDataset:
    """Sample and simulate a whole population in one call."""
    config = config or SimConfig()
    people = sample_population(
        n_persons, seed=pop_seed, regime_targets=regime_targets,
        regime_person_kwargs=regime_person_kwargs, **person_kwargs
    )
    rng = np.random.default_rng(config.seed)
    records = [simulate_person(p, config, rng, u_schedule=u_schedule) for p in people]
    dims = people[0].dims if people else list(ENDO)
    return SyntheticDataset(dims=dims, config=config, records=records)


def simulate_preset(name: str, n_persons: int, T: int | None = None,
                    seed: int = 0, config_overrides: dict | None = None,
                    person_overrides: dict | None = None) -> SyntheticDataset:
    """Generate a population from a named benchmark preset."""
    preset = get_generator_preset(name)
    config = preset_config(name, seed=seed, T=T, config_overrides=config_overrides)
    person_kwargs = dict(preset.person_kwargs)
    if person_overrides:
        person_kwargs.update(person_overrides)
    return simulate_population(
        n_persons,
        config=config,
        pop_seed=seed,
        u_schedule=named_u_schedule(preset.u_schedule),
        regime_targets=preset.regime_targets,
        regime_person_kwargs=preset.regime_person_kwargs,
        **person_kwargs,
    )
