(Chap_HouseholdCalib)=
# Calibration of Household Preference Parameters

## Behavioral Assumptions

The preference parameters below are taken from the literature rather than from
Fijian data, and are the same across the OG-Core country models. They are not
country-specific and need no re-derivation for Fiji.

### Elasticity of labor supply

As discussed in the [OG-Core household theory documentation](https://pslmodels.github.io/OG-Core/content/theory/households.html),
we use the elliptical disutility of labor function developed by
{cite}`EvansPhillips:2017`. We then fit the parameters of the elliptical utility
function to match the marginal disutility from a constant Frisch elasticity
function. `OG-FJI` users enter the constant Frisch elasticity as a parameter.
{cite}`Peterman:2016` finds a range of Frisch elasticities estimated from
microeconomic and macroeconomic data, from 0 to 4. Peterman makes the case that
in lifecycle models without an extensive margin for employment the Frisch
elasticity should be higher. For `OG-FJI` we take a default value of 0.4 from
{cite}`Altonji:1986`.

### Intertemporal elasticity of substitution

The default value for the intertemporal elasticity of substitution, $\sigma$, is
taken from {cite}`ABMW:1999`. We set $\sigma = 1.5$.

### Rate of time preference

We take our default value for the rate of time preference parameter, $\beta$,
from {cite}`Carroll:2009`. We set the value to $\beta = 0.96$ on an annual basis.

### Frisch elasticity of labor supply

We take our default value for the Frisch elasticity of labor supply as
$\nu = 0.25$. This value was estimated by {cite}`McNelisEtAl:2009` (see p. 19).

## Disutility of labor ($\chi^n_s$)

```{important}
$\chi^n_s$, the 80-age profile of the disutility of labor, is **borrowed from
OG-USA and is not calibrated to Fiji**. This is the honest default state of
every country port in this family — the estimation machinery is broken or absent
across the repositories — and it is stated here rather than left implicit.

To actually calibrate it, either re-tilt the profile by a single scalar to match
an aggregate hours or labour-force-participation target (analogous to the
earnings Gini tilt in Chapter {ref}`Chap_LfEarn`), or wire the Fiji Bureau of
Statistics labour force survey through a real estimation routine.
```

## Remittances

Remittances are a large and persistent component of household income in Fiji,
driven by long-standing outward migration and by seasonal-worker schemes to
Australia and New Zealand. Leaving this block uncalibrated would produce a
spurious trade surplus and an implausible fiscal position.

Three things to set:

* $\alpha_{RM,1}$ — aggregate remittances as a share of GDP in the model's start
  period.
* $\alpha_{RM,T}$ — the long-run/steady-state share. Set equal to
  $\alpha_{RM,1}$ if no transition path is intended.
* $g_{RM}$ — the growth rate of remittances between the start period and
  $t_{G1}$.

Set the companion `eta_RM` matrix too, which distributes remittances across
lifetime-income groups and ages. A uniform distribution is a strong and probably
wrong assumption.

The theory is documented in the OG-Core chapter
["Remittances"](https://pslmodels.github.io/OG-Core/content/theory/households.html#remittances).

*Sources to use:* Reserve Bank of Fiji balance-of-payments and remittance
statistics; Fiji Bureau of Statistics Household Income and Expenditure Survey
for the distribution across households; World Bank remittance data as a
cross-check.
