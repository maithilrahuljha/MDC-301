# Week 1 · Day 1 worksheet — Overview and the ML lifecycle

## Learning objectives

**Chapter 1 — An Overview of Machine Learning (source objectives):**

- Say what machine learning is in a practical way, not just a catchy phrase.
- Tell the difference between supervised, unsupervised, and reinforcement learning.
- Explain why doing well on new data (not old data) is the real goal.
- Decide whether a problem is regression or classification.

**Chapter 2 — Machine Learning Model Lifecycle (source objectives):**

- Describe the six stages of the ML lifecycle.
- Explain why the lifecycle is a loop, not a line.
- Tell the difference between data drift and concept drift.
- Describe what CRISP-DM adds to the basic workflow.

**Vocabulary:** an *observation* is one data row; a *feature* is an input column; a *target* is the value a model is asked to predict; a *label* is a known target for an example. *Generalisation* means working well on new examples. *Drift* means that data or the relationship the model learned has changed over time.

## Concept recap

Machine learning is a way to choose a rule from a family of possible rules, measure how wrong its predictions are with a loss, and fit adjustable settings so the loss becomes smaller. A useful model must also work on new examples, not just memorise the examples used to fit it. With labelled input/output pairs, the task is supervised: predicting a number is regression, while predicting a category is classification. With no supplied target labels, an unsupervised method may find groups or other structure. Reinforcement learning instead learns from actions and rewards over time; it is only a brief comparison today.

A train/test split keeps some examples aside for a final check. If training performance is strong but test performance is much weaker, the model may have overfit. If both are weak, it may have underfit. The lifecycle makes this a practical loop: define the problem; collect and prepare data; train and choose a model; evaluate it; deploy it; then monitor and maintain it. Deployment is not the finish line. *Data drift* means the input-feature distribution changes; *concept drift* means the input-to-outcome relationship changes; *label drift* means the target rate changes. CRISP-DM (Cross-Industry Standard Process for Data Mining) contributes an iterative process that begins with understanding the problem and data and returns to earlier stages as evidence changes. In every stage, choose measures that match the real cost of mistakes.

## Read the math

Chapters 1–2 introduce a function, a loss, and fitted settings, but do not give a worked calculus example. This small **instructor bridge** makes that idea concrete; it is not a claimed quotation from the booklet.

Suppose a baseline predicts one constant `c` for every target `yᵢ`, and squared error is the loss:

`J(c) = Σᵢ (yᵢ − c)²`.

Differentiate and set the derivative to zero:

`dJ/dc = −2Σᵢ(yᵢ − c) = 0`.

Rearrange: `Σᵢ yᵢ = n c`, so the best constant is `c = ȳ`, the sample mean. The baseline is deliberately simple: a later model must beat it on held-out data, not merely fit the training rows. In the booklet's general language, the model family is the set of constant predictors, the loss is squared error, and the fitting method is this minimisation.

## Guided coding task 1 — identify features and target

**Starter code**

```python
import pandas as pd

observations = pd.DataFrame({
    "hours_studied": [1, 2, 4],
    "practice_quizzes": [0, 1, 3],
    "passed": [0, 0, 1],
})
# TODO: define X from the two feature columns and y from the target column.
X = None
y = None
print(X.shape)
print(y.tolist())
```

**Expected output**

```text
(3, 2)
[0, 0, 1]
```

## Guided coding task 2 — classify the learning problem

**Starter code**

```python
# TODO: fill in the task type for each example, then print task_types.
task_types = {
    "predict_tomorrow_temperature": None,
    "approve_or_decline_a_loan": None,
    "group_customers_without_labels": None,
    "robot_learns_from_rewards": None,
}
print(task_types)
```

**Expected output**

```text
{'predict_tomorrow_temperature': 'regression', 'approve_or_decline_a_loan': 'classification', 'group_customers_without_labels': 'unsupervised clustering', 'robot_learns_from_rewards': 'reinforcement learning'}
```

## Predict the output — live-quiz question `ch01_q02_supervised_unsupervised`

```python
labeled_examples = True
setting = "supervised" if labeled_examples else "unsupervised"
print(setting)
```

What does the final line print?

- A. `unsupervised`
- B. `supervised`
- C. `True`
- D. `None`

**Correct answer:** B. In this example, the target labels are supplied during learning, so the setting is supervised.

## Where Students Get Stuck

A model reports a `0.73` probability that a customer belongs to the “will leave” class. Is that regression or classification, and why? Now compare a model with 95% training accuracy and 62% test accuracy with one that scores 60% on both sets: which one overfits, which one underfits, and what evidence supports your answer?

## Submission checklist

- [ ] The Chapter 1 and Chapter 2 source objectives are present.
- [ ] `X` and `y` are separate and have the expected shapes.
- [ ] The task type is chosen from the target/signal, not from the software name.
- [ ] The lifecycle includes all six stages and a feedback loop from monitoring.
- [ ] The constant-baseline derivation is labelled as an instructor bridge.
- [ ] Commit the worksheet and your completed code to your assignment repository.
