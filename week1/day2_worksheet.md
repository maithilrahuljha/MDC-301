# Week 1 · Day 2 worksheet — Tools, estimators, and regression

## Learning objectives

**Chapter 5 — Tools for Machine Learning (source objectives):**

- Describe the four layers of a practical ML stack.
- Choose the right tool for each layer.
- Set up a reproducible Python environment.
- Avoid tool churn and premature optimisation.

**Chapter 6 — Scikit-learn Machine Learning Ecosystem (source objectives):**

- Use the estimator API the same way across model families.
- Tell transformers and predictors apart.
- Build pipelines that prevent data leakage.
- Use cross-validation and grid search correctly.

**Chapter 7 — Introduction to Regression (source objectives):**

- State the regression problem clearly.
- Explain why linear regression is the right place to start.
- Describe the bias–variance trade-off in regression.
- Compute and interpret MSE, RMSE, MAE, and R².

**Vocabulary:** an *API (application programming interface)* is the documented functions and methods a library exposes for other programs to use. An *estimator* is a model object with a shared scikit-learn interface; `fit` learns settings from data; a *transformer* learns/applies an input transformation; a *predictor* returns estimates. A *pipeline* chains transformations and a predictor. *Cross-validation* repeats train/validation splits to estimate performance. A *hyperparameter* is a setting chosen before fitting. *Data leakage* occurs when held-out information influences fitting or model choice.

## Concept recap

A practical ML toolkit has layers. NumPy and pandas help represent and inspect data; scikit-learn provides classical models and preprocessing; deep-learning libraries serve other model families; deployment tools package or serve a model. Start with the smallest tool set that solves the task, and keep a project-specific Python environment so package changes do not unexpectedly break another project.

Scikit-learn uses a consistent estimator interface. A predictor's `fit(X, y)` learns from examples and `predict(X)` returns estimates; learned settings often have names ending in an underscore, such as `coef_`. A transformer such as `StandardScaler` learns transformation settings with `fit` and applies them with `transform`. A pipeline joins transformers to a final predictor, so preprocessing is learned from training data and applied consistently to new rows. Split first; do not fit a scaler on the full dataset. Cross-validation rotates validation folds, while grid search compares selected hyperparameter values inside that process. Keep the test set for the final evaluation.

Regression predicts a numeric target. MSE squares errors, RMSE takes the square root so the result is in target units, and MAE uses absolute errors. R² compares a model with a mean-only baseline and can be negative on held-out data. A simple linear model is a useful first case because its parameters and errors are easy to inspect. The bias–variance idea explains why a model can be too simple or too sensitive to its training sample; neither training score nor a library name alone tells us whether the model will generalise.

## Read the math

Chapter 7 derives the **bias–variance decomposition**. Fix an input `x`; write the outcome as `y = f(x) + ε`, where `E[ε]=0` and `Var(ε)=σ²`. Let `f̂_D(x)` be a model prediction that changes with the training dataset `D`. Add and subtract its average prediction:

`y − f̂_D = [f(x) − E_D f̂_D] + [E_D f̂_D − f̂_D] + ε`.

Square both sides and take expectation over training sets and noise. The cross-terms vanish because the model fluctuation is centred and the noise has mean zero and is independent. The remaining terms are

`E[(y − f̂_D)²] = [f(x) − E_D f̂_D]² + E[(f̂_D − E_D f̂_D)²] + σ²`.

These are **bias² + variance + irreducible noise**. The decomposition is an explanation of expected error across possible training sets, not a score computed from one split. For a single test set, also report its metrics honestly: `MSE = (1/n)Σ(yᵢ−ŷᵢ)²`, `RMSE = √MSE`, and `MAE = (1/n)Σ|yᵢ−ŷᵢ|`.

## Guided coding task 1 — fit an estimator and predict

**Starter code**

```python
from sklearn.linear_model import LinearRegression

X_train = [[1], [2], [3]]
y_train = [2, 4, 6]
model = LinearRegression()
# TODO: fit on the training examples and predict for [[4]].
```

**Expected output**

```text
[8.]
```

## Guided coding task 2 — split first, then fit a pipeline

**Starter code**

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X = np.array([[1], [2], [3], [4], [5], [6]], dtype=float)
y = np.array([2, 4, 6, 8, 10, 12], dtype=float)
# TODO: split with test_size=2 and random_state=7.
# TODO: fit a pipeline with StandardScaler then LinearRegression on X_train only.
# Print train/test sizes, pipeline step names, and number of predictions.
```

**Expected output**

```text
train=4 test=2
pipeline_steps=['standardscaler', 'linearregression']
predictions=2
```

## Predict the output — worksheet self-check

After fitting `X_train = [[1], [2], [3]]` and `y_train = [2, 4, 6]` with `LinearRegression`, what does this line print?

```python
print(model.predict([[4]]))
```

- A. `[4.]`
- B. `[8.]`
- C. `[6.]`
- D. It returns the fitted coefficients instead of a prediction.

**Correct answer:** B. The fitted line has slope 2 and intercept 0; the display may be `[8.]` or `[8.0]` depending on the numeric representation.

## Where Students Get Stuck

What is the difference between `fit`, `transform`, and `predict`? Explain why splitting first and using a pipeline prevents test-set leakage. A final version check: scikit-learn maximises cross-validation scores, so `neg_mean_squared_error` is negative; multiply by `-1` before taking its square root to report RMSE.

## Submission checklist

- [ ] The source objectives for Chapters 5–7 are present; deep-learning tools and hyperparameter search remain brief previews.
- [ ] The first estimator is fitted on training rows and predicts a new row.
- [ ] The pipeline is fitted only on `X_train` and transforms the test rows consistently.
- [ ] The split uses `random_state=7` and prints the expected sizes.
- [ ] The bias–variance terms and regression metrics are named correctly.
- [ ] Commit the worksheet and code; keep the random seed in the repository.
