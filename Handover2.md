{
  "handover_version": "1.0",
  "generated_at": "2026-10-03",
  "agent": "Carter",
  "operator": "bilbywilby",
  "project": {
    "name": "ez_pennsylvania_election_info_November_3_2026",
    "repository_root": "/home/droid/ez_pennsylvania_election_info_November_3_2026",
    "primary_branch": "main",
    "remote": "origin"
  },
  "objective": "Process ballot-measure PDFs with spaCy, generate plain HTML output, verify rendered output, and commit the completed tooling to main.",
  "environment": {
    "platform": "Linux",
    "python": "3.13",
    "architecture": "aarch64",
    "spacy": "3.8.16",
    "pypdf2": "3.0.1",
    "w3m": "required for HTML inspection",
    "spaCy_model": "en_core_web_sm",
    "pep_668": "externally-managed-environment"
  },
  "repository_paths": {
    "input_pdfs": "research/*.pdf",
    "output_html": "processed/nlp/*_plain.html",
    "nlp_script": "scripts/analytics/nlp/ballot_measure_simplifier.py",
    "verification_script": "scripts/verify/pipeline_power.py",
    "reports_directory": "processed/reports",
    "json_manifest": "processed/reports/html_manifest.json",
    "failure_report": "processed/reports/failed_files.txt",
    "summary_report": "processed/reports/summary.txt"
  },
  "implemented_workflow": [
    "Create processed/nlp/",
    "Discover research/*.pdf with nullglob-safe logic",
    "Process PDFs with ballot_measure_simplifier.py",
    "Write one *_plain.html file per PDF",
    "Throttle batch workers to the CPU count",
    "Check output size and closing HTML markup",
    "Render previews with w3m",
    "Generate line counts and verification reports",
    "Review staged Git changes",
    "Commit changes to main",
    "Push main to origin"
  ],
  "known_fixes": [
    {
      "issue": "tac piped to head caused SIGPIPE under pipefail",
      "resolution": "Use tail -n 5 instead of tac ... | head -n 5"
    },
    {
      "issue": "Unbounded background workers caused resource contention",
      "resolution": "Throttle active workers to nproc"
    },
    {
      "issue": "Literal wildcard ran when no PDFs existed",
      "resolution": "Use nullglob and check array length"
    },
    {
      "issue": "spaCy model was unavailable",
      "resolution": "Install en_core_web_sm inside a virtual environment or use the explicitly approved system-package override"
    },
    {
      "issue": "Child Python process cannot change the parent shell directory",
      "resolution": "Use cd \"$(python3 ez_navigate.py)\""
    }
  ],
  "pending_actions": [
    "Confirm the spaCy model loads successfully",
    "Run the PDF processing pipeline",
    "Run scripts/verify/pipeline_power.py",
    "Review processed/reports/html_manifest.json",
    "Review processed/reports/failed_files.txt if present",
    "Inspect git diff and git diff --cached",
    "Commit intended changes to main",
    "Push main to origin"
  ],
  "recommended_commands": [
    "cd /home/droid/ez_pennsylvania_election_info_November_3_2026",
    "python3 -c \"import spacy; spacy.load('en_core_web_sm'); print('spaCy model OK')\"",
    "python3 -m compileall -q scripts",
    "python3 scripts/verify/pipeline_power.py",
    "git switch main",
    "git pull --ff-only origin main",
    "git status --short --branch",
    "git add -A",
    "git diff --cached --stat",
    "git commit -m \"Add PDF NLP verification and project tooling\"",
    "git push origin main"
  ],
  "git_state": {
    "target_branch": "main",
    "commit_status": "not confirmed",
    "push_status": "not confirmed",
    "required_pre_push_check": "git status --short --branch"
  },
  "handover_notes": [
    "Do not use git add -A without reviewing the staged diff if generated reports or PDFs should remain untracked.",
    "Do not force-push main.",
    "If git pull --ff-only fails, inspect branch divergence before committing or pushing.",
    "Do not use --break-system-packages unless modifying the system Python environment is intentional."
  ]
}
