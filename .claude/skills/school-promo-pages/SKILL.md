---
name: school-promo-pages
description: Use when adding or changing a school page on weintervisa.com (/schools, /schools/<slug>) from files a school sent to info@ — data file, owner-approval gate, fee tables on phones, Gmail attachment limits. Roles: web dev, web design/UX, CRM, QA.
---
# School promo pages (learned 21 Nov 2026, WEI-SCHOOL-BACKLOG-1120 step 4)

## Rules (owner, 20 Nov 2026)
- Only schools that **replied to us**, and only what they **sent us** (fee list, course list, marketing material, or an email that says it is for promotion). Never schools that have not replied, never "do-not-contact" schools, never a school that said it is not taking new agents.
- Do not wait for every school: ship one school, then add the next when its file arrives.
- No logos or photos unless the school gave them for promotion. No personal names. No "partner"/"official agent" claim unless the agreement is signed.
- Preview only until the owner approves: `"approved": false` in `content/schools.json`. The `--production` build drops unapproved schools; if none are approved, `/schools` is not built and `/courses` does not link it (test 12 checks both).

## Add a school
1. Find the reply in info@ (Gmail `from:<school domain> has:attachment`), read the files.
2. Save the files to Drive `07 Providers/<School>/` as `<school>_<type>_<year>.pdf`.
3. Add one object to `content/schools.json`: slug, name, summary, campuses, cricos, rto, https website, intakes, `fee_columns` (campus names), `fee_note` (what the total includes), `source` {file, received, year}, courses [{code, name, cricos, weeks, fees{campus: int}}]. No courses yet → leave `courses: []` and say "fees coming soon"; the card button then says "School details".
4. `python3 build.py && python3 tests/test_site.py && node tests/e2e.mjs` (e2e reads the slugs from the JSON).
5. Owner approves → set `"approved": true` in the same file (that is the only switch).

## Tricks / mistakes to avoid
- Gmail attachment download refuses files over 12 MB (e.g. a 15.6 MB marketing PDF). Do not retry or route it through Make; ask a person to use "Save to Drive" in Gmail, then read it from Drive.
- `get_thread` on threads with signature images is huge: it saves to a file; use `jq` to list `.messages[].attachments[].filename` and the first part of each body.
- Fee tables on phones: turn rows into blocks under 480px and label cells with `data-col` + `::before`. Make the `<caption>` `display:block` too, or it shrinks to one word per line.
- Always add the caveat: fees and dates can change; the school confirms them in the offer letter; visa questions go to a registered migration agent.
- Owner approved Alana Kaye College and Frontier Education on 22 Nov 2026 (both `approved: true`). A school added later starts at `false` again and needs its own approval; a test checks the approved names.
