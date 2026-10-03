# Refactor summary

**Added:** `data/` (facts + provenance), `tools/` (calendar, builder, validator,
finance identities, research manifest, link checker), `tests/` (10 tests),
`.github/workflows/ci.yml`, `public/js/countdown.js`, `research/MANIFEST.json`,
`research/VERIFICATION.md`.

**Replaced:** `public/index.html` (now generated; adds deadlines, countdowns,
eligibility, mail-ballot rules, dark mode, mobile layout, print styles).

**Removed (unsafe or non-functional):**
- `sanitize_and_deploy.sh`: ran `git add .`, auto-committed, force-appended
  `*.pdf` to `.gitignore` (contradicting tracked research PDFs), pushed to main.
- `verify_ballot.sh`: dumped a homepage through `tac | head`, which reverses
  the text and verifies nothing. Replaced by `tools/check_links.py`.

**Changed:** `.gitignore` (root-only `*.pdf`, logs, nested clone), `static.yml`
(validates before publishing), `main.yml` (also triggers on `data/`, `tools/`),
`deploy-pages-wiki.yml` (least-privilege default token), `verify_env.sh`,
`.vscode/launch.json` (was an unusable lldb placeholder).

**Open items:** `static.yml` uses `deploy-pages@v5` while the wiki workflow uses
`@v4`; pick one after checking the latest release. No research file was deleted.
