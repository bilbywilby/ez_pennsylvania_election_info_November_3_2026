# Contributing guide

Thank you for helping improve this nonpartisan civic-technology project.

This repository is focused on Pennsylvania election information, ballot measures, source documents, public records, accessible voter guides, and reproducible data-processing workflows.

## Project principles

- remain nonpartisan and neutral
- preserve original source materials
- distinguish working research from verified public output
- prefer official sources and public records over commentary or campaign rhetoric
- label uncertainty explicitly instead of guessing

## What belongs where

- `public/` — public-facing site output, HTML, and static resources
- `research/` — source PDFs, archival materials, and working notes
- `data/` — machine-readable facts and metadata with provenance
- `tools/` — scripts used to generate or validate outputs
- `tests/` — automated checks for correctness and regressions

If you are uncertain whether a file belongs in `research/` or `public/`, default to preserving it in `research/` and ask for review before promoting it to the public site.

## Source and verification rules

Before publishing a fact or claim:

- verify the source is authoritative or publicly documented
- prefer multiple independent sources when possible
- label missing or contradictory information as `unknown`, `unverified`, `conflicting`, or `needs_review`
- preserve source lineage and review context wherever practical

Any public-facing file that makes a factual claim should be traceable to a source record containing:

- source ID or stable identifier
- title or filename
- URL or repository path
- publication or retrieval date
- page/section reference when available
- verification status
- reviewer or review timestamp

## AI-generated content policy

AI-generated notes, summaries, or analysis files are allowed as working research only when clearly labeled as drafts. They are not authoritative sources and should not be published as final factual material without human review.

When adding AI-assisted material:

- place it in `research/` or another clearly marked draft area
- mark the file or section as `draft`, `unverified`, or `needs_review`
- do not present it as official wording, legal advice, or voter guidance without review

## Pull request expectations

Keep changes focused and reviewable.

Before opening a pull request, make sure:

- the change is consistent with the repository’s nonpartisan scope
- the relevant validation script runs successfully
- no source files are deleted or overwritten without an explicit reason
- public output is updated only after checking source provenance
- any uncertainty is described clearly in the change summary

## Validation commands

Run the relevant checks before requesting review:

```bash
python tools/build_site.py
python tools/finance_check.py
python validate.py
```

## Maintainer review

Maintainers may request changes when:

- evidence is missing or weak
- a file crosses the line from research to public publication without review
- the wording could be mistaken for campaign messaging
- the content is not clearly labeled with its verification status

## Safety and repository care

- do not delete or overwrite preserved research documents without explicit project direction
- do not commit credentials, secrets, or tokens to the repository
- do not use fragile shell interpolation or unsafe deployment behavior
- use Python 3, UTF-8, type hints, and deterministic outputs where practical

## Questions

If you are unsure whether a draft note belongs in the public site or research archive, ask before publishing. For this repository, accuracy and transparency matter more than speed.
