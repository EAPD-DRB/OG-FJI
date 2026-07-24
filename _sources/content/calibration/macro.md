(Chap_MacroCalib)=
# Calibration of Macroeconomic Parameters

## Economic Assumptions

### Growth rate of labor-augmenting technological change

$g_y$ is the model's long-run productivity growth rate. Derive it from average
annual real GDP-per-capita growth over a deliberately chosen window, set as
named constants in `ogfji/macro_params.py` with a written rationale: start the
window after a structural break, end it before the latest shock, and reject
unrepeatable booms.

For Fiji the window choice is not routine. Growth is dominated by tourism and is
highly volatile — the COVID collapse and the rebound that followed are both far
outside any sustainable long-run rate, and tropical cyclones produce repeated
sharp interruptions. A naive "all history" average, or a window that includes
the rebound years, will misstate $g_y$.

Critically, $g_y$ must be *consistent with the growth the `debt_ratio_ss` anchor
assumes*: in steady state GDP growth $\approx g_y + g_{n,ss}$. If the debt target
reflects a stabilization plan built on a medium-term recovery, use that
recovery's productivity growth, not a stagnant realized window. Pairing a
stagnant $g_y$ with a stabilization debt target is internally inconsistent, and
the model's debt will not hold at the target.

*Sources to use:* Fiji Bureau of Statistics national accounts; IMF Article IV
and World Economic Outlook for the medium-term path.

## Open Economy Parameters

Fiji is a small, open, tourism- and remittance-dependent Pacific island economy.
The open-economy block matters more here than for a large economy, and the
inherited Philippine values should not be assumed transferable.

### Foreign holding of government debt in the initial period

`initial_foreign_debt_ratio` — the initial-period share of government debt held
by foreign investors. The subsequent path is endogenous.

*Sources to use:* Fiji Ministry of Finance debt reporting; the IMF Article IV
debt-sustainability analysis (DSA).

### Foreign purchases of newly issued debt

$\zeta_D$ — the share of newly issued debt bought by foreigners. The standard
default is to set it equal to `initial_foreign_debt_ratio`, assuming the foreign
share of new issuance matches the foreign share of the stock. Use the DSA's
projected medium-term flow instead if the realized flow is a crisis-period
outlier, such as a donor surge or a debt standstill.

### Foreign holdings of excess capital

$\zeta_K$ — the share of the gap between domestically-supplied capital and the
capital demanded at the world interest rate that foreign investors fill. It is
effectively the degree of capital-account openness, and it is harder to pin down
than the debt parameters because purchases of "excess" capital demand are not
directly measured.

Anchor it to the normalized Chinn-Ito capital-account openness index for Fiji,
then cross-check the *level* against an independent target: the foreign share of
the capital stock in the Reserve Bank of Fiji's International Investment
Position, or the FDI stock relative to GDP.

```{warning}
Do not leave $\zeta_K$ at a high placeholder such as 0.9. That value drives
domestic capital $K_d = B - D_d$ toward zero, the $K_d \geq 0$ constraint binds
along the transition, and the resource constraint fails to close. This is a
recurring failure across the country models, not a hypothetical.
```

### World interest rate

`world_int_rate_annual` prices foreign capital and foreign debt in the
small-open-economy block. For an open, investment-grade sovereign, set it to a
global risk-free rate plus the country's sovereign spread. For a near-closed or
distressed sovereign, leave it at the risk-free benchmark and route country risk
through a low $\zeta_K$ and the debt-elastic premium instead — adding a spread
for a distressed sovereign is the wrong model. Decide which case Fiji is in and
document the choice.

*Sources to use:* Reserve Bank of Fiji; IMF Article IV; sovereign rating
reports.

### Remittances as a share of GDP

Remittance inflows are a large share of household income in Fiji, so leaving
this block off would produce a spurious trade surplus and an implausible fiscal
squeeze. $\alpha_{RM,1}$ governs the model's start period and $\alpha_{RM,T}$
the long run; set $\alpha_{RM,1} = \alpha_{RM,T}$ if no transition path is
wanted. Set the companion `eta_RM` household-distribution matrix as well —
remittances are not evenly distributed across lifetime-income groups. These are
hand-set JSON values, never fetched from an API.

*Sources to use:* Reserve Bank of Fiji balance-of-payments statistics; World
Bank remittance data as a cross-check.

## Government Debt, Spending and Transfers

### Government Debt

The path of government debt is endogenous; the initial value is exogenous.
Calibrate the initial debt-to-GDP *ratio* rather than a currency value, to avoid
converting between model units and Fiji dollars.

Two distinct parameters, often confused:

