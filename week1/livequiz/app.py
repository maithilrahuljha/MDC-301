"""Small, formative-only MDC-301 Week 1 live quiz server.

A single Flask-SocketIO process holds the current question state. SQLite WAL
persists participant answers. This is intentionally not an exam/LMS platform.
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import secrets
import sqlite3
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_socketio import SocketIO, emit, join_room
from werkzeug.middleware.proxy_fix import ProxyFix

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

socketio = SocketIO()


def _truthy(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    database_path = Path(os.getenv("DATABASE_PATH", "data/responses.sqlite3"))
    if not database_path.is_absolute():
        database_path = ROOT / database_path
    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "local-development-secret-change-me"),
        ADMIN_TOKEN=os.getenv("ADMIN_TOKEN", "change-me-before-sharing"),
        SESSION_CODE=os.getenv("SESSION_CODE", "MDC301W1").strip().upper(),
        DATABASE_PATH=str(database_path),
        QUESTION_BANK=os.getenv("QUESTION_BANK", str(ROOT / "questions.json")),
        QUIZ_DAY=os.getenv("QUIZ_DAY", "all").strip().lower(),
        COOKIE_SECURE=_truthy("COOKIE_SECURE", "false"),
        TRUST_PROXY=_truthy("TRUST_PROXY", "false"),
        SQLITE_TIMEOUT=20,
        MAX_CONTENT_LENGTH=100_000,
    )
    if test_config:
        app.config.update(test_config)

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = bool(app.config["COOKIE_SECURE"])

    app.extensions["week1_quiz_state"] = {
        "current_index": 0,
        "revealed": False,
        "host_sids": set(),
    }

    # Socket.IO must be kept to one worker unless a shared message queue and
    # sticky sessions are deliberately added. See the deployment guide.
    socketio.init_app(
        app,
        async_mode=os.getenv("SOCKETIO_ASYNC_MODE", "gevent"),
        cors_allowed_origins=None,
        ping_interval=25,
        ping_timeout=60,
        max_http_buffer_size=1_000_000,
        logger=False,
        engineio_logger=False,
    )
    if app.config["TRUST_PROXY"]:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    _register_routes(app)
    init_db(app)
    load_questions(app)
    return app


def _database_path() -> Path:
    return Path(current_app.config["DATABASE_PATH"])


def _connect() -> sqlite3.Connection:
    path = _database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(
        str(path), timeout=float(current_app.config.get("SQLITE_TIMEOUT", 20))
    )
    connection.row_factory = sqlite3.Row
    timeout_ms = int(float(current_app.config.get("SQLITE_TIMEOUT", 20)) * 1000)
    connection.execute(f"PRAGMA busy_timeout = {timeout_ms}")
    return connection


def init_db(app: Flask) -> None:
    """Create the persistent tables; safe to call again after changing DB path in tests."""
    with app.app_context():
        with _connect() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS participants (
                    participant_id TEXT PRIMARY KEY,
                    session_code TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    github_username TEXT NOT NULL DEFAULT '',
                    joined_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS responses (
                    session_code TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    participant_id TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    github_username TEXT NOT NULL DEFAULT '',
                    question_type TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    is_correct INTEGER,
                    submitted_at TEXT NOT NULL,
                    PRIMARY KEY (session_code, question_id, participant_id)
                );
                CREATE INDEX IF NOT EXISTS idx_responses_question
                    ON responses(session_code, question_id);
                CREATE INDEX IF NOT EXISTS idx_responses_user
                    ON responses(session_code, github_username);
                """
            )


