# Firms

The model uses one Cobb–Douglas production industry. Penn World Table 11.0
reports Fiji's adjusted labor share at 0.48863 in 2023, so the private capital
share is:

```text
gamma = 1 - 0.48863 = 0.51137
```

Source: [PWT labor share for Fiji via FRED](https://fred.stlouisfed.org/series/LABSHPFJA156NRUG).
The PWT adjustment is preferred to treating gross operating surplus plus mixed
income as pure capital income.

`gamma_g=0`, `alpha_I=0`, and `initial_Kg_ratio=0` in this first pass. Public
capital should be added only with a separately documented production and stock
calibration.
