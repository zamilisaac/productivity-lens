---
name: pl-lint
description: Productivity Lens house-rules check. Scans spotlight PDFs, newsletter HTML, Content JSON, editions and distribution text for rank words (top, best, leader, ranked, outperform, laggard, worst), investment language, "x of y" positions, figures that are not in the Content file, "the company discloses that", US spellings, jargon, exclamation marks, emojis and hyphens used as minus signs. Use this before showing any Productivity Lens output to the user, in PRODUCE, FULL, TEST, RUN, REVIEW (automatic checks), EDITION and DISTRIBUTE, after any re-render or FRONTIER_UPDATE, and whenever a draft newsletter, LinkedIn post or email text is written for Productivity Lens.
---

# pl-lint — house rules

One script, `scripts/lint.py`. Needs `pdfplumber` for PDFs.

Why: the no-ranking and no-investment-advice rules are the project's red lines, and "every number in every output appears in the Content file" is what makes the outputs auditable. Both are easy to break in a single word, and easy to check mechanically.

## Run

```bash
python scripts/lint.py --content "<...>/5306_FarmFresh_FY2026_Content.json" \
  "<PL>/04_Spotlights/5306_FarmFresh_FY2026_Spotlight.pdf" \
  "<PL>/04_Spotlights/Newsletter/5306_FarmFresh_FY2026_Newsletter.html" \
  "<...>/5306_FarmFresh_FY2026_Content.json" \
  --out "<...>/5306_FarmFresh_FY2026_Lint.json"
```

Also run it on the BM Content file and BM PDF (with `--content` pointing at `Content_BM.json`), on editions (`05_Editions/`) and on DISTRIBUTE text (no `--content` needed there unless figures are quoted).

## Reading the result

**Errors (exit code 1) must be fixed before the output goes to the user:**
- rank word, "x of y" position, or investment language: rewrite the sentence in the Content file, then re-render.
- "number not in Content file": the output shows a figure the Content file doesn't contain. Either it was typed into an output by hand (remove it), or it is missing from the Content file (add it there with value, page and quote, then re-run the evidence check).
- "the company discloses/reports that": describe the achievement itself.

**Warnings to fix unless there's a good reason:** US spelling (use the UK form given), jargon, exclamation marks, emojis, `-3.2%` instead of `−3.2%`, ALL CAPS sentences.

Built-in exemptions: report quotes (`quote` fields) are never linted, because they must stay verbatim; the required phrases "not a ranking" and "not investment advice" are allowed; chart axis ticks (multiples of 5 on the chart page) are not treated as figures; small whole numbers (0–10) and years are allowed.

## In the REVIEW automatic checks

Record "no ranking words" and "every number in every output appears in the Content file" as pass/fail from this report.
