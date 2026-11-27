---
name: unslop-we
description: Use with the unslop skill (.claude/skills/unslop) on any weintervisa.com page or GetWec screen — how a scheduled run sets the direction without waiting for the owner, which of our rules beat unslop's, the icon set and the before/after for Nora. Roles: web design/UX, web dev, QA. Started 27 Nov 2026 (WEI-SKILL-UNSLOP-1126).
---

# unslop for We International (web + GetWec)

`unslop` (in `.claude/skills/unslop/`) is by Damir Sokolovsky (@heydamir), CC BY 4.0 — the folder is an unmodified copy (upstream commit in `UPSTREAM`, `LICENSE` + `CITATION.cff` kept). Never edit those files; put our changes here.

## What changes for us
1. **Direction without waiting.** Unslop step 4 says "set the direction and stop for the user". Scheduled runs do not wait for the owner: write the 5 lines (product, character, world, moments, signature) in the PR body and the AI Office log, then go on. The owner's own decisions are the brand and beat any direction:
   - weintervisa.com: home layout **A "four doors"** (owner 25 Nov 2026), teal `--brand #0f5c63`, warm paper `--bg`, EN + TH pairs, ≤ 450 words on home, one goal + one clear button per page (skill `website-readability`).
   - GetWec: HubSpot-like work pattern (left menu, search on top, tables, 3-column record) — pattern only, never HubSpot's look; Thai UI labels.
2. **Polish mode by default** on pages the owner already approved: fix only what the audit found; layout, sections and copy meaning stay; bigger ideas go into the report as suggestions.
3. **Our copy rules win:** no owner name or personal email; never visa advice ("Check your visa conditions on homeaffairs.gov.au or with a registered migration agent"); no promises of jobs, PR or income; prices only from the school files; no "ฟรี" inside Thai `<main>`; no fake urgency or invented discounts (policy-wei-enrolment-focus item 7).
4. **Images:** no paid generation. Use photos already in `assets/img/` or build the moment in code. Any credit-based image follows the studio budget rules and goes to the owner first.
5. **Icons:** `group_pages.icon(name)` — our own line icons (24 viewBox, 1.5 stroke, `currentColor`, muted). Add a new glyph to `_ICON_PATHS` instead of an emoji. GetWec: same rule, no emoji in labels or buttons.
6. **Credit:** "unslop by @heydamir" only in a story video or the skill files, never on a page.
7. **Story video:** optional; if made, render with `-preset veryfast` (the upstream script uses slow; pass a copy, do not edit the script) and keep it in the redesign Drive folder.

## Traps we found
- **Class-name collisions read as "grey, washed-out" slop.** Lead forms are `<form class="lead">` and the intro paragraph is `.lead` (muted, 19px), so every form on the site (16 pages) inherited muted text and 19px selects. Fix in CSS with a more specific rule (`form.lead { color: var(--ink); font-size: 17px; }`), not by renaming the class: `tests/e2e.mjs` clicks `form.lead button`. When text looks faded, check computed styles before touching colours.
- Back-to-back `<section class="wrap">` blocks stack 24 + 24 px padding plus the child's margin; use `.wrap.join` (padding-top 0) for a section that continues the one above (enrol form, "Another option").
- Prices in tables: `font-variant-numeric: tabular-nums` so A$ amounts line up.
- **A title rule that hits every `<strong>`.** `.tip strong { display: block }` was meant for the tip's title but also broke "**up to 4 months**" out of its sentence onto its own line (fast-track EN + TH). Scope title styles to `> strong:first-child`; check other tips still open with their title (`grep -rhoE 'class="tip[^"]*">.{0,25}' site`).
- **Emoji in JSON content.** Pages rebuilt from Wix keep the emoji as the first item of each row (`["🎓", "text"]`). Swap it for an icon name in the EN **and** `content/th/` JSON with a plain string replace (re-dumping the JSON rewrites the whole file and buries the diff), render with `icon(name)`, and drop "▶ " / trailing emoji from button and bubble text.
- Blank boxes in a full-page Playwright screenshot are usually `loading="lazy"` images that never scrolled into view, not missing files — check `assets/img/` before "fixing" them.

## Checks that must still pass
- weintervisa-site: `python3 tests/test_site.py` + `node tests/e2e.mjs` (phone + desktop). GetWec: `npm test`.
- Phone screenshot of every page touched (390 px) — icons next to wrapped text align to the top line.
- Before/after image (same crop, side by side) → Drive redesign folder https://drive.google.com/drive/folders/1t6F1xZYZaPn5vFQXfi8ANAiYoMnOCjKs, link in the AI Office log for Nora.

## Log
- 27 Nov 2026: home A EN + TH, polish mode (emoji → line icons, sentence-case kicker, heading weight 600, no headline period). Suggestions left for the owner: a headline only we could say, door links that name the page, one "Talk to us" per screen.
- 27 Nov 2026 (10:13 run): Working Holiday school pages (Charter, KCA, EN + TH), polish mode: form text muted→ink site-wide (class collision), section gaps, tabular prices; guard tests in `tests/test_site.py`. Suggestion left (done in PR #45): the 6-row fee list on phones repeats "English needed / Tuition / Materials" in every row — a per-field group (Aged care / Hospital / Childcare) with the two ways in side by side would read faster.
- 27 Nov 2026 (14:13 run): `/fast-track-courses` EN + TH (main Working Holiday page, owner's enrolment focus), polish mode: 12 emoji → line icons (new glyphs `cap`, `work`, `care`, `hospital`, `question`, `checklist`; health cover reuses `shield` like home), "▶" and 🎒 dropped from buttons/bubble, tip `<strong>` inline again; guard tests. Suggestions left: `/homestay` still has 9 emoji; the page has 4 "free course plan" buttons — one per screen is enough.
