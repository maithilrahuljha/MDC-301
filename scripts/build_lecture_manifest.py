#!/usr/bin/env python3
"""Regenerate or verify lecture/manifest.json with SHA-256 and Git blob hashes."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "lecture"
MANIFEST = LECTURE / "manifest.json"


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if lecture/manifest.json does not match the current lecture files",
    )
    args = parser.parse_args()

    if not LECTURE.is_dir():
        print("ERROR: lecture/ does not exist", file=sys.stderr)
        return 1

    records: dict[str, dict[str, str]] = {}
    for path in sorted(item for item in LECTURE.rglob("*") if item.is_file() and item != MANIFEST):
        relative = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        records[relative] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": git_blob_sha1(data),
        }
    payload = {
        "schema_version": 1,
        "algorithm": "sha256 plus Git blob SHA-1",
        "files": records,
        "note": "Generated from lecture/; manifest.json is excluded from its own file map.",
    }
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != rendered:
            print("ERROR: lecture/manifest.json is stale; run python scripts/build_lecture_manifest.py", file=sys.stderr)
            return 1
        print(f"lecture/manifest.json is current ({len(records)} file hashes)")
        return 0

    MANIFEST.write_text(rendered, encoding="utf-8")
    print(f"Wrote lecture/manifest.json ({len(records)} file hashes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