def load_questions(app: Flask | None = None) -> list[dict[str, Any]]:
    """Read, validate, and optionally select one day's question bank."""
    target_app = app or current_app
    bank_path = Path(target_app.config["QUESTION_BANK"])
    with bank_path.open(encoding="utf-8") as stream:
        payload = json.load(stream)
    questions = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(questions, list) or not questions:
        raise ValueError("Question bank must contain a non-empty 'questions' list")
    seen: set[str] = set()
    for q in questions:
        if not isinstance(q, dict):
            raise ValueError("Every question must be a JSON object")
        qid = str(q.get("id", ""))
        if not re.fullmatch(r"[a-z0-9_]{4,80}", qid) or qid in seen:
            raise ValueError(f"Question id is invalid or duplicated: {qid!r}")
        seen.add(qid)
        if not isinstance(q.get("day"), int) or q["day"] not in range(1, 6):
            raise ValueError(f"Question {qid} must have an integer day from 1 to 5")
        if not str(q.get("chapter", "")).strip() or not str(q.get("task", "")).strip():
            raise ValueError(f"Question {qid} needs a chapter and worksheet task")
        if q.get("type") not in {"mcq", "word_cloud"}:
            raise ValueError(f"Unsupported question type for {qid}: {q.get('type')!r}")
        if not str(q.get("prompt", "")).strip():
            raise ValueError(f"Question {qid} needs a prompt")
        if q["type"] == "mcq":
            choices = q.get("choices", [])
            if not isinstance(choices, list) or not 2 <= len(choices) <= 5:
                raise ValueError(f"MCQ {qid} must have 2 to 5 choices")
            if any(not isinstance(choice, dict) for choice in choices):
                raise ValueError(f"MCQ {qid} choices must be objects")
            keys = [str(choice.get("key", "")).strip() for choice in choices]
            if (
                len(set(keys)) != len(keys)
                or any(not key for key in keys)
                or any(not str(choice.get("text", "")).strip() for choice in choices)
                or str(q.get("correct", "")) not in keys
            ):
                raise ValueError(f"MCQ {qid} needs unique non-empty choices and one valid correct key")
        else:
            try:
                max_length = int(q.get("max_length", 35))
                max_words = int(q.get("max_words", 1))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Word cloud {qid} needs numeric limits") from exc
            if not 1 <= max_length <= 35 or max_words != 1:
                raise ValueError(f"Word cloud {qid} must accept exactly one word, up to 35 characters")

    day_filter = str(target_app.config.get("QUIZ_DAY", "all")).strip().lower()
    if day_filter in {"", "all", "0"}:
        selected = questions
    elif day_filter in {"1", "2", "3", "4", "5"}:
        selected = [question for question in questions if question["day"] == int(day_filter)]
        if not selected:
            raise ValueError(f"Question bank has no questions for day {day_filter}")
    else:
        raise ValueError("QUIZ_DAY must be 'all' or a day number from 1 to 5")
    if app is not None:
        app.extensions["week1_questions"] = selected
    return selected


def _state() -> dict[str, Any]:
    return current_app.extensions["week1_quiz_state"]


def _questions() -> list[dict[str, Any]]:
    """Return the validated question list cached when the app was created."""
    questions = current_app.extensions.get("week1_questions")
    if questions is None:
        return load_questions()
    return questions


def _question_payload(index: int, *, host: bool = False) -> dict[str, Any] | None:
    questions = _questions()
    if index < 0 or index >= len(questions):
        return None
    q = questions[index]
    revealed = bool(_state()["revealed"])
    payload = {
        "id": q["id"],
        "day": q["day"],
        "chapter": q["chapter"],
        "task": q["task"],
        "type": q["type"],
        "prompt": q["prompt"],
        "index": index + 1,
        "total": len(questions),
        "revealed": revealed,
    }
    if q["type"] == "mcq":
        payload["choices"] = q["choices"]
    else:
        payload["max_length"] = int(q.get("max_length", 35))
        payload["max_words"] = int(q.get("max_words", 1))
    if host or revealed:
        if q["type"] == "mcq":
            payload["correct"] = q["correct"]
        payload["explanation"] = q.get("explanation", "")
    return payload


def _response_for(participant_id: str, question_id: str) -> sqlite3.Row | None:
    with _connect() as connection:
        return connection.execute(
            """SELECT answer, is_correct FROM responses
               WHERE session_code=? AND question_id=? AND participant_id=?""",
            (current_app.config["SESSION_CODE"], question_id, participant_id),
        ).fetchone()


