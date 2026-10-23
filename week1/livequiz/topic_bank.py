"""Validation and adapter for self-contained Week 1 topic quiz files.

The public topic-bank schema stores zero-based answer indexes. The live app
uses its existing letter-key schema internally; this module converts between
those formats without changing the importable source files.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

TOPIC_BANK_DIR = Path(__file__).resolve().parent / "topic_banks"
QUESTION_COUNT = 10
_OPTION_KEYS = ("A", "B", "C", "D", "E")
_ID_RE = re.compile(r"[a-z0-9_]{4,80}\Z")
_QUIZ_ID_RE = re.compile(r"[a-z0-9-]{4,80}\Z")

# The supervised/unsupervised topic is course Chapter 1 material, not the
# supplied guide's career-focused Chapter 3. Keep this mapping explicit so a
# topic sequence number is never mistaken for the guide's chapter number.
TOPIC_MANIFEST: dict[str, dict[str, Any]] = {
    "ch01_intro_to_ml": {
        "day": 1,
        "chapter": "ch01",
        "source_chapters": ["ch01"],
        "topic_name": "Introduction to Machine Learning",
    },
    "ch02_ml_lifecycle": {
        "day": 1,
        "chapter": "ch02",
        "source_chapters": ["ch02"],
        "topic_name": "Machine Learning Model Lifecycle",
    },
    "topic03_supervised_vs_unsupervised": {
        "day": 1,
        "chapter": "ch01",
        "source_chapters": ["ch01"],
        "topic_name": "Supervised vs Unsupervised Learning",
    },
    "ch05_tools_and_sklearn": {
        "day": 2,
        "chapter": "ch05-ch06",
        "source_chapters": ["ch05", "ch06"],
        "topic_name": "Tools and the Scikit-learn Ecosystem",
    },
    "ch08_simple_linear_regression": {
        "day": 3,
        "chapter": "ch08",
        "source_chapters": ["ch08"],
        "topic_name": "Simple Linear Regression",
    },
    "ch09_multiple_linear_regression": {
        "day": 4,
        "chapter": "ch09",
        "source_chapters": ["ch09"],
        "topic_name": "Multiple Linear Regression",
    },
    "ch10_polynomial_and_regularisation": {
        "day": 4,
        "chapter": "ch10",
        "source_chapters": ["ch10"],
        "topic_name": "Polynomial and Regularised Regression",
    },
    "ch12_logistic_regression": {
        "day": 5,
        "chapter": "ch11-ch12",
        "source_chapters": ["ch11", "ch12"],
        "topic_name": "Logistic Regression",
    },
}


def validate_topic_quiz(
    payload: Any,
    *,
    expected_slug: str | None = None,
    require_ten: bool = True,
) -> dict[str, Any]:
    """Validate a standalone quiz object and return its inner ``quiz`` mapping."""
    if not isinstance(payload, dict) or not isinstance(payload.get("quiz"), dict):
        raise ValueError("A topic file must be a JSON object containing a 'quiz' object")
    quiz = payload["quiz"]
    required = {
        "id", "name", "course", "week", "day", "chapter", "topic_slug",
        "topic_name", "source_chapters", "question_count", "questions",
    }
    missing = sorted(required - quiz.keys())
    if missing:
        raise ValueError(f"Topic quiz is missing required metadata: {', '.join(missing)}")

    slug = quiz["topic_slug"]
    if not isinstance(slug, str) or slug not in TOPIC_MANIFEST:
        raise ValueError(f"Unknown topic_slug: {slug!r}")
    if expected_slug is not None and slug != expected_slug:
        raise ValueError(f"Topic slug {slug!r} does not match selected file {expected_slug!r}")
    if not isinstance(quiz["id"], str) or not _QUIZ_ID_RE.fullmatch(quiz["id"]):
        raise ValueError("Quiz id must contain only lowercase letters, digits, or hyphens")
    if not isinstance(quiz["name"], str) or not quiz["name"].strip():
        raise ValueError("Topic quiz needs a non-empty name")
    if quiz["course"] != "MDC-301" or type(quiz["week"]) is not int or quiz["week"] != 1:
        raise ValueError("Topic quiz metadata must identify MDC-301 Week 1")

    expected = TOPIC_MANIFEST[slug]
    if type(quiz["day"]) is not int or quiz["day"] != expected["day"]:
        raise ValueError(f"Topic {slug} must be assigned to day {expected['day']}")
    if quiz["chapter"] != expected["chapter"]:
        raise ValueError(f"Topic {slug} must map to course chapter {expected['chapter']}")
    if quiz["topic_name"] != expected["topic_name"]:
        raise ValueError(f"Topic {slug} must use the name {expected['topic_name']!r}")
    if quiz["source_chapters"] != expected["source_chapters"]:
        raise ValueError(f"Topic {slug} has incorrect source-chapter metadata")

    questions = quiz["questions"]
    if not isinstance(questions, list) or not questions:
        raise ValueError(f"Topic {slug} must contain a non-empty questions list")
    if type(quiz["question_count"]) is not int or quiz["question_count"] != len(questions):
        raise ValueError(f"Topic {slug} question_count must equal the number of questions")
    if require_ten and len(questions) != QUESTION_COUNT:
        raise ValueError(f"Topic {slug} must contain exactly {QUESTION_COUNT} questions")

    seen_ids: set[str] = set()
    for number, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Question {number} in {slug} must be an object")
        question_id = question.get("id")
        if not isinstance(question_id, str) or not _ID_RE.fullmatch(question_id):
            raise ValueError(f"Question {number} in {slug} has an invalid id")
        if question_id in seen_ids:
            raise ValueError(f"Duplicate question id {question_id!r} in {slug}")
        seen_ids.add(question_id)
        if not isinstance(question.get("question"), str) or not question["question"].strip():
            raise ValueError(f"Question {question_id} needs non-empty question text")
        time_limit = question.get("time_limit", 25)
        if type(time_limit) is not int or not 5 <= time_limit <= 180:
            raise ValueError(f"Question {question_id} time_limit must be an integer from 5 to 180")
        if "explanation" in question and not isinstance(question["explanation"], str):
            raise ValueError(f"Question {question_id} explanation must be text")

        question_type = question.get("type")
        if question_type in {"multiple_choice", "true_false"}:
            options = question.get("options")
            if not isinstance(options, list) or not 2 <= len(options) <= len(_OPTION_KEYS):
                raise ValueError(f"Question {question_id} needs 2 to 5 options")
            if any(not isinstance(option, str) or not option.strip() for option in options):
                raise ValueError(f"Question {question_id} options must be non-empty text")
            if len({option.strip().casefold() for option in options}) != len(options):
                raise ValueError(f"Question {question_id} options must be unique")
            correct = question.get("correct")
            if type(correct) is not int or not 0 <= correct < len(options):
                raise ValueError(f"Question {question_id} correct must be a valid zero-based index")
            if question_type == "true_false" and options != ["True", "False"]:
                raise ValueError(f"True/false question {question_id} must use ['True', 'False'] options")
        elif question_type == "word_cloud":
            if "options" in question or "correct" in question:
                raise ValueError(f"Word-cloud question {question_id} must omit options and correct")
            max_length = question.get("max_length", 35)
            max_words = question.get("max_words", 1)
            if type(max_length) is not int or not 1 <= max_length <= 35 or type(max_words) is not int or max_words != 1:
                raise ValueError(f"Word-cloud question {question_id} must accept exactly one word up to 35 characters")
        else:
            raise ValueError(f"Unsupported question type for {question_id}: {question_type!r}")

    return quiz


def load_topic_quiz(path: str | Path, *, expected_slug: str | None = None) -> dict[str, Any]:
    """Read and validate one standalone topic file."""
    bank_path = Path(path)
    try:
        payload = json.loads(bank_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read topic bank {bank_path}: {exc}") from exc
    return validate_topic_quiz(payload, expected_slug=expected_slug)


def to_live_questions(quiz: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert validated zero-based topic questions to the live app's key schema."""
    quiz = validate_topic_quiz({"quiz": quiz})
    converted: list[dict[str, Any]] = []
    for item in quiz["questions"]:
        live: dict[str, Any] = {
            "id": item["id"],
            "day": quiz["day"],
            "chapter": quiz["chapter"],
            "task": quiz["topic_name"],
            "topic_slug": quiz["topic_slug"],
            "topic_name": quiz["topic_name"],
            "source_chapters": quiz["source_chapters"],
            "prompt": item["question"],
            "time_limit": item.get("time_limit", 25),
            "explanation": item.get("explanation", ""),
        }
        if item["type"] == "word_cloud":
            live.update(
                type="word_cloud",
                max_length=int(item.get("max_length", 35)),
                max_words=int(item.get("max_words", 1)),
            )
        else:
            options = item["options"]
            keys = list(_OPTION_KEYS[:len(options)])
            live.update(
                type="mcq",
                choices=[{"key": key, "text": text} for key, text in zip(keys, options)],
                correct=keys[item["correct"]],
                source_type=item["type"],
            )
        converted.append(live)
    return converted


def available_topics() -> list[dict[str, Any]]:
    """Return the topic selectors in a stable, instructor-friendly order."""
    return [
        {"slug": slug, **metadata}
        for slug, metadata in TOPIC_MANIFEST.items()
    ]
