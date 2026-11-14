#!/usr/bin/env python3
"""
Productivity Lens - Evidence audit (Playbook Module 4B, Step 1).

Checks, for every figure, that the quote appears word for word on the cited
PRINTED page, and that the number appears in the quote.

Input figures: csv/xlsx with columns (any order, header row found automatically):
  ID (optional) | Report (e.g. FY2026; optional if only one report) | Value | Page | Quote
  - DataSheet and Initiatives files work as they are (Page, Quote, Value/Reported result).
  - Content JSON: pass the .json; every object holding value/page/quote is checked.

Usage:
  python check_quotes.py --pages-cache .../5306_FarmFresh_FY2026_PageMap_pages.json \
      --figures .../5306_FarmFresh_FY2026_DataSheet.xlsx [--default-report FY2026] --out .../audit_step1.csv

Results: Confirmed | Mismatch-page (quote found on another page: correct page given)
         | Mismatch-value (quote found, number not in quote) | Not found | No quote
"""
import argparse, json, re, unicodedata
from pathlib import Path

import pandas as pd

TRANS = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-",
                       "\u2014": "-", "\u2212": "-", "\u00a0": " ", "\u2022": " ", "\ufb01": "fi", "\ufb02": "fl"})


def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).translate(TRANS).lower()
    s = re.sub(r"-\s*\n\s*", "", s)          # hyphenation across lines
    return re.sub(r"\s+", " ", s).strip()


def squash(s):
    return re.sub(r"[^a-z0-9.%]", "", norm(s))


def numbers_in(s):
    out = set()
    for m in re.finditer(r"\(?-?\d[\d,]*\.?\d*\)?", str(s)):
        t = m.group(0)
        neg = t.startswith("(") and t.endswith(")")
        t = t.strip("()").replace(",", "")
        try:
            v = float(t)
        except ValueError:
            continue
        out.add(-v if neg else v)
        out.add(v)
    return out


def value_in_quote(value, quote):
    if value is None or str(value).strip() in ("", "nan"):
        return "skip"
    vals = numbers_in(value)
    if not vals:
        return "skip"   # text value (e.g. a reported result phrase)
    q = numbers_in(quote)
    if vals & q:
        return "ok"
    for v in vals:
        for f in (1000, 1e6, 0.001, 1e-6):
            if any(abs(v * f - x) < 1e-6 * max(1, abs(x)) for x in q):
                return "unit"   # matches after RM'000 / million conversion -> check units
    return "missing"


def load_figures(path):
    p = Path(path)
    if p.suffix == ".json":
        rows = []
        def walk(o, trail):
            if isinstance(o, dict):
                if "quote" in o and "page" in o:
                    rows.append({"ID": trail, "Value": o.get("value"), "Page": o.get("page"),
                                 "Quote": o.get("quote"), "Report": o.get("report")})
                for k, v in o.items():
                    walk(v, f"{trail}.{k}" if trail else k)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, f"{trail}[{i}]")
        walk(json.loads(p.read_text()), "")
        return pd.DataFrame(rows)
    if p.suffix in (".xlsx", ".xlsm"):
        raw = pd.read_excel(p, header=None)
        hdr = next(i for i, r in raw.iterrows() if any(str(c).strip().lower().startswith("quote") for c in r))
        df = pd.read_excel(p, header=hdr)
    else:
        df = pd.read_csv(p)
    df.columns = [str(c).strip() for c in df.columns]
    ren = {}
    for c in df.columns:
        lc = c.lower()
        if lc.startswith("quote"): ren[c] = "Quote"
        elif lc == "page": ren[c] = "Page"
        elif lc in ("value", "reported result") and "Value" not in ren.values(): ren[c] = "Value"
        elif lc.startswith("source report") or lc == "report": ren[c] = "Report"
    df = df.rename(columns=ren)
    if "ID" not in df.columns:
        label = df["Item"] if "Item" in df.columns else df.get("Initiative", pd.Series(range(len(df))))
        yr = df["Year"].astype(str) if "Year" in df.columns else ""
        df["ID"] = label.astype(str) + (" " + yr if isinstance(yr, pd.Series) else "")
    return df.dropna(subset=["Quote"], how="all") if "Quote" in df.columns else df