def _live_summary(question: dict[str, Any]) -> dict[str, Any]:
    with _connect() as connection:
        rows = connection.execute(
            """SELECT answer, is_correct FROM responses
               WHERE session_code=? AND question_id=?""",
            (current_app.config["SESSION_CODE"], question["id"]),
        ).fetchall()
    total = len(rows)
    summary: dict[str, Any] = {"question_id": question["id"], "answered": total}
    if question["type"] == "mcq":
        counts = Counter(json.loads(row["answer"]).get("key", "") for row in rows)
        summary["counts"] = {str(c["key"]): int(counts.get(str(c["key"]), 0)) for c in question["choices"]}
        summary["correct"] = question["correct"] if _state()["revealed"] else None
    else:
        words: Counter[str] = Counter()
        for row in rows:
            text = str(json.loads(row["answer"]).get("text", "")).strip()
            if text:
                words[unicodedata.normalize("NFKC", text).casefold()] += 1
        summary["word_cloud"] = dict(words.most_common(40))
    return summary


def _emit_host_summary(question: dict[str, Any]) -> None:
    summary = _live_summary(question)
    for sid in list(_state()["host_sids"]):
        socketio.emit("live_summary", summary, to=sid)


def _csv_safe(value: Any) -> Any:
    """Prevent user-controlled CSV cells from being interpreted as formulas."""
    if not isinstance(value, str):
        return value
    if value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def _register_routes(app: Flask) -> None:
    @app.get("/")
    def student_page() -> str:
        return render_template("student.html", session_code=current_app.config["SESSION_CODE"])

    @app.route("/host", methods=["GET", "POST"])
    def host_page() -> str | Response:
        if request.method == "POST":
            supplied = request.form.get("admin_token", "")
            expected = str(current_app.config["ADMIN_TOKEN"])
            if secrets.compare_digest(supplied, expected) and expected != "change-me-before-sharing":
                session["host_authenticated"] = True
                return redirect(url_for("host_page"))
            return render_template("host.html", authenticated=False, error="The host key did not match."), 401
        if not session.get("host_authenticated"):
            return render_template("host.html", authenticated=False, error="")
        return render_template(
            "host.html",
            authenticated=True,
            session_code=current_app.config["SESSION_CODE"],
            join_url=request.url_root.rstrip("/"),
        )

    @app.get("/healthz")
    def healthz() -> Response:
        return jsonify(status="ok", session_code=current_app.config["SESSION_CODE"])

    @app.get("/export.csv")
    def export_csv() -> Response:
        if not session.get("host_authenticated"):
            return jsonify(error="host login required"), 401
        with _connect() as connection:
            rows = connection.execute(
                """SELECT session_code, question_id, display_name, github_username,
                          question_type, answer, is_correct, submitted_at
                   FROM responses WHERE session_code=?
                   ORDER BY submitted_at, question_id, display_name""",
                (current_app.config["SESSION_CODE"],),
            ).fetchall()
        output = io.StringIO(newline="")
        columns = [
            "session_code", "question_id", "display_name", "github_username",
            "question_type", "answer", "is_correct", "submitted_at",
        ]
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            item = dict(row)
            answer = json.loads(item["answer"])
            item["answer"] = answer.get("text", answer.get("key", ""))
            if item["is_correct"] is not None:
                item["is_correct"] = bool(item["is_correct"])
            writer.writerow({key: _csv_safe(value) for key, value in item.items()})
        response = Response(output.getvalue(), mimetype="text/csv; charset=utf-8")
        response.headers["Content-Disposition"] = 'attachment; filename="mdc301_week1_live_responses.csv"'
        response.headers["Cache-Control"] = "no-store"
        return response


@socketio.on("connect")
def on_connect(auth: Any = None) -> None:
    emit("server_ready", {"session_code": current_app.config["SESSION_CODE"]})


