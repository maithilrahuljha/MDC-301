# Week 1 topic-wise question banks

These eight standalone JSON files are the instructor's topic-wise quiz sources. Each file wraps a complete quiz object and contains exactly 10 questions. Scored questions use a **zero-based** `correct` option index; `word_cloud` questions omit both `options` and `correct`. Short explanations are included for instructors/review but are not shown to students before reveal.

| File / `QUIZ_TOPIC` slug | Topic | Course source chapter(s) | Day |
|---|---|---|---:|
| `ch01_intro_to_ml.json` | Introduction to Machine Learning | Ch 1 | 1 |
| `ch02_ml_lifecycle.json` | Machine Learning Model Lifecycle | Ch 2 | 1 |
| `topic03_supervised_vs_unsupervised.json` | Supervised vs Unsupervised Learning | Ch 1 | 1 |
| `ch05_tools_and_sklearn.json` | Tools and the Scikit-learn Ecosystem | Ch 5–6 | 2 |
| `ch08_simple_linear_regression.json` | Simple Linear Regression | Ch 8 | 3 |
| `ch09_multiple_linear_regression.json` | Multiple Linear Regression | Ch 9 | 4 |
| `ch10_polynomial_and_regularisation.json` | Polynomial and Regularised Regression | Ch 10 | 4 |
| `ch12_logistic_regression.json` | Logistic Regression | Ch 11–12 | 5 |

**Chapter-numbering note:** the third quiz is the third topic in this bank, not source Chapter 3. The supplied guide's Chapter 3 is a career topic excluded from Week 1; supervised and unsupervised learning are mapped to source Chapter 1.

## Run one topic in the included live app

1. From the repository root, see the exact slugs:

   ```bash
   python week1/livequiz/scripts/check_question_bank.py --list-topics
   ```

2. In `week1/livequiz/.env`, set `QUIZ_TOPIC` to one slug above, for example:

   ```text
   QUIZ_TOPIC=ch08_simple_linear_regression
   ```

3. Restart the server. It loads exactly that file's 10 questions; `QUIZ_DAY` is ignored while a topic is selected. Students and the host see the topic name and 10-question total. Change back to `QUIZ_TOPIC=all` to use the existing daily bank, where `QUIZ_DAY` selects 1–5 or `all`.

Validate every file and the daily bank with:

```bash
python week1/livequiz/scripts/check_question_bank.py
```

The JSON schema is a platform-neutral source format. The built-in app loads it directly. ClassQuiz, Mentimeter, and open.mentimeter may require a platform-specific template or converter; check the selected platform's current import format rather than assuming these JSON files are native imports.