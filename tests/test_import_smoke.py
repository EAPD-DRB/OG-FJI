"""
Import smoke tests for installed package usage.
"""

import json
import importlib.resources


def test_import_smoke():
    import ogfji
    from ogfji import macro_params
    from ogfji.calibrate import Calibration

    assert ogfji is not None
    assert macro_params is not None
    assert Calibration is not None


def test_packaged_data_available():
    """The packaged default parameters load from the installed wheel."""
    with importlib.resources.open_text(
        "ogfji", "ogfji_default_parameters.json"
    ) as f:
        defaults = json.load(f)
    assert isinstance(defaults, dict)
    assert defaults


def test_no_sam_shipped_yet():
    """
    No SAM has been sourced for Fiji, so read_SAM() returns None rather than
    raising. Single-industry OG-FJI does not need one.

    When a Fiji SAM is added, set SAM_FILENAME in ogfji/input_output.py, ship
    the file in ogfji/data/, list it in MANIFEST.in and pyproject.toml, and
    replace this test with one asserting the SAM loads.
    """
    from ogfji import input_output

    assert input_output.SAM_FILENAME is None
    assert input_output.read_SAM() is None
