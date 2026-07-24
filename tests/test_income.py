"""Tests for the Fiji earnings-profile adapter."""

import inspect

import numpy as np
import pytest

from ogfji import income


def test_default_uses_income_concept_gini():
    default = (
        inspect.signature(income.get_e_interp)
        .parameters["gini_to_match"]
        .default
    )
    assert default == pytest.approx(36.7)


def test_dimension_checks_happen_before_network_access():
    with pytest.raises(AssertionError):
        income.get_e_interp(
            20,
            80,
            7,
            np.ones(6) / 6,
            np.ones(80) / 80,
        )
