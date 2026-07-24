"""Regression tests pinning the initial Fiji calibration."""

import importlib.resources
import json

import numpy as np
import pytest

from ogcore.parameters import Specifications


def _defaults():
    path = importlib.resources.files("ogfji").joinpath(
        "ogfji_default_parameters.json"
    )
    return json.loads(path.read_text())


def test_defaults_load_into_ogcore():
    defaults = _defaults()
    p = Specifications(baseline=True)
    p.update_specifications(defaults)
    assert not p.errors
    assert p.I == 1
    assert p.M == 1
    assert p.start_year == 2026


def test_fiji_macro_and_fiscal_anchors():
    d = _defaults()
    assert d["initial_debt_ratio"] == pytest.approx(0.821)
    assert d["debt_ratio_ss"] == pytest.approx(0.80)
    assert d["initial_foreign_debt_ratio"] == pytest.approx(0.347)
    assert d["zeta_D"] == pytest.approx([0.347])
    assert d["zeta_K"] == pytest.approx([0.162432])
    assert d["g_y_annual"] == pytest.approx(0.03)
    assert d["alpha_RM_1"] == pytest.approx(0.071)
    assert d["alpha_RM_T"] == pytest.approx(0.071)
    assert d["alpha_FA"] == pytest.approx([0.005])
    assert d["alpha_T"] == pytest.approx([0.075])
    assert d["alpha_G"] == pytest.approx([0.185])
    assert d["alpha_I"] == pytest.approx([0.0])
    assert d["alpha_T"][0] + d["alpha_G"][0] == pytest.approx(0.26)


def test_fiji_production_and_tax_anchors():
    d = _defaults()
    assert d["gamma"] == pytest.approx([0.51137])
    assert d["gamma_g"] == pytest.approx([0.0])
    assert d["tax_func_type"] == "GS"
    assert d["analytical_mtrs"] is True
    assert d["etr_params"] == d["mtrx_params"] == d["mtry_params"]
    assert d["etr_params"][0][0][0] == pytest.approx(0.39)
    assert d["tau_payroll"] == pytest.approx([0.16, 0.18])
    assert d["tau_c"][0][0] == pytest.approx(0.213793)
    assert d["tau_bq"] == pytest.approx([0.0])
    assert d["cit_rate"][0][0] == pytest.approx(0.25)
    assert d["mean_income_data"] == pytest.approx(26248.6)


def test_earnings_are_normalized():
    d = _defaults()
    e = np.asarray(d["e"])
    omega = np.asarray(d["omega_SS"])
    lambdas = np.asarray(d["lambdas"])
    assert e.shape == (80, 7)
    assert np.sum(e * omega.reshape(80, 1) * lambdas.reshape(1, 7)) == (
        pytest.approx(1.0)
    )


def test_demographic_arrays_stay_within_ogcore_bounds():
    d = _defaults()
    imm_rates = np.asarray(d["imm_rates"])
    assert imm_rates.shape == (400, 80)
    assert imm_rates.max() <= 1.0
    assert imm_rates.min() >= -1.0
