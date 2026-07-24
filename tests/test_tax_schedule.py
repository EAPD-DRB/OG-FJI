"""Shape checks for Fiji's Gouveia–Strauss income-tax approximation."""

import importlib.resources
import json

import numpy as np


def test_progressive_tax_curve_has_fiji_shape():
    path = importlib.resources.files("ogfji").joinpath(
        "ogfji_default_parameters.json"
    )
    phi0, phi1, phi2 = json.loads(path.read_text())["etr_params"][0][0]
    income = np.array([10_000.0, 30_000.0, 50_000.0, 100_000.0, 1_000_000.0])
    etr = (
        phi0
        * (income - ((income ** (-phi1)) + phi2) ** (-1.0 / phi1))
        / income
    )
    assert np.all(np.diff(etr) > 0)
    assert etr[0] < 0.002
    assert etr[-1] > 0.35
    assert etr[-1] < phi0
