"""Non-destructive research inventory: sha256, size, and duplicate groups.

Writes research/MANIFEST.json. Never deletes or moves anything (the repo's
maintainer rules forbid removing source documents); duplicates are reported so
a human can decide.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "research"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build() -> dict:
    files = sorted(p for p in RES.iterdir() if p.is_file() and p.name != "MANIFEST.json")
    entries, first = [], {}
    for p in files:
        digest = sha256(p)
        dup = first.setdefault(digest, p.name)
        entries.append({"path": p.name, "bytes": p.stat().st_size, "sha256": digest,
                        "duplicate_of": None if dup == p.name else dup})
    dups = [e for e in entries if e["duplicate_of"]]
    return {"files": len(entries), "unique": len(entries) - len(dups),
            "redundant_bytes": sum(e["bytes"] for e in dups), "entries": entries}


if __name__ == "__main__":
    m = build()
    (RES / "MANIFEST.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
    print(f"{m['files']} files, {m['unique']} unique, {m['redundant_bytes']:,} redundant bytes")
