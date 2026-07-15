#!/usr/bin/env python3
"""Batch K retrospective analyses.

This script implements two deliberately bounded Layer-2 checks:

1. IPIP-NEO-120: a cross-sectional PER measurement audit.
2. Kossakowski et al. ESM: a one-person ME measurement/prediction audit.

It does not fit the complete UPG and cannot validate diagnosis, causal
treatment selection, or clinical effectiveness.  Raw files are read-only;
only aggregate or explicitly de-identified derived outputs are written.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import linear_sum_assignment
from scipy.stats import spearmanr
import sklearn
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from upg.chronology import (anchor_transitions, consecutive_ar1,
                            consecutive_pair_count)
from upg.data_paths import (PUBLIC_REQUIRED, PublicDataLayoutError,
                            resolve_public_data_root)
from upg.run_output import atomic_output_run


REPO_ROOT = Path(__file__).resolve().parents[3]
BATCH_ROOT = Path(__file__).resolve().parents[1]
DATA: Path | None = None
# Never overwrite the frozen, chronology-invalid legacy artifacts in
# results/real_data.  A corrected rerun is an explicit future study action.
OUT = BATCH_ROOT / "results" / "real_data_corrected" / "v3_calendar"

SEED = 20260712


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def finite_spearman(x, y) -> tuple[float, int, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    keep = np.isfinite(x) & np.isfinite(y)
    if keep.sum() < 3:
        return math.nan, int(keep.sum()), math.nan
    res = spearmanr(x[keep], y[keep])
    return float(res.statistic), int(keep.sum()), float(res.pvalue)


def circular_block_ci(x, y, block_length: int = 4, reps: int = 5000) -> list[float]:
    """Percentile CI that preserves short local ordering.

    This is an uncertainty description, not a population-generalization CI:
    the ESM archive contains one person.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    keep = np.isfinite(x) & np.isfinite(y)
    x, y = x[keep], y[keep]
    n = len(x)
    rng = np.random.default_rng(SEED)
    values = np.empty(reps, dtype=float)
    for b in range(reps):
        indices: list[int] = []
        while len(indices) < n:
            start = int(rng.integers(n))
            indices.extend(((start + np.arange(block_length)) % n).tolist())
        ix = np.asarray(indices[:n])
        values[b] = spearmanr(x[ix], y[ix]).statistic
    return [float(v) for v in np.nanquantile(values, [0.025, 0.975])]


def cronbach_alpha_complete(values: np.ndarray) -> tuple[float, int]:
    complete = values[np.isfinite(values).all(axis=1)]
    k = complete.shape[1]
    alpha = k / (k - 1) * (
        1.0 - complete.var(axis=0, ddof=1).sum() / complete.sum(axis=1).var(ddof=1)
    )
    return float(alpha), int(len(complete))


def varimax(phi: np.ndarray, gamma: float = 1.0, max_iter: int = 100,
            tolerance: float = 1e-8) -> np.ndarray:
    p, k = phi.shape
    rotation = np.eye(k)
    objective = 0.0
    for _ in range(max_iter):
        previous = objective
        loadings = phi @ rotation
        u, singular, vh = np.linalg.svd(
            phi.T
            @ (
                loadings ** 3
                - (gamma / p)
                * loadings
                @ np.diag(np.diag(loadings.T @ loadings))
            )
        )
        rotation = u @ vh
        objective = float(singular.sum())
        if previous and objective / previous < 1.0 + tolerance:
            break
    return phi @ rotation


DOMAIN_NAMES = ["Neuroticism", "Extraversion", "Openness", "Agreeableness", "Conscientiousness"]
DOMAIN_CODES = ["N", "E", "O", "A", "C"]
FACET_NAMES = [
    ["Anxiety", "Anger", "Depression", "Self-Consciousness", "Immoderation", "Vulnerability"],
    ["Friendliness", "Gregariousness", "Assertiveness", "Activity Level", "Excitement-Seeking", "Cheerfulness"],
    ["Imagination", "Artistic Interests", "Emotionality", "Adventurousness", "Intellect", "Liberalism"],
    ["Trust", "Morality", "Altruism", "Cooperation", "Modesty", "Sympathy"],
    ["Self-Efficacy", "Orderliness", "Dutifulness", "Achievement-Striving", "Self-Discipline", "Cautiousness"],
]


