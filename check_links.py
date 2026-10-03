"""Check that every external link in data/*.json still resolves (needs network).

Run locally or in CI on a schedule; it is deliberately not part of validate.py
so offline builds stay deterministic. Exit 1 on any non-2xx/3xx response.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = re.compile(r'https://[^\s"\']+')


def urls() -> list[str]:
    found: set[str] = set()
    for f in (ROOT / "data").glob("*.json"):
        found.update(URL.findall(f.read_text(encoding="utf-8")))
    return sorted(found)


def head(url: str) -> int:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "pa-election-linkcheck/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


if __name__ == "__main__":
    bad = 0
    for u in urls():
        code = head(u)
        ok = 200 <= code < 400
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {code or 'ERR':>3} {u}")
    sys.exit(1 if bad else 0)
