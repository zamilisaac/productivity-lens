#!/usr/bin/env python3
"""
Productivity Lens - PROFILE calculator (Playbook Module 3).

Reads a DataSheet (xlsx or csv, long format, one row per item per year) and
calculates the 8 core indicators for every year it can, with the working.

Usage:
  python pl_profile.py --datasheet 5306_FarmFresh_FY2026_DataSheet.xlsx \
      --company "Farm Fresh Berhad" --code 5306 --sector "Consumer Products & Services" \
      --fy 2026 --out-dir 03_Working/5306_FarmFresh/ [--name FarmFresh] \
      [--headcount-basis yearend|average] [--no-inventory] \
      [--scope-change-years 2023] [--sector-profiles-dir 03_Working/]

Outputs (never overwrites; adds _v2, _v3):
  [Code]_[Name]_FY[YYYY]_Profile.xlsx   template columns + all-years sheet + checks sheet
  [Code]_[Name]_FY[YYYY]_Profile.json   all years, used by pl_dtf.py
Exit code 0 = ran; check the "checks" list in the JSON for problems.
"""
import argparse, json, re, statistics, sys
from pathlib import Path

import pandas as pd

# ----------------------------------------------------------------- items
# Ordered: the first pattern that matches wins, so specific ones go first.
ITEM_PATTERNS = [
    ("capex", [r"purchase of (ppe|property)", r"\bcapex\b", r"acquisition of (ppe|property)"]),
    ("staff_costs", [r"staff cost", r"employee benefit", r"personnel cost"]),
    ("d_and_a", [r"depreciation\s*(and|&)\s*amorti[sz]ation", r"\bd\s*&\s*a\b"]),
    ("depreciation", [r"^depreciation"]),
    ("amortisation", [r"^amorti[sz]ation"]),
    ("finance_costs", [r"finance cost", r"interest expense"]),
    ("cost_of_sales", [r"cost of sales", r"cost of goods sold"]),
    ("pbt", [r"profit before tax", r"\bpbt\b", r"loss\)? before tax"]),
    ("net_ppe", [r"property,? plant", r"\bnet ppe\b", r"^ppe"]),
    ("inventories", [r"inventor"]),
    ("employees", [r"number of employees", r"headcount", r"^employees", r"workforce"]),
    ("revenue", [r"^revenue", r"^turnover", r"segment revenue"]),
]
COST_ITEMS = {"staff_costs", "d_and_a", "depreciation", "amortisation", "finance_costs",
              "cost_of_sales", "capex"}

INDICATORS = [
    ("rev_per_emp", "Revenue per employee", "RM"),
    ("va_per_emp", "Value added per employee", "RM"),
    ("va_per_staff_cost", "Value added per RM1 staff cost", "RM per RM1"),
    ("staff_cost_per_emp", "Average staff cost per employee", "RM"),
    ("capex_per_emp", "Capex per employee", "RM"),
    ("capital_intensity", "Capital intensity", "RM"),
    ("va_per_ppe", "Value added per RM1 fixed assets", "RM per RM1"),
    ("inv_turnover", "Inventory turnover", "times"),
]


def classify(item: str):
    s = str(item).strip().lower()
    for key, pats in ITEM_PATTERNS:
        if any(re.search(p, s) for p in pats):
            return key
    return None


def parse_year(year_cell, fy_cell, source_cell):
    """Return an absolute year (int) from 'FY2025', '2025', or 'FY-1' (relative)."""
    y = str(year_cell).strip().upper().replace(" ", "")
    m = re.search(r"(19|20)\d{2}", y)
    if m:
        return int(m.group(0))
    base = None
    for cell in (source_cell, fy_cell):
        if cell is not None and str(cell) != "nan":
            mm = re.search(r"(19|20)\d{2}", str(cell))
            if mm:
                base = int(mm.group(0)); break
    if base is None:
        return None
    if y in ("FY", "FY-0", "CURRENT"):
        return base
    mm = re.fullmatch(r"FY-(\d)", y)
    return base - int(mm.group(1)) if mm else None


