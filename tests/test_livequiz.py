import csv
import io
import json
from pathlib import Path

import pytest

import week1.livequiz.app as livequiz_app
from week1.livequiz.app import create_app, socketio

ROOT = Path(__file__).parents[1]
LIVEQUIZ = ROOT / "week1" / "livequiz"


@pytest.fixture
def live_app(tmp_path):
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-secret-key",
        "ADMIN_TOKEN": "test-only-admin-key",
        "SESSION_CODE": "TESTW1",
        "DATABASE_PATH": str(tmp_path / "responses.sqlite3"),
        "QUIZ_ID": "quiz1",
        "COOKIE_SECURE": False,
        "TRUST_PROXY": False,
    })


def test_relative_database_path_resolves_under_app_directory(monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", "data/relative-test.sqlite3")
    monkeypatch.setattr(livequiz_app, "init_db", lambda app: None)
    monkeypatch.setattr(livequiz_app, "load_questions", lambda app: [])
    app = create_app({"TESTING": True, "SECRET_KEY": "test-key", "ADMIN_TOKEN": "test-token"})
    expected = livequiz_app.ROOT / "data" / "relative-test.sqlite3"
    assert Path(app.config["DATABASE_PATH"]) == expected


def host_client(app):
    browser = app.test_client()
    login = browser.post("/host", data={"admin_token": "test-only-admin-key"})
    assert login.status_code == 302
    client = socketio.test_client(app, flask_test_client=browser)
    client.emit("host_auth")
    assert any(event["name"] == "host_state" for event in client.get_received())
    return browser, client


def join_student(app, participant_id="student_001", display_name="Learner", github_username="learner-gh"):
    browser = app.test_client()
    client = socketio.test_client(app, flask_test_client=browser)
    client.emit("join_session", {
        "participant_id": participant_id,
        "display_name": display_name,
        "github_username": github_username,
        "session_code": "TESTW1",
    })
    events = client.get_received()
    assert any(event["name"] == "joined" for event in events)
    return client, events


def event_data(events, name):
    return [event["args"][0] for event in events if event["name"] == name]


def test_quiz1_loads_q1_to_q8_and_withholds_the_answer(live_app):
    questions = live_app.extensions["week1_questions"]
    assert [question["id"] for question in questions] == [f"Q{number}" for number in range(1, 9)]
    assert {question["phase"] for question in questions} == {"BEFORE LAB 1 — HOUR 1"}
    assert live_app.extensions["week1_quiz_metadata"]["question_count"] == 8
    assert questions[0]["correct"] == "B"

    student, events = join_student(live_app)
    state = event_data(events, "question_state")[0]
    assert state["id"] == "Q1"
    assert state["slide"] == 5
    assert "correct" not in state and "explanation" not in state
    student.disconnect()


def test_quiz2_loads_q9_to_q20(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "quiz2-test-secret",
        "ADMIN_TOKEN": "quiz2-test-admin",
        "SESSION_CODE": "TESTQ2",
        "DATABASE_PATH": str(tmp_path / "quiz2.sqlite3"),
        "QUIZ_ID": "quiz2",
        "COOKIE_SECURE": False,
        "TRUST_PROXY": False,
    })
    questions = app.extensions["week1_questions"]
    assert [question["id"] for question in questions] == [f"Q{number}" for number in range(9, 21)]
    assert {question["phase"] for question in questions} == {"BETWEEN LAB 1 AND LAB 2 — HOUR 2"}
    assert app.extensions["week1_quiz_metadata"]["question_count"] == 12
    assert [question["slide"] for question in questions] == [21, 23, 25, 26, 28, 29, 30, 33, 34, 35, 36, 37]


def test_student_page_health_and_host_gate(live_app):
    browser = live_app.test_client()
    health = browser.get("/healthz")
    assert health.status_code == 200
    assert health.json == {"status": "ok", "session_code": "TESTW1"}
    student_page = browser.get("/")
    assert student_page.status_code == 200
    assert b"BEFORE LAB 1" in student_page.data
    assert b"GitHub password" not in student_page.data
    assert b"phone number" in student_page.data
    assert b"Clear saved identity" in student_page.data
    static_client = browser.get("/static/vendor/socket.io.min.js")
    assert static_client.status_code == 200 and len(static_client.data) > 10_000
    assert browser.get("/export.csv").status_code == 401
    assert browser.get("/host").status_code == 200
    assert browser.post("/host", data={"admin_token": "wrong"}).status_code == 401


def test_join_answer_reveal_and_formula_safe_csv(live_app):
    host_browser, host = host_client(live_app)
    student, events = join_student(live_app, display_name="=formula", github_username="learner-gh")
    state = event_data(events, "question_state")[0]
    assert state["id"] == "Q1"
    assert "correct" not in state and "explanation" not in state

    student.emit("submit_answer", {
        "participant_id": "student_001",
        "question_id": state["id"],
        "answer": "B",
    })
    ack = event_data(student.get_received(), "answer_ack")
    assert ack and ack[0]["already_submitted"] is False
    student.emit("submit_answer", {
        "participant_id": "student_001",
        "question_id": state["id"],
        "answer": "A",
    })
    duplicate_ack = event_data(student.get_received(), "answer_ack")
    assert duplicate_ack == [{"already_submitted": True, "answer": {"key": "B"}}]

    host.emit("host_reveal")
    revealed = event_data(student.get_received(), "question_state")
    assert revealed[-1]["revealed"] is True
    assert revealed[-1]["correct"] == "B"
    assert "ML learns from data" in revealed[-1]["explanation"]

    export = host_browser.get("/export.csv")
    assert export.status_code == 200
    rows = list(csv.DictReader(io.StringIO(export.data.decode("utf-8"))))
    assert len(rows) == 1
    assert rows[0]["question_id"] == "Q1"
    assert rows[0]["github_username"] == "learner-gh"
    assert rows[0]["display_name"] == "'=formula"
    assert rows[0]["is_correct"] == "True"
    host.disconnect()
    student.disconnect()


def test_bad_session_and_bad_multiple_choice_key_are_rejected(live_app):
    browser = live_app.test_client()
    bad_client = socketio.test_client(live_app, flask_test_client=browser)
    bad_client.emit("join_session", {
        "participant_id": "student_002",
        "display_name": "Learner",
        "github_username": "",
        "session_code": "WRONG",
    })
    assert event_data(bad_client.get_received(), "join_error")

    student, events = join_student(live_app, participant_id="student_003", github_username="")
    state = event_data(events, "question_state")[0]
    student.emit("submit_answer", {
        "participant_id": "student_003",
        "question_id": state["id"],
        "answer": "not-an-option",
    })
    assert event_data(student.get_received(), "answer_error")
    student.disconnect()
    bad_client.disconnect()


def test_bank_source_files_contain_only_the_two_replacement_quizzes():
    quiz1 = json.loads((LIVEQUIZ / "before_lab1_questions.json").read_text(encoding="utf-8"))
    quiz2 = json.loads((LIVEQUIZ / "between_lab1_and_lab2_questions.json").read_text(encoding="utf-8"))
    assert [question["id"] for question in quiz1["questions"]] == [f"Q{n}" for n in range(1, 9)]
    assert [question["id"] for question in quiz2["questions"]] == [f"Q{n}" for n in range(9, 21)]
    assert {path.name for path in LIVEQUIZ.glob("*questions.json")} == {
        "before_lab1_questions.json",
        "between_lab1_and_lab2_questions.json",
    }
