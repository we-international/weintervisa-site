---
name: website-lead-forms
description: Use when adding or changing a lead form on weintervisa.com (or any static site) that sends to GetWec — payload contract, preview safety, consent, tests with a mocked live endpoint. Roles: web dev, CRM/Mia, QA, UX.
---
# Website lead forms → GetWec (learned 18 Nov 2026)

## Contract (no GetWec change needed)
- Post to the GetWec `mia` Edge Function with `action: "lead"` — the same call the Mia web chat uses:
  `full_name, email, phone, location (thailand|australia|other), interest (≤300), consent:true, marketing, transcript:[{role:"user",text≤1000}], lang, page, website` (`website` = honeypot, must be empty).
- GetWec creates contact (dedupe by email) + case "interested" + Inbox conversation + Mia event + follow-up task.
- Put a short summary in `interest` ("Study application · Course area: … · Start: …") and the full form text in the transcript, so staff see everything in the Inbox.
- Email OR phone/LINE (≥5 chars) is enough; name ≥2 chars; consent required. Check the same rules in the browser.
- Keep a copy of GetWec `validateLead` in `tests/getwec-lead-contract.mjs`; e2e runs every form payload through it. If GetWec changes the contract, update both in the same week.
- Known gap (fix in getwec): leads from forms are stored as `source: 'chat'` and subject "Website chat: …". Add a `source`/`form` field when the repo is reachable.

## Safety
- Endpoint + **public anon key** go in `<meta name="getwec-endpoint|getwec-key">`, written only by a `--production` build when `config.json` has the key. Preview builds never send (the form says "Preview: not connected").
- Never ask for passport numbers or uploads on public forms (those live in the GetWec back office only). Say so under the form.
- Every form: consent box + privacy link, optional marketing box (unticked), "not a migration agent → registered migration agent" note.
- No promises the owner has not approved (reply time, "free consultation", guarantees) — tests grep for them.
- No cookies/trackers; nothing stored in the browser.

## Tests (QA)
- Preview: empty submit shows errors; filled submit → `window.__lastLeadPayload` passes the contract.
- Live without a real backend: `page.route(<page>)` → `route.fetch()` and inject the two meta tags; `page.route(<endpoint>)` fulfils `{"ok":true}`. Assert one POST, `apikey` header, contract OK, success text, form reset.
- Screenshot phone + desktop forms into Drive for review.

## UX gotchas
- A checkbox label using `display:flex` splits inline links into their own column → wrap the label text in one `<span>`.
- Inputs ≥44px high, `font: inherit` (stops iOS zoom), two-column rows only from 600px.
- Fetching our own live site with WebFetch needs a person to approve it, so an unattended run cannot copy Wix page text that way; Wix REST has no API for editor page text. Get page copy from the owner/team or a run with a browser.

## Migration agent cards on /migration-support (20 Nov 2026, WEI-MIG-FORM-1120)
- Agents sign up on the GetWec form (`https://getwec.pages.dev/partners/migration/`), not on this site. Staff check the MARN + the agent's website in GetWec and press "show on website".
- The site never calls GetWec from the visitor's browser for this (no extra requests, no trackers). CI fetches `GET <getwec_endpoint>?action=migration_partners` at build time (main, every 6 hours, or manual run) into `content/migration-partners.json`; if GetWec is down the committed snapshot stays.
- `content_pages.partner_cards()` escapes every value, skips entries without an https link, uses `rel="noopener nofollow"`, and never shows the agent's personal name (GetWec does not send it).
- Page text must keep: "We are not a migration agent", "We don't receive any commission or benefit from listed agents", check the MARN on the official register. Tests in `tests/test_site.py` section 11.
- The email allowlist test also allows the listed agents' own contact emails (from the JSON), nothing else.

## New form kinds (25 Nov 2026)
- GetWec accepts any `form` kind matching `^[a-z][a-z0-9_]{1,39}$` and stores the contact as `source: form:<kind>` — a new site form needs no GetWec change. Add a readable label to the `label` map in `assets/forms.js` (e.g. `whv_enrol: 'Working Holiday enrolment'`) so staff see it as the Inbox subject.
- A form without a phone field must make email required in HTML; the browser check puts the "email or phone" error under the email field.
- A fixed answer (e.g. everyone on a WHV page is in Australia) can be a hidden input (`location=australia`).
- Add every new form page to the forms loop in `tests/e2e.mjs` (preview + contract) and to `urls` (not to `content`, which is also checked under /th/).