def analyze_ipip() -> dict:
    assert DATA is not None
    path = DATA / "ipip_neo_johnson" / "data_120_300" / "IPIP120.dat"
    raw = np.memmap(path, dtype=np.uint8, mode="r")
    if raw.size % 153:
        raise ValueError("IPIP fixed-width file does not contain 153-byte records")
    records = raw.reshape(-1, 153)
    if not np.all(records[:, 151:153] == np.array([13, 10], dtype=np.uint8)):
        raise ValueError("IPIP record terminators differ from CRLF contract")
    items = records[:, 31:151] - np.uint8(48)
    if np.any(items > 5):
        raise ValueError("IPIP item outside documented 0..5 range")

    n_rows = int(items.shape[0])
    missing_item_cells = int((items == 0).sum())
    per_gate_count = int(((items > 0).sum(axis=1) >= 84).sum())  # 70% of 120

    domain_rows: list[dict] = []
    domain_alphas: list[float] = []
    domain_scores = np.empty((n_rows, 5), dtype=np.float32)
    for domain in range(5):
        # Inventory order cycles N,E,O,A,C across six facets and repeats the
        # 30-facet block four times. Source values are already reverse keyed.
        indices = np.asarray(
            [domain + 5 * facet + 30 * repeat for repeat in range(4) for facet in range(6)]
        )
        selected = items[:, indices]
        answered = (selected > 0).sum(axis=1)
        normalized = np.where(selected > 0, (selected.astype(float) - 1.0) / 4.0, np.nan)
        alpha, complete_n = cronbach_alpha_complete(normalized)
        scores = np.full(n_rows, np.nan, dtype=float)
        np.divide(np.nansum(normalized, axis=1), answered, out=scores, where=answered > 0)
        scores[answered < 17] = np.nan  # ceil(.70 * 24)
        domain_scores[:, domain] = scores.astype(np.float32)
        observed_sd = float(np.nanstd(scores, ddof=1))
        measurement_sd = observed_sd * math.sqrt(1.0 - alpha)
        domain_alphas.append(alpha)
        domain_rows.append(
            {
                "domain": DOMAIN_NAMES[domain],
                "code": DOMAIN_CODES[domain],
                "records_passing_70pct_gate": int(np.isfinite(scores).sum()),
                "complete_records_for_alpha": complete_n,
                "cronbach_alpha": alpha,
                "observed_score_sd": observed_sd,
                "classical_test_theory_sem": measurement_sd,
            }
        )

    pd.DataFrame(domain_rows).to_csv(OUT / "ipip_domain_metrics.csv", index=False)

    facet_scores = np.empty((n_rows, 30), dtype=np.float32)
    facet_valid = np.empty((n_rows, 30), dtype=bool)
    for domain in range(5):
        for facet in range(6):
            column = domain * 6 + facet
            indices = np.asarray([domain + 5 * facet + 30 * repeat for repeat in range(4)])
            selected = items[:, indices]
            answered = (selected > 0).sum(axis=1)
            summed = np.where(selected > 0, (selected.astype(float) - 1.0) / 4.0, 0.0).sum(axis=1)
            facet_valid[:, column] = answered >= 3
            scored = np.full(n_rows, np.nan, dtype=float)
            np.divide(summed, answered, out=scored, where=answered >= 3)
            facet_scores[:, column] = scored.astype(np.float32)

    all_facets = facet_valid.all(axis=1)
    complete_facets = facet_scores[all_facets].astype(float)
    facet_corr = np.corrcoef(complete_facets, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(facet_corr)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    unrotated = eigenvectors[:, :5] * np.sqrt(eigenvalues[:5])
    rotated = varimax(unrotated)

    # Match unlabeled factors to intended domains by a one-to-one assignment.
    agreement = np.zeros((5, 5), dtype=float)
    for domain in range(5):
        agreement[domain] = np.abs(rotated[domain * 6:(domain + 1) * 6]).sum(axis=0)
    intended, factors = linear_sum_assignment(-agreement)
    factor_to_domain = {int(factor): int(domain) for domain, factor in zip(intended, factors)}

    loading_rows: list[dict] = []
    recovered = 0
    for column in range(30):
        intended_domain = column // 6
        strongest_factor = int(np.argmax(np.abs(rotated[column])))
        recovered_domain = factor_to_domain[strongest_factor]
        correct = recovered_domain == intended_domain
        recovered += int(correct)
        row = {
            "facet_code": f"{DOMAIN_CODES[intended_domain]}{column % 6 + 1}",
            "facet": FACET_NAMES[intended_domain][column % 6],
            "intended_domain": DOMAIN_NAMES[intended_domain],
            "recovered_domain": DOMAIN_NAMES[recovered_domain],
            "correct_primary_loading": correct,
        }
        for factor in range(5):
            row[f"rotated_factor_{factor + 1}"] = float(rotated[column, factor])
        loading_rows.append(row)
    pd.DataFrame(loading_rows).to_csv(OUT / "ipip_facet_loadings.csv", index=False)
    np.savetxt(OUT / "ipip_facet_correlation.csv", facet_corr, delimiter=",")

    upper = np.triu_indices(30, 1)
    corr_first = np.corrcoef(complete_facets[::2], rowvar=False)
    corr_second = np.corrcoef(complete_facets[1::2], rowvar=False)
    split_structure_r = float(np.corrcoef(corr_first[upper], corr_second[upper])[0, 1])
    within: list[float] = []
    cross: list[float] = []
    for i, j in zip(*upper):
        target = within if i // 6 == j // 6 else cross
        target.append(abs(float(facet_corr[i, j])))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), constrained_layout=True)
    axes[0].bar(DOMAIN_CODES, domain_alphas, color="#365d73")
    axes[0].axhline(0.70, color="#a34a28", linestyle="--", linewidth=1)
    axes[0].set_ylim(0.65, 0.94)
    axes[0].set_ylabel("Cronbach alpha")
    axes[0].set_title("IPIP-NEO-120 domain reliability")
    image = axes[1].imshow(facet_corr, vmin=-0.5, vmax=0.8, cmap="RdBu_r")
    axes[1].set_title("30-facet correlation structure")
    axes[1].set_xlabel("Facet")
    axes[1].set_ylabel("Facet")
    fig.colorbar(image, ax=axes[1], shrink=0.84)
    fig.savefig(OUT / "ipip_measurement_audit.png", dpi=180)
    plt.close(fig)

    misses = [
        f"{r['facet_code']} {r['facet']}→{r['recovered_domain']}"
        for r in loading_rows if not r["correct_primary_loading"]
    ]
    return {
        "input_file": str(path),
        "input_sha256": sha256(path),
        "fixed_width_bytes_per_record": 153,
        "records": n_rows,
        "missing_item_cells": missing_item_cells,
        "records_passing_70pct_overall_gate": per_gate_count,
        "records_passing_all_30_facet_gates": int(all_facets.sum()),
        "domain_metrics": domain_rows,
        "first_five_correlation_eigenvalues": [float(v) for v in eigenvalues[:5]],
        "first_five_variance_fraction": float(eigenvalues[:5].sum() / 30.0),
        "facets_recovered_by_primary_varimax_loading": recovered,
        "facets_total": 30,
        "facet_recovery_fraction": recovered / 30.0,
        "misclassified_facets": misses,
        "split_half_facet_correlation_structure_r": split_structure_r,
        "median_abs_within_domain_facet_correlation": float(np.median(within)),
        "median_abs_cross_domain_facet_correlation": float(np.median(cross)),
        "claim_boundary": (
            "Cross-sectional measurement evidence for PER only; no temporal direction, "
            "person-specific edges, diagnosis, or whole-UPG validation."
        ),
    }


