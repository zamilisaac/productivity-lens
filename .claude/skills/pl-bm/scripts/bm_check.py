#!/usr/bin/env python3
"""
Productivity Lens - Bahasa Melayu check (Playbook Module 4D).

Compares Content.json (EN) with Content_BM.json field by field:
  ERRORS (must fix): different structure; any number, unit, page, quote, code
         or company name not identical; 'p.' page refs left in BM text;
         Bahasa Indonesia words; brand name changed.
  WARNINGS (review): glossary term not used where the EN field uses the
         English term; text that still looks English.

Usage: python bm_check.py --en Content.json --bm Content_BM.json [--out report.json]
Exit code 1 if any error.
"""
import argparse, csv, json, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXED_KEYS = {"value", "unit", "scope", "page", "quote", "audit_status", "report", "code", "fy", "company",
              "short_name", "tier", "grade", "years", "values", "mode", "key", "source_pages", "_sample"}
# Indonesian forms -> standard Bahasa Malaysia
INDONESIAN = {"perusahaan": "syarikat", "karyawan": "kakitangan / pekerja", "karena": "kerana", "produksi": "pengeluaran",
              "investasi": "pelaburan", "kualitas": "kualiti", "aktivitas": "aktiviti", "fasilitas": "kemudahan / fasiliti",
              "kapasitas": "kapasiti", "produktivitas": "produktiviti", "otomatisasi": "automasi", "pasokan": "bekalan",
              "dampak": "kesan", "menerapkan": "melaksanakan", "manajemen": "pengurusan", "pabrik": "kilang",
              "kantor": "pejabat", "uang": "wang", "mobil": "kereta", "bisa": "boleh", "efisiensi": "kecekapan",
              "infrastruktur": None, "inventaris": "inventori", "keuntungan bersih": None, "sumber daya": "sumber",
              "lowongan": "kekosongan", "pelatihan": "latihan", "tenaga ahli": "pakar", "sistem informasi": "sistem maklumat"}
INDONESIAN = {k: v for k, v in INDONESIAN.items() if v}
EN_STOP = {"the", "and", "with", "from", "this", "that", "their", "which", "into", "after", "before", "per", "each", "your"}


def numbers(s):
    s = str(s).replace("\u2212", "-")
    toks = re.findall(r"RM\s?[\d,]+(?:\.\d+)?\s?(?:m|j|million|juta|billion|bilion|bn)?|[-+]?\d[\d,]*(?:\.\d+)?\s?[%×x]?", s)
    norm = []
    for t in toks:
        t = t.replace(" ", "").replace(",", "")
        t = re.sub(r"(million|juta)$", "m", t); t = re.sub(r"(billion|bilion|bn)$", "b", t)
        t = re.sub(r"j$", "m", t)                 # RM47j (BM) == RM47m (EN)
        t = t.replace("x", "×")
        norm.append(t)
    return Counter(norm)


def walk(en, bm, path, errs, warns, texts):
    if isinstance(en, dict):
        if not isinstance(bm, dict):
            errs.append(f"{path}: structure differs"); return
        for k in en:
            if k not in bm:
                errs.append(f"{path}.{k}: missing in BM"); continue
            if k in FIXED_KEYS and k not in ("_sample",):
                if json.dumps(en[k], ensure_ascii=False) != json.dumps(bm[k], ensure_ascii=False):
                    errs.append(f"{path}.{k}: must be identical (EN {en[k]!r} vs BM {bm[k]!r})")
                continue
            walk(en[k], bm[k], f"{path}.{k}" if path else k, errs, warns, texts)
        extra = set(bm) - set(en)
        if extra:
            warns.append(f"{path}: extra keys in BM {sorted(extra)}")
    elif isinstance(en, list):
        if not isinstance(bm, list) or len(en) != len(bm):
            errs.append(f"{path}: list length differs ({len(en)} vs {len(bm) if isinstance(bm, list) else 'n/a'})"); return
        for i, (a, b) in enumerate(zip(en, bm)):
            walk(a, b, f"{path}[{i}]", errs, warns, texts)
    elif isinstance(en, str):
        if path == "lang":
            if bm != "bm":
                errs.append("lang must be 'bm'")
            return
        ne, nb = numbers(en), numbers(bm)
        if ne != nb:
            errs.append(f"{path}: numbers differ: EN {sorted((ne - nb).elements())} / BM {sorted((nb - ne).elements())}")
        texts.append((path, en, bm))
    else:
        if en != bm:
            errs.append(f"{path}: value differs ({en!r} vs {bm!r})")


def glossary():
    pairs = []
    with open(HERE.parent / "references" / "glossary.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            e, b = [x.strip() for x in r["English"].split(" / ")], [x.strip() for x in r["Bahasa Melayu"].split(" / ")]
            if len(e) == len(b):
                pairs += list(zip(e, b))
            else:
                pairs.append((r["English"], r["Bahasa Melayu"]))
    return sorted(pairs, key=lambda p: -len(p[0]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--en", required=True); ap.add_argument("--bm", required=True); ap.add_argument("--out")
    a = ap.parse_args()
    en = json.loads(Path(a.en).read_text(encoding="utf-8"))
    bm = json.loads(Path(a.bm).read_text(encoding="utf-8"))
    errs, warns, texts = [], [], []
    walk(en, bm, "", errs, warns, texts)
    gl = glossary()
    for path, e, b in texts:
        lb = b.lower()
        for word, fix in INDONESIAN.items():
            if re.search(rf"\b{re.escape(word)}\b", lb):
                errs.append(f"{path}: Bahasa Indonesia '{word}' -> use '{fix}'")
        if re.search(r"\bp\.\s?\d", b) or re.search(r"\bpp\.\s?\d", b):
            errs.append(f"{path}: page reference uses 'p.'; BM uses 'hlm.'")
        if "productivity lens" in e.lower() and "Productivity Lens" not in b:
            errs.append(f"{path}: brand must stay 'Productivity Lens'")
        for term_en, term_bm in gl:
            if term_en.lower() in e.lower() and len(term_en) > 4:
                core = term_bm.split("(")[0].strip().lower()
                if core and core not in lb:
                    warns.append(f"{path}: EN uses '{term_en}', BM does not use glossary term '{term_bm}'")
        words = re.findall(r"[a-z]+", lb)
        if len(words) >= 6 and sum(w in EN_STOP for w in words) / len(words) > 0.12:
            warns.append(f"{path}: looks untranslated: {b[:60]!r}")
    if en.get("company") and en.get("company") != bm.get("company"):
        errs.append("company name must stay identical")
    rep = {"pass": not errs, "errors": errs, "warnings": warns[:60], "fields_compared": len(texts)}
    s = json.dumps(rep, indent=2, ensure_ascii=False)
    if a.out:
        Path(a.out).write_text(s, encoding="utf-8")
    print(s)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
