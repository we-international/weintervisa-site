---
name: website-readability
description: Use when a weintervisa.com page (or any company site page) feels long, dense or "like a report", when planning a new page layout, or when showing the owner design options. Readability rules, how to measure a page, the mockup-for-owner workflow (/redesign/ on preview only) and the tests. Roles: web design/UX, web dev, SEO, QA.
---
# Website readability (learned 24 Nov 2026, WEI-WEB-REDESIGN-1123)

## Why this skill exists
The owner (23 Nov 2026) said the new site "reads like a report page, too much pushed in, hard to read; maybe split the pages differently".
Cause: the old rule "as many words as the Wix page or more" made every page a wall (home 16.8 phone screens, ~1,370 words; Working Holiday 10.8 screens).
That word-count rule is cancelled. The new rule is **easy to read + people find what they need fast**. SEO is kept by moving long text to its own page or folding it, never deleting it, and keeping every old Wix URL.

## Rules for every page
- One page answers one question. The top says it in one sentence (h1 + one short lead line).
- Phone first: home ≤ ~5 phone screens (390 × 844), other pages ≤ ~6. Paragraphs ≤ 3 lines on a phone (about ≤ 320 characters of text).
- One main button per screen. One "Talk to us" in the header. No row of 3 buttons.
- Long detail (fees, FAQ, steps, rules) → its own page, a `<details>` fold, or CSS tabs. Nothing important is lost: link to it.
- Doors, not lists: the home page shows 3–4 doors by who the visitor is (Working Holiday · Study · Nursing · Partners) with a real photo each.
- Proof is short and true: QEAC number, "course advice is free", office in Sydney, languages. Never invented reviews or testimonials.
- Plain, friendly English; headings say the benefit. No reply-time promises, no "guarantee", no visa advice (refer to a registered migration agent).
- No script needed: answer-pickers and tabs use radio inputs + CSS (`#q1:checked ~ #a1 {display:block}`), so pages stay fast and work without JS.
- Sticky bottom button on phones only (`position: sticky; bottom: 0`, hidden ≥ 760 px). Note: Playwright full-page screenshots show it in the middle of the page; that is a screenshot artefact, not a bug.

## Measure before and after
`node measure.mjs site / /fast-track-courses` (Playwright: scrollHeight ÷ viewport height = screens, plus word count, phone 390×844 and desktop 1366×900). Put the before/after table in the owner review.
Playwright from a script outside the repo: `createRequire('/opt/npm-tools/node_modules/')('playwright')` (plain `import 'playwright'` fails from the scratchpad).

## Showing the owner options (mockups)
- `redesign_mockups.py` builds `/redesign/` (index with a Now-vs-A-vs-B table + new sitemap, then each option) — **preview build only** (`if PREVIEW:` in build.py), noindex, not in sitemap.xml, a dark "Design mockup · for review only" bar on top.
- Use real text from `content/*.json`, shortened. Same footer (company, QEAC number, not-a-migration-agent line). Maya and Kenji images carry "fictional, AI-generated characters".
- Two clearly different directions (A calm/simple, B friendlier/interactive) for the home page and one key inner page, phone + desktop screenshots in Drive. Owner may mix ("home A + Working Holiday B").
- After the owner picks: rebuild the real pages, delete `redesign_mockups.py` and its tests in the same PR, swap the word-count tests for readability tests (screens, paragraph length, one h1, content still findable).

## Tests (tests/test_site.py, test_production.py)
- mockups noindex + not in sitemap; "for review only" + migration-agent line + QEAC; no unapproved promises; ≤ 400 words in the body; no paragraph over 320 characters; Maya/Kenji pages say they are fictional.
- production build has no `/redesign/`.
