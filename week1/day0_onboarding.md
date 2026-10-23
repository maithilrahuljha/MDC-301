# Day 0 · GitHub and Classroom 50 onboarding

This is a ten-minute, low-stakes setup rehearsal—not an ML lesson. You need a GitHub account and a browser. A GitHub **repository** is the online folder that stores your files and their history; a **commit** is a saved checkpoint. Classroom 50 is the course assignment system used here because GitHub Classroom was decommissioned on 28 August 2026.

## Before class

1. Open the course link supplied by your instructor. Sign in to GitHub using your own account. Never share your password, recovery code, or sign-in token with anyone.
2. Accept the invitation to the course GitHub organization. If GitHub sent an organization invitation by email, accept it first. Return to the course link and choose **Accept assignment**.
3. Wait for the page to say that your repository is ready, then select **Open repository**. It should be private unless your instructor explicitly says otherwise.
4. Check that the repository name includes the course assignment and your GitHub username. If the page says “Not a member yet,” “Assignment not found,” or “Submissions are closed,” stop and show the instructor; do not make a second account.

## Make one harmless practice edit in the browser

1. In your new repository, open `README.md` and select the pencil icon (**Edit this file**).
2. Add one line at the end: `My Week 1 repository is ready.` Do not add a phone number, password, home address, or other private information.
3. Select **Commit changes…**. Use the suggested commit message, then confirm **Commit changes** to the default branch.
4. Return to the repository home page. You should see the new line and a recent commit. That is your first saved change.
5. If this is a graded assignment, open the Classroom 50 assignment page and select **My submission**. Depending on the instructor's submission setting, the push/commit may start grading automatically; a **Submit** command may be required for submit-only assignments. Follow the instructor's assignment-page instructions.

## Open and work with the course files

- Read the repository `README.md` first. Open `week1/day1_worksheet.md` in GitHub to see the worksheet structure.
- To edit several files in a browser, open **Code → github.dev** (or press `.` while viewing the repository). The editor saves to a branch only after you choose **Source Control → Commit** and then **Sync/Push**. If the assignment requires a terminal to run Python, use the course lab computer or ask the instructor for help; do not paste passwords into the terminal or a notebook.
- If you want to work locally, install Git and Python only from the official links supplied by your instructor. Ask for help before running a command you do not understand. The instructor's `instructions.txt` contains the tested copy-and-paste commands.

## If something goes wrong

- **No organization invite:** check GitHub notifications and email, then ask the instructor to check the roster.
- **Wrong GitHub account:** sign out, sign in to the intended account, and reopen the assignment link; do not accept twice under another identity.
- **A commit is missing or the editor is confusing:** stop editing and ask a TA. The instructor can use the repository history to help recover a previous commit.
- **No laptop, no phone battery, or no network:** ask for the paper worksheet and record your GitHub username (not password) for later submission. The live quiz is formative; do not lose learning time trying to repair a device.

## Student layout at a glance

```text
mdc301-week1-<github-username>/
├── README.md
├── .gitignore
├── requirements.txt
└── week1/
    ├── day0_onboarding.md
    ├── day1_worksheet.md ... day5_worksheet.md
    ├── day3_regression.py
    ├── day5_logistic.py
    └── mini_capstone/
        ├── README.md
        ├── starter.ipynb
        ├── DATASET.md
        └── data/seoul_weather_noon_365.csv
```

Classroom 50 adds its own `.classroom50.yaml` and autograding workflow to each accepted assignment when the instructor enables autograding. Do not create or edit those generated control files unless the instructor asks.
