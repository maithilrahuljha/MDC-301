# Classroom 50 teacher-side pytest bundle

These eight acceptance tests are for the teacher-side Classroom 50 autograder bundle. They are intentionally separate from the student template, so students cannot edit the copy executed by the grader. Classroom 50 publishes its bundle for the runner through GitHub Pages; do not treat test code as confidential or use this low-stakes scaffold for a high-stakes exam. Never put private student data, credentials, or secret values in the bundle.

## Install into Classroom 50

1. In the private `classroom50` repository owned by the course GitHub organization, create the assignment through the Classroom 50 web app.
2. In the assignment's **Autograding tests** section, import `week1/classroom50-tests.json` from this repository (or copy its one test entry into the form). The file is a bare JSON array, the format accepted by `gh teacher assignment test set --tests`.
3. Set the assignment runtime to Python 3.12 if your organization exposes the runtime selector. The test setup installs the root `requirements.txt`; `pytest` runs the tests served in `$CLASSROOM50_BUNDLE_DIR` from the student's checkout.
4. Copy these two `test_*.py` files into the private `classroom50` repository under the assignment's teacher-only bundle path:

   `CLASSROOM/autograders/week1-implementation/`

   Replace `CLASSROOM` with the classroom slug if the organization uses a different path. The runner makes this directory available as `$CLASSROOM50_BUNDLE_DIR`; it is not copied into the student repository.
5. Wait for the Classroom 50 **Publish Pages** workflow to finish, accept a test assignment as a test student, and submit once. Verify the result contains eight test cases and a maximum of 16 points before inviting the full cohort.

The root `tests/` directory is for local instructor/student feedback. Do not use that copy as the scored test bundle because students could alter it in their own repository. Keep the bundle and the JSON test entry in sync whenever function names or scoring changes.

## Local check

From the repository root, with the root Python requirements installed:

```bash
python -m pytest -q tests/test_day3_regression.py tests/test_day5_logistic.py
```

The starter modules deliberately raise `NotImplementedError`, so the tests are expected to fail until the TODOs are completed. A completed implementation should pass all eight cases.
