"""Student implementation file for the Week 1 Day 5 worksheet."""
from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def demo_data() -> tuple[np.ndarray, np.ndarray]:
    """Return a fixed two-feature, binary dataset with a rare positive class."""
    x = np.array(
        [
            [0.0, 0.0], [0.2, 0.1], [0.4, 0.0], [0.6, 0.2],
            [0.8, 0.1], [1.0, 0.0], [1.2, 0.3], [1.4, 0.2],
            [1.6, 0.4], [1.8, 0.3], [2.0, 0.5], [2.2, 0.4],
        ],
        dtype=float,
    )
    y = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], dtype=int)
    return x, y


def fit_logistic_demo() -> tuple[
    object, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
]:
    """Split, scale inside a pipeline, fit, and return the model and split."""
    x, y = demo_data()
    # TODO: stratified 2/3–1/3 split (random_state=7), then fit a pipeline
    # containing StandardScaler and LogisticRegression(max_iter=1000).
    raise NotImplementedError("Implement fit_logistic_demo")


def evaluate_binary(
    model: object, x_test: np.ndarray, y_test: np.ndarray, threshold: float = 0.5
) -> dict[str, np.ndarray | float]:
    """Return positive-class probabilities, predictions, matrix, precision, recall."""
    # TODO: use probability column 1; threshold explicitly; fix labels=[0, 1]
    # for the confusion matrix; set zero_division=0 for precision/recall.
    raise NotImplementedError("Implement evaluate_binary")
