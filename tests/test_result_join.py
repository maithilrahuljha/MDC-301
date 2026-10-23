import csv
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "week1" / "livequiz" / "scripts" / "join_week1_results.py"


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run_join(quiz, grades, output, nickname_map=None):
    command = [sys.executable, str(SCRIPT), "--quiz", str(quiz), "--grades", str(grades), "--out", str(output)]
    if nickname_map:
        command.extend(["--nickname-map", str(nickname_map)])
    return subprocess.run(command, capture_output=True, text=True, check=False)


def load_output(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_join_uses_handles_and_verified_aliases_without_guessing(tmp_path):
    quiz = tmp_path / "quiz.csv"
    grades = tmp_path / "grades.csv"
    aliases = tmp_path / "nickname_map.csv"
    output = tmp_path / "joined.csv"
    write_csv(quiz, ["display_name", "github_username", "question_type", "is_correct"], [
        {"display_name": "=Alice", "github_username": "@ALICE", "question_type": "mcq", "is_correct": "True"},
        {"display_name": "J", "github_username": "", "question_type": "word_cloud", "is_correct": ""},
        {"display_name": "Pair", "github_username": "", "question_type": "mcq", "is_correct": "False"},
    ])
    # Classroom 50's web score export uses plural "usernames" for individual rows.
    write_csv(grades, ["usernames", "score", "max_score"], [
        {"usernames": "alice", "score": "9", "max_score": "16"},
        {"usernames": "bob", "score": "12", "max_score": "16"},
        {"usernames": "charlie", "score": "14", "max_score": "16"},
    ])
    write_csv(aliases, ["display_name", "github_username"], [
        {"display_name": "J", "github_username": "bob"},
        {"display_name": "Pair", "github_username": "bob"},
        {"display_name": "Pair", "github_username": "charlie"},
    ])

    result = run_join(quiz, grades, output, aliases)
    assert result.returncode == 0, result.stderr
    rows = load_output(output)
    by_handle = {row["github_username"]: row for row in rows if row["github_username"]}
    assert by_handle["alice"]["classroom50_grade"] == "9"
    assert by_handle["alice"]["classroom50_max_score"] == "16"
    assert by_handle["alice"]["match_status"] == "matched"
    assert by_handle["alice"]["mcq_correct"] == "1"
    assert by_handle["alice"]["display_names"] == "'=Alice"
    assert by_handle["bob"]["quiz_questions_answered"] == "1"
    assert by_handle["bob"]["classroom50_grade"] == "12"
    assert by_handle["charlie"]["match_status"] == "grade only; no quiz response"
    ambiguous = [row for row in rows if row["match_status"].startswith("unmatched")]
    assert len(ambiguous) == 1
    assert ambiguous[0]["display_names"] == "Pair"
    assert "more than one" in ambiguous[0]["review_note"]
    assert "manual review required" in ambiguous[0]["match_status"]


def test_cli_score_export_uses_latest_submission_first(tmp_path):
    quiz = tmp_path / "quiz.csv"
    grades = tmp_path / "scores.csv"
    output = tmp_path / "joined.csv"
    write_csv(quiz, ["display_name", "github_username", "question_type", "is_correct"], [
        {"display_name": "Student", "github_username": "student", "question_type": "mcq", "is_correct": "True"},
    ])
    write_csv(grades, ["username", "score", "max_score", "datetime", "submission_tag"], [
        {"username": "student", "score": "12", "max_score": "16", "datetime": "2026-10-20T12:00:00Z", "submission_tag": "submit/new"},
        {"username": "student", "score": "8", "max_score": "16", "datetime": "2026-10-19T12:00:00Z", "submission_tag": "submit/old"},
    ])
    result = run_join(quiz, grades, output)
    assert result.returncode == 0, result.stderr
    row = next(row for row in load_output(output) if row["github_username"] == "student")
    assert row["classroom50_grade"] == "12"
    assert row["classroom50_max_score"] == "16"
