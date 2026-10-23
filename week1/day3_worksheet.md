# Week 1 · Day 3 worksheet — Simple linear regression

## Learning objectives

**Chapter 8 — Introduction to Simple Linear Regression (source objectives):**

- Write the simple linear regression model and its assumptions.
- Derive the OLS estimators from scratch.
- Derive the variance of the OLS estimators.
- Show that R² equals the squared Pearson correlation.
- Implement and diagnose simple linear regression in scikit-learn.

**90-minute focus:** interpret the line, derive its OLS coefficients, fit the source's five-row example, and read a residual plot. The OLS-variance and `R² = r²` proofs are compact extensions if time permits.

**Vocabulary:** simple linear regression predicts a numeric target from one feature with a line. The *slope* is the fitted change in the mean target for a one-unit increase in the input; the *intercept* is the fitted mean at input zero, which may be meaningless outside the observed range. Ordinary least squares (OLS) minimises squared residuals. A *residual* is observed minus predicted; RMSE is a typical error size in target units. *Homoscedasticity* means constant error variance. `R²` (coefficient of determination) compares squared prediction error with a mean-only baseline; Pearson's `r` measures linear association. The *Hessian* is a matrix of second derivatives. In the optional identity, SST is total variation, SSR is regression-explained variation, and SSE is residual error.

## Concept recap

Simple linear regression connects one feature `X` to a numeric outcome `Y` with `Y = β₀ + β₁X + ε`. The fitted line is `Ŷ = β̂₀ + β̂₁X`; its slope estimates how the mean outcome changes for a one-unit increase in `X`, and its intercept estimates the mean at `X=0`. Do not give the intercept a real-world meaning if zero is outside the observed range. OLS chooses the line that minimises the sum of squared residuals, where each residual is `observed − predicted`.

The booklet groups assumptions under LINE: linearity in the parameters, independent observations, normal errors (needed for inference, not for point estimates), and equal error variance. A residual-versus-fitted plot is a diagnostic: a funnel suggests changing variance, curvature suggests the straight-line form misses structure, clusters may indicate subgroups, and isolated large residuals may be outliers. A pattern is a reason to investigate, not proof of causation. With an intercept, the OLS line passes through `(X̄, Ȳ)`, and in simple regression `R²` equals the squared Pearson correlation. A negative R² on held-out data means the model is worse than predicting the training mean; it is not a software error. In scikit-learn, `X` must be two-dimensional—even for one feature—and the fitted slope and intercept are stored in `coef_` and `intercept_`.

## Read the math

OLS minimises `S(b₀,b₁) = Σᵢ(Yᵢ − b₀ − b₁Xᵢ)²`. Differentiate with respect to both parameters and set the results to zero:

- `∂S/∂b₀ = −2Σᵢ(Yᵢ − b₀ − b₁Xᵢ) = 0`
- `∂S/∂b₁ = −2ΣᵢXᵢ(Yᵢ − b₀ − b₁Xᵢ) = 0`

The first equation gives `b₀ = Ȳ − b₁X̄`. Substitute this into the second equation and collect the slope terms:

`β̂₁ = Σᵢ(Xᵢ−X̄)(Yᵢ−Ȳ) / Σᵢ(Xᵢ−X̄)²`, and `β̂₀ = Ȳ − β̂₁X̄`.

For the booklet's five observations, `X=[1,2,3,4,5]` and `Y=[2.1,4.0,6.2,7.9,10.1]`. The means are `X̄=3` and `Ȳ=6.06`; the centered cross-product is `19.9`, and the centered sum of squares for `X` is `10`. Therefore `β̂₁=1.99`, `β̂₀=0.09`, and the prediction at `X=6` is `12.03`. The Hessian is positive definite when `X` varies, so these stationary values minimise the objective.

**Optional source derivations:** assume independent zero-mean errors with common variance `σ²`, and let `Sxx=Σ(Xᵢ−X̄)²`. Substituting `Yᵢ=β₀+β₁Xᵢ+εᵢ` into the slope formula gives `β̂₁=β₁+Σ(Xᵢ−X̄)εᵢ/Sxx`, hence `Var(β̂₁)=σ²/Sxx`. Since `Ȳ=β₀+β₁X̄+ε̄`, `β̂₀=β₀+ε̄−X̄Σ(Xᵢ−X̄)εᵢ/Sxx`; the two error terms have zero covariance because `Σ(Xᵢ−X̄)=0`, so `Var(β̂₀)=σ²(1/n+X̄²/Sxx)`. For simple OLS with an intercept, residuals are orthogonal to fitted values, giving `SST = SSR + SSE`; substituting the OLS slope yields `R² = [Σ(Xᵢ−X̄)(Yᵢ−Ȳ)]²/[Σ(Xᵢ−X̄)²Σ(Yᵢ−Ȳ)²] = r²`.

## Guided coding task 1 — fit the line and make one prediction

Complete `fit_simple_regression` and `predict_at` in `week1/day3_regression.py`. The fixed data matches the Chapter 8 scikit-learn example.

**Starter code**

```python
from week1.day3_regression import toy_data, fit_simple_regression, predict_at

X, y = toy_data()
model = fit_simple_regression(X, y)
print(f"slope={model.coef_[0]:.3f}")
print(f"intercept={model.intercept_:.3f}")
print(f"prediction_at_6={predict_at(model, 6):.3f}")
```

**Expected output**

```text
slope=1.990
intercept=0.090
prediction_at_6=12.030
```

## Guided coding task 2 — compute and interpret residuals

Complete `residual_report` in `week1/day3_regression.py`. Keep residual order aligned with the input rows.

**Starter code**

```python
from week1.day3_regression import toy_data, fit_simple_regression, residual_report

X, y = toy_data()
model = fit_simple_regression(X, y)
report = residual_report(y, model.predict(X))
print("residuals=" + str([round(float(v), 2) for v in report["residuals"]]))
print(f"rmse={report['rmse']:.3f}")
print(f"r2={report['r2']:.3f}")
```

**Expected output**

```text
residuals=[0.02, -0.07, 0.14, -0.15, 0.06]
rmse=0.101
r2=0.999
```

## Predict the output — live-quiz question `ch08_q02_predict_output`

For the fitted line `Ŷ = 0.09 + 1.99X`, what does the model predict when `X=6`?

- A. `2.08`
- B. `10.04`
- C. `12.03`
- D. `13.00`

**Correct answer:** C, because `0.09 + 1.99 × 6 = 12.03`.

## Where Students Get Stuck

Which residual in the five-row example is largest in absolute value, and what does its sign mean? Now interpret this separate residual-versus-fitted sketch: residuals are mostly negative at low fitted values, positive in the middle, then negative again at high fitted values. What should you investigate next, and what does the plot **not** prove? A suitable answer is that the curve suggests the straight-line form misses structure, so a polynomial feature is worth investigating with held-out data; the plot does not establish causation. Remember that scikit-learn expects `X.shape == (n_samples, 1)`, not a one-dimensional feature vector.

## Submission checklist

- [ ] Chapter 8 source objectives are present; the two statistical derivations are marked as optional extensions.
- [ ] `fit_simple_regression` returns a fitted `LinearRegression` estimator and matches the listed coefficients.
- [ ] `predict_at` reshapes one scalar into one sample with one feature.
- [ ] Residuals are `observed − predicted` and remain in row order.
- [ ] RMSE and R² match the expected output to three decimals.
- [ ] The residual-plot interpretation proposes a check and makes no causal claim.
- [ ] Commit `week1/day3_regression.py` and this worksheet.
