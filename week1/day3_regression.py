"""Student implementation file for the Week 1 Day 3 worksheet.

Implement the TODOs without changing the public function names.  The grader
imports these functions; the visible dataset is intentionally tiny and fixed.
"""
from __future__ import annotations

import numpy as np
from sklearn.linear_model import LinearRegression


def toy_data() -> tuple[np.ndarray, np.ndarray]:
    """Return five one-feature observations used in the worksheet."""
    x = np.array([1, 2, 3, 4, 5], dtype=float).reshape(-1, 1)
    y = np.array([2.1, 4.0, 6.2, 7.9, 10.1], dtype=float)
    return x, y


def fit_simple_regression(x: np.ndarray, y: np.ndarray) -> LinearRegression:
    """Fit and return an sklearn simple linear regression estimator."""
    # TODO: instantiate LinearRegression, fit it on x and y, and return it.
    raise NotImplementedError("Implement fit_simple_regression")


def predict_at(model: LinearRegression, x_value: float) -> float:
    """Return the fitted model's prediction for one scalar x value."""
    # TODO: reshape the scalar into one row/one feature before calling predict.
    raise NotImplementedError("Implement predict_at")


def residual_report(
    y_true: np.ndarray, y_pred: np.ndarray
) -> dict[str, np.ndarray | float]:
    """Return residuals, RMSE, and R-squared for one fitted model."""
    # TODO: residual = observed - predicted; use the same rows for all metrics.
    raise NotImplementedError("Implement residual_report")
