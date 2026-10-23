"""Static no-login Pages quiz checks."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "week1" / "livequiz" / "pages"
BANKS = ROOT / "week1" / "livequiz" / "topic_banks"


class _Ids(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name == "id" and value:
                self.ids.append(value)


def test_root_pages_redirect_and_nested_app_path() -> None:
    root = (ROOT / "index.html").read_text(encoding="utf-8")
    app = (PAGES / "app.js").read_text(encoding="utf-8")
    assert "./week1/livequiz/pages/" in root
    assert 'fetch(`../topic_banks/${encodeURIComponent(slug)}.json`' in app


def test_selector_matches_all_eight_valid_topic_banks() -> None:
    app = (PAGES / "app.js").read_text(encoding="utf-8")
    slugs = set(re.findall(r'\{ slug: "([a-z0-9_]+)"', app))
    files = {path.stem for path in BANKS.glob("*.json")}
    assert len(slugs) == 8
    assert slugs == files
    for slug in slugs:
        quiz = json.loads((BANKS / f"{slug}.json").read_text(encoding="utf-8"))["quiz"]
        assert quiz["topic_slug"] == slug
        assert len(quiz["questions"]) == 10


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


def test_supabase_sql_is_insert_only_for_anonymous_visitors() -> None:
    sql = (PAGES / "supabase_setup.sql").read_text(encoding="utf-8").lower()
    assert "enable row level security" in sql
    assert re.search(r"for\s+insert\s+to\s+anon\s+with check\s*\(\s*true\s*\)", sql)
    assert "grant insert on table public.week1_quiz_responses to anon" in sql
    assert "revoke all on table public.week1_quiz_responses from public, anon, authenticated" in sql
    assert not re.search(r"for\s+(select|update|delete)\s+to\s+anon", sql)


def test_instructions_cover_public_access_and_static_limitations() -> None:
    instructions = (ROOT / "instructions.txt").read_text(encoding="utf-8").lower()
    assert "deploy from a branch" in instructions
    assert "do not need a github account" in instructions
    assert "does not synchronize" in instructions
    assert "no live class-results screen" in instructions
    assert "service_role" in instructions
    assert "not a secure exam" in instructions
