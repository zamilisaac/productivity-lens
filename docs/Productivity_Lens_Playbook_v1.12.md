# PRODUCTIVITY LENS — PLAYBOOK v1.12

The end-to-end method. Each module is run by a command (see project instructions).

PREP → EXTRACT → PROFILE → DTF → numbers audit → CONTENT → ⏸ DECISIONS → SPOTLIGHT → final audit → SNAPSHOTS → BM → EMAIL → REVIEW → EDITION → DISTRIBUTE

└──────────────── Stage A: ANALYSE ────────────────┘   (gate)   └──────────────── Stage B: PRODUCE ────────────────┘

**Pilot scope (Phase 1):** 1–2 Bursa sectors, 20–30 companies. Phases 2 (Asia) and 3 (Global) reuse the same modules later.

**What changed in v1.12 (productivity focus):** a third productivity test question, **achieved, not planned** · a list of results that are **never operating results** (revenue, sales, profit, store or outlet counts, acquisitions, asset placements, certifications, awards, zero recalls or incidents, targets and plans) · **Tier 1 tightened**: capacity counts only when added inside existing sites; acquisitions, new markets, outlet openings and asset placements are never Tier 1 · **Grade A** needs a quantified operating change, never revenue or sales · **headline hierarchy**: Productivity result → Operating result → capacity Enabler only with the value added per employee movement beside it · a **productivity story spine** (Module 4) so the headline, intro, results and indicators tell one productivity story, falls included · **SME lessons** need Grade A with an Operating or Productivity result; Enablers are never lessons; the FY-2 and FY-4 reports are searched for initiatives when the latest report has too few · **frontier rule relaxed**: a company's own value added per employee may be shown on its own page even when it is at or beyond the frontier.

**Earlier (v1.11):** Distance to Frontier now has one headline measure, **frontier attainment** (value added per employee as a % of the sector frontier), with a one-line verdict · the five-indicator composite score and the 10th-percentile floor are removed; the other four indicators become a "Behind the gap" diagnostic table · the frontier is labelled "Selected listed-company peer frontier" and every DTF output prints its panel size and frontier vintage · the DTF window rolls with the latest financial year instead of being fixed at FY2022–FY2026 · DTF is described as "inspired by" OECD frontier research, never as the OECD method · every initiative gets an Evidence type (Enabler / Operating result / Productivity result) · every spotlight page carries a page strip and a one-line takeaway so the reader can follow the story from page to page. Value-added formula, Tiers, Grades, the 5-company threshold and Bursa-sector peer groups are unchanged.

**Earlier (v1.10):** every initiative must pass a two-question productivity test (Module 2A) · Tier 3 is counted only with a quantified cost or input saving · initiatives that fail go to a "Not counted" list instead of the inventory · the audit re-checks anything cited from the sustainability pages.

**Earlier (v1.9):** results are worded as reported (a capacity increase is not a productivity increase) · assets under construction are recorded and used in a fixed-asset sensitivity check · the Content file carries the working for every indicator, so the website can show the calculation and the evidence · a Deferred list records ideas reviewed but not adopted. Formulas, Tiers, Grades and DTF scoring are unchanged.

**Earlier (v1.8):** Distance to Frontier (Module 3B) using FY2022–FY2026 · three reports per company (FY, FY-2, FY-4) · spotlight now 4 pages + appendix, with word budgets and a fit check so pages are never crowded · 10 snapshots.

**Earlier (v1.7):** runs in Cowork with Google Drive for Desktop · two stages with a decision gate · one Content file feeds every output · Rules tab · chat mode saves after every module.

-----

## GLOBAL RULES (apply to every module)

  - **No quote, no number.** Every figure carries a short verbatim quote and the **printed** page number.
  - Use figures as reported. Do not estimate. If missing, write "Not found in documents reviewed".
  - All arithmetic in code (Python). Never calculate mentally.
  - Record the **scope** of every figure: Group, Malaysia, segment, plant or product line.
  - Productivity = getting more output from **people, machines, processes and capacity**. This is not a financial, valuation, investment or sustainability review.
  - No rankings or league tables. Companies in tables are listed alphabetically.
  - Plain UK English. Inspiring but honest. Caveats go in notes, not headlines.

-----

## WHERE IT RUNS AND HOW OUTPUTS ARE SAVED

### Primary: Cowork + Google Drive for Desktop

  - The Productivity Lens Drive folder is synced to the computer. Claude reads and writes **local files in that folder**. Google Drive for Desktop uploads them; no connector upload is used.
  - **Find the folder once per session:** look for Productivity Lens under the Google Drive mount (Windows: usually G:\\My Drive\\; Mac: \~/Library/CloudStorage/GoogleDrive-\*/My Drive/). Store the path in the session and confirm it in the "before every run" message.
  - **Create missing sub-folders** (e.g. 03\_Working/5306\_FarmFresh/) before saving. Never create a second Productivity Lens folder.
  - **Write, then check.** After saving each file, confirm it exists and is larger than 0 bytes. Count files saved vs files expected and report both in the completion message.
  - **Do not wait for sync.** Drive for Desktop syncs in the background. If the Drive app is paused or offline, the files are still safe locally and sync later; note "sync pending" if you can tell.
  - **Large reports are read locally**, so the 10 MB download limit does not apply. PREP still makes text files and page maps because they make extraction faster.
  - **Google Sheets (Ledger, Rules, Review):** update them through the Google Sheets connector. If the connector is not available, write the changes to 01\_Register/\_ledger\_pending.csv and apply them at the start of the next run where it is available. Report "Ledger: pending sync" in the completion message.

### Fallback: normal claude.ai chat

Files made in a normal chat can only reach Drive by being typed into the connector, so only small files are practical.

  - **Save through the Drive connector:** text and data files under about 200 KB (DataSheet, Initiatives, Profile, PageMap, Content, Decisions, Audit, Review, newsletter HTML). Spreadsheets can be uploaded as CSV and converted to Google Sheets.
  - **Do not attempt** PDFs, PNGs or any file over about 200 KB. Attach them in the chat and record Saved: chat only in the Ledger, so I know what to move.
  - Treat a save as done only when the connector returns a file ID.

### Chat mode: split the work and save as you go

A normal chat has a tool limit and cannot finish a FULL run. When the local folder cannot be found:

  - **Switch to chat mode automatically** and say so in the before-run message.
  - **FULL or TEST in chat mode = Stage A only.** Run PREP checks, EXTRACT, PROFILE, audit Steps 1–3, Content file and Decisions, then stop and tell me: "Start a new chat and type PRODUCE \[code\]."
  - **Save a checkpoint after every module**, before starting the next one: upload that module's file (CSV or text, under 200 KB) to 03\_Working/\[Code\_Name\]/ with the Drive connector and update the Ledger. A cut-off run then loses at most one module.
  - **Unreadable pages:** if the connector text is cut off, list the printed pages that could not be read, mark affected items "Not found in documents reviewed", and add "run PREP in Cowork" as the fix. Do not guess the missing pages.
  - **Gmail is optional.** If it is not connected, save the newsletter HTML and write "Newsletter email: HTML saved, Gmail not connected" on the email line. This is not a failure.

### Never

  - Never say a file is saved without checking.
  - Never overwrite; add \_v2, \_v3.
  - Never put subscriber data in this folder.

-----

## TWO STAGES AND THE DECISION GATE

The human review bottleneck is judgement calls, not quote-checking. If a judgement changes after rendering (e.g. headcount), every PDF and PNG has to be rebuilt. So judgements are settled **before** anything is rendered.

### Stage A — ANALYSE

PREP → EXTRACT → PROFILE → DTF → audit Steps 1–3 (evidence, calculation, completeness) → write the **Content file** → list **decisions**.

### The Content file (single source of truth)

03\_Working/\[Code\_Name\]/\[Code\]\_\[Name\]\_FY\[YYYY\]\_Content.json holds everything that appears in any output: headline · intro · 3 headline results (each with a one-line insight) · 4 snapshot indicators (FY, change, median) · initiative counts · top-10 initiative table · full initiative list (appendix) · page takeaways (one line each for pages 2–4) · DTF (mode, verdict, frontier value, attainment by year, gap in RM, panel size, frontier vintage, diagnostics, gap pointers, analysis, lesson pointer) · strengths and areas to watch · up to 3 SME lessons (qualifying only) · notes · source line. Every figure in it carries value, unit, scope, page, quote, audit\_status. Every calculated indicator also carries its **working**: the formula, each component (value, year, scope, page, quote) and the result, for every year shown. The website uses this for "View calculation" and "View evidence", so no figure is shown without its components and source page. **Rule:** the spotlight, snapshots, BM version and email are rendered from this file only. Nothing is written into an output that is not in the Content file.

### Decisions

