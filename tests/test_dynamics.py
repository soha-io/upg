"""Worked-case dynamics and generic dynamical-systems tools (Batch J Section 8)."""
import numpy as np

from upg import case_report
from upg.dynamics import signed_loops, spectral_radius


def test_untreated_attractor_and_stability():
    cr = case_report()
    assert abs(cr.untreated["DIS"] - 0.774) < 1e-3
    assert abs(cr.untreated_rho - 0.486) < 1e-3
    assert cr.bistable is False


def test_bifurcation_threshold():
    cr = case_report()
    assert abs(cr.lambda_max_B - 2.195) < 1e-3
    assert abs(cr.kappa_star - 0.456) < 1e-3


def test_treatment_state_shifting():
    cr = case_report()
    assert abs(cr.treated[0.5]["DIS"] - 0.58) < 1e-3
    assert abs(cr.treated[0.8]["DIS"] - 0.249) < 1e-3
    # withdrawal returns exactly to the pre-treatment attractor
    assert abs(cr.relapse_dis - 0.774) < 1e-3


def test_structure_change_holds():
    cr = case_report()
    assert abs(cr.surgery["DIS"] - 0.676) < 1e-3           # edge surgery alone
    assert abs(cr.surgery_maintained["DIS"] - 0.528) < 1e-3  # + maintenance dose


def test_loop_rankings():
    cr = case_report()
    amp_gain, amp_path = cr.top_amplifying[0]
    reg_gain, reg_path = cr.top_regulating[0]
    assert amp_path == ["NEED", "ME"] and abs(amp_gain - 0.400) < 1e-3
    assert reg_path == ["DIS", "THER"] and abs(reg_gain + 0.455) < 1e-3


def test_linear_fixed_point_example():
    # Batch I EX3: x* = (I-B)^-1 b, rho(B) = 0.727 (stable).
    B = np.array([[0.5, 0.4], [0.3, 0.2]])
    b = np.array([0.1, 0.2])
    xstar = np.linalg.solve(np.eye(2) - B, b)
    assert np.allclose(xstar, [0.571, 0.464], atol=1e-3)
    assert abs(spectral_radius(B) - 0.727) < 1e-3


def test_signed_loops_helper_directionality():
    # A simple 2-cycle a<->b with product of weights.
    W = np.array([[0.0, 0.5], [0.4, 0.0]])   # W[target, source]
    loops = signed_loops(W, ["a", "b"], lengths=(2,))
    assert len(loops) == 1
    gain, path = loops[0]
    assert abs(gain - 0.20) < 1e-12 and path == ["a", "b"]
