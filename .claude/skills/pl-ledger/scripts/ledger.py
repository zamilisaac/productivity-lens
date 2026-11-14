#!/usr/bin/env python3
"""
Productivity Lens - Ledger and Rules manager (Playbook: File intake, Ledger, Rules tab).

Works on the Templates workbook (.xlsx, sheets 'Ledger' and 'Rules') or on CSV
copies (e.g. exported from the Google Sheet, or 01_Register/_ledger_pending.csv).
Every change is printed as {"sheet", "row", "values"} so it can be mirrored to
Google Sheets with the Sheets connector.

Commands (all take --book PATH.xlsx  or  --ledger-csv PATH [--rules-csv PATH]):
  init                                   add Ledger/Rules sheets if missing
  check   --file F                       what to do with a report file (new/done/resume/skip/duplicate)
  add     --file F --company C --code X --fy 2026 --doctype AR [--sector S] [--intake READY]
  update  --code X --fy 2026 [--file F] --set "Pipeline status=EXTRACTED" --set "Last module done=EXTRACT" [--redo]
  fail    --code X --fy 2026 --reason "..."          (FAILED, Attempts+1; PARKED after 2)
  frontier-update --codes 9001,9002 --fy 2026        (set FRONTIER_UPDATE)
  queue   [--playbook v1.8]                          what is new / part-done / awaiting / done / skipped
  decisions                                          rows awaiting decisions with answers filled in
  rules   [--find TEXT]                              list rules (search situation/rule text)
  add-rule --situation S --rule R [--example E] [--source decision|review] [--test]
  md5     FILES...
"""
import argparse, csv, datetime as dt, hashlib, json, re, sys
from pathlib import Path

LEDGER_COLS = ["Drive file ID / local path", "File name", "Company", "Code", "FY", "Doc type", "Size MB", "MD5",
               "Intake status", "Pipeline status", "Last module done", "Open decisions", "Decisions",
               "Rules applied", "Output files", "Saved to", "Playbook version", "Attempts", "Date updated", "Notes"]
RULES_COLS = ["Rule ID", "Situation", "Rule", "Example (company, page)", "Date", "Source (decision / review)"]
INTAKE = {"READY", "PREPARED", "SKIPPED_TOO_LARGE", "SKIPPED_UNREADABLE", "SKIPPED_NOT_REPORT", "DUPLICATE"}
PIPE = ["NEW", "EXTRACTED", "PROFILED", "CONTENT", "AWAITING_DECISIONS", "APPROVED", "SPOTLIGHT", "AUDITED",
        "SNAPSHOTS", "BM", "EMAILED", "COMPLETE", "VERIFIED", "PUBLISHED"]
SPECIAL = {"FAILED", "PARKED", "FRONTIER_UPDATE"}
DONE = {"COMPLETE", "VERIFIED", "PUBLISHED"}
# module after "Last module done" -> where to resume
NEXT = {"": "PREP", "PREP": "EXTRACT", "EXTRACT": "PROFILE", "PROFILE": "DTF", "DTF": "AUDIT 1-3",
        "AUDIT 1-3": "CONTENT", "CONTENT": "DECISIONS", "DECISIONS": "SPOTLIGHT", "SPOTLIGHT": "AUDIT 4-6",
        "AUDIT 4-6": "SNAPSHOTS", "SNAPSHOTS": "BM", "BM": "EMAIL", "EMAIL": "REVIEW"}
TODAY = dt.date.today().isoformat()


