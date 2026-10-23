#!/usr/bin/env python3
"""Check lecture navigation, placeholders, badge lines, and quiz-ID references only.

This script deliberately does not validate quiz wording, answer options, keys, or quality.
Run from any directory with: python3 scripts/check_lecture_site.py
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "lecture"
ERRORS: list[str] = []
WARNINGS: list[str] = []


class HTMLScan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str, dict[str, str | None]]] = []
        self.quiz_ids: list[str] = []
        self.text: list[str] = []
        self.recap_text: list[str] = []
        self._in_recap = False
        self._skip_recap_source = False
        self._section_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value for key, value in attrs}
        if tag in {"a", "link", "script", "img", "source"}:
            key = "src" if tag in {"script", "img", "source"} else "href"
            value = values.get(key)
            if value:
                self.links.append((tag, value, values))
        if "data-quiz-id" in values and values["data-quiz-id"]:
            self.quiz_ids.append(str(values["data-quiz-id"]))
        if tag == "section" and values.get("aria-labelledby") == "recap-title":
            self._in_recap = True
            self._section_depth = 1
        elif self._in_recap and tag == "section":
            self._section_depth += 1
        if self._in_recap and tag == "p" and "source-note" in (values.get("class") or "").split():
            self._skip_recap_source = True

    def handle_endtag(self, tag: str) -> None:
        if self._in_recap and tag == "p":
            self._skip_recap_source = False
        if self._in_recap and tag == "section":
            self._section_depth -= 1
            if self._section_depth <= 0:
                self._in_recap = False

    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self._in_recap and not self._skip_recap_source:
            self.recap_text.append(data)


def error(message: str) -> None:
    ERRORS.append(message)


def check_relative_links(html_path: Path, scan: HTMLScan) -> None:
    for tag, raw_url, attrs in scan.links:
        url = urlsplit(raw_url)
        if url.scheme or url.netloc or raw_url.startswith("#"):
            continue
        path_part = unquote(url.path)
        if not path_part:
            continue
        target = (html_path.parent / path_part).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            error(f"{html_path.relative_to(ROOT)}: link escapes repository: {raw_url}")
            continue
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            if "data-optional-file" in attrs and tag == "a":
                continue
            if raw_url.startswith("#quiz-coming-soon"):
                continue
            error(f"{html_path.relative_to(ROOT)}: missing local {tag} target {raw_url}")
        if html_path.is_relative_to(LECTURE.resolve()):
            try:
                target.relative_to(LECTURE.resolve())
            except ValueError:
                if not (tag == "a" and "data-optional-file" in attrs):
                    error(f"{html_path.relative_to(ROOT)}: required lecture asset is outside lecture/: {raw_url}")


def collect_ids(value: object, found: set[str]) -> None:
    """Read only ID fields from JSON; intentionally ignore all quiz content fields."""
    if isinstance(value, dict):
        item_id = value.get("id")
        if isinstance(item_id, str):
            found.add(item_id)
        for child in value.values():
            collect_ids(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_ids(child, found)


def check_quiz_links() -> None:
    mapping_path = LECTURE / "week1" / "quiz-links.json"
    try:
        mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
        expected_ids = mapping["ids"]
        if len(expected_ids) != len(set(expected_ids)):
            error("lecture/week1/quiz-links.json: duplicate IDs in link map")
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        error(f"Could not read Week 1 quiz link map: {exc}")
        return

    pages: set[str] = set()
    for page in sorted((LECTURE / "week1").glob("session*.html")):
        scan = HTMLScan()
        scan.feed(page.read_text(encoding="utf-8"))
        pages.update(scan.quiz_ids)
    if pages != set(expected_ids):
        error(f"Quiz ID map/page mismatch: pages={sorted(pages)}, map={sorted(expected_ids)}")

    poll_path = (mapping_path.parent / mapping.get("poll", "")).resolve()
    try:
        poll_path.relative_to(ROOT.resolve())
    except ValueError:
        error("Week 1 poll URL must be a relative path inside the repository")
        return
    if not poll_path.is_file():
        WARNINGS.append(f"Poll page is absent ({mapping.get('poll')}); runtime links should say ‘Quiz coming soon’.")

    bank_path = (mapping_path.parent / mapping.get("source", "")).resolve()
    try:
        bank_path.relative_to(ROOT.resolve())
    except ValueError:
        error("Week 1 quiz source must be a relative path inside the repository")
        return
    if not bank_path.is_file():
        WARNINGS.append(f"Quiz source is absent ({mapping.get('source')}); runtime links should say ‘Quiz coming soon’.")
        helper = (LECTURE / "shared" / "js" / "quiz-links.js").read_text(encoding="utf-8")
        if "Quiz coming soon" not in helper:
            error("quiz-links.js is missing the graceful fallback label")
        return

    try:
        payload = json.loads(bank_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(f"Quiz source is not parseable JSON: {exc}")
        return
    bank_ids: set[str] = set()
    collect_ids(payload, bank_ids)
    missing = sorted(set(expected_ids) - bank_ids)
    if missing:
        error("Question ID references absent from the existing bank: " + ", ".join(missing))
    # No question text, choices, answer keys, explanations, counts, or quality are checked.


def check_recaps() -> None:
    for session in (3, 5):
        path = LECTURE / "week1" / f"session{session}.html"
        scan = HTMLScan()
        scan.feed(path.read_text(encoding="utf-8"))
        words = re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", " ".join(scan.recap_text), flags=re.UNICODE)
        if not 200 <= len(words) <= 300:
            error(f"{path.relative_to(ROOT)} recap must contain 200–300 words; found {len(words)}")


def main() -> int:
    if not LECTURE.is_dir():
        print("ERROR: lecture/ is missing", file=sys.stderr)
        return 1

    required = [LECTURE / "index.html"]
    required += [LECTURE / f"week{week}" / "index.html" for week in range(1, 9)]
    required += [LECTURE / "week1" / f"session{session}.html" for session in range(1, 6)]
    for path in required:
        if not path.is_file():
            error(f"Required page is missing: {path.relative_to(ROOT)}")

    for week in range(2, 9):
        path = LECTURE / f"week{week}" / "index.html"
        if path.is_file():
            body = path.read_text(encoding="utf-8")
            if f"Coming in Week {week}" not in body:
                error(f"{path.relative_to(ROOT)} must contain ‘Coming in Week {week}’")

    html_pages = sorted([ROOT / "index.html"] + list(LECTURE.rglob("*.html")))
    for path in html_pages:
        if not path.is_file():
            continue
        scan = HTMLScan()
        try:
            source = path.read_text(encoding="utf-8")
            scan.feed(source)
        except (OSError, UnicodeDecodeError) as exc:
            error(f"Could not read {path.relative_to(ROOT)}: {exc}")
            continue
        check_relative_links(path.resolve(), scan)

    badge_path = LECTURE / "week1" / "badges" / "badges.json"
    try:
        badge_data = json.loads(badge_path.read_text(encoding="utf-8"))
        badge_ids = [badge["id"] for badge in badge_data["badges"]]
        if badge_ids != [f"W01-S0{n}" for n in range(1, 6)]:
            error("Week 1 badge IDs must be W01-S01 through W01-S05 in order")
        progress = (ROOT / "progress.md").read_text(encoding="utf-8")
        for badge_id in badge_ids:
            if not re.search(rf"^- \[[ xX]\] {re.escape(badge_id)} — .+", progress, flags=re.MULTILINE):
                error(f"progress.md is missing a stable badge line for {badge_id}")
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        error(f"Could not check Week 1 badge lines: {exc}")

    for session in range(1, 6):
        path = LECTURE / "week1" / f"session{session}.html"
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8")
        badge_id = f"W01-S0{session}"
        if body.count("data-quiz-id=") != 3:
            error(f"{path.relative_to(ROOT)} must reference exactly three existing quiz IDs")
        if body.count('class="bug-challenge"') != 1:
            error(f"{path.relative_to(ROOT)} must have exactly one Break it / fix it challenge")
        if f'data-session-badge="{badge_id}"' not in body or f'data-unlock-badge="{badge_id}"' not in body:
            error(f"{path.relative_to(ROOT)} is missing its stable session badge controls")
        if "After this session, you can:" not in body:
            error(f"{path.relative_to(ROOT)} is missing its one-line ability statement")
        if session in (1, 2, 4) and ("Learning objectives" not in body or "Selected derivation" not in body):
            error(f"{path.relative_to(ROOT)} outline must include objectives and a selected derivation")
        if session in (3, 5):
            for required_text in ("data-python-cell", "data-python-code", "data-pyodide-run", "Expected"):
                if required_text not in body:
                    error(f"{path.relative_to(ROOT)} is missing working-cell/fallback marker {required_text!r}")
            if "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js" not in body:
                error(f"{path.relative_to(ROOT)} is missing the pinned Pyodide script URL")

    if not (ROOT / "index.html").is_file() or "lecture/index.html" not in (ROOT / "index.html").read_text(encoding="utf-8"):
        error("root index.html must funnel users to lecture/index.html")

    check_quiz_links()
    check_recaps()

    if WARNINGS:
        for item in WARNINGS:
            print(f"WARNING: {item}")
    if ERRORS:
        for item in ERRORS:
            print(f"ERROR: {item}", file=sys.stderr)
        print(f"Lecture checks failed: {len(ERRORS)} error(s)", file=sys.stderr)
        return 1
    print("Lecture checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
