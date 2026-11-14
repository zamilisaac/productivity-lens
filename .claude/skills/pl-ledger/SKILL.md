---
name: pl-ledger
description: Productivity Lens memory and intake manager. Reads and updates the Ledger (one row per report file) and the Rules tab, works out whether a report is new, already done, a duplicate, a skipped file to leave alone, or a part-done job to resume, enforces status order and the two-attempt retry cap, reads the user's decision answers, and flags FRONTIER_UPDATE companies. Use this at the start and after every module of any Productivity Lens run (PREP, ANALYSE, FULL, PRODUCE, APPROVE, QUEUE, RUN, REDO, TEST), whenever a report is dropped in the inbox, whenever a decision is approved or a rule added, and whenever the user asks what is done, queued, skipped or awaiting decisions. "Never repeat work" depends on it.
---

# pl-ledger — Ledger and Rules

One script, `scripts/ledger.py`. Needs `openpyxl` (`pip install openpyxl --break-system-packages`).

Why: the Ledger is the project's only memory between chats. Doing the checks in code (MD5, status order, retry cap) stops two failure modes: redoing finished work, and silently retrying a broken file forever.

## Where the Ledger lives

- **Cowork, local workbook** (`01_Register/Productivity_Lens_Templates.xlsx`): use `--book <path>`. The script edits the Ledger and Rules sheets in place. The workbook is the register, not an output, so the no-overwrite rule doesn't apply to it.
- **Google Sheet via connector**: read the sheet with the Sheets connector, save it as CSV, run with `--ledger-csv <file> --rules-csv <file>`, then write back the rows listed under `changes` (each has the sheet, row number and values).
- **No connector**: run with `--ledger-csv "<PL>/01_Register/_ledger_pending.csv"`; report "Ledger: pending sync". At the start of the next run where the sheet is available, apply the pending rows, then clear that file (rename it `_ledger_pending_applied_[date].csv`).

First time only: `python scripts/ledger.py init --book <workbook>` adds the Ledger and Rules sheets with the Playbook columns if they are missing (the current Templates workbook has neither).

## Start of every run

```bash
python scripts/ledger.py queue --book <wb> --playbook v1.8      # what's new, part-done, awaiting, done, skipped
python scripts/ledger.py decisions --book <wb>                   # answers typed in the Decisions column
python scripts/ledger.py rules --book <wb>                       # read every rule; apply them
```
Then, before opening any report file:
```bash
python scripts/ledger.py check --book <wb> --file "<path to pdf>" --spotlights-dir "<PL>/04_Spotlights/"
```
| action | do |
|---|---|
| new | `add` a row, then process |
| already_done | skip, list under "Already done" |
| already_done_backfill | spotlight exists but no row: `add` the row, set COMPLETE, skip |
| resume | start at `resume_at`, reading saved files from `03_Working/` |
| skip_same_md5 | leave it; retry only if parts or a `_text.txt` have appeared |
| retry_changed_file / duplicate / parked | as named; parked needs the user |

## After every module

```bash
python scripts/ledger.py update --book <wb> --code 5306 --fy 2026 \
  --set "Pipeline status=EXTRACTED" --set "Last module done=EXTRACT" \
  --set "Output files=5306_FarmFresh_FY2026_DataSheet.xlsx; 5306_FarmFresh_FY2026_Initiatives.xlsx" \
  --set "Saved to=03_Working/5306_FarmFresh/"
```
`Last module done` values: PREP, EXTRACT, PROFILE, DTF, AUDIT 1-3, CONTENT, DECISIONS, SPOTLIGHT, AUDIT 4-6, SNAPSHOTS, BM, EMAIL. Output files are appended, not replaced. Backwards moves are refused unless `--redo` (only for the REDO command). Updates by code never touch duplicate or skipped rows.

- Failure: `fail --code 5306 --fy 2026 --reason "..."` (second failure sets PARKED – needs you).
- Skipped file: `add ... --intake SKIPPED_TOO_LARGE --notes "over 10 MB, no cut version; fix: run PREP in Cowork"`.
- Frontier moved (from pl-calc's `frontier_update_codes`): `frontier-update --codes 9001,9002 --fy 2026`.

## Decisions and rules

- Before raising a decision, `rules --find "<keyword>"`. If a rule covers it, apply it, cite the Rule ID in "Rules applied", and don't ask.
- After APPROVE, add each answer as a rule unless the user said "this company only":
  `add-rule --situation "..." --rule "..." --example "5306, p.176" --source decision` (add `--test` during TEST runs: marks it "TEST – confirm"). The output lists possible overlapping rules; if one exists, mention it rather than adding a near-duplicate.
- Rules outrank Playbook defaults; flag any conflict in the audit.
