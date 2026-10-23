# MDC-301 Module 1 · Week 1 facilitator runbook

**Planning assumption:** five 90-minute meetings, one session per day. Confirm the official timetable, room, device policy, and network availability before teaching; none is specified in the supplied materials. The five time boxes below each total 90 minutes and can be compressed proportionally.

## Before students arrive

- Ask students to create accounts and fork the public course repository on Day 0; do not make 200 first-time account sign-ups the first in-class activity.
- Test `lecture/index.html`, `lecture/week1/`, Sessions 3 and 5, all Week 2–8 placeholders, and the existing Week 1 poll links.
- If the browser poll is unavailable, use the same question IDs in the instructor’s approved polling tool or run a verbal/hand-raise check. Do not invent replacements.
- Arrange table/pair groups and a low-bandwidth route: expected outputs are printed in the lesson; Pyodide is optional.
- Keep names, student IDs, grades, contact details, and credentials out of the projected gallery and public repository.

## Session 1 · Problem framing and the ML lifecycle

| Time | Instructor and student activity |
|---|---|
| 00–10 | **Fully scripted launch below.** Confirm site, set the service-monitoring story, identify features and target, and test the first existing poll link. |
| 10–18 | Teach the practical ML definition: function, adjustable parameters, loss, and performance on unseen data. Use one diagram, not a slide dump. |
| 18–22 | Run/launch `ch01_q01_target_feature` and `ch01_q02_supervised_unsupervised` (about 2 minutes each, grouped if needed). |
| 22–32 | Pairs label a toy table’s features, target, and decision. Ask them to say what happens if a prediction is wrong. |
| 32–39 | Teach supervised versus unsupervised examples; distinguish target labels from groups discovered without labels. |
| 39–43 | Existing check `ch02_q01_lifecycle_order`; ask one volunteer to justify the split-before-fit step. |
| 43–55 | Small groups order the lifecycle: frame → inspect → split → fit → evaluate → deploy → monitor. They mark where test leakage can occur. |
| 55–62 | Two opt-in groups share one lifecycle diagram. Correct the order without requiring students to publish personal details. |
| 62–70 | Teach generalization, training versus test data, and why “best training score” is not the goal. |
| 70–74 | Revisit the existing poll link or use a show-of-hands confidence check if bandwidth is poor. |
| 74–84 | Groups write a one-sentence problem statement with target, user decision, and a future evaluation plan. |
| 84–88 | Peer-check: is the target available at prediction time, and what would count as a useful prediction? |
| 88–90 | Invite the Problem Framer badge self-attestation; exit ticket: one risk of using test data during model selection. |

### S1 first ten minutes: exact facilitation script

- **00:00–02:00 — Set the frame.** Say: “Today we turn a service question into a prediction task. We will not create accounts or enter private information during the lecture. If your site is not ready, use the read-only course page and follow along.” Display the course URL and the “Public means world-readable” reminder.
- **02:00–04:00 — Verify navigation, not devices.** Open `lecture/index.html`, select Week 1, then point to the visible Week 2 placeholder. Ask students to open the same page or simply watch the projection. Do not require a camera, phone, QR scanner, or personal account to participate.
- **04:00–06:00 — Give a quiet first response.** Present the service-monitoring story: “A team wants to plan staffing for station demand.” Give 30 seconds of silent thinking, then ask pairs to name one possible input and the value they want to predict. Accept spoken, typed, or paper responses.
- **06:00–07:00 — Name the terms.** On the board, write `features X → model → target y` and label “decision” separately from the model. Ask one pair to point out which field would be the target.
- **07:00–10:00 — Low-risk check.** Launch existing ID `ch01_q01_target_feature` once from the lesson page. Explain that a broken/missing link becomes “Quiz coming soon”; use a hand signal or verbal response instead. Do not ask 200 students to troubleshoot sign-in or install Python in this window.

## Session 2 · Tools, scikit-learn, and data leakage

| Time | Instructor and student activity |
|---|---|
| 00–05 | Retrieve: students name one feature/target pair and one lifecycle step. |
| 05–13 | Teach the job of NumPy, pandas, Matplotlib, and scikit-learn; introduce `fit`, learned attributes, `transform`, and `predict`. |
| 13–17 | Existing check `ch05_q01_python_tools`; discuss the library choice. |
| 17–29 | Pairs trace an estimator snippet line-by-line and label input shapes. |
| 29–36 | Demonstrate `X` as a two-dimensional feature matrix and `y` as a one-dimensional target. |
| 36–40 | Existing check `ch06_q02_estimator_api`. |
| 40–52 | Break/fix: inspect a 1-D feature array and repair it with `reshape(-1, 1)`; discuss the API rule. |
| 52–60 | Show `train_test_split` before fitting; place a scaler and model in a pipeline. |
| 60–68 | Pairs mark which data each `fit` call sees; compare train-only transform with leakage. |
| 68–72 | Existing check `ch06_q03_transform_train_only`. |
| 72–84 | Students write/read a minimal pipeline on paper or in the downloaded starter; peers check shapes and split order. |
| 84–88 | Share two common errors and fixes. |
| 88–90 | Unlock Workflow Guard after the three linked checks; one-sentence exit: “A pipeline helps prevent ___.” |