* `initial_debt_ratio` is *measured* — the actual current ratio.
* `debt_ratio_ss` is a *policy anchor* — the government's target or stance. It
  shapes the entire steady state and must not be left at an inherited value.

Check whether any jump in the measured ratio is a valuation effect (an exchange
rate movement revaluing external debt) rather than real deterioration.

*Sources to use:* Fiji Ministry of Finance debt bulletins and budget
documentation; IMF Article IV / DSA.

### Aggregate transfers and government expenditures

$\alpha_T$ is non-pension transfers as a share of GDP (pensions are modeled
separately). $\alpha_G$ is government spending on goods and services as a share
of GDP, defined as total outlays less transfers, net interest and pensions.
$\alpha_I$ is infrastructure spending as a share of GDP.

```{important}
These are not free parameters. For debt to hold at `debt_ratio_ss` in the steady
state, the government must run a primary balance
$pb^* = \frac{r_{gov} - g}{1 + g} \times$ `debt_ratio_ss`, where
$g = g_y + g_n$. Primary spending must therefore equal revenue less $pb^*$:

$$\alpha_G + \alpha_T \approx \sum(\text{tax revenue})/Y - pb^*$$

OG-Core's steady-state closure silently forces spending to the consistent level,
so **the steady state always solves and looks fine even when this identity is
violated**. The transition does not: it holds $\alpha_G + \alpha_T$ at their
input values for the first $t_{G1}$ periods, so an over-set spending side makes
debt balloon before the closure violently corrects it — and with a debt-elastic
premium enabled, that overshoot feeds the premium and the transition runs away.
Damping and better solvers do not fix this, because it is a fiscal
inconsistency, not a convergence artifact.
```

Note also that over-collecting taxes *masks* this inconsistency: a placeholder
tax rate set too high, or a stray nonzero tax the documentation claims is off,
inflates revenue and accidentally balances an over-set spending side. Audit
revenue by instrument against actual collections rather than checking only the
total.

*Sources to use:* Fiji Ministry of Finance budget estimates and the annual
Economic and Fiscal Update; IMF Article IV for the medium-term fiscal path.

### Government interest rate wedge

The rate the government pays, $r_{gov,t}$, differs from the household rate
$r_t$. OG-Core captures the level wedge and a debt-elastic premium together:

$$r_{gov,t} = \max\Big(r_{gov,scale} \cdot r_t - r_{gov,shift} + r_{gov,DY} \cdot \tfrac{D_t}{Y_t} + r_{gov,DY2} \cdot \big(\tfrac{D_t}{Y_t}\big)^2,\; 0\Big)$$

**Level wedge.** Keep the estimated sovereign-vs-corporate pass-through *slope*
($r_{gov,scale}$) from Li, Magud, Werner and Witte (2021), [The Long-Run Impact
of Sovereign Yields on Corporate Yields in Emerging
Markets](https://www.imf.org/en/Publications/WP/Issues/2021/06/04/The-Long-Run-Impact-of-Sovereign-Yields-on-Corporate-Yields-in-Emerging-Markets-50224)
(IMF WP/21/155), but **re-anchor the shift** so the steady-state $r_{gov}$
equals Fiji's actual real *effective* rate on debt — nominal debt service
divided by gross debt, less expected inflation.

The published intercept is a cross-country emerging-market average that maps a
nominal USD bond-yield level onto the model's real marginal product of capital.
It can over-predict a small island economy's real borrowing cost, which inflates
the debt-stabilizing primary surplus and forces spending implausibly low. Note
that $r_{gov}$ multiplies the *whole* debt stock in
$\text{debt service} = r_{gov} D$, so it is an average effective rate — do not
use a marginal new-issue yield.

**Debt-elastic premium.** The $r_{gov,DY}$ and $r_{gov,DY2}$ terms let the
sovereign rate rise with the debt ratio. Use the
[Schmitt-Grohé and Uribe (2003)](https://www.nber.org/system/files/working_papers/w9270/w9270.pdf)
premium in convex form, **centered on `debt_ratio_ss`** so it is exactly zero at
the target and prices only transition overshoot:

$$r_{gov,DY} = -2 \cdot r_{gov,DY2} \cdot \bar{D}, \qquad r_{gov,shift} = \text{base} - r_{gov,DY2} \cdot \bar{D}^2$$

where $\bar{D}$ is `debt_ratio_ss`. A premium that bites *at* the target instead
compounds any overshoot into a runaway debt-service feedback. If a live-refresh
path ever returns the raw un-recentered shift, it silently de-centers the
premium and moves the steady state — keep the value frozen in the JSON.

*Sources to use:* Fiji Ministry of Finance debt service and gross debt (for the
effective rate); Reserve Bank of Fiji for inflation expectations.
