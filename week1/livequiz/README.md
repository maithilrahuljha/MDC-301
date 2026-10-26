# MDC-301 Week 1 quick checks

The Week 1 quiz bank now consists of exactly two phase-specific quizzes:

| Quiz | Source file | Questions | Lecture slides |
|---|---|---:|---|
| Quiz 1 — Before Lab 1, Hour 1 | [`before_lab1_questions.json`](before_lab1_questions.json) | Q1–Q8 (8) | 5, 6, 9, 10, 11, 12, 16, 17 |
| Quiz 2 — Between Lab 1 and Lab 2, Hour 2 | [`between_lab1_and_lab2_questions.json`](between_lab1_and_lab2_questions.json) | Q9–Q20 (12) | 21, 23, 25, 26, 28, 29, 30, 33, 34, 35, 36, 37 |

For each question, use the stated classroom sequence: **poll first, reveal the answer second, and ask a student to justify third.** Question IDs and the question/answer text are retained in the source JSON files.

## Pick the right quiz

The optional Flask/Socket.IO server reads one quiz per run. In `week1/livequiz/.env`, set:

```dotenv
QUIZ_ID=quiz1
```

Use `quiz1` for Q1–Q8 or `quiz2` for Q9–Q20. Stop the server, change `QUIZ_ID`, and restart it to switch quizzes. Use a fresh `SESSION_CODE` for each class/quiz if you want the CSV exports grouped separately. Existing SQLite responses are not erased when the quiz changes.

## Launch during class with VS Code

Follow the root [`live_quiz.txt`](../../live_quiz.txt) for a Windows PowerShell walkthrough: open the repository in VS Code, install requirements in a virtual environment, configure private host secrets, select `QUIZ_ID`, start the local server, and open the instructor/student pages.

The Flask/Socket.IO server is intended for a trusted class LAN. Students on the same Wi-Fi use the instructor laptop's private LAN address; they cannot use the instructor's `127.0.0.1` address from their own devices. **Do not tunnel, port-forward, or expose this local class server to the public Internet.** Keep `week1/livequiz/.env`, the host key, the response database, and CSV exports private and out of Git.

## Static practice page

[`pages/`](pages/) is the no-login static version served by GitHub Pages or a simple local HTTP server. It offers Lecture and Practice modes for both quizzes. Practice feedback stays in the browser. Its JSON files necessarily include the answer keys, so treat this static option as formative practice—not a secure exam. The static page does not synchronize devices or show live class results. Optional Supabase collection is off by default; never put a service-role key in browser code.

## Live server behavior

The local server provides a student join page at `/`, host controls at `/host`, and a health check at `/healthz`. The host advances and reveals questions; student screens update together while connected. Answers are saved in a local SQLite database and can be exported as CSV from the authenticated host page. Use aliases only if your class process requires them; never ask for passwords, phone numbers, or sensitive personal data. Follow institutional retention rules for exported responses.

Run the schema/ID check from the repository root:

```bash
python week1/livequiz/scripts/check_question_bank.py
```

It checks that Quiz 1 contains Q1–Q8, Quiz 2 contains Q9–Q20, and the slide, option, answer, and explanation fields are present. This check does not assess question quality or factual correctness.

The app has no independently certified 200-device capacity guarantee. Rehearse on the actual Wi-Fi and devices, confirm the campus firewall/client-isolation settings, and prepare an offline fallback. The included Docker/Caddy files are deployment examples, not part of the local VS Code classroom procedure.
