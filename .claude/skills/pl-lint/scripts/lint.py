#!/usr/bin/env python3
"""
Productivity Lens - house-rules lint (Style Guide s.1-2; Playbook Module 5 automatic checks).

Scans outputs (PDF, HTML, JSON, MD, TXT) and reports:
  ERRORS   rank words, investment language, "x of y" positions, figures that do
           not appear in the Content file, "the company discloses/reports that"
  WARNINGS US spellings, jargon, exclamation marks, emojis, hyphen used as a
           minus sign in a change, ALL CAPS sentences

Quotes from reports are exempt (JSON 'quote' fields are skipped).

Usage:
  python lint.py --content Content.json FILE [FILE ...] [--out report.json]
  python lint.py FILE ...            (no number check without --content)
Exit code 1 if any error.
"""
import argparse, json, re, sys
from pathlib import Path

RANK = r"\b(top|best|leaders?|leading|ranked|rankings?|outperform\w*|laggards?|worst|no\. ?1|number one)\b"
INVEST = r"\b(buy|sell|undervalued|overvalued|share price|target price|price target|recommend(ed|s|ation)?|investment case|upside)\b"
POSITION = r"\b\d+(st|nd|rd|th)? (of|out of) \d+\b"
DISCLOSES = r"\b(the company|the group|it) (discloses|reports|reported|disclosed) that\b"
US = {"organization": "organisation", "organize": "organise", "program ": "programme ", "labor": "labour",
      "center": "centre", "optimize": "optimise", "optimization": "optimisation", "analyze": "analyse",
      "color": "colour", "favor": "favour", "behavior": "behaviour", "modeling": "modelling",
      "utilize": "use", "utilization": "use", "standardize": "standardise", "digitize": "digitise",
      "prioritize": "prioritise", "minimize": "minimise", "maximize": "maximise", "fiber": "fibre"}
JARGON = ["synergy", "synergies", "holistic", "best-in-class", "world-class", "leverages", "leveraging", "leveraged",
          "paradigm", "game-changer", "cutting-edge"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
ALLOWED_CAPS = {"PRODUCTIVITY LENS", "DRAFT", "PDPA", "ERP", "AI", "RM", "SME", "PKS", "DTF", "FY", "MD&A", "PPE", "BM", "EN"}


def text_of(path):
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        import logging, pdfplumber
        logging.getLogger("pdfminer").setLevel(logging.ERROR)
        with pdfplumber.open(p) as pdf:
            return [(f"p{i}", pg.extract_text() or "") for i, pg in enumerate(pdf.pages, start=1)]
    raw = p.read_text(encoding="utf-8", errors="ignore")
    if p.suffix.lower() in (".html", ".htm"):
        raw = re.sub(r"(?is)<(style|script)[^>]*>.*?</\1>", " ", raw)
        raw = re.sub(r"(?s)<[^>]+>", " ", raw)
        import html
        raw = html.unescape(raw)
        return [("html", raw)]
    if p.suffix.lower() == ".json":
        out = []
        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ("quote", "_sample", "links"):
                        continue
                    walk(v, f"{path}.{k}" if path else k)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, f"{path}[{i}]")
            elif isinstance(o, str):
                out.append((path, o))
        walk(json.loads(raw), "")
        return out
    return [("text", raw)]


def num_tokens(s):
    s = s.replace("\u2212", "-")
    out = set()
    for t in re.findall(r"\d[\d,]*(?:\.\d+)?", s):
        t = t.replace(",", "")
        try:
            out.add(float(t))
        except ValueError:
            pass
    return out


