"""Tests for the offline and live OG-FJI calibration overlay."""

import warnings
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from ogfji.calibrate import Calibration, UN_COUNTRY_CODE


def _mock_specs(I=1, M=1):  # noqa: E741
    p = MagicMock()
    p.I = I
    p.M = M
    p.E = 20
    p.S = 80
    p.T = 160
    p.J = 7
    p.start_year = 2026
    p.lambdas = np.array([0.25, 0.25, 0.20, 0.10, 0.10, 0.09, 0.01])
    return p


def test_fiji_un_country_code():
    assert UN_COUNTRY_CODE == "242"


def test_offline_mode_returns_only_identity_values():
    result = Calibration(_mock_specs(), update_from_api=False).get_dict()
    np.testing.assert_array_equal(result["alpha_c"], np.array([1.0]))
    np.testing.assert_array_equal(result["io_matrix"], np.array([[1.0]]))
    assert "e" not in result
    assert "omega" not in result


def test_multi_industry_is_explicitly_rejected():
    with pytest.raises(ValueError, match="single-industry"):
        Calibration(_mock_specs(I=2, M=2))


@patch("ogcore.demographics.get_pop_objs")
@patch("ogfji.calibrate.income.get_e_interp")
def test_live_mode_uses_fiji_for_both_demographic_calls(mock_e, mock_pop):
    mock_pop.side_effect = [
        {"omega": np.ones((2, 80)), "omega_SS": np.ones(80) / 80},
        {"omega_SS": np.ones(80) / 80},
    ]
    mock_e.return_value = np.ones((80, 7))

    result = Calibration(_mock_specs(), update_from_api=True).get_dict()

    assert mock_pop.call_count == 2
    for call in mock_pop.call_args_list:
        assert call.kwargs["country_id"] == "242"
    assert result["e"].shape == (80, 7)


@patch("ogcore.demographics.get_pop_objs")
def test_live_failure_keeps_packaged_values(mock_pop):
    mock_pop.side_effect = RuntimeError("offline")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = Calibration(_mock_specs(), update_from_api=True).get_dict()
    assert any("Demographics/income" in str(item.message) for item in caught)
    assert "omega" not in result
    assert "e" not in result
