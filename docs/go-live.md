# weintervisa.com go-live (DNS day) — runbook

Owner presses every DNS / settings button; the team prepares, checks and watches. Nothing here
is done by a scheduled run. Wix stays paid and online until 15 Feb 2027, so it is the fallback.

## 0. Current DNS (read-only snapshot, workflow "DNS snapshot", 22 Nov 2026)

| Record | Value now | DNS day |
|---|---|---|
| NS | ns14.wixdns.net, ns15.wixdns.net (domain registered at Wix until 15 Feb 2031) | keep |
| `@` A | 185.230.63.107 / .171 / .186 (Wix), TTL 3600 | **change** → GitHub Pages |
| `www` CNAME | cdn3.wixdns.net, TTL 3600 | **change** → `we-international.github.io` |
| MX | aspmx.l.google.com (10), alt1–alt4 (20–50) — Google Workspace for info@ | **keep, do not touch** |
| TXT `@` | `v=spf1 include:_spf.google.com ~all`, `google-site-verification=…` | **keep** |
| DKIM `google._domainkey` / DMARC `_dmarc` | none | not needed for the move (see note 6) |
| AAAA, CAA | none | add AAAA (below); no CAA needed |

Run the workflow again on the day before (Actions → "DNS snapshot (read-only)" → Run) and compare.

## 1. Two days before (owner, 5 minutes)
1. Wix → Domains → weintervisa.com → Manage DNS records: lower TTL of the `@` A records and the `www` CNAME
   to the lowest Wix allows (e.g. 1 hour → the shortest option). Do not touch MX / TXT.
2. GitHub → organisation we-international → Settings → Pages → "Add a domain" → `weintervisa.com`.
   GitHub shows one TXT record `_github-pages-challenge-we-international` → add it in Wix DNS → "Verify".
   (Stops anyone else from using the domain on GitHub Pages.)

## 2. DNS day — pick a quiet hour (e.g. 22:00 Sydney, weekday)
1. **Team** opens the go-live PR (do not merge yet): `config.json` → `"live": true` and
   `"getwec_anon_key": "<public anon key>"` (the anon key is public; the service key never goes here).
   CI must be green: `tests/test_site.py` + `tests/test_production.py` + e2e.
2. **Owner**: Supabase → GetWec project → Edge Functions → `mia` → secret `ALLOWED_ORIGINS` includes
   `https://www.weintervisa.com,https://weintervisa.com` (GetWec `docs/GO-LIVE.md`).
3. **Owner**: weintervisa-site repo → Settings → Pages → Custom domain = `www.weintervisa.com` → Save.
   (DNS still points at Wix, so visitors see nothing change yet.)
4. **Team** merges the go-live PR right away and waits for "Build and deploy" to be green → GitHub now serves the
   production build (indexable, canonical www, forms connected). Do this *before* the DNS change, so no visitor
   ever gets the preview build.
5. **Owner**, in Wix DNS:
   - `@` A: replace the three Wix IPs with `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `@` AAAA (add): `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `www` CNAME: `cdn3.wixdns.net` → `we-international.github.io`
   - MX, TXT: unchanged.
6. When Settings → Pages shows the certificate is ready (usually minutes, up to an hour): tick **Enforce HTTPS**.
   Until then some visitors may see a certificate warning on https — this is why we pick a quiet hour.

## 3. Checks right after (team, from CI or a browser)
- https://www.weintervisa.com/ and https://weintervisa.com/ (→ www) load; padlock OK.
- 5 old URLs: `/post/<any slug>`, `/courses`, `/homestay`, `/welcome` (→ `/`), `/games` (→ weintergames.com).
- `/robots.txt` says `Allow: /` + sitemap; a page source has no `noindex`.
- Send `/contact-us` once with sample data ("Test (sample)", test@example.com) → it appears in GetWec Inbox → close it.
- Email: send a test to info@ from outside and reply — MX unchanged, so it must work as before.
- Google Search Console (domain already verified by the TXT record): submit `https://www.weintervisa.com/sitemap.xml`.

## 4. Rollback (if anything is wrong)
Put the old records back in Wix DNS: `@` A 185.230.63.107 / .171 / .186 (remove the GitHub A/AAAA) and
`www` CNAME `cdn3.wixdns.net`. The Wix site is still published, so it comes back as the TTL runs out.

## 5. After
- Watch 404s for 2 weeks (GitHub Pages has no logs: check Search Console → Pages → Not found).
- Wix forms stay on until the new forms have worked for a week (policy-zoho-retire); then propose closing them.
- Before 15 Feb 2027 (owner): move the Google Workspace subscription for info@ from Wix to Google directly,
  and decide whether the domain stays at Wix (paid to 2031, DNS keeps working) or moves to VentraIP.

## 6. Note (not part of the move)
The snapshot shows no DKIM and no DMARC for weintervisa.com. Mail from info@ is more likely to land in spam
without them. Both are free: Google Admin → Apps → Gmail → Authenticate email → generate DKIM → add the TXT in
Wix DNS → Start authentication; then add `_dmarc` TXT `v=DMARC1; p=none; rua=mailto:info@weintervisa.com`.
Owner decides; it can be done any day, independent of the website.
