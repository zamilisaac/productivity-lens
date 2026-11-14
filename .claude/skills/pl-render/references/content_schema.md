# Content file schema (`[Code]_[Name]_FY[YYYY]_Content.json`)

The single source of truth. The renderer prints display strings exactly as written here and does no arithmetic, so every number in every output can be traced to this file. `assets/sample_content.json` is a complete example (fictional company).

Every figure object also carries `value`, `unit`, `scope`, `page`, `quote`, `audit_status` (and `report`, e.g. `FY2024`, if it came from an older report). `pl-evidence/check_quotes.py` audits every object that has `page` and `quote`.

| Field | Used on | Notes / budget (EN words; BM = EN − 15%) |
|---|---|---|
| lang | all | `en` or `bm` |
| company, short_name, code, fy, year_end, sector | all | short_name in CamelCase, used in file names |
| source_line | footer | "Source: [Company] Annual Report FY[YYYY]" |
| headline | p1, card 05, email | ≤20 words, from a Tier 1 initiative |
| intro | p1 | ≤35 words |
| email_intro | email | 2 sentences |
| headline_results[3] | p1, card 05, email | `big`, `label` (≤6), `context` ("up from x"), `page`, `insight` (≤15) + figure fields |
| snapshot.indicators[4] | p1, card 06, email | `label`, `fy_display`, `change_display` (real minus sign −), `median_display` ("pending" or value) |
| snapshot.notes | p1 | ≤30 words (2 lines) |
| snapshot.source_pages | card 06 | e.g. "88–96" |
| initiative_line | p1 | "[n] initiatives found: [n] core · [n] supporting · [n] resource" |
| key_initiatives[≤10] | p2 | `initiative`, `what`, `result` (≤8 words each), `tier`, `grade`, `page`. Order: T1A, T1B, T2 |
| appendix_line | p2 | "All [n] initiatives are listed in the appendix." |
| strengths[2], watch[2] | p2 | ≤30 words each, operating performance only |
| dtf.mode | p3 | 1 or 2 (from pl-calc) |
| dtf.title, big_display, big_label | p3, card 07 | "Distance to Frontier" / "Five-year progress" |
| dtf.years, dtf.series | chart | series: `{name, role: company/median/index, values[]}`; max 3 lines |
| dtf.table_headers, dtf.table | p3 | rows `{indicator, cells[]}` of display strings |
| dtf.analysis | p3 | ≤70 words |
| dtf.notes | p3 | ≤35 words (2 lines) |
| dtf.email_line, card_sentence, source_pages | email, card 07 | one sentence each |
| lessons[3] | p4, cards 08–10, email | `label`, `title` (≤14), `did` (≤40), `did_short` (1 line), `sme` (≤40), `starter` (≤25), `measure` (≤20), `page` |
| notes | p4 | ≤50 words (3 lines) |
| appendix[] | p5 | every initiative not on p2: `name`, `grade`, `page`, `tier` |
| audit_status | email | "Ready for human review" or "Needs attention: …" |
| email.subject_headline, email.preview | email | ≤60 and ≤90 characters |
| links.spotlight_pdf, bm_pdf, snapshots | email | Drive links or folder paths |

The BM file has the same structure and identical numbers, pages and quotes; only text fields are translated (`pl-bm` checks this).
