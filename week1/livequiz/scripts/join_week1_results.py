#!/usr/bin/env python3
"""Join formative quiz responses to a Classroom 50 grade export by GitHub handle.

Nicknames are never used as identity unless the instructor provides a manually
verified --nickname-map CSV. Ambiguous aliases remain unmatched for review.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

HANDLE_HEADERS = {
    "githubusername", "githubuser", "username", "usernames", "github", "login", "user",
    "studentusername", "studentgithubusername", "ghusername", "repositoryowner",
}
GRADE_HEADERS = {"score", "grade", "points", "autogradescore", "currentgrade", "totalpoints"}
MAX_SCORE_HEADERS = {"maxscore", "maximumscore", "maxpoints", "pointspossible"}


def compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def normalize_handle(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^https?://github\.com/", "", value, flags=re.I).strip("/")
    value = value.rsplit("/", 1)[-1].lstrip("@").strip()
    return value.casefold()


def normalize_name(value: str) -> str:
    return " ".join(value.split()).casefold()


def choose_column(
    headers: list[str], candidates: set[str], explicit: str | None, label: str, required: bool = True
) -> str | None:
    if explicit:
        if explicit not in headers:
            raise ValueError(f"{label} column {explicit!r} is not in CSV headers: {headers}")
        return explicit
    matches = [header for header in headers if compact(header) in candidates]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"Several {label} columns match {matches}; pass an explicit --{label.replace(' ', '-').lower()}-column")
    if required:
        raise ValueError(
            f"Could not find a {label} column in headers {headers}. "
            f"Pass --{label.replace(' ', '-').lower()}-column with the exact header name."
        )
    return None


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header row: {path}")
        rows = list(reader)
        return list(reader.fieldnames), rows


def load_aliases(path: Path | None) -> dict[str, set[str]]:
    aliases: dict[str, set[str]] = defaultdict(set)
    if path is None:
        return aliases
    headers, rows = read_csv(path)
    name_column = choose_column(headers, {"displayname", "nickname", "alias"}, None, "display name")
    handle_column = choose_column(headers, HANDLE_HEADERS, None, "GitHub username")
    for line, row in enumerate(rows, start=2):
        name = normalize_name(row.get(name_column or "", ""))
        handle = normalize_handle(row.get(handle_column or "", ""))
        if not name or not handle:
            raise ValueError(f"Nickname map row {line} needs both display_name and github_username")
        aliases[name].add(handle)
    return aliases


def as_correct(value: str) -> bool:
    return value.strip().casefold() in {"1", "true", "yes", "y"}


def spreadsheet_safe(value: Any) -> Any:
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiz", required=True, type=Path, help="CSV downloaded from the quiz host")
    parser.add_argument("--grades", required=True, type=Path, help="Classroom 50 grade CSV with a GitHub handle and score")
    parser.add_argument("--nickname-map", type=Path, help="Optional, instructor-verified CSV: display_name,github_username")
    parser.add_argument("--out", required=True, type=Path, help="Destination combined CSV; keep outside Git")
    parser.add_argument("--quiz-handle-column", help="Exact GitHub username column in quiz CSV")
    parser.add_argument("--grade-handle-column", help="Exact GitHub username/login column in grade CSV")
    parser.add_argument("--grade-column", help="Exact numeric score column in grade CSV")
    parser.add_argument("--grade-max-column", help="Exact maximum-points column in grade CSV (optional)")
    args = parser.parse_args()

    try:
        quiz_headers, quiz_rows = read_csv(args.quiz)
        grade_headers, grade_rows = read_csv(args.grades)
        quiz_handle_col = choose_column(quiz_headers, HANDLE_HEADERS, args.quiz_handle_column, "quiz handle", required=False)
        grade_handle_col = choose_column(grade_headers, HANDLE_HEADERS, args.grade_handle_column, "grade handle")
        grade_col = choose_column(grade_headers, GRADE_HEADERS, args.grade_column, "grade")
        grade_max_col = choose_column(
            grade_headers, MAX_SCORE_HEADERS, args.grade_max_column, "grade max", required=False
        )
        aliases = load_aliases(args.nickname_map)

        # CLI downloads include multiple attempt rows per student, newest first;
        # the web export is one row per student. Preserve only the first CLI row.
        attempt_export = bool({compact(header) for header in grade_headers} & {"submissiontag", "datetime"})
        grades: dict[str, tuple[str, str]] = {}
        for line, row in enumerate(grade_rows, start=2):
            handle = normalize_handle(row.get(grade_handle_col or "", ""))
            if not handle:
                raise ValueError(f"Grade export row {line} has no GitHub handle")
            if handle in grades:
                if attempt_export:
                    continue
                raise ValueError(f"Grade export has more than one row for @{handle}; resolve duplicates before joining")
            grades[handle] = (
                row.get(grade_col or "", "").strip(),
                row.get(grade_max_col or "", "").strip() if grade_max_col else "",
            )

        stats: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"names": set(), "answered": 0, "mcq_answered": 0, "mcq_correct": 0}
        )
        unmatched: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"names": set(), "answered": 0, "mcq_answered": 0, "mcq_correct": 0, "reason": "no verified handle"}
        )
        for line, row in enumerate(quiz_rows, start=2):
            display_name = " ".join(row.get("display_name", "").split())
            raw_handle = row.get(quiz_handle_col, "") if quiz_handle_col else ""
            handle = normalize_handle(raw_handle)
            if not handle:
                candidates = aliases.get(normalize_name(display_name), set())
                if len(candidates) == 1:
                    handle = next(iter(candidates))
                elif len(candidates) > 1:
                    key = f"{display_name} (ambiguous alias)"
                    bucket = unmatched[key]
                    bucket["reason"] = "nickname map contains more than one matching GitHub handle"
                    bucket["names"].add(display_name)
                    bucket["answered"] += 1
                    if row.get("question_type", "").casefold() == "mcq":
                        bucket["mcq_answered"] += 1
                        bucket["mcq_correct"] += int(as_correct(row.get("is_correct", "")))
                    continue
            if not handle:
                key = display_name or f"quiz row {line}"
                bucket = unmatched[key]
                bucket["names"].add(display_name)
                bucket["answered"] += 1
                if row.get("question_type", "").casefold() == "mcq":
                    bucket["mcq_answered"] += 1
                    bucket["mcq_correct"] += int(as_correct(row.get("is_correct", "")))
                continue

            bucket = stats[handle]
            bucket["names"].add(display_name)
            bucket["answered"] += 1
            if row.get("question_type", "").casefold() == "mcq":
                bucket["mcq_answered"] += 1
                bucket["mcq_correct"] += int(as_correct(row.get("is_correct", "")))

        args.out.parent.mkdir(parents=True, exist_ok=True)
        fields = [
            "github_username", "display_names", "quiz_questions_answered", "mcq_answered",
            "mcq_correct", "formative_mcq_accuracy", "classroom50_grade", "classroom50_max_score",
            "match_status", "review_note",
        ]
        with args.out.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for handle in sorted(set(grades) | set(stats)):
                values = stats.get(handle, {"names": set(), "answered": 0, "mcq_answered": 0, "mcq_correct": 0})
                mcq_answered = values["mcq_answered"]
                accuracy = f"{values['mcq_correct'] / mcq_answered:.4f}" if mcq_answered else ""
                status = "matched" if handle in grades and handle in stats else (
                    "grade only; no quiz response" if handle in grades else "quiz handle not in grade export"
                )
                grade_score, grade_max = grades.get(handle, ("", ""))
                writer.writerow({
                    "github_username": spreadsheet_safe(handle),
                    "display_names": spreadsheet_safe(" | ".join(sorted(name for name in values["names"] if name))),
                    "quiz_questions_answered": values["answered"],
                    "mcq_answered": mcq_answered,
                    "mcq_correct": values["mcq_correct"],
                    "formative_mcq_accuracy": accuracy,
                    "classroom50_grade": spreadsheet_safe(grade_score),
                    "classroom50_max_score": spreadsheet_safe(grade_max),
                    "match_status": status,
                    "review_note": "Formative summary only; do not treat as an exam score.",
                })
            for name in sorted(unmatched):
                values = unmatched[name]
                mcq_answered = values["mcq_answered"]
                accuracy = f"{values['mcq_correct'] / mcq_answered:.4f}" if mcq_answered else ""
                writer.writerow({
                    "github_username": "",
                    "display_names": spreadsheet_safe(" | ".join(sorted(values["names"]))),
                    "quiz_questions_answered": values["answered"],
                    "mcq_answered": mcq_answered,
                    "mcq_correct": values["mcq_correct"],
                    "formative_mcq_accuracy": accuracy,
                    "classroom50_grade": "",
                    "match_status": "unmatched; manual review required",
                    "review_note": spreadsheet_safe(values["reason"]),
                })

        print(f"Saved {len(set(grades) | set(stats)) + len(unmatched)} rows to {args.out}")
        print(f"Grade handles: {len(grades)}; quiz handles: {len(stats)}; unmatched quiz identities: {len(unmatched)}")
        print("Nickname matching is only applied from the supplied map; verify every alias before using this formative summary.")
        return 0
    except (OSError, ValueError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
