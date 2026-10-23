import numpy as np
from sklearn.linear_model import LinearRegression

from week1.day3_regression import (
    fit_simple_regression,
    predict_at,
    residual_report,
    toy_data,
)


def _fitted_model():
    x, y = toy_data()
    return x, y, fit_simple_regression(x, y)


def test_fit_returns_linear_estimator():
    x, y, model = _fitted_model()
    assert isinstance(model, LinearRegression)
    assert model.n_features_in_ == 1
    assert len(model.predict(x)) == len(y)


def test_coefficients_and_scalar_prediction():
    _, _, model = _fitted_model()
    assert np.isclose(model.coef_[0], 1.99, atol=1e-8)
    assert np.isclose(model.intercept_, 0.09, atol=1e-8)
    assert np.isclose(predict_at(model, 6), 12.03, atol=1e-8)


def test_residuals_and_rmse_use_observed_minus_predicted():
    x, y, model = _fitted_model()
    report = residual_report(y, model.predict(x))
    assert np.allclose(report["residuals"], [0.02, -0.07, 0.14, -0.15, 0.06])
    assert np.isclose(report["rmse"], np.sqrt(0.0102), atol=1e-8)


def test_r_squared_matches_toy_data():
    x, y, model = _fitted_model()
    report = residual_report(y, model.predict(x))
    assert np.isclose(report["r2"], 0.9987138101482901, atol=1e-8)
