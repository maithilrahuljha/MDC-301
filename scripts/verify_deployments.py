#!/usr/bin/env python3
"""Create an instructor CSV for student Pages status and lecture integrity.

The script checks public URLs, GitHub tree hashes for lecture/, week indexes,
progress.md badge lines, and existence of configured question IDs only. It does
not inspect/validate quiz stems, choices, keys, explanations, or student code.

Usage:
  python3 scripts/verify_deployments.py --roster tools/student_roster.csv --output tools/deployment-status.csv

A GitHub token is optional for small batches. For a 200-student roster, set
GITHUB_TOKEN in the process environment (or authenticate `gh`) to avoid the
unauthenticated GitHub API rate limit. Never commit the token or roster.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "lecture"
USER_AGENT = "MDC-301-lecture-deployment-check/1.0"
TIMEOUT = 20


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def get_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    try:
        result = subprocess.run(["gh", "auth", "token"], check=True, capture_output=True, text=True, timeout=5)
        token = result.stdout.strip()
        return token or None
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def request_bytes(url: str, token: str | None = None, *, accept: str = "*/*") -> tuple[int, bytes, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.status, response.read(), response.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), exc.geturl()


def api_tree(owner: str, repo: str, branch: str, token: str | None) -> dict[str, str]:
    branch_path = urllib.parse.quote(branch, safe="")
    url = f"https://api.github.com/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/git/trees/{branch_path}?recursive=1"
    status, body, _ = request_bytes(url, token, accept="application/vnd.github+json")
    if status != 200:
        detail = body.decode("utf-8", "replace")[:220].replace("\n", " ")
        raise RuntimeError(f"GitHub tree API HTTP {status}: {detail}")
    payload = json.loads(body)
    if payload.get("truncated"):
        raise RuntimeError("GitHub tree API returned a truncated tree")
    return {
        item["path"]: item["sha"]
        for item in payload.get("tree", [])
        if item.get("type") == "blob" and isinstance(item.get("path"), str) and isinstance(item.get("sha"), str)
    }


def expected_lecture_tree() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): git_blob_sha1(path.read_bytes())
        for path in sorted(item for item in LECTURE.rglob("*") if item.is_file())
    }


def pages_base(owner: str, repo: str, override: str = "") -> str:
    if override.strip():
        return override.strip().rstrip("/") + "/"
    hostname = f"https://{owner.lower()}.github.io/"
    if repo.lower() == f"{owner.lower()}.github.io":
        return hostname
    return urllib.parse.urljoin(hostname, urllib.parse.quote(repo, safe="") + "/")


def raw_url(owner: str, repo: str, branch: str, path: str) -> str:
    branch_part = urllib.parse.quote(branch, safe="")
    encoded_path = "/".join(urllib.parse.quote(part, safe="") for part in PurePosixPath(path).parts)
    return f"https://raw.githubusercontent.com/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/{branch_part}/{encoded_path}"


def collect_ids(value: Any, found: set[str]) -> None:
    """Extract only ID strings from JSON; do not validate other quiz fields."""
    if isinstance(value, dict):
        candidate = value.get("id")
        if isinstance(candidate, str):
            found.add(candidate)
        for child in value.values():
            collect_ids(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_ids(child, found)


def repo_path_from_week1(relative_path: str) -> str:
    joined = PurePosixPath("lecture/week1") / PurePosixPath(relative_path)
    parts: list[str] = []
    for part in joined.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part not in {".", ""}:
            parts.append(part)
    return PurePosixPath(*parts).as_posix()


def read_roster(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"github_username", "repo_name"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("Roster CSV must have github_username,repo_name headers; branch and pages_url are optional")
        return [
            {key: (value or "").strip() for key, value in row.items() if key}
            for row in reader
            if (row.get("github_username") or "").strip() and (row.get("repo_name") or "").strip()
        ]


def verify_one(row: dict[str, str], expected_tree: dict[str, str], quiz_source_rel: str,
               quiz_poll_rel: str, quiz_ids: list[str], token: str | None) -> dict[str, str]:
    owner = row["github_username"].strip()
    repo = row["repo_name"].strip()
    branch = row.get("branch", "").strip() or "main"
    base = pages_base(owner, repo, row.get("pages_url", ""))
    errors: list[str] = []
    notes: list[str] = []
    result: dict[str, str] = {
        "github_username": owner,
        "repo_name": repo,
        "branch": branch,
        "pages_url": base,
        "site_http": "error",
        "lecture_hash": "error",
        "week_indexes": "error",
        "week_placeholders": "error",
        "badge_lines": "error",
        "badges_checked": "error",
        "quiz_id_references": "error",
        "status": "ERROR",
        "notes": "",
    }

    # Public Pages root.
    try:
        code, _, final_url = request_bytes(base)
        result["site_http"] = str(code)
        if code != 200:
            errors.append(f"Pages returned HTTP {code}")
        else:
            result["pages_url"] = final_url
    except Exception as exc:  # network errors are an individual row result
        errors.append(f"Pages request: {exc}")

    # One Git tree request provides all lecture blob hashes and path-existence checks.
    tree: dict[str, str] = {}
    try:
        tree = api_tree(owner, repo, branch, token)
        actual = {path: sha for path, sha in tree.items() if path.startswith("lecture/")}
        result["lecture_hash"] = "match" if actual == expected_tree else "mismatch"
        if actual != expected_tree:
            expected_paths, actual_paths = set(expected_tree), set(actual)
            missing = sorted(expected_paths - actual_paths)
            extra = sorted(actual_paths - expected_paths)
            changed = sorted(path for path in expected_paths & actual_paths if expected_tree[path] != actual[path])
            fragments = []
            if missing: fragments.append("missing=" + ",".join(missing[:3]))
            if extra: fragments.append("extra=" + ",".join(extra[:3]))
            if changed: fragments.append("changed=" + ",".join(changed[:3]))
            errors.append("lecture/ hash mismatch (" + "; ".join(fragments) + ")")
        expected_week_paths = {f"lecture/week{week}/index.html" for week in range(1, 9)}
        missing_weeks = sorted(path for path in expected_week_paths if path not in tree)
        result["week_indexes"] = "present" if not missing_weeks else "missing"
        if missing_weeks:
            errors.append("missing week index: " + ", ".join(missing_weeks))
    except Exception as exc:
        errors.append(f"GitHub tree check: {exc}")

    # Check all eight public week URLs and placeholder labels.
    http_results: list[str] = []
    placeholder_ok: list[str] = []
    for week in range(1, 9):
        week_url = urllib.parse.urljoin(base, f"lecture/week{week}/")
        try:
            code, body, _ = request_bytes(week_url)
            http_results.append(f"W{week}:{code}")
            if code == 200:
                if week == 1:
                    placeholder_ok.append(f"W{week}:content")
                else:
                    text = body.decode("utf-8", "replace")
                    if f"Coming in Week {week}" in text:
                        placeholder_ok.append(f"W{week}:ok")
                    else:
                        placeholder_ok.append(f"W{week}:wrong-label")
                        errors.append(f"Week {week} page lacks ‘Coming in Week {week}’")
            else:
                placeholder_ok.append(f"W{week}:http-{code}")
                errors.append(f"Week {week} URL returned HTTP {code}")
        except Exception as exc:
            http_results.append(f"W{week}:error")
            placeholder_ok.append(f"W{week}:error")
            errors.append(f"Week {week} request: {exc}")
    result["week_indexes"] = ";".join(http_results)
    result["week_placeholders"] = ";".join(placeholder_ok)

    # progress.md is fetched as raw text; check stable lines and completed marks separately.
    progress_path = "progress.md"
    try:
        code, body, _ = request_bytes(raw_url(owner, repo, branch, progress_path))
        if code != 200:
            result["badge_lines"] = "missing"
            result["badges_checked"] = "0/5"
            errors.append(f"progress.md raw URL returned HTTP {code}")
        else:
            progress = body.decode("utf-8", "replace")
            present = 0
            checked = 0
            for number in range(1, 6):
                badge_id = f"W01-S0{number}"
                match = re_badge_line(progress, badge_id)
                if match:
                    present += 1
                    if match[0].lower() == "x":
                        checked += 1
            result["badge_lines"] = f"{present}/5"
            result["badges_checked"] = f"{checked}/5"
            if present != 5:
                errors.append("progress.md does not contain all five Week 1 badge lines")
            if checked != 5:
                notes.append("not all five Week 1 badges are checked")
    except Exception as exc:
        errors.append(f"progress.md check: {exc}")

    # ID-only check: locate the mapped source path, then extract exact strings from keys named `id`.
    quiz_source_repo_path = repo_path_from_week1(quiz_source_rel)
    quiz_poll_repo_path = repo_path_from_week1(quiz_poll_rel)
    poll_missing = quiz_poll_repo_path not in tree
    if poll_missing:
        notes.append("poll page absent; lecture must show ‘Quiz coming soon’")
    if quiz_source_repo_path not in tree:
        result["quiz_id_references"] = "coming-soon (bank absent)"
        notes.append("quiz bank absent; lecture must show ‘Quiz coming soon’")
    else:
        try:
            code, body, _ = request_bytes(raw_url(owner, repo, branch, quiz_source_repo_path))
            if code != 200:
                result["quiz_id_references"] = f"source-http-{code}"
                errors.append(f"quiz source file returned HTTP {code}")
            else:
                payload = json.loads(body)
                student_ids: set[str] = set()
                collect_ids(payload, student_ids)
                missing_ids = sorted(set(quiz_ids) - student_ids)
                if missing_ids:
                    result["quiz_id_references"] = f"missing {len(missing_ids)} ID(s)"
                    errors.append("question IDs missing from mapped source: " + ", ".join(missing_ids))
                else:
                    suffix = "; poll missing" if poll_missing else ""
                    result["quiz_id_references"] = f"{len(quiz_ids)}/{len(quiz_ids)} IDs found{suffix}"
        except Exception as exc:
            result["quiz_id_references"] = "error"
            errors.append(f"quiz ID-only check: {exc}")

    result["status"] = "ERROR" if errors else ("REVIEW" if notes else "OK")
    result["notes"] = " | ".join(errors + notes)
    return result


def re_badge_line(text: str, badge_id: str) -> tuple[str, str] | None:
    import re
    pattern = rf"^- \[([ xX])\] {re.escape(badge_id)} — (.+)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return (match.group(1), match.group(2)) if match else None


def load_quiz_map() -> tuple[str, str, list[str]]:
    mapping = json.loads((LECTURE / "week1" / "quiz-links.json").read_text(encoding="utf-8"))
    source = str(mapping["source"])
    poll = str(mapping["poll"])
    ids = [str(item) for item in mapping["ids"]]
    if len(ids) != len(set(ids)):
        raise ValueError("lecture/week1/quiz-links.json contains duplicate IDs")
    return source, poll, ids


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", required=True, type=Path, help="CSV with github_username,repo_name; optional branch,pages_url")
    parser.add_argument("--output", type=Path, default=ROOT / "deployment-status.csv")
    args = parser.parse_args()

    if not args.roster.is_file():
        parser.error(f"roster file does not exist: {args.roster}")
    try:
        roster = read_roster(args.roster)
        quiz_source, quiz_poll, quiz_ids = load_quiz_map()
    except Exception as exc:
        parser.error(str(exc))
    if not roster:
        parser.error("roster contains no student rows")

    token = get_token()
    if not token:
        print("WARNING: no GitHub token found; unauthenticated API limits may stop a 200-row run. Set GITHUB_TOKEN or run `gh auth login`.", file=sys.stderr)
    expected_tree = expected_lecture_tree()
    fields = [
        "github_username", "repo_name", "branch", "pages_url", "site_http", "lecture_hash",
        "week_indexes", "week_placeholders", "badge_lines", "badges_checked", "quiz_id_references", "status", "notes",
    ]
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    total = len(roster)
    for index, row in enumerate(roster, start=1):
        result = verify_one(row, expected_tree, quiz_source, quiz_poll, quiz_ids, token)
        rows.append(result)
        print(f"[{index}/{total}] {result['github_username']}/{result['repo_name']}: {result['status']}")
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {output_path.relative_to(ROOT) if output_path.is_relative_to(ROOT) else output_path} ({len(rows)} rows)")
    return 1 if any(row["status"] == "ERROR" for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
