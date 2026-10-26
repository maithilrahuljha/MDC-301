# MDC-301 Module 1 · Lecture-site design and delivery contract

## 1. Teaching frame and Week 1 plan

**Narrative frame:** a service-monitoring team needs to make one better decision from data: plan staffing from demand and recognize a station risk before service degrades. Each meeting moves that decision one step through the model lifecycle. The story makes features, targets, model choice, residuals, class thresholds, and evaluation feel connected rather than like a list of algorithms. It does not introduce the later rainfall, Falcon 9, or careers units; those are only foreshadowed in the week map.

Without the recurring service-monitoring decision, students can experience lifecycle, regression, polynomial features, and logistic classification as unrelated formulas and APIs; there is no reason to ask when a prediction is useful or which error matters. The story supplies that through-line and a low-stakes peer explanation without pretending that all weeks share one dataset. The loop for each meeting is deliberately small and repeatable: (1) state a decision and a visible promise; (2) teach one concept or derivation in a short block; (3) use a Week 1 quick-check question by ID; (4) predict or repair a result; (5) compare reasoning with a partner; (6) record a badge and a one-line explanation. The two new phase-specific quizzes are linked from the session pages using their stable Q1–Q20 IDs; the lecture does not duplicate stems, options, or keys. Poll participation is a separate service/export, not a data collection feature of this lecture site.

| Top-level topic (exact order and wording) | Session page | Selected derivation / practice | Week 1 quick-check IDs |
|---|---|---|---|
| 1. ML lifecycle, supervised vs unsupervised learning | 1 | Empirical-risk objective; frame a service decision; separate labelled targets from discovered groups | Q1–Q4 |
| 2. Tools and the scikit-learn ecosystem | 2 | MSE; fit/transform/predict; training-only preprocessing and pipelines | Q5–Q8 |
| 3. Simple, multiple and polynomial regression | 3 (simple OLS) | OLS first-order conditions (full derivation), a one-feature fit, and squared-error interpretation | Q9, Q10, Q15 |
| 3. Simple, multiple and polynomial regression | 4 (multiple + polynomial) | Matrix normal equations; feature expansion; degree/overfitting check (outline) | Q11–Q14 |
| 4. Logistic regression as a classification method | 5 | Log-loss from Bernoulli maximum likelihood; one gradient step; threshold and evaluation | Q16–Q20 |

The top-level order has **four topics across the existing five session pages**; Sessions 3 and 4 are two parts of Topic 3, not separate topics. Their self-check links are grouped under that shared topic. The 20 supplied quick checks are linked by stable IDs, while question text and answer keys remain in the two Week 1 JSON files. Sessions 1, 2, and 4 are explicitly marked **outline** pages with objectives and selected derivations. Sessions 3 and 5 are the complete worked HTML lessons. Each session has one “Break it / fix it” challenge: data leakage (S1), the scikit-learn 2-D reshape rule (S2), the R² baseline interpretation (S3), unnecessary polynomial degree (S4), and a logistic convergence warning (S5). Session 5 also explains that probability scores must be thresholded to compare with class labels, that the supplied notebook’s training score is not a generalization estimate, and that thresholds are chosen without peeking at test labels. Week 1 uses only the requested scope and excludes booklet Chapters 3–4.

**Source and assumptions.** The user-provided *Machine Learning: A Beginner-Friendly Guide* PDF was extracted and checked for the OLS derivation (Chapter 8.3, printed p. 26) and log-loss/gradient derivation (Chapter 12, printed pp. 45–47); those equations and local notation are transcribed in the session pages. The supplied ML-vs-conventional, labelled-vs-unlabelled, train/test/cross-validation, linear-regression, and Day 3/Day 5 worksheets informed the plain-language explanations. The user-pasted linear and logistic regression notebooks supply the worked-example context; their data downloads are not required, and misleading training-only/exact-probability accuracy checks are corrected in the lesson. Some slide PDFs yielded little or no selectable text, so no verbatim claim is attributed to them. Géron is supplementary, not the scope authority. Optional official scikit-learn references on estimators, linear models, preprocessing, cross-validation, and common pitfalls are linked from the Week 1 pages and were checked on 2026-10-24. No official timetable, device inventory, or module-breakdown PDF was available in this checkout. The runbook assumes five 90-minute meetings for planning only; the instructor must fill in the actual schedule and device/network plan before class.

