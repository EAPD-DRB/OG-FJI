---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(Chap_LfEarn)=
# Lifetime Earnings Profiles

Among households in `OG-FJI`, we model variations in the labor productivity over the lifecycle and between households of different skill groups. Together, these variations in productivity generate a distribution of earnings that is calibrated to match the level of inequality in Fiji. This chapter describes the calibration of the lifecycle earnings profiles and the distribution of earnings in the model.

Differences among workers' productivity is one of the key dimensions of heterogeneity to model in a micro-founded macroeconomy. In this chapter, we characterize this heterogeneity as deterministic lifetime productivity paths to which new cohorts of agents in the model are randomly assigned. In `OG-FJI`, households' labor income comes from the equilibrium wage and the agent's endogenous quantity of labor supply. In this section, we augment the labor income expression with an individual productivity $e_{j,s}$, where $j$ is the index of the ability type or path of the individual and $s$ is the age of the individual with that ability path.

```{math}
:label: EqLaborIncome
  \text{labor income:}\quad x_{j,s,t}\equiv w_t e_{j,s}n_{j,s,t} \quad\forall j,t \quad\text{and}\quad E+1\leq s\leq E+S
```

In this specification, $w_t$ is an equilibrium wage representing a portion of labor income that is common to all workers. Individual quantity of labor supply is $n_{j,s,t}$, and $e_{j,s}$ represents a labor productivity factor that augments or diminishes the productivity of a worker's labor supply relative to average productivity.

We calibrate the model such that each lifetime income group has a different life-cycle profile of earnings. Since the distribution on income and wealth are key aspects of our model, we calibrate these processes so that we can represent earners in the top 1 percent of the distribution of lifetime income.

We calibrate deterministic productivity paths such that each lifetime income group has a different life-cycle profile of earnings. The distribution of income and wealth are often focal components of macroeconomic models. These calibrations require the use of microeconomic data on household incomes, but this level of data is not readily available for Fiji from public sources or surveys. To overcome this, we start with the proposition that estimated productivity curves calibrated for the [OG-USA](https://pslmodels.github.io/OG-USA/content/calibration/earnings.html) model, generated from micro-level earnings data, represent a generalized relationship between age and lifetime income {cite}`DeBackerEtAl:2017`. As such, our objective is to generate the curves for the U.S. and then adjust their generalized shapes to produce those for Fiji. In other words, our strategic approach is to begin with the lifecycle labor productivity profiles estimated from detailed U.S. data and then adjust these to match the distribution of income in Fiji, as measured with the Gini coefficient. This is done by finding the value of $a$, such that:

```{math}
  :label: eqnEarningsCalib
    e^{FJI} = e^{USA} * exp^{(a * e^{USA})}
```

and where $e^{FJI}$, when applied to the population distribution of Fiji, returns a Gini coefficient that matches the target Gini for Fiji. The tilt is solved in `ogfji/income.py`, and the target is the module constant `GINI_TO_MATCH`.

`GINI_TO_MATCH` is currently **30.7**, Fiji's most recent World Bank estimate (2019, series `SI.POV.GINI`), built from the Household Income and Expenditure Survey.

```{warning}
**Welfare-concept mismatch.** The tilt is solved against a US anchor of
`gini_usa_data = 41.5`, which is the World Bank's **income**-concept Gini for
the United States. Fiji's 30.7 is a **consumption**-concept Gini, and
consumption Ginis run materially below income Ginis for the same economy.
Matching one against the other understates Fijian inequality and flattens the
calibrated $e$ matrix.

Before this is used for published results, replace `GINI_TO_MATCH` with an
income-concept Gini for Fiji — from WID, or an income-based tabulation of the
Fiji Bureau of Statistics HIES — so that both sides of the ratio are the same
welfare concept. This is a known trap across the country models, not a
Fiji-specific quirk.
```

The $\boldsymbol{\lambda}$ lifetime-income group shares are the family-standard $J=7$ values and are not re-derived per country. The `factor` parameter is solved endogenously in the steady state and is not a calibration input.

```{figure} ./images/ability_profiles.png
---
height: 350px
name: FigLogAbil
---
Exogenous life cycle income ability paths $\log(e_{j,s})$ with $S=80$ and $J=7$
```

{numref}`Figure %s <FigLogAbil>` shows a calibration for $J=7$ deterministic lifetime ability paths $e_{j,s}$ corresponding to labor income percentiles $\boldsymbol{\lambda}=[0.25, 0.25, 0.20, 0.10, 0.10, 0.09, 0.01]$. Because there are few individuals above age 80 in the data, {cite}`DeBackerEtAl:2017` extrapolate these estimates for model ages 80-100 using an arctan function.
