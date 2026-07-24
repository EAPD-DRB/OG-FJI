# OG-FJI calibration status

**Read this before using any OG-FJI output.**

OG-FJI was created by porting the structure of [OG-PHL](https://github.com/EAPD-DRB/OG-PHL).
The machinery, tests and CI are complete and the model runs, but **most
parameter values are still the Philippine ones inherited from that port**. The
model will solve and produce plausible-looking numbers that do not describe Fiji.

This file is the checklist of what is real and what is not. Update it as blocks
are calibrated, and delete it once nothing is left inherited.

## What is genuinely Fiji

| Block | Status | Notes |
| --- | --- | --- |
| Demographics (`omega`, `omega_SS`, `rho`, `imm_rates`, `g_n`, `g_n_ss`) | **Done** | Regenerated from UN World Population Prospects with `country_id = 242` (Fiji). Steady-state population growth is -0.157%/yr, against -0.575%/yr for the Philippines. |
| Earnings matrix `e` | **Provisional** | Regenerated for Fiji from the demographics and a Gini target, but the Gini has a concept mismatch — see below. |
| `country_id` / `UN_COUNTRY_CODE` | **Done** | 242, defined once in `ogfji/calibrate.py`, guarded by `tests/test_country_id.py`. |
| Preference parameters (`sigma`, `beta`, `frisch`, `nu`) | **N/A** | Taken from the literature, identical across all country models. Nothing to re-derive. |
| Elasticity of substitution `epsilon` | **N/A** | Cobb-Douglas (1.0), family-wide default. |

## What is still Philippine and must be replaced

Each row names the Fijian institution that owns the number. Search by role — the
national institution that administers a figure outranks any international
re-publication of it.

### Macro and open economy — `docs/book/content/calibration/macro.md`

| Parameter | Source to use |
| --- | --- |
| `g_y_annual` | Fiji Bureau of Statistics national accounts; IMF Article IV / WEO. Choose the window carefully: tourism-driven volatility, the COVID collapse and rebound, and cyclone interruptions all distort a naive average. Must be consistent with the growth `debt_ratio_ss` assumes. |
| `initial_debt_ratio` | Fiji Ministry of Finance debt reporting (measured). |
| `debt_ratio_ss` | Ministry of Finance / IMF Article IV (a *policy anchor*, not a measurement — do not leave inherited). |
| `initial_foreign_debt_ratio`, `zeta_D` | Ministry of Finance debt composition; IMF DSA projected flow. |
| `zeta_K` | Chinn-Ito openness index, cross-checked against the Reserve Bank of Fiji International Investment Position. **Do not leave at a high placeholder** — it drives domestic capital negative and breaks the transition. |
| `world_int_rate_annual` | Risk-free rate plus Fiji's sovereign spread (RBF, Article IV, rating reports). |
| `alpha_RM_1`, `alpha_RM_T`, `g_RM`, `eta_RM` | Reserve Bank of Fiji balance-of-payments. Remittances are large for Fiji; leaving them off produces a spurious trade surplus. |
| `r_gov_scale`, `r_gov_shift` | Keep the Li et al. (2021) slope; **re-anchor the shift** to Fiji's real effective rate on debt (debt service ÷ gross debt, less expected inflation). |
| `r_gov_DY`, `r_gov_DY2` | Recompute the centered debt-elastic premium against the new `debt_ratio_ss`. |
| `initial_Kg_ratio` | Only matters if `gamma_g > 0`. Solve the steady-state law of motion; Fiji's donor-financed infrastructure may put the measured stock above the sustainable level. |

### Government — `docs/book/content/calibration/government.md`

| Parameter | Source to use |
| --- | --- |
| `alpha_T` | Ministry of Finance budget estimates and Economic and Fiscal Update. |
| `alpha_G` | Ministry of Finance; total outlays less transfers, net interest and pensions. |
| `alpha_I` | Ministry of Finance capital budget; ADB / World Bank infrastructure diagnostics. |

> **Check the fiscal identity.** `alpha_G + alpha_T` must equal revenue less the
> primary balance that `debt_ratio_ss` requires. The steady state solves even
> when this is violated; the *transition* diverges. This is the single most
> destabilizing calibration error in this model family.

### Firms — `docs/book/content/calibration/firms.md`

| Parameter | Source to use |
| --- | --- |
| `gamma`, `gamma_g` | ILOSTAT / FBoS labour share. Apply a Gollin self-employment adjustment: Fiji has a large subsistence and own-account sector whose mixed income is booked as capital, and communal (*iTaukei*) land tenure means land rent is not a private corporate return. |

### Taxes — `docs/book/content/calibration/taxes.md`

Every rate below is currently a Philippine value, and several are tied to
Philippine legislation (the TRAIN Law) that has no Fijian counterpart.

| Parameter | Source to use |
| --- | --- |
| `etr_params`, `mtrx_params`, `mtry_params` | FRCS statutory schedule and collections. **Prefer a progressive GS fit over flat-linear** — it needs only the statutory schedule plus a collections target. |
| `mean_income_data` | FBoS Household Income and Expenditure Survey, in Fiji dollars. |
| `cit_rate`, `adjustment_factor_for_cit_receipts`, `c_corp_share_of_assets` | FRCS collections; account for concessionary regimes and incentives. |
| `tau_c` | **All** indirect taxes, not VAT alone: VAT, Service Turnover Tax, Environment and Climate Adaptation Levy, departure tax, excises, customs. |
| `tau_payroll` | Statutory rate × covered share of the *wage bill* (not headcount). Fiji National Provident Fund. |
| `tau_bq` | Fiji's actual estate/inheritance treatment. **Verify explicitly** — a stray inherited nonzero bequest tax silently collected several percent of GDP in a sibling model. |
| `h_wealth`, `m_wealth`, `p_wealth` | Zero by default; confirm. |

### Earnings — `docs/book/content/calibration/earnings.md`

| Parameter | Issue |
| --- | --- |
| `GINI_TO_MATCH` (`ogfji/income.py`) | Currently **30.7** (Fiji 2019, World Bank `SI.POV.GINI`). That is a **consumption**-concept Gini being matched against an **income**-concept US anchor of 41.5. This understates Fijian inequality and flattens the `e` matrix. Replace with an income-concept Gini (WID, or an income tabulation of the FBoS HIES). |

### Labour supply

| Parameter | Status |
| --- | --- |
| `chi_n` | **Borrowed from OG-USA and uncalibrated** — the honest default state of every port in this family. Either re-tilt by a single scalar to an hours or participation target, or wire the FBoS labour force survey through a real estimation routine. Do not present it as calibrated. |

## Not yet possible

| Item | Blocker |
| --- | --- |
| Multi-industry (M > 1) | **No SAM has been sourced for Fiji.** `CONS_DICT` and `PROD_DICT` in `ogfji/constants.py` are empty and `SAM_FILENAME` in `ogfji/input_output.py` is `None`. Search FBoS supply-and-use tables first, then UNU-WIDER / IFPRI country SAMs, then global databases as a lower-confidence last resort. |
| Live demographic refresh without a UN token | **Fiji is not in the offline mirror.** `ogcore.demographics` falls back to [EAPD-DRB/Population-Data](https://github.com/EAPD-DRB/Population-Data), which has no Fiji directory, and ogcore's country lookup has no entry for `242` — the fallback raises `KeyError: '242'`. Normal use is unaffected (the packaged JSON holds the solved arrays and needs no network), but a refresh needs a working UN Data Portal API token. **Fix:** add a Fiji directory to Population-Data and open a PR on `PSLmodels/OG-Core` adding `"242": "FJI"`. |
| Committed demographic figures for the population path | The fertility, mortality, immigration and ability-profile figures in the docs are Fijian. The population-distribution-path and population-growth-path figures were not regenerated and are deliberately **not committed** rather than shipped as stale Philippine figures. Run `uv run python docs/create_doc_figures.py` and add them. |

## The scaffold's current steady state

The model solves. This is the steady state it produces today, from the packaged
defaults with `Calibration(p, update_from_api=False)`:

| Moment | Scaffold value | Comment |
| --- | --- | --- |
| `r` | 0.0738 | |
| `r_gov` | 0.0518 | |
| `K/Y` | 4.19 | Runs high against PWT across the whole model family; a structural trait, not a country error. |
| `D/Y` | 0.600 | Holds the inherited Philippine `debt_ratio_ss`. |
| `D_f/D` | 0.200 | Inherited. |
| `K_f/K` | 0.321 | **Solver warns `K_d has negative elements`** during the solve — the classic symptom of `zeta_K` set too high. |
| `factor` | 184,368 | In Philippine pesos, not Fiji dollars. |
| Total revenue / Y | 27.7% | |
| PIT / Y | **19.1%** | **Implausible.** A flat rate applied to everyone over-collects badly versus a progressive schedule. This is the single clearest signal the tax block is not Fiji's. |
| CIT / Y | 2.2% | |
| Indirect / Y | 5.2% | |
| Bequest tax / Y | **1.1%** | A nonzero bequest tax inherited from Philippine legislation with no Fijian counterpart. |
| Resource constraint error | -8.8e-14 | Solves cleanly. |

Two things to read from this table. First, the machinery works end to end — so
the calibration work can start immediately rather than after a debugging phase.
Second, **a model that solves cleanly is not a model that is calibrated**: PIT at
19% of GDP and a phantom bequest tax are exactly the kind of over-collection
that masks a spending-exceeds-revenue gap, so the fiscal block will need
re-checking as a whole once the rates are replaced, not instrument by
instrument.

Regenerate this table after each block is calibrated, and delete it when the
calibration is complete.

## Validating the result

Do not check parameters one at a time — most are weakly identified alone. Build
a steady-state dashboard in `macro.md` comparing the solved steady state against
Fijian data, with a source column for each moment.

Lead with fiscal data: tax collections by instrument as a share of GDP (PIT,
CIT, indirect, payroll), the debt ratio, its foreign share, and the effective
real rate on debt. These are published precisely, map one-to-one onto model
ratios, and are self-checking through the government budget identity. Then add
`K/Y`, `C/Y`, `(I+I_g)/Y`, `NX/Y`, `RM/Y`, `r` and `factor` as a second tier.

Read the model side from the solved steady state with
`ogcore.utils.safe_read_pickle` on `OUTPUT_BASELINE/SS/SS_vars.pkl` rather than
eyeballing printed output.

Two known family traits — report them, do not chase them by distorting a Fijian
parameter: the model's endogenous `K/Y` runs high against the Penn World Table
across every country in the family, and "net exports" is a balance-of-payments
residual of the resource constraint rather than a modeled trade flow.
