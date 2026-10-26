# Week 1 · Day 4 worksheet — Multiple and polynomial regression

## Learning objectives

**Chapter 9 — Introduction to Multiple Linear Regression (source objectives):**

- Write the multiple regression model in scalar and matrix form.
- Derive the normal equations using matrix calculus.
- Derive the covariance matrix of the OLS estimator.
- Prove that perfect collinearity makes the design matrix singular.
- Derive the variance inflation factor.
- Diagnose and fix multicollinearity.

**Chapter 10 — Polynomial and Non-Linear Regression (source objectives):**

- Prove that polynomial regression is linear in parameters.
- Build polynomial regression pipelines in scikit-learn.
- Derive the Ridge regression closed-form solution.
- Derive the Lasso KKT conditions and coordinate-descent update.
- Derive the ElasticNet objective and its limiting cases.
- Diagnose overfitting with validation curves.

**Week 1 focus:** practise multiple-feature coefficients, the normal-equation idea, polynomial feature mapping, a Ridge pipeline, and train/validation discipline. The full covariance/VIF proofs and Lasso/ElasticNet derivations are optional extensions if the timetable is tight.

**Vocabulary:** a *coefficient* is a fitted weight; in multiple regression it describes the fitted change for one feature while the other included features are held fixed. *Multicollinearity* means features overlap in the information they carry. A *polynomial feature* is a power such as `x²`. *Regularisation* adds a penalty to discourage large coefficients. Ridge uses an L2 penalty; Lasso uses an L1 penalty and can set coefficients to zero. *KKT* means Karush–Kuhn–Tucker: conditions that characterize an optimum, including for a constrained or nondifferentiable objective.

## Concept recap

Multiple linear regression predicts a numeric target from several input columns. In scalar form, each coefficient describes the fitted change in the target for a one-unit change in that feature while the other included features stay fixed. This is not the same as fitting a separate simple regression for each column. In matrix form, the observations, augmented design matrix, and coefficients combine as `y = X̃β + ε`; ordinary least squares chooses coefficients that make squared residuals small. If two columns are perfectly dependent, the design matrix cannot identify a unique set of coefficients. Near-dependence makes the coefficient estimates unstable; variance inflation factor (VIF) is one warning measure. R² does not decrease when ordinary least squares gets extra features, so adjusted R² can help compare models of different sizes.

Polynomial regression adds terms such as `x²` and `x³`. The prediction can curve as `x` changes, yet the model remains linear in its coefficients. `PolynomialFeatures` creates the terms, and a scikit-learn `Pipeline` keeps transformations tied to the training data. A high degree can fit training points closely but behave poorly on new data; choose complexity with validation evidence, not training error alone. Ridge shrinks coefficients with an L2 penalty; Lasso uses L1 and can make some weights exactly zero; ElasticNet combines both. For this introductory session, practise the polynomial map and Ridge. Treat the full Lasso KKT and ElasticNet derivations as optional extensions, and do not interpret a selected coefficient as proof of causation.

## Read the math

For a multiple-regression design matrix `X̃` with a leading column of ones for the intercept, ordinary least squares minimizes

`S(β) = (y − X̃β)ᵀ(y − X̃β)`.

Expand and differentiate:

`S(β) = yᵀy − 2βᵀX̃ᵀy + βᵀX̃ᵀX̃β`,

`∇β S = −2X̃ᵀy + 2X̃ᵀX̃β`.

Setting the gradient to zero gives the **normal equations** `X̃ᵀX̃ β̂ = X̃ᵀy`. If `X̃ᵀX̃` is invertible, `β̂ = (X̃ᵀX̃)⁻¹X̃ᵀy`. Perfectly dependent feature columns make this inverse unavailable; correlated features can still make estimates unstable.

For one input, define `φ(x) = [1, x, x², …, xᵈ]ᵀ`. Then polynomial regression is `f(x; β) = φ(x)ᵀβ`. For any scalars `a,b` and coefficient vectors `β,γ`, `f(x; aβ+bγ) = a f(x; β) + b f(x; γ)`: it is linear in the fitted parameters even when its curve is nonlinear in `x`.

For the Ridge derivation, take `X` to be the predictor matrix without a constant column; the intercept is handled separately. The L2-penalised objective is `Sλ(β) = ||y−Xβ||²₂ + λ||β||²₂`. Its gradient is `−2Xᵀy + 2XᵀXβ + 2λβ`; setting it to zero yields `β̂ridge = (XᵀX + λI)⁻¹Xᵀy`. For the scikit-learn `Ridge` objective used here, `alpha` corresponds to `λ`; its separate intercept is not penalized.

