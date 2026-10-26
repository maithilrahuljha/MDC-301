# Week 1 artifact acceptance checklist

Use this after edits and before sharing. Each row is a one-line pass condition for one tracked deliverable. The supplied guide's objectives/derivations have been incorporated; the instructor must still proofread adapted examples against `ML-reference.pdf` and confirm the missing Module 1 schedule/title.

| Artifact | One-line acceptance check |
|---|---|
| `README.md` | It links to the no-login public Pages quiz and setup/framework/checklist, and states privacy and synchronization limits. |
| `instructions.txt` | A nontechnical instructor can publish via GitHub Pages settings, optionally configure Supabase, test without student accounts, and follow the data-handling notes. |
| `index.html` | The root Pages URL redirects to the quiz in `week1/livequiz/pages/`. |
| `.gitignore` | Virtual environments, Python caches, `.env`, quiz databases/exports, and notebook outputs are not tracked. |
| `requirements.txt` | A clean Python 3.11+ virtual environment installs the shared data-science and pytest packages. |
| `docs/week1-framework.md` | The exact four-topic Week 1 order maps consistently to the existing five sessions; platform, runbook, capstone, scale plan, and notation notes match the files. |
| `docs/week1-acceptance-checklist.md` | Every tracked deliverable has an explicit one-line verification condition. |
| `.github/classroom/README.md` | It warns that GitHub Classroom is retired and points instructors to the current Classroom 50 setup. |
| `.github/classroom/autograding.json` | The surrounding README/framework explicitly labels it legacy-only and never presents it as the current Classroom 50 grader. |
| `week1/classroom50-tests.json` | It is a valid bare JSON array with one 16-point pytest entry that runs teacher-side tests through `$CLASSROOM50_BUNDLE_DIR`. |
| `week1/classroom50-autograder/README.md` | It explains how to place the eight tests in the Classroom 50 teacher bundle, away from editable student repositories. |
| `week1/classroom50-autograder/test_day3_regression.py` | Four independent Day 3 tests grade estimator, coefficient/prediction, residual/RMSE, and R² behavior. |
| `week1/classroom50-autograder/test_day5_logistic.py` | Four independent Day 5 tests grade the pipeline/split, probabilities, confusion matrix, and precision/recall. |
| `week1/day0_onboarding.md` | A GitHub beginner can accept the course invitation, create a safe browser commit, find help, and use the offline option without sharing credentials. |
| `week1/day1_worksheet.md` | It follows the required section order, includes Ch 1–2 objectives and a 200–300-word recap, and labels the instructor-created constant-baseline bridge. |
| `week1/day2_worksheet.md` | It follows the required section order, includes Ch 5–7 objectives, a 200–300-word recap, a bias–variance derivation, and two runnable code tasks with outputs. |
| `week1/day3_worksheet.md` | It uses Ch 8 objectives, OLS derivation and source five-row data, reproduces exact code outputs, and interprets a curved residual plot without causal claims. |
| `week1/day4_worksheet.md` | It follows the required section order, includes Ch 9–10 objectives/recap, normal-equation/polynomial/Ridge derivations, and two tasks with reproducible outputs. |
| `week1/day5_worksheet.md` | It aligns Ch 11–12 objectives/recap and sigmoid/logit/MLE derivation with two tasks stating probability, threshold, positive class, and metric outputs. |
| `week1/day3_regression.py` | The four named student TODO functions import cleanly and pass all four visible/teacher-side tests once implemented. |
| `week1/day5_logistic.py` | The two named student TODO functions use the required pipeline and evaluation contract and pass all four visible/teacher-side tests once implemented. |
| `tests/test_day3_regression.py` | The local visible regression tests pass against a completed student implementation and intentionally fail on untouched TODOs. |
| `tests/test_day5_logistic.py` | The local visible classifier tests pass against a completed student implementation and intentionally fail on untouched TODOs. |
| `tests/test_livequiz.py` | Test clients select Quiz 1 or Quiz 2, submit one answer, verify the host reveal, export formula-safe CSV, and check app-relative database paths without real student data. |
| `tests/test_result_join.py` | The join script normalizes handles, requires verified alias mappings, reports ambiguous aliases, and avoids guessing identities. |
| `tests/test_week1_quizzes.py` | The two phase files and checker report Quiz 1 Q1–Q8 and Quiz 2 Q9–Q20. |
| `tests/test_static_quiz.py` | The Pages redirect, two quiz files, quiz selector/DOM, blank Supabase config, and insert-only policy are checked. |
| `week1/livequiz/README.md` | The two Week 1 phases, static practice page, local Flask server, and LAN/privacy instructions are documented. |
| `week1/livequiz/pages/index.html` | Students select Quiz 1 or Quiz 2 in Lecture or repeatable Practice mode without student accounts. |
| `week1/livequiz/pages/app.js` | The page loads either phase JSON from the Pages root, supports Q-ID deep links, and keeps practice feedback local. |
| `week1/livequiz/pages/styles.css` | The quiz is responsive and keyboard-focusable without third-party font/CDN dependencies. |
| `week1/livequiz/pages/config.js` | Optional Supabase URL/key settings are blank by default and warn against service-role secrets. |
| `week1/livequiz/pages/supabase_setup.sql` | The response table uses bounded fields, enables RLS, and gives anonymous visitors insert access only. |
| `week1/livequiz/LICENSE` | The live-quiz scaffold source has a clear MIT license, while vendored client/data notices remain separate. |
| `week1/livequiz/app.py` | The same-origin Flask-SocketIO app validates the selected phase file, withholds keys until host reveal, persists answers, and requires non-placeholder secrets for launch. |
| `week1/livequiz/before_lab1_questions.json` | It contains the supplied Quiz 1, Q1–Q8, with slide, options, answer, and explanation fields. |
| `week1/livequiz/between_lab1_and_lab2_questions.json` | It contains the supplied Quiz 2, Q9–Q20, with slide, options, answer, and explanation fields. |
| `live_quiz.txt` | It gives the VS Code/PowerShell local server steps, quiz selection, host flow, trusted-LAN setup, and no-public-exposure warning. |
| `week1/livequiz/requirements.txt` | A clean Python environment installs the Flask/gevent server and Socket.IO client needed for the local live quiz. |
| `week1/livequiz/.env.example` | It documents QUIZ_ID=quiz1/quiz2, placeholders, and local server configuration only. |
| `week1/livequiz/.dockerignore` | Docker builds exclude local secrets, databases, exports, and Python caches. |
| `week1/livequiz/Dockerfile` | It creates a non-root Python container, includes both phase files and local assets, and listens on port 8000. |
| `week1/livequiz/compose.yaml` | It runs one quiz worker plus Caddy, retains SQLite in a named volume, and does not publish the database port. |
| `week1/livequiz/Caddyfile` | It clearly marks the example hostname and reverse-proxies HTTP/WebSocket traffic to the quiz service. |
| `week1/livequiz/templates/student.html` | The mobile join and answer page requests no password/phone, displays the selected quiz, and loads the local Socket.IO client. |
| `week1/livequiz/templates/host.html` | The host key gates controls/export and the page shows the selected quiz, session code, live totals, and response summary. |
| `week1/livequiz/static/student.js` | Students reconnect, join, submit one answer per question, see slide labels, and cannot see answer keys before reveal. |
| `week1/livequiz/static/host.js` | Host controls reveal/advance safely, show slide labels, and render responses as text rather than executable HTML. |
| `week1/livequiz/static/vendor/socket.io.min.js` | The checked-in client works without a third-party CDN and matches the documented Socket.IO version. |
| `week1/livequiz/static/vendor/SOCKET.IO-LICENSE.txt` | The vendored client’s MIT notice is retained. |
| `week1/livequiz/static/vendor/README.txt` | The bundled dependency, exact version, source, and update-smoke-test requirement are recorded. |
| `week1/livequiz/scripts/check_question_bank.py` | One command checks both quiz files, Q1–Q20 ordering, slide lists, A–D options, correct-option metadata, and explanations. |
| `week1/livequiz/scripts/load_test_socketio.py` | Synthetic clients use generated IDs, join and answer without real roster data, and report failures with a nonzero exit status. |
| `week1/livequiz/scripts/join_week1_results.py` | The CSV join matches normalized handles or instructor-verified aliases, flags unmatched/ambiguous identities, and labels results formative. |
| `week1/livequiz/nickname_map.example.csv` | It supplies only the required alias-map headers and contains no real student names. |
| `week1/mini_capstone/README.md` | The one-lab plan, repository layout, setup, expected data/split counts, and 100-point rubric are actionable. |
| `week1/mini_capstone/DATASET.md` | The UCI source, DOI, CC BY 4.0 credit, subset, positive count, and present-time/non-forecast limitation are stated. |
| `week1/mini_capstone/requirements.txt` | A clean environment can install Jupyter, pandas, scikit-learn, and plotting dependencies. |
| `week1/mini_capstone/starter.ipynb` | The valid notebook finds the CSV from either documented working directory and contains TODO stages for four regressors plus logistic classification. |
| `week1/mini_capstone/data/seoul_weather_noon_365.csv` | It contains exactly 365 noon records and carries the UCI attribution; rainfall remains data, not the Week 1 classifier target. |

## Final release gate

- [ ] Proofread all source objectives/notation and adapted examples against the instructor's `ML-reference.pdf`; resolve Appendix E's chapter-index offset and confirm course title/timetable before distribution.
- [ ] Confirm Classroom 50 organization access, due dates, and repository visibility with the instructor/organization owner.
- [ ] Run `python week1/livequiz/scripts/check_question_bank.py` and `python -m pytest -q tests/test_livequiz.py tests/test_result_join.py tests/test_week1_quizzes.py tests/test_static_quiz.py` from the repository root.
- [ ] Complete the Day 3/5 starter TODOs in a test copy and confirm all eight tests pass; confirm untouched starters fail as expected.
- [ ] Publish the Pages site; test its URL in a private browser without sign-in and on two real devices. If using Flask, rehearse on the actual network and treat the 200-client test as a target, not a capacity guarantee.
- [ ] Confirm privacy/retention for any Classroom 50 roster/grades, Supabase rows, quiz CSV, aliases, and SQLite data; prepare the paper/offline fallback.
