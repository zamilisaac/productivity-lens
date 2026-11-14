#!/usr/bin/env python3
"""
Productivity Lens - Distance to Frontier (Playbook Module 3B).

Reads every *_Profile*.json in the sector (from pl_profile.py) and produces:
  - the company's DTF file (Mode 1 frontier scores, or Mode 2 five-year progress)
  - the sector panel  03_Working/_Sector/[Sector]_Frontier.xlsx (+ .json)
  - a list of earlier companies to set to FRONTIER_UPDATE if frontier/floor moved

Usage:
  python pl_dtf.py --code 5306 --profiles-dir 03_Working/ --sector "Consumer Products & Services" \
      --out-dir 03_Working/5306_FarmFresh/ --sector-dir 03_Working/_Sector/ [--start 2022 --end 2026]

No-ranking rules are built in: companies are only ever listed alphabetically,
the frontier is a percentile, and no rank or position is output.
"""
import argparse, json, re, statistics
from pathlib import Path

import numpy as np
import pandas as pd

DTF_IND = [
    ("va_per_emp", "Value added per employee"),
    ("rev_per_emp", "Revenue per employee"),
    ("va_per_staff_cost", "Value added per RM1 staff cost"),
    ("va_per_ppe", "Value added per RM1 fixed assets"),
    ("inv_turnover", "Inventory turnover"),
]
BANNED = re.compile(r"\b(top|best|leader|leading|ranked|rank|outperform\w*|laggard|worst)\b", re.I)


def next_free(path: Path):
    if not path.exists():
        return path
    n = 2
    while (c := path.with_name(f"{path.stem}_v{n}{path.suffix}")).exists():
        n += 1
    return c


