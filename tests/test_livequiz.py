import csv
import io
import json
from pathlib import Path

import pytest

import week1.livequiz.app as livequiz_app
from week1.livequiz.app import create_app, socketio


@pytest.fixture
def live_app(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-secret-key",
        "ADMIN_TOKEN": "test-only-admin-key",
        "SESSION_CODE": "TESTW1",
        "DATABASE_PATH": str(tmp_path / "responses.sqlite3"),
        "QUESTION_BANK": str(Path(__file__).parents[1] / "week1" / "livequiz" / "questions.json"),
        "QUIZ_DAY": "1",
        "COOKIE_SECURE": False,
        "TRUST_PROXY": False,
    })
    return app


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


def test_bank_is_valid_and_has_five_questions_for_each_day(live_app):
    with live_app.app_context():
        questions = live_app.extensions["week1_questions"]
    assert len(questions) == 5
    assert {question["day"] for question in questions} == {1}
    assert any(question["type"] == "word_cloud" for question in questions)
    assert any(question["id"] == "ch08_q03_residual_plot" for question in json.loads(
        Path(live_app.config["QUESTION_BANK"]).read_text(encoding="utf-8")
    )["questions"])
    all_bank = json.loads(Path(live_app.config["QUESTION_BANK"]).read_text(encoding="utf-8"))["questions"]
    assert len(all_bank) == 25
    assert {day: sum(q["day"] == day for q in all_bank) for day in range(1, 6)} == {day: 5 for day in range(1, 6)}


def test_student_page_health_and_host_gate(live_app):
    browser = live_app.test_client()
    health = browser.get("/healthz")
    assert health.status_code == 200
    assert health.json == {"status": "ok", "session_code": "TESTW1"}
    student_page = browser.get("/")
    assert student_page.status_code == 200
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
    assert state["id"] == "ch01_q01_target_feature"
    assert "correct" not in state and "explanation" not in state

    student.emit("submit_answer", {
        "participant_id": "student_001",
        "question_id": state["id"],
        "answer": "C",
    })
    ack = event_data(student.get_received(), "answer_ack")
    assert ack and ack[0]["already_submitted"] is False
    student.emit("submit_answer", {
        "participant_id": "student_001",
        "question_id": state["id"],
        "answer": "A",
    })
    duplicate_ack = event_data(student.get_received(), "answer_ack")
    assert duplicate_ack == [{"already_submitted": True, "answer": {"key": "C"}}]

    host.emit("host_reveal")
    revealed = event_data(student.get_received(), "question_state")
    assert revealed[-1]["revealed"] is True
    assert revealed[-1]["correct"] == "C"
    assert "explanation" in revealed[-1]

    export = host_browser.get("/export.csv")
    assert export.status_code == 200
    rows = list(csv.DictReader(io.StringIO(export.data.decode("utf-8"))))
    assert len(rows) == 1
    assert rows[0]["github_username"] == "learner-gh"
    assert rows[0]["display_name"] == "'=formula"
    assert rows[0]["is_correct"] == "True"
    host.disconnect()
    student.disconnect()


def test_bad_session_and_bad_word_cloud_are_rejected(live_app):
    browser = live_app.test_client()
    bad_client = socketio.test_client(live_app, flask_test_client=browser)
    bad_client.emit("join_session", {
        "participant_id": "student_002",
        "display_name": "Learner",
        "github_username": "",
        "session_code": "WRONG",
    })
    assert event_data(bad_client.get_received(), "join_error")

    host_browser, host = host_client(live_app)
    student, events = join_student(live_app, participant_id="student_003", github_username="")
    for _ in range(4):
        host.emit("host_advance")
        host.get_received()
        student_events = student.get_received()
    word_state = event_data(student_events, "question_state")[-1]
    assert word_state["type"] == "word_cloud"

    student.emit("submit_answer", {
        "participant_id": "student_003",
        "question_id": word_state["id"],
        "answer": "too many words",
    })
    assert event_data(student.get_received(), "answer_error")
    student.emit("submit_answer", {
        "participant_id": "student_003",
        "question_id": word_state["id"],
        "answer": "Monitor",
    })
    assert event_data(student.get_received(), "answer_ack")
    summaries = event_data(host.get_received(), "live_summary")
    summary = [item for item in summaries if item.get("question_id") == word_state["id"]][-1]
    assert summary["word_cloud"] == {"monitor": 1}
    host.disconnect()
    student.disconnect()
