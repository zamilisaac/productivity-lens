#!/usr/bin/env python3
"""
Productivity Lens - word budgets (Playbook Module 4, fit check part 1).

Counts words in every Content-file block against the EN budgets; BM budgets
are EN minus 15% (rounded down). Run on Content.json and Content_BM.json
BEFORE rendering, so cuts happen in the Content file, never by shrinking type.

Usage: python word_budget.py path/to/Content.json [--lang en|bm]
Exit code 1 if any block is over budget.
"""
import json, math, sys, argparse

EN = {
    "headline": 20, "intro": 35,
    "headline_results[].label": 6, "headline_results[].insight": 15,
    "snapshot.notes": 30,
    "key_initiatives[].initiative": 8, "key_initiatives[].what": 8, "key_initiatives[].result": 8,
    "strengths[]": 30, "watch[]": 30,
    "dtf.analysis": 70, "dtf.notes": 35,
    "lessons[].title": 14, "lessons[].did": 40, "lessons[].sme": 40,
    "lessons[].starter": 25, "lessons[].measure": 20,
    "notes": 50,
}
COUNTS = {"headline_results": 3, "lessons": 3, "strengths": 2, "watch": 2}
MAX_ROWS = {"key_initiatives": 10}


def words(s):
    return len(str(s or "").split())


def get_all(c, path):
    if "[]" not in path:
        cur = c
        for p in path.split("."):
            cur = (cur or {}).get(p) if isinstance(cur, dict) else None
        return [(path, cur)]
    head, _, tail = path.partition("[]")
    arr = c.get(head) or []
    out = []
    for i, item in enumerate(arr):
        val = item if not tail else item.get(tail.lstrip("."))
        out.append((f"{head}[{i}]{tail}", val))
    return out


def check(c, lang):
    factor = 0.85 if lang == "bm" else 1.0
    fails, rows = [], []
    for path, lim in EN.items():
        limit = math.floor(lim * factor)
        for p, val in get_all(c, path):
            n = words(val)
            rows.append((p, n, limit))
            if n > limit:
                fails.append(f"{p}: {n} words > {limit}")
            if val in (None, "") and not path.startswith(("snapshot.notes", "dtf.notes")):
                fails.append(f"{p}: empty")
    for k, n in COUNTS.items():
        if len(c.get(k) or []) != n:
            fails.append(f"{k}: needs exactly {n} items, has {len(c.get(k) or [])}")
    for k, n in MAX_ROWS.items():
        if len(c.get(k) or []) > n:
            fails.append(f"{k}: max {n} rows, has {len(c.get(k))}")
    return fails, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--lang")
    a = ap.parse_args()
    c = json.load(open(a.content, encoding="utf-8"))
    lang = a.lang or c.get("lang", "en")
    fails, rows = check(c, lang)
    print(json.dumps({"lang": lang, "pass": not fails, "over_budget": fails,
                      "blocks": [{"block": p, "words": n, "limit": l} for p, n, l in rows]}, indent=2, ensure_ascii=False))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
