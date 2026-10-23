#!/usr/bin/env python3
"""Regenerate lecture/manifest.json with SHA-256 and Git blob hashes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "lecture"
MANIFEST = LECTURE / "manifest.json"


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    if not LECTURE.is_dir():
        raise SystemExit("lecture/ does not exist")
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
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote lecture/manifest.json ({len(records)} file hashes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