def content_numbers(c):
    nums = set()
    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            nums.add(float(o)); nums.add(round(abs(float(o)), 1)); nums.add(abs(float(o)))
        elif isinstance(o, str):
            nums.update(num_tokens(o))
    walk(c)
    return nums


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--content")
    ap.add_argument("--out")
    a = ap.parse_args()
    allowed = None
    if a.content:
        c = json.loads(Path(a.content).read_text(encoding="utf-8"))
        allowed = content_numbers(c)
        allowed |= {float(x) for x in range(0, 11)} | {float(y) for y in range(2015, 2036)}
        allowed |= {200.0, 96.0, 100.0, 90.0, 10.0, 50.0, 15.0, 28.0}  # frontier 100, P90/P10, 50–200 staff
    errors, warnings = [], []
    for f in a.files:
        for where, t in text_of(f):
            loc = f"{Path(f).name}:{where}"
            low = t.lower()
            for pat, msg, bucket in ((RANK, "rank word", errors), (INVEST, "investment language", errors),
                                     (POSITION, "position / 'x of y'", errors), (DISCLOSES, "'the company discloses/reports that'", errors)):
                for m in re.finditer(pat, low):
                    ctx = t[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                    if msg == "position / 'x of y'" and re.search(r"page \d+ / \d+|halaman \d+ / \d+", ctx.lower()):
                        continue
                    if msg == "rank word" and re.search(r"\b(not|no|never)(\s+a)?\s+(rank|ranking|ranked)", low[max(0, m.start()-14):m.end()]):
                        continue
                    if msg == "investment language" and "not investment advice" in low[max(0, m.start()-20):m.end()+20]:
                        continue
                    bucket.append(f"{loc}: {msg} '{m.group(0)}' … {ctx.strip()} …")
            for us, uk in US.items():
                for m in re.finditer(rf"\b{re.escape(us.strip())}\w*", low):
                    if us.strip() == "program" and re.search(r"programm", m.group(0)):
                        continue
                    if us.strip() == "center" and m.group(0).startswith("centre"):
                        continue
                    warnings.append(f"{loc}: US spelling '{m.group(0)}' -> '{uk.strip()}'")
                    break
            for j in JARGON:
                if re.search(rf"\b{re.escape(j)}\b", low):
                    warnings.append(f"{loc}: jargon '{j}'")
            if "!" in t:
                warnings.append(f"{loc}: exclamation mark")
            if EMOJI.search(t):
                warnings.append(f"{loc}: emoji")
            for m in re.finditer(r"(?<![\w\d])-\d+(?:\.\d+)?%", t):
                warnings.append(f"{loc}: hyphen used as minus in '{m.group(0)}' -> use '−'")
            for sent in ([] if f.lower().endswith(".pdf") else re.split(r"(?<=[.!?])\s+|\n", t)):
                words = re.findall(r"[A-Za-z]{2,}", sent)
                if len(words) >= 5 and all(w.isupper() for w in words) and sent.strip().upper() not in ALLOWED_CAPS:
                    if not any(sent.strip().startswith(x) for x in ALLOWED_CAPS):
                        warnings.append(f"{loc}: ALL CAPS sentence '{sent.strip()[:50]}'")
            if allowed is not None and not f.endswith(".json"):
                has_chart = any(t in low for t in ("analyst calculation", "kiraan penganalisis", "our calculation", "kiraan kami"))
                for m in re.finditer(r"\d[\d,]*(?:\.\d+)?", t):
                    v = float(m.group(0).replace(",", ""))
                    if has_chart and v <= 300 and v % 5 == 0:   # chart axis ticks
                        continue
                    if v not in allowed:
                        ctx = t[max(0, m.start() - 25): m.end() + 15].replace("\n", " ")
                        errors.append(f"{loc}: number {m.group(0)} not in Content file … {ctx.strip()} …")
    errors = list(dict.fromkeys(errors)); warnings = list(dict.fromkeys(warnings))
    rep = {"pass": not errors, "errors": errors[:100], "warnings": warnings[:100],
           "error_count": len(errors), "warning_count": len(warnings)}
    s = json.dumps(rep, indent=2, ensure_ascii=False)
    if a.out:
        Path(a.out).write_text(s, encoding="utf-8")
    print(s)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
