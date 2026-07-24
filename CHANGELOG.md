# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial structural port of the OG-Core country-model scaffold to Fiji, created from [OG-PHL](https://github.com/EAPD-DRB/OG-PHL). Package renamed to `ogfji`, with the full test suite, CI workflows, Makefile, packaging and Jupyter Book documentation structure of the sibling country models.
- Fijian demographics. `UN_COUNTRY_CODE` is set to `242` (Fiji) in `ogfji/calibrate.py` and referenced from every call site; the packaged `ogfji_default_parameters.json` demographic arrays (`omega`, `omega_SS`, `rho`, `imm_rates`, `g_n`, `g_n_ss`) and the derived earnings matrix `e` were regenerated from UN World Population Prospects data with `python -m ogfji.update_baseline_demographics`. Fiji's steady-state population growth is -0.157% a year, against -0.575% for the Philippines.
- `tests/test_country_id.py`, a regression guard asserting the UN country code is Fiji's, that no module inlines the literal, and that the packaged demographic arrays are Fijian and well formed. A stale country code is the most common regression when porting a country model in this family, and it has previously survived review because nothing asserted it.
- `GINI_TO_MATCH` in `ogfji/income.py` as a named constant (36.7, Fiji
  2013–14 HIES, reported in the 2019 Voluntary National Review). This is an
  income-concept Gini, matching the concept of the 41.5 U.S. anchor used by
  the earnings tilt.
- Fast value-pinning and progressive-tax shape tests for the calibrated
  defaults.

### Changed

- Replaced the structural-port placeholders with sourced Fiji calibration
  values: initial debt/GDP 0.60 → 0.821 and its steady-state policy anchor
  0.60 → 0.80; foreign debt share and `zeta_D` 0.20 → 0.347; `zeta_K`
  0.40 → 0.162432; labor-augmenting growth 3.713% → 3.0%; capital share
  0.53785 → 0.51137; remittances/GDP 0.072 → 0.071; and grants/GDP 0 →
  0.005. Sources are the Fiji 2026–27 Budget Supplement and Estimates, IMF
  2026 Article IV, PWT 11.0, Chinn–Ito, and World Bank, linked in the
  calibration chapters.
- Replaced flat personal-income-tax placeholders with a progressive
  Gouveia–Strauss schedule anchored to Fiji's 39% top rate and collections;
  set indirect taxes from 0.12 → 0.213793, the CIT receipt adjustment from
  0.30 → 0.372898, payroll contributions from 0.14 → 0.16 initially and
  0.18 long run, and bequest tax from 0.06 → 0. Sources are FRCS, FNPF, and
  the Fiji 2026–27 Budget documents linked in `taxes.md`.
- Kept the upstream UN WPP Fiji demographic arrays and renormalized the
  income-Gini-tilted earnings matrix to those population weights. The model
  remains single-industry; inherited SAM concordances were not imported.
- Disabled live macro and fiscal replacement: the packaged JSON is the
  offline source of truth, while `update_from_api=True` may refresh only UN
  demographics and their dependent earnings matrix.
- `docs/create_doc_figures.py` imports `UN_COUNTRY_CODE` from the package instead of hardcoding a country code, and drops the `pre_pop_dist` argument removed from `ogcore.demographics.get_pop_objs`.
- The calibration documentation chapters describe the method and name the Fijian institution that owns each parameter, rather than carrying over Philippine values and citations.
- Ruff uses `extend-exclude` rather than `exclude`, so its built-in exclusions still apply and `ruff format .` no longer descends into the local virtualenv. `.venv/` is also gitignored.
- The Codecov upload is advisory until the repository has a `CODECOV_TOKEN` secret, and PyPI publishing is manual (`workflow_dispatch`) rather than on every push to main.

### Removed

- The Philippine social accounting matrix and its concordances. `SAM_FILENAME` in `ogfji/input_output.py` is `None` and `CONS_DICT`/`PROD_DICT` in `ogfji/constants.py` are empty until a Fiji SAM or supply-and-use table is sourced. OG-FJI runs single-industry (`M=1`, `I=1`), which needs neither.
- The multi-industry example script, for the same reason.
- The Philippine-specific UN training materials and country figures.
- Unused tax-function test fixtures inherited from the port (74 MB, referenced by no test).

### Notes

- `ogcore.demographics` falls back to [EAPD-DRB/Population-Data](https://github.com/EAPD-DRB/Population-Data) when the UN Data Portal API is unavailable, but that mirror has no Fiji directory and ogcore's country lookup has no entry for code `242`, so the fallback raises `KeyError: '242'`. Normal use is unaffected because the packaged parameter file holds the solved demographic arrays, but refreshing demographics requires a working UN API token. Closing the gap needs a Fiji directory in Population-Data and a pull request against `PSLmodels/OG-Core`.