## 2. Static-site architecture decision

**Selected approach: plain semantic HTML + one shared CSS file + small vanilla JavaScript helpers, published from `main` / `/(root)` with GitHub Pages.** No package manager, generator, database, server, or student-side build is needed. The root `index.html` is a small workspace landing page with a prominent route to the real lecture entry point, `lecture/index.html`. The lecture folder can be copied alone into a fresh repository; its week navigation, shared assets, placeholders, and lesson content resolve inside `lecture/`. Optional quiz links and exercise downloads are feature-detected and fail closed with “Quiz coming soon” or a visible download note.

Why this option rather than the named alternatives:

- **MkDocs Material:** strong search/navigation, but Python build configuration, theme/plugins, and CI introduce a toolchain and more points of failure for beginners.
- **Reveal.js:** excellent for slide presentations, but less suitable as a sequence of accessible, readable lesson pages and downloadable student work.
- **Quarto/Marp:** useful authoring systems, but require a render/build workflow and generated outputs; that is unnecessary for this no-build static teaching surface.
- **Plain HTML:** direct editing in GitHub’s browser UI, stable relative paths, simple diffs, keyboard-visible controls, and one deployment path. The trade-off is fewer generator conveniences; the shared shell and checker scripts supply consistency.

MathJax and Pyodide are the only optional browser CDNs. If either is blocked, surrounding explanations and expected outputs remain available. The site does not autoplay, request an account, or send lesson-cell data to a server. The optional Week 1 static quiz application is a separate dependency.

### Annotated tree

```text
index.html                         Workspace landing; prominent link to lecture/index.html
.nojekyll                          Keep GitHub Pages from treating this as a Jekyll project
instructions.txt                   Student step-by-step public Pages deployment guide
lecture/
  index.html                       Actual 8-week lecture entry; every week link resolves
  README.md                        Static-site and maintenance contract
  manifest.json                    Generated SHA-256 list for integrity checks (manifest excludes itself)
  shared/
    css/site.css                   Responsive palette, focus states, cards, code and math blocks
    js/site.js                     Accessible reveal controls and local badge/progress helpers
    js/quiz-links.js               Resolve only IDs; show “Quiz coming soon” on any missing dependency
    js/pyodide-cell.js             Optional, on-click client-side Python runtime
  week1/
    index.html                     Exact four-topic order mapped to five session pages
    day0.html                      Student one-page setup guide
    session1.html                  Outline, objectives, selected derivation and Q1–Q4
    session2.html                  Outline, objectives, selected derivation and Q5–Q8
    session3.html                  Complete OLS lesson, checked derivation, Pyodide cell, fix-it, Q9/Q10/Q15
    session4.html                  Outline, objectives, normal equations and Q11–Q14
    session5.html                  Complete logistic lesson, MLE derivation, gradient step, cell, Q16–Q20
    facilitator-runbook.md         Five 90-minute schedules; Session 1 first ten minutes scripted
    README.md                      Week 1 scope, source notes, and quiz paths
    quiz-links.json                Link-only mapping; stores no quiz question content
    badges/badges.json             Five stable Week 1 badge definitions
  week2/index.html                 Styled “Coming in Week 2” placeholder
  ...
  week8/index.html                 Styled “Coming in Week 8” placeholder
exercises/
  week1/README.md                  Five downloadable plain-Python session starters and limitations
  week1/session1.py ... session5.py
  week2/ ... week8/                Empty starter folders until each week is released
notes/README.md                    Public-repository privacy reminder; otherwise starts empty
progress.md                        Student-editable badge lines and reflection slots
scripts/
  check_lecture_site.py             Local link, week, badge, and quiz-ID reference checks only
  build_lecture_manifest.py         Regenerate lecture/manifest.json after a lecture edit
  verify_deployments.py             Instructor CSV status/hash/placeholder/quiz-reference checker
  build_student_hub.py              Optional opt-in, local gallery generator
```

