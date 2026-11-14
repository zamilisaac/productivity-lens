#!/usr/bin/env python3
"""
Productivity Lens - report preparer (PDF cutter)

Makes every annual / sustainability report readable by Claude's 10 MB limit.
Run it on your PC, in Claude Cowork, or in Claude Code, pointed at the
Google Drive for Desktop copy of "Productivity Lens/02_Reports".

For every PDF over the limit it tries, in order:
  1. Compress (Ghostscript, if installed)  -> one smaller PDF
  2. Split by size into parts              -> _part1of3.pdf, _part2of3.pdf ...
  3. Text sidecar (always made)            -> _text.txt with page markers
It never deletes anything. Originals over the limit are moved to
02_Reports/_Oversize_Originals/ so the next run does not process them again.
Every action is written to 02_Reports/_prep_log.csv for Claude to read.

Usage:
  pip install pypdf pdfplumber
  python pl_prepare_reports.py "C:/Users/me/My Drive/Productivity Lens/02_Reports"
  python pl_prepare_reports.py <folder> --limit-mb 9.5 --dry-run
"""
import argparse
import csv
import datetime as dt
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

SKIP_DIRS = {"_Oversize_Originals", "_Inbox"}
LOG_NAME = "_prep_log.csv"
LOG_COLS = ["timestamp", "original_file", "md5", "size_mb", "pages",
            "action", "output_files", "notes"]


def md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


def already_logged(log_path: Path) -> set:
    if not log_path.exists():
        return set()
    with open(log_path, newline="", encoding="utf-8") as f:
        return {row["md5"] for row in csv.DictReader(f)}


def write_log(log_path: Path, row: dict) -> None:
    new = not log_path.exists()
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LOG_COLS)
        if new:
            w.writeheader()
        w.writerow(row)


def find_gs():
    for name in ("gs", "gswin64c", "gswin32c"):
        if shutil.which(name):
            return shutil.which(name)
    return None


def try_compress(src: Path, dst: Path, gs: str) -> bool:
    """Ghostscript /ebook keeps text sharp and shrinks photos (150 dpi)."""
    cmd = [gs, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.6",
           "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dBATCH", "-dQUIET",
           f"-sOutputFile={dst}", str(src)]
    try:
        subprocess.run(cmd, check=True, timeout=900)
        return dst.exists() and dst.stat().st_size > 0
    except Exception:
        return False


def split_by_size(src: Path, out_dir: Path, limit_mb: float) -> list:
    """Greedy split: add pages to a part until it would pass the limit."""
    reader = PdfReader(str(src))
    n = len(reader.pages)
    stem = src.stem
    ranges, start = [], 0
    while start < n:
        end = start + 1
        last_ok = start + 1
        # grow in steps, checking real written size
        step = 10
        while end <= n:
            w = PdfWriter()
            for i in range(start, end):
                w.add_page(reader.pages[i])
            tmp = out_dir / f".{stem}_probe.pdf"
            with open(tmp, "wb") as f:
                w.write(f)
            size = mb(tmp)
            tmp.unlink()
            if size <= limit_mb:
                last_ok = end
                if end == n:
                    break
                end = min(n, end + step)
            else:
                if step > 1:          # back off and refine
                    end = last_ok + 1
                    step = 1
                    continue
                break
        if last_ok == start:          # one single page is over the limit
            last_ok = start + 1
        ranges.append((start, last_ok))
        start = last_ok

    outputs = []
    total = len(ranges)
    for k, (a, b) in enumerate(ranges, 1):
        w = PdfWriter()
        for i in range(a, b):
            w.add_page(reader.pages[i])
        out = out_dir / f"{stem}_part{k}of{total}_pdfp{a+1}-{b}.pdf"
        with open(out, "wb") as f:
            w.write(f)
        outputs.append(out)
    return outputs


