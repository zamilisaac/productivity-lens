#!/usr/bin/env python3
"""
Productivity Lens - initiative classifier (Playbook v1.12, Module 2A).

Claude answers fact questions F1-F6 for every candidate initiative (see references/rubric.md).
This script turns those answers into the Playbook labels, the same way every time:
counted / not counted (+ reason), Tier, Grade, Evidence type, lesson and headline eligibility,
plus warnings when the quote and the answers do not agree.

Commands
  run      answers file -> Initiatives workbook (Initiatives, Not counted, Decisions sheets) + JSON summary
  compare  first answers vs an independent second pass -> disagreements to send to Decisions
  test     answers with expected labels (gold set) -> agreement report; exit 1 if below --min

Input: .csv or .xlsx (first sheet) with the columns in ANSWER_COLS (extra columns are kept).
"""
import argparse
import json
import re
import sys
from pathlib import Path

PLAYBOOK = "v1.12"

ANSWER_COLS = ["id", "company", "code", "fy", "initiative", "page", "source", "quote",
               "category", "status", "result_kind", "input", "figure", "area"]
OPTIONAL_COLS = ["type", "what_they_did", "investment", "reported_result", "where",
                 "uncertain", "uncertain_reason", "rule", "rule_outcome", "result_year"]

ALLOWED = {
    "source": {"AR", "SR", "both"},
    "category": {"operations", "csr", "marketing", "acquisition", "new_market",
                 "pricing_product", "hr_benefit", "governance"},
    "status": {"achieved", "planned"},
    "result_kind": {"output_per_input", "time", "cost", "quality_yield", "downtime",
                    "input_per_unit", "input_saving", "utilisation", "capacity", "investment_scale",
                    "revenue_profit", "counts_scale", "environmental_only",
                    "compliance_award", "training_hours", "none"},
    "input": {"people", "machine_time", "materials", "energy", "water", "space", "stock", "none"},
    "figure": {"before_after", "single_impact", "none"},
    "area": {"line_machinery", "automation_digital", "process_layout", "capacity_existing_site",
             "consolidation", "workforce_skills", "distribution_restructure", "quality_yield",
             "supply_chain_logistics", "new_site", "resource"},
}

TIER = {"line_machinery": 1, "automation_digital": 1, "process_layout": 1,
        "capacity_existing_site": 1, "consolidation": 1, "workforce_skills": 1,
        "distribution_restructure": 1, "quality_yield": 1,
        "supply_chain_logistics": 2, "new_site": 2, "resource": 3}

NEVER = {"revenue_profit": "revenue, sales or profit",
         "counts_scale": "store, outlet, customer, asset or herd counts (scale only)",
         "compliance_award": "certification, award or compliance record",
         "training_hours": "training hours"}
OPERATING = {"time", "cost", "quality_yield", "downtime", "input_per_unit", "input_saving", "utilisation"}
PRODUCTIVITY = {"output_per_input"}
MEASURED = OPERATING | PRODUCTIVITY
CATEGORY_TXT = {"csr": "CSR or community", "marketing": "branding or marketing",
                "acquisition": "acquisition or disposal", "new_market": "new market or country entry",
                "pricing_product": "pricing or product launch", "hr_benefit": "HR benefit",
                "governance": "governance or reporting"}

# Words in the quote that contradict an answer -> warning for the reviewer
WARN_WORDS = [
    (r"\b(will|plans? to|planned|target(?:s|ed)?|expected|aims? to|to be commissioned|under construction)\b",
     "status", lambda a: a["status"] == "achieved", "quote has planning words but status = achieved"),
    (r"\b(tco2e?|co2|carbon|emission|renewable|greenhouse)\b",
     "result_kind", lambda a: a["result_kind"] in MEASURED | {"capacity"},
     "quote has environmental terms; check the result is operating, not environmental only"),
    (r"\b(iso ?\d{3,5}|certif\w*|award\w*|accredit\w*|halal|haccp|gmp)\b",
     "result_kind", lambda a: a["result_kind"] in MEASURED,
     "quote mentions certification/award; check the result is not a compliance record"),
    (r"\b(revenue|sales|turnover|profit|margin|market share)\b",
     "result_kind", lambda a: a["result_kind"] in MEASURED | {"capacity"},
     "quote mentions revenue/sales/profit; check the result is not revenue only"),
    (r"\b(acquir\w*|acquisition|purchase of|bought)\b",
     "category", lambda a: a["category"] == "operations",
     "quote mentions an acquisition; check category"),
]


