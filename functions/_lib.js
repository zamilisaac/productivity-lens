// Shared helpers for the newsletter sign-up (Cloudflare Pages Functions + D1).
// Files starting with "_" are not routes. The D1 database is bound to the Pages project as `DB`.

// Bump this when the privacy notice changes; it is stored with each consent.
export const CONSENT_VERSION = "2026-11-15-3";

export const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

const EMAIL_RE = /^[^\s@"<>]{1,64}@[^\s@"<>]{1,190}\.[A-Za-z]{2,24}$/;

export function cleanEmail(v) {
  const e = String(v ?? "").trim().toLowerCase();
  return e.length <= 254 && EMAIL_RE.test(e) ? e : null;
}

export async function readBody(request) {
  const type = request.headers.get("content-type") || "";
  if (type.includes("application/json")) return await request.json().catch(() => ({}));
  if (type.includes("form")) return Object.fromEntries(await request.formData());
  return {};
}

// Only accept posts from this site's own pages (simple guard against cross-site posting).
export function sameOrigin(request) {
  const origin = request.headers.get("origin");
  if (!origin) return true;
  return origin === new URL(request.url).origin;
}

// Data minimisation: email, language, consent time and notice version only. No IP address, no tracking.
export async function ensureTable(db) {
  await db
    .prepare(
      "CREATE TABLE IF NOT EXISTS subscribers (" +
        "email TEXT PRIMARY KEY, lang TEXT NOT NULL, consent_at TEXT NOT NULL, " +
        "consent_version TEXT NOT NULL, source TEXT, created_at TEXT NOT NULL)"
    )
    .run();
}
