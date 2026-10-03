#!/usr/bin/env python3
"""Validate election information outputs for structural integrity and source lineage."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

REQUIRED_LINEAGE_KEYS: Set[str] = {
    "source_id",
    "title",
    "url",
    "publication_date",
    "verification_status",
    "last_reviewed",
}

VALID_STATUSES: Set[str] = {
    "verified",
    "unverified",
    "conflicting",
    "superseded",
    "needs_review",
    "unknown",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify source lineage and integrity of NLP-extracted civic data."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Path to directory containing processed JSON files",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        required=False,
        help="Path to JSON schema file for validation (optional)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on first error instead of collecting all",
    )
    return parser.parse_args()


def validate_record(record: Dict[str, Any], file_path: Path, strict: bool = False) -> List[str]:
    """Validate a single record for required lineage fields and status validity."""
    errors: List[str] = []

    # Verify root fields
    if "lineage" not in record:
        errors.append(f"{file_path}: Missing mandatory 'lineage' object.")
        if strict:
            return errors

    lineage = record.get("lineage", {})
    missing_keys = REQUIRED_LINEAGE_KEYS - set(lineage.keys())
    if missing_keys:
        errors.append(
            f"{file_path}: Missing required lineage keys: {sorted(list(missing_keys))}"
        )
        if strict:
            return errors

    status = lineage.get("verification_status")
    if status not in VALID_STATUSES:
        errors.append(
            f"{file_path}: Invalid verification_status '{status}'. Must be one of {sorted(list(VALID_STATUSES))}"
        )
        if strict:
            return errors

    # Validate that unverified/conflicting/needs_review records have explanatory notes
    if status in {"unverified", "conflicting", "needs_review"}:
        if "notes" not in record:
            errors.append(
                f"{file_path}: Record with status '{status}' must include 'notes' field explaining the issue."
            )

    return errors


def process_directory(input_dir: Path, strict: bool = False) -> int:
    """Process all JSON files in directory and validate lineage."""
    if not input_dir.is_dir():
        print(
            f"Error: Target directory '{input_dir}' does not exist.",
            file=sys.stderr,
        )
        return 1

    total_files = 0
    total_errors = 0

    for json_file in sorted(input_dir.glob("**/*.json")):
        total_files += 1
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                for idx, entry in enumerate(data):
                    errors = validate_record(entry, json_file, strict)
                    total_errors += len(errors)
                    for err in errors:
                        print(f"FAIL [{json_file}#{idx}]: {err}", file=sys.stderr)
                    if errors and strict:
                        return 1
            elif isinstance(data, dict):
                errors = validate_record(data, json_file, strict)
                total_errors += len(errors)
                for err in errors:
                    print(f"FAIL [{json_file}]: {err}", file=sys.stderr)
                if errors and strict:
                    return 1

        except json.JSONDecodeError as e:
            print(
                f"FAIL: {json_file} is not valid JSON: {e}",
                file=sys.stderr,
            )
            total_errors += 1
            if strict:
                return 1
        except Exception as e:
            print(
                f"ERROR: Unable to process {json_file}: {e}",
                file=sys.stderr,
            )
            total_errors += 1
            if strict:
                return 1

    print(
        f"\nVerification complete: Processed {total_files} file(s) with {total_errors} error(s)."
    )
    return 1 if total_errors > 0 else 0


def main() -> None:
    args = parse_args()
    exit_code = process_directory(args.input_dir, strict=args.strict)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