def load_profiles(dir_, sector):
    """Latest profile per company code in the sector (highest _vN wins)."""
    best = {}
    for f in Path(dir_).rglob("*_Profile*.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        if d.get("sector") != sector:
            continue
        m = re.search(r"_v(\d+)\.json$", f.name)
        ver = int(m.group(1)) if m else 1
        code = d["code"]
        if code not in best or (d["fy"], ver) > (best[code][0]["fy"], best[code][1]):
            best[code] = (d, ver)
    return {c: v[0] for c, v in best.items()}


def value(p, yr, k):
    y = p["years"].get(str(yr))
    if not y or y["meta"].get("scope_change"):
        return None
    ind = y["indicators"].get(k, {})
    return ind.get("value")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", required=True)
    ap.add_argument("--profiles-dir", required=True)
    ap.add_argument("--sector", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--sector-dir", required=True)
    ap.add_argument("--start", type=int, default=2022)
    ap.add_argument("--end", type=int, default=2026)
    ap.add_argument("--min-companies", type=int, default=5)
    ap.add_argument("--min-company-years", type=int, default=20)
    a = ap.parse_args()

    profs = load_profiles(a.profiles_dir, a.sector)
    if a.code not in profs:
        raise SystemExit(f"No profile JSON for {a.code} in sector '{a.sector}' under {a.profiles_dir}")
    years = list(range(a.start, a.end + 1))
    me = profs[a.code]
    notes = []

    scopes = sorted({p.get("employee_scope", "Group") for p in profs.values()})
    if len(scopes) > 1:
        notes.append(f"Mixed headcount scopes in panel {scopes}: per-employee indicators are not like-for-like. Raise a decision.")

    company_years = sum(1 for p in profs.values() for y in years if value(p, y, "va_per_emp") is not None)
    mode = 1 if (len(profs) >= a.min_companies and company_years >= a.min_company_years) else 2

    # ---------- sector panel (always saved, alphabetical)
    panel_rows = []
    for code in sorted(profs, key=lambda c: profs[c]["company"].lower()):
        p = profs[code]
        for y in years:
            row = {"Company": p["company"], "Code": code, "Year": y}
            for k, label in DTF_IND:
                row[label] = value(p, y, k)
            panel_rows.append(row)
    panel = pd.DataFrame(panel_rows)

    frontier = {}
    if mode == 1:
        for k, label in DTF_IND:
            vals = panel[label].dropna().to_numpy(dtype=float)
            if len(vals) >= 5:
                frontier[k] = {"frontier_p90": float(np.percentile(vals, 90, method="linear")),
                               "floor_p10": float(np.percentile(vals, 10, method="linear")),
                               "n": int(len(vals))}

    def score(k, v):
        f = frontier.get(k)
        if v is None or not f or f["frontier_p90"] == f["floor_p10"]:
            return None
        s = (v - f["floor_p10"]) / (f["frontier_p90"] - f["floor_p10"]) * 100
        return max(0.0, min(100.0, s))

    def composite(p, y):
        sc = [score(k, value(p, y, k)) for k, _ in DTF_IND]
        sc = [s for s in sc if s is not None]
        return (sum(sc) / len(sc)) if len(sc) >= 4 else None

    out = dict(company=me["company"], code=a.code, sector=a.sector, fy=me["fy"], mode=mode,
               panel_companies=len(profs), panel_company_years=company_years,
               label="Value added = analyst-calculated nominal proxy", notes=notes)

    if mode == 1:
        out["title"] = "Distance to Frontier"
        out["frontier_definition"] = "Frontier = 90th percentile of sector company-years; floor = 10th percentile; not a ranking."
        out["frontier"] = frontier
        out["indicators"] = {}
        for k, label in DTF_IND:
            out["indicators"][k] = {"label": label,
                                    "values": {y: value(me, y, k) for y in years},
                                    "scores": {y: score(k, value(me, y, k)) for y in years}}
        comp = {y: composite(me, y) for y in years}
        med = {}
        for y in years:
            cs = [c for c in (composite(p, y) for p in profs.values()) if c is not None]
            med[y] = statistics.median(cs) if cs else None
        out["composite"] = comp
        out["sector_median_composite"] = med
        valid = [y for y in years if comp[y] is not None]
        if len(valid) >= 2:
            d = comp[valid[-1]] - comp[valid[0]]
            out["direction"] = "stable" if abs(d) <= 5 else ("closing" if d > 0 else "widening")
            out["change_points"] = d
            out["direction_basis"] = f"FY{valid[0]}->FY{valid[-1]}"
        else:
            out["direction"] = "n.c."
        last = {k: out["indicators"][k]["scores"][a.end] for k, _ in DTF_IND}
        ranked_low = sorted([(v, k) for k, v in last.items() if v is not None])[:2]
        out["gap_drivers"] = [dict(DTF_IND)[k] for _, k in ranked_low]
        if comp.get(a.end) is None:
            notes.append(f"Composite FY{a.end} not calculated: fewer than 4 applicable indicators. Show indicator scores only.")
    else:
        out["title"] = "Five-year progress"
        out["panel_label"] = "Five-year progress \u00b7 sector frontier pending"
        out["indicators"] = {}
        for k, label in DTF_IND:
            base = value(me, a.start, k)
            idx = {y: (None if base in (None, 0) or value(me, y, k) is None else 100 * value(me, y, k) / base)
                   for y in years}
            out["indicators"][k] = {"label": label, "values": {y: value(me, y, k) for y in years}, "index": idx}
            if base is None:
                notes.append(f"{label}: FY{a.start} base missing, index not calculated.")
        vi = out["indicators"]["va_per_emp"]["index"].get(a.end)
        out["headline_index"] = vi

    missing_years = [y for y in years if me["years"].get(str(y)) is None]
    if len([y for y in years if value(me, y, "va_per_emp") is not None]) < 3:
        notes.append("Fewer than 3 years available: no trend can be shown.")
    if missing_years:
        notes.append(f"Years with no data: {missing_years}")

    # ---------- frontier change detection
    sector_slug = re.sub(r"[^A-Za-z0-9]+", "", a.sector.title())
    sdir = Path(a.sector_dir); sdir.mkdir(parents=True, exist_ok=True)
    prev_files = sorted(sdir.glob(f"{sector_slug}_Frontier*.json"), key=lambda p: p.stat().st_mtime)
    to_update = []
    if prev_files:
        prev = json.loads(prev_files[-1].read_text())
        moved = any(abs(prev.get("frontier", {}).get(k, {}).get(m, 0) - frontier.get(k, {}).get(m, 0)) > 1e-9
                    for k, _ in DTF_IND for m in ("frontier_p90", "floor_p10"))
        mode_changed = prev.get("mode") != mode
        if moved or mode_changed:
            to_update = sorted([c for c in prev.get("codes", []) if c != a.code])
    out["frontier_update_codes"] = to_update

    # ---------- save
    assert not BANNED.search(" ".join(notes)), "rank word in notes"
    name = Path(a.out_dir).name.split("_", 1)[-1] if "_" in Path(a.out_dir).name else a.code
    od = Path(a.out_dir); od.mkdir(parents=True, exist_ok=True)
    jpath = next_free(od / f"{a.code}_{name}_FY{me['fy']}_DTF.json")
    jpath.write_text(json.dumps(out, indent=2, default=str))
    xpath = next_free(od / f"{a.code}_{name}_FY{me['fy']}_DTF.xlsx")
    rows = []
    for k, d in out["indicators"].items():
        for y in years:
            rows.append({"Indicator": d["label"], "Year": y, "Value": d["values"][y],
                         ("Score (0-100)" if mode == 1 else "Index (FY%d=100)" % a.start):
                         (d["scores"][y] if mode == 1 else d["index"][y])})
    with pd.ExcelWriter(xpath) as w:
        pd.DataFrame(rows).to_excel(w, sheet_name="DTF", index=False)
        if mode == 1:
            pd.DataFrame({"Year": years, "Composite": [out["composite"][y] for y in years],
                          "Sector median composite": [out["sector_median_composite"][y] for y in years]}
                         ).to_excel(w, sheet_name="Trend", index=False)
        pd.DataFrame({"Note": notes or ["none"]}).to_excel(w, sheet_name="Notes", index=False)

    sj = next_free(sdir / f"{sector_slug}_Frontier.json")
    sj.write_text(json.dumps({"sector": a.sector, "mode": mode, "years": years, "frontier": frontier,
                              "codes": sorted(profs), "company_years": company_years}, indent=2))
    sx = next_free(sdir / f"{sector_slug}_Frontier.xlsx")
    with pd.ExcelWriter(sx) as w:
        panel.to_excel(w, sheet_name="Panel (alphabetical)", index=False)
        pd.DataFrame([{"Indicator": dict(DTF_IND)[k], **v} for k, v in frontier.items()] or
                     [{"Indicator": "frontier pending", "frontier_p90": None, "floor_p10": None, "n": None}]
                     ).to_excel(w, sheet_name="Frontier", index=False)
    saved = [jpath, xpath, sj, sx]
    for p in saved:
        assert p.exists() and p.stat().st_size > 0, f"save failed: {p}"
    print(json.dumps({"mode": mode, "title": out["title"], "saved": [str(p) for p in saved],
                      "composite_end": out.get("composite", {}).get(a.end) if mode == 1 else None,
                      "direction": out.get("direction"), "gap_drivers": out.get("gap_drivers"),
                      "frontier_update_codes": to_update, "notes": notes}, indent=2, default=str))


if __name__ == "__main__":
    main()