The Week 1 quiz sources are `week1/livequiz/before_lab1_questions.json` (Q1–Q8) and `week1/livequiz/between_lab1_and_lab2_questions.json` (Q9–Q20). The lecture link map verifies IDs across both files; each link opens one question in the static quiz app, while the full quiz files remain selectable there. The Pages app is not a real-time aggregate by itself. If a future week receives a quiz bank, update only that week’s link map and verify IDs without copying stems or keys into lecture pages.

## 3. Pyodide decision and graceful fallback

| Option | Strength | Cost / limitation | Role here |
|---|---|---|---|
| Pyodide (browser Python) | Actual Python syntax and scikit-learn estimator API; no local install or server | First run downloads a Python runtime plus scientific packages; may take minutes on slow Wi-Fi, use substantial memory, be blocked by policy, or fail on an older device | Optional run button on Sessions 3 and 5; always gated by a click |
| Precomputed output | Instant, deterministic, works with JavaScript blocked and without a Python runtime | Does not let a learner change data or execute code | Always visible next to each cell; the minimum viable path |
| JavaScript-only chart | Very small and interactive; good for geometric intuition | Not Python and cannot demonstrate `fit`/`predict` in scikit-learn | Not used as a substitute for the Python API; can be added later as a small visual only |

The hybrid is the safe choice: students can read the lesson and expected output without execution; those with a compatible browser can opt into real Python. A first run commonly needs **tens of megabytes** (roughly 10–20 MB compressed for the core runtime plus scientific dependencies that can add another 20–40 MB; browser cache, release version, and network change the result). Do not promise this works offline or on every managed device. The fallback is the printed expected output and downloadable `.py`; executing the `.py` requires Python and packages, so a student with neither a working browser runtime nor local Python needs a lab computer or instructor demonstration. That limitation is stated rather than hidden.

Pinned script URLs used by the complete lessons:

```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js" defer></script>
<script src="../shared/js/pyodide-cell.js" defer></script>
```

The shared runner uses `loadPyodide({indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"})` and loads `numpy`, `matplotlib`, and `scikit-learn` only after the learner presses **Run this Python cell**. The Session 3 cell fits `LinearRegression` to the supplied five-point data and plots observations plus the fitted line. It has expected values slope `1.99`, intercept `0.09`, prediction at 6 `12.03`. Session 5 uses `StandardScaler` inside a pipeline and logistic regression. It does not load pandas in these tiny cells; pandas is not needed for the examples. If a later week uses pandas, add that package only to the relevant cell to avoid increasing the first-load cost for everyone.

## 4. Badges, self-checks, and poll links

Week 1 has five badges, one per session: `W01-S01 Problem Framer`, `W01-S02 Workflow Guard`, `W01-S03 Line Fitter`, `W01-S04 Feature Shaper`, `W01-S05 Probability Auditor`. Stable ID format is `WNN-SNN`; each lecture week adds five definitions in `lecture/weekN/badges/badges.json`. Names can reflect that week’s content, but IDs and storage format do not change. The site records local completion in browser key `mdc301.lecture.badges.v1`; it then supplies a copyable Markdown line for `progress.md`. When poll links are available, it records only which existing IDs were opened in `mdc301.selfcheck.opened.v1` before enabling the badge; it never records answers. If links are missing or browser storage is blocked, use the instructor’s verbal/paper fallback and honest self-attestation. There is no server or answer telemetry. The script checks all five Week 1 lines in the student’s tracked file.

The Week 1 session pages link all 20 supplied Q IDs across the five sessions. `lecture/shared/js/quiz-links.js` fetches the configured phase JSON files and checks for exact `id` values; it does not inspect or validate quiz wording, choices, correct answers, difficulty, or quality. The poll page receives `question_id` and `quiz` query parameters. If a bank, ID, poll page, or network is unavailable, the link becomes keyboard-readable **Quiz coming soon**. A lecture-only copy therefore renders without quiz files. Later weeks can use their own confirmed quiz source and IDs without copying question text or keys into lecture pages.

## 5. Weekly maintenance contract

