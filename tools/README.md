# Instructor-only helper scripts

`build_student_hub.py` and `scripts/verify_deployments.py` are instructor-run utilities. They use only Python’s standard library and make no changes to student repositories.

- Start from `tools/student_roster.example.csv` or `tools/student_hub_optin.example.csv`; these contain headers only.
- Copy to the ignored local names `tools/student_roster.csv` and `tools/student_hub_optin.csv`. Keep real rosters/opt-in data out of Git.
- The deployment checker uses the GitHub tree API and public Pages/raw URLs. For a 200-person roster, use the instructor’s existing `gh` login or set `GITHUB_TOKEN` in the shell environment; do not paste it into a script, CSV, or repository.
- The gallery includes only rows with `opt_in=yes`; its output `instructor-hub/student-gallery.html` is ignored. Opening the HTML locally is enough to project it; no web server is required.
- The quiz check extracts exact `id` strings from the mapped JSON only. It never checks question text, options, answer keys, explanations, scoring, or quality.
