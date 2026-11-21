---
name: website-thai-pages
description: Use when adding or changing a Thai page (/th/...) or the language switch on weintervisa.com — hreflang pairs, html lang, Thai forms, tests. Roles: web dev, SEO, web design/UX, QA.
---
# Thai pages on weintervisa.com

Owner rule (20 Nov 2026): every page in English + Thai, `/th/...` + hreflang, Thai written for people (no raw machine translation). Our team speaks Thai and English only; never promise other languages (Mia the AI may chat in any language).

## How it is built
- `thai_pages.py`: `TH_OF` (English path → Thai path) is the single list of pairs. `TH_PAGES` holds Thai bodies (`th/<page>` → title, description, body). The Thai home is `site/th/index.html` (URL `/th/`).
- `build.py` `page(..., lang="th")`: `<html lang="th">`, Thai nav (`NAV_TH`), Thai footer, skip link and menu label.
- `lang_links()`: pages in a pair get `hreflang` en / th / x-default (= English) both ways; header switch `.lang` goes to the other version. English pages without a Thai version link "ไทย" → `/th/`.
- Thai pages link to English pages where no Thai page exists yet; say "(ภาษาอังกฤษ)" next to such links where it matters (blog).
- Forms: `assets/forms.js` reads `document.documentElement.lang`; Thai pages get Thai messages and send `lang: "th"` (GetWec `preferred_lang`). Keep the word "Preview" in the preview messages (e2e looks for it).
- Option values in Thai forms are Thai (staff read Thai); keep `data-summary` labels in English so staff summaries look the same for both languages.

## Adding a Thai page
1. Write the Thai body in `thai_pages.py` (same facts as English, no new promises; keep the visa note: "ไม่ใช่ migration agent" + "registered migration agent").
2. Add `"/<en>": "/th/<en>"` to `TH_OF` and the body to `TH_PAGES`.
3. If it is in the Thai nav, point `NAV_TH` at the Thai path.
4. Add the URL to `tests/e2e.mjs` `urls`. `python3 tests/test_site.py` checks html lang, hreflang pair, switch, "body mainly Thai", visa note, no promises, sitemap count.

## Second set (21 Nov 2026)
- Content pages in Thai live in `thai_content.py` (`PAIRS` = English → Thai paths, `PAGES`, `JSONLD`); `thai_pages.py` merges them into `TH_OF` / `TH_PAGES`. (Courses, schools and blog index came in set 3, below.)
- Shared builders take a labels dict instead of copying code, e.g. `content_pages.partner_cards(partners, LABELS_TH)`.
- e2e checks every `/th` + content page automatically (`content` list filtered in `tests/e2e.mjs`).

## Third set (21 Nov 2026, 14:13 run)
- `thai_more.py`: `/th/courses` (45 study areas with Thai names in `AREA_TH`, keyed by CMS slug; build stops if a new CMS area has no Thai entry), `/th/blog` (built in `build.py` because it needs the posts), `/th/schools` + `/th/schools/<slug>`.
- Thai nav now points at `/th/courses` and `/th/blog`; Thai bodies no longer say "(ภาษาอังกฤษ)" next to course links.
- English proper names that must stay English (course titles in fee tables, blog post titles, campus names, school names) are wrapped in an element with `lang="en"`. Screen readers switch voice, and the "body mainly Thai" test strips `lang="en"` elements before counting English words. Don't use `lang="en"` to hide ordinary sentences that should be Thai.
- School pages keep the approval gate: Thai school pairs are added to `TH_OF` only for `schools.SCHOOLS` (empty in production until the owner approves), so production has no `/th/schools`. Every school needs Thai `SUMMARY_TH`, `INTAKES_TH`, `FEE_NOTE_TH` entries — the build stops otherwise, so adding a school to `content/schools.json` means adding its Thai lines too.
- Mobile fee table in Thai: `data-col="ระยะเวลา"`; campus columns keep the English campus name.
- `/th/privacy-policy` (21 Nov 2026, owner: "ทำได้เลย"): a sentence-by-sentence Thai copy of the owner-approved English notice in `thai_more.PRIVACY_TH`, with "ถ้าต่างกัน ให้ถือตามฉบับภาษาอังกฤษ". Change both together: the test checks the same number of sections, Sydney, OAIC, no cookies. Thai footer and the consent box on Thai forms link the Thai notice. Never add a promise to the Thai copy that the English one lacks.
- Still English only: blog post bodies.

## Traps
- "Body mainly Thai" test counts English words of 4+ letters: a page that repeats "registered migration agent" fails. Write the Thai term ("เอเจนต์ด้านวีซ่าที่ขึ้นทะเบียน") and give the English term once in brackets; the footer already carries the required phrase.
- The no-promise regex `รับประกัน(ผล|ที่เรียน|วีซ่า|งาน)(?!ได้)` also hits honest denials ("ไม่มีการรับประกันงาน"). Phrase as "ไม่มีใครรับประกัน…ได้" or "รับประกันว่า…".
- Never use "ฟรี" on Thai pages (blocked word); say "ไม่มีค่าใช้จ่าย" where the owner approved "free".
- Thai line breaks: Thai has no spaces between words; keep headings short and check the 375px screenshot (no overflow).
- `\b` does not work around Thai words in regexes (tests use plain substrings).
- After editing `assets/forms.js`, rebuild before running e2e (`build.py` copies assets into `site/`).
