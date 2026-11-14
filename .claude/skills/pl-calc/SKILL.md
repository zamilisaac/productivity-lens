---
name: "pl-calc"
description: Productivity Lens calculation engine. Calculates the 8 core productivity indicators (PROFILE, Module 3) and Distance to Frontier or five-year progress (DTF, Module 3B) from a Productivity Lens DataSheet, using tested scripts so every company is calculated the same way. Use this whenever running PROFILE, DTF, ANALYSE, FULL, TEST, RUN or audit Step 2 (calculation audit) for Productivity Lens, whenever a sector median or sector frontier must be recalculated, when a company is set to FRONTIER_UPDATE, or whenever anyone asks for revenue/value added per employee, VA per RM1 staff cost, capital intensity, inventory turnover or DTF scores for a Bursa company. Use it instead of writing fresh calculation code.
---

# pl-calc — Profile and Distance to Frontier

Two scripts do all Productivity Lens arithmetic. Running the same code every time is what makes the "all arithmetic in code" rule trustworthy: audit Step 2 just re-runs the script and compares, rather than checking newly written code.

Scripts are in `scripts/` next to this file. Needs `pandas`, `numpy`, `openpyxl` (`pip install pandas numpy openpyxl --break-system-packages` if missing).

## 1. PROFILE (`scripts/pl_profile.py`)

Input: the DataSheet from EXTRACT (xlsx in template layout, or csv). See `references/datasheet_format.md` for the columns and item names the script recognises. Read it if a run reports "row ignored" or an item is missing.

```bash
python scripts/pl_profile.py --datasheet "<path>/5306_FarmFresh_FY2026_DataSheet.xlsx" \
  --company "Farm Fresh Berhad" --code 5306 --sector "Consumer Products & Services" \
  --fy 2026 --name FarmFresh --out-dir "<Productivity Lens>/03_Working/5306_FarmFresh/" \
  --sector-profiles-dir "<Productivity Lens>/03_Working/"
```

Options to set from the Rules tab or an approved decision (never guess them):
- `--headcount-basis average` when the company reports average headcount (default: year-end, averaged opening + closing).
- `--no-inventory` for firms without meaningful stock (inventory turnover becomes "not applicable").
- `--scope-change-years 2023` for years with an acquisition/disposal over 20% of scope (left out of the DTF trend).
- `--unit-multiplier 1000` (default) converts RM'000 to RM per employee. Use `1` if figures are already in RM.

What it does for you: resolves FY-n years, takes the later (restated) report when two reports give the same year, sums depreciation + amortisation if only separate lines exist, treats costs as positive whatever sign was typed, matches scope (Malaysia headcount → Malaysia figures, else "Scope mismatch"), marks missing openings "n.c.", checks value added reconciles every year, and computes the sector median once 5+ companies have profiles.

Outputs (never overwrites, adds `_v2`): `..._Profile.xlsx` (template columns + AllYears + Checks sheets) and `..._Profile.json` (input for DTF and for pl-render).

**Read the `checks` list in the printed output.** Lines starting `DECISION` are decision triggers for the Decisions file unless the Rules tab already covers them. `DECISION/RESTATED` means two reports disagreed; the later one was used and the figure must be noted "restated".

## 2. DTF (`scripts/pl_dtf.py`)

Run after PROFILE. It reads every `*_Profile*.json` in the sector (latest version per company).

```bash
python scripts/pl_dtf.py --code 5306 --sector "Consumer Products & Services" \
  --profiles-dir "<Productivity Lens>/03_Working/" \
  --out-dir "<Productivity Lens>/03_Working/5306_FarmFresh/" \
  --sector-dir "<Productivity Lens>/03_Working/_Sector/" --start 2022 --end 2026
```

- **Mode 1** (5+ companies and 20+ company-years): P90 frontier, P10 floor (`numpy.percentile`, linear), scores capped 0–100, composite needs 4+ indicators, sector median composite per year, direction (±5 points = stable), 1–2 gap drivers.
- **Mode 2** (otherwise): each indicator indexed FY2022 = 100, labelled "Five-year progress · sector frontier pending".
- Saves `..._DTF.json/.xlsx` and `_Sector/[Sector]_Frontier.json/.xlsx` (panel listed alphabetically).
- `frontier_update_codes` in the output = companies to set to `FRONTIER_UPDATE` in the Ledger (frontier, floor or mode moved). Hand this list to pl-ledger.

## 3. Writing the DTF analysis (3–4 sentences, max 70 words)

Use only numbers from the DTF JSON: (1) where the company is now, (2) direction since FY2022 using the `direction` field, (3) the `gap_drivers`, (4) a link to a Tier 1 initiative only when a quote supports it; otherwise describe timing, never cause. Never name another company, never give a position, and never use: top, best, leader, ranked, outperform, laggard, worst.

## 4. Audit Step 2

Re-run both scripts into a scratch folder (e.g. `/tmp/audit/`) from the DataSheet only, then compare every indicator with the saved Profile/DTF JSON. Any difference = ⚠️ Mismatch. Do not edit the scripts during a run to make numbers fit; if a script is wrong, stop and report it.
