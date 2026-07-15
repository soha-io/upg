"""Regression tests for the quarantined Batch K calendar defect."""
from datetime import date
import math

import pytest

from upg.chronology import (anchor_transitions, consecutive_ar1,
                            consecutive_pair_count, parse_esm_date)


def test_cross_year_dates_stay_monotonic():
    dates = [parse_esm_date(value) for value in (
        "24/12/12", "31/12/12", "07/01/13", "21/01/13", "11/02/13",
    )]
    transitions = anchor_transitions(dates)
    assert [item.current.year for item in transitions] == [2012, 2012, 2013, 2013]
    assert transitions[1].current == date(2012, 12, 31)
    assert transitions[1].target == date(2013, 1, 7)
    assert all(item.target > item.current for item in transitions)


def test_horizon_labels_report_actual_anchor_gaps():
    dates = [date(2012, 12, 24), date(2012, 12, 31),
             date(2013, 1, 14), date(2013, 2, 4)]
    transitions = anchor_transitions(dates)
    assert [item.horizon_days for item in transitions] == [7, 14, 21]
    assert [item.horizon_label for item in transitions] == ["7-day", "14-day", "21-day"]


def test_non_monotonic_or_duplicate_anchors_are_rejected():
    with pytest.raises(ValueError, match="strictly increasing"):
        anchor_transitions([date(2013, 1, 7), date(2012, 12, 31)])
    with pytest.raises(ValueError, match="unique"):
        anchor_transitions([date(2013, 1, 7), date(2013, 1, 7)])


def test_ar1_does_not_bridge_a_missing_calendar_day():
    dates = [date(2013, 1, 1), date(2013, 1, 2),
             date(2013, 1, 4), date(2013, 1, 5)]
    values = [1.0, 2.0, 100.0, 101.0]
    # Valid pairs are 1→2 and 100→101, both slope-one.  Treating adjacent
    # rows as adjacent days would add the invalid 2→100 bridge.
    assert consecutive_ar1(dates, values, minimum_pairs=2) == pytest.approx(1.0)


def test_ar1_missing_value_removes_both_touching_pairs():
    dates = [date(2013, 1, day) for day in range(1, 6)]
    values = [1.0, float("nan"), 3.0, 4.0, 5.0]
    assert consecutive_ar1(dates, values, minimum_pairs=2) == pytest.approx(1.0)
    assert math.isnan(consecutive_ar1(dates, values, minimum_pairs=3))


def test_ar1_threshold_counts_pairs_not_observed_values():
    dates = [date(2013, 1, day) for day in range(1, 10)]
    values = [float(day) for day in range(1, 10)]
    assert consecutive_pair_count(dates, values) == 8
    assert consecutive_ar1(dates, values, minimum_pairs=8) == pytest.approx(1.0)
    assert math.isnan(consecutive_ar1(dates, values, minimum_pairs=9))


def test_ar1_pair_count_excludes_calendar_gaps_and_missing_values():
    dates = [date(2013, 1, 1), date(2013, 1, 2), date(2013, 1, 4),
             date(2013, 1, 5), date(2013, 1, 6)]
    values = [1.0, 2.0, 3.0, float("nan"), 5.0]
    assert consecutive_pair_count(dates, values) == 1