ME_ITEMS = [
    "mood_relaxed", "mood_down", "mood_irritat", "mood_satisfi",
    "mood_lonely", "mood_anxious", "mood_enthus", "mood_suspic",
    "mood_cheerf", "mood_guilty", "mood_doubt", "mood_strong",
    "pat_restl", "pat_agitate", "pat_worry", "pat_concent",
    "se_selflike", "se_ashamed", "se_selfdoub", "se_handle",
]
POSITIVE_ITEMS = {
    "mood_relaxed", "mood_satisfi", "mood_enthus", "mood_cheerf",
    "mood_strong", "pat_concent", "se_selflike", "se_handle",
}
MINUS3_TO_3_ITEMS = {"mood_down", "mood_lonely", "mood_anxious", "mood_guilty"}


def me_item_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    transformed = pd.DataFrame(index=frame.index)
    for item in ME_ITEMS:
        value = pd.to_numeric(frame[item], errors="coerce")
        normalized = (value + 3.0) / 6.0 if item in MINUS3_TO_3_ITEMS else (value - 1.0) / 6.0
        transformed[item] = 1.0 - normalized if item in POSITIVE_ITEMS else normalized
        valid = transformed[item].isna() | transformed[item].between(0.0, 1.0)
        if not bool(valid.all()):
            raise ValueError(f"Out-of-range normalized value in {item}")
    return transformed


