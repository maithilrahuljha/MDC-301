from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "week1" / "livequiz" / "scripts" / "check_question_bank.py"


def test_question_bank_checker_accepts_both_phase_files():
    result = subprocess.run(
        [sys.executable, str(CHECKER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "quiz1=before_lab1_questions.json questions=8" in result.stdout
    assert "quiz2=between_lab1_and_lab2_questions.json questions=12" in result.stdout
    assert "total_questions=20" in result.stdout


def test_question_bank_checker_can_select_one_phase():
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--quiz", "quiz2"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "quiz2=between_lab1_and_lab2_questions.json questions=12" in result.stdout
    assert "total_questions=12" in result.stdout