Any judgement call that could change a number, a headline or a lesson becomes a **decision**, saved as \[Code\]\_\[Name\]\_FY\[YYYY\]\_Decisions.md and added to the Ledger. Typical triggers: headcount definition (permanent vs contract, year-end vs average, Group vs Malaysia); two conflicting figures for the same item; scope mismatches; a figure that changed by more than 50%; a restated prior year; an initiative whose Tier is unclear.

**Each decision is written as:**

Q1 Headcount — affects all per-employee ratios

   (A) 1,669 incl. 403 contract staff (p.189, p.176)  ✓ recommended – matches reported total

   (B) 1,266 permanent staff only

  - Always give a recommended answer and why in one line.
  - **Check the Rules tab first.** If a rule already covers the case, apply it, note the rule ID, and do **not** ask.

### The gate

  - **No open decisions** (none found, or all covered by Rules) → continue to Stage B automatically.
  - **Open decisions** → stop this company at AWAITING\_DECISIONS, give the ⏸️ completion message, and move on to the next company in the queue. Never wait.
  - **How I answer** (either works):

      - In chat: APPROVE 5306 (accept all recommendations) or APPROVE 5306 Q1=B Q2=A.
      - On my phone: type A, B or OK (= recommended) in the Ledger **Decisions** column. The next RUN reads it.
  - After approval: apply the answers to the DataSheet, Profile and Content file (as \_v2 if they change), re-run audit Steps 1–2 on the changed figures, then Stage B.
  - **Every answer becomes a rule** in the Rules tab (see below) unless I mark it "this company only".

### Stage B — PRODUCE

SPOTLIGHT (render) → audit Steps 4–6 (scorecard, fix, audit report) → SNAPSHOTS → BM → EMAIL. All rendered from the approved Content file using the HTML templates in 07\_Templates/. If the templates do not exist yet, create them on the first run following the Style Guide, save them there, and reuse them for every company so all reports look identical.

### The Rules tab

Sheet **Rules** in Productivity\_Lens\_Templates: Rule ID | Situation | Rule | Example (company, page) | Date | Source (decision / review). Examples of the kind of rule this builds up:

  - "Headcount: use the reported total including contract staff; state the split in notes."
  - "Where narrative text and a table disagree, use the table and note the narrative figure." Read the Rules tab at the start of every run. Rules outrank the defaults in this Playbook where they conflict; flag any such conflict in the audit.

-----

## FILE INTAKE, LEDGER AND ERROR HANDLING — NEVER HALT, NEVER REPEAT

The run must **never stop or wait** because of one problem file or one open question, and must **never redo work that is already done**.

### The Ledger (the project's memory)

Sheet **Ledger** in Productivity\_Lens\_Templates (01\_Register/). One row per report file. Chat memory is not used for this; the Ledger is the source of truth.

**Columns:** Drive file ID / local path | File name | Company | Code | FY | Doc type (AR / SR / AR part) | Size MB | MD5 | Intake status | Pipeline status | Last module done | Open decisions | **Decisions** (my answers) | Rules applied | Output files | Saved to | Playbook version | Attempts | Date updated | Notes

**Intake status:** READY · PREPARED (split, compressed or text file used) · SKIPPED\_TOO\_LARGE · SKIPPED\_UNREADABLE · SKIPPED\_NOT\_REPORT · DUPLICATE

**Pipeline status:** NEW → EXTRACTED → PROFILED → CONTENT → AWAITING\_DECISIONS → APPROVED → SPOTLIGHT → AUDITED → SNAPSHOTS → BM → EMAILED = COMPLETE → VERIFIED → PUBLISHED Special: FAILED · PARKED (failed twice, needs me) · FRONTIER\_UPDATE (sector frontier or median changed; re-render DTF page, DTF card and snapshot box only, with the new frontier vintage; never applied to PUBLISHED rows)

**Rules**

1.  **Check the Ledger before opening any report.** Use file details only (path or ID, name, size, MD5).
2.  A file is **already done** if its ID, path or MD5 is in the Ledger at COMPLETE or later, or a spotlight for the same Code + FY exists in 04\_Spotlights/. Skip it and list it under "Already done". If the spotlight exists but the Ledger has no row, add the row (backfill).
3.  A SKIPPED\_\* file with the **same MD5** is not retried. Retry only if the file changed or prepared parts / a text file have appeared next to it.
4.  **Resume, don't restart.** Start at the module after "Last module done", reading saved files from 03\_Working/.
5.  **Update the Ledger after every module.**
6.  Only REDO \[company\] reprocesses a COMPLETE company. Outputs then get \_v2, \_v3.
7.  One job = one company and its latest FY: the FY, FY-2 and FY-4 annual reports (for DTF) plus the latest sustainability report. The older reports are used for the DTF data and, where the latest report has fewer than three initiatives with a Grade A Operating or Productivity result, for initiatives and lessons too (Module 2A, "Earlier reports"). **The sustainability report is optional:** if it is missing, unreadable or too large, finish from the annual report and note the gap. **Older reports are optional too:** if FY-2 or FY-4 is missing, run DTF on the years available (minimum 3 years for a trend) and list the missing report in the summary.
8.  **Retry cap:** on failure set FAILED and add 1 to Attempts. After 2 failed attempts set PARKED – needs you with the reason, and stop retrying it.
9.  Record the Playbook version used on each row. QUEUE lists COMPLETE reports made under an older version, so I can choose to REDO them.

### Large files (over 10 MB)

  - **In Cowork:** read the file locally. No size limit applies. Do not skip for size.
  - **In a normal chat** (target 9.5 MB per file), use the first that works:

    1.  Prepared versions next to the report: \*\_partNofM\_pdfpX-Y.pdf and/or \*\_text.txt. Read all parts as **one report**. Intake = PREPARED.
    2.  The Drive connector's text read (read\_file\_content), once. Use it only if the text includes the financial statements and notes (search "statement of cash flows" and "property, plant and equipment"). Note Source: Drive text extract.
    3.  Nothing works → **ignore the file**: ⚠️ SKIPPED: \[file\] – over 10 MB, no cut version, Intake SKIPPED\_TOO\_LARGE, carry on. Fix: "run PREP in Cowork".

**Page numbers with parts or text files:** pdfpX-Y and === PDF page n === are **file positions, not printed page numbers**. Always cite the **printed** page. If it cannot be seen, write "PDF p.n (printed page not visible)" and flag it.

**Text file limits:** text files lose table layout. Take table figures from the PDF where possible. If only text is available, flag every table figure in the audit.

### Other files to skip

  - password-protected, corrupted or cannot be opened → SKIPPED\_UNREADABLE
  - scanned image with no readable text → SKIPPED\_UNREADABLE
  - not an annual or sustainability report (e.g. a circular or brochure) → SKIPPED\_NOT\_REPORT
  - same MD5 as a file already in the Ledger → DUPLICATE

**When a file is skipped:** mark ⚠️ SKIPPED: \[file name\] – \[reason\], update the Ledger, **continue immediately**, and list it in the final summary with a suggested fix.

**If one part of a report fails:** carry on, mark affected items "Not found in documents reviewed", note it in the audit.

**If a module fails** (e.g. snapshots, BM or email): finish all other modules, keep Pipeline status at the last module that succeeded, and report ⚠️ \[module\] FAILED – \[reason\] on that module's line of the completion message. Never leave the line out.

### Batch runs (RUN and scheduled runs)

Never pause for confirmation. Order of work:

1.  Read Ledger, Rules and ImprovementLog; apply any pending Ledger changes from \_ledger\_pending.csv.
2.  **PREP** the inbox and any new reports.
3.  **Approved companies first:** any row where I have filled the Decisions column → apply answers → Stage B.
4.  **Part-done companies** → resume.
5.  **FRONTIER\_UPDATE** **companies** → re-render the DTF page, snapshot box, cards 06–07 and the email DTF line only (as \_v2, printed with the new frontier vintage). PUBLISHED companies are skipped: their outputs keep the vintage they were published with.
6.  **New companies** → Stage A (and Stage B if no open decisions).

**Limit:** at most **2 Stage A runs** per chat (Stage B runs are lighter; up to 4). Leave the rest in the queue.

### Batch summary (end of every RUN or scheduled run)

📋 BATCH SUMMARY \[date\]

\- Completed: \[n\] → \[Code Name FY, …\]

\- ⏸️ Awaiting your decisions: \[n\] → \[Code: Q1 … (recommended A) …\]

\- Resumed: \[n\] · Frontier updates: \[n\]

\- Already done (not reopened): \[n\]

\- ⚠️ Skipped / failed / parked: \[n\] → \[file – reason – fix\]

\- Files saved: \[x of y\] checked present · Not saved: \[list or none\]

\- Still in queue: \[n\]

If the Gmail connector is available, also send this summary to me as **one digest email draft** with links to each finished spotlight (instead of separate emails per company, when there is more than one).

-----

