# Macroeconomy and open-economy block

Long-run labor-augmenting productivity growth is set to 3.0% per year. This
uses the Fiji Government's 10-year baseline real-growth assumption and the
near-flat population path at the end of the IMF projection rather than a
short-run post-pandemic average.

`zeta_K=0.162432` is Fiji's normalized 2023
[Chinn–Ito capital-account openness index](https://web.pdx.edu/~ito/Chinn-Ito_website.htm).
The low value is consistent with Fiji's exchange-rate peg and capital-flow
measures; it should not be replaced by a foreign-capital stock share.

The world real interest rate is 4%. Country risk enters through low capital
openness and a centered debt-elastic government premium:

```text
r_gov = scale * r - shift + 0.04 * (D/Y - 0.80)^2
```

In OG-Core coefficients this is `r_gov_DY=-0.064`,
`r_gov_DY2=0.04`, and `r_gov_shift=-0.0378061`. At `D/Y=0.80` and
`r=0.04`, the implied government rate is 2.2%, matching the 4.7% weighted
nominal debt rate less 2.5% long-run inflation in Fiji's
[2026–27 Budget Supplement](https://www.finance.gov.fj/wp-content/uploads/2026/06/2026-2027-Budget-Supplement.pdf).
The intercept must be re-anchored after the steady state determines `r`.

Remittances are 7.1% of GDP, the World Bank's 2024 value on its
[Fiji country page](https://data.worldbank.org/country/fiji). They are held
constant as a GDP share in the first release.
