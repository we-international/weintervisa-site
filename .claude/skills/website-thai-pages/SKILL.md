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

## Traps
- Thai line breaks: Thai has no spaces between words; keep headings short and check the 375px screenshot (no overflow).
- `\b` does not work around Thai words in regexes (tests use plain substrings).
- After editing `assets/forms.js`, rebuild before running e2e (`build.py` copies assets into `site/`).
