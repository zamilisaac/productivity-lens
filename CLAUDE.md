# Productivity Lens – project notes for Claude

Productivity spotlights on Bursa Malaysia listed companies, built from annual and sustainability reports.
Output is in English and Bahasa Melayu.

## Working with the user
- The user writes in Bahasa Melayu (mixed with English). Reply in Bahasa Melayu.
- When the user asks you to check something, check it yourself with your tools and report the result.
  Do not ask the user to check it for you.
- This repository is **public**. Never commit internal data, the real Ledger, unapproved drafts,
  staff names or emails. Keep those in Drive/SharePoint.

## Repository layout
- `.claude/skills/` – the six Productivity Lens skills (use them, do not rewrite their logic):
  `pl-ledger` (Ledger/Rules, intake), `pl-evidence` (PageMap, quote audit), `pl-calc` (8 indicators, DTF),
  `pl-bm` (Bahasa Melayu Content file), `pl-lint` (house rules), `pl-render` (PDF, PNG, newsletter HTML),
  `pl-classify` (productivity test: Claude answers fact questions F1–F6, `classify.py` decides the labels).
- Never label initiatives (counted, Tier, Grade, Evidence type) by judgement: use `pl-classify`.
- `private/` is git-ignored: Drive copies and real gold sets live there, never in commits.
- `inbox/`, `ledger/`, `data/`, `content/en|bm/`, `output/`, `templates/`, `scripts/`, `docs/` – workflow folders.
- `site/index.html` – the live Productivity Lens website (Home, Stories, Ideas library,
  How we check, EN/BM toggle; story data is embedded in the file). Written for newcomers: short human
  headlines (`HL`) with the data headline as the deck; story order = results → what they did → what you can
  try → the numbers; plain labels (Measured result / Scale only / Described only; Core / Supporting /
  Resource move); a five-term glossary; specialist method folded at the end of "How we check". `site/assets/` holds the favicon and the social preview image (`og-image.png`, 1200×630).
- Website wording rules: no internal workflow text on public pages (no Playbook versions, REDO, "full run");
  no "x of y" wording; BM page references use "hlm."; story lists are alphabetical; text at least 13px.
- `site/` is exactly what the user hosts on Cloudflare Pages – the website must always keep working.
- Companies re-done under Playbook v1.12 are applied to the website as one data block per company, placed just
  before `function route(){` in `site/index.html`, built from the approved Content / Content_BM files
  (done: Dutch Lady 3026 Content_v6, Farm Fresh 5306 Content_v7). Stories may have 0–3 lessons (R045).
- Rendering in cloud sessions: `export PL_CHROMIUM=/opt/pw-browsers/chromium` before `pl-render` scripts.
- `scripts/requirements.txt` – Python dependencies (kept out of the repo root so Cloudflare Pages does not try to install them) (`python -m playwright install chromium` for rendering).

## Personal project, newsletter and downloads (2026-11-14)
- Productivity Lens is a **personal project**: no MPC logo, name or branding anywhere on the site or outputs.
  (`docs/` still mentions MPC in two lines; the Drive copies are the source, change them there first.)
- Reviewed stories (Review sheet status Verified) get a "Reviewed" note and EN/BM PDF downloads from
  `site/spotlights/` (`PDFS` map in `site/index.html`). Only add a PDF there after the user verifies it.
- Newsletter sign-up: Cloudflare Pages Functions in `functions/` (`/api/subscribe`, `/api/unsubscribe`) with a D1
  database bound to the Pages project as **`DB`** (table `subscribers`, created on first use). Stored: email,
  language, consent time, notice version, source. No IP. Unsubscribe deletes the row. Without the binding the API
  answers 503 `not_configured` and the form says sign-up is not open yet.
  D1 binding `DB` connected and tested live on 2026-11-14 (subscribe, re-subscribe, unsubscribe; test rows deleted).
  Bindings only reach new deployments: after changing a binding, push (or retry the deployment) before testing.
- PDPA privacy notice at `#privacy` (EN/BM). `CONTACT` in `site/index.html` is empty until the user gives a contact
  address; bump `CONSENT_VERSION` in `functions/_lib.js` and the notice date whenever the notice changes.

## Spotlight design (style A, 2026-11-14)
- `pl-render` now uses the website identity: Geist font (OFL, `assets/fonts/Geist-*.ttf`), ink #0B0B0F, lime #D4F542,
  violet #9466FF. Spotlight PDF length follows the content (3–6 pages): story, what they did + what your firm can try,
  the numbers, frontier, all moves and sources. Social cards and the newsletter email use the same palette.
- Content files may carry `short_headline` (plain human headline, EN ≤ 16 words, BM ≤ 13); the data headline becomes the deck.
  Used for Dutch Lady Content_v8 / BM_v5 and Farm Fresh Content_v9 / BM_v9.
- Plain words everywhere (site and spotlights): frontier = "benchmark" / BM "penanda aras" (never "sempadan"); peers = "similar companies" /
  "syarikat sejenis"; peer median = "typical similar company" / "biasa bagi syarikat sejenis"; firm/SME = "business" / "perniagaan (kecil)";
  analyst proxy = "our own estimate" / "anggaran kami". Specialist method notes may keep "90th percentile".
- The Style Guide v1.12 on Drive still describes Lora/Inter and teal: update it there, then copy it here.

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

## Cloudflare Pages (connected 2026-11-14)
- Live site: https://productivitylens.pages.dev/ – Cloudflare Pages project `productivitylens`, connected to this
  repo: every push to `main` deploys `site/` automatically (no build command, output directory `site`).
- Check a deploy: GitHub check run "Cloudflare Pages" on the pushed commit
  (`curl https://api.github.com/repos/zamilisaac/productivity-lens/commits/<sha>/check-runs`), then compare
  `curl https://productivitylens.pages.dev/` with `site/index.html`.
- Keep the repo root free of `requirements.txt` / `package.json`: Pages would try to install them and the build fails.
