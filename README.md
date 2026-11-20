# weintervisa.com — new static site (moving off Wix)

Owner: We International Education & Visa Pty Ltd · Team: Web & CRM.

- `content/posts/*.md` — the 37 live blog posts exported read-only from the Wix Blog API (17 Nov 2026).
- `build.py` — builds `site/` (preview mode by default: noindex + robots Disallow). `--production` only after the owner approves the DNS switch.
- URLs stay the same as Wix: `/post/<slug>` is `site/post/<slug>.html` (GitHub Pages serves it without `.html` or a trailing slash). Feed stays at `/blog-feed.xml`.
- `/welcome` → `/`, `/games` → https://weintergames.com/ (Games removed from the menu).
- `tools/fetch_images.py` — copies Wix-hosted images into `assets/img/` (run where static.wixstatic.com is reachable, e.g. the CI runner).
- Tests: `python3 tests/test_site.py` (URLs, links, no personal data, no trackers, legal footer, feed, sitemap) and `node tests/e2e.mjs` (phone + desktop, all URLs, no sideways scroll, screenshots).
- Rules: no cookies/analytics until the privacy page says so · no personal names or emails (only info@weintervisa.com) · QEAC shows the number only · we are not a migration agent (refer to a registered migration agent) · never change DNS or close Wix ourselves — propose to the owner.

- `pages.py` — form pages: `/contact-us` (enquiry form) and `/charter-application` (study application form).
- `content_pages.py` — 12 content pages at the Wix paths (about, courses + 45 study areas, nursing pathways, fast-track, English, student services, homestay, OSHC, migration support, referral partners, FAQ, privacy). Source: the Wix CMS drafts `WEIWebsitePages` + `WEICourseCategories` (read-only export → `content/study-areas.json`). Skill: `.claude/skills/wix-cms-page-export`.
- `assets/forms.js` — lead forms → GetWec `mia` Edge Function `action: "lead"` (contract copy: `tests/getwec-lead-contract.mjs`). Sends only in a `--production` build with `getwec_anon_key` set in `config.json`; preview never sends. Skill: `.claude/skills/website-lead-forms`.

Still to decide (owner): 4 Wix-app pages in `tests/pending-pages.json` — /partner-portal, /schedule, /videos, /challenges. Privacy notice is a draft for owner review. Local copies of images still to do.
