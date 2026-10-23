#!/usr/bin/env python3
"""Validate and summarize the course's importable five-day question bank."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

BANK = Path(__file__).resolve().parents[1] / "questions.json"


def main() -> int:
    data = json.loads(BANK.read_text(encoding="utf-8"))
    questions = data["questions"]
    counts = Counter(question["day"] for question in questions)
    days = sorted(counts)
    if days != [1, 2, 3, 4, 5] or any(counts[day] != 5 for day in days):
        raise SystemExit("Expected exactly five questions for each day 1–5.")
    print(f"questions={len(questions)} days={days} per_day={[counts[day] for day in days]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
