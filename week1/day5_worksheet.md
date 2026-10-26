# Week 1 · Day 5 worksheet — Logistic regression for classification

## Learning objectives

**Chapter 11 — Introduction to Logistic Regression (source objectives):**

- Explain why linear regression is unsuitable for binary classification.
- Derive the sigmoid function and its key properties.
- Derive the logit (log-odds) transformation.
- Derive the softmax function for multiclass classification.
- Interpret log-odds and odds ratios.
- Choose decision thresholds appropriate to the application.

**Chapter 12 — Training a Logistic Regression Model (source objectives):**

- Derive the log-loss from maximum likelihood.
- Derive the gradient and Hessian of the log-loss.
- Derive Newton’s method and the IRLS update.
- Derive the gradient descent update and its convergence conditions.
- Derive the regularised logistic regression objective.
- Diagnose and fix convergence warnings.
- Choose and interpret classification metrics beyond accuracy.
- Tune decision thresholds for imbalanced problems.

**Week 1 focus:** understand sigmoid probability, log-odds, the Bernoulli-likelihood-to-log-loss connection, leakage-safe fitting, a stated threshold, and confusion-matrix/precision/recall interpretation. Gradient/Hessian, Newton/IRLS, softmax, and full threshold-tuning derivations are optional extensions if the 90-minute block is tight.

**Vocabulary:** *classification* predicts a category; logistic regression maps a weighted score through a *sigmoid* to an estimated probability between 0 and 1. A *Bernoulli* variable is a binary outcome taking values 0 or 1. *Odds* are `p/(1−p)`; *log-odds* are their natural logarithm. An *odds ratio* is the multiplicative change in odds for a one-unit feature change; for coefficient `βⱼ`, it is `e^(βⱼ)`. *Maximum-likelihood estimation* chooses parameters that make the observed labels most probable. A *threshold* converts probability into a class decision. A *confusion matrix* counts true/false positives and negatives. The *positive class* is the category designated as 1. *Precision* asks what share of predicted positives were correct; *recall* asks what share of actual positives were found. The *gradient* collects first derivatives; the *Hessian* collects second derivatives; *IRLS* (iteratively reweighted least squares) is a Newton-style way to fit logistic regression by repeatedly solving weighted least-squares problems.

## Concept recap

Logistic regression is a classification method even though “regression” appears in its name. A plain linear-regression output can fall outside `[0,1]` and squared numeric error does not match binary labels, so it is unsuitable as a class probability. Logistic regression starts with a weighted sum of features, then applies the sigmoid so the result is a probability between zero and one. The sigmoid is symmetric around `0.5`, and its derivative is `σ(z)(1−σ(z))`. Taking the log of the odds reverses the sigmoid: the model assumes the positive class’s log-odds are a linear combination of the features. A coefficient therefore changes log-odds, not probability by a fixed amount; exponentiating it gives an odds ratio.

The probability is not yet a class decision. A threshold such as `0.5` is a choice tied to the relative cost of false positives and false negatives; it can be changed, but choose it using validation data rather than the final test set. The model learns its weights by maximising the likelihood of the observed binary labels, or equivalently minimising negative log-likelihood (log-loss). A scikit-learn pipeline can scale features on training data only before fitting `LogisticRegression`, reducing leakage and helping the solver converge. Inspect convergence warnings rather than ignoring them.

After fitting, report more than accuracy. A confusion matrix shows which mistakes occurred; precision and recall focus on the designated positive class. If positives are rare, accuracy can look high while the model misses nearly all of them. The metric and threshold should match the problem, and any threshold tuning belongs on validation data.

## Read the math

For score `z = β₀ + β₁x₁ + … + βₚxₚ`, the sigmoid is `p = σ(z) = 1/(1+e^(−z))`. Since `e^(−z)>0`, `0<p<1`. Differentiating gives `σ′(z)=σ(z)(1−σ(z))`. To invert the sigmoid, start from `p=1/(1+e^(−z))`; rearranging gives `p/(1−p)=eᶻ`, so

`log(p/(1−p)) = z = β₀ + β₁x₁ + … + βₚxₚ`.

Thus logistic regression is linear in log-odds. For multiple classes, the optional softmax extension is `P(Y=k|x)=eᶻᵏ/Σⱼeᶻʲ`, where `zₖ` is the model's score for class `k`; its class probabilities sum to one.

For binary labels `yᵢ∈{0,1}`, let `pᵢ=σ(xᵢᵀβ)`. The likelihood is

`𝓛(β) = ∏ᵢ pᵢʸⁱ(1−pᵢ)^(1−yᵢ)`.

Taking logs changes the product into a sum. Maximising that log-likelihood is the same as minimising its negative:

`𝓙(β) = −ℓ(β) = −Σᵢ[yᵢ log(pᵢ) + (1−yᵢ)log(1−pᵢ)]`.

