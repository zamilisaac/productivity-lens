#!/usr/bin/env python3
"""
Productivity Lens - PageMap builder (Playbook Module 0, step 3).

For each PDF (or part files read as one report, or a *_text.txt with
'=== PDF page n ===' markers) it:
  1. caches the text of every page  -> <stem>_pages.json  (used by check_quotes.py)
  2. works out the PRINTED page number of every PDF page (seen on the page,
     or inferred from neighbouring pages, or none)
  3. lists candidate pages for each PageMap section

Usage:
  python page_map.py --report FY2026=path/AR2026.pdf [--report FY2024=part1.pdf,part2.pdf] \
      --out path/03_Working/5306_FarmFresh/5306_FarmFresh_FY2026_PageMap.xlsx

Part files: give them in order, comma-separated; PDF page numbers continue across parts.
"""
import argparse, json, re, statistics
from collections import Counter
from pathlib import Path

SECTIONS = {
    "Contents page": [r"\bcontents\b"],
    "Chairman's statement": [r"chairman'?s? (statement|message|letter)", r"message from (the|our) chairman"],
    "MD&A": [r"management discussion and analysis", r"\bmd&a\b"],
    "Operations / segment review": [r"operations? review", r"segment(al)? review", r"business review"],
    "Income statement": [r"statements? of (profit or loss|comprehensive income)", r"income statement"],
    "Balance sheet": [r"statements? of financial position", r"balance sheet"],
    "Cash flow statement": [r"statements? of cash flows?"],
    "Segment note": [r"operating segments", r"segment(al)? information"],
    "PPE note": [r"property,? plant and equipment"],
    "Staff costs note": [r"employee benefits? expense", r"staff costs"],
    "Five-year summary": [r"five[- ]year (financial )?(summary|highlights|record)", r"5[- ]year"],
    "Sustainability statement": [r"sustainability (statement|report)"],
    "Employee numbers": [r"(total|number of) (employees|workforce|headcount)", r"workforce (by|profile|breakdown)"],
}


def read_pdf_pages(paths):
    import pdfplumber
    pages = []
    for path in paths:
        with pdfplumber.open(path) as pdf:
            for pg in pdf.pages:
                h, w = float(pg.height), float(pg.width)
                text = pg.extract_text() or ""
                words = pg.extract_words() or []
                band = [wd for wd in words if wd["top"] < 0.07 * h or wd["bottom"] > 0.93 * h]
                cands = []
                for wd in band:
                    t = wd["text"].strip()
                    if re.fullmatch(r"\d{1,3}", t):
                        cands.append((int(t), "left" if wd["x0"] < w / 2 else "right"))
                pages.append(dict(text=text, cands=cands, file=Path(path).name))
    return pages


def read_text_file(path):
    raw = Path(path).read_text(errors="ignore")
    chunks = re.split(r"===\s*PDF page\s*(\d+)\s*===", raw)
    pages = []
    for i in range(1, len(chunks), 2):
        text = chunks[i + 1]
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        edge = lines[:2] + lines[-2:]
        cands = [(int(l), "?") for l in edge if re.fullmatch(r"\d{1,3}", l)]
        pages.append(dict(text=text, cands=cands, file=Path(path).name))
    return pages