**One exact release mechanism:** the instructor updates the canonical template on its `main` branch; students manually fetch only the new week folder plus the navigation/manifest and that week’s offline starter folder. No student work outside those paths is overwritten; no earlier `lecture/weekM/` is edited for `M < N`. Once lesson content is ready, the update/QA overhead is designed to fit within an hour. There is no local generator build; GitHub Pages automatically republishes the static branch after a commit (that publish step is not avoidable on Pages).

### Authoring workflow (Week 2 example)

1. Agree the Week 2 scope and five meeting outcomes from the official course plan. Do not infer timetable/device details or pull future hooks into Week 1.
2. Replace the placeholder at `lecture/week2/index.html`; add `lecture/week2/session1.html` through `session5.html` and `lecture/week2/badges/badges.json`. Keep relative links to `../shared/` and local week links. Add `lecture/week2/quiz-links.json` only when a separate quiz source and confirmed IDs exist; otherwise label each quiz reference “Quiz coming soon.”
3. Add five offline starters to `exercises/week2/` and a short README. Do not put quiz content in these files.
4. Add a Week 2 card to `lecture/index.html`. Extend `progress.md` by replacing generic Week 2 badge names while preserving `W02-S01`–`W02-S05`.
5. Run `python3 scripts/check_lecture_site.py`, regenerate the manifest with `python3 scripts/build_lecture_manifest.py`, and inspect the diff. With a canonical local `main` branch, `git diff --exit-code main -- lecture/week1/` must exit `0`; do not edit any earlier `lecture/weekM/`.
6. Preview from the repository root with `python -m http.server 8000`; test Week 1, new Week 2, Week 3–8 placeholders, keyboard focus, code fallback, and quiz fallback. Then merge the release to the canonical template `main` branch.
7. Students add the course repo as a read-only remote once and fetch only the new content. Example for Week 2 (replace `<course-owner>` only if the instructor supplies a different canonical template):

```sh
git remote add course-template https://github.com/maithilrahuljha/MDC-301.git
git fetch course-template
git checkout -b add-week-2
git checkout course-template/main -- lecture/week2 lecture/index.html lecture/manifest.json exercises/week2
git add lecture/week2 lecture/index.html lecture/manifest.json exercises/week2
git commit -m "Add Week 2 lecture"
git push -u origin add-week-2
```

After review, merge that student branch into their own `main`. Pages publishes from `main` / `/(root)`. This command cannot overwrite `lecture/week1/`, `progress.md`, `notes/`, or other exercise folders. For later weeks, change only the `week2`/`Week 2` path strings to the new week number.

### Backward-compatibility contract

- Keep stable public URLs `lecture/weekN/` and `lecture/weekN/sessionM.html` after a week is released; do not rename or move a released week.
- Keep `lecture/shared/css/site.css` class names used by pages, the localStorage key, the `WNN-SNN` ID format, badge line grammar, `quiz-links.json` fields (`schema_version`, `week`, `sources`, `poll`, `ids`, `missing_label`), and the graceful missing-quiz state.
- Keep paths relative; do not introduce a root-absolute `/lecture/...` link that breaks a project Pages URL under `/MDC-301/`.
- A breaking shared CSS/JS or badge schema change needs a versioned migration note and a regression run over every released week.
- Check that `git diff --name-only main -- lecture/week1/ ... lecture/weekN-1/` is empty before release. Do not rewrite older week files to make the new week easier.
- Week 1 uses the two supplied phase files under `week1/livequiz/`; the lecture folder stores only confirmed Q IDs and source/poll link metadata. Future weeks may add their own question files without copying stems or answer keys into lecture pages.

## 6. Accessibility, privacy, and integrity

