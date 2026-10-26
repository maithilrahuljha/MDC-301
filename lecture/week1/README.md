# Week 1 content and dependencies

## Exact topic order

The Week 1 overview presents these four top-level topics, in this exact order and wording:

1. **ML lifecycle, supervised vs unsupervised learning** — Session 1.
2. **Tools and the scikit-learn ecosystem** — Session 2.
3. **Simple, multiple and polynomial regression** — Sessions 3 and 4 (simple OLS first; multiple and polynomial features next).
4. **Logistic regression as a classification method** — Session 5.

This keeps the existing five-session architecture while grouping Sessions 3 and 4 under one regression topic. Sessions 1, 2, and 4 remain outline pages with objectives and selected derivations; Sessions 3 and 5 are the complete worked lessons. Booklet Chapters 3–4 are excluded from Week 1.

## Source and teaching notes

- The course booklet remains the authority for scope, notation, and voice. The OLS derivation in Session 3 was checked against Chapter 8.3 (printed p. 26); the logistic likelihood and gradient step in Session 5 were checked against Chapter 12.1 (printed pp. 45–47). Géron is supplementary only.
- The supplied PDFs inform the plain-language explanations: *1-Understanding ML vs Conventional deteministic etc.pdf*, *2-Supervised and unsupervised- labelled unlabelled data.pdf*, *3- Training Testing cross validation.pdf*, *3-Handout 25 aug.pdf*, *4-Linear Regreesion-Introduction.pdf*, *5-Handsout 1 Aug PG AML.pdf*, *5-Linear Regression Training and polynomial Regression.pdf*, and *ML-reference.pdf*. The supplied linear-regression scratch notebook motivates the simple engine-size-to-price example; its data download is not required for the lesson. The logistic-regression notebook motivates the sigmoid, likelihood, and gradient explanation.
- A few slide PDFs yielded little or no selectable text during extraction. No verbatim claim is attributed to those pages; checked booklet derivations and the user-provided notebooks are used where exact wording matters.
- The supplied notebook examples are taught with evaluation safeguards: a training-set score is not a generalization estimate, probabilities must be converted to labels before label comparisons, and preprocessing/model fitting must not see held-out test data.
- Optional further reading links to the official scikit-learn source on [getting started and estimators](https://github.com/scikit-learn/scikit-learn/blob/main/doc/getting_started.rst), [linear models and logistic regression](https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/linear_model.rst), [preprocessing and polynomial features](https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/preprocessing.rst), [cross-validation](https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/cross_validation.rst), and [common pitfalls](https://github.com/scikit-learn/scikit-learn/blob/main/doc/common_pitfalls.rst). These official references were checked on 2026-10-24.
- No official course timetable, device inventory, or module-breakdown PDF was available, so the facilitator runbook labels five 90-minute sessions as a planning assumption and leaves logistics for the instructor to fill.

## Existing question links

The supplied Q1–Q20 checks are linked from the five session pages under the matching four-topic sequence: Q1–Q4 in Session 1, Q5–Q8 in Session 2, Q9, Q10, and Q15 in Session 3, Q11–Q14 in Session 4, and Q16–Q20 in Session 5. The lecture pages contain links only; question text and answer keys live in the two quiz JSON files.

`week1/livequiz/before_lab1_questions.json` contains Quiz 1 (Q1–Q8) and `week1/livequiz/between_lab1_and_lab2_questions.json` contains Quiz 2 (Q9–Q20). `quiz-links.json` checks IDs across both files, and `week1/livequiz/pages/app.js` opens the requested Q ID from the matching phase quiz. The same files feed the optional local Flask/Socket.IO server.

If the separate quiz workflow later supplies `quizzes/weekN/`, update that week’s `quiz-links.json` to its exact relative source and poll URL and run the ID-reference checker. If the path or any ID is missing, keep the visible “Quiz coming soon” fallback; never invent an ID.
