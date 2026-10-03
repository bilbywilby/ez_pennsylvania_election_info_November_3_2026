# Verification notes (2026-10-03)

The `research/*.md` working notes are saved AI-assistant chat output. Treat them
as leads, not sources. This pass checked the load-bearing numbers.

## Deadlines (published on the site)
Registration Oct 19, mail-ballot application Oct 27 5:00 p.m., ballot receipt
Nov 3 8:00 p.m. (postmark not sufficient), polls 7 a.m.-8 p.m.: corroborated by
3+ sources each; see `data/election.json`. **Not corroborated:** the "4:00 PM
(paper)" registration cutoff in `voter-guide-and-ballot-questions.md`. Sources
say paper applications must be *received* by Oct 19 and online by 11:59 p.m.

## Governor finance numbers
Passed cross-source identities (`python tools/finance_check.py`):
- Shapiro: $38.32M (Jun 8) + $13.3M - $31.8M = $19.8M (residual $15K).
- Garrity: $1.12M + $1.8M - $1.58M = $1.34M vs. ~$1.3M reported.
- Shapiro $23.3M (2025) + $31.7M (2026) = $55.0M, matching the $55M reported
  since 2025; Garrity $1.49M + $3.8M = $5.29M vs. $5.3M.

Flagged: Dave White $105K vs. $100K reported; "labor ~$2M" is $1.3M by the note's
own itemization; duplicate $230K for "Bob Asher PAC"; "$36M cash" is a stale
June figure. Details in `data/finance_snapshot.json`.

## Not re-verified in this pass
PA-07 figures, State Senate/House matchups, the three Lehigh County questions,
polling-place and drop-box details. These stay out of the published page until
each has two sources and `status: "verified"`.

## Duplicates
5 byte-identical PDFs (see `MANIFEST.json`, `duplicate_of`). Nothing deleted.
