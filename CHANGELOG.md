# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial structural port of the OG-Core country-model scaffold to Fiji, created from [OG-PHL](https://github.com/EAPD-DRB/OG-PHL). Package renamed to `ogfji`, with the full test suite, CI workflows, Makefile, packaging and Jupyter Book documentation structure of the sibling country models.
- Fijian demographics. `UN_COUNTRY_CODE` is set to `242` (Fiji) in `ogfji/calibrate.py` and referenced from every call site; the packaged `ogfji_default_parameters.json` demographic arrays (`omega`, `omega_SS`, `rho`, `imm_rates`, `g_n`, `g_n_ss`) and the derived earnings matrix `e` were regenerated from UN World Population Prospects data with `python -m ogfji.update_baseline_demographics`. Fiji's steady-state population growth is -0.157% a year, against -0.575% for the Philippines.
- `CALIBRATION_STATUS.md`, the authoritative record of which parameter blocks are genuinely Fijian and which are still inherited Philippine values, with the Fijian institution that owns each number that must be replaced.
- `tests/test_country_id.py`, a regression guard asserting the UN country code is Fiji's, that no module inlines the literal, and that the packaged demographic arrays are Fijian and well formed. A stale country code is the most common regression when porting a country model in this family, and it has previously survived review because nothing asserted it.
- `GINI_TO_MATCH` in `ogfji/income.py` as a named constant (30.7, Fiji 2019, World Bank `SI.POV.GINI`), documenting the welfare-concept mismatch against the income-concept US anchor that the earnings tilt is solved against.

### Changed

- `docs/create_doc_figures.py` imports `UN_COUNTRY_CODE` from the package instead of hardcoding a country code, and drops the `pre_pop_dist` argument removed from `ogcore.demographics.get_pop_objs`.
- The calibration documentation chapters describe the method and name the Fijian source for each parameter, rather than carrying over Philippine values and citations. Every chapter whose values are still inherited says so.

### Removed

- The Philippine social accounting matrix and its concordances. `SAM_FILENAME` in `ogfji/input_output.py` is `None` and `CONS_DICT`/`PROD_DICT` in `ogfji/constants.py` are empty until a Fiji SAM or supply-and-use table is sourced. OG-FJI runs single-industry (`M=1`, `I=1`), which needs neither.
- The multi-industry example script, for the same reason.
- The Philippine-specific UN training materials and country figures.

### Known limitations

- **Not calibrated to Fiji.** Macro, fiscal, tax and firm parameters are still the inherited Philippine values. See `CALIBRATION_STATUS.md`.
- **Fiji is absent from the offline population-data mirror.** `ogcore.demographics` falls back to [EAPD-DRB/Population-Data](https://github.com/EAPD-DRB/Population-Data) when the UN Data Portal API is unavailable, but that mirror has no Fiji directory and ogcore's country lookup has no entry for code `242`, so the fallback raises `KeyError: '242'`. Normal use is unaffected because the packaged JSON holds the solved demographic arrays, but refreshing demographics requires a working UN API token. Fixing this needs a Fiji directory in Population-Data and a pull request against `PSLmodels/OG-Core`.