def norm(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.lower() in {"nan", "none"} and s != "none" else s


def load(path):
    p = Path(path)
    if p.suffix.lower() in {".xlsx", ".xlsm"}:
        import openpyxl
        ws = openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0]
        rows = list(ws.iter_rows(values_only=True))
        head = [norm(h) for h in rows[0]]
        data = [{head[i]: norm(r[i]) for i in range(len(head)) if head[i]} for r in rows[1:]
                if any(c not in (None, "") for c in r)]
    else:
        import csv
        with open(p, newline="", encoding="utf-8-sig") as f:
            data = [{k.strip(): norm(v) for k, v in r.items() if k} for r in csv.DictReader(f)]
    return data


def validate(rows):
    errors = []
    seen = set()
    for n, r in enumerate(rows, 2):
        for c in ANSWER_COLS:
            if not r.get(c):
                errors.append(f"row {n} ({r.get('id','?')}): missing '{c}'")
        for c, ok in ALLOWED.items():
            v = r.get(c, "")
            if v and v not in ok:
                errors.append(f"row {n} ({r.get('id','?')}): {c}='{v}' not allowed ({', '.join(sorted(ok))})")
        if r.get("id") in seen:
            errors.append(f"row {n}: duplicate id '{r.get('id')}'")
        seen.add(r.get("id"))
        if r.get("rule_outcome") and r["rule_outcome"] not in {"pass", "fail"}:
            errors.append(f"row {n}: rule_outcome must be pass or fail")
    return errors


