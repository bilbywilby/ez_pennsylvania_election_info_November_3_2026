#!/usr/bin/env python3
"""Validate public JSON outputs for determinism, schema integrity, and lineage metadata.

This script enforces:
- JSON can be parsed successfully
- files are UTF-8 text
- JSON is deterministically formatted (sorted keys, stable indentation)
- any record containing a 'lineage' object includes required metadata
- statuses are restricted to known values
- public links are HTTPS
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

VALID_STATUSES = {
    "verified",
    "unverified",
    "conflicting",
    "superseded",
    "needs_review",
    "unknown",
}

REQUIRED_LINEAGE_KEYS = {
    "source_id",
    "title",
    "url",
    "publication_date",
    "verification_status",
    "last_reviewed",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate public JSON outputs for determinism and lineage metadata."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory containing public JSON files to validate",
    )
    return parser.parse_args()


def canonical_json(data: Any) -> str:
    """Return deterministically formatted JSON (sorted keys, fixed indentation)."""
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        separators=(",", ": "),
    ) + "\n"


def find_json_files(root: Path) -> Iterable[Path]:
    """Recursively find all .json files in root directory."""
    for path in sorted(root.rglob("*.json")):
        if path.is_file():
            yield path


def validate_lineage_structure(record: Any, file_path: Path) -> list[str]:
    """Validate lineage metadata if present in record."""
    errors: list[str] = []

    if not isinstance(record, dict):
        return errors

    lineage = record.get("lineage")
    if lineage is None:
        return errors

    if not isinstance(lineage, dict):
        errors.append(f"{file_path}: 'lineage' must be an object.")
        return errors

    # Check required keys
    missing = sorted(REQUIRED_LINEAGE_KEYS - set(lineage.keys()))
    if missing:
        errors.append(
            f"{file_path}: missing lineage keys: {', '.join(missing)}"
        )

    # Validate verification_status
    status = lineage.get("verification_status")
    if status is not None and status not in VALID_STATUSES:
        errors.append(
            f"{file_path}: invalid verification_status '{status}'. "
            f"Allowed values: {', '.join(sorted(VALID_STATUSES))}"
        )

    # Validate URL is HTTPS
    url = lineage.get("url")
    if url is not None and not isinstance(url, str):
        errors.append(f"{file_path}: lineage.url must be a string.")
    elif isinstance(url, str) and url and not url.startswith("https://"):
        errors.append(f"{file_path}: lineage.url must use HTTPS: {url}")

    # Validate date fields look reasonable
    for key in ("publication_date", "last_reviewed"):
        value = lineage.get(key)
        if isinstance(value, str) and value:
            # Check for ISO-8601 or YYYY-MM-DD format
            if "T" not in value and "-" not in value:
                errors.append(
                    f"{file_path}: lineage.{key} should be ISO-8601 or YYYY-MM-DD, got: {value}"
                )

    # Require notes field for uncertain statuses
    if status in {"unverified", "conflicting", "needs_review", "unknown"}:
        if "notes" not in record:
            errors.append(
                f"{file_path}: status '{status}' requires a 'notes' field explaining the uncertainty."
            )

    return errors


def validate_json_file(file_path: Path) -> list[str]:
    """Validate a single JSON file for format, encoding, and lineage metadata."""
    errors: list[str] = []

    # Check UTF-8 encoding
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{file_path}: file is not valid UTF-8.")
        return errors

    # Parse JSON
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"{file_path}: invalid JSON: {exc}")
        return errors

    # Normalize to list of records
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = [data]
    else:
        errors.append(f"{file_path}: top-level JSON value must be an object or array.")
        return errors

    # Validate lineage in each record
    for item in items:
        errors.extend(validate_lineage_structure(item, file_path))

    # Check deterministic formatting
    canonical = canonical_json(data)
    if text != canonical:
        errors.append(
            f"{file_path}: JSON is not deterministically formatted. "
            "Run: python3 -c \"import json, sys; d=json.load(sys.stdin); "
            "sys.stdout.write(json.dumps(d, sort_keys=True, indent=2, separators=(',', ': ')) + '\\n')\" < {file_path} > {file_path}.tmp && mv {file_path}.tmp {file_path}"
        )

    return errors


def main() -> int:
    args = parse_args()
    root = args.data_dir

    if not root.exists():
        print(f"ERROR: data directory '{root}' does not exist.", file=sys.stderr)
        return 1

    total_files = 0
    total_errors = 0

    for p in find_json_files(root):
        total_files += 1
        file_errors = validate_json_file(p)
        total_errors += len(file_errors)
        for err in file_errors:
            print(f"FAIL: {err}", file=sys.stderr)

    print(
        f"\nValidation complete: checked {total_files} JSON file(s) with {total_errors} error(s)."
    )
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
