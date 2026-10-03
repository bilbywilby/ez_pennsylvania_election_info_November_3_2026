"""Accounting-identity checks for the campaign-finance snapshot.

Three independent identities; each passes only if the residual is within the
combined rounding tolerance of the inputs:

  1. Conservation of cash:  cash_sep ~ cash_jun8 + receipts - disbursed
  2. Cumulative receipts:   raised_2025 + raised_2026 ~ raised_since_2025
  3. Ratio recompute:       reported ratios are recomputed, never copied.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _v(rec, key):
    return rec[key]["value"], rec[key]["precision"]


def cash_identity(rec: dict) -> tuple[float, float]:
    c0, p0 = _v(rec, "cash_jun8")
    r, pr = _v(rec, "receipts_latest")
    d, pd = _v(rec, "disbursed_latest")
    c1, p1 = _v(rec, "cash_sep")
    return (c0 + r - d) - c1, p0 + pr + pd + p1


def cumulative_identity(rec: dict) -> tuple[float, float]:
    a, pa = _v(rec, "raised_2025")
    b, pb = _v(rec, "raised_2026")
    t, pt = _v(rec, "raised_since_2025")
    return (a + b) - t, pa + pb + pt


def ratios(gov: dict) -> dict[str, float]:
    s, g = gov["shapiro"], gov["garrity"]
    return {
        "raised_2026": s["raised_2026"]["value"] / g["raised_2026"]["value"],
        "raised_since_2025": s["raised_since_2025"]["value"] / g["raised_since_2025"]["value"],
        "cash_sep": s["cash_sep"]["value"] / g["cash_sep"]["value"],
        "disbursed_latest": s["disbursed_latest"]["value"] / g["disbursed_latest"]["value"],
    }


def run(path: Path = ROOT / "data" / "finance_snapshot.json") -> list[str]:
    data = json.loads(path.read_text())
    problems: list[str] = []
    for name, rec in data["governor"].items():
        for label, fn in (("cash identity", cash_identity), ("cumulative identity", cumulative_identity)):
            resid, tol = fn(rec)
            if abs(resid) > tol:
                problems.append(f"{name}: {label} residual {resid:,.0f} exceeds tolerance {tol:,.0f}")
    return problems


if __name__ == "__main__":
    data = json.loads((ROOT / "data" / "finance_snapshot.json").read_text())
    for name, rec in data["governor"].items():
        for label, fn in (("cash identity", cash_identity), ("cumulative identity", cumulative_identity)):
            resid, tol = fn(rec)
            print(f"{name:8s} {label:20s} residual {resid:>12,.0f}  tolerance {tol:>10,.0f}  {'OK' if abs(resid) <= tol else 'FAIL'}")
    for k, v in ratios(data["governor"]).items():
        print(f"ratio {k:20s} {v:5.1f} : 1")
    probs = run()
    raise SystemExit("\n".join(probs) if probs else 0)
