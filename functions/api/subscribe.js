// POST /api/subscribe  {email, lang: "en"|"bm", consent: true, source?, website? (honeypot)}
import { CONSENT_VERSION, json, cleanEmail, readBody, sameOrigin, ensureTable } from "../_lib.js";

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json(403, { ok: false, error: "forbidden" });
  if (!env.DB) return json(503, { ok: false, error: "not_configured" });
  const body = await readBody(request);
  if (body.website) return json(200, { ok: true }); // honeypot filled: a bot; say ok, store nothing
  const email = cleanEmail(body.email);
  if (!email) return json(400, { ok: false, error: "invalid_email" });
  if (!(body.consent === true || body.consent === "on" || body.consent === "true"))
    return json(400, { ok: false, error: "consent_required" });
  const lang = body.lang === "bm" ? "bm" : "en";
  const source = String(body.source || "site").replace(/[^a-z0-9-]/gi, "").slice(0, 40) || "site";
  const now = new Date().toISOString();
  await ensureTable(env.DB);
  await env.DB.prepare(
    "INSERT INTO subscribers (email, lang, consent_at, consent_version, source, created_at) VALUES (?1, ?2, ?3, ?4, ?5, ?3) " +
      "ON CONFLICT(email) DO UPDATE SET lang = excluded.lang, consent_at = excluded.consent_at, consent_version = excluded.consent_version"
  )
    .bind(email, lang, now, CONSENT_VERSION, source)
    .run();
  return json(200, { ok: true });
}

export const onRequest = () => json(405, { ok: false, error: "method_not_allowed" });
