"""Render public/index.html from data/*.json.

Deterministic: the output depends only on the data files (no build-time clock),
so CI can rebuild and diff it. The live countdown is computed in the browser
from the ISO timestamps embedded in each row.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from electoral_calendar import deadline, election_day  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "index.html"


def load(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def fmt_day(d: date) -> str:
    return f"{d.strftime('%A, %B')} {d.day}, {d.year}"


def fmt_time(dt) -> str:
    h = dt.hour % 12 or 12
    return f"{h}:{dt.minute:02d} {'a.m.' if dt.hour < 12 else 'p.m.'} {dt.tzname()}"


def render(election: dict, resources: dict) -> str:
    e = date.fromisoformat(election["election"]["date"])
    assert e == election_day(e.year), "election date does not match the statutory rule"

    rows = []
    for d in election["deadlines"]:
        if d["status"] != "verified":  # publication gate
            continue
        dl = deadline(d["id"], e, d["rule"]["days_before_election"], d["rule"]["time"])
        src = " ".join(
            f'<a href="{escape(u)}" rel="noopener">[{i}]</a>' for i, u in enumerate(d["sources"], 1)
        )
        rows.append(
            f'<tr data-deadline="{dl.iso}">'
            f'<th scope="row">{escape(d["label"])}</th>'
            f'<td><time datetime="{dl.day.isoformat()}">{escape(fmt_day(dl.day))}</time><br>'
            f'<span class="t">{escape(fmt_time(dl.at))}</span></td>'
            f'<td class="left" aria-hidden="true"><span class="countdown">&nbsp;</span></td>'
            f'<td class="detail">{escape(d["detail"])} <span class="src">Sources: {src}</span></td></tr>'
        )
    elig = "".join(f"<li>{escape(x)}</li>" for x in election["eligibility"])
    links = "".join(
        f'<li><a href="{escape(r["url"])}" rel="noopener">{escape(r["label"])}</a>'
        f' <span class="use">&mdash; {escape(r["use"])}</span></li>'
        for r in resources["official"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="description" content="Pennsylvania November 3, 2026 general election: registration, mail ballot, and Election Day deadlines, with links to official sources.">
<title>Pennsylvania Election Deadlines | November 3, 2026</title>
<link rel="stylesheet" href="css/styles.css">
<script src="js/countdown.js" defer></script>
</head>
<body>
<header>
<h1>Pennsylvania Election: Key Deadlines</h1>
<p>General election, {escape(fmt_day(e))}. Last checked {escape(election["as_of"])}.</p>
</header>
<main>
<section aria-labelledby="dates">
<h2 id="dates">Deadlines (Eastern Time)</h2>
<div class="scroll"><table>
<thead><tr><th scope="col">Milestone</th><th scope="col">When</th><th scope="col">Time left</th><th scope="col">What it means</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>
<p class="note">{escape(election["confirm_note"])}</p>
</section>
<section aria-labelledby="who">
<h2 id="who">Who can vote</h2>
<ul>{elig}</ul>
</section>
<section aria-labelledby="official">
<h2 id="official">Official resources</h2>
<ul>{links}</ul>
</section>
<section aria-labelledby="research">
<h2 id="research">Research and method</h2>
<p>Only facts corroborated by multiple sources are published on this page; each row links its sources.
Working research lives in the
<a href="https://github.com/bilbywilby/ez_pennsylvania_election_info_November_3_2026/tree/main/research" rel="noopener">research folder</a>
and is not verified unless marked.</p>
</section>
</main>
<footer>
<p>Independent informational project. Not an official government resource.</p>
</footer>
</body>
</html>
"""


def main() -> int:
    html = render(load("election.json"), load("resources.json"))
    if "--check" in sys.argv:
        return 0 if OUT.exists() and OUT.read_text(encoding="utf-8") == html else 1
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
