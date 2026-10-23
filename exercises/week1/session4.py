"""Session 4 starter: multiple features and a polynomial pipeline."""

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

# Invented station example: two input features, one numeric target.
X = np.array([[1, 0], [2, 1], [3, 0], [4, 1], [5, 0], [6, 1]], dtype=float)
y = np.array([4, 7, 8, 13, 14, 21], dtype=float)

multiple = LinearRegression().fit(X, y)
print("multiple prediction:", round(float(multiple.predict([[3.5, 1]])[0]), 2))

# For a single feature, polynomial expansion adds x^2, x^3, ... as columns.
x = np.array([[1], [2], [3], [4], [5], [6]], dtype=float)
y_curve = np.array([2, 5, 10, 17, 26, 37], dtype=float)
polynomial = make_pipeline(
    PolynomialFeatures(degree=2, include_bias=False),
    StandardScaler(),
    Ridge(alpha=1.0),
)
polynomial.fit(x, y_curve)
print("degree-2 prediction:", round(float(polynomial.predict([[7]])[0]), 2))

# TODO: list the columns created by degree=2 for one feature.
# TODO: choose a degree with training/validation data, never by repeatedly
#       selecting the best test score.
