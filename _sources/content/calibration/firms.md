(Chap_FirmCalib)=
# Calibration of Firms Parameters

## Aggregate Production Function and Capital Accumulation

The [OG-Core firm theory documentation](https://pslmodels.github.io/OG-Core/content/theory/firms.html)
outlines the constant-returns-to-scale, constant-elasticity-of-substitution
production function of the representative firm. This function has two
parameters: the elasticity of substitution and capital's share of output.

### Elasticity of substitution

`OG-FJI`'s default parameterization has an elasticity of substitution of
$\varepsilon = 1.0$, which implies a Cobb-Douglas production function. This is
the family-wide default and is not country-specific.

### Capital's share of output

The baseline method is $\gamma = 1 - \text{labor share}$, taking the labor share
from ILOSTAT or Fiji Bureau of Statistics national accounts, and then carving
the public capital share $\gamma_g$ out of the *capital* side rather than the
labor side.

```{important}
For Fiji, the raw labor share is likely to be biased. A large share of activity
is subsistence agriculture, informal, and own-account work, and the mixed income
of the self-employed is booked as operating surplus — that is, as capital
income. This is the standard Gollin bias, and it inflates the measured capital
share.

Two ways to correct it, in increasing rigor:

* *Aggregate triangulation.* Adjust the economy-wide labor share upward using
  non-circular evidence: a growth-accounting check that $\gamma = (r + \delta)(K/Y)$
  implies a plausible return, the direction-of-bias argument from Gollin, and
  country institutions — for Fiji, communal (*iTaukei*) land tenure means a
  substantial part of land rent is not a private corporate return. State the
  result as a range with a center, not a false point estimate.
* *Cross-sectional rescale.* Only available with a SAM: keep the per-industry
  dispersion but rescale so the value-added-weighted mean equals the
  economy-wide capital share.
```

```{caution}
Do not let $\gamma$ be refreshed from a live API. The `update_from_api=True`
path in sibling repos recomputed the naive $1 - \text{ILOSTAT}$ labor share and
silently clobbered a hand-triangulated value, undoing the whole argument above.
Curated structural parameters must be removed from the live path entirely — an
`if update_from_api` guard is not enough. `ogfji/macro_params.py` is written this
way deliberately; keep it that way.
```

*Sources to use:* ILOSTAT labor-income share; Fiji Bureau of Statistics national
accounts and the labour force survey for the self-employment share; Penn World
Table for the capital-output ratio used in the growth-accounting cross-check.
