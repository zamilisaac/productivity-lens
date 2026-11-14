"""Build site/kb.json: the only text the Ask feature (/api/ask) may answer from.

Loads site/index.html in headless Chromium and collects passages from REVIEWED stories only
(companies listed in the PDFS map), in English and Bahasa Melayu, each with its report page.
Run after any change to a reviewed story's data block:

    python scripts/build_kb.py

Uses PL_CHROMIUM if set (cloud sessions: /opt/pw-browsers/chromium).
"""
import json, os, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "site" / "index.html"
OUT = ROOT / "site" / "kb.json"

JS = r"""() => {
  const out = [];
  const strip = s => String(s || "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
  const add = (c, lg, ref, text) => { text = strip(text); if (text) out.push({ slug: c.slug, company: SHORT[c.slug] || c.name.replace(/ (Berhad|Bhd)$/, ""), lang: lg, ref: strip(ref), text }); };
  for (const lg of ["en", "bm"]) {
    lang = lg;
    const P = p => (lg === "bm" ? "hlm." : (String(p).includes(",") ? "pp." : "p.")) + p;
    for (const c of COMPANIES.filter(c => c.reviewed)) {
      const nm = c.name;
      add(c, lg, c.fy, `${nm} (${c.fy}). ${(c.hl && c.hl[lg]) || ""} ${c.headline[lg]}. ${c.intro[lg]}`);
      (c.results || []).forEach(r => add(c, lg, r.page[lg], `${nm}: ${r.label[lg]} ${r.big[lg]} (${r.ctx[lg]}). ${r.insight[lg]}`));
      (c.table || []).forEach(r => add(c, lg, P(r.p), `${nm}: ${r.n[lg]}. ${r.w[lg]}. ${lg === "bm" ? "Keputusan" : "Result"}: ${r.r[lg]}.`));
      (c.lessons || []).forEach(l => add(c, lg, "", `${nm} – ${lg === "bm" ? "idea untuk perniagaan kecil" : "idea for a small business"}: ${l.title[lg]}. ${l.body[lg].join(" ")}`));
      (c.snapshot || []).forEach(s => add(c, lg, c.fy, `${nm}: ${s.k[lg]} ${s.v} (${s.cs} ${lg === "bm" ? "berbanding tahun lepas" : "vs last year"}).`));
      ["strengths", "watch"].forEach(k => (c[k] && (c[k][lg] || c[k])).forEach && (c[k][lg] || c[k]).forEach(x => add(c, lg, "", `${nm}: ${typeof x === "string" ? x : (x[lg] || x.t || JSON.stringify(x))}`)));
      const X = (typeof DTF_CO_TXT !== "undefined") && DTF_CO_TXT[c.slug], D = DTF.co[c.slug];
      if (X && D) add(c, lg, "", `${nm}: ${DTF_TXT[lg].line(D)} ${X[lg].a}`);
    }
  }
  return out;
}"""

def main():
    exe = os.environ.get("PL_CHROMIUM")
    with sync_playwright() as p:
        b = p.chromium.launch(**({"executable_path": exe} if exe else {}))
        pg = b.new_page()
        pg.goto(SITE.as_uri())
        pg.wait_for_timeout(300)
        chunks = pg.evaluate(JS)
        b.close()
    OUT.write_text(json.dumps({"built": "from site/index.html (reviewed stories only)", "chunks": chunks}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(chunks)} passages -> {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