## Session 3 · Simple linear regression and OLS

| Time | Instructor and student activity |
|---|---|
| 00–06 | Retrieve: mark feature, target, and train/test rows in the worked example. |
| 06–16 | Teach the line, slope/intercept interpretation, residual, and squared-error objective. |
| 16–21 | Launch existing IDs `ch08_q01_slope_intercept` and `ch08_q02_predict_output`; keep each poll short. |
| 21–33 | Board-derive the booklet’s OLS first-order conditions; pause for the mean-centering step. |
| 33–38 | Existing check `ch08_q03_residual_plot`; ask for a reason to inspect residuals. |
| 38–50 | Run or project the Session 3 Pyodide cell. If slow, use the always-visible expected output. |
| 50–58 | Break/fix the R² interpretation: zero can mean “no better than the mean baseline,” not “code failed.” |
| 58–68 | Inspect the residual-versus-fitted diagnostic: curvature, funnel, clusters, and outliers. |
| 68–73 | Short stretch / device break; leave the expected plot on screen. |
| 73–83 | Pairs predict at a new input, then state whether it is interpolation or extrapolation. |
| 83–88 | Volunteers explain one coefficient and one limitation. |
| 88–90 | Badge self-attestation; exit ticket: one pattern that would make a straight line inadequate. |

## Session 4 · Multiple and polynomial regression

| Time | Instructor and student activity |
|---|---|
| 00–05 | Retrieve the single-feature design matrix and add a second column. |
| 05–15 | Teach multiple regression, coefficient interpretation “holding included features fixed,” and the augmented intercept column. |
| 15–19 | Existing check `ch09_q01_multiple_features`. |
| 19–32 | Derive the matrix normal equations from squared residuals; use a small shape-check before multiplying matrices. |
| 32–37 | Students check the dimensions of \(X^TX\), \(X^Ty\), and \(\hat\beta\). |
| 37–47 | Teach polynomial basis features \((x,x^2,\dots)\) and why the model remains linear in its coefficients. |
| 47–51 | Existing check `ch10_q02_polynomial_basis`. |
| 51–62 | Break/fix: unnecessarily high polynomial degree and train-score-only reasoning. Repair with validation/cross-validation, regularization where appropriate, and one final test report. |
| 62–72 | Discuss high-degree variance, regularization, and why a stable solver is preferable to explicitly inverting a matrix. |
| 72–77 | Existing check `ch10_q04_ridge`. |
| 77–86 | Pairs sketch a degree-1 and a degree-3 fit; annotate which set is allowed to choose degree. |
| 86–90 | Feature Shaper badge; exit ticket: “linear in which quantities?” |

## Session 5 · Logistic regression and classification

| Time | Instructor and student activity |
|---|---|
| 00–05 | Retrieve: numeric target or class label? Give a service-monitoring classification example. |
| 05–15 | Teach linear score, sigmoid probability, decision threshold, and log-odds. |
| 15–19 | Existing check `ch11_q01_sigmoid_range`. |
| 19–29 | Derive binary log-loss from the Bernoulli likelihood using the booklet’s notation. |
| 29–34 | Work one gradient-descent step from the page; check the direction of the slope update. |
| 34–39 | Existing check `ch11_q02_probability_label`. |
| 39–51 | Run/project the scaled Pyodide logistic cell. Do not wait for every device; expected checks are printed. |
| 51–61 | Break/fix: diagnose the convergence warning and scale in a training-only pipeline; reinforce that thresholds are chosen on validation data, not the test set. |
| 61–70 | Compare accuracy with the confusion matrix, precision, recall, F1, and ROC/PR-AUC. |
| 70–75 | Existing check `ch12_q03_precision_recall_imbalanced`. |
| 75–84 | Groups identify which mistake is more costly in the example and justify a metric/threshold trade-off. |
| 84–88 | Opt-in peer share: one probability interpretation and one limitation. |
| 88–90 | Probability Auditor badge; five-session exit ticket: one Week 1 idea that now connects to the lifecycle. |

## Facilitation at 200 learners

- Use pairs or table groups; accept paper, speech, or digital responses. No activity depends on every student opening the same external page at once.
- For a live response tool, use the instructor’s approved service and announce a session label. The existing static quiz page can launch a question by ID; it does not itself display a real-time aggregate unless an instructor has separately configured the existing response service.
- Ask for volunteers before projecting student work. The hub is opt-in and displays only a chosen public URL or pseudonym.
- If a student has no account or is blocked by account verification, use the read-only course site and the approved offline/lab route. Do not share accounts.