def printed_pages(pages):
    """Return list of (printed_label, status) for each PDF page (1-based index)."""
    offsets = {}
    spread = Counter()
    for i, p in enumerate(pages, start=1):
        nums = sorted({n for n, _ in p["cands"]})
        if len(nums) >= 2 and any(b - a == 1 for a, b in zip(nums, nums[1:])):
            spread[i] += 1
        if nums:
            offsets[i] = [n - i for n in nums]
    flat = [o for v in offsets.values() for o in v]
    if not flat:
        return [("not visible", "none")] * len(pages)
    mode = Counter(flat).most_common(1)[0][0]
    out = []
    # local offset: nearest page with a seen candidate, prefer candidates close to the global mode
    seen = {}
    for i, offs in offsets.items():
        best = min(offs, key=lambda o: abs(o - mode))
        if abs(best - mode) <= 40:  # ignore stray digits like '2026' fragments, years, tables
            seen[i] = best
    for i in range(1, len(pages) + 1):
        if i in seen:
            n = i + seen[i]
            nums = sorted({c for c, _ in pages[i - 1]["cands"]})
            label = f"{n}-{n+1}" if (n + 1) in nums else str(n)
            out.append((label, "seen"))
        else:
            near = sorted(seen, key=lambda j: abs(j - i))[:1]
            if near and abs(near[0] - i) <= 3:
                out.append((str(i + seen[near[0]]), "inferred"))
            else:
                out.append(("not visible", "none"))
    return out


def find_sections(pages, labels):
    res = {}
    for name, pats in SECTIONS.items():
        hits = []
        for i, p in enumerate(pages, start=1):
            head = "\n".join(p["text"].splitlines()[:8]).lower()
            body = p["text"].lower()
            score = sum(3 for pt in pats if re.search(pt, head)) + sum(1 for pt in pats if re.search(pt, body))
            if score:
                hits.append((score, i))
        # skip the contents page itself for everything except "Contents page"
        hits.sort(key=lambda x: (-x[0], x[1]))
        res[name] = [(i, labels[i - 1][0]) for _, i in hits[:3]]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="append", required=True,
                    help="LABEL=path[,path2] e.g. FY2026=AR.pdf or FY2026=AR_text.txt")
    ap.add_argument("--out", required=True, help="PageMap .xlsx path (cache json saved alongside)")
    a = ap.parse_args()
    import pandas as pd
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        n = 2
        while (c := out.with_name(f"{out.stem}_v{n}{out.suffix}")).exists():
            n += 1
        out = c
    cache, map_rows, sec_rows, summary = {}, [], [], {}
    for spec in a.report:
        label, files = spec.split("=", 1)
        files = [f.strip() for f in files.split(",")]
        pages = read_text_file(files[0]) if files[0].endswith(".txt") else read_pdf_pages(files)
        labels = printed_pages(pages)
        cache[label] = [dict(pdf_page=i + 1, printed=labels[i][0], status=labels[i][1],
                             file=p["file"], text=p["text"]) for i, p in enumerate(pages)]
        for i, (lab, st) in enumerate(labels, start=1):
            map_rows.append({"Report": label, "PDF page": i, "Printed page": lab, "Status": st,
                             "File": pages[i - 1]["file"], "Chars": len(pages[i - 1]["text"])})
        for name, hits in find_sections(pages, labels).items():
            sec_rows.append({"Report": label, "Section": name,
                             "Candidates (printed p. / PDF p.)": "; ".join(f"p.{pr} / PDF p.{i}" for i, pr in hits) or "Not found",
                             "Confirmed printed page": ""})
        empty = sum(1 for p in pages if len(p["text"].strip()) < 20)
        summary[label] = {"pages": len(pages), "printed_seen": sum(1 for l in labels if l[1] == "seen"),
                          "printed_inferred": sum(1 for l in labels if l[1] == "inferred"),
                          "no_text_pages": empty}
        if empty > 0.5 * len(pages):
            summary[label]["warning"] = "Mostly no text: likely scanned images -> SKIPPED_UNREADABLE"
    cache_path = out.with_name(out.stem + "_pages.json")
    cache_path.write_text(json.dumps(cache))
    with pd.ExcelWriter(out) as w:
        pd.DataFrame(sec_rows).to_excel(w, sheet_name="Sections", index=False)
        pd.DataFrame(map_rows).to_excel(w, sheet_name="PageNumbers", index=False)
    for p in (out, cache_path):
        assert p.exists() and p.stat().st_size > 0
    print(json.dumps({"saved": [str(out), str(cache_path)], "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