def to_number(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "").replace("\u2212", "-")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        x = float(s)
    except ValueError:
        return None
    return -x if neg else x


def norm_scope(s):
    s = str(s or "Group").strip().lower()
    if "malaysia" in s:
        return "Malaysia"
    return "Group" if s in ("", "nan", "group", "consolidated") else str(s).strip().title()


def load(path):
    p = Path(path)
    if p.suffix.lower() in (".xlsx", ".xlsm"):
        raw = pd.read_excel(p, header=None)
        # template sheets have title rows; find the header row containing "Item"
        hdr = next(i for i, r in raw.iterrows() if any(str(c).strip() == "Item" for c in r))
        df = pd.read_excel(p, header=hdr)
    else:
        df = pd.read_csv(p)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def col(df, *names):
    for n in names:
        for c in df.columns:
            if c.lower().startswith(n.lower()):
                return c
    return None


def build_table(df, checks):
    c_item, c_val, c_year = col(df, "Item"), col(df, "Value"), col(df, "Year")
    c_fy, c_scope = col(df, "FY"), col(df, "Scope")
    c_src, c_restated = col(df, "Source report", "Source"), col(df, "Restated")
    c_page, c_quote = col(df, "Page"), col(df, "Quote")
    rows = []
    for _, r in df.iterrows():
        key = classify(r[c_item]) if c_item else None
        val = to_number(r[c_val]) if c_val else None
        if key is None or val is None:
            continue
        yr = parse_year(r[c_year], r[c_fy] if c_fy else None, r[c_src] if c_src else None)
        if yr is None:
            checks.append(f"Could not read year for item '{r[c_item]}' ({r[c_year]}); row ignored")
            continue
        src = r[c_src] if c_src else (r[c_fy] if c_fy else None)
        m = re.search(r"(19|20)\d{2}", str(src)) if src is not None else None
        rows.append(dict(key=key, item=r[c_item], year=yr, value=val,
                         scope=norm_scope(r[c_scope] if c_scope else None),
                         src_year=int(m.group(0)) if m else 0,
                         restated=str(r[c_restated]).strip().upper().startswith("Y") if c_restated else False,
                         page=r[c_page] if c_page else None,
                         quote=r[c_quote] if c_quote else None))
    # resolve duplicates: same key/year/scope -> latest source report wins (restated rule)
    table = {}
    for row in sorted(rows, key=lambda x: x["src_year"]):
        k = (row["key"], row["year"], row["scope"])
        if k in table and abs(table[k]["value"] - row["value"]) > 1e-9:
            checks.append(f"DECISION/RESTATED: {row['key']} {row['year']} {row['scope']}: "
                          f"{table[k]['value']:,} (report {table[k]['src_year']}) vs {row['value']:,} "
                          f"(report {row['src_year']}). Used the later report; mark 'restated'.")
        table[k] = row
    # combine separate depreciation + amortisation if no D&A total
    for (key, yr, sc) in list(table):
        if key == "depreciation" and ("d_and_a", yr, sc) not in table:
            dep = table[(key, yr, sc)]["value"]
            am = table.get(("amortisation", yr, sc), {}).get("value", 0.0)
            table[("d_and_a", yr, sc)] = dict(table[(key, yr, sc)], key="d_and_a", value=abs(dep) + abs(am),
                                               item="Depreciation + amortisation (summed)")
    return table


def get(table, key, yr, scope):
    r = table.get((key, yr, scope))
    if r is None:
        return None
    return abs(r["value"]) if key in COST_ITEMS else r["value"]


def fmt(x, dp=0):
    return "n.c." if x is None else f"{x:,.{dp}f}"


