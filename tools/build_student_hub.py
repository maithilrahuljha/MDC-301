#!/usr/bin/env python3
"""Build a local, opt-in student-site gallery from a CSV; no server or tracking."""
from __future__ import annotations

import argparse
import csv
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "tools" / "student_hub_optin.csv"
DEFAULT_OUTPUT = ROOT / "instructor-hub" / "student-gallery.html"
USERNAME = re.compile(r"^[A-Za-z0-9-]{1,39}$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_INPUT, help="Private CSV with github_username,repo_name,display_name,opt_in")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if not args.csv.is_file():
        parser.error(f"CSV not found: {args.csv}. Copy tools/student_hub_optin.example.csv to this private path and add only opt-in rows.")

    cards: list[str] = []
    with args.csv.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"github_username", "repo_name", "display_name", "opt_in"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            parser.error("CSV headers must be github_username,repo_name,display_name,opt_in")
        for row in reader:
            if (row.get("opt_in") or "").strip().lower() not in {"yes", "y", "true", "1"}:
                continue
            username = (row.get("github_username") or "").strip()
            repo = (row.get("repo_name") or "").strip()
            if not USERNAME.fullmatch(username) or not repo or "/" in repo or ".." in repo:
                continue
            display = (row.get("display_name") or "").strip() or username
            url = (row.get("pages_url") or "").strip()
            if not url:
                suffix = "" if repo.lower() == f"{username.lower()}.github.io" else "/" + repo
                url = f"https://{username}.github.io{suffix}/"
            if not url.startswith("https://"):
                continue
            cards.append(
                '<article class="card"><h2>' + html.escape(display) + '</h2><a href="' + html.escape(url, quote=True) + '">Open public course site</a></article>'
            )

    if not cards:
        parser.error("No valid opt-in rows found; no gallery was written")
    content = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MDC-301 · Opt-in student sites</title><style>
:root{font-family:system-ui,sans-serif;color:#12243a;background:#f4f7fb}body{max-width:1100px;margin:auto;padding:2rem}h1{font-size:2rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}.card{background:white;border:1px solid #d8e0ea;border-radius:1rem;padding:1rem}a{color:#064f7c}a:focus-visible{outline:3px solid #db8121;outline-offset:3px}</style></head>
<body><main><h1>MDC-301 · opt-in student sites</h1><p>Only students who explicitly opted in are listed. Use public URLs or pseudonyms; this file is for local projection and must not be committed or published.</p><div class="grid">
""" + "\n".join(cards) + "\n</div></main></body></html>\n"
    out = args.output if args.output.is_absolute() else ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"Wrote local opt-in gallery: {shown} ({len(cards)} sites)")
    print("Do not commit or publish the opt-in CSV or generated gallery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