def ar1_coefficient(series: pd.Series, minimum: int = 8) -> float:
    """Calendar-safe AR(1) using observed t-1→t pairs only."""
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("AR(1) series must have a DatetimeIndex")
    return consecutive_ar1(
        [stamp.date() for stamp in series.index],
        series.to_numpy(dtype=float),
        minimum_pairs=minimum,
    )


def ar1_pair_count(series: pd.Series) -> int:
    """Number of valid observed consecutive-day pairs available to AR(1)."""
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("AR(1) series must have a DatetimeIndex")
    return consecutive_pair_count(
        [stamp.date() for stamp in series.index],
        series.to_numpy(dtype=float),
    )


def nested_ridge_alpha(x: np.ndarray, y: np.ndarray) -> float:
    """Choose alpha only inside the historical training window."""
    candidates = [0.01, 0.1, 1.0, 10.0, 100.0]
    if len(y) < 7:
        return 10.0
    first_test = max(4, len(y) // 2)
    losses = {alpha: [] for alpha in candidates}
    for test in range(first_test, len(y)):
        scaler = StandardScaler().fit(x[:test])
        train_x = scaler.transform(x[:test])
        test_x = scaler.transform(x[test:test + 1])
        for alpha in candidates:
            model = Ridge(alpha=alpha).fit(train_x, y[:test])
            losses[alpha].append(float((model.predict(test_x)[0] - y[test]) ** 2))
    return min(candidates, key=lambda alpha: (np.mean(losses[alpha]), alpha))


def analyze_kossakowski() -> dict:
    assert DATA is not None
    path = DATA / "kossakowski_esm" / "ESMdata" / "ESMdata.csv"
    raw = pd.read_csv(path)
    raw_rows = int(len(raw))
    aborted = int(raw["resp_abort"].eq(1).sum())
    unknown_abort_flag = int(raw["resp_abort"].isna().sum())
    # Only explicit aborts are excluded. The two missing abort flags are kept,
    # but remain visible in the audit; their item coverage is independently gated.
    data = raw.loc[~raw["resp_abort"].eq(1)].copy()

    matrix = me_item_matrix(data)
    answered = matrix.notna().sum(axis=1)
    data["me_load"] = matrix.mean(axis=1).where(answered >= 12)  # 60% of 20
    data["me_item_coverage"] = answered / len(ME_ITEMS)
    alpha, alpha_n = cronbach_alpha_complete(matrix.to_numpy(dtype=float))
    observed_sd = float(data["me_load"].std(ddof=1))
    measurement_sd = observed_sd * math.sqrt(1.0 - alpha)

    scl_items = [column for column in data.columns if column.startswith("SCL.90.R.")]
    if len(scl_items) != 13:
        raise ValueError(f"Expected 13 SCL weekly items, found {len(scl_items)}")
    data["weekly_dep"] = data[scl_items].mean(axis=1, skipna=True) / 4.0
    data.loc[data[scl_items].notna().sum(axis=1) < 10, "weekly_dep"] = np.nan

    data["calendar_date"] = pd.to_datetime(
        data["date"], format="%d/%m/%y", errors="raise"
    ).dt.normalize()
    documented_day = pd.to_numeric(data["dayno"], errors="raise").astype(int)
    if not bool((data["calendar_date"].dt.dayofyear == documented_day).all()):
        raise ValueError("date and dayno disagree in the Kossakowski archive")

    daily = (
        data.groupby("calendar_date", sort=True)
        .agg(
            me_load=("me_load", "mean"),
            concentration=("concentrat", "first"),
            phase=("phase", "first"),
            source_dayno=("dayno", "first"),
        )
        .sort_index()
    )
    weekly = (
        data.loc[data["weekly_dep"].notna()]
        .groupby("calendar_date", sort=True)
        .agg(weekly_dep=("weekly_dep", "first"), source_dayno=("dayno", "first"))
        .sort_index()
    )
    if not daily.index.is_monotonic_increasing or not weekly.index.is_monotonic_increasing:
        raise ValueError("calendar aggregation did not produce monotonic dates")

    weekly["me_7day"] = np.nan
    weekly["ar1_21day"] = np.nan
    weekly["ar1_21day_valid_consecutive_pairs"] = 0
    weekly["variance_21day"] = np.nan
    for day in weekly.index:
        window7 = daily.loc[
            (daily.index >= day - pd.Timedelta(days=6)) & (daily.index <= day),
            "me_load",
        ]
        if window7.notna().sum() >= 3:
            weekly.loc[day, "me_7day"] = float(window7.mean())
        window21 = daily.loc[
            (daily.index >= day - pd.Timedelta(days=20)) & (daily.index <= day),
            "me_load",
        ]
        weekly.loc[day, "ar1_21day_valid_consecutive_pairs"] = ar1_pair_count(window21)
        weekly.loc[day, "ar1_21day"] = ar1_coefficient(window21, minimum=8)
        if window21.notna().sum() >= 8:
            weekly.loc[day, "variance_21day"] = float(window21.var(ddof=1))
    weekly["target_date"] = pd.NaT
    weekly["horizon_days"] = np.nan
    weekly["horizon_label"] = None
    for transition in anchor_transitions([stamp.date() for stamp in weekly.index]):
        current = pd.Timestamp(transition.current)
        weekly.loc[current, "target_date"] = pd.Timestamp(transition.target)
        weekly.loc[current, "horizon_days"] = transition.horizon_days
        weekly.loc[current, "horizon_label"] = transition.horizon_label
    weekly["next_anchor_change"] = weekly["weekly_dep"].shift(-1) - weekly["weekly_dep"]

    concurrent_rho, concurrent_n, concurrent_p = finite_spearman(
        weekly["me_7day"], weekly["weekly_dep"]
    )
    ar_rho, ar_n, ar_p = finite_spearman(weekly["ar1_21day"], weekly["next_anchor_change"])
    variance_rho, variance_n, variance_p = finite_spearman(
        weekly["variance_21day"], weekly["next_anchor_change"]
    )
    dose_rho, dose_n, dose_p = finite_spearman(daily["concentration"], daily["me_load"])

    concurrent_ci = circular_block_ci(weekly["me_7day"], weekly["weekly_dep"], 4, 5000)
    ar_ci = circular_block_ci(weekly["ar1_21day"], weekly["next_anchor_change"], 4, 5000)
    variance_ci = circular_block_ci(
        weekly["variance_21day"], weekly["next_anchor_change"], 4, 5000
    )

    # Expanding-window, next-anchor prediction. Every row carries its exact
    # source date, target date, and calendar gap; no 14/21-day gap is called
    # "next week". Every test point occurs strictly after its training points.
    transitions = weekly[["weekly_dep", "me_7day", "ar1_21day"]].copy()
    transitions["target"] = weekly["weekly_dep"].shift(-1)
    transitions["target_date"] = weekly["target_date"]
    transitions["horizon_days"] = weekly["horizon_days"]
    transitions = transitions.dropna()
    x = transitions[["weekly_dep", "me_7day", "ar1_21day"]].to_numpy(dtype=float)
    y = transitions["target"].to_numpy(dtype=float)
    predictions: list[float] = []
    persistence: list[float] = []
    truth: list[float] = []
    alphas: list[float] = []
    forecast_dates: list[str] = []
    target_dates: list[str] = []
    horizon_days: list[int] = []
    initial_training = 10
    for test in range(initial_training, len(y)):
        alpha_selected = nested_ridge_alpha(x[:test], y[:test])
        scaler = StandardScaler().fit(x[:test])
        model = Ridge(alpha=alpha_selected).fit(scaler.transform(x[:test]), y[:test])
        predictions.append(float(model.predict(scaler.transform(x[test:test + 1]))[0]))
        persistence.append(float(x[test, 0]))
        truth.append(float(y[test]))
        alphas.append(alpha_selected)
        forecast_dates.append(transitions.index[test].date().isoformat())
        target_dates.append(pd.Timestamp(transitions.iloc[test]["target_date"]).date().isoformat())
        horizon_days.append(int(transitions.iloc[test]["horizon_days"]))
    predictions_a = np.asarray(predictions)
    persistence_a = np.asarray(persistence)
    truth_a = np.asarray(truth)
    model_mae = float(np.mean(np.abs(predictions_a - truth_a)))
    persistence_mae = float(np.mean(np.abs(persistence_a - truth_a)))
    model_rmse = float(np.sqrt(np.mean((predictions_a - truth_a) ** 2)))
    persistence_rmse = float(np.sqrt(np.mean((persistence_a - truth_a) ** 2)))
    forecast_by_horizon_days = {}
    horizon_array = np.asarray(horizon_days)
    for gap in sorted(set(horizon_days)):
        selected = horizon_array == gap
        forecast_by_horizon_days[str(gap)] = {
            "n": int(selected.sum()),
            "model_mae": float(np.mean(np.abs(predictions_a[selected] - truth_a[selected]))),
            "persistence_mae": float(np.mean(np.abs(persistence_a[selected] - truth_a[selected]))),
            "model_rmse": float(np.sqrt(np.mean((predictions_a[selected] - truth_a[selected]) ** 2))),
            "persistence_rmse": float(np.sqrt(np.mean((persistence_a[selected] - truth_a[selected]) ** 2))),
        }

    forecast_table = pd.DataFrame(
        {
            "current_date": forecast_dates,
            "target_date": target_dates,
            "horizon_days": horizon_days,
            "observed_next_anchor_dep": truth,
            "ridge_prediction": predictions,
            "persistence_prediction": persistence,
            "ridge_alpha_selected_inside_training_window": alphas,
        }
    )
    forecast_table.to_csv(OUT / "kossakowski_rolling_forecasts.csv", index=False)
    weekly.reset_index().to_csv(OUT / "kossakowski_weekly_derived.csv", index=False)

    phase_daily = daily.groupby("phase")["me_load"].mean()
    phase_weekly = (
        data.loc[data["weekly_dep"].notna()]
        .groupby(["phase", "calendar_date"])["weekly_dep"]
        .first()
        .groupby("phase")
        .mean()
    )
    phase_rows = [
        {
            "phase": int(phase),
            "daily_me_load_mean": float(phase_daily.loc[phase]),
            "weekly_depression_mean": float(phase_weekly.loc[phase]),
        }
        for phase in sorted(set(phase_daily.index) & set(phase_weekly.index))
    ]
    pd.DataFrame(phase_rows).to_csv(OUT / "kossakowski_phase_summary.csv", index=False)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), constrained_layout=True)
    axes[0].plot(daily.index, daily["me_load"], color="#365d73", linewidth=1.3, label="Daily ME load")
    axes[0].scatter(weekly.index, weekly["weekly_dep"], color="#a34a28", s=24, label="Weekly depression")
    axes[0].set_ylim(0, 0.75)
    axes[0].set_ylabel("Normalized load (0–1)")
    axes[0].set_title("One-person ESM series: descriptive trajectories")
    axes[0].legend(frameon=False, ncol=2)
    positions = np.arange(len(truth_a))
    axes[1].plot(positions, truth_a, "o-", color="#1d2b33", label="Observed")
    axes[1].plot(positions, predictions_a, "o--", color="#a34a28", label="Ridge")
    axes[1].plot(positions, persistence_a, "o:", color="#6d7b83", label="Persistence")
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels(
        [f"{current}\n→ {target} ({gap}d)"
         for current, target, gap in zip(forecast_dates, target_dates, horizon_days)],
        rotation=45,
        ha="right",
    )
    axes[1].set_xlabel("Calendar-date forecast origin and exact horizon")
    axes[1].set_ylabel("Next-anchor depression")
    axes[1].set_title("Strict rolling-origin forecast audit")
    axes[1].legend(frameon=False, ncol=3)
    fig.savefig(OUT / "kossakowski_real_data_audit.png", dpi=180)
    plt.close(fig)

    return {
        "input_file": str(path),
        "input_sha256": sha256(path),
        "raw_rows": raw_rows,
        "explicit_aborts_excluded": aborted,
        "unknown_abort_flags_retained_and_item_gated": unknown_abort_flag,
        "rows_after_abort_filter": int(len(data)),
        "rows_passing_60pct_me_gate": int(data["me_load"].notna().sum()),
        "mean_me_item_coverage": float(data["me_item_coverage"].mean()),
        "days": int(daily.index.nunique()),
        "weekly_anchors": int(len(weekly)),
        "me_items": ME_ITEMS,
        "me_complete_occasion_alpha": alpha,
        "complete_occasions_for_alpha": alpha_n,
        "me_observed_sd": observed_sd,
        "me_classical_test_theory_sem": measurement_sd,
        "concurrent_7day_me_vs_weekly_dep": {
            "spearman_rho": concurrent_rho,
            "n": concurrent_n,
            "p_value_descriptive": concurrent_p,
            "circular_block_95pct_interval": concurrent_ci,
        },
        "anchor_gap_days": {
            str(int(gap)): int(count)
            for gap, count in weekly["horizon_days"].dropna().value_counts().sort_index().items()
        },
        "ar1_21day_vs_next_anchor_dep_change": {
            "minimum_valid_consecutive_day_pairs": 8,
            "valid_consecutive_day_pairs_by_anchor": [
                int(value)
                for value in weekly["ar1_21day_valid_consecutive_pairs"].tolist()
            ],
            "spearman_rho": ar_rho,
            "n": ar_n,
            "p_value_descriptive": ar_p,
            "circular_block_95pct_interval": ar_ci,
        },
        "variance_21day_vs_next_anchor_dep_change": {
            "spearman_rho": variance_rho,
            "n": variance_n,
            "p_value_descriptive": variance_p,
            "circular_block_95pct_interval": variance_ci,
        },
        "daily_medication_concentration_vs_me": {
            "spearman_rho": dose_rho,
            "n": dose_n,
            "p_value_descriptive": dose_p,
            "interpretation": "Observational and strongly phase/time-confounded; not a medication effect.",
        },
        "rolling_origin_forecast": {
            "features": ["current weekly depression", "current 7-day ME load", "current 21-day AR(1)"],
            "initial_training_transitions": initial_training,
            "forecasts": len(truth),
            "model_mae": model_mae,
            "persistence_mae": persistence_mae,
            "model_rmse": model_rmse,
            "persistence_rmse": persistence_rmse,
            "model_beats_persistence_mae": model_mae < persistence_mae,
            "model_beats_persistence_rmse": model_rmse < persistence_rmse,
            "by_exact_horizon_days": forecast_by_horizon_days,
        },
        "phase_descriptives": phase_rows,
        "claim_boundary": (
            "N=1 partial ME/weekly-DIS feasibility and falsification check. The full UPG is "
            "unidentifiable; time-varying treatment is confounded with phase; no causal, "
            "diagnostic, treatment-selection, or population claim is permitted."
        ),
    }


