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

## Lesson 25 Nov 2026: the owner picked home A — turning a mockup into the real site
- Real pages live in `group_pages.py` (home doors EN+TH, 6-item menu, footer links, /families, /take-a-break); CSS goes into `assets/site.css` (port only the classes you use, scoped: `.door .door-ico` — a generic `.door span` rule beat a bare `.door-ico` and shrank the icon to text size; check a phone screenshot every time).
- Keep the old long home code (`home_page.render`, `content/home.json`) — the rule is "don't delete"; its sections already live on the door pages. Keep `/redesign/` until every page in it is decided (Working Holiday A/B was still open).
- Menu highlight: pick the **longest** menu path the page sits under (`nav_current`), else `/courses` and `/courses/nursing-…` both light up.
- Replace the old "as full as Wix" tests with: ≤ 450 words on home, 4 doors that resolve, every help link resolves, menu order, footer links, Thai home = same sections/doors with Thai links only.
- Thai copy: the tests ban the word "ฟรี" inside `<main>` (promise rule) — write "ไม่มีค่าใช้จ่าย" or drop it; English "free games" is fine.
- Link out only to URLs already confirmed in the repo or AI Office. No guessed YouTube/TPT links: leave the card out and ask in the report (Kindoza Kids videos, Solune walk clips).
- One-way group rule: the visa site may link to the game studio and the kids' shop; those pages send nothing to GetWec and carry no student data (tested).

