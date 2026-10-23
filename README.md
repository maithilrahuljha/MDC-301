# MDC-301 · Module 1 · Week 1 teaching kit

A Week 1-only worksheet framework, public formative quiz, and single-lab mini-capstone for a 200-student cohort. Start with [`instructions.txt`](instructions.txt) to publish the no-login GitHub Pages quiz; then read [`docs/week1-framework.md`](docs/week1-framework.md) and the [file-by-file acceptance checklist](docs/week1-acceptance-checklist.md).

## Important before distribution

- **Source status:** the user-provided `ML-reference.pdf` (*Machine Learning: A Beginner-Friendly Guide with Code and Math*) is now the course-content reference for Chapters 1–12; the five worksheets include those source objectives and source-aligned derivations. Its Appendix E derivation-index chapter numbers appear one chapter too high after Chapter 7; follow the table of contents and chapter headings, and see the framework notes. The original PDF is not copied into this repository, so keep it available for final proofreading. The Module 1 breakdown PDF, confirmed full course title, and actual timetable were not supplied.
- **Géron code reference:** [`maithilrahuljha/handson-ml2`](https://github.com/maithilrahuljha/handson-ml2) is a secondary implementation reference only. Its README identifies it as the second-edition notebooks and points to newer third-edition material. Do not use its chapter numbering to replace the supplied course guide, and test old API calls against the installed scikit-learn version.
- **Placeholder facts:** the full course title, actual timetable, and due dates were not provided. The framework labels its sample schedule as an assumption; confirm all course-specific details before publication.
- **Platform change:** GitHub Classroom was decommissioned on 28 August 2026. The current setup documentation uses Classroom 50; the legacy `.github/classroom/autograding.json` file is kept only as an archival compatibility artifact. Classroom 50 uses `week1/classroom50-tests.json` and teacher-side tests in `week1/classroom50-autograder/`.
- **Topic-wise tests:** `week1/livequiz/topic_banks/` contains eight standalone 10-question quizzes; choose a `QUIZ_TOPIC` slug to run one. See its README for the source-chapter map, including why the supervised/unsupervised topic is Chapter 1 material, not source Chapter 3.
- **Public quiz and privacy:** `week1/livequiz/pages/` is the no-login GitHub Pages option; students need not join an organization or create a GitHub account. Supabase response collection is optional and insert-only. Read `instructions.txt` before enabling it. Never commit a Supabase service-role key, Flask `.env`, response database/export, or populated `nickname_map.csv`.
- **Scale and synchronization:** the static page follows instructor cues but does not synchronize progress or show live class totals. Rehearse on the real network; there is no 200-device capacity guarantee. Keep a paper/offline fallback.

## Start here

1. Read [`instructions.txt`](instructions.txt) for the simple GitHub Pages quiz and optional Supabase setup. Classroom 50 assignment setup remains documented separately in [`docs/week1-framework.md`](docs/week1-framework.md).
2. Review [`week1/day0_onboarding.md`](week1/day0_onboarding.md), then check the five worksheets in `week1/`.
3. Run `python week1/livequiz/scripts/check_question_bank.py`; expected: the 25-question daily bank plus eight topic banks with 10 questions each.
4. Install the root `requirements.txt` plus `week1/livequiz/requirements.txt`, then run `python -m pytest -q tests/test_livequiz.py tests/test_result_join.py tests/test_topic_banks.py tests/test_static_quiz.py`; expected: 17 passed.
5. Complete the Day 3/5 starter TODOs in a test copy before expecting their eight pytest checks to pass; untouched student TODOs are supposed to fail.
6. Use `week1/mini_capstone/README.md` for the one-lab project, UCI data credit, notebook, and rubric.