@socketio.on("disconnect")
def on_disconnect(reason: Any = None) -> None:
    _state()["host_sids"].discard(request.sid)


@socketio.on("join_session")
def on_join_session(data: Any) -> None:
    data = data if isinstance(data, dict) else {}
    session_code = str(data.get("session_code", "")).strip().upper()
    participant_id = str(data.get("participant_id", "")).strip()
    display_name = re.sub(r"\s+", " ", str(data.get("display_name", "")).strip())[:32]
    github_username = str(data.get("github_username", "")).strip().lstrip("@")[:39]
    if session_code != current_app.config["SESSION_CODE"]:
        emit("join_error", {"message": "That session code does not match. Check the projected code."})
        return
    if not re.fullmatch(r"[A-Za-z0-9_-]{3,64}", participant_id):
        emit("join_error", {"message": "The browser could not create a participant ID. Refresh and try again."})
        return
    if not display_name:
        emit("join_error", {"message": "Enter a display name or a short classroom alias."})
        return
    if github_username and not re.fullmatch(r"[A-Za-z0-9-]{1,39}", github_username):
        emit("join_error", {"message": "GitHub handles may contain letters, numbers, and hyphens only."})
        return

    now = datetime.now(timezone.utc).isoformat()
    with _connect() as connection:
        connection.execute(
            """INSERT INTO participants(participant_id, session_code, display_name, github_username, joined_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(participant_id) DO UPDATE SET
                 session_code=excluded.session_code,
                 display_name=excluded.display_name,
                 github_username=excluded.github_username""",
            (participant_id, session_code, display_name, github_username, now),
        )
        participant_count = connection.execute(
            "SELECT COUNT(*) AS n FROM participants WHERE session_code=?", (session_code,)
        ).fetchone()["n"]

    join_room(session_code)
    emit("joined", {"display_name": display_name, "session_code": session_code})
    current = _question_payload(_state()["current_index"])
    if current:
        emit("question_state", current)
        prior = _response_for(participant_id, current["id"])
        if prior:
            emit("answer_ack", {"already_submitted": True, "answer": json.loads(prior["answer"])})
    socketio.emit("participant_count", {"count": int(participant_count)}, room=session_code)
    if current:
        _emit_host_summary(_questions()[_state()["current_index"]])


@socketio.on("host_auth")
def on_host_auth(data: Any = None) -> None:
    if not session.get("host_authenticated"):
        emit("host_error", {"message": "Open /host and enter the instructor key first."})
        return
    code = current_app.config["SESSION_CODE"]
    join_room(code)
    _state()["host_sids"].add(request.sid)
    emit("host_state", {
        "question": _question_payload(_state()["current_index"], host=True),
        "participant_count": _participant_count(),
    })
    if _state()["current_index"] < len(_questions()):
        emit("live_summary", _live_summary(_questions()[_state()["current_index"]]))


def _participant_count() -> int:
    with _connect() as connection:
        row = connection.execute(
            "SELECT COUNT(*) AS n FROM participants WHERE session_code=?",
            (current_app.config["SESSION_CODE"],),
        ).fetchone()
    return int(row["n"])


def _host_only() -> bool:
    if request.sid not in _state()["host_sids"]:
        emit("host_error", {"message": "Only the authenticated instructor can control this session."})
        return False
    return True


@socketio.on("host_reveal")
def on_host_reveal(data: Any = None) -> None:
    if not _host_only():
        return
    index = _state()["current_index"]
    questions = _questions()
    if index >= len(questions):
        return
    _state()["revealed"] = True
    question = questions[index]
    socketio.emit("question_state", _question_payload(index), room=current_app.config["SESSION_CODE"])
    for sid in list(_state()["host_sids"]):
        socketio.emit("host_question_state", _question_payload(index, host=True), to=sid)
    _emit_host_summary(question)