**Optional source derivations (extension):** from `β̂OLS=(X̃ᵀX̃)⁻¹X̃ᵀy` and `y=X̃β+ε`, write `β̂OLS=β+(X̃ᵀX̃)⁻¹X̃ᵀε`. Thus, when `Var(ε)=σ²I`, `Var(β̂OLS)=A(σ²I)Aᵀ=σ²(X̃ᵀX̃)⁻¹`, with `A=(X̃ᵀX̃)⁻¹X̃ᵀ`. Under perfect collinearity, a nonzero vector `v` satisfies `X̃v=0`, so `β` and `β+tv` give identical predictions: coefficients are not uniquely identifiable. For feature `j`, regressing it on the other features gives `Rⱼ²`; only its residual variation remains to identify its coefficient, shrinking by `1−Rⱼ²`. Comparing its coefficient variance with the no-collinearity case gives `VIFⱼ=1/(1−Rⱼ²)`: large VIF signals overlap, not causation. With `p` predictors, `R²adj=1−(1−R²)(n−1)/(n−p−1)`.

For these regularized objectives, let `X` contain predictors only; fit the intercept separately and leave it unpenalized. For Lasso, use the scaled objective `(1/(2n))||y−Xβ||²₂ + λ||β||₁`. Its KKT condition is `Xⱼᵀ(y−Xβ)/n = λ sign(βⱼ)` when `βⱼ≠0`, and `|Xⱼᵀ(y−Xβ)/n|≤λ` when `βⱼ=0`. To derive the coordinate update, hold other coefficients fixed and let `rⱼ` be the residual excluding feature `j`; the one-variable objective is `(qⱼ/2)βⱼ²−zⱼβⱼ+λ|βⱼ|`, where `qⱼ=XⱼᵀXⱼ/n` and `zⱼ=Xⱼᵀrⱼ/n`. Minimising each sign region gives zero when `|zⱼ|≤λ`, otherwise `(zⱼ−λ sign(zⱼ))/qⱼ`; together this is soft-thresholding `βⱼ←Sλ(zⱼ)/qⱼ`, with `Sλ(z)=sign(z)max(|z|−λ,0)`. ElasticNet combines both penalties as `(1/(2n))||y−Xβ||²₂ + λ[ρ||β||₁+(1−ρ)||β||²₂/2]`; `ρ=1` gives Lasso and `ρ=0` Ridge. These results are reference extensions, not required for the two coding tasks.

## Guided coding task 1 — fit a multiple regression model

Use the first four rows for fitting and the final row as a held-out example. The target is constructed as `2 + 2x₁ + 3x₂`.

**Starter code**

```python
import numpy as np
from sklearn.linear_model import LinearRegression

X_train = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=float)
y_train = np.array([2, 4, 5, 7], dtype=float)
X_test = np.array([[2, 1]], dtype=float)
model = LinearRegression()
# TODO: fit on X_train/y_train, then print intercept, coefficients, prediction.
```

**Expected output**

```text
intercept=2.000
coefficients=[2.0, 3.0]
prediction=9.000
```

## Guided coding task 2 — polynomial features with a Ridge pipeline

**Starter code**

```python
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

X = np.arange(6, dtype=float).reshape(-1, 1)
y = X.ravel() ** 2 + 1
# TODO: split with test_size=2, random_state=7.
# Use include_bias=False because Ridge supplies an unpenalized intercept.
# TODO: model = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), Ridge(alpha=1.0))
# Fit on X_train/y_train; print split sizes, features for x=3, and prediction count.
```

**Expected output**

```text
train=4 test=2
features_at_3=[[3.0, 9.0]]
predictions=2
```

## Predict the output — worksheet self-check

For one input `x=3` and degree 2, what feature row does `PolynomialFeatures(include_bias=True)` produce?

- A. `[3, 9]`
- B. `[1, 3, 9]`
- C. `[1, 3]`
- D. `[1, 9, 27]`

**Correct answer:** B.

## Where Students Get Stuck

Explain why adding `x²` makes the prediction curve bend but keeps the model linear in its fitted coefficients. In multiple regression, why can adding a correlated feature change a coefficient's sign? Finally, why should degree be selected using validation evidence rather than the lowest training error?

## Submission checklist

- [ ] Chapter 9 and Chapter 10 objectives are included; the Week 1 focus is distinguished from optional extensions.
- [ ] Multiple regression uses two feature columns and interprets coefficients conditionally.
- [ ] The polynomial feature row for `x=3` is `[1, 3, 9]`.
- [ ] The train/test split happens before fitting the pipeline.
- [ ] Ridge is described as an L2-regularised model; Lasso/ElasticNet are preview/extension topics.
- [ ] Commit the worksheet and code to your assignment repository.
