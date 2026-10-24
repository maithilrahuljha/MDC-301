# MDC-301 · Module 1 · Week 1 worksheet and live-quiz framework

**Scope:** Week 1 only · **cohort assumption:** 200 students · **research checked:** 23 October 2026

## 1. Decisions, placeholders, and source limits

- **Official course title and timetable:** neither was supplied. This framework uses the course code **MDC-301** and a sample schedule of five 90-minute teaching blocks plus one 120-minute lab. These durations only make the runbook concrete; the instructor must confirm the actual title and schedule.
- **User-provided course source:** `ML-reference.pdf` was attached during this conversation. It is a 62-page guide titled *Machine Learning: A Beginner-Friendly Guide with Code and Math*; its Chapters 1–12 match the requested Week 1 map, and its table of contents confirms that Chapters 3–4 are the career chapters to exclude. The worksheets now include the source objectives and align their recaps/derivations to those chapters. The original PDF is not copied into this repository, so keep the instructor's source file available for final proofreading. **Source QA note:** Appendix E's derivation index appears to number most derivations one chapter too high after Ch 7 (for example, it points simple OLS to Ch 9 and logistic MLE to Ch 13); map by the table of contents and actual chapter headings, and correct the index in the source before its next release. The Module 1 breakdown PDF remains absent; the official full course title and timetable are still unknown.
- **Géron is a secondary implementation reference:** the user supplied [`maithilrahuljha/handson-ml2`](https://github.com/maithilrahuljha/handson-ml2). Its README identifies it as the second-edition notebook repository and says the third-edition notebooks are more up to date. Use it for coding patterns only; follow the supplied course guide for objectives, derivations, and notation. The README and relevant Ch 1, Ch 3, and Ch 4 notebook contents were spot-checked on 23 October 2026.

**Do not confuse the two books' chapter numbers.** In the supplied guide, Ch 3–4 are careers and are outside Week 1. Géron's Ch 3 is classification and Ch 4 is training linear models; those notebooks are useful only as supplementary code references. The corresponding Week 1 source map is:

| Week 1 session | Supplied guide | Printed pages | Géron 2nd-edition code reference (optional) |
|---|---|---:|---|
| Day 1 · ML overview/lifecycle | Ch 1–2 | 1–8 | [`01_the_machine_learning_landscape.ipynb`](https://github.com/maithilrahuljha/handson-ml2/blob/master/01_the_machine_learning_landscape.ipynb), [`02_end_to_end_machine_learning_project.ipynb`](https://github.com/maithilrahuljha/handson-ml2/blob/master/02_end_to_end_machine_learning_project.ipynb) |
| Day 2 · tools/API/regression intro | Ch 5–7 | 15–24 | Ch 1–2 implementation patterns; do not transfer their syllabus numbering |
| Day 3 · simple regression | Ch 8 | 25–29 | [`04_training_linear_models.ipynb`](https://github.com/maithilrahuljha/handson-ml2/blob/master/04_training_linear_models.ipynb) |
| Day 4 · multiple/polynomial/Ridge | Ch 9–10 | 30–40 | [`04_training_linear_models.ipynb`](https://github.com/maithilrahuljha/handson-ml2/blob/master/04_training_linear_models.ipynb) |
| Day 5 · logistic classification | Ch 11–12 | 41–51 | [`03_classification.ipynb`](https://github.com/maithilrahuljha/handson-ml2/blob/master/03_classification.ipynb) and Ch 4 |

The supplied guide's scikit-learn Ch 6 snippet uses `mean_squared_error(..., squared=False)`. That keyword is absent from the installed scikit-learn 1.9.1 API (`TypeError`); for current outputs use `np.sqrt(mean_squared_error(y_true, y_pred))`. Check APIs against the course environment and version ranges in `requirements.txt` rather than copying older notebook calls blindly.

- **Course boundary:** Week 1 covers ML introduction and lifecycle, supervised versus unsupervised learning, Python/scikit-learn tools, simple/multiple/polynomial regression, and logistic regression for classification. Do not teach booklet Chapters 3 or 4; Chapter 4 and careers belong in Module 4 Week 8. Only briefly foreshadow the Week 4 rainfall classifier and Module 3 Week 7 Falcon 9 capstone. Do not teach either future project in this kit.
- **GitHub Classroom is retired:** GitHub's [official changelog](https://github.blog/changelog/2026-08-27-github-classroom-deprecated/) says GitHub Classroom was decommissioned on 28 August 2026. Use [Classroom 50](https://github.com/foundation50/classroom50) for new assignments; do not describe `.github/classroom/autograding.json` as an active grader. Classroom 50 is free/open-source software but requires a GitHub organization on Team or Enterprise; verified educators may qualify for a free Team-tier organization through GitHub Education. If the institution must pay for an organization plan, the charge depends on its current GitHub contract; this kit does not assume or quote a price, so ask the organization owner before proceeding. Confirm current organization eligibility and institutional data policy before roster import. Current [web teacher](https://github.com/foundation50/classroom50/wiki/Web-Teacher-Guide), [web student](https://github.com/foundation50/classroom50/wiki/Web-Student-Guide), and [autograding](https://github.com/foundation50/classroom50/wiki/Autograding-Basics) guides were checked 23 October 2026.

## 2. Four-topic order and five-session teaching plan

The student-facing Week 1 overview uses these exact top-level headings in order: **ML lifecycle, supervised vs unsupervised learning** (Day 1); **Tools and the scikit-learn ecosystem** (Day 2); **Simple, multiple and polynomial regression** (Days 3–4); and **Logistic regression as a classification method** (Day 5). The existing five-session schedule below remains intact, with simple regression first and multiple/polynomial regression as the second part of Topic 3.

A 90-minute block is a planning assumption, not a supplied timetable. The 120-minute mini-capstone is a separate single-lab activity after Day 5. Terms are introduced plainly: a **feature** is an input column, a **target** is the value being predicted, a **residual** is observed minus predicted, and **held-out** data is data deliberately kept away from fitting.

| Session | Outcome and sequence | Reproducible derivation | Coding demonstration | Misconception to surface |
|---|---|---|---|---|
| **Day 1 · Ch 1–2: what ML is and its lifecycle** | Given a problem statement, identify labels/target when supplied, distinguish supervised/unsupervised/reinforcement learning, classify regression vs classification, and place work in the six-stage lifecycle loop. | Ch 1–2 are conceptual rather than a calculus derivation. The worksheet adds a clearly labelled bridge: minimise `J(c)=Σᵢ(yᵢ−c)²`; `dJ/dc=−2Σᵢ(yᵢ−c)=0`, hence `c=ȳ`. | Use a small pandas table to make `X` from two input columns and `y` from a target column; classify four task descriptions. | “Unsupervised” means there is no supplied target label for the task; it does not mean the algorithm has no objective or can never be evaluated. |
| **Day 2 · Ch 5–7: tools, estimator API, first workflow** | Describe the four tool-stack layers; use `fit`, `transform`, `predict`, and a pipeline; report regression metrics and preserve a test set. | Ch 7 bias–variance decomposition: add/subtract `E_D f̂_D(x)` from `y−f̂_D(x)`; after expectation the cross terms vanish, leaving `Bias² + Variance + σ²`. | Fit a scikit-learn estimator on training rows, scale inside a pipeline, predict on untouched rows, and print split sizes. | “The test set is harmless to use because its labels are hidden.” Even unlabeled test features can leak if used to fit preprocessing or choose a model. |
| **Day 3 · Ch 8: simple linear regression and residual diagnostics** | Write the model/assumptions, derive OLS coefficients, interpret slope/intercept, calculate residuals/RMSE/R², and read a residual plot; variance and `R²=r²` proofs are extensions. | Minimise `S(b₀,b₁)=Σᵢ(Yᵢ−b₀−b₁Xᵢ)²`; the two first-order conditions yield `β̂₁=Σ(Xᵢ−X̄)(Yᵢ−Ȳ)/Σ(Xᵢ−X̄)²` and `β̂₀=Ȳ−β̂₁X̄`. | Fit the source's five-row `LinearRegression` example, print the fitted line/prediction, compute residuals and metrics, and interpret a curved residual plot. | Residuals are `observed−predicted`, so negative means the model predicted too high. A curve/funnel is a reason to investigate, not proof of causation or a guarantee that a model is unusable. |
| **Day 4 · Ch 9–10: multiple and polynomial regression; regularization preview** | Write scalar/matrix models, build polynomial pipelines, and preview Ridge; full VIF/covariance/Lasso KKT/ElasticNet derivations are optional extensions. | With augmented design `X̃=[1|X]`, `S(β)=||y−X̃β||²`; `∇S=−2X̃ᵀy+2X̃ᵀX̃β`, giving `β̂=(X̃ᵀX̃)⁻¹X̃ᵀy`. Feature map `φ(x)=[1,x,…,xᵈ]` stays linear in `β`; Ridge adds `λ||β||²` to feature coefficients. | Split before fitting, fit two-feature `LinearRegression`, then fit `PolynomialFeatures` and `Ridge` in a pipeline; print coefficients and transformed features. | Polynomial regression is not “nonlinear in its coefficients.” A flexible curve or regularizer does not excuse using test rows to fit or select the model. |
| **Day 5 · Ch 11–12: logistic regression for classification** | Explain why OLS is unsuitable for binary labels, derive sigmoid/logit and log-loss from Bernoulli maximum likelihood, and interpret threshold/positive-class metrics; solver derivations are extensions. | `p=σ(xᵀβ)` maps scores to probabilities; `log(p/(1−p))=xᵀβ`. For Bernoulli labels, `𝓛=∏ᵢpᵢʸⁱ(1−pᵢ)^(1−yᵢ)`; minimising `−log 𝓛` gives binary log-loss. | Fit `StandardScaler` inside a pipeline with `LogisticRegression`; show `predict_proba`, an explicit threshold, confusion matrix `[0,1]`, precision and recall. | High accuracy can hide missed rare positives. Metric/threshold choice depends on error costs; `predict_proba` is not a class label. |

**Compression rule:** if contact time is shorter, reduce discussion or pair practice; do not remove the split-before-fit rule, residual-plot interpretation, or the rare-positive precision/recall comparison. The fully timed 90-minute Day 3 example is in §4.3.

## 3. Worksheets, student implementation, and Classroom 50

### 3.1 Required worksheet order and readiness

Every worksheet follows: **objectives → 200–300-word plain-English recap → Read the math → two guided code tasks (starter + expected output) → predict-output MCQ → “Where Students Get Stuck” reflection → submission checklist**.

- All five worksheets now include the source objectives for their assigned chapters and 200–300-word recaps. Day 1's constant-mean derivation is explicitly marked as an instructor bridge because Ch 1–2 provide concepts, not a worked calculus derivation. Day 2 uses the Ch 7 bias–variance derivation; Day 3 uses the exact Ch 8 toy rows and OLS formula; Day 4 aligns its matrix/polynomial/Ridge derivations to Ch 9–10; Day 5 derives sigmoid/logit and Bernoulli log-loss from Ch 11–12.
- Day 3/5 fixed teaching data are adapted to keep output deterministic and beginner-sized; the Day 5 fixture is synthetic, not the book's breast-cancer dataset. Advanced objectives (e.g. VIF/Lasso KKT/IRLS) remain explicitly labelled extensions rather than silently omitted. Confirm the instructor's available time and preserve the original source PDF for review.
- Day 0 onboarding is in `week1/day0_onboarding.md`; it uses browser-first steps so GitHub beginners can accept, edit, commit, and find help before a terminal is required.

### 3.2 Instructor source, student template, and generated student repository

The root of this repository is the **instructor source kit**, not a curated student template. In Classroom 50, make a separate template repository inside the course organization containing only student-facing work:

```text
mdc301-week1-template/             # instructor-owned GitHub Template repository
├── README.md                      # assignment brief, help, dates confirmed by instructor
├── .gitignore
├── requirements.txt
└── week1/
    ├── day0_onboarding.md
    ├── day1_worksheet.md ... day5_worksheet.md
    ├── day3_regression.py
    ├── day5_logistic.py
    └── mini_capstone/
        ├── README.md
        ├── requirements.txt
        ├── DATASET.md
        ├── starter.ipynb
        └── data/seoul_weather_noon_365.csv
```

Do **not** copy `.env`, quiz response data/exports, teacher-only autograder tests, or service credentials into that template. The visible root `tests/` folder is for local smoke feedback; it is not a secure grade source. Classroom 50 generates its own control files:

```text
mdc301-week1-<github-username>/    # private student repository, by default
├── README.md
├── .gitignore
├── requirements.txt
├── .classroom50.yaml              # generated; do not put in template
├── .github/workflows/autograde.yaml  # generated; do not put in template
└── week1/                         # files copied from the template
```

Teacher grading files live in the course organization's private `classroom50` repository, under the classroom/assignment autograder bundle, not in student checkouts:

```text
<classroom50-org-repo>/
└── <CLASSROOM>/
    └── autograders/week1-implementation/
        ├── test_day3_regression.py
        └── test_day5_logistic.py
```

The exact `<CLASSROOM>` directory is the Classroom 50 classroom slug; confirm it in the organization's repository. The assignment test config calls pytest on `$CLASSROOM50_BUNDLE_DIR`, so the executed tests remain outside the student's editable repository. Classroom 50 publishes its runner bundle through GitHub Pages; do not treat test code as confidential or put secrets/private student data in it. These low-stakes checks are not an exam security boundary. `week1/classroom50-autograder/README.md` describes this copy step. Before enrolment, test one assignment with a staff/student test account.

### 3.3 Current autograding config and lifecycle

`week1/classroom50-tests.json` is a **bare JSON array** for Classroom 50's **Autograding tests** import: one `python` pytest test, 16 points, eight cases, two points per passing case. The setup installs the student template's root `requirements.txt`; the run command invokes the teacher-side bundle. Classroom 50's `python` test type automatically installs pytest. Select Python 3.12 in the assignment runtime if available, and allow 300 seconds for dependency setup. The config file lives outside the `classroom50` repository; the web form copies it into assignment state.

`.github/classroom/autograding.json` is retained solely as an **archived GitHub Classroom compatibility example**. GitHub Classroom has been retired; Classroom 50 neither reads nor imports this legacy file. Do not ship it as an active workflow.

**Teacher lifecycle:** (1) verify a Team/Enterprise GitHub organization or approved GitHub Education benefit; (2) sign in at `classroom50.org` and perform one-time organization setup as owner, including its service token; (3) create classroom and roster from the institution-approved list; (4) create/mark the separate student template repository; (5) create a private individual assignment, import the test array, add teacher-side test files, set runtime/deadline; (6) wait for the publish workflow and test the assignment; (7) invite students and provide Day 0 onboarding; (8) collect scores from the submissions page, review code and failures, provide feedback; (9) export/archive and delete roster/grade data according to institutional policy. The instructor must confirm whether students should accept/submit through the browser or use optional command-line tools; browser acceptance is supported. Organization administration and data-protection approval are sysadmin/institution tasks.

Classroom 50 is free/open source but uses GitHub Pages, organization permissions, and GitHub Actions. Check the current plan, Actions quota/billing settings, and privacy policy before use. It is not the old GitHub Classroom service.

## 4. Live-quiz selection, deployment, and results

### 4.1 Public no-login GitHub Pages quiz

The simple open-classroom path is the static site at `week1/livequiz/pages/`. The root `index.html` redirects to it. In repository **Settings → Pages**, choose **Deploy from a branch**, select `main` and `/(root)`, and save. Students open the public Pages URL without a GitHub account or organization membership. Lecture mode is paced with instructor announcements; practice mode can be repeated. The static page does not synchronize students' screens or show class totals.

Supabase collection is optional. If configured, the browser sends lecture responses with a public anon/publishable key. `week1/livequiz/pages/supabase_setup.sql` enables RLS and anonymous insert only; it creates no public read policy. Practice answers are not uploaded. Tell students what data is collected and follow institutional retention rules. Public answer keys and anonymous inserts make this a formative quiz, not a secure assessment. Root `instructions.txt` gives the Settings steps and privacy guidance.

### 4.2 Open-source options compared

| Option | License and operating cost | Hosting/login and formats | 200-student evidence and fit |
|---|---|---|---|
| **This kit: GitHub Pages static quiz** | Static repository files; no separate server to operate. | Public browser URL, no student sign-in; optional Supabase response inserts. Instructor cues progress; no shared live control. | Not load-tested for this cohort. Simplest path for open access and repeatable practice; not a secure test. |
| **ClassQuiz** (`mawoka-myblock/ClassQuiz`) | MPL-2.0; self-host software is free, but server/admin time and any VPS are not. | Docker Compose with multiple services and configuration; browser participants; docs list MCQ, range, voting, text, order, check-choice; no built-in word-cloud question is listed in its documented types. | Project materials report tests up to 300 players. This is the strongest published scale claim among reviewed options, not an independent guarantee. More deployment work than this one-week kit needs. |
| **open.mentimeter** (`Rishi-ZAiFi/open.mentimeter`) | MIT; local self-host has no licence fee; hardware/IT still costs time. | Node/React/Socket.IO; README advertises MCQ, word cloud, Q&A, JSON upload, spreadsheet export, and local-first joining. | No independent 200-user benchmark found. Code inspection on the checked commit found the participant UI checks a `wordcloud` question type while the server payload path appeared to omit that field; test import/live behavior before relying on word clouds. The inspected app also handles participant names/phone-like fields, so review privacy before deployment. |
| **Livequiz** (`ineiti/livequiz`) | AGPL-3.0; free software, but self-host support/deployment has a cost. | Docker Compose/hosted option; Markdown practice activities. A Mentimeter-style live word cloud and straightforward class CSV workflow were not verified in its docs. | No verified 200-client test found; useful for exercises, but not the required word cloud + response-join workflow. |
| **This kit: Flask + Flask-SocketIO** | The live-quiz scaffold is MIT-licensed (`week1/livequiz/LICENSE`); Flask BSD-3-Clause, Flask-SocketIO MIT, gevent MIT; no licence fee. Local LAN has no server rental; optional VPS has recurring charge. | One Python process, same-origin browser UI, MCQ + one-word cloud, SQLite, host CSV download. No participant account, phone, or password; students may enter an optional GitHub handle. | A 200-device classroom is the **load-test target only**; this repository has not been independently capacity-certified. One gevent worker and SQLite WAL simplify an instructor-run first deployment. Run synthetic and real-device rehearsals; use a paper backup. |

**Recommendation:** use the static GitHub Pages quiz for open access and the simplest deployment; the instructor paces it verbally. Use the included Flask-SocketIO app when synchronized host-controlled progress and response aggregation are required. Either option is formative, not a high-stakes assessment service. Rehearse on the actual network, keep a paper fallback, and do not promise 200-device capacity based on a README claim or synthetic test alone.

Sources checked 23 October 2026: [ClassQuiz question types](https://classquiz.de/docs/quiz/question-types), [ClassQuiz self-hosting](https://classquiz.de/docs/self-host), [open.mentimeter repository](https://github.com/Rishi-ZAiFi/open.mentimeter), [Livequiz repository](https://github.com/ineiti/livequiz), and [Flask-SocketIO deployment guidance](https://flask-socketio.readthedocs.io/en/latest/deployment.html). Flask-SocketIO's multi-worker production guidance requires sticky sessions and a shared message queue such as Redis; this kit deliberately uses one worker.

### 4.3 Included daily bank and topic-wise tests

`week1/livequiz/questions.json` remains the daily source bank: 25 stable IDs, five questions per day, MCQ keys/explanations, and one one-word cloud each day. The eight standalone JSON files in `week1/livequiz/topic_banks/` each contain 10 questions and are the sources for independently selectable topic tests. Their interchange schema uses `multiple_choice`, `true_false`, and `word_cloud`; `correct` is a zero-based option index, while word-cloud items omit `options` and `correct`. `topic_bank.py` validates these objects and adapts answer indexes to the app's letter-key format without changing the source files. The bank README lists file slugs, chapter mappings, and selection steps.

Set `QUIZ_TOPIC=all` to use the daily bank; `QUIZ_DAY=1`…`5` selects one day's five-question set and `all` serves all 25. To run a topic test, set `QUIZ_TOPIC` to a slug printed by `check_question_bank.py --list-topics`; the app loads that file's 10 questions and ignores `QUIZ_DAY`. In particular, the supervised/unsupervised topic is mapped to supplied-guide Chapter 1. It is sequence item 3 in the topic bank, not source Chapter 3 (the guide's career chapter). Run `check_question_bank.py` to validate the daily and all topic banks. These files are generic JSON interchange sources; third-party quiz products may require their own native import template or conversion.

In the Flask/Socket.IO option, the instructor restarts the server when changing day or topic; saved responses persist, but current question position is process memory and returns to the first selected question after restart. The static Pages quiz requires no server restart.

For the separate Flask/Socket.IO option, the instructor-facing page shows host controls and students join by browser with a session code and display alias; its existing UI also offers an optional GitHub username. This is not required for the public Pages quiz. Do not ask for a GitHub password, phone, or sensitive personal information. Protect and delete the Flask CSV under institutional policy. The laptop recipe uses unencrypted HTTP and is only for a trusted network; use HTTPS for an untrusted/public network. The no-login Pages/Supabase steps are in root `instructions.txt`; Flask operations are documented in `week1/livequiz/README.md` and its deployment files.

### 4.4 Ninety-minute runbook: Day 3 simple regression

This sample is 90 minutes and can be re-timed; it alternates instruction, low-stakes quiz, and worksheet practice. Do not grade speed or attendance from quiz clicks.

| Minute | Instructor action | Layer/type | Why now |
|---:|---|---|---|
| 00–04 | State the learning objective; ask for a one-sentence prediction of a line fit. | Teach / orient | Makes the goal observable before formulas. |
| 04–15 | Explain `ŷ=b₀+b₁x`, slope/intercept, feature/target, and train/test boundary. | Teach | Establishes common language. |
| 15–19 | Ask `ch08_q01_slope_intercept`. | Live quiz / MCQ | Surfaces whether slope and intercept are swapped. |
| 19–31 | Worksheet Task 1: fit the five-row example; print coefficients/prediction. | Individual/pair practice | Moves from concept to estimator API. |
| 31–43 | Derive OLS normal equations on board and map symbols to code. | Teach / derivation | Connects the estimator to its objective. |
| 43–48 | Ask `ch08_q02_predict_output`. | Live quiz / predict output | Checks mental execution. |
| 48–62 | Worksheet Task 2: residuals, RMSE, R²; compare values with a partner. | Practice | Makes error direction/scale concrete. |
| 62–72 | Show residual-vs-fitted examples: random scatter vs curve/funnel; explain what they cannot prove. | Teach / diagnostic | Treats a plot as evidence to investigate, not a verdict or causal proof. |
| 72–77 | Ask `ch08_q03_residual_plot`. | Live quiz / diagnostic MCQ | Directly checks interpretation of a systematic curve. |
| 77–86 | Answer “Where Students Get Stuck”; annotate a residual and write a model-check sentence. | Reflection | Rewards interpretation over code copying. |
| 86–90 | Verbal exit: name a next model check; preview Day 4 in one sentence. | Teach / exit | Ends with transfer, not speed scoring. |

### 4.5 Quiz/GitHub grade join and nickname reconciliation

Host CSV export is `mdc301_week1_live_responses.csv`; Classroom 50's web score CSV uses `usernames`, `score`, and `max_score` (for this individual assignment), while `gh teacher download` writes `username`, score columns, and submission metadata. CLI downloads may contain several attempts per student, newest first; `week1/livequiz/scripts/join_week1_results.py` keeps the first (latest) row when attempt metadata is present. It detects the documented headers or accepts explicit column names. It normalizes handles case-insensitively and strips `@`; it never identifies a person from a display name by itself. If an alias was used, an instructor may create a separate `display_name,github_username` map only after verifying each identity against the approved roster. Duplicate/ambiguous aliases are reported as unmatched for manual review; there is no fuzzy matching. Example from repository root:

```bash
python week1/livequiz/scripts/join_week1_results.py \
  --quiz exports/quiz.csv \
  --grades exports/classroom50-grades.csv \
  --nickname-map exports/nickname_map.csv \
  --out exports/week1-joined.csv
```

Omit `--nickname-map` if no alias map is being used. If the CSV has unusual headers, use `--grade-handle-column`, `--grade-column`, optional `--grade-max-column`, or `--quiz-handle-column` with the exact header text. Output reports quiz-only, grade-only, matched, and unmatched identities. It includes an explicitly **formative** MCQ accuracy summary; do not add it to the course grade or penalize device/network failures.

## 5. One-lab mini-capstone

**Question:** “How do noon weather measures relate to bike demand?” The project is a 120-minute lab assumption after Day 5, using the included 365 noon-row Seoul Bike Sharing subset. Students compare simple linear, multiple linear, degree-2 polynomial, and Ridge regression for rental count, then fit logistic regression for **above-median demand**. Define the positive label using the median rental count in the chronological training rows only (`rented_bike_count > 659` for this fixed subset); apply that cutoff unchanged to test labels. The 292/73 time split is made before fitting. This is a contemporaneous pattern exercise, not a future-demand forecast.

The notebook is `week1/mini_capstone/starter.ipynb`; it supports launching from the repository root or mini-capstone folder. Its code cells are fill-in stages for a data audit, train/test split, four regression pipelines, and one scaled logistic classifier. The classifier excludes the rental-count target, `rainfall_mm`, and `snowfall_cm` from its features. It **does not teach or build the Week 4 rainfall classifier**. The data is adapted from [UCI Seoul Bike Sharing Demand](https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand), DOI `10.24432/C5F62R`, CC BY 4.0; exact attribution and scope limits are in `DATASET.md`.

Repository shape:

```text
week1/mini_capstone/
├── README.md                # questions, setup, run steps, schedule and rubric
├── requirements.txt         # notebook/model dependencies
├── DATASET.md               # UCI attribution, licence, subset and limitation
├── starter.ipynb            # runnable skeleton with model TODOs
└── data/seoul_weather_noon_365.csv
```

**Lab flow:** 0–10 minutes framing/data roles; 10–25 chronological split; 25–55 simple/multiple/polynomial comparisons; 55–70 scaled Ridge preview; 70–100 logistic classification and confusion matrix; 100–115 interpretation/limitations; 115–120 save/commit/check attribution. The 100-point rubric is in `week1/mini_capstone/README.md`: data audit (10), split/pipeline hygiene (20), regression comparisons (25), classifier (20), interpretation (15), reproducibility/communication (10).

## 6. Slide-deck delta (do not regenerate the deck)

1. **Remove from Week 1:** the supplied guide's Chapters 3 and 4 (ML-engineering career day; data-scientist/AI-engineer comparison). Chapter 4 careers belong in Module 4 Week 8. These numbers are **not** Géron's: Géron's Ch 3 classification and Ch 4 linear models are optional code references, not course chapter assignments.
2. **Keep and align:** supplied-guide Chapters 1–2 (ML, labels/features, lifecycle) and Chapter 5 (tools) with explicit supervised/unsupervised and held-out-test checks.
3. **Add/sequence mapped Week 1 content:** supplied-guide Ch 6 scikit-learn estimator API (`fit`, `predict`, `Pipeline`); Ch 7 regression target/loss; Ch 8 simple OLS/residual plot; Ch 9 multiple regression; Ch 10 polynomial basis/Ridge-Lasso preview; Ch 11 sigmoid/probability; Ch 12 log-loss/training/classification evaluation.
4. **No Chapter 13 in the supplied guide:** its table of contents proceeds from Ch 12 to appendices. Do not add a thirteenth chapter to Week 1 based on Géron's separate book.
5. **Slide order:** problem/prediction → supervised/unsupervised and features/target → lifecycle/split → tools → estimator API → regression target → OLS/residuals → multiple features → polynomial map/Ridge preview → sigmoid/probability → log-loss/threshold → confusion matrix/precision/recall → short Week 4/Week 7/Week 8 “later” preview. Use the supplied guide's β-based symbols; use Géron only as an implementation reference and bridge notation explicitly.

## 7. 200-student scaling, failure mitigation, and offline fallback

### Scale boundary

Plan for 200 long-lived browser connections, a join burst, and up to 200 short answer submissions per question. The server uses one gevent worker, same-origin Socket.IO, SQLite WAL, short payloads, and one-word free text. This is a proposed classroom configuration, **not a benchmark result or capacity promise**. Run the bundled `scripts/load_test_socketio.py --clients 200` against the actual network, then test phones/laptops and Wi-Fi access-point behavior. The optional VPS recipe uses a 2-GiB minimum and one worker; 2 vCPU is preferable if affordable, but compute is not the only bottleneck. Do not add workers without shared Socket.IO message queue plus sticky sessions. Do not expose the database port.

VPS example price checked 23 Oct 2026: DigitalOcean lists a 2-GiB, 1-vCPU Basic Droplet at US$12/month before tax/add-ons; verify current pricing and obtain procurement approval. A local laptop/LAN has no server-rental fee. Classroom 50's software is free, but its GitHub organization plan and Actions usage must be checked. No open-source product reviewed has an independent benchmark proving this kit will serve 200 students on this campus.

| Failure mode | Mitigation / fallback |
|---|---|
| Campus Wi-Fi client isolation or firewall blocks laptop host | Rehearse on the exact SSID; ask IT to allow student-to-host TCP 8000. If policy prevents it, use the approved VPS URL or paper; do not create one 200-person phone hotspot. |
| Socket reconnect storm or laptop/VPS overload | Ramp the test; start early; have paper MCQs ready; split the cohort if needed. Keep one worker. Treat server restart as a return to question one (saved responses remain in SQLite). |
| GitHub Actions queue/usage limits | Check organization quotas; avoid everyone pushing repeatedly; have students submit once per worksheet. If grading queues, collect commits and run the same pytest suite locally as a temporary instructor workflow. Do not make API calls per student. |
| Student cannot join GitHub organization or accept assignment | Verify roster/invitation, use the browser Day 0 guide, and ask the instructor/organization owner to correct membership; never share accounts or passwords. Paper worksheet is the in-class fallback. |
| Student has no device, low battery, or browser closes | Do not score speed/attendance; let them use another device or paper. Their browser ID may not transfer to a second device; reconcile only through their verified GitHub handle or a manually verified alias. |
| Dependency/setup or test timeout | Pre-install requirements on lab machines; run local tests and one Classroom 50 test submission. Allow 300 seconds for dependency installation; use the offline CSV and approved local wheel cache if WAN is unavailable. |
| Inappropriate/free-text cloud content | One word only; host sees the cloud first; do not project unreviewed responses. Stop submissions if needed; avoid collecting sensitive personal data. |
| No internet | If local Wi-Fi works, the quiz bank, vendored Socket.IO client, and dataset run without WAN. Otherwise use printed questions/worksheets and the included dataset copy. GitHub commits/score collection resume when service returns; follow the institution's approved offline submission route. |
| Roster/export/privacy concern | Use private student repositories and institutional storage; limit CSV access; never commit `.env`, SQLite, quiz export, or grade export. Agree a deletion date with the institution. |

## 8. Notation bridge — use the supplied guide's symbols first

The provided guide's Appendix C defines the symbols below. Its main-text Chapter 9 uses `X` for an augmented design matrix with a leading intercept column, while Appendix C describes `X` as the `(n,p)` feature matrix. To make dimensions explicit in teaching, use `X` for the feature-only matrix and write `X̃=[1|X]` for the augmented design when deriving an intercept; explain that the source sometimes reuses `X` for `X̃`.

| Concept | Supplied-guide notation | Géron 2nd-edition/common notation | Instructor bridge |
|---|---|---|---|
| Samples and features | `n` observations; `p` features | `m` is often used for examples | Translate `m ↔ n` once; use `n` in Week 1 worksheets. |
| Inputs and targets | `X` shape `(n,p)`; `xᵢ` is row/vector `i`; `y` shape `(n,)` | `X`, `y`; conventions vary by chapter | State rows are examples and columns are features; distinguish `X` from one row `xᵢ`. |
| Intercept/design matrix | Chapter 9 adds a leading column of ones; use `X̃` in class | Often called `X_b` or included in `θ₀` | A leading ones column changes the matrix width to `(n,p+1)`; do not silently mix dimensions. |
| Coefficients | `βⱼ` is a true/unknown coefficient; `β̂ⱼ` is its estimate | `θⱼ`, `θ₀`, `θ₁` are common | Keep the supplied guide's `β` in derivations; Python attributes may be `coef_`/`intercept_`. |
| Error, residual, prediction | `ε` true error; `ε̂ᵢ` residual; `ŷ` prediction | `y−ŷ` residual, `hθ(x)` prediction | For this course, residual is always `observed − predicted`; do not call it the true error `ε`. |
| Loss and logistic link | `L(·)` loss; `σ(·)` sigmoid | `J(θ)`/`σ(θᵀx)` common | Keep probability `p` distinct from thresholded class; likelihood and negative log-loss are different quantities. |
| Means and matrix operations | `X̄`, `Xᵀ`, `X⁻¹` | Same operations, intercept notation differs | `X⁻¹` exists only for square nonsingular matrices; prefer the exact normal-equation expression and state its rank condition. |
| Norms and derivatives | `||v||₂`, `||v||₁`, `∇`, `H`, `W` | Similar symbols | `H` is the Hessian; `W` is the logistic weight matrix in Ch 12. Define each before use. |
| Regularisation strength | `λ` | `λ` or library `alpha`/`C` | Map to the library objective explicitly: Ridge `alpha` follows its stated squared-error penalty; logistic `C` is inverse-strength under the guide's convention. |

Géron is a coding reference, not a notation authority for MDC-301. The bridge is not evidence of a discrepancy unless the instructor confirms it against the supplied guide and the exact Géron edition being used.

## 9. Acceptance gate

The file-by-file, one-line acceptance checklist is [`week1-acceptance-checklist.md`](week1-acceptance-checklist.md). The release gate is: proofread source-aligned objectives/notation and adapted examples against the instructor's PDF; confirm the missing course title/timetable; rehearse a Classroom 50 submission if used; validate the question bank/test suite; publish and test Pages without sign-in on real devices; rehearse any selected Flask server; approve privacy/retention; prepare the paper/offline fallback. See [`instructions.txt`](../instructions.txt) for concise Pages/Supabase setup and data-handling steps.
