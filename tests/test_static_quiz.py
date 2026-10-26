"""Static no-login Pages quiz checks."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "week1" / "livequiz" / "pages"
LIVEQUIZ = ROOT / "week1" / "livequiz"
QUIZ_FILES = {"before_lab1_questions.json", "between_lab1_and_lab2_questions.json"}


class _Ids(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name == "id" and value:
                self.ids.append(value)


def test_root_pages_redirect_and_static_app_loads_phase_files() -> None:
    root = (ROOT / "index.html").read_text(encoding="utf-8")
    app = (PAGES / "app.js").read_text(encoding="utf-8")
    assert "./week1/livequiz/pages/" in root
    assert 'fetch(`../${encodeURIComponent(quizDefinition.file)}`' in app
    assert {path.name for path in LIVEQUIZ.glob("*questions.json")} == QUIZ_FILES


def test_selector_matches_both_replacement_quizzes() -> None:
    app = (PAGES / "app.js").read_text(encoding="utf-8")
    files = set(re.findall(r'file: "([a-z0-9_]+\.json)"', app))
    slugs = set(re.findall(r'slug: "(quiz[12])"', app))
    assert files == QUIZ_FILES
    assert slugs == {"quiz1", "quiz2"}
    for filename, first, last in (
        ("before_lab1_questions.json", 1, 8),
        ("between_lab1_and_lab2_questions.json", 9, 20),
    ):
        quiz = json.loads((LIVEQUIZ / filename).read_text(encoding="utf-8"))
        assert [item["id"] for item in quiz["questions"]] == [f"Q{number}" for number in range(first, last + 1)]


def test_page_contains_every_dom_id_used_by_app() -> None:
    parser = _Ids()
    parser.feed((PAGES / "index.html").read_text(encoding="utf-8"))
    app = (PAGES / "app.js").read_text(encoding="utf-8")
    refs = set(re.findall(r'\$\("([a-z0-9-]+)"\)', app))
    assert len(parser.ids) == len(set(parser.ids))
    assert refs <= set(parser.ids)


def test_config_is_blank_and_practice_never_posts_answers() -> None:
    config = (PAGES / "config.js").read_text(encoding="utf-8")
    app = (PAGES / "app.js").read_text(encoding="utf-8")
    assert re.search(r'url:\s*""', config)
    assert re.search(r'anonKey:\s*""', config)
    assert "service_role" in config
    assert 'if (state.mode === "practice")' in app
    assert 'method: "POST"' in app
    assert "practice answers are never uploaded" in app.lower()


def test_supabase_sql_accepts_new_quiz_slugs_and_keeps_insert_only_policy() -> None:
    sql = (PAGES / "supabase_setup.sql").read_text(encoding="utf-8").lower()
    assert "add constraint week1_quiz_responses_topic_slug_check check (topic_slug in (" in sql
    assert "'quiz1', 'quiz2'" in sql
    assert "^q([1-9]|1[0-9]|20)$" in sql
    assert "enable row level security" in sql
    assert re.search(r"for\s+insert\s+to\s+anon\s+with check\s*\(\s*true\s*\)", sql)
    assert "grant insert on table public.week1_quiz_responses to anon" in sql
    assert "revoke all on table public.week1_quiz_responses from public, anon, authenticated" in sql
    assert not re.search(r"for\s+(select|update|delete)\s+to\s+anon", sql)


def test_local_launch_instructions_cover_vs_code_and_private_server() -> None:
    instructions = (ROOT / "live_quiz.txt").read_text(encoding="utf-8").lower()
    assert "vs code" in instructions
    assert "quiz_id=quiz1" in instructions
    assert "quiz_id=quiz2" in instructions
    assert "127.0.0.1" in instructions
    assert "do not expose" in instructions
