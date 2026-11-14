---
name: pl-evidence
description: Productivity Lens evidence tools. Builds the PageMap (printed page number for every PDF page, plus where each report section starts) and runs the evidence audit that confirms every quote appears word for word on its cited printed page and that the number is in the quote. Use this whenever running PREP, EXTRACT, ANALYSE, FULL, TEST, RUN or self-audit Step 1 for Productivity Lens, whenever citing a page from an annual or sustainability report, when a report comes as split parts or a _text.txt file, or whenever a figure's quote or page needs checking. Use it rather than checking quotes by eye, because "no quote, no number" depends on it.
---

# pl-evidence — PageMap and quote checks

Two scripts in `scripts/`. Needs `pdfplumber` and `pandas` (`pip install pdfplumber pandas openpyxl --break-system-packages`).

Why this matters: annual reports rarely start printed numbering on PDF page 1, and split parts or text files restart counting. Citing a file position instead of the printed page is the most common evidence error. These scripts make the printed page explicit and check every quote mechanically, so the human reviewer only spot-checks.

## 1. Build the PageMap (Module 0, step 3)

```bash
python scripts/page_map.py \
  --report FY2026="<...>/5306_FarmFresh_FY2026_AR.pdf" \
  --report FY2024="<...>/5306_FarmFresh_FY2024_AR.pdf" \
  --report FY2022="<...>/FY2022_AR_part1of2_pdfp1-150.pdf,<...>/FY2022_AR_part2of2_pdfp151-290.pdf" \
  --report SR2026="<...>/5306_FarmFresh_FY2026_SR.pdf" \
  --out "<Productivity Lens>/03_Working/5306_FarmFresh/5306_FarmFresh_FY2026_PageMap.xlsx"
```

- Parts are given in order, comma-separated, and read as one report.
- A `*_text.txt` with `=== PDF page n ===` markers works too (printed pages are then guessed from the first/last lines; flag every table figure from text files).
- Output: `PageMap.xlsx` (Sections sheet with up to 3 candidate pages per section; PageNumbers sheet) and `PageMap_pages.json` (page text cache used by the checker).
- **Status column:** `seen` = number printed on that page; `inferred` = from neighbouring pages (cite as printed page but flag in the audit); `none` = cite as "PDF p.n (printed page not visible)".
- Open the top candidate for each section once and fill "Confirmed printed page". The candidates are a shortcut, not proof.
- If the summary says "Mostly no text", the report is a scanned image: mark `SKIPPED_UNREADABLE` and move on.

## 2. Use the PageMap while extracting

Go straight to the confirmed pages. When you take a figure, copy the quote exactly as printed (a short phrase that includes the number) and the printed page from the PageNumbers sheet, never the PDF position.

## 3. Evidence audit (Step 1)

```bash
python scripts/check_quotes.py \
  --pages-cache "<...>/5306_FarmFresh_FY2026_PageMap_pages.json" \
  --figures "<...>/5306_FarmFresh_FY2026_DataSheet.xlsx" \
  --default-report FY2026 --out "<...>/5306_FarmFresh_FY2026_Audit_Step1.csv"
```

Run it three times: DataSheet, Initiatives, and the Content JSON (the JSON is walked for every object with `value`/`page`/`quote`; add a `report` field such as `FY2024` to items from older reports). For the DataSheet, the `Source report` column picks the right report.

| Result | Action |
|---|---|
| Confirmed | ✅ |
| Mismatch-page | ⚠️ replace the page with "Correct printed page" |
| Mismatch-value | ⚠️ the number is not in the quote; if the detail says unit conversion, check RM'000 vs RM million |
| Not found | ❌ re-open the page; if still not there, remove the figure ("Not found in documents reviewed") |
| No quote | ❌ find a quote or remove the figure |

Text in tables sometimes extracts with odd spacing; the checker also tries a match with spaces and punctuation removed, so a genuine "Not found" usually means the quote was paraphrased. Report "Figures confirmed x of y" from the `confirmed` and `figures` counts.
