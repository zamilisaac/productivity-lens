# Productivity Lens – project notes for Claude

Productivity spotlights on Bursa Malaysia listed companies, built from annual and sustainability reports.
Output is in English and Bahasa Melayu.

## Working with the user
- The user writes in Bahasa Melayu (mixed with English). Reply in Bahasa Melayu.
- When the user asks you to check something, check it yourself with your tools and report the result.
  Do not ask the user to check it for you.
- This repository is **public**. Never commit internal MPC data, the real Ledger, unapproved drafts,
  staff names or emails. Keep those in Drive/SharePoint.

## Repository layout
- `.claude/skills/` – the six Productivity Lens skills (use them, do not rewrite their logic):
  `pl-ledger` (Ledger/Rules, intake), `pl-evidence` (PageMap, quote audit), `pl-calc` (8 indicators, DTF),
  `pl-bm` (Bahasa Melayu Content file), `pl-lint` (house rules), `pl-render` (PDF, PNG, newsletter HTML).
- `inbox/`, `ledger/`, `data/`, `content/en|bm/`, `output/`, `templates/`, `scripts/`, `docs/` – workflow folders.
- `site/` – website published with Cloudflare Pages. `site/data/spotlights.json` lists published spotlights
  (`company`, `sector`, `fy`, `headline`, `pdf`); PDFs go in `site/spotlights/`.
- `requirements.txt` – Python dependencies (`python -m playwright install chromium` for rendering).

## Not in the repo yet
- Productivity Lens Playbook (skills refer to v1.8), Templates workbook (`Productivity_Lens_Templates.xlsx`),
  Style Guide, real company reports and Content files.

## Cloudflare Pages status (as of 2026-11-14)
- Live site: https://productivitylens.pages.dev/ – serves the existing MPC-branded "Productivity Lens · MPC"
  page (EN/BM toggle, menu). Its source is **not** in this repo.
- The repo is **not yet connected** to that Pages project: a push to `main` produced no Cloudflare build.
- Plan: add the existing site's source files into `site/` first, then connect Git
  (production branch `main`, no build command, output directory `site`). A Direct Upload project cannot
  be switched to Git, so a new Git-connected project may be needed, with the domain moved across.
- Connecting before the source is in `site/` would replace the live MPC page with the placeholder.
- `*.pages.dev` is not reachable with curl from cloud sessions; WebFetch works for productivitylens.pages.dev.