This is binary log-loss (cross-entropy); a confident wrong probability receives a large penalty. **Optional solver results:** let `X` include the intercept column, `p̂=σ(Xβ)`, and `W=diag(p̂ᵢ(1−p̂ᵢ))`. Then `∇β𝓙=Xᵀ(p̂−y)` and `H=XᵀWX`, a positive-semidefinite Hessian. Newton's step is `βnew=β−(XᵀWX)⁻¹Xᵀ(p̂−y)` when the inverse exists; line search (adjusting step size) or damping (adding a stabilising term) can make updates safer. The equivalent IRLS pseudo-response is `z=Xβ+W⁻¹(y−p̂)`, followed by weighted least squares `βnew=(XᵀWX)⁻¹XᵀWz`. Gradient descent uses `β(t+1)=β(t)−ηXᵀ(p̂−y)`. Since each diagonal weight is at most `1/4`, a sufficient full-batch step-size bound is `0<η<2/L`, with `L≤||X||₂²/4` (`||X||₂` is the spectral norm, or largest singular value); feature scaling helps conditioning.

A common L2-regularised objective is `𝓙λ(β)=𝓙(β)+(λ/2)||βfeatures||₂²`, excluding the intercept; the gradient gains `λβfeatures`. Scikit-learn's `C` is inversely related to regularisation strength (the exact scaling also depends on its loss convention). To address convergence warnings, scale features inside the training pipeline, allow more iterations when needed, and inspect separation (a boundary perfectly divides classes) or collinearity rather than suppressing the warning. Beyond accuracy, F1 is the harmonic mean `2·precision·recall/(precision+recall)`; a receiver operating characteristic (ROC) curve and a precision–recall curve compare thresholds, while threshold choice should be made on validation data.

## Guided coding task 1 — fit a leakage-safe classifier

Complete `fit_logistic_demo` in `week1/day5_logistic.py`. It must split with stratification, fit `StandardScaler` only inside a scikit-learn `Pipeline`, and return the fitted model plus the four split arrays. In this toy data, label `1` is the positive class.

**Starter code**

```python
from week1.day5_logistic import fit_logistic_demo

model, (X_train, X_test, y_train, y_test) = fit_logistic_demo()
print(f"train={len(y_train)} test={len(y_test)}")
print(f"positive_train={int(y_train.sum())} positive_test={int(y_test.sum())}")
print(f"pipeline_steps={[name for name, _ in model.steps]}")
```

**Expected output**

```text
train=8 test=4
positive_train=2 positive_test=1
pipeline_steps=['standardscaler', 'logisticregression']
```

## Guided coding task 2 — report probabilities and class metrics

Complete `evaluate_binary`. Use the positive-class probability column, make the threshold explicit, and fix confusion-matrix order to `[0, 1]`. This evaluates a preselected threshold; do not tune the threshold on the test set.

**Starter code**

```python
from week1.day5_logistic import fit_logistic_demo, evaluate_binary

model, (_, X_test, _, y_test) = fit_logistic_demo()
report = evaluate_binary(model, X_test, y_test, threshold=0.5)
print(f"probabilities_in_range={bool(((report['probabilities'] >= 0) & (report['probabilities'] <= 1)).all())}")
print(f"matrix_shape={report['confusion_matrix'].shape}")
print(f"matrix_total={int(report['confusion_matrix'].sum())}")
print(f"precision={report['precision']:.3f} recall={report['recall']:.3f}")
```

**Expected output**

```text
probabilities_in_range=True
matrix_shape=(2, 2)
matrix_total=4
precision=1.000 recall=1.000
```

These values are stable for the fixed data/split with the listed dependency range. If a compatible scikit-learn release produces a different final decimal, record it with `import sklearn; print(sklearn.__version__)` and confirm the confusion counts explain the difference.

## Predict the output — worksheet self-check

```python
probability = 0.63
threshold = 0.50
predicted_class = int(probability >= threshold)
print(predicted_class)
```

What does the code print?

- A. `1`
- B. `0.63`
- C. `0`
- D. `63`

**Correct answer:** A. The estimated probability is above the explicit `0.50` threshold, so the chosen class is 1. This is a decision, not certainty.

## Where Students Get Stuck

Name the positive class in your example. In a confusion matrix with rows = true class and columns = predicted class, point to false negatives. If the positive class is rare, explain why accuracy alone could hide a poor detector. Finally, explain why a logistic coefficient is a change in log-odds—not a fixed increase in probability.

## Submission checklist

- [ ] The Chapter 11 and Chapter 12 source objectives are present; advanced solver derivations are clearly marked as optional extensions.
- [ ] `StandardScaler` is inside the pipeline and is fit on training data only.
- [ ] `predict_proba` probabilities are not described as final class labels.
- [ ] The positive class and decision threshold are stated explicitly.
- [ ] The confusion matrix uses label order `[0, 1]`; precision and recall are both reported.
- [ ] Accuracy is not used alone, and the threshold is not selected on the test set.
- [ ] Commit `week1/day5_logistic.py` and this worksheet.