def classify(a):
    """Apply Playbook Module 2A to one row of answers. Returns a dict of labels."""
    out = {"counted": "Y", "fail_reason": "", "tier": TIER[a["area"]], "grade": "",
           "evidence_type": "", "lesson_eligible": "N", "headline_role": "", "warnings": [],
           "decision_needed": ""}
    rk, fig, area = a["result_kind"], a["figure"], a["area"]
    quantified = fig != "none"

    def fail(reason):
        if out["counted"] == "Y":
            out["counted"], out["fail_reason"] = "N", reason

    # Test question order follows the Playbook: exclusions, achieved, operating result, input link,
    # then the stricter rules for particular areas.
    if a["category"] != "operations":
        fail(f"excluded: {CATEGORY_TXT[a['category']]}")
    if a["status"] == "planned":
        fail("planned, not yet achieved")
    if rk in NEVER:
        fail(f"never an operating result: {NEVER[rk]}")
    if rk == "environmental_only":
        fail("result in environmental or social terms only")
    if a["input"] == "none":
        fail("no link to an input (people, machine time, materials, energy, water, space, stock)")
    operating_measure = rk in MEASURED and quantified
    if a["source"] == "SR" and not operating_measure:
        fail("sustainability pages only, and the quote has no operating measure")
    if area == "resource" and not (rk in {"cost", "input_per_unit", "input_saving"} and quantified):
        fail("Tier 3 without a quantified cost or input saving")
    if area == "new_site" and not operating_measure:
        fail("new site without an operating result")
    if area == "quality_yield" and not (rk in {"quality_yield", "downtime"} and quantified):
        fail("quality item without a measured defect, yield or downtime figure")
    if area == "distribution_restructure" and rk not in MEASURED:
        fail("distribution item without an operating measure")

    # Evidence type: highest the quote supports; capacity or scale alone is an Enabler
    if quantified and rk in PRODUCTIVITY:
        out["evidence_type"] = "Productivity result"
    elif quantified and rk in OPERATING:
        out["evidence_type"] = "Operating result"
    else:
        out["evidence_type"] = "Enabler"

    # Grade
    if quantified and (rk in MEASURED or rk == "capacity"):
        out["grade"] = "A"
    elif quantified and rk == "investment_scale":
        out["grade"] = "B"
    else:
        out["grade"] = "C"

    # Rules tab override (recorded, never silent)
    if a.get("rule") and a.get("rule_outcome"):
        before = out["counted"]
        out["counted"] = "Y" if a["rule_outcome"] == "pass" else "N"
        if out["counted"] == "N":
            out["fail_reason"] = f"{a['rule']}: {out['fail_reason'] or 'fails under the rule'}"
        else:
            out["fail_reason"] = ""
        if before != out["counted"]:
            out["warnings"].append(f"{a['rule']} changed the engine result ({before} -> {out['counted']})")

    if out["counted"] == "Y":
        if out["grade"] == "A" and out["evidence_type"] != "Enabler" and out["tier"] in (1, 2):
            out["lesson_eligible"] = "Y"
        # Playbook headline hierarchy (Module 4): Tier 1, Grade A only
        if out["tier"] == 1 and out["grade"] == "A":
            if out["evidence_type"] == "Productivity result":
                out["headline_role"] = "1 Productivity result"
            elif out["evidence_type"] == "Operating result":
                out["headline_role"] = "2 Operating result"
            elif rk == "capacity":
                out["headline_role"] = "3 capacity Enabler (only with VA per employee beside it)"
        # Distribution items: Playbook example asks for the cost in RM
        if area == "distribution_restructure" and rk == "cost" and not quantified:
            out["warnings"].append("distribution cost not stated in RM; confirm before using as a result")
            out["decision_needed"] = "Y"

    # Quote checks
    q = a.get("quote", "")
    for pat, field, cond, msg in WARN_WORDS:
        if re.search(pat, q, re.I) and cond(a):
            out["warnings"].append(msg)
    if quantified and not re.search(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|million|billion|double[ds]?|half|halved)\b", q, re.I):
        out["warnings"].append("figure answered as quantified but the quote has no number")
    rr = a.get("reported_result", "")
    if rr:
        missing = [n for n in re.findall(r"\d[\d,]*(?:\.\d+)?", rr)
                   if n.replace(",", "") not in re.sub(r"(?<=\d),(?=\d)", "", q)]
        if missing:
            out["warnings"].append(f"reported result numbers not in quote: {', '.join(missing)}")
    if a.get("uncertain", "").upper() == "Y":
        out["decision_needed"] = "Y"
        out["warnings"].append(f"uncertain: {a.get('uncertain_reason') or 'no reason given'}")
    if out["warnings"] and out["counted"] == "Y" and out["lesson_eligible"] == "Y":
        out["decision_needed"] = "Y"
    return out


def run_rows(rows):
    res = []
    for r in rows:
        c = classify(r)
        res.append({**r, **{k: (v if not isinstance(v, list) else " | ".join(v)) for k, v in c.items()}})
    return res


INIT_COLS = ["company", "code", "sector", "fy", "initiative", "type", "tier", "grade", "evidence_type",
             "where", "what_they_did", "investment", "reported_result", "page", "quote",
             "lesson_eligible", "headline_role", "warnings", "id"]
NC_COLS = ["initiative", "fail_reason", "page", "quote", "id"]
DEC_COLS = ["id", "initiative", "page", "counted", "tier", "grade", "evidence_type", "warnings", "quote"]
ANS_COLS = ANSWER_COLS + ["uncertain", "uncertain_reason", "rule", "rule_outcome"]


def write_xlsx(path, res):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    sheets = [("Initiatives", INIT_COLS, [r for r in res if r["counted"] == "Y"]),
              ("Not counted", NC_COLS, [r for r in res if r["counted"] == "N"]),
              ("Decisions", DEC_COLS, [r for r in res if r["decision_needed"] == "Y"]),
              ("Answers", ANS_COLS, res)]
    for i, (name, cols, data) in enumerate(sheets):
        ws = wb.active if i == 0 else wb.create_sheet()
        ws.title = name
        ws.append(cols)
        for c in ws[1]:
            c.font = Font(bold=True)
        for r in data:
            ws.append([r.get(c, "") for c in cols])
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
    wb.save(path)