## Lesson 27 Nov 2026: first unslop pass on home A (skill `unslop` + `unslop-we`)
- Audit = light slop (polish mode, the owner's layout kept): emoji used as icons (trust line, "Already here" picks, the partner door), an UPPERCASE tracked kicker, 700-weight headings, a period at the end of the headline.
- Fixed: one set of line icons drawn in `group_pages.py` (`icon(name)`, 24 viewBox, 1.5 stroke, colour = muted text role, `aria-hidden`), leading emoji stripped from `content/*/home.json` trust lines at render time (the JSON keeps its text), `.kicker` sentence case with no tracking, h1/h2 weight 600, no trailing period on the EN headline. Thai: no letter spacing anywhere (it splits vowel and tone marks).
- Not changed (suggestions for the report, owner decides): the headline "Study in Australia, your way" passes the template check badly — it could sit on any agency's site; "See more →" ×4 could name the page; two "Talk to us" buttons on one screen.
- Before/after image goes to the redesign Drive folder for Nora; never put the unslop credit on the page.

- 27 Nov 2026 (16:13 run): one **solid** button per screen. On `/fast-track-courses` the three course cards each had a solid "Get a course plan" — on a phone two sit on one screen next to the section CTA. Cards now use `btn ghost` (same link, quieter); the solid button stays on the hero, "how it works" and the closing CTA. Test in `tests/test_site.py` (course cards: 3 × ghost, 0 × solid).

## Lesson 27 Nov 2026 (18:13 run): nursing page 9.6 → 7.9 phone screens without deleting a word
- Measure per section first (`main > section` heights ÷ 844) — it shows where the screens go (here: 4 course cards 1.7, map 1.6).
- Course cards whose only action is "email us" → one `<details class="faq course-fold">` per course (name + type in the summary, ≥44 px tap row). A link on every card that repeats the email list further down is noise: one "pick your course in the email list below ↓" link instead.
- A second illustration that adds nothing on a phone: `class="… wide-only"` (hidden < 760 px), the desktop keeps it.
- Checklists and "sources / reviewed / disclaimer" small print fold into `<details>`; the visa referral box stays visible (rule), and the HTML still holds every official link (tests count them in the HTML, not visible text).
- Words stay in the HTML, so the old "as full as Wix" word test still passes; Playwright `innerText` drops closed folds, so a visible-word count falls (817 → 742) — say which count you report.
- Kept visible on purpose: the 4-step registration map + "Good to know" box (it stops people booking the wrong course). Next candidate if the owner wants ≤ 6: fold each map step's detail.
- Thai copy: new UI keys go in `content/th/nursing.json` "ui" (one-line JSON style — don't re-dump the whole file, it rewrites 249 lines).

## Lesson 27 Nov 2026 (20:13 run): /courses 49.4 → 6.6 phone screens (TH 46.2 → 6.7), no words deleted
- Measure every page first (58 non-redirect pages, phone 390×844): /courses was the outlier at 49 screens; next are /blog 20, /fast-track-courses 12, /english-practice 10, /homestay 9.8.
- A long catalogue = fold by group: `<details class="group-fold"><summary><h2 id="…">Group (n courses)</h2></summary>…</details>`. A heading inside `<summary>` is valid HTML, keeps the h2 outline for SEO and keeps the old anchor id, so home-page and in-page links still land.
- Topic pictures in a list → `.wide-only` (hidden < 760 px; lazy images that are `display:none` are not downloaded on phones).
- Links into closed folds: Chrome opens the folds round a #target by itself; older Safari/Firefox do not → `assets/reveal.js` (15 lines: on click of a `#` link, on `hashchange` and on load, open every ancestor `<details>` of the target). Page still works without it. Give targets `scroll-margin-top: 72px` or they hide under the sticky header (course rows landed at top 0 before).
- Check in a real browser after the change: tap an interest chip, a city → course link, and deep links `/courses#<group>` / `#<study-area>`: fold open + target top = 72 px.
- Playwright WebKit is not installed in the cloud box (only Chromium) — don't install it; test the fallback logic by reading it, Chromium for the rest.

## Lesson 27 Nov 2026 (22:13 run): /blog 20.1 → 4.3 phone screens (TH 15.4 → 3.7), no post unlinked
- A blog index of 39 picture cards = 20 phone screens. Now: the 6 newest as picture cards ("Latest posts"), then "All N posts by topic" = one `<details class="group-fold">` per blog category with short **title + date rows** (`.post-rows`, ≥44 px tap row, no image, no excerpt).
- Every post stays linked from `/blog`, `/th/blog` and its topic page (crawl + old Wix links); the RSS feed and `/post/<slug>` URLs are untouched. Topic pages (`/blog/categories/<slug>`): 6 cards + "More … posts" rows (9.2 → 5.3 screens).
- Topic folds carry `id="<category slug>"` + `assets/reveal.js`, so `/blog#life-in-australia` opens the fold.
- Test the set of linked slugs (`re.findall(r'href="/post/([^"]+)"')`), not the number of cards — the old Thai test counted `<li class="card">` and broke when rows replaced cards.
- Measuring with a tiny static server: `/blog` is also a folder (`blog/categories/`), so ask for `/blog.html` or the server serves a 404 and the page measures as 1.0 screen.

## Lesson 28 Nov 2026 (08:13 run): /fast-track-courses 12.1 → 9.0 phone screens (TH 12.2 → 8.8), no words deleted
- Picture cards that are also jump targets (finder `#chc33021`): keep the card, put the photo **outside** the fold with `wide-only`, and put the **id on the `<details>`** (`reveal.js` starts at the target itself, so a details target opens; an id on the parent `<li>` would not). Keep the outline with `.course:has(.ft-fold:target)`. Check in Chromium: every finder tap → fold open, top = 72 px; deep link `#hlt33115` the same.
- Desktop keeps the 3-card grid with photos (folded body under each); phones get compact rows. One CSS class (`.ft-fold`, built on `.group-fold`) serves course cards and the settle-in cards.
- Small wins add up: Maya/Kenji bubbles `wide-only` (the picture stays), hero points without boxes on phones, the 3 "compare" links in one fold, "why in demand" sources and a dated news aside folded (summary names it: "Maya says: care worker visa news", not a repeat of the first words).
- Kept visible on purpose: the 3 steps + Kenji's 4-month (condition 8548) tip and the mid-page plan box with "don't send passport numbers" — they stop wrong bookings and unsafe emails. Getting to ≤ 6 would mean folding those; ask the owner first.
- Tests: fold ids = finder ids, photos `wide-only`, every settle/compare/source link still in the HTML, Thai page checked against `content/th/fast-track.json` (its links differ: `/th/...`).

## Lesson 28 Nov 2026 (08:13 run, 2nd page): /homestay 9.8 → 8.5 phone screens (TH 8.2)
- Money stays visible: the AHN price table, both years, the matching fee, the "prices can change" note and the source are never folded (tested: no `<details>` inside the table). Instead `.fees.compact`: on phones each row is the package line + one line with both years (`td { display: inline-block }`).
- Folded: the 3 "good to know" cards (same `.ft-fold` card fold as /fast-track-courses) and the 3 "why apply through us" bullets in the apply box (the button and the "Education Provider" tip stay visible).
- Kept visible: the scam warning + Kenji's tip (safety), the 6 steps.
- Thai `ui` in `content/th/homestay.json` is one long line: add a key by string-replacing after `"contact": "/th/contact-us"`, never a regex that expects one key per line.

## Lesson 28 Nov 2026 (10:13 run): /english-practice 10.2 → 6.5 phone screens (TH 10.1 → 6.4), no words deleted
- A quiz of 8 cards (3.4 screens) = a taste + a fold: the first 3 questions open, the other 5 in one `<details class="group-fold quiz-more" id="more-questions">` titled "5 more questions" (count from the data, Thai key `moreQ`). The quiz's own answer `<details>` stay plain, so the "8 answers in `<details>`" test still counts them.
- Three open cards in a 2-column grid leave a hole on desktop: give the open list 3 columns ≥ 1000 px (`#quiz > .quizzes`), the folded list keeps the old grid.
- A shop block (6 product cards, 2.3 screens) folds behind "See the 6 printables"; the shop link, "opens Etsy" note and the fictional-characters line stay visible.
- Every page that gets a fold with an id loads `/assets/reveal.js` and the fold gets `scroll-margin-top: 72px` — without it a deep link landed at top 0 under the sticky header (checked in Chromium: `#more-questions` open, top = 72 px).
- Thai `ui` keys added in place with one string replace (the file is one-line JSON per key; never re-dump it).

## Lesson 28 Nov 2026 (12:13 run): the 3 course-compare pages under 6 phone screens (aged care 6.2 → 5.9, TH 6.1 → 5.8; childcare 5.4, hospital 5.6)
- One template (`compare_page.py`) serves all three, so one fold fixes all: "What the course is" (3 bullets) → `<details class="group-fold" id="about-course"><summary><h2>…</h2></summary>`.
- Stay visible on purpose: the fee table, "Which one fits your visa?" + 8548, the visa-check and not-a-migration-agent boxes, and the childcare Diploma line (it carries a fee: money is never folded). Test checks the fold holds no table and no A$.
- A quick measure script without the repo tool: static server + Playwright, `main > section` heights ÷ 844 per section; the form is 2.3 of the 6 screens and is not folded (it is the page's job).