def run_analysis() -> dict:
    ipip = analyze_ipip()
    kossakowski = analyze_kossakowski()
    summary = {
        "analysis_id": "batch-k-retrospective-v3-calendar-corrected",
        "chronology_contract": (
            "full calendar dates, strictly increasing anchor order, and exact "
            "source-to-target horizon_days on every forecast"
        ),
        "seed": SEED,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "ipip_neo_120": ipip,
        "kossakowski_esm": kossakowski,
        "global_boundary": (
            "These analyses provide partial retrospective evidence only. They do not validate "
            "the complete UPG as a diagnostic device or establish that UPG-guided care cures "
            "or improves any disorder."
        ),
    }
    with (OUT / "real_data_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)

    claims = [
        ["K-EMP-01", "IPIP domain scores are internally consistent in this archive", "E2 retrospective cross-sectional", "supported", "IPIP domain alpha .817–.905"],
        ["K-EMP-02", "A five-component solution exactly recovers every IPIP facet", "E2 retrospective cross-sectional", "falsified", f"{ipip['facets_recovered_by_primary_varimax_loading']}/30 primary loadings"],
        ["K-EMP-03", "The transparent ME load tracks concurrent weekly depression in this person", "E2 retrospective N=1", "supported_narrowly", f"rho={kossakowski['concurrent_7day_me_vs_weekly_dep']['spearman_rho']:.3f}"],
        ["K-EMP-04", "Rolling AR(1) predicts next-anchor depression change in this person", "E2 retrospective N=1", "not_supported", f"rho={kossakowski['ar1_21day_vs_next_anchor_dep_change']['spearman_rho']:.3f}"],
        ["K-EMP-05", "The small multivariable model beats persistence prospectively within the series", "E2 rolling-origin N=1", "not_supported", f"RMSE {kossakowski['rolling_origin_forecast']['model_rmse']:.3f} vs {kossakowski['rolling_origin_forecast']['persistence_rmse']:.3f}"],
        ["K-EMP-06", "The complete UPG is clinically validated", "E3 prospective required", "not_tested", "No full-stratum prospective cohort or trial"],
    ]
    with (OUT / "empirical_claims.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["claim_id", "claim", "evidence_level", "status", "result"])
        writer.writerows(claims)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def main(argv: list[str] | None = None) -> None:
    global DATA, OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-root", type=Path,
        help="public input root (precedence: explicit path, "
             "UPG_PUBLIC_DATA_ROOT, sibling upg-data/redistributable)",
    )
    parser.add_argument(
        "--out", type=Path, default=OUT,
        help="new, nonexistent versioned output directory; defaults to "
             "results/real_data_corrected/v3_calendar",
    )
    args = parser.parse_args(argv)
    try:
        DATA = resolve_public_data_root(repo_root=REPO_ROOT, explicit=args.data_root)
    except PublicDataLayoutError as exc:
        parser.error(str(exc))
    assert DATA is not None
    final_out = args.out.expanduser().resolve()
    required = tuple(DATA / relative for relative in PUBLIC_REQUIRED)
    protected = (
        BATCH_ROOT / "results" / "real_data",
        BATCH_ROOT / "evidence" / "audit",
    )
    inputs = {
        "ipip_neo_120": required[0],
        "kossakowski_esm": required[1],
        "analysis_script": Path(__file__),
        "chronology_helper": REPO_ROOT / "src" / "upg" / "chronology.py",
        "data_path_helper": REPO_ROOT / "src" / "upg" / "data_paths.py",
        "output_helper": REPO_ROOT / "src" / "upg" / "run_output.py",
        "project_metadata": REPO_ROOT / "pyproject.toml",
        "environment_lock": REPO_ROOT / "uv.lock",
    }
    try:
        with atomic_output_run(
            final_out,
            protected_dirs=protected,
            inputs=inputs,
            metadata={
                "analysis_id": "batch-k-retrospective-v3-calendar-corrected",
                "seed": SEED,
            },
        ) as temporary:
            OUT = temporary
            run_analysis()
    except (FileExistsError, PermissionError, RuntimeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
