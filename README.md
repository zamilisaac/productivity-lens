# Productivity Lens

Productivity spotlights for Bursa-listed companies, built from annual and sustainability reports.

## Workflow

1. **Intake** – drop reports into `inbox/`; the Ledger records each file and its status.
2. **Prep / Extract** – build the PageMap and extract figures with quotes (no quote, no number).
3. **Analyse** – calculate the 8 core productivity indicators and Distance to Frontier (DTF).
4. **Content** – approved English Content JSON, then Bahasa Melayu (`Content_BM.json`).
5. **Produce** – render the 4-page spotlight PDF, snapshot PNGs and newsletter HTML.
6. **Lint & review** – house-rules check before anything is shared.

## Folders

| Folder | Contents |
| --- | --- |
| `inbox/` | Incoming report files (not committed) |
| `ledger/` | Ledger and Rules (one row per report file) |
| `data/datasheets/` | Company DataSheets |
| `data/pagemaps/` | PageMaps (printed page per PDF page) |
| `content/en/`, `content/bm/` | Approved Content JSON (EN and BM) |
| `output/` | Spotlights, snapshots, newsletter HTML |
| `templates/` | Render templates, fonts, Style Guide assets |
| `scripts/` | Helper scripts |
| `docs/` | Style Guide, glossary, method notes |
| `.claude/skills/` | Productivity Lens skills (scripts, templates, fonts) |

Large PDFs and rendered images are excluded by `.gitignore`; regenerate them from the Content JSON.

## Skills (`.claude/skills/`)

| Skill | Role |
| --- | --- |
| `pl-ledger` | Ledger and Rules: intake, status order, retry cap, never repeat work |
| `pl-evidence` | PageMap and quote audit (no quote, no number) |
| `pl-calc` | 8 core indicators (PROFILE) and Distance to Frontier (DTF) |
| `pl-bm` | Bahasa Melayu Content file and consistency checks |
| `pl-lint` | House-rules check before anything is shared |
| `pl-render` | Spotlight PDF, snapshot PNGs, newsletter HTML |

Claude Code loads these automatically when this repository is opened.

## Setup

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

Fonts: Lora and Inter, under the SIL Open Font License (see `.claude/skills/pl-render/assets/fonts/`).
`sample_content.json` is fictional test data.

## Website

The `site/` folder (the Productivity Lens · MPC website, `site/index.html`) is published with Cloudflare Pages (production branch `main`, no build command, output directory `site`). Every push to `main` redeploys it.
