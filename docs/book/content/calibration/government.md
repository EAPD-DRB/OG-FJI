# Government, debt, and spending

The initial central-government debt ratio is 82.1% of GDP at end-July 2026.
External debt is 34.7% of the stock, so both
`initial_foreign_debt_ratio` and `zeta_D` are 0.347. The steady-state
`debt_ratio_ss=0.80` is a policy anchor, not a claim that current debt already
equals the target. The 80% target is described in the fiscal-strategy
discussion in the [IMF 2026 Article IV report](https://www.imf.org/-/media/files/publications/cr/2026/english/1fjiea2026001.pdf).

The long-run spending closure uses the IMF FY2030–31 projection:

- tax revenue: 24.5% of GDP;
- foreign grants: 0.5%;
- primary expenditure: 26.0%;
- transfers: 7.5%.

Therefore `alpha_T=0.075` and `alpha_G=0.185`. Because the public-capital
block is off, `alpha_G` includes both current non-transfer purchases and
capital expenditure. This produces the -1% primary balance consistent with a
stable high-debt economy when the real debt cost remains below real growth.

The transition path must still be checked against the full government budget
identity before policy use.