# MODULE 0 — PREP (PREP; runs automatically at the start of every ANALYSE, FULL and RUN)

**Goal:** every report filed, readable and mapped before extraction starts.

1.  **File the inbox.** For each file in 02\_Reports/\_Inbox/: read the first few pages to identify company, Bursa code, FY and document type (AR / SR). Rename to \[Code\]\_\[ShortName\]\_FY\[YYYY\]\_AR.pdf (or \_SR). **FY = the financial year the report covers** (check the cover or the financial statements), not the year it was published and move to 02\_Reports/\[Sector\]/\[Code\_Name\]/FY\[YYYY\]/. If it cannot be identified, leave it in the inbox and list it in the summary. Add a Ledger row (NEW).
2.  **Prepare large files.** In Cowork, run pl\_prepare\_reports.py on 02\_Reports/ (it makes text files, and splits or compresses anything over 9.5 MB for use in normal chats). If Python packages are missing, install them (pip install pypdf pdfplumber). If the script is missing, skip this step and note it.
3.  **Build the page map** 03\_Working/\[Code\_Name\]/\[Code\]\_\[Name\]\_FY\[YYYY\]\_PageMap: the **printed** page (and PDF page) of: contents page, Chairman's statement, MD\&A, operations / segment reviews, income statement, balance sheet, cash flow statement, segment note, PPE note, staff costs / employee benefits note, five-year summary, sustainability statement, employee numbers. Mark any not found.

-----

# MODULE 1 — SOURCE (SOURCE \[sector\])

**Goal:** a pilot list of companies and a clean file plan.

1.  Use web search to list Main Market companies in the requested Bursa sector (or sub-sector). Show: company, Bursa code, sub-sector, latest financial year end, investor-relations page link.
2.  Suggest **20–30 pilot companies**, preferring:

      - manufacturing, distribution or other operating businesses (avoid pure investment holding)
      - a mix of sizes, so mid-tier readers see firms closer to their scale
      - companies whose latest annual report is available
3.  Mark each as **Selected / Reserve**, with a one-line reason.
4.  Output as a table I can paste into the **Register** sheet of the templates workbook. Also add one **Ledger** row per Selected company (Pipeline status NEW), so QUEUE and RUN can pick them up.
5.  Create any missing folders below (Cowork) or remind me of the plan (chat):

Productivity Lens/                      (synced to the computer by Google Drive for Desktop)

├── 01\_Register/          Templates workbook: Register, Ledger, Rules, ImprovementLog, Review

├── 02\_Reports/

│   ├── \_Inbox/           drop new downloads here, any file name

│   ├── \_Oversize\_Originals/   originals over 10 MB, moved by the PDF cutter

│   ├── \_prep\_log.csv     PDF cutter log

│   └── \[Sector\]/\[Code\_Name\]/FY\[YYYY\]/   AR + SR (PDF, parts, \_text.txt)

├── 03\_Working/\[Code\_Name\]/   DataSheet, Initiatives, Profile, DTF, PageMap, Content, Decisions, Audit, Review

├── 03\_Working/\_Sector/   \[Sector\]\_Frontier.xlsx (sector panel, frontier, medians, Vintages log)

├── 04\_Spotlights/        spotlight PDFs (EN + BM)

│   ├── Snapshots/        PNGs

│   └── Newsletter/       newsletter HTML

├── 05\_Editions/          newsletter issues

├── 06\_Distribution/      email text (no personal data)

└── 07\_Templates/         HTML render templates + pl\_prepare\_reports.py

**Reports needed per company:** annual reports for **FY, FY-2 and FY-4** (e.g. FY2026, FY2024, FY2022). Each report also shows the previous year, so these three cover FY2021–FY2026. Plus the latest sustainability report if separate. Go by the financial year covered, not the publication year.

**Tip:** save downloads straight into 02\_Reports/\_Inbox/; PREP files and renames them. If Bursa lists the report in parts, download all parts.

**Note:** I download the PDFs myself from the company IR page or Bursa announcements. Verify every company detail from web search before use.

-----

# MODULE 2 — EXTRACT (EXTRACT \[company\])

**Input:** annual / integrated report + sustainability report (if separate). **Output:** (a) Initiative Inventory, (b) Raw Data Sheet. Both as Excel files using the template columns, saved to 03\_Working/\[Code\_Name\]/. **Decision triggers:** while extracting, note every judgement call (headcount definition, conflicting figures, scope, restatements, unclear Tier, an initiative that is borderline on the productivity test). Apply the Rules tab where it covers the case; list the rest for the Decisions file.

**Start from the PageMap** (Module 0) to go straight to the right sections. If the report came in parts or as a text file, read all parts as one document. Read both documents in full: Chairman's statement, MD\&A, operations and segment reviews, case studies, financial statements and notes (incl. segment note, PPE note, staff costs note), five-year summary and sustainability statement.

## 2A. Initiative Inventory

List **every** productivity initiative. Then **re-scan the whole report** once more for missed ones.

**Exclude:** CSR, donations, branding/marketing campaigns, governance, pure sustainability reporting, acquisitions and disposals, new market or country entry, pricing and product launches, HR benefits (pay reviews, allowances, retention perks, wellbeing, flexible hours).

**Productivity test — every initiative must pass all three questions**

1.  **Input link:** does it raise output, or cut the input used per unit of output? Inputs are people, machine time, materials, energy, water, space and stock.
2.  **Operating result:** is the reported result (or, where no result is given, the stated purpose) in operating terms: units, hours, RM cost, yield, downtime, lead time or headcount? A result stated only in environmental or social terms (tCO2e, % renewable energy, certification, awards, community benefit) fails.
3.  **Achieved, not planned:** has the result already happened in the period the report covers? Targets, expected capacity, plants or systems still under construction and "will" or "plans to" statements fail. Record them in "Not counted" with the reason "planned, not yet achieved".

**Never an operating result on their own** (an initiative whose only result is one of these fails question 2): revenue, sales, profit or margin growth · market share · number of stores, outlets, customers, dealers or countries · size of an acquisition (lines, trucks, sites bought) · assets placed in the market (freezers, coolers, vending machines) · herd or plantation size · certifications and audits passed · awards · "zero recalls", "zero incidents" or other safety or compliance records · training hours.

<!-- end list -->

  - **Tier 3 is stricter:** count it only where a cost or input saving is quantified (e.g. "RM1.2 million saved", "kWh per litre fell from x to y"). A Tier 3 item with no such figure fails.
  - **Quality items:** pass only with a measured defect, reject, rework, yield, complaint or downtime figure per unit or per period. Certification or a clean recall record alone fails.
  - **Distribution items:** pass only with an operating measure such as cost per delivery, drops per route, delivery lead time or sales per outlet or per agent. Opening outlets or placing assets in the market is scale, not productivity.
  - **Workforce items:** upskilling and multi-skilling used in operations pass. General training hours, pay, benefits, diversity and safety programmes fail, unless the report gives an operating result such as downtime avoided.
  - **Found only in the sustainability pages:** an initiative cited only from the sustainability statement or sustainability report (check the PageMap) passes only if its quote contains an operating measure.
  - **Borderline:** apply the Rules tab; otherwise raise a decision with a recommended answer.

|  |  |
| :-: | :-: |
| \*\*Example\*\* | \*\*Result\*\* |
| Solar panels, reported as "tCO2e avoided" | Fails |
| Water recycling, reported with RM or volume saved per unit | Passes (Tier 3) |
| Lighter packaging, reported as "plastic reduced" only | Fails |
| Lighter packaging, reported with material cost saved | Passes (Tier 3) |
| General training hours per employee | Fails |
| Operators trained to run two lines | Passes (Tier 1) |
| New plant revenue rose from RM14.3m to RM31.9m | Fails (revenue only) |
| New hub expected to make 1 million pieces a day | Fails (planned, not achieved) |
| Acquired a firm with 5 lines and 25 trucks | Fails (acquisition) |
| 11,000 freezers placed with retailers | Fails (asset placement, scale only) |
| Zero product recalls; ISO 22000 certified | Fails (compliance record) |
| Agents cut from 971 to 252 with lower distribution cost stated in RM | Passes (Tier 1) |
| Drive-in racking raised rack utilisation by 13% | Passes (Tier 1) |

**Initiatives that fail are recorded, not dropped.** List them on a second sheet of the Initiatives file, **"Not counted"**: Initiative | Why it fails | Page | Quote. They are left out of every count, the page-2 table, the appendix and the lessons. All counts in every output include only initiatives that pass.

**Earlier reports.** If the latest report gives fewer than three initiatives that pass with a Grade A Operating or Productivity result, read the FY-2 report, then the FY-4 report, for initiatives with such results. Add each to the inventory with its source report (e.g. "p.27 (FY2024 AR)") and the year of the result. They count like any other initiative, and every output names the year of the result.

**Tier (productivity relevance)**

