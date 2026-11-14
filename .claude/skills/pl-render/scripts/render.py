#!/usr/bin/env python3
"""
Productivity Lens - renderer (Playbook Modules 4, 4C, 4D, 4E).

Renders ONLY from an approved Content JSON (EN or BM), with the bundled
templates and fonts, so every company looks identical.

  python render.py spotlight --content C.json --out-dir 04_Spotlights/ [--png-dir 04_Spotlights/Snapshots/]
  python render.py cards     --content C.json --out-dir 04_Spotlights/Snapshots/
  python render.py email     --content C.json --out-dir 04_Spotlights/Newsletter/
  python render.py all       --content C.json --root "<Productivity Lens>"

Each command runs the fit check in the browser (overflow per page/block,
minimum type sizes) and prints a JSON report. Exit code 1 = fit check failed:
cut words in the Content file and render again. Never shrink type.

Needs: jinja2, playwright with chromium (pip install playwright jinja2 --break-system-packages;
python -m playwright install chromium).
"""
import os as _os_launch
import argparse, json, re, sys, tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
FONTS = (ASSETS / "fonts").as_uri()
LABELS = json.loads((ASSETS / "labels.json").read_text(encoding="utf-8"))
env = Environment(loader=FileSystemLoader(str(ASSETS)), autoescape=select_autoescape(["html", "j2"]))

# Style A palette (same tokens as the website)
VIOLET, VIOLET_INK, INK, GREY, RULE = "#9466FF", "#4B2A9E", "#0B0B0F", "#5A5A66", "#E2E0E8"
TEAL, SLATE = VIOLET, INK   # old names kept for any external caller
BANNED = re.compile(r"\b(top|best|leader|leading|ranked|outperform\w*|laggard|worst|no\. ?1)\b", re.I)



def _launch_args():
    """Use a pre-installed Chromium when PL_CHROMIUM points at it (cloud sessions ship one at
    /opt/pw-browsers/chromium); otherwise Playwright's own download."""
    exe = _os_launch.environ.get("PL_CHROMIUM")
    return {"executable_path": exe} if exe else {}

def next_free(path: Path):
    if not path.exists():
        return path
    n = 2
    while (c := path.with_name(f"{path.stem}_v{n}{path.suffix}")).exists():
        n += 1
    return c


def base_name(c):
    sfx = "_BM" if c.get("lang") == "bm" else ""
    return f"{c['code']}_{c['short_name']}_FY{c['fy']}", sfx


