"""
Regression guard on the country this repository actually calibrates.

The single most common regression when porting an OG-Core country model is a
stale country code: `calibrate.py` gets refreshed by copying a sibling repo and
the UN M49 code is not swapped, so the model silently calibrates the wrong
country's demographics. This has happened more than once in this family of
repositories, in both cases surviving review because nothing asserted it.

These tests are deliberately cheap -- no solve, no network.
"""

import json
import importlib.resources

import numpy as np

from ogfji.calibrate import UN_COUNTRY_CODE

# UN M49 numeric code for Fiji.
FIJI_M49 = "242"


def test_un_country_code_is_fiji():
    assert UN_COUNTRY_CODE == FIJI_M49


def test_country_code_not_inlined_elsewhere():
    """
    Every UN data call must go through the UN_COUNTRY_CODE constant rather
    than an inlined literal, so there is exactly one place to change.
    """
    import inspect

    from ogfji import calibrate, update_baseline_demographics

    for module in (calibrate, update_baseline_demographics):
        src = inspect.getsource(module)
        # The constant's own definition is the only place the literal appears.
        assert src.count(f'"{FIJI_M49}"') <= 1, (
            f"{module.__name__} inlines the country code literal; "
            "reference UN_COUNTRY_CODE instead"
        )


def _packaged_defaults():
    with importlib.resources.open_text(
        "ogfji", "ogfji_default_parameters.json"
    ) as f:
        return json.load(f)


def test_packaged_demographics_are_fijian():
    """
    The packaged demographic arrays must be Fiji's, not a sibling country's.

    Fiji's solved steady-state population growth rate is mildly negative,
    around -0.16% a year. The Philippine value this repository was ported from
    is roughly -0.58%. A regenerated-for-the-wrong-country JSON would land on
    the latter, so pin the sign and a generous band around the Fijian value.
    """
    defaults = _packaged_defaults()
    g_n_ss = defaults["g_n_ss"]

    assert -0.005 < g_n_ss < 0.0, (
        f"steady-state population growth {g_n_ss:.5f} is outside the band "
        "expected for Fiji -- were the demographics regenerated for the "
        "wrong country_id?"
    )


def test_packaged_demographic_arrays_are_well_formed():
    """Demographic arrays are present, finite and correctly shaped."""
    defaults = _packaged_defaults()

    for key in ("omega_SS", "rho", "imm_rates", "e"):
        assert key in defaults, f"{key} missing from packaged defaults"
        arr = np.asarray(defaults[key], dtype=float)
        assert arr.size > 0
        assert np.all(np.isfinite(arr)), f"{key} contains non-finite values"

    omega_ss = np.asarray(defaults["omega_SS"], dtype=float)
    assert np.isclose(omega_ss.sum(), 1.0, atol=1e-6), (
        "steady-state population distribution does not sum to 1"
    )