def pages_for(cache_report, page_label):
    """PDF-page entries whose printed label equals or contains the cited printed page."""
    lab = str(page_label).strip().lower().replace("p.", "").replace("pp.", "").strip()
    if lab.endswith(".0"):
        lab = lab[:-2]
    wanted = {x.strip() for x in re.split(r"[;,&]| and ", lab) if x.strip()}
    hits = []
    for e in cache_report:
        pr = str(e["printed"])
        parts = set(pr.split("-")) if re.fullmatch(r"\d+-\d+", pr) else {pr}
        if wanted & parts:
            hits.append(e)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages-cache", required=True, action="append")
    ap.add_argument("--figures", required=True)
    ap.add_argument("--default-report")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cache = {}
    for c in a.pages_cache:
        cache.update(json.loads(Path(c).read_text()))
    default = a.default_report or (list(cache)[0] if len(cache) == 1 else None)
    df = load_figures(a.figures)
    results = []
    for _, r in df.iterrows():
        q = r.get("Quote")
        rep = r.get("Report") if "Report" in r and str(r.get("Report")) not in ("nan", "None") else default
        m = re.search(r"(19|20)\d{2}", str(rep)) if rep else None
        rep_key = next((k for k in cache if m and m.group(0) in k), rep)
        row = {"ID": r.get("ID"), "Report": rep_key, "Value": r.get("Value"), "Page cited": r.get("Page"),
               "Quote": q, "Result": None, "Correct printed page": "", "Detail": ""}
        if q is None or str(q).strip() in ("", "nan", "(quote)"):
            row["Result"] = "No quote"; results.append(row); continue
        if rep_key not in cache:
            row["Result"] = "Not found"; row["Detail"] = f"report {rep} not in page cache"; results.append(row); continue
        nq, sq = norm(q), squash(q)
        found_on = [e for e in cache[rep_key] if nq in norm(e["text"]) or (len(sq) > 12 and sq in squash(e["text"]))]
        cited = pages_for(cache[rep_key], r.get("Page"))
        on_cited = [e for e in cited if e in found_on]
        if on_cited:
            vq = value_in_quote(r.get("Value"), q)
            if vq in ("ok", "skip"):
                row["Result"] = "Confirmed"
            elif vq == "unit":
                row["Result"] = "Mismatch-value"; row["Detail"] = "number matches only after a unit conversion (RM'000 vs million?)"
            else:
                row["Result"] = "Mismatch-value"; row["Detail"] = "value not in quote"
            if any(e["status"] != "seen" for e in on_cited):
                row["Detail"] += " | printed page inferred, not seen on page: flag"
        elif found_on:
            row["Result"] = "Mismatch-page"
            row["Correct printed page"] = "; ".join(
                (e["printed"] if e["printed"] != "not visible" else f"PDF p.{e['pdf_page']} (printed page not visible)")
                for e in found_on[:3])
        else:
            row["Result"] = "Not found"
            if not cited:
                row["Detail"] = "cited page not in page map"
        results.append(row)
    res = pd.DataFrame(results)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        n = 2
        while (c := out.with_name(f"{out.stem}_v{n}{out.suffix}")).exists():
            n += 1
        out = c
    res.to_csv(out, index=False) if out.suffix == ".csv" else res.to_excel(out, index=False)
    assert out.exists() and out.stat().st_size > 0
    counts = res["Result"].value_counts().to_dict() if len(res) else {}
    print(json.dumps({"saved": str(out), "figures": len(res), "confirmed": int(counts.get("Confirmed", 0)),
                      "counts": counts,
                      "fix_list": res[res["Result"] != "Confirmed"][["ID", "Result", "Correct printed page", "Detail"]]
                      .head(30).to_dict("records")}, indent=2, default=str))


if __name__ == "__main__":
    main()
