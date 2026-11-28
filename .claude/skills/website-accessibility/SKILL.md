---
name: website-accessibility
description: Use when building or changing any page of the new weintervisa.com site (or any static site the Web & CRM team owns), and before the DNS day. Runs axe-core (WCAG 2.1 A/AA + best practice) on every built page on phone and desktop, lists the mistakes we already made, and says how to fix them without changing the look.
---

# Website accessibility (axe) — Web & CRM team

Started 28 Nov 2026 (weintervisa-site PR "a11y axe"). First full scan: 99 pages × phone + desktop,
3 rule types failing on 150 page-views; all fixed in the same PR, now 0.

## The check
- `python3 build.py && node tests/a11y.mjs` — every page in `site/` (not `assets/`, not `/redesign/`
  mock-ups, not meta-refresh redirects), phone 375 px and desktop 1280 px, rules
  `wcag2a wcag2aa wcag21a wcag21aa best-practice`. Any violation = exit 1.
- CI: `.github/workflows/a11y.yml` on every PR and push to main (free, public repo).
  It installs `playwright@1.48.2 axe-core@4.10.2` with `--no-save` (the repo has no package.json).
- Cloud workspace: Playwright is global, axe-core is not. `npm i axe-core@4.10.2` in the scratchpad, then
  `NODE_PATH=$(npm root -g):<scratchpad>/node_modules node tests/a11y.mjs`.
- A page that only redirects destroys the page context while axe loads ("Execution context was destroyed"):
  skip files with `http-equiv="refresh"`.

## Mistakes we made (and the fix that keeps the look)
1. `<aside class="cta|tip">` inside `<main>` → `landmark-complementary-is-top-level` on almost every page.
   A call-to-action box or a tip is not a side column. Use `<div class="cta">` / `<div class="tip">`;
   the CSS targets the class, not the tag, so nothing moves. Do not add new `<aside>` inside `<main>`.
2. Card titles as `<h3>` straight after the page `<h1>` (home "four doors", /schools cards, EN + TH)
   → `heading-order`. Make the card title `<h2>` and give `.door h2` / `.agent h2` the old h3 size and
   weight in CSS. Check both language builders (EN in `group_pages.py`/`schools.py`, TH in `thai_more.py`).
3. Empty `<th>` over a link column (course compare tables) → `empty-table-header`. Put screen-reader text in
   it: `<th scope="col"><span class="vh">Details</span></th>` (`.vh` = visually hidden, in `site.css`).

## Already fine (keep it that way)
- Colour contrast passes on every page (axe checks the first paint only; check folded content by eye).
- One `<h1>` per page and no horizontal scroll are also checked in `tests/e2e.mjs`.
- Lead forms: every field has a label; errors are text, not colour only.

## When adding a page
Run the check before the PR. If a rule is truly wrong for a page, fix the markup anyway; do not add an
exclude list to the test.