- Semantic headings, landmarks, skip link, real anchors, visible keyboard focus, generous tap targets, responsive reflow, strong text contrast, text-based equations, `alt` text for generated plots, and reduced-motion support are included. No video/audio/animation autoplays. Keyboard-test links, checkboxes, buttons, disclosures, and cells before release.
- MathJax is text-rendered and optional; the prose describes the equation. Pyodide does nothing until clicked. `prefers-reduced-motion` disables smooth scrolling. Quiz status and cell output use polite live regions.
- GitHub Free Pages requires the student repo to be public. Every committed file is world-readable. Do not commit credentials, tokens, personal data, student IDs, grades, private notes, or real class datasets. Use invented/toy data. Keep private notes outside the repository. The `.gitignore` excludes common secrets and local opt-in hub data.
- The lecture app has no server-side code and does not record responses. Browser localStorage contains badge completion only. A separately configured quiz tool may collect responses; the instructor must announce its privacy policy and use its own export/retention controls.
- Integrity is lightweight and transparent: lecture-folder hashes detect accidental edits, commit history shows weekly work, and an instructor can ask a short teach-back (“explain your coefficient/threshold and one limitation”). Do not rely on client-side code as an invigilator or secretly track students.

## 7. Deployment at 200 students and failure routes

One student repo per student isolates Pages builds. The usual documented GitHub Pages guidance is a published site limit of 1 GB, a soft bandwidth guideline around 100 GB/month, a soft limit around 10 deployments/builds per hour per repository, and a build timeout around 10 minutes; confirm the live GitHub Pages limits before term start because policies can change. The course site is far below the size limit. Two hundred separate repositories do not send 200 commits to one repository, but first-deploy queues, account verification, campus Wi-Fi, and CDN/network access can still cause delays. Ask students to create accounts and fork on Day 0; schedule first deploys in waves (for example, four groups of about 50) if the campus connection is constrained. Do not make everyone install packages or download Pyodide simultaneously.

| Failure | Low-cost response |
|---|---|
| No account / account verification or flagged | Do not share accounts. Use the read-only public course site and instructor-approved lab/offline submission route. |
| First Pages deploy is 404 | Check repo is public, branch `main`, folder `/(root)`, root `index.html` present; wait up to 10 minutes and reload. |
| Blank/broken page | Check file-name case and relative paths; open `lecture/index.html` directly. `.nojekyll` is tracked. |
| One week is a 404 | Verify `lecture/weekN/index.html`; restore the folder from the course template. |
| Poll link unavailable | It should say “Quiz coming soon.” Use the instructor’s separate poll tool or verbal check; do not create a replacement ID. |
| Pyodide/CDN blocked or slow | Skip Run, use printed output and derivation; download `.py` for later or use a lab machine. |
| Wi-Fi failure | Continue from downloaded lesson/source or instructor projection; do not claim `.py` executes without Python. |
| Lost or overwritten lecture week | Fetch only `lecture/weekN`, `lecture/index.html`, `lecture/manifest.json`, and `exercises/weekN` from `course-template/main`; review before commit. |
| Public repo contains private material | Remove it from Git history using the institution’s incident process; rotate any exposed credential immediately. Do not assume deleting a file makes a published secret safe. |

The optional instructor hub is a local static gallery generated from an opt-in CSV. It stores no attendance or grades. See `tools/build_student_hub.py` and its example CSV; keep the real CSV and generated HTML untracked.

## 8. Assessment and delivery checklist

### 100-point rubric (instructor can inspect a roster in batches)

| Criterion | Points | Evidence |
|---|---:|---|
| Published student Pages URL returns HTTP 200 and opens the course root | 15 | `verify_deployments.py` URL result |
| Eight-week navigation; Week 2–8 show the correct non-404 placeholders | 10 | URL checks and page text |
| Canonical lecture folder unchanged for the released version | 20 | GitHub tree blob hashes vs canonical `lecture/` |
| Five Week 1 exercise starters are present and the student’s run/notes are attributable | 20 | Repository paths plus brief instructor sampling; script does not execute untrusted code |
| Five bug-fix explanations and model limitation notes | 15 | Short rubric: identify failure (5), give valid fix (5), state evaluation/interpretation limit (5) |
| Formative poll participation | 10 | Export from the instructor’s separate polling tool; no response data is read by this site |
| Short Week 1 reflection in `progress.md` | 10 | One idea learned, one limitation, one next step; no personal data required |
| **Total** | **100** | |

