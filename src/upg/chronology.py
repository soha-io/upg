"""Calendar-safe helpers for intensive-longitudinal evaluation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import math
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class AnchorTransition:
    current: date
    target: date
    horizon_days: int

    @property
    def horizon_label(self) -> str:
        return f"{self.horizon_days}-day"


def parse_esm_date(value: str) -> date:
    """Parse the Kossakowski archive's documented day/month/two-digit-year."""
    return datetime.strptime(value, "%d/%m/%y").date()


def anchor_transitions(values: Iterable[date]) -> list[AnchorTransition]:
    """Return explicitly labelled consecutive calendar-anchor transitions.

    Day-of-year integers are deliberately not accepted: they lose the year at
    December/January boundaries and can leak later observations into history.
    """
    dates = list(values)
    if len(set(dates)) != len(dates):
        raise ValueError("anchor dates must be unique")
    transitions = []
    for current, target in zip(dates, dates[1:]):
        gap = (target - current).days
        if gap <= 0:
            raise ValueError("anchor dates must be strictly increasing")
        transitions.append(AnchorTransition(current, target, gap))
    return transitions


def _consecutive_day_pairs(
    dates: Iterable[date], values: Iterable[float]
) -> tuple[list[float], list[float]]:
    """Validate a series and return its finite observed t-1 -> t pairs."""
    day_list = list(dates)
    value_list = [float(value) for value in values]
    if len(day_list) != len(value_list):
        raise ValueError("dates and values must have equal length")
    x, y = [], []
    for previous_day, current_day, previous, current in zip(
        day_list, day_list[1:], value_list, value_list[1:]
    ):
        gap = (current_day - previous_day).days
        if gap <= 0:
            raise ValueError("dates must be strictly increasing")
        if gap == 1 and math.isfinite(previous) and math.isfinite(current):
            x.append(previous)
            y.append(current)
    return x, y


def consecutive_pair_count(
    dates: Iterable[date], values: Iterable[float]
) -> int:
    """Count finite observed consecutive-calendar-day t-1 -> t pairs."""
    x, _ = _consecutive_day_pairs(dates, values)
    return len(x)


def consecutive_ar1(
    dates: Iterable[date], values: Iterable[float], minimum_pairs: int = 8
) -> float:
    """OLS AR(1) slope using only observed consecutive-calendar-day pairs.

    Missing values remove their adjacent pairs, and a missing calendar day is
    never bridged.  This prevents a value at ``t-2`` from silently becoming
    the lag-1 predictor for ``t`` after ``dropna``. ``minimum_pairs`` is a
    threshold on valid t-1 -> t pairs, not on observed values.
    """
    if minimum_pairs < 1:
        raise ValueError("minimum_pairs must be positive")
    x, y = _consecutive_day_pairs(dates, values)
    if len(x) < minimum_pairs:
        return math.nan
    design = np.column_stack([np.ones(len(x)), np.asarray(x, dtype=float)])
    return float(np.linalg.lstsq(design, np.asarray(y, dtype=float), rcond=None)[0][1])
