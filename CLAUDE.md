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
  `pl-bm` (Bahasa Melayu Content file), `pl-lint` (house rules), `pl-render` (PDF, PNG, newsletter HTML),
  `pl-classify` (productivity test: Claude answers fact questions F1–F6, `classify.py` decides the labels).
- Never label initiatives (counted, Tier, Grade, Evidence type) by judgement: use `pl-classify`.
- `private/` is git-ignored: Drive copies and real gold sets live there, never in commits.
- `inbox/`, `ledger/`, `data/`, `content/en|bm/`, `output/`, `templates/`, `scripts/`, `docs/` – workflow folders.
- `site/index.html` – the live Productivity Lens · MPC website (Home, Stories, Initiative library,
  How it works, EN/BM toggle; story data is embedded in the file). `site/assets/` holds the MPC logo,
  favicon and the social preview image (`og-image.png`, 1200×630).
- Website wording rules: no internal workflow text on public pages (no Playbook versions, REDO, "full run");
  no "x of y" wording; BM page references use "hlm."; story lists are alphabetical; text at least 13px.
- `site/` is exactly what the user hosts on Cloudflare Pages – the website must always keep working.
- `requirements.txt` – Python dependencies (`python -m playwright install chromium` for rendering).

## Method documents (copied from Drive 07_Templates)
- `docs/Productivity_Lens_Playbook_v1.12.md` – the full method. Read it before any run.
- `docs/00_Project_Commands_and_Rules_v1.12.md` – commands (PREP, ANALYSE, FULL, PRODUCE, RUN …) and rules.
- `docs/Productivity_Lens_Style_Guide_v1.12.md` – wording, colours, fonts.
- `templates/*.csv` – column layouts for DataSheet, DTF, Sector Frontier, Ledger, Rules, Review.
- `scripts/pl_prepare_reports.py` – compresses/splits oversize report PDFs and writes text sidecars.
If Drive has a newer version than the repo, the Drive copy wins; update the repo copy.

## Google Drive (working data – stays in Drive, not in this public repo)
Folder "Productivity Lens" (Drive connector):
- `01_Register/` – live Ledger, Rules, Review, ImprovementLog (Google Sheet "Productivity_Lens_Templates_old.")
- `02_Reports/` – company reports (+ `_Inbox`, `_Oversize_Originals`)
- `03_Working/` – one folder per company (`[Code]_[Name]`); a second `03_Working` holds sector frontier / peer panel files
- `04_Spotlights/` – spotlight PDFs (EN/BM, `_vN` = later version), `Snapshots/`, `Newsletter/` HTML
- `05_Editions/`, `06_Distribution/`, `07_Templates/`
Spotlights are still **Draft** in the Review sheet; the website carries the user's own banner "Prototype. Draft content, not yet reviewed". Do not remove that banner or add new company content to `site/` unless the user asks.

## Cloudflare Pages status (as of 2026-11-14)
- Live site: https://productivitylens.pages.dev/ – its source is now `site/index.html` in this repo.
- The repo is **not yet connected** to that Pages project: a push to `main` produced no Cloudflare build.
- Next step: connect Git
  (production branch `main`, no build command, output directory `site`). A Direct Upload project cannot
  be switched to Git, so a new Git-connected project may be needed, with the domain moved across.
- `*.pages.dev` is not reachable with curl from cloud sessions; WebFetch works for productivitylens.pages.dev.
