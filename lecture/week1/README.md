# Week 1 content and dependencies

This folder contains the Week 1 lecture pages, Day 0 setup page, facilitator runbook, deliverables checklist, badge definitions, and question-ID link map. Session 1, 2, and 4 pages are intentionally outlines; Session 3 and 5 are the complete worked lessons. The fixed scope is ML introduction/lifecycle, supervised vs. unsupervised learning, Python/scikit-learn, simple/multiple/polynomial regression, and logistic regression for classification. Booklet Chapters 3–4 are excluded.

## Source verification

The selected derivations in Sessions 3 and 5 were checked against the supplied *Machine Learning: A Beginner-Friendly Guide* PDF: Chapter 8.3 (printed p. 26) and Chapter 12.1 (printed pp. 45–46); the logistic gradient update is from Chapter 12 (printed p. 47). The Week 1 worksheets supply the companion code and data values. Géron is supplementary only. No official course timetable, device inventory, or module breakdown PDF was available, so the facilitator runbook labels five 90-minute sessions as a planning assumption and leaves logistics for the instructor to fill.

## Existing quiz-bank path discrepancy

The expected `quizzes/week1/` directory is not present in this checkout. The current repository has `week1/livequiz/questions.json` (daily IDs) and eight topic files under `week1/livequiz/topic_banks/` (a different ID scheme). The linked IDs in `quiz-links.json` were checked against the current daily bank. No quiz file was copied, moved, re-keyed, or edited. `week1/livequiz/pages/app.js` received only query-string routing so existing daily-bank IDs can open their question in that app. It does not change any stem, option, key, or explanation.

If the separate quiz workflow later supplies `quizzes/weekN/`, update that week’s `quiz-links.json` to its exact relative source and poll URL and run the ID-reference checker. If the path or any ID is missing, keep the visible “Quiz coming soon” fallback; never invent an ID.