def calc_year(table, yr, emp_scope, basis, no_inv, unit_mult):
    """Return dict indicator -> {value, note, working} for one year."""
    G = "Group"
    out = {}
    E = lambda y: get(table, "employees", y, emp_scope)
    e1, e0 = E(yr), E(yr - 1)
    if basis == "average":
        avg_emp, emp_w = e1, f"average headcount reported {fmt(e1)}"
    else:
        avg_emp = (e1 + e0) / 2 if (e1 is not None and e0 is not None) else None
        emp_w = f"avg employees ({fmt(e0)} + {fmt(e1)}) / 2 = {fmt(avg_emp, 1)}"
    emp_note = None if avg_emp else ("n.c. - opening headcount missing" if e1 is not None else "Not found in documents reviewed")

    def va(scope):
        parts = {k: get(table, k, yr, scope) for k in ("pbt", "staff_costs", "d_and_a", "finance_costs")}
        missing = [k for k, v in parts.items() if v is None]
        if missing:
            return None, parts, missing
        return sum(parts.values()), parts, []

    va_g, parts_g, miss_g = va(G)
    va_e, parts_e, miss_e = va(emp_scope)
    per_emp_scope_ok = emp_scope == G or not miss_e
    va_emp_scope = va_e if emp_scope != G else va_g

    def per_emp(code, numer, numer_w, scope_needed=True):
        if not per_emp_scope_ok and scope_needed:
            out[code] = dict(value=None, note="Scope mismatch", working=f"headcount is {emp_scope}; matching {emp_scope} figures missing")
        elif numer is None:
            out[code] = dict(value=None, note="n.c. - numerator missing", working=numer_w)
        elif avg_emp is None:
            out[code] = dict(value=None, note=emp_note, working=emp_w)
        else:
            v = numer * unit_mult / avg_emp
            out[code] = dict(value=v, note=None, working=f"{numer_w} x {unit_mult:,} / {emp_w} = {fmt(v, 0)}")

    rev = get(table, "revenue", yr, emp_scope)
    per_emp("rev_per_emp", rev, f"revenue {fmt(rev)} ({emp_scope})")
    va_w = ("VA = PBT {pbt} + staff {staff_costs} + D&A {d_and_a} + finance {finance_costs}".format(
        **{k: fmt(v) for k, v in (parts_e if emp_scope != G else parts_g).items()}))
    per_emp("va_per_emp", va_emp_scope, va_w + f" = {fmt(va_emp_scope)}")
    sc = get(table, "staff_costs", yr, emp_scope)
    per_emp("staff_cost_per_emp", sc, f"staff costs {fmt(sc)}")
    cx = get(table, "capex", yr, emp_scope)
    per_emp("capex_per_emp", cx, f"purchase of PPE {fmt(cx)}")
    p1, p0 = get(table, "net_ppe", yr, emp_scope), get(table, "net_ppe", yr - 1, emp_scope)
    avg_ppe_e = (p1 + p0) / 2 if (p1 is not None and p0 is not None) else None
    per_emp("capital_intensity", avg_ppe_e, f"avg net PPE ({fmt(p0)} + {fmt(p1)}) / 2 = {fmt(avg_ppe_e, 1)}")

    # ratios (Group scope)
    sc_g = get(table, "staff_costs", yr, G)
    if va_g is None or sc_g in (None, 0):
        out["va_per_staff_cost"] = dict(value=None, note="n.c. - " + ("VA components missing: " + ", ".join(miss_g) if miss_g else "staff costs missing"), working="")
    else:
        v = va_g / sc_g
        out["va_per_staff_cost"] = dict(value=v, note=None, working=f"VA {fmt(va_g)} / staff costs {fmt(sc_g)} = {v:.2f}")
    g1, g0 = get(table, "net_ppe", yr, G), get(table, "net_ppe", yr - 1, G)
    avg_ppe = (g1 + g0) / 2 if (g1 is not None and g0 is not None) else None
    if va_g is None or not avg_ppe:
        out["va_per_ppe"] = dict(value=None, note="n.c. - " + ("opening PPE missing" if g1 is not None and g0 is None else "VA or PPE missing"), working="")
    else:
        v = va_g / avg_ppe
        out["va_per_ppe"] = dict(value=v, note=None, working=f"VA {fmt(va_g)} / avg net PPE ({fmt(g0)} + {fmt(g1)})/2 = {v:.2f}")
    if no_inv:
        out["inv_turnover"] = dict(value=None, note="not applicable", working="no meaningful stock")
    else:
        cos = get(table, "cost_of_sales", yr, G)
        i1, i0 = get(table, "inventories", yr, G), get(table, "inventories", yr - 1, G)
        if cos is None or i1 is None or i0 is None or (i1 + i0) == 0:
            out["inv_turnover"] = dict(value=None, note="n.c. - " + ("opening inventory missing" if i0 is None and i1 is not None else "figures missing"), working="")
        else:
            v = cos / ((i1 + i0) / 2)
            out["inv_turnover"] = dict(value=v, note=None, working=f"cost of sales {fmt(cos)} / avg inventory ({fmt(i0)} + {fmt(i1)})/2 = {v:.2f}x")

    va_check = None
    if va_g is not None:
        recheck = sum(parts_g.values())
        va_check = "OK" if abs(recheck - va_g) < 1e-6 else "FAIL"
    return out, dict(va_group=va_g, va_components=parts_g, va_missing=miss_g, va_reconciles=va_check,
                     avg_employees=avg_emp, employee_scope=emp_scope)


