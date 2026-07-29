# Findings - Air Quality in Dar es Salaam

## Data

Hourly PM2.5 (`P2`) readings for site 11, sourced from MongoDB, localized to
`Africa/Dar_es_Salaam`, outliers (`P2 >= 100`) removed, resampled to hourly,
gaps forward-filled. Site 11 was selected as the site with the most complete
readings among the 3 available (11, 23, 29).

80/20 chronological train/test split — no shuffling, to respect time order
and avoid leaking future information into training.

## Exploratory analysis

- The raw time series shows a clear daily oscillation, and the 7-day rolling
  average confirms a longer weekly cycle on top of it.
- The ACF decays gradually, consistent with an autoregressive process.
- The PACF cuts off sharply after lag 2, consistent with the data's true
  underlying AR(2) structure.

## Model selection

- **Baseline** (predict the training mean for every point). Baseline MAE = 8.35.
- **AR order search**: trained `AutoReg` for lags 1 through 50, tracking
  training MAE at each order (`select_best_p` / `mae_by_lag` in
  `src/air_quality/model.py`). Training MAE keeps improving well past the
  PACF's lag-2 cutoff as expected, since more lag terms can always reduce
  training error by fitting noise, not just signal. The minimum lands at
  **p = 42** (training MAE ≈ 0.85), with both neighboring values (p=41,
  p=43) higher, a genuine interior minimum, not an artifact of stopping
  the search early.
- **Theory-informed alternative**: AR(2), matching the PACF cutoff and the
  data's true generating process. Training MAE ≈ 1.01.

## Held-out evaluation

Walk-forward validation (`walk_forward_validate` in `model.py`): at each
step of the test set, refit on all data seen so far, training data plus
every test point revealed up to that point, and forecast one step ahead.
This is an expanding-window, one-step-ahead evaluation, not a single static
forecast from the end of training.

| Model | Training MAE | Test MAE (walk-forward) |
|---|---|---|
| AR(42) — MAE-minimizing | 0.85 | 0.90 |
| AR(2) — PACF-informed | 1.01 | 1.06 |

A Diebold-Mariano test on the two forecasts' loss differentials (h=1, MAE
loss) gives **DM = -8.75, p < 0.0001**: the gap is statistically significant,
not sampling noise.

**Conclusion**: despite the data's true order being 2, AR(42) generalizes
about as well as it fits in-sample (~0.05 MAE degradation from train to
test, same size as AR(2)'s degradation) and remains the more accurate model
on unseen data. The PACF-cutoff intuition about the *generating process*
held up, but it didn't translate into "the simpler model wins" for
forecasting accuracy on this dataset. The extra lag terms cost little in
variance given the size of the training set, and may be partially absorbing
daily/weekly seasonal structure that a bare AR(2) can't represent on its
own.

Residual diagnostics (histogram, ACF) for both fitted models look reasonably
well behaved on the training set, but that is expected of any fitted model
on its own training residuals and is not by itself evidence of good
generalization. The walk-forward comparison above is what the model choice
is actually based on.