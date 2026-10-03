# Pennsylvania Election Information — November 3, 2026

This repository is a nonpartisan civic-technology project for Pennsylvania election information, ballot measures, public records, source documents, accessible voter guides, and reproducible data-processing workflows.

It is built to help people find verified election information without endorsing any candidate, ballot position, or political party. The project is informational only and should not be treated as official legal, campaign, or government advice.

## Mission

- provide trustworthy, reproducible election information for Pennsylvania
- preserve public-source lineage for factual claims
- keep source materials and working research separate from published content
- support accessible, offline-friendly public information workflows
- make verification possible for journalists, researchers, and community contributors

## Repository structure

- `public/` — published site output for GitHub Pages and public-facing HTML
- `research/` — preserved source documents, PDFs, and working notes; draft notes are not final sources
- `data/` — structured facts, source metadata, and provenance records
- `tools/` — scripts for building, validating, checking links, and generating derived outputs
- `tests/` — validation and regression tests
- `.github/workflows/` — CI and deployment automation
- `docs/` — project documentation and wiki source materials when present

## Important policy: published content vs. research

This repository keeps three different layers of material:

- `public/` contains published information intended for public consumption.
- `data/` contains validated or review-ready structured facts and provenance.
- `research/` contains source PDFs, working notes, and exploratory analysis.

AI-generated research notes, drafts, and chat exports may live in `research/`, but they are not authoritative sources by default. They should be treated as leads, working notes, or unverified material until a maintainer marks them as verified.

If a fact is missing, contradictory, stale, or unverified, label it explicitly with statuses such as `unknown`, `unverified`, `conflicting`, `superseded`, or `needs_review`.

## Verification standards

For any public claim, the project prefers an explicit source trail with:

- stable source ID
- title or filename
- official URL or repository path
- retrieval or publication date
- page, section, or line reference where available
- verification status
- review timestamp

The validation suite is intended to enforce these expectations before a site or dataset is published.

## Local checks

Use the project validation scripts before merging or publishing changes:

```bash
python tools/build_site.py
python tools/finance_check.py
python validate.py
```

## Contributor expectations

Please read `CONTRIBUTING.md` before opening a pull request.

Contributors are expected to:

- remain nonpartisan and neutral
- preserve research materials instead of deleting them without clear intent
- use official government or public-source material when possible
- cite sources and verification status explicitly
- avoid publishing claims that have not been checked
- prefer small, reviewable changes

## Maintainer expectations

The repository maintainer’s role is to keep the project accurate, transparent, and reproducible. In practice that means:

- preserving source documents and research archives
- separating raw research from published site content
- validating changes before deployment
- avoiding destructive overwrites of source material
- documenting uncertainty when information is incomplete

## Project-specific references

- `.github/agents/repo-maintainer.agent.md` — maintainer rules for this repository
- `research/VERIFICATION.md` — verification notes and known caveats
- `research/README.md` — description of research materials and preservation policy
- `public/index.html` — generated public page for election deadlines and links

## Disclaimer

This project is an independent informational project and is not an official government resource. Always confirm critical dates, ballot content, polling locations, or legal requirements against current official sources before acting.
