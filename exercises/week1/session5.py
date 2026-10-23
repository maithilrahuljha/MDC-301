"""Session 5 starter: scaled logistic regression and classification metrics."""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Invented binary labels; do not substitute private/student data.
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]], dtype=float)
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(solver="lbfgs", max_iter=1000, C=1.0),
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]

print("probabilities between 0 and 1:", bool(np.all((y_probability >= 0) & (y_probability <= 1))))
print("confusion matrix:")
print(confusion_matrix(y_test, y_pred))
print("precision:", round(float(precision_score(y_test, y_pred, zero_division=0)), 3))
print("recall:", round(float(recall_score(y_test, y_pred, zero_division=0)), 3))

# TODO: explain why accuracy alone can hide a rare-positive failure.
# TODO: choose any decision threshold on validation data, not on y_test.
