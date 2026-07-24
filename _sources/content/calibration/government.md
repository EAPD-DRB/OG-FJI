(Chap_GovCalib)=
# Calibration of Government Parameters

The three spending shares below are set jointly with the debt anchor and the tax
system, not independently. Read the fiscal-consistency note in Chapter
{ref}`Chap_MacroCalib` before setting any of them: if $\alpha_G + \alpha_T$ is
inconsistent with the revenue the tax system raises and the primary balance that
`debt_ratio_ss` requires, the steady state will still solve and look fine while
the transition path diverges.

## Government Transfers as a Share of GDP

$\alpha_T$ is spending on transfer programs as a share of GDP, excluding
pensions, which OG-Core models separately. Take it from the functional
classification of the budget rather than as a residual.

*Sources to use:* Fiji Ministry of Finance budget estimates and the annual
Economic and Fiscal Update; the Fiji National Provident Fund for the boundary
between pensions and other social spending; World Bank World Development
Indicators as a cross-check only.

## Government Spending as a Share of GDP

$\alpha_G$ is government spending on goods and services as a share of GDP:

$$\text{Government spending} = \text{Total outlays} - \text{Transfers} - \text{Net interest on debt} - \text{Pensions}$$

OG-Core accepts a vector, so a short forecast path — for example the budget's
own forward estimates — can be supplied rather than a single value. Whatever is
used, subtract the calibrated $\alpha_T$ so the two do not double count.

*Sources to use:* Fiji Ministry of Finance budget estimates and forward
estimates; IMF Article IV for the medium-term fiscal path.

## Government spending on infrastructure as a share of GDP

$\alpha_I$ is public infrastructure investment as a share of GDP. It drives the
public capital stock, which enters production through $\gamma_g$.

```{note}
If $\gamma_g > 0$, set `initial_Kg_ratio` deliberately rather than inheriting
it. Solve the model's own steady-state law of motion

$$\bar{K}_g/\bar{Y} = \frac{(1-\varphi_g)\,\alpha_I}{e^{g_y}(1+g_n) - (1-\delta_g)}$$

and if the measured public capital stock is far above that sustainable level,
start at the measured value and let it depreciate toward the steady state. Fiji
carries substantial donor- and climate-resilience-financed infrastructure, so
the measured stock may sit above the level its own investment rate sustains.
```

*Sources to use:* Fiji Ministry of Finance capital budget; Asian Development
Bank and World Bank country infrastructure diagnostics.
