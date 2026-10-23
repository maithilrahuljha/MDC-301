"""Session 3 starter: simple OLS and a residual check."""

import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1], [2], [3], [4], [5]], dtype=float)
y = np.array([2.1, 4.0, 6.2, 7.9, 10.1])

model = LinearRegression(fit_intercept=True).fit(X, y)
prediction_at_6 = model.predict([[6]])[0]
residuals = y - model.predict(X)

print(f"slope={model.coef_[0]:.2f}")
print(f"intercept={model.intercept_:.2f}")
print(f"prediction_at_6={prediction_at_6:.2f}")
print("residuals:", np.round(residuals, 2).tolist())

# Expected: slope=1.99, intercept=0.09, prediction_at_6=12.03.
# TODO: explain why predicting at x=6 is extrapolation for these five rows.
# Optional with Matplotlib: plot residuals against fitted values and look for shape.
