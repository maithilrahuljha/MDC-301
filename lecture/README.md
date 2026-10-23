# Lecture site contract

`lecture/index.html` is the real lecture entry point. The root repository `index.html` is a workspace landing page that links to it. The lecture site is plain HTML/CSS/JavaScript; there is no server-side component or student-side build.

## Portability

Copying only this directory into a fresh repository preserves the eight-week map and all eight working week indexes. Week 1 pages use the shared assets here. Optional quiz links and exercise downloads point outside this directory and must degrade gracefully; missing quiz files show **Quiz coming soon**. MathJax and Pyodide are optional pinned CDNs; expected outputs and readable lesson content do not depend on them.

## Stable paths and contracts

- Do not rename released URLs `weekN/` or `weekN/sessionM.html`.
- Keep all content for a week under `lecture/weekN/`; keep reusable assets in `lecture/shared/`.
- Keep badge IDs in `WNN-SNN` form and their Markdown line format `- [x] WNN-SNN — Badge Name`. Browser state uses localStorage key `mdc301.lecture.badges.v1`; opened self-check IDs use `mdc301.selfcheck.opened.v1`. The student copies the badge line to `progress.md`.
- `weekN/quiz-links.json` stores only link metadata and confirmed question IDs. Quiz text, options, and answer keys remain in the separate quiz system.
- Keep relative links so a GitHub project site under `/<repo>/` works. Do not require a file outside `lecture/` to render the lecture pages.
- Never edit an earlier `lecture/weekM/` when adding Week N (M < N). Shared-contract changes require a regression run and a migration note.

## Local checks

From the repository root, run:

```sh
python3 scripts/check_lecture_site.py
python3 scripts/build_lecture_manifest.py
python -m http.server 8000
```

Expected: the checker prints `Lecture checks passed`; the manifest script prints the number of files recorded; the static server reports port 8000. Open `http://localhost:8000/` and follow the links. Stop the server with `Ctrl+C`.

The longer rationale, Week 2 release example, privacy/accessibility rules, rubric, scale plan, and slide delta are in `docs/lecture-series-design.md`. Student Pages deployment is in the root `instructions.txt`; the Day 0 student page is `week1/day0.html`.
