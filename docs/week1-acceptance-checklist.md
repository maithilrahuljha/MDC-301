# Week 1 artifact acceptance checklist

Use this after edits and before sharing. Each row is a one-line pass condition for one tracked deliverable. The supplied guide's objectives/derivations have been incorporated; the instructor must still proofread adapted examples against `ML-reference.pdf` and confirm the missing Module 1 schedule/title.

| Artifact | One-line acceptance check |
|---|---|
| `README.md` | It names the kit, links to setup/framework/checklist, identifies the supplied guide/Géron reference correctly, and states the remaining source/platform limits. |
| `instructions.txt` | A nontechnical instructor can follow it in order, paste the platform-specific commands, see expected outputs, and identify sysadmin-only steps. |
| `.gitignore` | Virtual environments, Python caches, `.env`, quiz databases/exports, and notebook outputs are not tracked. |
| `requirements.txt` | A clean Python 3.11+ virtual environment installs the shared data-science and pytest packages. |
| `docs/week1-framework.md` | The five sessions, platform decision, runbook, capstone, slide delta, scale plan, and notation bridge are internally consistent with the files. |
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
| `tests/test_livequiz.py` | Test clients can join, submit only one saved answer, reveal, view a one-word cloud, export a formula-safe CSV, and verify app-relative database paths without real student data. |
| `tests/test_result_join.py` | The join script normalizes handles, requires verified alias mappings, reports ambiguous aliases, and avoids guessing identities. |
| `week1/livequiz/README.md` | Local, VPS, import, privacy, day-filter, synthetic-load, and license notes match the implemented server. |
| `week1/livequiz/LICENSE` | The live-quiz scaffold source has a clear MIT license, while vendored client/data notices remain separate. |
| `week1/livequiz/app.py` | The same-origin Flask-SocketIO app validates the question bank, protects host controls, persists answers, and starts only with non-placeholder secrets. |
| `week1/livequiz/questions.json` | JSON validation reports 25 unique questions, exactly five per day, with a Day 3 residual-plot item and one word-cloud prompt each day. |
| `week1/livequiz/requirements.txt` | A clean environment installs the Flask/gevent server and asyncio client needed for the synthetic load test. |
| `week1/livequiz/.env.example` | It documents configuration keys and contains placeholders only, never reusable credentials. |
| `week1/livequiz/.dockerignore` | Docker builds exclude local secrets, databases, exports, and Python caches. |
| `week1/livequiz/Dockerfile` | It creates a non-root Python container, includes local static assets, and listens on port 8000. |
| `week1/livequiz/compose.yaml` | It runs one quiz worker plus Caddy, retains SQLite in a named volume, and does not publish the database port. |
| `week1/livequiz/Caddyfile` | It clearly marks the example hostname and reverse-proxies HTTP/WebSocket traffic to the quiz service. |
| `week1/livequiz/templates/student.html` | The mobile join and answer page requests no password/phone and loads the locally vendored Socket.IO client. |
| `week1/livequiz/templates/host.html` | The host key gates controls/export and the page shows the session code, live totals, and reviewable word cloud. |
| `week1/livequiz/static/student.js` | Students can reconnect, join, submit one answer per question, and cannot see the answer key before reveal. |
| `week1/livequiz/static/host.js` | Host controls reveal/advance safely and render user responses as text rather than executable HTML. |
| `week1/livequiz/static/vendor/socket.io.min.js` | The checked-in client works without a third-party CDN and matches the documented Socket.IO version. |
| `week1/livequiz/static/vendor/SOCKET.IO-LICENSE.txt` | The vendored client’s MIT notice is retained. |
| `week1/livequiz/static/vendor/README.txt` | The bundled dependency, exact version, source, and update-smoke-test requirement are recorded. |
| `week1/livequiz/scripts/check_question_bank.py` | One command prints the expected five-day/25-question summary and exits nonzero for a wrong day count. |
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
- [ ] Run `python week1/livequiz/scripts/check_question_bank.py` and `python -m pytest -q tests/test_livequiz.py tests/test_result_join.py` from the repository root.
- [ ] Complete the Day 3/5 starter TODOs in a test copy and confirm all eight tests pass; confirm untouched starters fail as expected.
- [ ] Test one Classroom 50 acceptance/submission and the server on two real devices; conduct a synthetic 200-client rehearsal on the actual network before class.
- [ ] Confirm privacy/retention for roster, quiz CSV, grade CSV, aliases, and SQLite data; prepare the paper/offline fallback.
