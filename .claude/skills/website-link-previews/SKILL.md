---
name: website-link-previews
description: Use when adding or changing a page on the new weintervisa.com site (or any static site the Web & CRM team owns), when a shared link shows no picture on Facebook, LINE or WhatsApp, or before the DNS day. Every page gets one absolute JPEG/PNG og:image, og:type, og:locale and a large-image card; Thai pages get the Thai card. Roles: SEO, web dev, QA. Learned 28 Nov 2026.
---
# Link previews (Open Graph) — learned 28 Nov 2026

Students share our pages in LINE and Facebook groups. A link with no picture looks like spam and gets fewer taps.
The SEO site check (GetWec #/seo) scored the site 100 but does not look at previews, so this was missed:
60 of 99 pages had no `og:image`, and the 39 that had one used a **relative** path (`/assets/img/...`),
which Facebook, LINE and WhatsApp ignore.

## Rules (build.py `share_meta()`)
- One `og:image` per page, always absolute: `https://www.weintervisa.com/assets/...` (same host as the canonical).
- Pick order: the page's own picture (post cover, else the first `/assets/img/` image in the body) → the default card.
- JPEG or PNG only. A WebP picture falls back to the card, because not every chat app shows WebP previews.
- Default card: `assets/share-en.png` / `assets/share-th.png`, 1200x630, drawn by `node tools/share_image.mjs`
  (Playwright, local fonts, 0 credits). Thai pages always use the Thai card. Home uses the card, not a photo.
- Also on every page: `og:type` (`article` for /post/, else `website`), `og:site_name` "We International",
  `og:locale` (`en_AU` / `th_TH`), `twitter:card` = `summary_large_image`.
- The card text is the home heading + one plain line + the domain. No people's names, no QEAC name, no promises.
  Redraw both cards when the home heading changes.

## Checks
- `tests/test_site.py`: every page has exactly one absolute JPEG/PNG og:image whose file is in the build,
  one og:type, one twitter card; no Thai page uses the English card; cards are 1200x630 (read from the PNG header,
  CI has no Pillow).
- On preview the image URLs point at www.weintervisa.com (still Wix), so previews only work after the DNS day.
  After the switch, paste 2–3 URLs into the Facebook Sharing Debugger (free, read-only) to refresh its cache.

## Mistakes to avoid
- Thai on a card: write the line break yourself (`<br>` at the space). Chromium breaks Thai at odd places.
- `import { chromium } from 'playwright'` fails in this repo's tools (ESM ignores NODE_PATH): use
  `createRequire(import.meta.url)('playwright')` like `tools/compare_shots.mjs`.
