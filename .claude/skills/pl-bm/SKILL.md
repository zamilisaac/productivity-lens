---
name: pl-bm
description: Productivity Lens Bahasa Melayu version. Guides translation of the approved English Content file into Content_BM.json in standard Bahasa Malaysia (DBP style) using the project glossary, then checks in code that every number, unit, page, quote, company name and code is identical to English, that page references use "hlm.", and that no Bahasa Indonesia words slipped in. Use this whenever running BM, PRODUCE, FULL, TEST or RUN for Productivity Lens, whenever a BM spotlight, BM snapshot card or Content_BM file is made or rebuilt (including FRONTIER_UPDATE), or whenever anyone asks for a Malay version of a spotlight.
---

# pl-bm — Bahasa Melayu version

The BM spotlight is a translation of the approved English Content file, never a re-extraction. The risk is not language quality alone: a single number changed in translation would put an unchecked figure in front of readers. So the checks are done in code.

## 1. Translate (only after the final English audit)

1. Copy `[Code]_[Name]_FY[YYYY]_Content.json` to `..._Content_BM.json`. Set `"lang": "bm"`.
2. Translate **text fields only**. Leave untouched: `value`, `unit`, `scope`, `page`, `quote`, `audit_status`, `report`, `code`, `fy`, `company`, `short_name`, `tier`, `grade`, `years`, `values`, `mode`, `key`, `source_pages`. Quotes stay in the report's own language.
3. Use `references/glossary.csv` for every key term, so all spotlights read the same.
4. Write standard Bahasa Malaysia, formal but friendly; short sentences; rewrite naturally rather than word for word. Use "syarikat", not "perusahaan"; "kakitangan", not "karyawan".
5. Keep machine, system and product names in English where the company uses English (e.g. "rotary milking parlour", "SYSPRO ERP"); add a short BM explanation in brackets the first time if needed.
6. Numbers stay as in English: RM2.70, 180,000, −3.2%. Short forms in tables and cards: RM47j (= RM47m), 239.5j L. Page references in text: "hlm.23".
7. Brand stays **Productivity Lens**.
8. `display` strings such as `"Sector median: pending"` become "Belum tersedia" where they are words; the numbers in them stay.

## 2. Check

```bash
python scripts/bm_check.py --en "<...>/Content.json" --bm "<...>/Content_BM.json" --out "<...>/[Code]_[Name]_FY[YYYY]_BM_Check.json"
python <pl-render>/scripts/word_budget.py "<...>/Content_BM.json"      # BM budgets = EN − 15%
```

- **Errors** (exit code 1) must all be fixed: structure differences, any number/page/quote/name not identical, "p." in BM text, Bahasa Indonesia words (the message gives the BM word to use), brand changed.
- **Warnings** are for review: a glossary term not used where English used the term, or text that still looks English. Rewording around a glossary term is fine when it reads more naturally; untranslated text is not.
- Over word budget: shorten the BM wording. Never cut a figure or page reference, never shrink type.

## 3. Render

Render with pl-render (`render.py spotlight` and `render.py cards` with the BM Content file). The fit check runs on BM too; BM is often 10–20% longer, so check the cards especially. No BM email: the English email links to the BM files.
