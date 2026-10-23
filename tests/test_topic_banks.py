import json
from pathlib import Path

import pytest

from week1.livequiz.app import create_app, socketio
from week1.livequiz.topic_bank import (
    TOPIC_BANK_DIR,
    TOPIC_MANIFEST,
    load_topic_quiz,
    to_live_questions,
    validate_topic_quiz,
)


def event_data(events, name):
    return [event["args"][0] for event in events if event["name"] == name]


def test_eight_topic_files_are_self_contained_and_have_ten_questions_each():
    assert {path.stem for path in TOPIC_BANK_DIR.glob("*.json")} == set(TOPIC_MANIFEST)
    ids = set()
    for slug, expected in TOPIC_MANIFEST.items():
        quiz = load_topic_quiz(TOPIC_BANK_DIR / f"{slug}.json", expected_slug=slug)
        assert quiz["question_count"] == 10
        assert len(quiz["questions"]) == 10
        assert quiz["day"] == expected["day"]
        assert quiz["chapter"] == expected["chapter"]
        for question in quiz["questions"]:
            assert question["id"] not in ids
            ids.add(question["id"])
            if question["type"] in {"multiple_choice", "true_false"}:
                assert type(question["correct"]) is int
                assert 0 <= question["correct"] < len(question["options"])
            else:
                assert question["type"] == "word_cloud"
                assert "options" not in question and "correct" not in question

    # This topic is Chapter 1 content; the supplied guide's Chapter 3 is careers.
    supervised = load_topic_quiz(
        TOPIC_BANK_DIR / "topic03_supervised_vs_unsupervised.json",
        expected_slug="topic03_supervised_vs_unsupervised",
    )
    assert supervised["chapter"] == "ch01"
    assert supervised["source_chapters"] == ["ch01"]


def test_zero_based_answers_convert_to_live_letter_keys():
    quiz = load_topic_quiz(TOPIC_BANK_DIR / "ch01_intro_to_ml.json")
    live_questions = to_live_questions(quiz)
    assert len(live_questions) == 10
    assert live_questions[0]["correct"] == "B"  # source index 1
    assert live_questions[0]["choices"][1] == {
        "key": "B",
        "text": quiz["questions"][0]["options"][1],
    }

    lifecycle = load_topic_quiz(TOPIC_BANK_DIR / "ch02_ml_lifecycle.json")
    cloud = to_live_questions(lifecycle)[-1]
    assert cloud["type"] == "word_cloud"
    assert "correct" not in cloud and "choices" not in cloud
    assert cloud["max_words"] == 1


def test_app_runs_selected_topic_as_ten_question_test(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "topic-test-secret",
        "ADMIN_TOKEN": "topic-test-admin",
        "SESSION_CODE": "TOPIC1",
        "DATABASE_PATH": str(tmp_path / "topic.sqlite3"),
        "QUESTION_BANK": str(Path(__file__).parents[1] / "week1" / "livequiz" / "questions.json"),
        "TOPIC_BANK_DIR": str(TOPIC_BANK_DIR),
        "QUIZ_TOPIC": "ch08_simple_linear_regression",
        # Topic mode takes precedence over the legacy daily filter.
        "QUIZ_DAY": "1",
        "COOKIE_SECURE": False,
        "TRUST_PROXY": False,
    })
    questions = app.extensions["week1_questions"]
    assert len(questions) == 10
    assert {question["day"] for question in questions} == {3}
    assert app.extensions["week1_quiz_metadata"]["topic_slug"] == "ch08_simple_linear_regression"

    student_browser = app.test_client()
    page = student_browser.get("/")
    assert b"Simple Linear Regression" in page.data
    assert b"10 questions" in page.data
    student = socketio.test_client(app, flask_test_client=student_browser)
    student.emit("join_session", {
        "participant_id": "topic_student_1",
        "display_name": "Learner",
        "github_username": "",
        "session_code": "TOPIC1",
    })
    state = event_data(student.get_received(), "question_state")[0]
    assert state["id"] == "simple_reg_q01"
    assert state["topic_name"] == "Simple Linear Regression"
    assert "correct" not in state

    host_browser = app.test_client()
    assert host_browser.post("/host", data={"admin_token": "topic-test-admin"}).status_code == 302
    host = socketio.test_client(app, flask_test_client=host_browser)
    host.emit("host_auth")
    host.get_received()
    host.emit("host_reveal")
    revealed = event_data(student.get_received(), "question_state")[-1]
    assert revealed["correct"] == "B"
    student.disconnect()
    host.disconnect()


def test_topic_validator_rejects_non_zero_based_answer_index():
    payload = json.loads((TOPIC_BANK_DIR / "ch01_intro_to_ml.json").read_text(encoding="utf-8"))
    payload["quiz"]["questions"][0]["correct"] = len(payload["quiz"]["questions"][0]["options"])
    with pytest.raises(ValueError, match="zero-based index"):
        validate_topic_quiz(payload)