|  |  |
| :-: | :-: |
| \*\*Tier\*\* | \*\*Covers\*\* |
| \*\*1 Core\*\* | machinery and production lines; automation, digital, AI; process redesign, lean, layout; capacity added inside existing sites (new or faster lines, extra shifts, debottlenecking); facility consolidation; workforce upskilling, multi-skilling, reducing reliance on low-cost/foreign labour; distribution, dealer or fleet restructuring with an operating measure; yield, quality and rework with a measured rate. **Never Tier 1:** acquisitions, new sites or countries, outlet openings, asset placements |
| \*\*2 Supporting\*\* | supply chain, sourcing, logistics, localising production, resilience measures, new plants and sites (only once operating, with an operating result) |
| \*\*3 Resource\*\* | water, waste, effluent, energy, material substitution; counted only with a quantified cost or input saving |

**Grade (evidence)**

|  |  |
| :-: | :-: |
| \*\*Grade\*\* | \*\*Meaning\*\* |
| \*\*A\*\* | Quantified operating change or impact stated by the company (before→after \*\*or\*\* a single stated impact, e.g. "70,000 → 180,000 pcs/day", "141,000 L diesel avoided"). Revenue, sales or any item on the "never an operating result" list is never Grade A |
| \*\*B\*\* | Quantified scale of the investment only, no operating change (e.g. "12 robotic palletisers installed") |
| \*\*C\*\* | Described, not quantified |

**Evidence type (what the report actually shows)** — a separate label. It does not change the Tier or the Grade.

| Evidence type | Meaning | Example |
| :-: | :-: | :-: |
| **Enabler** | An investment or action was made: machine, line, system, training, capacity. No measured operating change is reported. | "Installed a new automated line"; "capacity rose by 50%" |
| **Operating result** | A measured change in time, cost, defects, downtime or input used per unit. | "Machine downtime fell by 20%" |
| **Productivity result** | A measured change in output or value added per worker, per machine hour or per another stated input. | "Output per worker rose by 15%" |

  - Pick the **highest type the quote supports**. A capacity or scale figure alone is an Enabler, even at Grade A.
  - An Enabler is described as what the company invested in or put in place; it is never written up as a productivity gain.

**Initiative type** (pick one, for cross-company comparison): New/upgraded line · Automation/digital · Process redesign · Capacity expansion · Facility consolidation · Workforce/skills · Distribution/channel · Supply chain · Quality/yield · Resource substitution · Other.

**Columns:** Company | Code | Sector | FY | Initiative | Type | Tier | Grade | Evidence type | Where | What they did | Investment | Reported result | Page | Quote

If a reported figure **fell**, record it accurately; never present it as an achievement.

**Say what was reported, nothing more.** Describe each result as the kind of change the company reported: capacity, output, cost, time, yield or headcount. A capacity increase is written as "capacity rose", never "productivity rose". Write that productivity rose or improved only where the report itself says so, with the quote. This rule does not change the Grade: a quantified capacity change is still Grade A.

## 2B. Raw Data Sheet

Extract these items for **every year FY-5 to FY** (e.g. FY2021–FY2026):

  - From the **FY report**: FY and FY-1.
  - From the **FY-2 report**: FY-2 and FY-3.
  - From the **FY-4 report**: FY-4 and FY-5 (FY-5 is needed only for opening balances).
  - Where a later report restates a year, use the later (restated) figure and note "restated".
  - If a comparative is missing (often headcount), list exactly which extra report is needed (e.g. "FY2023 AR – headcount only") and carry on.

Items:

|  |  |
| :-: | :-: |
| \*\*Item\*\* | \*\*Usual location\*\* |
| Revenue | Income statement |
| Cost of sales | Income statement |
| Profit before tax (PBT) | Income statement |
| Staff costs / employee benefits expense | Notes |
| Depreciation and amortisation | Notes / cash flow |
| Finance costs | Income statement |
| Net property, plant and equipment (PPE) | Balance sheet |
| Assets under construction / capital work-in-progress (net carrying amount, part of net PPE) | PPE note |
| Purchase of PPE (capex) | Cash flow statement |
| Inventories | Balance sheet |
| Number of employees (state: year-end or average; Group or Malaysia) | Sustainability statement / notes |
| Malaysia segment revenue, PBT, assets (if headcount is Malaysia-only) | Segment note |
| Up to 2 sector physical measures (e.g. tonnes, litres, units, outlets, vehicles) | Operations review |