The automated status script covers URLs, lecture hashes, all eight week indexes/placeholders, the five Week 1 badge lines, and question-ID references. It never grades or validates quiz content. Human grading is limited to the explanation/reflection and a small rotating sample; do not run student Python during the automated check.

### Release checklist

- [ ] Confirm Week 1 scope and official timetable/device details; fill instructor-only placeholders.
- [ ] Confirm all eight week index links return a page; Week 2–8 say “Coming in Week N.”
- [ ] Review the checked booklet derivations and the two complete session recaps.
- [ ] Confirm all 20 session-page question IDs resolve across the two Week 1 quiz files; preserve the supplied quiz text and keys.
- [ ] Test that a lecture-only copy renders and missing quiz files say “Quiz coming soon.”
- [ ] Keyboard-test, narrow-screen test, reduced-motion test, and inspect high contrast.
- [ ] Run local checker, regenerate manifest, test Pages preview, and compare the old-week diff.
- [ ] Confirm root index links to the lecture entry, Pages source is `main` / `/(root)`, and `.nojekyll` is tracked.
- [ ] Remove private data from any public copy; use only synthetic examples.
- [ ] Announce the repository/publicness warning, expected deploy delay, no-account route, and poll privacy policy.

## 9. Optional instructor hub

`tools/build_student_hub.py` reads only rows whose opt-in field is `yes` from a CSV with `github_username,repo_name,display_name,opt_in`. It emits an HTML gallery for projection; a display name is optional and may be a pseudonym. The sample file contains no students. Keep the real opt-in CSV and generated page local/untracked, do not publish a roster, and make opting in unnecessary for credit.

Copy `tools/student_hub_optin.example.csv` to the ignored local path `tools/student_hub_optin.csv`, add only students who opted in, then run:

```sh
python3 tools/build_student_hub.py --csv tools/student_hub_optin.csv --output instructor-hub/student-gallery.html
```

Expected output: `Wrote local opt-in gallery: instructor-hub/student-gallery.html (N sites)` followed by a warning not to commit or publish it. The real input and generated file are in `.gitignore`.

### Deployment-status CSV

Copy `tools/student_roster.example.csv` to the ignored local file `tools/student_roster.csv` and add only the public GitHub username and repository slug (plus optional `branch` or `pages_url`). For a large class, provide an instructor token only through the process environment or authenticate `gh`; never put it in the CSV or repository. Run:

```sh
python3 scripts/verify_deployments.py --roster tools/student_roster.csv --output tools/deployment-status.csv
```

Expected output is one line per student (`[1/N] username/repo: OK`, `REVIEW`, or `ERROR`) and a final `Wrote tools/deployment-status.csv (N rows)`. The CSV contains Pages HTTP status, all eight week URLs, placeholder text, full `lecture/` Git-blob hash match, badge-line presence/completion, and question-ID reference results. `REVIEW` means the public site and structure passed but a Week 1 badge is not checked yet or a quiz bank is absent (the expected fallback is “Quiz coming soon”). The script reads quiz JSON only to collect `id` strings; it does not inspect quiz content. At most 60 unauthenticated GitHub API requests per hour are generally available, so use `GITHUB_TOKEN` or `gh auth login` for a 200-student run and execute in batches if necessary.

## 10. Existing slide-deck delta

No Beamer source deck was present in this checkout, so no slide file is changed. For the described deck that currently covers Chapters 1, 2, 4, and 5:

- Remove Chapter 4 from Week 1; it is out of scope and may be reserved for the later career unit.
- Keep Chapter 1 and Chapter 2, then insert the tools/scikit-learn/API content from Chapters 5–6, regression framing from Chapter 7, simple OLS from Chapter 8, multiple regression from Chapter 9, polynomial regression from Chapter 10, and logistic regression/training from Chapters 11–12.
- Reorder as S1: 1–2; S2: 5–7 and estimator workflow; S3: 8; S4: 9–10; S5: 11–12. Do not bring Chapters 3–4 into Week 1.
- Add one slide per session for the decision story, one source-aligned derivation, one “Where students get stuck” repair, and one quick-check question ID. Preserve the exact four-topic Week 1 order across the five session pages (Sessions 3–4 share Topic 3) and use the booklet’s notation as the authority.
