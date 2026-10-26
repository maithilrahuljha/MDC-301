#!/usr/bin/env python3
"""Check the two Week 1 phase quiz files and their Q1–Q20 IDs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
LIVEQUIZ_DIR = ROOT / "week1" / "livequiz"
QUIZZES = {
    "quiz1": ("before_lab1_questions.json", range(1, 9)),
    "quiz2": ("between_lab1_and_lab2_questions.json", range(9, 21)),
}


def validate_quiz(quiz_id: str) -> tuple[int, list[int]]:
    filename, numbers = QUIZZES[quiz_id]
    path = LIVEQUIZ_DIR / filename
    payload: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{filename} must contain a JSON object")
    if payload.get("file") != filename or payload.get("quiz_id") != quiz_id:
        raise ValueError(f"{filename} file/quiz metadata does not match {quiz_id}")
    if payload.get("course") != "MDC-301" or payload.get("week") != 1:
        raise ValueError(f"{filename} must identify MDC-301 Week 1")
    if not all(isinstance(payload.get(key), str) and payload[key].strip() for key in ("title", "phase", "instructions")):
        raise ValueError(f"{filename} needs a title, phase, and instructions")

    questions = payload.get("questions")
    expected_ids = [f"Q{number}" for number in numbers]
    if not isinstance(questions, list) or [q.get("id") if isinstance(q, dict) else None for q in questions] != expected_ids:
        raise ValueError(f"{filename} must contain IDs {expected_ids[0]} through {expected_ids[-1]} in order")

    slides: list[int] = []
    for question in questions:
        qid = question["id"]
        if question.get("phase") != payload["phase"]:
            raise ValueError(f"{qid} phase does not match {filename}")
        slide = question.get("slide")
        if type(slide) is not int or slide < 1:
            raise ValueError(f"{qid} needs a positive integer slide number")
        slides.append(slide)
        if question.get("type") != "multiple_choice":
            raise ValueError(f"{qid} must be a multiple-choice question")
        if not isinstance(question.get("question"), str) or not question["question"].strip():
            raise ValueError(f"{qid} needs question text")
        options = question.get("options")
        if not isinstance(options, dict) or list(options) != ["A", "B", "C", "D"]:
            raise ValueError(f"{qid} must have A–D options in order")
        if any(not isinstance(value, str) or not value.strip() for value in options.values()):
            raise ValueError(f"{qid} has an empty option")
        correct = question.get("correct_option")
        if correct not in options or question.get("correct_answer") != options[correct]:
            raise ValueError(f"{qid} has inconsistent correct-option metadata")
        if not isinstance(question.get("explanation"), str) or not question["explanation"].strip():
            raise ValueError(f"{qid} needs an explanation")

    if payload.get("slides") != slides:
        raise ValueError(f"{filename} slides list must match question slide order")
    return len(questions), slides


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--quiz", choices=sorted(QUIZZES), help="check one phase quiz")
    group.add_argument("--list-quizzes", action="store_true", help="list the two selectable quiz IDs")
    args = parser.parse_args(argv)

    if args.list_quizzes:
        for quiz_id, (filename, numbers) in QUIZZES.items():
            print(f"{quiz_id}\t{filename}\tQ{numbers.start}–Q{numbers.stop - 1}")
        return 0

    quiz_ids = [args.quiz] if args.quiz else list(QUIZZES)
    for quiz_id in quiz_ids:
        count, slides = validate_quiz(quiz_id)
        filename = QUIZZES[quiz_id][0]
        print(f"{quiz_id}={filename} questions={count} slides={slides}")
    print(f"total_questions={sum(validate_quiz(quiz_id)[0] for quiz_id in quiz_ids)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Quiz-bank validation failed: {error}") from error