def next_free(path: Path):
    if not path.exists():
        return path
    n = 2
    while True:
        cand = path.with_name(f"{path.stem}_v{n}{path.suffix}")
        if not cand.exists():
            return cand
        n += 1


def sector_medians(dir_, sector, fy, own_code):
    vals, codes = {k: [] for k, _, _ in INDICATORS}, set()
    if not dir_:
        return None, 0
    for f in Path(dir_).rglob("*_Profile*.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        if d.get("sector") != sector or d.get("code") in codes:
            continue
        yrs = d.get("years", {})
        if str(fy) not in yrs:
            continue
        codes.add(d.get("code"))
        for k, _, _ in INDICATORS:
            v = yrs[str(fy)]["indicators"].get(k, {}).get("value")
            if v is not None:
                vals[k].append(v)
    if len(codes) < 5:
        return None, len(codes)
    return {k: (statistics.median(v) if len(v) >= 5 else None) for k, v in vals.items()}, len(codes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasheet", required=True)
    ap.add_argument("--company", required=True); ap.add_argument("--code", required=True)
    ap.add_argument("--sector", required=True); ap.add_argument("--fy", type=int, required=True)
    ap.add_argument("--name", help="ShortName for file names (CamelCase)")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--headcount-basis", choices=["yearend", "average"], default="yearend")
    ap.add_argument("--no-inventory", action="store_true")
    ap.add_argument("--unit-multiplier", type=float, default=1000.0,
                    help="RM'000 figures -> RM per employee (default 1000)")
    ap.add_argument("--scope-change-years", default="", help="comma list, e.g. 2023")
    ap.add_argument("--sector-profiles-dir")
    ap.add_argument("--first-year", type=int, help="earliest year to calculate (default FY-4)")
    a = ap.parse_args()

    checks = []
    table = build_table(load(a.datasheet), checks)
    emp_scopes = sorted({k[2] for k in table if k[0] == "employees"})
    emp_scope = "Malaysia" if emp_scopes == ["Malaysia"] else "Group"
    if len(emp_scopes) > 1:
        checks.append(f"DECISION: headcount reported in more than one scope {emp_scopes}; used Group. Confirm via Rules tab.")
    first = a.first_year or a.fy - 4
    scope_change = {int(y) for y in a.scope_change_years.split(",") if y.strip()}

    years = {}
    for yr in range(first, a.fy + 1):
        ind, meta = calc_year(table, yr, emp_scope, a.headcount_basis, a.no_inventory, a.unit_multiplier)
        meta["scope_change"] = yr in scope_change
        if meta["va_reconciles"] == "FAIL":
            checks.append(f"VA does not reconcile in {yr}")
        years[str(yr)] = dict(indicators=ind, meta=meta)

    # large-change check (>50%) on FY vs FY-1 -> decision trigger
    for k, label, _ in INDICATORS:
        v1 = years[str(a.fy)]["indicators"][k]["value"]
        v0 = years.get(str(a.fy - 1), {}).get("indicators", {}).get(k, {}).get("value")
        if v1 is not None and v0 not in (None, 0) and abs(v1 / v0 - 1) > 0.5:
            checks.append(f"DECISION: {label} changed {100*(v1/v0-1):+.1f}% FY{a.fy} vs FY{a.fy-1} (>50%). Check scope/definition.")

    medians, n_peers = sector_medians(a.sector_profiles_dir, a.sector, a.fy, a.code)
    name = a.name or re.sub(r"[^A-Za-z0-9]", "", a.company.replace("Berhad", "").replace("Bhd", ""))
    base = f"{a.code}_{name}_FY{a.fy}_Profile"
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)

    result = dict(company=a.company, code=a.code, sector=a.sector, fy=a.fy, employee_scope=emp_scope,
                  headcount_basis=a.headcount_basis, label="Value added = analyst-calculated nominal proxy",
                  sector_median_status="pending" if medians is None else f"median of {n_peers} companies",
                  sector_median=medians, years=years, checks=checks)
    jpath = next_free(out / f"{base}.json")
    jpath.write_text(json.dumps(result, indent=2, default=str))

    # Excel in template columns
    rows = []
    for k, label, unit in INDICATORS:
        c = years[str(a.fy)]["indicators"][k]; p = years.get(str(a.fy - 1), {}).get("indicators", {}).get(k, {})
        v1, v0 = c["value"], p.get("value")
        ch = None if v1 is None or v0 in (None, 0) else 100 * (v1 / v0 - 1)
        per_emp = k in ("rev_per_emp", "va_per_emp", "staff_cost_per_emp", "capex_per_emp", "capital_intensity")
        scope_lbl = ("Malaysia operations" if emp_scope == "Malaysia" else "Group") if per_emp else "Group"
        med = (medians or {}).get(k)
        rows.append({"Company": a.company, "Code": a.code, "Sector": a.sector, "FY": f"FY{a.fy}",
                     "Indicator": f"{label} ({unit})",
                     "FY value": round(v1, 2) if v1 is not None else (c["note"] or "n.c."),
                     "FY-1 value": round(v0, 2) if v0 is not None else (p.get("note") or "n.c."),
                     "Change %": round(ch, 1) if ch is not None else "n.c.",
                     "Sector median": round(med, 2) if med is not None else "pending",
                     "Scope": scope_lbl, "Working": c["working"]})
    allyrs = [{"Year": y, "Indicator": dict((k, l) for k, l, _ in INDICATORS)[k],
               "Value": v["value"], "Note": v["note"], "Working": v["working"],
               "Scope change": d["meta"]["scope_change"]}
              for y, d in years.items() for k, v in d["indicators"].items()]
    xpath = next_free(out / f"{base}.xlsx")
    with pd.ExcelWriter(xpath) as w:
        pd.DataFrame(rows).to_excel(w, sheet_name="Profile", index=False)
        pd.DataFrame(allyrs).to_excel(w, sheet_name="AllYears", index=False)
        pd.DataFrame({"Check": checks or ["No issues found"]}).to_excel(w, sheet_name="Checks", index=False)
    for p in (jpath, xpath):
        assert p.exists() and p.stat().st_size > 0, f"save failed: {p}"
    print(json.dumps({"saved": [str(jpath), str(xpath)], "employee_scope": emp_scope,
                      "sector_median": result["sector_median_status"], "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
