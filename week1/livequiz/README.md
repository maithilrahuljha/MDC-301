# MDC-301 Week 1 live check

The live-quiz scaffold source in this directory is MIT-licensed; see [`LICENSE`](LICENSE). The locally vendored Socket.IO browser client and the capstone dataset retain their separate notices/licenses.

A small formative, browser-based quiz for five course days. Socket.IO (a library for two-way live messages between a browser and server) carries questions and answers. The bank contains 25 questions (five per day), multiple-choice questions (MCQs) plus a one-word cloud on every day. SQLite (a small local file database) stores responses; a teacher can download a CSV (comma-separated values spreadsheet). It is not an exam platform, attendance system, or independently load-certified 200-user service.

**Terms:** a *LAN* (local-area network) is the private Wi-Fi/network shared by the instructor laptop and student devices; a `.env` file holds private app settings and secrets; *HTTPS* is the encrypted web connection used on a public server; *DNS* maps a hostname to a server address; a *VPS* is a rented virtual private server.

## Requirements and private setup

Python 3.11+ is recommended for local use. From the repository root:

```bash
python -m venv .venv
python -m pip install --disable-pip-version-check -r week1/livequiz/requirements.txt
```

Expected last line: `Successfully installed ... Flask ... Flask-SocketIO ... gevent ...` (exact package versions may differ). Copy `week1/livequiz/.env.example` to `week1/livequiz/.env`, generate two different long secrets, and replace both example values. The `.env` file is ignored by Git. Never commit or send it to students.

For a laptop/LAN run, set `COOKIE_SECURE=false`, `TRUST_PROXY=false`, and `QUIZ_DAY=1` in `.env`. Change `QUIZ_DAY` to `1`, `2`, `3`, `4`, or `5` before each separate daily run; `all` loads all 25 questions. Changing question day does not erase saved responses, but the active question position is in memory and starts at the first question after restart.

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

`questions.json` is the importable source bank; a restart reloads it. Each object uses:

- `id`: stable lowercase identifier, unique across the full bank.
- `day`: integer 1–5; `chapter` and `task` link to the worksheet.
- `type`: `mcq` or `word_cloud`.
- MCQ: `prompt`, 2–5 `choices` with unique keys and text, a `correct` key, and an `explanation`.
- Word cloud: `prompt`, `max_length` from 1–35, `max_words: 1`, and an explanation. The host screen renders content as text (not HTML); do not invite personal or sensitive information.

The server validates the entire JSON bank at startup, then filters it by `QUIZ_DAY`. Keys and explanations are withheld from student browsers until the host reveals an MCQ. The bundled browser Socket.IO file is local, so the live session does not fetch a JavaScript CDN.

## Host controls and result export

1. Open `/host`, enter the `ADMIN_TOKEN` from the instructor-only `.env`, then open host controls.
2. Project the session code and join address. Students provide a display alias and optional GitHub username. They never enter their GitHub password or phone number. The browser stores the alias/optional username and reconnect ID in local storage; on a shared device students can use **Clear saved identity from this browser** after the quiz.
3. Reveal/close the current question, then select **Next question**. The host view shows aggregate MCQ counts and a one-word cloud. Review word responses before projecting them.
4. Select **Download CSV** after class. The export contains only answered responses and the optional handle/alias. It is sensitive course data: store it outside Git, restrict access, and delete it according to the institution's retention policy.

For score reconciliation, copy `nickname_map.example.csv` to a private folder and fill it only with instructor-verified `display_name,github_username` pairs. Then run `scripts/join_week1_results.py` against the quiz export and the current Classroom 50 score CSV; ambiguous aliases are reported for review, never guessed. The combined output is formative only.

The server stores responses in `week1/livequiz/data/responses.sqlite3` for a local run; Git ignores that directory. SQLite uses write-ahead logging (WAL), a mode that lets readers continue while short database writes are recorded. One process and one worker are required. A restart preserves saved responses but resets question position. Export before changing quiz days or restarting if you need a copy of results.

## VPS deployment

See the complete copy/paste steps and sysadmin checklist in the root `instructions.txt`. The Docker recipe uses one Flask-SocketIO/gevent worker behind Caddy for HTTPS; it does not expose SQLite to the network. Before using a public hostname, set `COOKIE_SECURE=true`, `TRUST_PROXY=true`, use unique secrets, point DNS at the server, and allow TCP 80/443. The host key and export are private. Contact a system administrator for firewall/DNS/cloud-account tasks.

## Synthetic load check

With the server already running, install the quiz requirements and use a separate device/VM on the same network:

```bash
python week1/livequiz/scripts/load_test_socketio.py --url http://192.168.1.20:8000 --session-code MDC301W1 --clients 200
```

Replace `192.168.1.20` with the instructor's private IPv4 address. Expected if this single test succeeds: `Connections and answer acknowledgements: 200/200` and `Failures: 0`. This synthetic rehearsal is not a guarantee of 200-device capacity; check the actual access point and devices, and arrange a paper/offline fallback.