def text_sidecar(src: Path, out_dir: Path) -> Path:
    """Plain text with a marker per PDF page. Printed page numbers stay in
    the text (usually in the header/footer), so quotes can still be cited."""
    import pdfplumber
    out = out_dir / f"{src.stem}_text.txt"
    with pdfplumber.open(str(src)) as pdf, open(out, "w", encoding="utf-8") as f:
        f.write(f"SOURCE FILE: {src.name}\n")
        f.write("NOTE: '=== PDF page n ===' is the file page index, "
                "NOT the printed page number. Cite the printed number.\n\n")
        for i, page in enumerate(pdf.pages, 1):
            f.write(f"\n=== PDF page {i} ===\n")
            try:
                f.write(page.extract_text() or "[no extractable text]")
            except Exception as e:
                f.write(f"[text extraction failed: {e}]")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="02_Reports folder (Drive for Desktop path)")
    ap.add_argument("--limit-mb", type=float, default=9.5,
                    help="target max size per file (default 9.5, under the 10 MB limit)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.folder).expanduser()
    if not root.is_dir():
        sys.exit(f"Folder not found: {root}")
    log_path = root / LOG_NAME
    done = already_logged(log_path)
    oversize_dir = root / "_Oversize_Originals"
    gs = find_gs()
    print(f"Ghostscript: {'found' if gs else 'not found (split only)'}")

    pdfs = [p for p in root.rglob("*.pdf")
            if not any(part in SKIP_DIRS for part in p.parts)
            and "_part" not in p.stem and not p.name.startswith(".")]

    for p in sorted(pdfs):
        size = mb(p)
        if size <= args.limit_mb:
            continue
        digest = md5(p)
        if digest in done:
            print(f"Already prepared, skipping: {p.name}")
            continue
        print(f"Over limit ({size:.1f} MB): {p.relative_to(root)}")
        if args.dry_run:
            continue

        row = {"timestamp": dt.datetime.now().isoformat(timespec="seconds"),
               "original_file": str(p.relative_to(root)), "md5": digest,
               "size_mb": f"{size:.1f}", "pages": "", "action": "",
               "output_files": "", "notes": ""}
        try:
            row["pages"] = len(PdfReader(str(p)).pages)
        except Exception as e:
            row.update(action="SKIPPED", notes=f"cannot open PDF: {e}")
            write_log(log_path, row)
            print("  ⚠️ cannot open, skipped")
            continue

        outputs, notes = [], []
        work = p
        # 1. compress
        if gs:
            comp = p.with_name(p.stem + "_compressed.pdf")
            if try_compress(p, comp, gs):
                if mb(comp) <= args.limit_mb:
                    outputs.append(comp)
                    row["action"] = "COMPRESSED"
                    notes.append(f"{size:.1f} MB -> {mb(comp):.1f} MB")
                else:
                    work = comp          # split the smaller version
                    notes.append(f"compressed to {mb(comp):.1f} MB, still over")
            else:
                notes.append("compression failed")
        # 2. split
        if not outputs:
            try:
                parts = split_by_size(work, p.parent, args.limit_mb)
                big = [x.name for x in parts if mb(x) > args.limit_mb]
                outputs.extend(parts)
                row["action"] = "SPLIT"
                notes.append(f"{len(parts)} parts")
                if big:
                    notes.append(f"single page still over limit: {', '.join(big)}")
                if work != p and work.exists():
                    work.unlink()        # remove the intermediate compressed file
            except Exception as e:
                notes.append(f"split failed: {e}")
        # 3. text sidecar (always)
        try:
            outputs.append(text_sidecar(p, p.parent))
        except Exception as e:
            notes.append(f"text sidecar failed: {e}")

        if not row["action"]:
            row["action"] = "TEXT_ONLY" if outputs else "SKIPPED"
        # move original out of the way so it is never read again
        oversize_dir.mkdir(exist_ok=True)
        dest = oversize_dir / p.relative_to(root)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dest))
        notes.append("original moved to _Oversize_Originals")

        row["output_files"] = " | ".join(x.name for x in outputs)
        row["notes"] = "; ".join(notes)
        write_log(log_path, row)
        print(f"  ✅ {row['action']}: {row['output_files']}")

    print(f"\nDone. Log: {log_path}")


if __name__ == "__main__":
    main()
