"""AR model selection and walk-forward validation for PM2.5 forecasting."""

import pandas as pd
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.ar_model import AutoReg


def baseline_mae(y_train: pd.Series) -> float:
    """Naive baseline: predict the training mean for every point."""

    y_pred_baseline = len(y_train) * [y_train.mean()]

    return mean_absolute_error(y_train, y_pred_baseline)


def mae_by_lag(y_train: pd.Series, p_range: range) -> pd.Series:
    """Train AR(p) for every p in p_range, return training MAE indexed by p."""

    maes = []

    for p in p_range:
        ar = AutoReg(
            y_train,
            lags = p,
            old_names = False).fit()
        
        y_pred = ar.predict()
        mae = mean_absolute_error(y_train.iloc[p:], y_pred.iloc[p:])
        maes.append(mae)

    return pd.Series(maes, name="mae", index=p_range)


def select_best_p(y_train: pd.Series, p_range: range) -> int:
    """Train AR(p) models across p_range, return the p with lowest training MAE."""

    return int(mae_by_lag(y_train, p_range).idxmin())


def walk_forward_validate(y_train: pd.Series, y_test: pd.Series, best_p: int) -> pd.Series:
    """Walk-forward validation: retrain at each step using all history so far,
    forecast one step ahead, then append the true value to history before
    the next iteration.

    Returns predictions indexed by the real forecast timestamps (not a bare
    0..n range), so the result lines up index-for-index with y_test and can
    be safely checked with y_pred.index.equals(y_test.index) rather than
    relying on both series happening to be in the same order.
    """
    
    y_pred = pd.Series(dtype="float64")
    history = y_train.copy()

    for i in range(len(y_test)):
        model = AutoReg(
            history,
            lags = best_p,
            old_names = False).fit()
        
        next_pred = model.forecast()
        y_pred = pd.concat([y_pred, next_pred])
        history = pd.concat([history, y_test.iloc[[i]]])

    y_pred.name = "prediction"

    return y_pred
