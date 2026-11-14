---
name: pl-render
description: Productivity Lens renderer. Turns an approved Content JSON into the A4 spotlight PDF (3–6 pages, length follows the content), page and social-card snapshot PNGs, and the newsletter email HTML, in English or Bahasa Melayu, using fixed templates, the bundled Geist font and the website palette (ink, lime, violet), with an automatic fit check (word budgets, overflow, minimum type size, clipped chart labels). Use this whenever running PRODUCE, SPOTLIGHT, SNAPSHOT, BM, EMAIL, FULL, TEST, RUN, a FRONTIER_UPDATE re-render or audit Step 4b for Productivity Lens, or whenever a spotlight, snapshot card or newsletter email needs to be made or rebuilt. Use it instead of writing HTML or PDF code from scratch, so every company looks identical.
---

# pl-render — spotlight, snapshots and email

Everything is drawn from the approved Content file only. The templates in `assets/` are the house design; don't edit them during a company run. If the design needs to change, change the template once and re-render.

Needs `jinja2`, `pypdf` and Playwright with Chromium:
```bash
pip install jinja2 pypdf playwright --break-system-packages && python -m playwright install chromium
```

## 1. Content file first

Read `references/content_schema.md` for every field and its word budget; `assets/sample_content.json` is a complete worked example (fictional). Display strings (e.g. `"RM142,300"`, `"−3.2%"`) are written in the Content file; the renderer does no arithmetic, which is what guarantees "every number in every output appears in the Content file".

## 2. Word budgets (before rendering)

```bash
python scripts/word_budget.py "<...>/5306_FarmFresh_FY2026_Content.json"
python scripts/word_budget.py "<...>/5306_FarmFresh_FY2026_Content_BM.json"   # EN − 15%
```
Exit code 1 lists every block over budget. Cut words in the Content file (adjectives, repeated context, second examples first). Never cut a figure or page reference.

## 3. Render

```bash
# everything for one language, into the standard folders
python scripts/render.py all --content "<...>/Content.json" --root "<Productivity Lens>"

# or one part
python scripts/render.py spotlight --content C.json --out-dir "<PL>/04_Spotlights/" --png-dir "<PL>/04_Spotlights/Snapshots/"
python scripts/render.py cards     --content C.json --out-dir "<PL>/04_Spotlights/Snapshots/"
python scripts/render.py email     --content C.json --out-dir "<PL>/04_Spotlights/Newsletter/"
```

Produces, with the Playbook file names (never overwrites; adds `_v2`):
- `..._Spotlight.pdf` (3–6 pages; flexible, chapters: story, what they did + what your firm can try, the numbers, frontier, all moves and sources) and `..._Snap_01–04.png` (A4 at 200 dpi, 1654 × 2340)
- `..._Snap_05.png` headline · `06` snapshot · `07` DTF · `08–10` lessons (1080 × 1350)
- `..._Newsletter.html` (600 px, inline CSS, system fonts, website palette). BM content gives `_BM` files and no email.

## 4. Fit check (audit Step 4b)

The JSON report after each command has `fit_pass` and `fit_fails`. It checks: 3–6 pages; no page body or block overflowing; gaps between blocks; body ≥ 9.5 pt, tables ≥ 9 pt, notes and chips ≥ 8 pt; card text ≥ 28 px and not cut off; chart labels not clipped; no rank words; email subject ≤ 60 and preview ≤ 90 characters. Exit code 1 = failed.

If it fails: cut words in the Content file, re-run `word_budget.py`, render again (files get `_v2`). Maximum 2 rounds, then flag "Needs attention". Never change font sizes or spacing in the template to make content fit.

After a pass, still open page 1 and one card PNG with the `view` tool and look at them: the checks catch overflow, not awkward wording.

## 5. FRONTIER_UPDATE

Update only the `snapshot`, `dtf` and email-line fields in a `_v2` Content file from the new pl-calc output, then run `spotlight`, `cards` and `email` again. Nothing else in the Content file changes.

## Sending the email
This skill only saves the HTML. If Gmail is connected, create a draft to the user's own address with that HTML (never to anyone else); otherwise report "HTML saved, Gmail not connected".