**Columns:** Company | Code | FY | Item | Value (RM'000 or unit) | Year | Scope | Source report (FY of the report) | Page | Quote | Restated (Y/N)

-----

# MODULE 3 — PROFILE (PROFILE \[company\])

**Input:** the Raw Data Sheet from Module 2. **Output:** Profile table (Excel) with 8 core indicators; sector median when available.

## The 8 core indicators

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*\\\#\*\* | \*\*Indicator\*\* | \*\*Formula\*\* | \*\*What it tells an SME\*\* |
| 1 | Revenue per employee | Revenue ÷ avg employees | Sales generated per worker |
| 2 | Value added per employee | Value added ÷ avg employees | Wealth created per worker |
| 3 | Value added per RM1 staff cost | Value added ÷ staff costs | Return on every ringgit of wages |
| 4 | Average staff cost per employee | Staff costs ÷ avg employees | Wage level, investment in people |
| 5 | Capex per employee | Purchase of PPE ÷ avg employees | Investment in machines per worker |
| 6 | Capital intensity | Avg net PPE ÷ avg employees | How well equipped each worker is |
| 7 | Value added per RM1 fixed assets | Value added ÷ avg net PPE | Output from machines and buildings |
| 8 | Inventory turnover | Cost of sales ÷ avg inventory | How fast stock moves |

**Value added** = PBT + staff costs + depreciation & amortisation + finance costs. Label it "analyst-calculated nominal proxy".

**Calculation rules**

1.  Use averages (opening + closing ÷ 2). If an opening figure is missing, show that year as "n.c." rather than mixing methods.
2.  Check the value-added components add up, for every year.
3.  **Scope match:** if headcount is Malaysia-only, use Malaysia segment figures for per-employee ratios and label them "Malaysia operations". If no match is possible, mark "Scope mismatch" and leave blank.
4.  Show FY, FY-1, change %, and the working for each.
5.  Optional: 1–2 sector physical indicators (e.g. litres per employee), only if numerator and denominator have the same scope.
6.  **Fixed-asset sensitivity check:** assets under construction do not produce output yet. Recalculate indicator 7 as value added ÷ (avg net PPE − avg assets under construction) for every year, and show it in the Profile next to indicator 7, labelled "sensitivity: excluding assets under construction". It is a check only: indicator 7, the sector median and the DTF diagnostics keep using net PPE as reported. If assets under construction are not disclosed for a year, show "n.c." for that year. The result goes in the Profile and the Content file working; it is not shown on spotlight pages or cards.

**Sector median**

  - When **5 or more** companies in the same Bursa sector have profiles (attach their profile files or read them from Drive), calculate the median for each indicator.
  - Show each company's value next to the median. Never rank.
  - Below 5 companies: "Sector median: pending".
  - **When the 5th company in a sector reaches** **PROFILED****:** calculate the median and set every earlier company in that sector to FRONTIER\_UPDATE in the Ledger (see Module 3B). Only their snapshot box, DTF page, cards 06–07 and the email sections are re-rendered (\_v2); nothing else changes.

After PROFILE and DTF (Module 3B), run audit Steps 1–3 (Module 4B) on the DataSheet and Inventory, then write the **Content file** and the **Decisions file** (see "Two stages and the decision gate").

-----

# MODULE 3B — DISTANCE TO FRONTIER (DTF \[company\]; runs automatically after PROFILE)

**Goal:** answer three questions a reader can repeat in one breath: **how close** is the company's value added per employee to the sector frontier, is the gap **closing**, and **what sits behind it**. All calculations in code.

**Input:** the multi-year DataSheet (see 2B), the Profile, and every other Profile in the same Bursa sector from 03\_Working/. **Output:** \[Code\]\_\[Name\]\_FY\[YYYY\]\_DTF (Excel) and the sector panel file 03\_Working/\_Sector/\[Sector\]\_Frontier.xlsx.

**How it is described:** "inspired by OECD research on frontier firms". Never "the OECD method", "OECD-aligned" or "OECD-style". The OECD work uses the top 5% of firms in large, representative firm datasets and multi-factor productivity; this is labour productivity among a small set of selected listed companies.

## The DTF window

The **latest five financial years in the sector panel** (FY-4 to FY of the newest report in the panel; today FY2022–FY2026). The window is never hard-coded. When a report for a newer FY enters the panel, the window rolls forward one year and a new frontier vintage starts (see "Frontier vintage"). A company whose latest report is one year behind is shown for the years it has.

## Headline measure: frontier attainment

One measure only: **value added per employee** (Module 3, indicator 2), calculated for every year of the window with the Module 3 rules (averages, scope match, value-added check).

  - **Sector panel:** every company-year in the window for that Bursa sector, same scope (Group unless all are Malaysia-only). The panel includes the company itself.
  - **Frontier** = 90th percentile of value added per employee across the panel (numpy.percentile, linear method). It is **one RM value for the whole window**. Label it **"Selected listed-company peer frontier"**, never "the industry frontier" or "the Malaysian frontier".
  - **Frontier attainment** = company value ÷ frontier × 100, shown as a whole %. Capped at 0 and 100; 100 = "at or beyond the frontier".
  - **Gap in RM** = frontier − company value per employee (0 when at or beyond the frontier). Always show the two RM values next to the %.
  - **Sector median attainment** = sector median value added per employee for that year ÷ frontier × 100.
  - There is **no floor and no composite score**. The 10th percentile is no longer calculated.

## Mode 1 — Distance to Frontier (sector has 5+ companies and 20+ company-years)

  - **Trend:** frontier attainment for each year of the window, plus sector median attainment for each year.
  - **Verdict** (fixed wording, from the change in attainment between the first and the latest year shown; needs at least 3 years):

| Change in attainment | Verdict |
| :-: | :-: |
| 100 in the latest year | At the frontier |
| up by more than 5 points | Closing the gap |
| within 5 points either way | Holding steady |
| down by more than 5 points | Gap widening |

  - **Verdict line** (max 20 words): verdict + latest attainment + first-year attainment. Example: "Closing the gap: 63% of the sector frontier in FY2026, up from 50% in FY2022."
  - Because the frontier is one fixed value for the window, the trend shows **the company's own movement towards that bar**. Say so in the notes.

## Behind the gap (diagnostics, not scores)

The other four indicators are no longer scored or averaged. They are shown as plain values to help explain the gap:

1.  Revenue per employee
2.  Value added per RM1 staff cost
3.  Value added per RM1 fixed assets
4.  Inventory turnover (mark "not applicable" for firms without meaningful stock)

  - Show each as: first year of the window · latest year · sector median (latest year).
  - **Gap pointers:** the 1–2 diagnostics where the company's latest value is furthest **below** the sector median, in %. If none is below the median, write "No diagnostic is below the sector median".
  - **Reading rule for value added per RM1 staff cost:** always read it with average staff cost per employee (indicator 4). A high ratio together with staff cost per employee below the sector median is described as "lower wage level", never as a strength.
  - Diagnostics describe; they do not prove a cause.

## Mode 2 — Five-year progress (interim, fewer than 5 companies in the sector)

  - No frontier, no peers. Show value added per employee and the four diagnostics as an index, **first year of the window = 100**.
  - Label the panel "Five-year progress · sector frontier pending".
  - Switches to Mode 1 automatically when the sector qualifies.

## Frontier vintage (published numbers do not move)

  - Every time the panel is recalculated, add a row to the **Vintages** sheet of \[Sector\]\_Frontier.xlsx: vintage label (month and year) · window · number of companies · number of company-years · frontier value · sector median by year · Playbook version.
  - **Every DTF output prints its vintage**: "Frontier vintage: \[Mon YYYY\] · \[n\] companies · \[n\] company-years · includes this company".
  - When a new company reaches PROFILED, recalculate the panel. If the frontier or median moves, set every earlier company in that sector **that is not yet PUBLISHED** to FRONTIER\_UPDATE. Only their DTF page, DTF card, snapshot box and the email DTF line are re-rendered (\_v2), with the new vintage.
  - **PUBLISHED outputs are frozen.** They keep the vintage printed on them and are never re-rendered. A later edition or a REDO uses the new vintage and states: "Frontier updated since \[earlier vintage\]; earlier editions are unchanged."

## No-ranking rules for DTF (rule 6 applies in full)

  - The frontier is a **percentile, not a company**. Outputs never name the company-year that sets it.
  - Attainment % is capped at 100 in charts, gap bars and verdicts. A company's **own** value added per employee may be shown as reported on its own page, card or email, even where it is at or beyond the frontier; the attainment line then reads "at or beyond the frontier" (100%) and the gap is RM0. Readers may be able to work out that the company is above the frontier; this is accepted, because the figure is the company's own.
  - Never show another company's value on a company's page, and never a rank, a position or "x of y".
  - Never list or sort companies by attainment, in spotlights, editions or anywhere else.
  - Words not allowed: top, best, leader, ranked, outperform, laggard, worst.

## Analysis (3 sentences + pointer, for the spotlight; max 60 words)

1.  **Level:** "\[Company\] generated RM\[x\] of value added per employee in FY\[YYYY\], \[y\]% of the sector frontier of RM\[z\]."
2.  **Direction:** the verdict and the change in points since the first year.
3.  **Behind the gap:** the gap pointers against the sector median.
4.  **Lesson pointer** (one line, max 15 words): the page-4 lesson on the same subject as a gap pointer, e.g. "Lesson 2 on page 4 shows one way to raise output from existing machines." Link to an initiative **only where the report supports it with a quote**; otherwise describe timing only ("the rise in FY2025 coincides with the new Taiping lines"), never cause. If no lesson matches, leave the pointer out.

## Data checks (add to audit Step 2)

  - Every year's figures have a quote and page from the report they came from.
  - Restated figures: use the latest report that shows that year; note "restated".
  - Headcount definition must be the same in every year (apply the Rules tab). If it changes, flag the year and raise a decision.
  - Acquisitions or disposals that change the scope by more than 20% in a year: mark that year "scope change" and leave it out of the trend line.
  - Attainment = company value ÷ frontier, re-run from the DataSheet and the sector panel; frontier, panel size and vintage match the Vintages sheet.
  - No composite score, no floor and no indicator score appears anywhere in the DTF file or the Content file.
  - Values labelled "analyst-calculated nominal proxy". Optional real-terms VA per employee only with a cited DOSM deflator.

-----

# MODULE 4 — SPOTLIGHT (SPOTLIGHT \[company\])

**Stage:** A writes the content; B renders it. **Input:** Initiative Inventory, Profile, DTF, the reports, Rules tab. **Output (Stage A):** the Content file — all wording and figures below. **Output (Stage B):** 4-page A4 PDF plus a 1-page appendix, rendered from the **approved** Content file with 07\_Templates/spotlight.html, following the Style Guide. Saved to 04\_Spotlights/.

## SME lessons (the heart of the spotlight)

Write **up to three lessons** (three where three qualify), each on **one named initiative**.

**Eligibility (all must hold):** the initiative passes the productivity test · **Grade A** · Evidence type **Productivity result or Operating result** (an Enabler is never a lesson, even at Grade A) · not a sustainability measure or an HR benefit · the result has already been achieved. Search the FY report first, then FY-2, then FY-4 (Module 2A, "Earlier reports"). If fewer than three initiatives qualify, write only those that do: in drafts mark the empty slot "Under review"; on published outputs show only the qualifying lessons and never pad.

**Selection among eligible initiatives:** Tier 1 first (Tier 2 only if needed) → Productivity result before Operating result → the highest impact on output per worker, per machine or per unit of input, as reported → at most one Tier 3 lesson, only if a cost or input saving is quantified → the three lessons must be **three different initiative types** → among equals, what a 50–200 person firm can realistically adapt.

**Each lesson:**

1.  **Title** — the specific move. ✗ "Track output per machine" ✓ "Add a second line inside the existing plant before building a new one"
2.  **What \[Company\] did and achieved** — exact change, where, when, scale/cost, reported result + page.
3.  **The SME version** — how a smaller firm applies it, incl. who it suits.
4.  **Starter step** — one low-cost action to start this month.
5.  **How to measure** — a simple before-and-after measure.

**Not allowed:** lessons not tied to a named initiative; generic advice; using the company as a warning; lessons on capacity alone, scale, revenue, outlet growth, acquisitions, certifications, safety records, sustainability or HR benefits.

## Layout (4 pages + appendix; uncrowded is a hard rule)

This layout overrides any page count in the Style Guide. **Fit the page by cutting content, never by shrinking type or spacing.**

**Reading thread (every page) — so the reader carries the story from one page to the next**

  - **Page strip** at the top of pages 1–4, same place and style on each: "1 The story · 2 What they did · 3 Where they stand · 4 What you can do", with the current page highlighted.
  - **Takeaway line** directly under the title of pages 2–4: the one thing to remember from that page, max 15 words (EN; the page-3 verdict line may run to 20), plain words, with one number where possible. Never an "x of y" count. Page 1 uses the headline as its takeaway.
      - Page 2: the pattern in the initiatives, e.g. "Most of the effort went into new lines and automation."
      - Page 3: the DTF verdict line (Module 3B).
      - Page 4: what the three lessons have in common, or the first step.
  - **Same thing, same look:** the company is always one colour and the frontier always another, on every chart, card and page. An initiative or figure named on one page keeps exactly the same name and number on every other page.
  - **One pointer forward per page, max:** page 3 points to a page-4 lesson (Module 3B lesson pointer). No other cross-references.
  - The takeaway lines are written in Stage A and stored in the Content file. They use only figures already in the Content file.

**Page 1 — The story**

  - Headline (max 20 words EN / 24 BM): "\[Company\]: \[what they did and achieved\]", following the **headline hierarchy** below.
  - Intro: max 35 words, written to the story spine below.
  - Three headline results: big number, label (max 6 words), "up from x · p.n", and **one insight line** (max 15 words). No separate insights block.
  - **Productivity snapshot box:** 4 core indicators (VA per employee, VA per RM1 staff cost, capex per employee, inventory turnover) with FY, change and sector median (or "pending"). Notes under the box: max 2 lines.
  - One line: "\[n\] initiatives found: \[n\] core · \[n\] supporting · \[n\] resource". No initiative table on this page.

**Headline hierarchy (pick the first that exists)**

1.  A Tier 1 Grade A **Productivity result** (output or value added per worker, per machine hour or per unit of input).
2.  A Tier 1 Grade A **Operating result** (time, cost, defects, downtime or input per unit), e.g. "[Company]: drive-in racking raised rack utilisation 13% and cut pallets stored off-site" (name the year if the result comes from an earlier report).
3.  A Tier 1 Grade A **capacity Enabler**, only together with the value added per employee movement from the Profile in the headline or the first intro sentence, worded as reported: "capacity rose", never "productivity rose".

Never a headline: revenue, sales or profit · store, outlet or customer counts · acquisitions · certifications, awards, zero recalls or other compliance records · sustainability measures · HR benefits · targets or plans. A result from an earlier report may lead only if nothing in the latest report qualifies; name its year.

**Productivity story spine (every story, spotlight and web page)**

The headline, intro, results and indicators must tell **one productivity story**: what the company changed → what happened to output or inputs → what happened to productivity.

  - **Intro sentence 1:** the named move and its operating result. **Intro sentence 2:** what happened to value added per employee (Profile, FY vs FY-1), worded honestly, including a fall: e.g. "Capacity rose, but value added per employee rose only 3.4% as headcount grew."
  - **Three headline results:** at least **two** are Grade A Operating or Productivity results; at most one capacity Enabler; none from the "never an operating result" list. Each insight line ties the result to an input: per worker, per shift, per machine, per unit, per square metre.
  - **If the results rise but the indicators fall** (or the reverse), the intro or the first insight line says so. Never let the headline imply a productivity gain that the snapshot does not show.
  - **Takeaway lines** are written in productivity terms (output, inputs, value added), never in scale or revenue terms.
  - **Strengths and areas to watch** cover productivity and operating performance only.
  - Nothing in the story uses "productivity" for a capacity, revenue or scale change (rule 15).

**Page 2 — Key initiatives**

  - Table of the **10 most important** Tier 1–2, Grade A–B initiatives: Initiative | What they did | Reported result | Tier | Grade | Page. Cells max 8 words.
  - Order: Tier 1 Grade A, Tier 1 Grade B, then Tier 2.
  - One line under the table: "All \[n\] initiatives are listed in the appendix."
  - Two strengths and two areas to watch (productivity and operating performance only), max 25 words each.

**Page 3 — Distance to Frontier ("Where they stand")**

Read from top to bottom, the page answers in order: how close, which direction, what sits behind it, what to do next.

  - Title: "Distance to Frontier" (Mode 1) or "Five-year progress" (Mode 2).
  - Takeaway = the **verdict line** (Mode 1, max 20 words) or the progress line (Mode 2).
  - One big number: latest-year **frontier attainment %** (Mode 1) or VA per employee index (Mode 2). Under it, in ringgit: "RM\[x\] per employee · frontier RM\[z\] · gap RM\[g\]".
  - **Gap bar** (Mode 1): one horizontal bar from 0 to the frontier, with three markers: the company in the first year, the company in the latest year, and the sector median (latest year). No other company appears.
  - One line chart over the window: company attainment, sector median attainment, frontier = 100 (Mode 1); or the indices (Mode 2).
  - **"Behind the gap" table:** the four diagnostics with first-year value, latest-year value and sector median. Gap pointers marked. Values only, no scores.
  - Analysis: max 60 words (Module 3B), then the lesson pointer line.
  - Notes (max 3 lines): "Selected listed-company peer frontier: 90th percentile of \[n\] company-years from \[n\] Bursa \[sector\] companies, FY\[first\]–FY\[last\], including this company. Vintage \[Mon YYYY\]. One fixed frontier for the window. Not a ranking. Nominal analyst proxy. Inspired by OECD research on frontier firms; not the OECD method."

**Page 4 — SME lessons (up to three)**

  - Each lesson: label line · title (max 14 words) · What they did and achieved (max 40 words) · The SME version (max 40 words) · Starter step (max 25 words) · How to measure (max 20 words).
  - Notes (max 3 lines): sources; figures as reported, not independently audited; value added is an analyst proxy; not investment advice.

**Appendix — All initiatives found (1 page)**

  - Every initiative not in the page-2 table, as a clean two-column list grouped by Tier: name · grade · page. One item per line, no running paragraphs. Never drop any.
  - If it does not fit one page, use a smaller second column, never a paragraph.

**Spacing rules (all pages)**

  - Body text at least 10 pt, line height at least 1.4, table text at least 9 pt.
  - At least 8 mm between blocks; nothing touches the page margins.
  - **BM word budgets are the EN limits − 15%**, because BM runs longer. Shorten wording; never cut a figure or page reference.

**Writing:** one caveat line at most, in the notes. Name machines, systems, plants and numbers. Strengths describe achievements, never "the company discloses…". Word every result as reported ("capacity rose", "output rose", "cost fell"); never write that productivity rose because capacity did (Module 2A).

-----

# MODULE 4B — SELF-AUDIT (Steps 0–3 in Stage A on the data and Content file; Steps 4–6 in Stage B on the rendered spotlight)

**Goal:** catch and fix errors before the human sees anything. Act as a sceptical, independent auditor, not the author.

## Step 0 — Learn from past mistakes

Before writing anything, read the **Rules** tab and the **ImprovementLog** sheet in Productivity\_Lens\_Templates (or from Drive). Apply every "Rule to add" from past reviews.

## Step 1 — Evidence audit

For **every** figure in the spotlight, profile and inventory:

  - Re-open the source page and check the quote **appears word for word**.
  - Check the number in the output matches the quote exactly (units, RM'000 vs RM million, year).
  - Check the printed page number is right.
  - Check each initiative result is worded as the kind of change in its quote (capacity, output, cost, time, yield, headcount). "Productivity rose" needs a quote that says so. Result per figure: ✅ Confirmed · ⚠️ Mismatch (fix it) · ❌ Not found (remove it).

## Step 2 — Calculation audit

  - Re-run every indicator **in a fresh code cell**, from the DataSheet only.
  - Check value-added components add up, for each year.
  - Check averages use the same method across years, and scopes match.
  - Re-run the DTF calculation from the DataSheet and sector panel (Module 3B data checks).
  - Re-run the fixed-asset sensitivity check; confirm assets under construction come from the PPE note of each year's report.
  - Confirm every indicator in the Content file has its working and that the components reproduce the result.

## Step 3 — Completeness audit

  - Re-scan the report for initiatives not in the inventory (search terms: line, plant, automation, system, digital, capacity, upgrade, efficiency, training, dealer, outlet, fleet, warehouse, yield, rework, cost saving). Add any missed.
  - Confirm every counted initiative appears on page 2 or in the appendix.
  - **Re-apply the productivity test** (Module 2A) to every counted initiative. For each one cited from the sustainability pages (PageMap), confirm its quote has an operating measure. Move any that fail to "Not counted" and correct the counts.
  - Search the inventory for: carbon, emission, solar, renewable, ESG, recycl, community, certification, award, recall, revenue, sales, store, outlet, acquisition, acquired, freezer, expected, target, plan, will, under construction, benefit, allowance. Review each hit against the three-question test and the "never an operating result" list; do not remove automatically.
  - Check every Grade A item has an operating change (not revenue or scale), and every lesson is Grade A with an Operating or Productivity result.
  - Check the story spine: the intro states the value added per employee movement, and no headline or result implies a productivity gain the snapshot does not show.
  - Read the "Not counted" sheet once for items with an operating result that were excluded by mistake.

## Step 4 — Quality scorecard (score each 1–5)

|  |  |
| :-: | :-: |
| \*\*Check\*\* | \*\*5 means\*\* |
| Accuracy | every figure confirmed |
| Completeness | no missed initiatives |
| Productivity focus | headline follows the hierarchy; ≥2 of 3 results are Operating or Productivity results; every lesson Grade A with an Operating or Productivity result; story spine holds; no ESG, HR-benefit, revenue or scale drift |
| Lesson strength | each lesson specific, tied to a named initiative, with result, SME version, starter step, measure |
| Variety | three different initiative types |
| Clarity | plain English, one caveat line, no jargon; each page's takeaway can be understood without reading the rest of the page |
| Format | 4 pages + appendix, fit check passed, style guide followed, no rankings or rank words, page strip and takeaway line on every page |

## Step 4b — Fit check (on the rendered PDF, EN and BM)

  - Count words per block against the Module 4 budgets (in code).
  - Render each page and look at it: no overflow, no text running into another block, white space between blocks, body text ≥ 10 pt.
  - If a page fails: cut lowest-priority words first (adjectives, repeated context, second examples), re-render, check again. Never shrink type.

## Step 5 — Fix and repeat

  - If **any score is below 4**, or any ❌/⚠️ was found: fix the output and run Steps 1–4 again.
  - Maximum **2 fix rounds**. If still below 4, stop and flag it for the human.

## Step 6 — Audit report (save to 03\_Working/\[Code\_Name\]/)

\[Code\]\_\[Name\]\_FY\[YYYY\]\_Audit containing:

1.  Scorecard (before and after fixes).
2.  What was changed and why.
3.  Figures confirmed: x of y.
4.  **Top 5 items for the human to check first**: the riskiest figures, each with quote and page. Judgement calls are not listed here; they went to the Decisions file and the Ledger.
5.  Status: **Ready for human review** or **Needs attention**.

-----

# MODULE 4C — SNAPSHOTS (SNAPSHOT \[company\]; Stage B, after the final audit)

**Goal:** PNG images for quick viewing and sharing (WhatsApp, LinkedIn, slides, approval packs).

**Make these PNGs** from the **approved Content file** and the audited spotlight only:

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*\\\#\*\* | \*\*Snapshot\*\* | \*\*Size (px)\*\* | \*\*Content\*\* |
| 1–4 | Page images | A4 at 200 dpi (1654 × 2339) | Each of the 4 spotlight pages as a PNG (not the appendix) |
| 5 | Headline card | 1080 × 1350 | Company, FY, headline, the 3 headline results with big numbers |
| 6 | Productivity snapshot card | 1080 × 1350 | The 4 snapshot indicators with change and sector median (or "pending") |
| 7 | DTF card | 1080 × 1350 | Frontier attainment % with the two RM values (or five-year progress), the verdict line, the trend line, frontier vintage in the footer |
| 8–10 | SME lesson cards | 1080 × 1350 each | One lesson per card: title, what they did and achieved, SME starter step |

**Rules**

  - Render from the HTML templates in 07\_Templates/ (card.html, page images from the spotlight PDF), using the Style Guide colours and fonts.
  - Text at least 28px on social cards; no paragraph longer than 3 lines.
  - Every card shows "Productivity Lens" and, at the bottom, "Source: \[Company\] Annual Report FY\[YYYY\], p.\[x\]".
  - Use only figures already confirmed in the self-audit. No new numbers.
  - No company logos, stock photos or photos of people.
  - After rendering, open each PNG and check: no cut-off text, no overlap, readable on a phone. Fix and re-render if needed.
  - File names: \[Code\]\_\[Name\]\_FY\[YYYY\]\_Snap\_\[01–10\].png. Save to 04\_Spotlights/Snapshots/ (Cowork). In a normal chat, attach in the chat and mark Saved: chat only.

-----

# MODULE 4D — BAHASA MELAYU VERSION (BM \[company\]; Stage B, after the snapshots)

**Goal:** a Bahasa Melayu spotlight PDF and BM snapshot cards, for SME owners who prefer BM.

**Order:** translate only **after** the final audit, from the approved English Content file. Translate the text fields into \[Code\]\_\[Name\]\_FY\[YYYY\]\_Content\_BM.json (numbers, pages and quotes stay identical), then render with the same templates. Never re-extract or add new content. **Check in code:** every number in the BM Content file matches the English one exactly.

**Outputs**

  - \[Code\]\_\[Name\]\_FY\[YYYY\]\_Spotlight\_BM.pdf — same 4-page layout plus appendix as English, saved to 04\_Spotlights/. Use the BM word budgets (EN − 15%) and run the fit check.
  - \[Code\]\_\[Name\]\_FY\[YYYY\]\_Snap\_BM\_\[01–10\].png — same 10 snapshots, in BM, saved to 04\_Spotlights/Snapshots/.

**Rules**

  - Standard **Bahasa Malaysia** (Dewan Bahasa dan Pustaka style), formal but friendly. Not Bahasa Indonesia (e.g. use "syarikat", not "perusahaan"; "kakitangan", not "karyawan").
  - **Numbers, units, page numbers and company names stay exactly the same.** Keep RM and decimal points as in English (RM2.70).
  - Machine, system and product names stay in English where the company uses English (e.g. "rotary milking parlour", "SYSPRO ERP"); add a short BM explanation in brackets the first time if needed.
  - Brand name stays **Productivity Lens**.
  - Use the glossary below for every key term, so all spotlights read consistently.
  - Rewrite naturally; do not translate word for word. Keep sentences short.
  - Check every BM PNG for cut-off text (BM is often 10–20% longer); shorten wording, never shrink text below 28px on cards.

**Glossary (EN → BM)**

|  |  |
| :-: | :-: |
| \*\*English\*\* | \*\*Bahasa Melayu\*\* |
| Productivity | Produktiviti |
| Company spotlight | Sorotan syarikat |
| Headline results | Keputusan utama |
| Key insights | Pandangan utama |
| Productivity snapshot | Ringkasan produktiviti |
| Revenue per employee | Hasil bagi setiap pekerja |
| Value added per employee | Nilai ditambah bagi setiap pekerja |
| Value added per RM1 staff cost | Nilai ditambah bagi setiap RM1 kos kakitangan |
| Average staff cost per employee | Purata kos kakitangan bagi setiap pekerja |
| Capex per employee | Perbelanjaan modal bagi setiap pekerja |
| Capital intensity | Intensiti modal |
| Value added per RM1 fixed assets | Nilai ditambah bagi setiap RM1 aset tetap |
| Inventory turnover | Pusing ganti inventori |
| Sector median | Median sektor |
| Pending | Belum tersedia |
| Analyst-calculated nominal proxy | Anggaran nominal kiraan penganalisis |
| Initiative | Inisiatif |
| Tier 1 core / Tier 2 supporting / Tier 3 resource | Tahap 1 teras / Tahap 2 sokongan / Tahap 3 sumber |
| Grade A / B / C | Gred A / B / C |
| Production line | Barisan pengeluaran |
| Automation | Automasi |
| Capacity | Kapasiti |
| Process redesign | Reka bentuk semula proses |
| Workforce / upskilling | Tenaga kerja / peningkatan kemahiran |
| Distribution / dealer network | Pengedaran / rangkaian pengedar |
| Supply chain | Rantaian bekalan |
| Strengths | Kekuatan |
| Areas to watch | Perkara untuk dipantau |
| SME lessons | Pengajaran untuk PKS |
| What they did and achieved | Apa yang dilakukan dan hasilnya |
| The SME version | Versi PKS |
| Starter step | Langkah permulaan |
| How to measure | Cara mengukur |
| Annual report | Laporan tahunan |
| Source | Sumber |
| Not investment advice | Bukan nasihat pelaburan |
| Distance to Frontier | Jarak ke Sempadan |
| Frontier | Sempadan |
| Gap | Jurang |
| Five-year progress | Kemajuan lima tahun |
| Sector frontier pending | Sempadan sektor belum tersedia |
| Frontier attainment | Pencapaian berbanding sempadan |
| Selected listed-company peer frontier | Sempadan rakan setara syarikat tersenarai terpilih |
| Closing the gap | Jurang semakin rapat |
| Holding steady | Jurang kekal stabil |
| Gap widening | Jurang semakin melebar |
| At the frontier | Di paras sempadan |
| Behind the gap | Di sebalik jurang |
| Frontier vintage | Versi sempadan |
| Inspired by OECD research on frontier firms | Diilhamkan oleh kajian OECD mengenai firma sempadan |
| The story / What they did / Where they stand / What you can do | Kisahnya / Apa yang dilakukan / Kedudukan semasa / Apa yang anda boleh lakukan |
| Enabler / Operating result / Productivity result | Pemboleh / Hasil operasi / Hasil produktiviti |
| Key initiatives | Inisiatif utama |
| Appendix: all initiatives found | Lampiran: semua inisiatif yang ditemui |
| Figures as reported, not independently audited | Angka seperti yang dilaporkan syarikat, tidak diaudit secara bebas |

-----

# MODULE 4E — NEWSLETTER EMAIL (EMAIL \[company\]; last step of Stage B)

**Goal:** when a report is finished, I receive it as a newsletter-style email, so I can read it on my phone exactly as a subscriber would.

**Recipient:** **only my own email address.** Never send to anyone else. Subscriber sending happens later, outside Claude, after review and approval (Module 7).

**How to send**

  - **Always** save the HTML file \[Code\]\_\[Name\]\_FY\[YYYY\]\_Newsletter.html to 04\_Spotlights/Newsletter/.
  - If the Gmail connector is available: also create a **Gmail draft addressed to me** with that HTML. In a RUN with more than one finished company, make one digest draft instead (see Batch summary).
  - If neither works: report ⚠️ EMAIL FAILED – \[reason\] on the email line. Never leave the line out.

**Email format**

  - Subject: Productivity Lens | \[Company\]: \[headline, max 60 characters\]
  - Preview text (max 90 characters): the single strongest result.
  - Mobile-friendly HTML: single column, 600px wide, inline CSS only, Style Guide colours, system fonts (Arial/Georgia), no scripts.

**Email content (in this order)**

1.  Header bar: **Productivity Lens** · Company · FY.
2.  Headline and a 2-sentence intro.
3.  **Three headline results** as large-number blocks, each with its page reference.
4.  **Productivity snapshot**: the 4 indicators with change and sector median (or "pending").
5.  **Distance to Frontier**: the verdict line (or five-year progress), with the frontier vintage.
6.  **SME lessons** (up to three, qualifying only), short form: title, what they did and achieved (1 line), starter step (1 line).
7.  Links: full spotlight PDF (EN), BM version, and snapshots folder — Drive links (read the share link with the Drive connector if available; otherwise give the folder path), or "attached in Claude chat" in a normal chat.
8.  Status line from the self-audit: "Ready for human review" or "Needs attention: \[reason\]".
9.  Footer: "Source: \[Company\] Annual Report FY\[YYYY\]. Figures as reported, not independently audited. Not investment advice. DRAFT – not for distribution until reviewed."

**Rules**

  - Use only the approved Content file. No new figures.
  - Text ≥ 14px; big numbers ≥ 28px; works without images (images are a bonus only).
  - One BM email is not needed; link to the BM files instead.
  - After the email step, set Pipeline status to COMPLETE in the Ledger and record all output file names.

-----

# MODULE 5 — REVIEW (REVIEW \[company\]; spot-check list is made automatically at the end of Stage B)

**Goal:** make my human check fast. The self-audit already checks every quote, so my review focuses on judgement and a small random sample. Judgement calls were settled at the decision gate, before rendering.

**Produce, and add to the Review sheet** (one row per spot-check, with a tick-box column, so I can review on my phone in Google Sheets):

1.  **Spot-check list** chosen at random (at least 3 from the spotlight's page 1), each with figure, quote and page.

      - **First 5 companies reviewed: 10 spot-checks each.**
      - **After 5 companies in a row pass 10/10: 5 spot-checks each.**
      - **If any spot-check fails: back to 10** for the next 5 companies.
2.  **Automatic checks** (pass/fail, done in code where possible): every initiative on page 2 or in the appendix · every figure has a quote and page · value added reconciles · headline and ≥2 lessons from Tier 1 · headline follows the hierarchy and is not on the "never an operating result" list · ≥2 of 3 headline results are Operating or Productivity results · every lesson Grade A with an Operating or Productivity result · intro states the value added per employee movement · no counted initiative is planned, revenue-only, an acquisition, an asset placement or a compliance record · 3 different initiative types in lessons · no ranking words ("top", "best", "leader", "ranked", "outperform", "laggard", "worst") · 4 pages + appendix, fit check passed · every number in every output appears in the Content file · every indicator in the Content file has its working · no result described as a productivity gain unless its quote says so · every counted initiative passes the productivity test; none is counted on an environmental or social result alone · every counted initiative has an Evidence type and no Enabler is worded as a productivity gain · DTF shows attainment, both RM values, panel size and frontier vintage · no composite or indicator score anywhere · the words "OECD method", "OECD-aligned" and "industry frontier" do not appear · page strip and takeaway line present on every page.
3.  **Risk flags** not already settled as decisions: any page that was hard to read, any text-only table figure.
4.  **Sign-off:** when all spot-checks are ticked, set the Review row Status to Verified and the Ledger to VERIFIED. EDITION uses only VERIFIED companies.

**After review:** for every issue I find, add a row to **ImprovementLog**: Date | Company | Issue | Root cause | Rule to add. If the fix is a judgement rule, also add it to the **Rules** tab. Future runs read both first.

-----

# MODULE 6 — EDITION (EDITION \[sector / issue no.\])

**Input:** 3–5 companies at VERIFIED in the Ledger, with their Content files, profiles and inventories read from 03\_Working/ (same sector preferred). **Output saved to:** 05\_Editions/. A sector view may show the sector frontier value, its vintage and the median attainment trend. Never list or sort companies by attainment. **Output:** a newsletter issue, A4 PDF, 6–8 pages.

1.  **Cover + editor's note** (half page): the issue theme in 3–4 sentences, e.g. "How F\&B firms add capacity without adding headcount".
2.  **Sector at a glance** (1 page): the 8 core indicators for each company **listed alphabetically**, plus the sector median. No ranks, no colour-coding of winners.
3.  **What the companies are doing** (1 page): count of initiatives by type across companies, and 3 patterns seen in several firms.
4.  **Company spotlights** (1 page each): condensed — headline, 3 results, strongest SME lesson.
5.  **The SME playbook** (1 page): the 5 strongest lessons across all companies, each with starter step and measure.
6.  **Methodology and notes** (short): sources, value-added definition, scope rules, sector median basis, frontier definition (selected listed-company peer frontier, panel size, vintage), "inspired by OECD research on frontier firms; not the OECD method", not investment advice.

-----

# MODULE 7 — DISTRIBUTE (DISTRIBUTE \[issue no.\])

**Output:**

1.  3 email subject lines + preview text.
2.  Email body (≤150 words) with the issue theme, 3 takeaways and a link placeholder \[LINK\].
3.  LinkedIn post (≤120 words).
4.  **Send checklist:**

      - Every company in the edition is VERIFIED in the Ledger; set them to PUBLISHED after sending
      - Copyright position on annual-report content confirmed
      - Subscribers opted in; privacy notice and unsubscribe link present (PDPA 2010)
      - Approval obtained if issued under MPC's name
      - Subscriber data stored in the email tool only, not in this project

Sending is done outside Claude (e.g. Mailchimp or MailerLite). Never place subscriber names or emails into this project.

-----

# DEFERRED — REVIEWED, NOT ADOPTED

Ideas reviewed on 11 and 13 November 2026 and kept in view. **Do not apply any of them in a run** until they are moved into a module above.

  - **Loss-making years (KIV):** when a loss is larger than staff costs + depreciation + finance costs, value added is negative and attainment would be below zero. For now the 0 cap applies and the year shows 0%. A clearer treatment (e.g. showing "loss year, not scored") is to be decided.
  - **Non-operating items in PBT** (e.g. fair-value changes on biological assets, finance income): record them and test an adjusted value added.
  - **Year-by-year (moving) frontier:** not adopted. With 5–10 companies per sector, a frontier for a single year would rest on too few observations. Revisit if a sector panel reaches about 20 companies.
  - **Peer groups by activity (MSIC) instead of Bursa sector:** not adopted. Listed companies per activity are too few. The limitation is stated in the frontier label and notes instead.
  - **Larger minimum sample (20–30 companies):** not adopted for the same reason. The 5-company threshold stays, with panel size printed on every output.
  - **Dairy peer group:** whether peers report dairy segment figures and headcount, and how different financial year ends are aligned.
  - **Real-terms value added** with a documented deflator, as standard rather than optional.
  - **Production-approach value added** (output less intermediate inputs).
  - **Physical indicators** in DTF (labour hours, capacity utilisation, energy, milk per cow).
  - **Further changes to the Tier and Grade definitions** beyond those made in v1.12.
  - **Peer similarity scores.**
  - **Move from newsletter to website:** this Playbook still describes the newsletter outputs; a fuller rewrite is pending.

**Adopted in v1.12:** Tier 1 and Grade A tightened (productivity focus). **Adopted in v1.11 and removed from this list:** DTF panel disclosure · the composite DTF score question (composite removed).

-----

# PHASES 2 AND 3 (LATER)

  - **Phase 2 – Asia:** same modules; add currency and financial-year conversion notes; compare only within sector.
  - **Phase 3 – Global:** same modules; reference points from high-productivity economies such as Singapore, Finland and Switzerland.
  - Graphify (Claude Code) can map initiatives across companies once 10+ inventories exist in 03\_Working/.

**END OF PLAYBOOK v1.12**