# ------------------------------------------------------------------ chart
def chart_svg(c, L, w=680, h=270, big=False):
    d = c["dtf"]
    years = d["years"]
    series = d["series"]          # [{name, values, role: company|median|index}]
    fs = 28 if big else 11
    left, right, top, bottom = (70, 330, 20, 50) if big else (36, 160, 14, 28)
    vals = [v for s in series for v in s["values"] if v is not None]
    if d["mode"] == 1:
        lo, hi = 0, 100
    else:
        step = 5 if max(vals + [100]) - min(vals + [100]) <= 40 else 10
        lo = step * int(min(vals + [100]) * 0.97 // step)
        hi = step * (int(max(vals + [100]) * 1.03 // step) + 1)
    X = lambda i: left + i * (w - left - right) / max(1, len(years) - 1)
    Y = lambda v: top + (hi - v) * (h - top - bottom) / (hi - lo)
    out = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" font-family="Geist, Arial, sans-serif" font-size="{fs}">']
    ticks = [0, 25, 50, 75, 100] if d["mode"] == 1 else list(range(int(lo), int(hi) + 1, step))
    for t in ticks:
        out.append(f'<line x1="{left}" x2="{w-right}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{RULE}" stroke-width="1"/>')
        out.append(f'<text x="{left-6}" y="{Y(t)+fs/3:.1f}" text-anchor="end" fill="{GREY}">{t}</text>')
    for i, y in enumerate(years):
        out.append(f'<text x="{X(i):.1f}" y="{h-bottom+fs+8}" text-anchor="middle" fill="{GREY}">FY{y}</text>')
    if d["mode"] == 1:
        out.append(f'<line x1="{left}" x2="{w-right}" y1="{Y(100):.1f}" y2="{Y(100):.1f}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="2 3"/>')
        out.append(f'<text x="{w-right+8}" y="{Y(100)+fs/3:.1f}" fill="{INK}">{L["frontier_label"]}</text>')
    styles = {"company": (VIOLET, "", 3), "median": (INK, "6 4", 1.8), "index": (VIOLET, "", 2.5)}
    idx_cols = [VIOLET, INK, GREY]
    text_col = {VIOLET: VIOLET_INK}
    # the frontier label is a label too: a company at 100% must not print its name on top of it
    label_y = [Y(100)] if d["mode"] == 1 else []
    for k, s in enumerate(series[:3]):
        col, dash, sw = styles.get(s["role"], (TEAL, "", 2))
        if s["role"] == "index":
            col = idx_cols[k % 3]; dash = "" if k == 0 else ("6 4" if k == 1 else "2 3")
        pts = [(X(i), Y(v)) for i, v in enumerate(s["values"]) if v is not None]
        if not pts:
            continue
        out.append(f'<polyline fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}" points="' +
                   " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')
        for x, y in pts:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{sw+0.5}" fill="{col}"/>')
        ly = pts[-1][1]
        while any(abs(ly - o) < fs * 1.2 for o in label_y):
            ly += fs * 1.2
        label_y.append(ly)
        out.append(f'<text x="{pts[-1][0]+8:.1f}" y="{ly+fs/3:.1f}" fill="{text_col.get(col, col)}" font-weight="600">{s["name"]}</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ browser checks
FIT_JS = """
() => {
  // Style A flows across pages, so the checks are: nothing wider than the page, type not too small,
  // chart labels inside the chart. Page count is checked on the PDF.
  const px = pt => pt * 96 / 72;
  const res = {wide: [], small_text: []};
  document.querySelectorAll('[data-block]').forEach(el => { if (el.scrollWidth > el.clientWidth + 1) res.wide.push(el.dataset.block); });
  const clipped = [];
  document.querySelectorAll('svg').forEach(svg => { const vb = svg.viewBox.baseVal; if (!vb || !vb.width) return;
    svg.querySelectorAll('text').forEach(t => { const bb = t.getBBox();
      if (bb.x < vb.x - 0.5 || bb.y < vb.y - 0.5 || bb.x + bb.width > vb.x + vb.width + 0.5 || bb.y + bb.height > vb.y + vb.height + 0.5)
        clipped.push(t.textContent); }); });
  res.chart_clipped = clipped;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode; if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (el.closest('svg')) continue;
    const size = parseFloat(getComputedStyle(el).fontSize);
    let min = px(9.5);
    if (el.closest('.note, .chip, .verdict, .glance-h, .gl, .gs, .ctx, .pg, .m, .h, .count, .k, th, .no, .meta, .pill, .appx, .d')) min = px(8);
    else if (el.closest('table, .wd, .rr, .ins, .sw li, .chh p')) min = px(9);
    if (size + 0.05 < min) res.small_text.push({text: n.textContent.trim().slice(0, 40), pt: +(size * 72 / 96).toFixed(1)});
  }
  return res;
}
"""
CARD_JS = """
() => { const m = document.querySelector('.main'); const small = [];
  const clipped = [];
  document.querySelectorAll('svg').forEach(svg => { const vb = svg.viewBox.baseVal;
    svg.querySelectorAll('text').forEach(t => { const bb = t.getBBox();
      if (bb.x < vb.x - 0.5 || bb.y < vb.y - 0.5 || bb.x + bb.width > vb.x + vb.width + 0.5 || bb.y + bb.height > vb.y + vb.height + 0.5)
        clipped.push(t.textContent); }); });

  document.querySelectorAll('#card *').forEach(el => { if (el.closest('svg')) return;
    if ([...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(el).fontSize) < 28)
      small.push(el.textContent.trim().slice(0, 30)); });
  return {overflow: m.scrollHeight > m.clientHeight + 1, small_text: small, chart_clipped: clipped}; }
"""


def browser():
    from playwright.sync_api import sync_playwright
    return sync_playwright()


def check_text(c):
    """Rank words and missing pieces in the Content file (quick guard; pl-lint is the full check)."""
    blob = json.dumps({k: v for k, v in c.items() if k not in ("appendix", "key_initiatives")}, ensure_ascii=False)
    blob = re.sub(r'"quote":\s*"[^"]*"', "", blob)
    return sorted(set(m.group(0).lower() for m in BANNED.finditer(blob)))


# ------------------------------------------------------------------ commands
MIN_PAGES, MAX_PAGES = 3, 6


def render_spotlight(c, out_dir, png_dir=None):
    L = {**LABELS[c.get("lang", "en")], **(c.get("label_overrides") or {})}  # per-company wording (ImprovementLog 2026-11-08)
    groups = {}
    for it in c.get("appendix", []):
        groups.setdefault(int(it["tier"]), []).append(it)
    html = env.get_template("spotlight.html.j2").render(
        c=c, L=L, fonts=FONTS, chart_svg=chart_svg(c, L, 680, 250), appendix_groups=sorted(groups.items()))
    name, sfx = base_name(c)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    pdf = next_free(out_dir / f"{name}_Spotlight{sfx}.pdf")
    tmp = Path(tempfile.mkdtemp()) / "spotlight.html"
    tmp.write_text(html, encoding="utf-8")
    with browser() as p:
        b = p.chromium.launch(**_launch_args())
        pg = b.new_page(viewport={"width": 794, "height": 1123})
        pg.goto(tmp.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
        pg.emulate_media(media="print")
        fit = pg.evaluate(FIT_JS)
        pg.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
        b.close()
    from pypdf import PdfReader
    n_pages = len(PdfReader(str(pdf)).pages)
    pngs = []
    if png_dir:   # page images straight from the PDF, so they match it exactly (200 dpi)
        import pypdfium2 as pdfium
        Path(png_dir).mkdir(parents=True, exist_ok=True)
        doc = pdfium.PdfDocument(str(pdf))
        for i in range(min(4, len(doc))):
            f = next_free(Path(png_dir) / f"{name}_Snap{sfx}_{i+1:02d}.png")
            doc[i].render(scale=200 / 72).to_pil().save(f); pngs.append(str(f))
        doc.close()
    fails = [f"block wider than the page: {w}" for w in fit["wide"]]
    fails += [f"text below minimum size: {s['text']!r} {s['pt']}pt" for s in fit["small_text"][:10]]
    if fit.get("chart_clipped"):
        fails.append(f"chart labels cut off: {fit['chart_clipped']}")
    if not MIN_PAGES <= n_pages <= MAX_PAGES:
        fails.append(f"PDF has {n_pages} pages, expected {MIN_PAGES}–{MAX_PAGES}")
    rank = check_text(c)
    if rank:
        fails.append(f"rank words in content: {rank}")
    saved = [str(pdf)] + pngs
    for s_ in saved:
        assert Path(s_).exists() and Path(s_).stat().st_size > 0, f"save failed {s_}"
    return {"saved": saved, "pages": n_pages, "fit_pass": not fails, "fit_fails": fails}


def render_cards(c, out_dir, start=5):
    L = {**LABELS[c.get("lang", "en")], **(c.get("label_overrides") or {})}  # per-company wording (ImprovementLog 2026-11-08)
    name, sfx = base_name(c)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    tpl = env.get_template("card.html.j2")
    jobs = [("headline", {"src_page": c["headline_results"][0]["page"]}),
            ("snapshot", {"src_page": c["snapshot"].get("source_pages", c["headline_results"][0]["page"])}),
            ("dtf", {"src_page": c["dtf"].get("source_pages", "—"), "chart_svg": chart_svg(c, L, 952, 520, big=True)})]
    for i, l in enumerate(c["lessons"], start=1):
        jobs.append(("lesson", {"lesson": l, "lesson_no": i, "src_page": l["page"]}))
    saved, fails = [], []
    with browser() as p:
        b = p.chromium.launch(**_launch_args())
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        tmpd = Path(tempfile.mkdtemp())
        for n, (kind, extra) in enumerate(jobs, start=start):
            html = tpl.render(c=c, L=L, fonts=FONTS, kind=kind, **extra)
            t = tmpd / f"card{n}.html"; t.write_text(html, encoding="utf-8")
            pg.goto(t.as_uri()); pg.evaluate("document.fonts.ready")
            chk = pg.evaluate(CARD_JS)
            if chk["overflow"]:
                fails.append(f"card {n:02d} ({kind}): text cut off")
            if chk.get("chart_clipped"):
                fails.append(f"card {n:02d}: chart labels cut off: {chk['chart_clipped']}")
            if chk["small_text"]:
                fails.append(f"card {n:02d}: text under 28px: {chk['small_text'][:3]}")
            f = next_free(out_dir / f"{name}_Snap{sfx}_{n:02d}.png")
            pg.query_selector("#card").screenshot(path=str(f)); saved.append(str(f))
        b.close()
    for s in saved:
        assert Path(s).exists() and Path(s).stat().st_size > 0
    return {"saved": saved, "fit_pass": not fails, "fit_fails": fails}


def render_email(c, out_dir):
    if c.get("lang") == "bm":
        return {"saved": [], "note": "No BM email: the EN email links to the BM files."}
    em = c.get("email", {})
    subject = f"Productivity Lens | {c['company']}: {em.get('subject_headline', c['headline'])}"
    preview = em.get("preview", "")
    fails = []
    if len(em.get("subject_headline", c["headline"])) > 60:
        fails.append("subject headline over 60 characters")
    if len(preview) > 90:
        fails.append("preview text over 90 characters")
    links = c.get("links", {"spotlight_pdf": "(path)", "bm_pdf": "(path)", "snapshots": "(path)"})
    L = {**LABELS[c.get("lang", "en")], **(c.get("label_overrides") or {})}
    html = env.get_template("email.html.j2").render(c=c, L=L, subject=subject, preview=preview, links=links)
    if re.search(r"<script|<link|@import", html, re.I):
        fails.append("email contains script or external CSS")
    name, _ = base_name(c)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    f = next_free(out_dir / f"{name}_Newsletter.html")
    f.write_text(html, encoding="utf-8")
    assert f.exists() and f.stat().st_size > 0
    return {"saved": [str(f)], "subject": subject, "preview": preview, "fit_pass": not fails, "fit_fails": fails}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["spotlight", "cards", "email", "all"])
    ap.add_argument("--content", required=True)
    ap.add_argument("--out-dir")
    ap.add_argument("--png-dir")
    ap.add_argument("--root", help="Productivity Lens folder (for 'all')")
    a = ap.parse_args()
    c = json.loads(Path(a.content).read_text(encoding="utf-8"))
    rep = {}
    if a.cmd == "spotlight":
        rep = render_spotlight(c, a.out_dir, a.png_dir)
    elif a.cmd == "cards":
        rep = render_cards(c, a.out_dir)
    elif a.cmd == "email":
        rep = render_email(c, a.out_dir)
    else:
        root = Path(a.root)
        rep["spotlight"] = render_spotlight(c, root / "04_Spotlights", root / "04_Spotlights" / "Snapshots")
        rep["cards"] = render_cards(c, root / "04_Spotlights" / "Snapshots")
        rep["email"] = render_email(c, root / "04_Spotlights" / "Newsletter")
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    ok = rep.get("fit_pass", True) if a.cmd != "all" else all(v.get("fit_pass", True) for v in rep.values())
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
