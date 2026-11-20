---
name: wix-to-static-migration
description: Use when moving weintervisa.com (or any Wix site) to a free static host without breaking URLs — exporting Wix Blog posts, keeping /post/<slug>, redirects, preview noindex, tests. Roles: web dev, SEO, QA.
---
# Wix → static site (learned 17 Nov 2026)

## Export blog posts (read-only)
- Wix Blog `POST https://www.wixapis.com/blog/v3/posts/query` with `fieldsets: ["RICH_CONTENT","SEO","URL"]`, sort `firstPublishedDate DESC`, `paging.limit` ≤ 100.
- Convert Ricos → Markdown **inside** ExecuteWixAPI (PARAGRAPH, HEADING, lists, BLOCKQUOTE, DIVIDER, IMAGE, TABLE; TEXT decorations BOLD/ITALIC/LINK). Return a `unknown` node-type counter so nothing is lost silently (we found 1 VIDEO → `{{youtube ID}}`).
- ExecuteWixAPI truncates results over ~25k tokens (~100k chars) and the JSON breaks. Page it: 37 posts ≈ 120k chars → 2 calls of 19. Large tool output is saved to a file → parse it with Python instead of re-typing (saves tokens).
- `seoData.tags`: title tag = `type:"title"` (`children`), description = `type:"meta"` with `props.name=="description"`. Many posts have none → fall back to title/excerpt.
- The live post URL is `https://www.weintervisa.com/post/<slug>` (`fieldsets URL` confirms it).

## Keep every URL
- GitHub Pages serves `/post/<slug>` from `post/<slug>.html` (no trailing slash, no redirect) → write that file, not `post/<slug>/index.html` (that adds a 301 to `/slug/`).
- Same feed path as Wix: `/blog-feed.xml`. Old home `/welcome` → `/`. Static redirects = meta refresh + canonical + noindex.
- Turn absolute links to our own domain into site-relative links so the preview host works.
- A link test over all built pages finds dead links that are **already broken on Wix** (17 Nov: Head On post → missing "what's on in October" post). Redirect them to /blog and report.

## Preview safety
- Preview build: `<meta name=robots content=noindex>` on every page + `robots.txt Disallow: /`; no CNAME until the owner approves the DNS day. `--production` flips both.
- Sandbox can't reach weintervisa.com or static.wixstatic.com (proxy 403) → images look broken in local screenshots; copy them with `tools/fetch_images.py` from CI before the switch (Wix media may stop after the plan ends).

## Checks (tests/test_site.py + tests/e2e.mjs)
All Wix slugs exist · no broken internal links (pages still to build listed separately) · no personal name/email, only info@weintervisa.com · no trackers/cookies · footer: company name, QEAC number only, "not a migration agent" · feed/sitemap counts · phone 375px + desktop: status, one h1, no sideways scroll.
- In ESM tests, load the global Playwright with `createRequire(import.meta.url)("playwright")` (NODE_PATH does not work for `import`).

- 2026-11-20: the preview lives at a project page (we-international.github.io/weintervisa-site/), so root-relative links (/assets/site.css, /post/...) broke and the page showed unstyled. The Pages workflow now rebuilds with `SITE_BASE=/weintervisa-site` before upload (build.py `apply_base_path`, preview only). Tests still run on the plain build. Drop the step on the DNS day (custom domain serves from the root).
