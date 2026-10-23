# Week 1 mini-capstone · How do noon weather measures relate to bike demand?

**Audience:** one 120-minute lab after Day 5 (sample duration; confirm the actual timetable). **Dataset:** 365 noon observations, one row per date, from UCI's Seoul Bike Sharing Demand data.

**Plain-English terms:** an *observation* is one data row; a *feature* is an input column; a *target* is the quantity or class to predict. A *train/test split* sets aside some rows for final checking; a *held-out* row is not used to fit or choose the model. *Regression* predicts a numeric value; *classification* predicts a category. A *pipeline* fits data-preparation steps and a model together. Polynomial features add powers such as `x²`, allowing a linear model in its coefficients to trace a curve; logistic regression estimates class probabilities. RMSE is a typical prediction error in the target's units; R² compares the fitted model with a mean-only baseline. *Regularization* adds a penalty that discourages very large coefficients; Ridge uses the squared-coefficient (L2) penalty. A *confusion matrix* counts correct and incorrect class decisions; precision measures the share of predicted positives that are truly positive, and recall measures the share of real positives found. Here the *positive class* is an above-median-demand observation (`high_demand=1`), with the cutoff fixed from the training rows only. A chronological split keeps earlier dates for training and later dates untouched for testing.

**Aim:** compare a one-feature model, a multiple-feature model, a curved polynomial-feature model, a regularized model, and a binary classifier for high versus lower bike demand. Explain what each can and cannot claim. The logistic exercise is **not** the Week 4 rainfall classifier; rainfall is not a classification target in this Week 1 lab.

## Questions

1. How well can one temperature feature predict noon bike rentals with a straight line?
2. Does adding several non-rain weather measurements change held-out error?
3. Does a quadratic temperature basis capture a curve, and what happens when Ridge penalizes large coefficients?
4. How well can a logistic classifier distinguish above-median from lower bike demand using the other noon weather features?
5. For the high-demand classifier, what do false positives and false negatives mean? Why should its threshold and metrics match the use case?

## Requirements and run steps

The notebook and CSV are in this folder, so students need no data download. From the repository root:

```bash
python -m pip install -r week1/mini_capstone/requirements.txt
python -m jupyter notebook week1/mini_capstone/starter.ipynb
```

Expected first data/split output:

```text
rows=365 columns=14
train=292 test=73
high_demand_threshold=659.0
high_demand: train=146 test=54
```

The dataset and its credit are in [`DATASET.md`](DATASET.md). Keep `date` for ordering and inspection; do not use it as a numeric predictor in this first lesson. The first 80% of dates are training data, and the final 20% are the untouched test set. The **label cutoff** is the median bike count in the training rows only; apply it unchanged to both training and test labels. Do not use held-out rental counts to choose it. This target-label cutoff is separate from the logistic model's probability threshold, which is a decision setting.

## Lab schedule (120 minutes)

| Time | Student work | Instructor check |
|---:|---|---|
| 00–10 | Read the question, identify features/targets, inspect columns and missing values. | Regression target is `rented_bike_count`; classification target is derived from the training median only. |
| 10–25 | Create the chronological split and report rows/threshold/positive counts. | The test set is the last 73 dates and is not used in fitting or cutoff selection. |
| 25–55 | Fit simple, multiple, and degree-2 polynomial regressions; compare RMSE and R². | Predictions/metrics are computed on the same held-out rows. |
| 55–70 | Fit Ridge on scaled multiple predictors; explain why scaling is in the pipeline. | The scaler is fitted only on training data. |
| 70–100 | Fit logistic regression for above-median demand; view confusion matrix, precision, and recall. | The rental-count target and rain/snow columns are absent from classifier `X`. |
| 100–115 | Write a short interpretation and one limitation. | Students name false positives/negatives and explain why results are not causal or a future forecast. |
| 115–120 | Run all cells, save, commit notebook and a short README note. | Confirm reproducibility and attribution. |

## Repository layout

```text
mini_capstone/
├── DATASET.md
├── README.md
├── requirements.txt
├── starter.ipynb
└── data/
    └── seoul_weather_noon_365.csv
```

## Submission rubric (100 points)

| Criterion | Points | Full-credit evidence |
|---|---:|---|
| Question framing and data audit | 10 | Identifies both targets, 365 observations, feature roles, units, the training-median cutoff, and limitations. |
| Split and pipeline hygiene | 20 | Chronological 292/73 split is made before fitting; the test set is never used for scaling, training, model selection, or cutoff choice. |
| Linear model comparisons | 25 | Fits simple/multiple linear regression, degree-2 polynomial regression, and Ridge; reports held-out RMSE/R² with a short comparison. |
| Logistic classifier | 20 | Uses a pipeline, excludes target/leakage columns, reports predictions and a confusion matrix with class order `[0, 1]`. |
| Interpretation | 15 | Reports precision and recall, explains the false-positive/false-negative trade-off, and avoids claiming causation or forecasting. |
| Reproducibility and communication | 10 | Notebook runs top to bottom, includes the CC BY 4.0 citation, and is committed with a concise conclusion. |

**Later-topic boundary:** the Week 4 rainfall classifier is only a brief course preview; this lab does not build it. The Week 1 classifier uses bike demand as its class label and a contemporaneous noon-weather snapshot.
