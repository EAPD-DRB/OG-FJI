# Taxes

## Personal income tax

OG-FJI uses a Gouveia–Strauss (`GS`) tax function with a 39% asymptotic top
rate. The two shape parameters are fitted to Fiji's progressive resident
schedule and its PAYE collection target:

```text
(phi0, phi1, phi2) = (0.39, 2.6345931624, 1.7236172001e-13)
```

The same triple is stored in `etr_params`, `mtrx_params`, and `mtry_params`;
`analytical_mtrs=True`. The statutory schedule has a FJ$30,000 zero-rate
threshold and rates from 18% to 39%. Sources:
[FRCS personal income tax](https://frcs.org.fj/our-services/taxation/individuals/personal-income-tax/)
and the [official rate schedule](https://frcs.org.fj/wp-content/uploads/2024/05/SIG-on-Change-in-Individual-Income-Tax-Rates.pdf).

The income scale is FJ$26,248.60, the mean annual household income in the
2019–20 HIES. This matches the family-income concept used by the country-model
tax scaling and is close to the PAYE-to-labor-income yield in the 2026–27
Budget Estimates.

## Payroll contributions

The employee and employer FNPF contributions are each 8% from August 2026,
giving 16% in the first model year. The employer rate is scheduled to return
to 10%, so the long-run rate is 18%. Source:
[2026–27 Budget Address, paragraphs 253–255](https://www.finance.gov.fj/wp-content/uploads/2026/06/2026-2027-Budget-Address.pdf).
FNPF is a funded retirement account rather than central-government tax
revenue. `frac_tax_payroll` is 0.805503 in the first year and 0.823295
thereafter, based on the payroll wedge relative to the fitted PAYE yield, so
validation tables can report it separately. OG-Core still includes the wedge
in total household tax liabilities; this accounting limitation must be shown
explicitly in fiscal validation.

## Corporate and indirect taxes

The statutory CIT rate is 25%. Company-tax receipts are FJ$495.0 million in
the 2026–27 Budget Estimates, or 3.34% of GDP. The initial corporate
adjustment factor, 0.372898, maps that yield to the PWT capital-income share;
it remains provisional until matched to solved business-tax revenue.

Indirect taxes are FJ$2.232 billion, or 15.05% of GDP. Dividing by the World
Bank's 2024 household-consumption share of 70.38% gives
`tau_c=0.213793`. This intentionally includes VAT, customs and excise,
departure tax, and other indirect levies rather than setting `tau_c` equal to
the 12.5% statutory VAT rate.

Sources: [2026–27 Budget Estimates](https://www.parliament.gov.fj/wp-content/uploads/2026/06/2026-2027-Budget-Estimates.pdf),
[FRCS tax rates](https://frcs.org.fj/tax-rates-and-codes/), and
[World Bank household consumption](https://data.worldbank.org/indicator/NE.CON.PRVT.ZS?locations=FJ).

Fiji has no estate tax represented in this first pass, so `tau_bq=0`.
