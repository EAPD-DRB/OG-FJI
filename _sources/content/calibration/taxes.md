(Chap_Tax)=
# Taxes in OG-FJI

```{warning}
**Not yet calibrated to Fiji.** Every tax rate in the packaged parameter file is
the Philippine value inherited when this repository was ported from `OG-PHL`,
including rates tied to Philippine legislation. They must be replaced before any
OG-FJI result is meaningful. See `CALIBRATION_STATUS.md`.
```

The government is not an optimizing agent in `OG-FJI`. It levies taxes on
household income, corporate income, and consumption. With those resources it
provides transfers to households, spends on public goods, and makes rule-based
adjustments to stabilize the economy in the long run. It can run deficits or
surpluses in a given year and so must be able to accumulate debt or savings. The
spending and debt parameters are discussed in Chapter {ref}`Chap_MacroCalib`;
taxes are discussed here.

## The governing principle: effective, not statutory, rates

Every rate below should be calibrated as **actual collections divided by the
model-wide base**, not as the statutory rate. This matters for Fiji, where a
substantial share of activity is subsistence, informal, or otherwise outside the
tax net, so effective rates sit well below statutory ones.

Apply the principle *consistently across every instrument*. A common and costly
inconsistency in the country models is discounting personal income tax for
informality while leaving payroll or corporate tax at the full statutory rate.

## Personal income taxes

The government sector influences households through government transfers $TR_t$
and through the total tax liability function $T_{s,t}$, which decomposes into
the effective tax rate times total income as shown in the OG-Core
documentation.[^TaxEq]

```{math}
:label: EqHHBC
  c_{j,s,t} + b_{j,s+1,t+1} &= (1 + r_{hh,t})b_{j,s,t} + w_t e_{j,s} n_{j,s,t} + \\
  &\quad\quad\zeta_{j,s}\frac{BQ_t}{\lambda_j\omega_{s,t}} + \eta_{j,s,t}\frac{TR_{t}}{\lambda_j\omega_{s,t}} + ubi_{j,s,t} - T_{s,t}  \\
  &\quad\forall j,t\quad\text{and}\quad s\geq E+1 \quad\text{where}\quad b_{j,E+1,t}=0\quad\forall j,t
```

### Choosing the functional form

Three options, in increasing fidelity:

1. **Flat `linear`** — a single effective and marginal rate. Cheapest, no
   progressivity. Acceptable as a first pass, but see the warning below.
2. **Progressive parametric form fit to the statutory schedule** — genuine
   progressivity with *no microdata*. It needs only Fiji's statutory PIT
   schedule plus a collections target, so it is available now and is strongly
   preferred over flat-linear.
3. **Microdata-estimated nonlinear** — requires filer microdata and a
   Tax-Calculator equivalent. Not currently feasible for Fiji.

```{important}
Prefer **GS (Gouveia-Strauss)** over HSV. Set `tax_func_type = "GS"`, with
parameters $(\phi_0, \phi_1, \phi_2)$ and tax
$T(y) = \phi_0\,(y - (y^{-\phi_1} + \phi_2)^{-1/\phi_1})$ on total income.
Calibrate it as: $\phi_0$ = the statutory top marginal rate (an anchor, not a
fit); $\phi_1$ fit to the schedule's curvature; $\phi_2$ tuned in-model to the
PIT-to-GDP collections target, which is where the effective-rate and
informality wedge enters.

GS floors the effective rate at exactly zero, which is faithful wherever a
statutory threshold exempts the bottom of the distribution. HSV's effective rate
goes *negative* below the threshold, and that implicit bottom-end subsidy is not
cosmetic — in a sibling country model it drained transition revenue and helped
push the transition into a debt runaway where GS with the same targets
converged.
```

Note that `etr_params`, `mtrx_params` and `mtry_params` vary by period and age
only, never by lifetime-income group $j$; group heterogeneity enters through
each household's income arguments. `mtrx_params` is the marginal rate on
**labor** income and `mtry_params` the marginal rate on **capital** income — the
`x`/`y` naming is not mnemonic and is easy to get backwards.

`mean_income_data`, used in tax function estimation, must be set to mean
household income in Fiji dollars.

*Sources to use:* Fiji Revenue and Customs Service (FRCS) statutory schedules
and annual collections; Fiji Ministry of Finance revenue tables; Fiji Bureau of
Statistics Household Income and Expenditure Survey for mean income.

## Bequest and wealth taxes

Wealth taxes are set to zero by default. Set $\tau_{bq}$ to Fiji's actual estate
or inheritance tax treatment.

```{caution}
Check this value explicitly rather than inheriting it. A stray nonzero bequest
tax left over from a sibling repo silently collected several percent of GDP in
one country model while the documentation stated bequest tax was zero — and that
phantom revenue masked a spending-exceeds-revenue gap until someone fixed the
tax. Grep the packaged JSON for every nonzero tax the documentation claims is
off.
```

## Corporate income taxes

Set `cit_rate` from Fiji's statutory corporate rate, then adjust toward the
effective rate actually collected using `adjustment_factor_for_cit_receipts` and
`c_corp_share_of_assets`. Fiji operates tax incentives and concessionary regimes
in several sectors, so the collected rate will diverge from the headline rate.

*Sources to use:* FRCS collections by instrument; Ministry of Finance revenue
tables; the IMF Article IV tax-expenditure discussion.

## Consumption and indirect taxes

`tau_c` should capture **all** consumption and indirect taxes, not VAT alone —
in Fiji that means VAT together with the Service Turnover Tax, Environment and
Climate Adaptation Levy, departure tax, excises and customs duties, to the
extent they fall on household consumption. Calibrate as total indirect
collections divided by the consumption base.

## Informality

Choose the rung the data supports:

1. *Narrative only* — name informality as the reason effective rates sit below
   statutory ones, pick a stylized effective rate, and flag it as provisional.
2. *Structural two-sector* — use OG-Core's multi-industry machinery with an
   informal industry carrying `cit_rate = 0` and `tau_c = 0`. Requires a SAM,
   which Fiji does not yet have here.
3. *Household graded non-compliance* — set
   `labor_income_tax_noncompliance_rate` and `capital_income_tax_noncompliance_rate`
   by lifetime-income group, with the compliant-group effective rate solved from
   a revenue identity. Keep labor and capital non-compliance equal: OG-Core's
   steady-state diagnostic tiles the capital array from the labor one, and a
   mismatch produces a misleading diagnostic.

```{caution}
OG-Core's transition path applies year-0 compliance and filer values to the
whole path's revenue accounting. A *time-varying* compliance reform therefore
yields inconsistent transition revenue — behavior responds while revenue does
not. Steady states are fine. A formalization reform needs the upstream fix
first; the symptom is reform revenue tracking the baseline exactly while labor
supply moves.
```

## Footnotes

[^TaxEq]: See the online OG-Core documentation, Chapter ["Government"](https://pslmodels.github.io/OG-Core/content/theory/government.html), Section ["Effective and Marginal Tax Rates"](https://pslmodels.github.io/OG-Core/content/theory/government.html#effective-and-marginal-tax-rates), equation [(57)](https://pslmodels.github.io/OG-Core/content/theory/government.html#equation-eqtaxcalcliabetr2).
