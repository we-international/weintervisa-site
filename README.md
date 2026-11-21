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
- `home_page.py` — home page `/` rebuilt on 21 Nov 2026 from the LIVE Wix home page (`content/home.json`, from the compare run's saved text + markup): hero, homestay band (AHN), 7 'which one sounds like you' paths, popular Cert III courses, study areas + all study-area groups → `/courses#<group>`, how we help, video link, English practice + quiz, 3 steps, FAQ, latest posts, Organization + WebSite schema. Images show once `tools/fetch_images.py` has copied them.
- `fasttrack_page.py` + `content/fast-track.json` — `/fast-track-courses` (Working Holiday 417/462) rebuilt from the live Wix page the same way: course picker → course cards, 3 steps, Cert III courses, video, where it can lead, settle in (AHN homestay, cover, first-week checklist), FAQ, WHM news, guides.
- `englishpractice_page.py` + `content/english-practice.json` — `/english-practice` rebuilt from the live Wix page: 8-question quiz (no script), Say It Wrong + Wobbi Says channels, games (WE International Game Studio), English courses, KindozaStudio kids' printables.
- `homestay_page.py` + `content/homestay.json` — `/homestay` rebuilt from the live Wix page: AHN partner link, scam warning, why homestay first, 6 steps, AHN prices 2026/2027 (dated 26 Oct 2026, source), house rules, FAQ.
- `nursing_page.py` (`content/nursing.json`), `oshc_page.py` (`content/oshc.json`), `about_page.py` (`content/about.json`, `content/referral-partners.json`) — rebuilt from the live Wix pages on 22 Nov 2026; `/contact-us` and `/student-services` expanded the same day (Messenger, booking, where to start).
- `schools.py` + `content/schools.json` — school pages `/schools` and `/schools/<slug>` from files schools sent us (only schools that replied). `"approved": false` = preview only; production leaves them out until the owner approves. Skill: `.claude/skills/school-promo-pages`.
- `assets/forms.js` — lead forms → GetWec `mia` Edge Function `action: "lead"` (contract copy: `tests/getwec-lead-contract.mjs`). Sends only in a `--production` build with `getwec_anon_key` set in `config.json`; preview never sends. Skill: `.claude/skills/website-lead-forms`.

- `thai_pages.py`, `thai_content.py`, `thai_more.py` — Thai pages `/th/...` (every page except `/privacy-policy` and post bodies). Skill: `.claude/skills/website-thai-pages`.

Wix-app pages (owner 20 Nov 2026: rebuild in GetWec): /partner-portal → GetWec partner portal, /schedule → GetWec /book/ (redirects); still to build: /videos, /challenges (`tests/pending-pages.json`). Privacy notice approved by the owner on 20 Nov 2026. Images: the 27 blog images are local in `assets/img/` (copied by the workflow "Copy Wix images into the repo", 21 Nov 2026); the test fails if any page loads an image from Wix. /videos and /challenges: the Wix apps hold no content (0 programmes, no video library) → owner to choose redirect or a later GetWec feature.

- `tools/live_urls.py` + `tools/compare_shots.mjs` (workflow "Live Wix vs new site", CI only, read-only): live sitemap URLs must all exist here (`tests/wix-live-urls.json`), and Wix-vs-new screenshots go to a `review/compare-<run>` branch. Blog categories: `content/blog-categories.json` → `/blog/categories/<slug>`.
