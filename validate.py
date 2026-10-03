"""Repository validation gate. Exit 0 only if every check passes.

Checks: deadline arithmetic vs. published data, source provenance, HTTPS-only
links, finance identities, generated-site freshness, basic HTML accessibility.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site  # noqa: E402
import finance_check  # noqa: E402
from electoral_calendar import deadline, election_day  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def check_election(el: dict) -> list[str]:
    errs: list[str] = []
    e = date.fromisoformat(el["election"]["date"])
    if e != election_day(e.year):
        errs.append(f"election date {e} is not the statutory Election Day {election_day(e.year)}")
    ids = set()
    for d in el["deadlines"]:
        if d["id"] in ids:
            errs.append(f"duplicate deadline id {d['id']}")
        ids.add(d["id"])
        calc = deadline(d["id"], e, d["rule"]["days_before_election"], d["rule"]["time"])
        if calc.day.isoformat() != d["date"]:
            errs.append(f"{d['id']}: data says {d['date']} but rule gives {calc.day}")
        if d["status"] == "verified":
            srcs = d.get("sources", [])
            if len(set(srcs)) < 2:
                errs.append(f"{d['id']}: verified items need >= 2 distinct sources")
            for u in srcs:
                if not u.startswith("https://"):
                    errs.append(f"{d['id']}: non-HTTPS source {u}")
    return errs


def check_resources(res: dict) -> list[str]:
    return [f"non-HTTPS resource {r['url']}" for r in res["official"] if not r["url"].startswith("https://")]


def check_html(path: Path) -> list[str]:
    errs, h = [], path.read_text(encoding="utf-8")
    if not re.search(r'<html[^>]*\slang="', h):
        errs.append("missing <html lang>")
    if len(re.findall(r"<h1[\s>]", h)) != 1:
        errs.append("page must have exactly one <h1>")
    if 'name="viewport"' not in h:
        errs.append("missing viewport meta")
    if re.search(r'href="http://', h):
        errs.append("insecure http:// link")
    if re.search(r"<img(?![^>]*\balt=)", h):
        errs.append("<img> without alt")
    return errs


def main() -> int:
    el = build_site.load("election.json")
    res = build_site.load("resources.json")
    errs = check_election(el) + check_resources(res) + finance_check.run()
    html = build_site.render(el, res)
    if not build_site.OUT.exists() or build_site.OUT.read_text(encoding="utf-8") != html:
        errs.append("public/index.html is stale: run `python tools/build_site.py`")
    errs += check_html(build_site.OUT)
    for e in errs:
        print("FAIL:", e)
    print("OK" if not errs else f"{len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
