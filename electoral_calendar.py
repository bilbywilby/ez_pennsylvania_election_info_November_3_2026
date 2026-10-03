"""Deadline arithmetic for a Pennsylvania general election.

Pure functions, stdlib only. Every deadline is derived from Election Day by a
rule (days before, wall-clock time) and localized with the IANA zone, so the
EDT -> EST change (first Sunday of November) is handled by the tz database
instead of by hand.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")


def election_day(year: int) -> date:
    """Tuesday next after the first Monday in November."""
    nov1 = date(year, 11, 1)
    first_monday = nov1 + timedelta(days=(0 - nov1.weekday()) % 7)
    return first_monday + timedelta(days=1)


@dataclass(frozen=True)
class Deadline:
    id: str
    day: date
    at: datetime  # timezone-aware, America/New_York

    @property
    def iso(self) -> str:
        return self.at.isoformat()


def deadline(id_: str, election: date, days_before: int, hhmm: str) -> Deadline:
    hh, mm = (int(p) for p in hhmm.split(":"))
    day = election - timedelta(days=days_before)
    return Deadline(id_, day, datetime.combine(day, time(hh, mm), tzinfo=TZ))


def days_between(a: date, b: date) -> int:
    return (b - a).days


if __name__ == "__main__":  # quick manual check
    e = election_day(2026)
    for i, n, t in (("register", 15, "23:59"), ("mail_apply", 7, "17:00"), ("mail_return", 0, "20:00")):
        d = deadline(i, e, n, t)
        print(f"{i:12s} {d.iso}")
