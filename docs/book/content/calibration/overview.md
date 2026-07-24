# Calibration overview

The packaged file `ogfji_default_parameters.json` is the source of truth for
offline runs. The first release is deliberately single-industry: `I=M=1`,
`alpha_c=[1]`, and `io_matrix=[[1]]`.

| Block | Parameter | Value | Primary anchor |
|---|---:|---:|---|
| Demographics | UN M49 country | 242 | UN M49 |
| Earnings | income Gini | 36.7 | Fiji 2013–14 HIES/VNR |
| Production | private capital share | 0.51137 | PWT 11.0 labor share |
| Productivity | `g_y_annual` | 0.030 | long-run real GDP potential |
| Debt | initial debt/GDP | 0.821 | end-July 2026 estimate |
| Debt | steady-state anchor | 0.800 | FY2028–29 public-debt target |
| Debt | external share | 0.347 | end-July 2026 debt portfolio |
| Capital openness | `zeta_K` | 0.162432 | normalized Chinn–Ito index |
| Remittances | GDP share | 0.071 | World Bank, 2024 |
| Aid | GDP share | 0.005 | IMF FY2030–31 grants |
| Fiscal | transfers/GDP | 0.075 | IMF FY2030–31 |
| Fiscal | other primary spending/GDP | 0.185 | IMF FY2030–31 |
| Retirement | eligibility age | 55 | FNPF |
| Tax | top PIT rate | 0.39 | FRCS schedule |
| Tax | CIT rate | 0.25 | FRCS |
| Tax | indirect effective rate | 0.213793 | collections/household consumption |

The fiscal and debt vintage combines the
[2026–27 Budget Supplement](https://www.finance.gov.fj/wp-content/uploads/2026/06/2026-2027-Budget-Supplement.pdf),
the [2026–27 Budget Estimates](https://www.parliament.gov.fj/wp-content/uploads/2026/06/2026-2027-Budget-Estimates.pdf),
and the [IMF 2026 Article IV report](https://www.imf.org/-/media/files/publications/cr/2026/english/1fjiea2026001.pdf).

## Known provisional items

- The sovereign-rate intercept is analytically anchored to a 2.2% real
  effective debt cost, but must be re-centered on the model's solved private
  return.
- The corporate receipt adjustment is initialized from company-tax
  collections divided by the PWT capital-income share. It must be tuned
  against solved business-tax revenue.
- `chi_n` is borrowed unchanged from OG-USA; no Fiji time-use calibration is
  claimed.
- Public investment is included in non-transfer government purchases, but
  `gamma_g`, `alpha_I`, and the initial public-capital stock are zero until a
  separate public-capital calibration is available.
- FNPF contributions are represented in household payroll wedges and tagged
  separately with `frac_tax_payroll`; OG-Core does not yet map those funded
  contributions into individual retirement accounts.
- There is no Fiji SAM in this release.
