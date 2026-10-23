#!/usr/bin/env python3
"""Validate the daily bank and eight standalone topic-wise quiz banks."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LIVEQUIZ_DIR = ROOT / "week1" / "livequiz"
DAILY_BANK = LIVEQUIZ_DIR / "questions.json"
TOPIC_DIR = LIVEQUIZ_DIR / "topic_banks"
sys.path.insert(0, str(ROOT))

from week1.livequiz.topic_bank import TOPIC_MANIFEST, load_topic_quiz  # noqa: E402


def validate_daily_bank() -> tuple[int, dict[int, int]]:
    payload = json.loads(DAILY_BANK.read_text(encoding="utf-8"))
    questions = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(questions, list) or len(questions) != 25:
        raise ValueError("Daily questions.json must contain exactly 25 questions")
    counts = Counter(question.get("day") for question in questions)
    if sorted(counts) != [1, 2, 3, 4, 5] or any(counts[day] != 5 for day in range(1, 6)):
        raise ValueError("Expected exactly five daily-bank questions for each day 1–5")
    ids = [question.get("id") for question in questions]
    if any(not isinstance(qid, str) or not qid for qid in ids) or len(set(ids)) != len(ids):
        raise ValueError("Daily question ids must be present and unique")
    return len(questions), dict(counts)


def validate_all_topics() -> tuple[int, list[int]]:
    files = sorted(TOPIC_DIR.glob("*.json"))
    expected = set(TOPIC_MANIFEST)
    found = {path.stem for path in files}
    if found != expected:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        raise ValueError(f"Topic files do not match the manifest; missing={missing}, extra={extra}")
    all_ids: set[str] = set()
    quiz_ids: set[str] = set()
    counts: list[int] = []
    for slug in TOPIC_MANIFEST:
        quiz = load_topic_quiz(TOPIC_DIR / f"{slug}.json", expected_slug=slug)
        if quiz["id"] in quiz_ids:
            raise ValueError(f"Quiz id {quiz['id']!r} is duplicated across topic files")
        quiz_ids.add(quiz["id"])
        for question in quiz["questions"]:
            if question["id"] in all_ids:
                raise ValueError(f"Question id {question['id']!r} is duplicated across topic files")
            all_ids.add(question["id"])
        counts.append(len(quiz["questions"]))
    if counts != [10] * len(TOPIC_MANIFEST):
        raise ValueError("Every topic bank must contain exactly 10 questions")
    return len(files), counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--topic", choices=sorted(TOPIC_MANIFEST), help="validate one topic bank")
    group.add_argument("--list-topics", action="store_true", help="list selectable topic slugs and source chapters")
    args = parser.parse_args(argv)

    if args.list_topics:
        for slug, metadata in TOPIC_MANIFEST.items():
            chapters = ",".join(metadata["source_chapters"])
            print(f"{slug}\t{metadata['topic_name']}\t{chapters}")
        return 0

    if args.topic:
        quiz = load_topic_quiz(TOPIC_DIR / f"{args.topic}.json", expected_slug=args.topic)
        open_responses = sum(question["type"] == "word_cloud" for question in quiz["questions"])
        scored = len(quiz["questions"]) - open_responses
        print(
            f"topic={args.topic} questions={len(quiz['questions'])} "
            f"scored={scored} word_cloud={open_responses} "
            f"source_chapters={','.join(quiz['source_chapters'])}"
        )
        return 0

    daily_count, daily_counts = validate_daily_bank()
    topic_count, topic_counts = validate_all_topics()
    print(
        f"daily_questions={daily_count} days={sorted(daily_counts)} "
        f"per_day={[daily_counts[day] for day in range(1, 6)]} "
        f"topic_banks={topic_count} topic_questions={sum(topic_counts)} "
        f"per_topic={topic_counts}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        raise SystemExit(f"Question-bank validation failed: {error}") from error
