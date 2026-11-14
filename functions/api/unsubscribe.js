// POST /api/unsubscribe  {email}
// Deletes the address and everything stored with it. The reply is the same whether or not the address was
// on the list, so the form cannot be used to find out who has subscribed.
import { json, cleanEmail, readBody, sameOrigin, ensureTable } from "../_lib.js";

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json(403, { ok: false, error: "forbidden" });
  if (!env.DB) return json(503, { ok: false, error: "not_configured" });
  const body = await readBody(request);
  const email = cleanEmail(body.email);
  if (!email) return json(400, { ok: false, error: "invalid_email" });
  await ensureTable(env.DB);
  await env.DB.prepare("DELETE FROM subscribers WHERE email = ?1").bind(email).run();
  return json(200, { ok: true });
}

export const onRequest = () => json(405, { ok: false, error: "method_not_allowed" });