def summary(res):
    counted = [r for r in res if r["counted"] == "Y"]
    by = lambda k, data: {str(v): sum(1 for r in data if str(r[k]) == str(v)) for v in sorted({str(r[k]) for r in data})}
    return {"playbook": PLAYBOOK, "candidates": len(res), "counted": len(counted),
            "not_counted": len(res) - len(counted),
            "tier": by("tier", counted), "grade": by("grade", counted),
            "evidence_type": by("evidence_type", counted),
            "lesson_eligible": sum(1 for r in counted if r["lesson_eligible"] == "Y"),
            "decisions": sum(1 for r in res if r["decision_needed"] == "Y"),
            "fail_reasons": by("fail_reason", [r for r in res if r["counted"] == "N"]),
            "enough_for_story": sum(1 for r in counted if r["lesson_eligible"] == "Y") >= 3}


def cmd_run(a):
    rows = load(a.answers)
    errs = validate(rows)
    if errs:
        print("Answer file has errors - fix them first:\n  " + "\n  ".join(errs[:50]))
        return 2
    res = run_rows(rows)
    out = Path(a.out)
    write_xlsx(out, res)
    s = summary(res)
    out.with_suffix(".summary.json").write_text(json.dumps(s, indent=2, ensure_ascii=False))
    print(json.dumps(s, indent=2, ensure_ascii=False))
    if not s["enough_for_story"]:
        print("\nFewer than three lesson-eligible initiatives: read the FY-2, then FY-4 reports (Playbook 2A).")
    return 0


FACTS = ["category", "status", "result_kind", "input", "figure", "area", "source"]


def cmd_compare(a):
    first = {r["id"]: r for r in load(a.first)}
    second = {r["id"]: r for r in load(a.second)}
    diffs = []
    for i, r2 in second.items():
        r1 = first.get(i)
        if not r1:
            diffs.append({"id": i, "field": "-", "first": "missing", "second": "present"})
            continue
        for f in FACTS:
            if r1.get(f) != r2.get(f):
                diffs.append({"id": i, "initiative": r1.get("initiative", ""), "field": f,
                              "first": r1.get(f), "second": r2.get(f)})
        c1, c2 = classify(r1), classify(r2)
        for k in ["counted", "tier", "grade", "evidence_type", "lesson_eligible"]:
            if c1[k] != c2[k]:
                diffs.append({"id": i, "initiative": r1.get("initiative", ""), "field": f"=> {k}",
                              "first": c1[k], "second": c2[k]})
    print(json.dumps({"checked": len(second), "disagreements": diffs}, indent=2, ensure_ascii=False))
    return 1 if any(d["field"].startswith("=>") for d in diffs) else 0


EXPECT = {"counted": "expected_counted", "tier": "expected_tier", "grade": "expected_grade",
          "evidence_type": "expected_evidence_type"}


def cmd_test(a):
    rows = load(a.gold)
    errs = validate(rows)
    if errs:
        print("Gold set has errors:\n  " + "\n  ".join(errs[:50]))
        return 2
    total, agree, mism = {}, {}, []
    for r in rows:
        c = classify(r)
        for k, col in EXPECT.items():
            exp = r.get(col, "")
            if not exp or (k != "counted" and r.get("expected_counted") == "N"):
                continue
            got = str(c[k])
            total[k] = total.get(k, 0) + 1
            if got.lower() == exp.lower():
                agree[k] = agree.get(k, 0) + 1
            else:
                mism.append({"id": r["id"], "initiative": r.get("initiative", ""), "label": k,
                             "expected": exp, "got": got, "fail_reason": c["fail_reason"]})
    rate = {k: round(100 * agree.get(k, 0) / n, 1) for k, n in total.items()}
    rep = {"gold_rows": len(rows), "agreement_pct": rate, "mismatches": mism}
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    if a.out:
        Path(a.out).write_text(json.dumps(rep, indent=2, ensure_ascii=False))
    worst = min(rate.values()) if rate else 0
    return 0 if worst >= a.min else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("answers"); r.add_argument("--out", required=True)
    c = sub.add_parser("compare"); c.add_argument("first"); c.add_argument("second")
    t = sub.add_parser("test"); t.add_argument("gold"); t.add_argument("--min", type=float, default=95.0)
    t.add_argument("--out")
    a = ap.parse_args()
    sys.exit({"run": cmd_run, "compare": cmd_compare, "test": cmd_test}[a.cmd](a))


if __name__ == "__main__":
    main()