# ------------------------------------------------------------------ storage
class Store:
    def __init__(self, a, sheet, wb=None):
        self.sheet, self.changes = sheet, []
        cols = LEDGER_COLS if sheet == "Ledger" else RULES_COLS
        self.cols = cols
        if a.book:
            import openpyxl
            self.kind, self.path = "xlsx", Path(a.book)
            self.wb = wb or openpyxl.load_workbook(self.path)
            if sheet not in self.wb.sheetnames:
                ws = self.wb.create_sheet(sheet)
                ws["A1"] = f"{sheet.upper()} — Productivity Lens"
                ws["A2"] = ("One row per report file. Source of truth for what is done. Updated after every module."
                            if sheet == "Ledger" else
                            "Judgement rules from approved decisions and reviews. Read before every run; rules outrank Playbook defaults.")
                for i, c in enumerate(cols, start=1):
                    ws.cell(row=4, column=i, value=c)
                self.changes.append({"sheet": sheet, "row": 4, "values": "header created"})
            self.ws = self.wb[sheet]
            self.hdr = next(r for r in range(1, 15) if self.ws.cell(r, 1).value == cols[0])
            self.head = [self.ws.cell(self.hdr, c).value for c in range(1, self.ws.max_column + 1)]
            for c in cols:   # add any missing columns at the end
                if c not in self.head:
                    self.head.append(c); self.ws.cell(self.hdr, len(self.head), c)
            self.rows = []
            for r in range(self.hdr + 1, self.ws.max_row + 1):
                vals = {h: self.ws.cell(r, i + 1).value for i, h in enumerate(self.head) if h}
                if any(v not in (None, "") for v in vals.values()):
                    self.rows.append(dict(_row=r, **{k: ("" if v is None else v) for k, v in vals.items()}))
        else:
            self.kind = "csv"
            self.path = Path(a.ledger_csv if sheet == "Ledger" else (a.rules_csv or Path(a.ledger_csv).with_name("_rules_pending.csv")))
            self.rows = []
            if self.path.exists():
                with open(self.path, newline="", encoding="utf-8") as f:
                    for i, r in enumerate(csv.DictReader(f), start=2):
                        self.rows.append(dict(_row=i, **r))
            self.head = cols

    def put(self, row, values):
        values = {k: v for k, v in values.items() if k != "_row"}
        if row is None:
            row = dict(_row=(max([r["_row"] for r in self.rows], default=(self.hdr if self.kind == "xlsx" else 1)) + 1))
            self.rows.append(row)
        row.update(values)
        if self.kind == "xlsx":
            for k, v in values.items():
                self.ws.cell(row["_row"], self.head.index(k) + 1, v)
        self.changes.append({"sheet": self.sheet, "row": row["_row"], "values": values})
        return row

    def save(self):
        if not self.changes:
            return
        if self.kind == "xlsx":
            self.wb.save(self.path)
        else:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=self.head, extrasaction="ignore")
                w.writeheader()
                for r in sorted(self.rows, key=lambda x: x["_row"]):
                    w.writerow(r)
        assert self.path.exists() and self.path.stat().st_size > 0


