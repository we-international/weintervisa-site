// Copy of GetWec validateLead (getwec repo: supabase/functions/_shared/mia-core.js, app v1, 14 Nov 2026).
// The site's forms must produce payloads this accepts. If GetWec changes the contract, update both.
const EMAIL_RE = /^[^@\s]{1,64}@[^@\s]{1,190}\.[a-z]{2,}$/i;
export function validateLead(input) {
  const errors = {};
  const v = {
    full_name: String(input.full_name || '').trim().slice(0, 120),
    email: String(input.email || '').trim().toLowerCase().slice(0, 200),
    phone: String(input.phone || '').trim().slice(0, 60),
    interest: String(input.interest || '').trim().slice(0, 300),
    consent: input.consent === true,
  };
  if (input.action !== 'lead') errors.action = 'must be lead';
  if (v.full_name.length < 2) errors.full_name = 'required';
  if (v.email && !EMAIL_RE.test(v.email)) errors.email = 'invalid';
  if (!v.email && v.phone.length < 5) errors.contact = 'email_or_phone';
  if (!v.consent) errors.consent = 'required';
  if (String(input.website || '').trim()) errors.bot = 'honeypot';
  if (input.location && !['thailand', 'australia', 'other'].includes(input.location)) errors.location = 'unknown';
  if (String(input.interest || '').length > 300) errors.interest = 'too long (would be cut)';
  for (const m of input.transcript || []) if (String(m.text).length > 1000) errors.transcript = 'too long (would be cut)';
  return { ok: Object.keys(errors).length === 0, errors };
}