@socketio.on("host_advance")
def on_host_advance(data: Any = None) -> None:
    if not _host_only():
        return
    questions = _questions()
    next_index = _state()["current_index"] + 1
    if next_index >= len(questions):
        _state()["current_index"] = len(questions)
        socketio.emit("session_complete", {"total": len(questions)}, room=current_app.config["SESSION_CODE"])
        return
    _state()["current_index"] = next_index
    _state()["revealed"] = False
    question = questions[next_index]
    socketio.emit("question_state", _question_payload(next_index), room=current_app.config["SESSION_CODE"])
    for sid in list(_state()["host_sids"]):
        socketio.emit("host_question_state", _question_payload(next_index, host=True), to=sid)
    _emit_host_summary(question)


@socketio.on("submit_answer")
def on_submit_answer(data: Any) -> None:
    data = data if isinstance(data, dict) else {}
    participant_id = str(data.get("participant_id", "")).strip()
    question_id = str(data.get("question_id", "")).strip()
    index = _state()["current_index"]
    questions = _questions()
    if index >= len(questions):
        emit("answer_error", {"message": "The quiz has finished."})
        return
    q = questions[index]
    if _state()["revealed"]:
        emit("answer_error", {"message": "This question is closed; wait for the next one."})
        return
    if question_id != q["id"]:
        emit("answer_error", {"message": "This answer is for an old question. Reconnect to the current one."})
        return

    with _connect() as connection:
        participant = connection.execute(
            """SELECT display_name, github_username FROM participants
               WHERE participant_id=? AND session_code=?""",
            (participant_id, current_app.config["SESSION_CODE"]),
        ).fetchone()
    if not participant:
        emit("answer_error", {"message": "Join the session before submitting an answer."})
        return

    is_correct: int | None
    if q["type"] == "mcq":
        key = str(data.get("answer", "")).strip()
        valid_keys = {str(choice["key"]) for choice in q["choices"]}
        if key not in valid_keys:
            emit("answer_error", {"message": "Choose one of the displayed options."})
            return
        answer_payload = {"key": key}
        is_correct = int(key == str(q["correct"]))
    else:
        text = re.sub(r"\s+", " ", str(data.get("answer", "")).strip())
        max_length = int(q.get("max_length", 35))
        max_words = int(q.get("max_words", 1))
        if not text or len(text) > max_length or len(text.split()) > max_words:
            emit("answer_error", {"message": f"Enter {max_words} word(s), up to {max_length} characters."})
            return
        answer_payload = {"text": text}
        is_correct = None

    submitted_at = datetime.now(timezone.utc).isoformat()
    with _connect() as connection:
        result = connection.execute(
            """INSERT INTO responses(
                   session_code, question_id, participant_id, display_name, github_username,
                   question_type, answer, is_correct, submitted_at
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(session_code, question_id, participant_id) DO NOTHING""",
            (
                current_app.config["SESSION_CODE"], q["id"], participant_id,
                participant["display_name"], participant["github_username"], q["type"],
                json.dumps(answer_payload, ensure_ascii=False), is_correct, submitted_at,
            ),
        )
        inserted = result.rowcount == 1
        if inserted:
            saved_answer = answer_payload
        else:
            saved = connection.execute(
                """SELECT answer FROM responses
                   WHERE session_code=? AND question_id=? AND participant_id=?""",
                (current_app.config["SESSION_CODE"], q["id"], participant_id),
            ).fetchone()
            saved_answer = json.loads(saved["answer"]) if saved else answer_payload
    emit("answer_ack", {"already_submitted": not inserted, "answer": saved_answer})
    _emit_host_summary(q)


app = create_app()


if __name__ == "__main__":
    unsafe_values = {
        "change-me-before-sharing",
        "local-development-secret-change-me",
        "replace-with-a-long-random-secret",
        "replace-with-a-different-long-random-secret",
    }
    if app.config["ADMIN_TOKEN"] in unsafe_values or app.config["SECRET_KEY"] in unsafe_values:
        raise SystemExit(
            "Set unique FLASK_SECRET_KEY and ADMIN_TOKEN values in week1/livequiz/.env before starting."
        )
    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        debug=False,
        allow_unsafe_werkzeug=False,
    )
