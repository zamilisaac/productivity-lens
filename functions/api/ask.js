// POST /api/ask  {q, lang: "en"|"bm"}
// Answers questions ONLY from reviewed stories (site/kb.json, built by scripts/build_kb.py).
// Needs a Workers AI binding named `AI` on the Pages project. Without it, the passages that match
// the question are returned instead of an AI answer. Questions are not stored or logged.
import { json, readBody, sameOrigin } from "../_lib.js";

const MODELS = ["@cf/meta/llama-3.3-70b-instruct-fp8-fast", "@cf/meta/llama-3.1-8b-instruct"];
const STOP = new Set(("the a an and or of to in on for with what how why did does do is are was were it its this that from by at as be can " +
  "about which who when where much many more less than into their they them there have has had will would could should your you our we " +
  "yang dan atau di ke dari daripada untuk dengan apa bagaimana kenapa mengapa ini itu ialah adalah ada boleh tentang syarikat " +
  "pada oleh sebagai juga lebih kurang mereka kami kita anda saya telah sudah akan dalam bagi").split(" "));
const RANK = /\b(top|best|leaders?|leading|ranked|rankings?|outperform\w*|laggards?|worst|terbaik|teratas|terburuk|juara)\b/i;

let KB = null;
async function loadKb(env, request) {
  if (KB) return KB;
  const r = await env.ASSETS.fetch(new URL("/kb.json", request.url));
  KB = (await r.json()).chunks || [];
  return KB;
}

const words = s => String(s).toLowerCase().normalize("NFKD").replace(/[^\p{L}\p{N}\s.%]/gu, " ").split(/\s+/)
  .map(w => w.replace(/\.$/, "")).filter(w => w.length > 2 && !STOP.has(w));

function retrieve(chunks, q, lang) {
  const qs = [...new Set(words(q))];
  if (!qs.length) return [];
  const scored = chunks.filter(c => c.lang === lang).map(c => {
    const t = c.text.toLowerCase(), co = c.company.toLowerCase();
    let s = 0;
    for (const w of qs) {
      if (co.includes(w)) s += 1.5;
      else if (t.includes(w)) s += 1;
      else if (w.length > 5 && t.includes(w.slice(0, 5))) s += 0.5; // stems: capacity/kapasiti, consolidat…
    }
    return { c, s };
  }).filter(x => x.s >= 1).sort((a, b) => b.s - a.s);
  return scored.slice(0, 6).map(x => x.c);
}

// Every number in the answer must appear in the passages ("no quote, no number").
const nums = s => (String(s).match(/\d[\d,]*(?:\.\d+)?/g) || []).map(n => n.replace(/,/g, "")).filter(n => n.length > 0);
function numbersBacked(answer, ctx) {
  const have = new Set(nums(ctx));
  return nums(answer).every(n => have.has(n));
}

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json(403, { status: "error", error: "forbidden" });
  const body = await readBody(request);
  const q = String(body.q || "").trim().slice(0, 300);
  const lang = body.lang === "bm" ? "bm" : "en";
  if (q.length < 3) return json(400, { status: "error", error: "empty" });

  const hits = retrieve(await loadKb(env, request), q, lang);
  const sources = hits.map(c => ({ slug: c.slug, company: c.company, ref: c.ref, text: c.text }));
  if (!hits.length) return json(200, { status: "none" });
  if (!env.AI) return json(200, { status: "sources", reason: "no_ai", sources });

  const ctx = hits.map((c, i) => `[${i + 1}] ${c.company}${c.ref ? ` (${c.ref})` : ""}: ${c.text}`).join("\n");
  const sys = (lang === "bm"
    ? "Anda pembantu Productivity Lens. Jawab dalam Bahasa Melayu yang mudah, maksimum 120 patah perkataan. Guna HANYA fakta dalam PETIKAN. Jangan tambah angka, syarikat atau fakta lain. Selepas setiap fakta, letak rujukan halaman dalam kurungan seperti (Farm Fresh, hlm.23). Jika petikan tidak menjawab soalan, jawab tepat: TIADA. Jangan menyusun atau membandingkan syarikat sebagai terbaik atau terburuk. Bukan nasihat pelaburan."
    : "You are the Productivity Lens assistant. Answer in plain English, at most 120 words. Use ONLY facts in the PASSAGES. Do not add any number, company or fact that is not in them. After each fact put the page reference in brackets, like (Farm Fresh, p.23). If the passages do not answer the question, reply exactly: NONE. Never rank companies or call any best, top or worst. Not investment advice.");
  const messages = [{ role: "system", content: sys }, { role: "user", content: `PASSAGES:\n${ctx}\n\nQUESTION: ${q}` }];

  let answer = "";
  for (const m of MODELS) {
    try { const r = await env.AI.run(m, { messages, max_tokens: 350, temperature: 0.1 }); answer = String(r.response || "").trim(); if (answer) break; }
    catch (e) { /* try the next model */ }
  }
  if (!answer) return json(200, { status: "sources", reason: "no_ai", sources });
  if (/^(NONE|TIADA)\b/i.test(answer)) return json(200, { status: "none" });
  if (!numbersBacked(answer, ctx + " " + q) || RANK.test(answer)) return json(200, { status: "sources", reason: "unchecked", sources });
  return json(200, { status: "answer", answer, sources });
}

export const onRequest = () => json(405, { status: "error", error: "method_not_allowed" });