def md5(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def fyn(x):
    m = re.search(r"(19|20)\d{2}", str(x))
    return m.group(0) if m else str(x)


def find(L, code=None, fy=None, file=None, md=None):
    hits = []
    for r in L.rows:
        if file and (str(r.get("Drive file ID / local path")) == str(file) or r.get("File name") == Path(file).name):
            hits.append(r); continue
        if md and r.get("MD5") == md:
            hits.append(r); continue
        if code and str(r.get("Code")) == str(code) and (fy is None or fyn(r.get("FY")) == fyn(fy)):
            it = str(r.get("Intake status") or "")
            if not (it.startswith("SKIPPED") or it == "DUPLICATE"):   # updates by code never touch skipped/duplicate rows
                hits.append(r)
    return hits


def out(obj, changes=()):
    if changes:
        obj["changes"] = list(changes)
    print(json.dumps(obj, indent=2, default=str))


# ------------------------------------------------------------------ commands
def cmd_check(a, L):
    f = Path(a.file)
    md = md5(f) if f.exists() else None
    size = round(f.stat().st_size / 1e6, 2) if f.exists() else None
    rows = find(L, file=a.file) + [r for r in find(L, md=md) if md]
    if a.spotlights_dir and not rows:
        m = re.match(r"(\d{4})_[A-Za-z0-9]+_FY(\d{4})", f.name)
        if m and list(Path(a.spotlights_dir).glob(f"{m.group(1)}_*_FY{m.group(2)}_Spotlight*.pdf")):
            return out({"action": "already_done_backfill", "reason": "spotlight exists, no Ledger row: add the row (backfill)",
                        "md5": md, "size_mb": size})
    if not rows:
        return out({"action": "new", "md5": md, "size_mb": size})
    r = rows[0]
    st, it = r.get("Pipeline status", ""), r.get("Intake status", "")
    if st in DONE:
        return out({"action": "already_done", "status": st, "row": r["_row"]})
    if st == "PARKED":
        return out({"action": "parked", "row": r["_row"], "notes": r.get("Notes")})
    if str(it).startswith("SKIPPED"):
        if r.get("MD5") == md:
            return out({"action": "skip_same_md5", "intake": it, "row": r["_row"],
                        "retry_if": "file changed, or prepared parts / _text.txt now exist next to it"})
        return out({"action": "retry_changed_file", "intake": it, "row": r["_row"], "md5": md})
    if r.get("MD5") == md and str(r.get("Drive file ID / local path")) != str(a.file):
        return out({"action": "duplicate", "of_row": r["_row"], "of_file": r.get("File name")})
    last = str(r.get("Last module done", "")).upper()
    return out({"action": "resume", "status": st, "last_module_done": last, "resume_at": NEXT.get(last, "check manually"),
                "row": r["_row"], "open_decisions": r.get("Open decisions"), "decisions_answered": r.get("Decisions")})


def cmd_add(a, L):
    f = Path(a.file)
    md = md5(f) if f.exists() else ""
    dup = [r for r in find(L, md=md) if md]
    intake = "DUPLICATE" if dup else (a.intake or "READY")
    if intake not in INTAKE:
        sys.exit(f"bad intake status {intake}")
    row = L.put(None, {"Drive file ID / local path": str(a.file), "File name": f.name, "Company": a.company,
                       "Code": a.code, "FY": f"FY{fyn(a.fy)}", "Doc type": a.doctype,
                       "Size MB": round(f.stat().st_size / 1e6, 2) if f.exists() else "", "MD5": md,
                       "Intake status": intake, "Pipeline status": "" if intake == "DUPLICATE" or intake.startswith("SKIPPED") else "NEW", "Attempts": 0,
                       "Playbook version": a.playbook, "Date updated": TODAY,
                       "Notes": f"duplicate of row {dup[0]['_row']}" if dup else (a.notes or "")})
    L.save(); out({"added_row": row["_row"], "intake": intake}, L.changes)


def parse_sets(sets):
    d = {}
    for s in sets or []:
        k, _, v = s.partition("=")
        d[k.strip()] = v.strip()
    return d


def cmd_update(a, L):
    rows = find(L, file=a.file) if a.file else find(L, code=a.code, fy=a.fy)
    if not rows:
        sys.exit("no matching Ledger row")
    vals = parse_sets(a.set)
    unknown = [k for k in vals if k not in LEDGER_COLS]
    if unknown:
        sys.exit(f"unknown column(s): {unknown}")
    new = vals.get("Pipeline status")
    warnings = []
    for r in rows:
        cur = r.get("Pipeline status", "")
        if new and new not in PIPE and new not in SPECIAL:
            sys.exit(f"bad status {new}")
        if new in PIPE and cur in PIPE and PIPE.index(new) < PIPE.index(cur) and not a.redo:
            sys.exit(f"refused: {cur} -> {new} goes backwards (use --redo only for REDO)")
        if cur in DONE and not a.redo and new and new not in DONE and new != "FRONTIER_UPDATE":
            sys.exit(f"refused: row is {cur}; only REDO reopens it")
        if "Output files" in vals and r.get("Output files"):
            vals["Output files"] = "; ".join(dict.fromkeys(
                [x.strip() for x in (str(r["Output files"]) + ";" + vals["Output files"]).split(";") if x.strip()]))
        L.put(r, dict(vals, **{"Date updated": TODAY}))
    L.save(); out({"updated_rows": [r["_row"] for r in rows], "warnings": warnings}, L.changes)


def cmd_fail(a, L):
    rows = find(L, code=a.code, fy=a.fy)
    if not rows:
        sys.exit("no matching Ledger row")
    res = []
    for r in rows:
        n = int(r.get("Attempts") or 0) + 1
        st = "PARKED" if n >= 2 else "FAILED"
        note = (f"PARKED – needs you: {a.reason}" if st == "PARKED" else f"FAILED: {a.reason}")
        L.put(r, {"Pipeline status": st, "Attempts": n, "Notes": note, "Date updated": TODAY})
        res.append({"row": r["_row"], "status": st, "attempts": n})
    L.save(); out({"result": res}, L.changes)


def cmd_frontier(a, L):
    res = []
    for code in [c.strip() for c in a.codes.split(",") if c.strip()]:
        for r in find(L, code=code, fy=a.fy):
            if r.get("Pipeline status") in ("NEW", "EXTRACTED"):
                continue
            L.put(r, {"Pipeline status": "FRONTIER_UPDATE", "Date updated": TODAY,
                      "Notes": (str(r.get("Notes") or "") + f" | frontier/median changed {TODAY}: re-render DTF page, snapshot box, cards 06–07, email DTF line (_v2)").strip(" |")})
            res.append(r["_row"])
    L.save(); out({"set_frontier_update_rows": res}, L.changes)


def cmd_queue(a, L):
    groups = {}
    for r in L.rows:
        st = r.get("Pipeline status") or "NEW"
        it = str(r.get("Intake status") or "")
        key = ("skipped" if it.startswith("SKIPPED") or it == "DUPLICATE" else
               "done" if st in DONE else
               "awaiting_decisions" if st == "AWAITING_DECISIONS" else
               "approved_ready_for_stage_B" if st == "APPROVED" else
               "frontier_update" if st == "FRONTIER_UPDATE" else
               "parked" if st == "PARKED" else
               "new" if st == "NEW" else "part_done")
        tag = it if key == "skipped" else st
        groups.setdefault(key, []).append(f"{r.get('Code')} {r.get('Company')} {r.get('FY')} {r.get('Doc type')} [{tag}] {r.get('File name')}")
    older = [f"{r.get('Code')} {r.get('FY')} ({r.get('Playbook version')})" for r in L.rows
             if r.get("Pipeline status") in DONE and a.playbook and r.get("Playbook version") and r.get("Playbook version") != a.playbook]
    answered = [f"{r.get('Code')} {r.get('FY')}: {r.get('Decisions')}" for r in L.rows
                if r.get("Pipeline status") == "AWAITING_DECISIONS" and str(r.get("Decisions") or "").strip()]
    out({"counts": {k: len(v) for k, v in groups.items()}, "groups": groups,
         "decisions_answered_ready_to_apply": answered,
         "complete_under_older_playbook (REDO?)": older})


def cmd_decisions(a, L):
    rows = [r for r in L.rows if r.get("Pipeline status") == "AWAITING_DECISIONS"]
    res = []
    for r in rows:
        ans = str(r.get("Decisions") or "").strip()
        parsed = {}
        if ans.upper() in ("OK", "A", "B", "C") and not re.search(r"Q\d", ans, re.I):
            parsed = {"all": "recommended" if ans.upper() == "OK" else ans.upper()}
        else:
            for m in re.finditer(r"Q(\d+)\s*=\s*([A-Z]+|OK)", ans, re.I):
                parsed[f"Q{m.group(1)}"] = m.group(2).upper()
        res.append({"row": r["_row"], "code": r.get("Code"), "fy": r.get("FY"), "open": r.get("Open decisions"),
                    "answer_raw": ans, "parsed": parsed, "ready": bool(ans)})
    out({"awaiting": res})


def cmd_rules(a, R):
    rows = R.rows
    if a.find:
        t = a.find.lower()
        rows = [r for r in rows if t in str(r.get("Situation", "")).lower() or t in str(r.get("Rule", "")).lower()]
    out({"rules": [{k: v for k, v in r.items() if k != "_row"} for r in rows]})


def cmd_add_rule(a, R):
    t = (a.situation + " " + a.rule).lower()
    similar = [r.get("Rule ID") for r in R.rows if
               len(set(re.findall(r"[a-z]{5,}", t)) & set(re.findall(r"[a-z]{5,}", (str(r.get("Situation")) + " " + str(r.get("Rule"))).lower()))) >= 3]
    nums = [int(m.group(1)) for r in R.rows if (m := re.match(r"R(\d+)", str(r.get("Rule ID"))))]
    rid = f"R{(max(nums) + 1) if nums else 1:03d}"
    rule = a.rule + (" [TEST – confirm]" if a.test else "")
    R.put(None, {"Rule ID": rid, "Situation": a.situation, "Rule": rule, "Example (company, page)": a.example or "",
                 "Date": TODAY, "Source (decision / review)": a.source})
    R.save(); out({"added": rid, "possible_overlap_with": similar}, R.changes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("files", nargs="*")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--book"); g.add_argument("--ledger-csv")
    ap.add_argument("--rules-csv")
    for k in ("file", "company", "code", "fy", "doctype", "sector", "intake", "reason", "codes", "find",
              "situation", "rule", "example", "notes", "spotlights-dir"):
        ap.add_argument(f"--{k}")
    ap.add_argument("--source", default="decision")
    ap.add_argument("--playbook", default="v1.8")
    ap.add_argument("--set", action="append")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    if a.cmd == "md5":
        return out({f: {"md5": md5(f), "size_mb": round(Path(f).stat().st_size / 1e6, 2)} for f in a.files})
    if not (a.book or a.ledger_csv):
        sys.exit("give --book or --ledger-csv")
    if a.cmd in ("rules", "add-rule"):
        R = Store(a, "Rules")
        return (cmd_rules if a.cmd == "rules" else cmd_add_rule)(a, R)
    L = Store(a, "Ledger")
    if a.cmd == "init":
        R = Store(a, "Rules", wb=L.wb if a.book else None)
        if a.book:
            L.changes += R.changes; L.save()
        else:
            L.changes.append("init"); R.changes.append("init"); L.save(); R.save()
        return out({"ledger_header_row": getattr(L, "hdr", 1), "ledger_rows": len(L.rows)}, L.changes + R.changes)
    {"check": cmd_check, "add": cmd_add, "update": cmd_update, "fail": cmd_fail, "frontier-update": cmd_frontier,
     "queue": cmd_queue, "decisions": cmd_decisions}[a.cmd](a, L)


if __name__ == "__main__":
    main()
