# DataSheet format read by pl_profile.py

Long format: one row per item per year. The template sheet (title rows above a header row) is fine; the script finds the header row that contains "Item".

| Column | Required | Notes |
|---|---|---|
| Item | yes | Matched by the names below (case-insensitive) |
| Value | yes | Number as reported. Commas, brackets for negatives and the − sign are handled |
| Year | yes | Best: absolute (`FY2025` or `2025`). Relative (`FY-1`) is resolved against Source report, else FY |
| FY | recommended | The job's FY, e.g. `FY2026` |
| Source report | recommended | FY of the report the figure came from, e.g. `FY2024`. Used to prefer restated figures |
| Scope | recommended | `Group` (default) or `Malaysia`. Anything else is kept as written |
| Page, Quote, Restated | for audit | Not used in the arithmetic; kept for traceability |

## Item names recognised (first match wins, in this order)

| Key | Matches item names like |
|---|---|
| capex | Purchase of PPE, Purchase of property…, Capex, Acquisition of PPE |
| staff_costs | Staff costs, Employee benefits expense, Personnel costs |
| d_and_a | Depreciation and amortisation, D&A |
| depreciation / amortisation | Depreciation… / Amortisation… (summed if no D&A total) |
| finance_costs | Finance costs, Interest expense |
| cost_of_sales | Cost of sales, Cost of goods sold |
| pbt | Profit before tax, PBT, (Loss) before tax |
| net_ppe | Property, plant and equipment; Net PPE |
| inventories | Inventories |
| employees | Number of employees, Headcount, Employees, Workforce |
| revenue | Revenue, Turnover, Segment revenue |

Physical measures (tonnes, litres, outlets) are not used by the 8 indicators; keep them in the DataSheet for the spotlight text.

## Units
Financial figures in RM'000 (default `--unit-multiplier 1000`). Ratios are unit-free. Per-employee results are in RM.

## Malaysia-only headcount
Give Malaysia segment figures with `Scope = Malaysia` (Revenue, PBT, staff costs, D&A, finance costs, PPE, capex). If any VA component is missing for Malaysia, per-employee indicators show "Scope mismatch".
