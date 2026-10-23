# MDC-301 Week 1 live check

The live-quiz scaffold source in this directory is MIT-licensed; see [`LICENSE`](LICENSE). The locally vendored Socket.IO browser client and the capstone dataset retain their separate notices/licenses.

This folder contains two ways to use the Week 1 quizzes:

* **Simple public path:** the static site in [`pages/`](pages/) is served through GitHub Pages. Students need no account, organization membership, server, or installation. Lecture mode follows instructor announcements but does not synchronize devices or show live totals. Practice is repeatable and never uploads answers. Supabase collection is optional and insert-only; see root [`instructions.txt`](../../instructions.txt).
* **Optional instructor-operated server:** the Flask/Socket.IO app described below offers synchronized host-controlled progress and a local SQLite response export. It needs Python or a server, security configuration, and rehearsal; it is not required for the public Pages quiz.

The server supports the existing 25-question daily bank and eight standalone 10-question topic banks. Neither option is an exam or attendance system; the 200-device cohort has not been independently capacity-certified.

**Terms for the server option:** a *LAN* (local-area network) is the private Wi-Fi shared by instructor and student devices; a `.env` file holds private settings/secrets; *HTTPS* is the encrypted public web connection; *DNS* maps a hostname to a server address; a *VPS* is a rented virtual server.

## Optional Flask server: private setup

Python 3.11+ is recommended for local use. From the repository root:

```bash
python -m venv .venv
python -m pip install --disable-pip-version-check -r week1/livequiz/requirements.txt
```

Expected last line: `Successfully installed ... Flask ... Flask-SocketIO ... gevent ...` (exact package versions may differ). Copy `week1/livequiz/.env.example` to `week1/livequiz/.env`, generate two different long secrets, and replace both example values. The `.env` file is ignored by Git. Never commit or send it to students.

For a laptop/LAN run, set `COOKIE_SECURE=false` and `TRUST_PROXY=false` in `.env`. For the daily bank, use `QUIZ_TOPIC=all` and set `QUIZ_DAY` to `1`, `2`, `3`, `4`, or `5`; `QUIZ_DAY=all` loads all 25 daily questions. For a topic-wise test, set `QUIZ_TOPIC` to one slug from `python week1/livequiz/scripts/check_question_bank.py --list-topics`; the selected file loads its 10 questions and takes precedence over `QUIZ_DAY`. Changing the selected bank does not erase saved responses, but the active question position is in memory and starts at the first question after restart.

## Local launch

From the repository root:

```bash
python week1/livequiz/app.py
```

Expected: the server announces `0.0.0.0:8000` and stays running. On that computer, check:

```bash
python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/healthz').read().decode())"
```

Expected: `{"session_code":"MDC301W1","status":"ok"}` (JSON key order may vary). Open `/host` on the instructor computer and `/` on student devices. For the LAN, students use `http://<instructor-laptop-private-IP>:8000/`, not `localhost`. Ask campus IT to check the port/firewall and client isolation before class; a Docker or Wi-Fi guest network may block student-to-laptop traffic.

## Day filtering and question schema

`questions.json` remains the source for the five-question-per-day bank. The independent JSON files in `topic_banks/` each contain a complete `quiz` object with exactly 10 topic questions. Their interchange schema uses `multiple_choice`, `true_false`, or `word_cloud`; `correct` is a zero-based option index, and a word-cloud item omits `options` and `correct`. `topic_bank.py` validates each file and maps zero-based indexes to the live app's A–E keys without changing the source JSON. The supervised/unsupervised topic maps to course Chapter 1; the filename uses `topic03_...` only as a topic sequence label because the supplied guide's Chapter 3 is outside Week 1.

Set `QUIZ_TOPIC` to a slug printed by `check_question_bank.py --list-topics` to run one 10-question topic test; the selected topic overrides `QUIZ_DAY`. Use `QUIZ_TOPIC=all` for the existing daily bank. At startup the server validates the selected quiz and filters the legacy bank by `QUIZ_DAY` only in daily mode. Keys and explanations are withheld from student browsers until the host reveals an MCQ. The bundled browser Socket.IO file is local, so the live session does not fetch a JavaScript CDN.

The topic JSON is a clean interchange source. ClassQuiz, Mentimeter, and open.mentimeter may require their own native import template or conversion; the bundled live app loads these topic files directly.

## Host controls and result export

1. For the Flask server option only, open `/host`, enter the `ADMIN_TOKEN` from the instructor-only `.env`, then open host controls. GitHub Pages does not have a host login.
2. Project the session code and join address. Flask-server participants provide a display alias and may enter an optional GitHub username. The public Pages quiz requires no student sign-in. The browser stores the alias/optional username and reconnect ID in local storage; on a shared device students can use **Clear saved identity from this browser** after the quiz.
3. Reveal/close the current question, then select **Next question**. The host view shows aggregate MCQ counts and a one-word cloud. Review word responses before projecting them.
4. Select **Download CSV** after class. The export contains only answered responses and the optional handle/alias. It is sensitive course data: store it outside Git, restrict access, and delete it according to the institution's retention policy.

For score reconciliation, copy `nickname_map.example.csv` to a private folder and fill it only with instructor-verified `display_name,github_username` pairs. Then run `scripts/join_week1_results.py` against the quiz export and the current Classroom 50 score CSV; ambiguous aliases are reported for review, never guessed. The combined output is formative only.

The server stores responses in `week1/livequiz/data/responses.sqlite3` for a local run; Git ignores that directory. SQLite uses write-ahead logging (WAL), a mode that lets readers continue while short database writes are recorded. One process and one worker are required. A restart preserves saved responses but resets question position. Export before changing quiz days or restarting if you need a copy of results.

## Optional VPS deployment for the Flask server

The recommended GitHub Pages path needs no VPS. If you choose the Flask server instead, `compose.yaml`, `Dockerfile`, and `Caddyfile` show a one-worker HTTPS deployment that does not expose SQLite to the network. Public hosting still requires an administrator to set secure cookies, proxy trust, unique secrets, DNS, firewall access on TCP 80/443, backups, and retention. If you are new to Docker/self-hosting, use GitHub Pages or ask IT to operate the server.

## Synthetic load check

With the server already running, install the quiz requirements and use a separate device/VM on the same network:

```bash
python week1/livequiz/scripts/load_test_socketio.py --url http://192.168.1.20:8000 --session-code MDC301W1 --clients 200
```

Replace `192.168.1.20` with the instructor's private IPv4 address. Expected if this single test succeeds: `Connections and answer acknowledgements: 200/200` and `Failures: 0`. This synthetic rehearsal is not a guarantee of 200-device capacity; check the actual access point and devices, and arrange a paper/offline fallback.
