"""Session 2 starter: trace fit/transform/predict and keep test rows held out."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
y = np.array([2.0, 4.1, 5.9, 8.2, 10.0, 11.8])

# Keep X two-dimensional: shape (n_samples, n_features).
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)
model = make_pipeline(StandardScaler(), LinearRegression())
model.fit(X_train, y_train)  # Both learned steps see training rows only.
print("prediction:", round(float(model.predict([[7.0]])[0]), 2))
print("test score:", round(float(model.score(X_test, y_test)), 3))

# TODO: print X.shape and X_train.shape.
# TODO: explain why fitting StandardScaler on X before the split would leak data.
# Expected: X has two dimensions; do not compare exact split-dependent values
# after changing the random seed or input rows.
