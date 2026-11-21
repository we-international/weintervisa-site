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
  - How (21 Nov 2026): workflow **"Copy Wix images into the repo"** (`.github/workflows/fetch-wix-images.yml`, `workflow_dispatch`, `contents: write`). The runner downloads the images, fails if any `static.wixstatic.com` link is left, runs the tests and pushes a NEW branch `claude/local-images-<run id>` committed as We International (never main). Then open a PR from that branch; a push made with `GITHUB_TOKEN` does not start CI, so add one small commit yourself (or re-run) so the PR checks run, then fast-forward main.
  - A workflow file must be on main before `workflow_dispatch` can run it: merge the workflow first, trigger it second.
  - `tests/test_site.py` counts Wix-hosted post images ("must be 0 before the DNS switch") and fails if a post points at a local image that is not in the repo.

## Checks (tests/test_site.py + tests/e2e.mjs)
All Wix slugs exist · no broken internal links (pages still to build listed separately) · no personal name/email, only info@weintervisa.com · no trackers/cookies · footer: company name, QEAC number only, "not a migration agent" · feed/sitemap counts · phone 375px + desktop: status, one h1, no sideways scroll.
- In ESM tests, load the global Playwright with `createRequire(import.meta.url)("playwright")` (NODE_PATH does not work for `import`).

- 2026-11-20: the preview lives at a project page (we-international.github.io/weintervisa-site/), so root-relative links (/assets/site.css, /post/...) broke and the page showed unstyled. The Pages workflow now rebuilds with `SITE_BASE=/weintervisa-site` before upload (build.py `apply_base_path`, preview only). Tests still run on the plain build. Drop the step on the DNS day (custom domain serves from the root).

## Live Wix vs new site (learned 21 Nov 2026)
- Workflow **"Live Wix vs new site"** (`.github/workflows/live-vs-new.yml`, runs on PRs that touch it or its tools, and by hand once on main). The runner reads the live sitemap (`tools/live_urls.py`: sitemap index → pages / blog-posts / blog-categories) and pushes `tests/wix-live-urls.json` + side-by-side screenshots (`tools/compare_shots.mjs`, Wix left, new right, phone + desktop) to an **orphan** branch `review/compare-<run id>` (never merged). Fetch it with `git fetch origin review/compare-<id>` and `git --work-tree=<dir> checkout FETCH_HEAD -- review`.
- `tests/test_site.py` then fails if any live sitemap URL is not a page or redirect in the new build (owner-pending app pages listed in `tests/pending-pages.json`). Re-run the workflow before the DNS day: the blog keeps getting new posts on Wix.
- First run found: 1 new post published on Wix after the export, 3 blog category pages `/blog/categories/<slug>`, and Wix app pages `/members` and `/file-share` (not in the first inventory). Categories: Wix Blog `GET https://www.wixapis.com/blog/v3/categories` + `categoryIds` on posts → `content/blog-categories.json` → chips on /blog and one page per category.
- Wix answers fast repeat visits from a datacenter with a bot check ("Please wait while we verify your request", ~17 words). Only the first page came through. The script waits up to 30 s for it to clear, goes slowly (6 s between live pages) and marks rows "(Wix bot check)". Do not try to get round it; screenshots from a normal browser are the fallback.
- Word counts on the live Wix page are near 0 even when it renders (content sits in an embed), so compare by the screenshot, not by text metrics.
- The live Wix pages are custom embeds (iframes) and are newer and much fuller than the CMS drafts we first rebuilt from (21 Nov run: home 1,312 words live vs 424 new, homestay 1,157 vs 151, fast-track 1,003 vs 199). The compare run saves each live page's text (`review/compare/text/<page>.txt`) and the markup of its main frame (`<page>.html`, scripts removed) so pages can be rebuilt from what visitors see. Rebuild from those, not from the CMS drafts.

## Rebuilding a page from the live Wix page (learned 21 Nov 2026, home v2)
- Source = `review/compare-<run>/text/<page>.txt` (what visitors read) + `<page>.html` (links, image URLs + alt, hidden FAQ answers inside `<details>`; extract them with a small regex script, the .txt only has the questions).
- Put the page's words in `content/<page>.json`, the layout in Python. Keep owner rules over live wording (e.g. live "talk to us in your language" → "Mia chats in your language; our team replies in Thai or English"). Drop `utm_*` parameters (no analytics), the Wix translate widget (we have the EN/TH switch) and YouTube thumbnails from i.ytimg.com (link to the video instead of loading a Google image).
- Images: list them as `{"wix": <url without /v1/fill...>, "file": "<id>-mv2.<ext>", "alt": ...}`. `home_page.img()` renders an `<img>` only when `assets/img/<file>` exists, so the page never loads from Wix and works before the copy. `tools/fetch_images.py` (workflow "Copy Wix images into the repo") also downloads every `{"wix","file"}` in `content/*.json`; its "no Wix links left" check looks at `content/posts` only.
- Test the rebuild against the live page: body word count ≥ live (home: 1,457 vs 1,312), every path/CTA link resolves, no `utm_`, the AI-character disclaimer is kept.
