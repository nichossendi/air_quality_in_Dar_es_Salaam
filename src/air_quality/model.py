"""AR model selection and walk-forward validation for PM2.5 forecasting."""

import pandas as pd


def baseline_mae(y_train: pd.Series) -> float:
    """Naive baseline: predict the training mean for every point."""
    raise NotImplementedError("Build in the modeling session")


def select_best_p(y_train: pd.Series, p_range: range) -> int:
    """Train AR(p) models across p_range, return the p with lowest training MAE."""
    raise NotImplementedError("Build in the modeling session")


def walk_forward_validate(y_train: pd.Series, y_test: pd.Series, best_p: int) -> pd.Series:
    """Walk-forward validation: retrain at each step using all history so far,
    forecast one step ahead, then append the true value to history before
    the next iteration.
    """
    raise NotImplementedError("Build in the modeling session")
