# Pennsylvania Election Information

This repository contains a small public-information site for the November 3,
2026 Pennsylvania general election, alongside source documents and working
research. It is an independent project, not an official election resource.
Verify dates, ballot details, and voting procedures with official sources.

## Repository layout

- [`public/`](public/) — Static site published to GitHub Pages.
- [`docs/`](docs/) — GitHub Wiki source pages.
- [`research/`](research/) — Original source documents and research archive;
  see the [research index](research/README.md).
- [`scripts/`](scripts/) — Environment checks, setup, and deployment dispatch.
- [`.github/workflows/`](.github/workflows/) — Pages, Wiki, and CodeQL workflows.

The former long-form root README has been preserved as
[consolidated election analysis](research/consolidated-election-analysis.md).

## Local checks

Run the repository layout check:

```bash
bash scripts/verify_env.sh
```

Prepare the admin support directory and dispatch script:

```bash
bash scripts/setup_admin_panel.sh
```

To trigger a repository dispatch, install GitHub CLI (`gh`) and set `GH_TOKEN`
or `GITHUB_TOKEN` in your environment:

```bash
bash scripts/trigger_dispatch.sh both production
```

The dispatch only starts the workflow; required GitHub Pages settings and the
`WIKI_SYNC_TOKEN` secret must also be configured in the repository.

## Deployments

- Changes to `public/` deploy through `main.yml`, which calls the reusable
  Pages workflow in `static.yml`.
- `deploy-pages-wiki.yml` supports manual and repository-dispatch deployments.
- `codeql.yml` scans GitHub Actions workflow code.

## Official information

- [Pennsylvania voting and election information](https://www.pa.gov/agencies/vote.html)
- [Lehigh County Voter Registration and Elections](https://www.lehighcounty.org/Departments/Voter-Registration)
