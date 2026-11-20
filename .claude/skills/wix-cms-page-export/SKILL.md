---
name: wix-cms-page-export
description: Use when a Wix page's text is needed for the new weintervisa.com but the live page cannot be read (JS-rendered body, proxy blocks the browser). Read the site's own CMS collections read-only through the Wix MCP and rebuild the page in plain English. Learned 19 Nov 2026 (16 pending pages → 12 built).
---

# Wix page text when the live page cannot be read

## What happened
- WebFetch of weintervisa.com returns only the title, meta description, menu and footer: the page body is drawn by JavaScript (Velo), so the fetcher sees no content.
- A headless browser from the cloud run is blocked by the proxy (ERR_TUNNEL_CONNECTION_FAILED). Do not keep retrying or look for other ways round it.
- The Wix Pages/Editor content is not in the REST API either.

## What works (read-only)
1. `GetSiteContext` (site id `412bcdd9-1f44-4690-a488-1bb8cbad3177`) → "Velo: Enabled" is the hint that pages read from CMS collections.
2. `ExecuteWixAPI`: `GET https://www.wixapis.com/wix-data/v2/collections` → list collections; count each NATIVE one with `POST /wix-data/v2/items/query` (`paging.limit 1`, `returnTotalCount`).
3. Page copy lives in **WEIWebsitePages** (24 drafts: slug, heading, intro, sections.items[{heading, body}], seoTitle, seoDescription, cta). Study areas in **WEICourseCategories** (45: title, group, description, status = provider agreement pending).
4. Export only those content collections. **Never read** StudentApplications, Partner* or Members/* (personal data) — count only.
5. Large results are saved to a tool-results file: parse that file with Python, save to `content/*.json` in the repo (content only, no `_owner`).

## Rebuild rules
- Map CMS slugs to the live Wix paths (about → /about-we-international, working-holiday → /fast-track-courses, accommodation → /homestay, partner-with-us → /referral-partners, faq → /frequently-asked-questions, privacy → /privacy-policy …).
- Rewrite in short, plain English; keep every caveat (not a promise, check before booking, no visa outcome guaranteed); never name an unverified partner.
- Pages with no draft (nursing): write only general public facts (NMBA/Ahpra decide registration; OBA = NCLEX-RN then OSCE) + "check the official site".
- Privacy notice must match what the new site really does (forms + chat → GetWec in Sydney, no cookies, AI assistant) and is marked "draft for owner review".
- Tests: each content page exists, one h1, SEO description, no unapproved promises; visa pages say "registered migration agent"; sitemap count = posts + 2 + static pages; remove built paths from `tests/pending-pages.json`.

## Home page (20 Nov 2026)
- The home draft is `WEIWebsitePages` slug `home` (kind home: heading, intro, cta + ctaTarget, 4 sections, seoTitle/Description). Query the collection once and filter by slug in code; return only content fields (drop `_owner`, `_id`).
- Save it as `content/home.json` and render from that file (never hard-code the copy) so a later CMS re-export is a one-file change.
- Link study-area groups to `/courses#<group-id>` and test that every chip has a matching `id` on /courses (same slug function on both pages).
- The live home is at `/welcome`; the new home is `/` and `/welcome` redirects there. Wix cover images still point at static.wixstatic.com (blocked from the cloud run) → cards show the empty frame until `tools/fetch_images.py` runs in CI.

## Left for the owner
Wix-app pages cannot be copied as static pages: /partner-portal (Members + Partner* collections), /schedule (Bookings), /videos (Wix Video), /challenges (Online Programs). Ask the owner: rebuild in GetWec, link out, or drop with a redirect.
