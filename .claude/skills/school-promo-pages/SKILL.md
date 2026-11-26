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
- Frontier (22 Nov 2026): the 15.6 MB marketing PDF became readable once a person saved it to Drive; `read_file_content` on the Drive file returns the text (price list + course sheets) — no download needed. Fee columns can be by student situation ("Already in Australia" / "Applying from overseas") instead of campus; a missing fee shows "Ask us" / "ถามเรา"; `cricos` per course is optional (an 11xxxNAT course may have none). Show the total (tuition + material + application) and say so in `fee_note`.

## Working Holiday school pages (25 Nov 2026, WEI-WHV-CHARTER-1125)
- Owner-directed pages (Charter Australia first, KCA second) live in `content/working-holiday.json` + `whv_page.py`, not in `schools.json`: they sell one route (enrol with us → we send the application) instead of a fee catalogue. Add a school = add one object with `options` (form course choices).
- Use the school's agent fee table for the visa type (Charter: the "Study and Work Program" 2027 table, published 24 Jul 2026, attached to Charter's 10 Sep 2026 email; KCA: the 30 Sep 2026 reply in thread "KCA 2027 Pricing Schedule"). Gmail threads with long HTML exceed the tool limit: read the saved JSON with `jq '.messages[].plaintextBody'`, and `pdftotext -layout` the fee PDF.
- Never copy commission lines (KCA's email states one) — test greps `commission|25%`.
- A program the school lists as "up to 12 months" on a WHV page: show it as the school's wording, add the Home Affairs 4-month rule (condition 8548) + VEVO link, and warn when the course is close to the limit (KCA 16 weeks). No visa advice: registered migration agent.
- Expired intake dates (KCA's 2026 dates ended 18 Nov) are not shown; say "ask us for the next start date".

## One course, many schools: comparison pages (26 Nov 2026, policy-wei-enrolment-focus item 2)
- When several schools sent fees for the same course code (CHC33021 at Charter, KCA, Alana Kaye, Frontier), build one comparison page (`compare_page.py`, `/courses/aged-care-certificate-iii` + `/th/...`) instead of a new data file: read every number from `working-holiday.json` and `schools.json`, so it can never disagree with the school pages. A test re-reads the JSON and checks every A$ amount is on the EN and TH page.
- Use `schools.SCHOOLS` (owner-approved only in `--production`); WHV schools come from `working-holiday.json`. Order shortest first, then lowest fee; each row links the school page (Thai links Thai).
- "Who it is for" is a fact, not visa advice: "Working Holiday 417/462 (Study and Work Program)" vs "International students (CRICOS course <code>)" + the 8548 4-month line + "Check your visa conditions on homeaffairs.gov.au or with a registered migration agent".
- Form: reuse `pages.apply_form` / Thai `apply_form` (passed in, never imported from `thai_pages` → circular import), preset Course area + Certificate III, and add a "School you like" select (`data-summary="School"`, English values, "Not sure yet" selected) so staff see the school in the GetWec subject. e2e checks the summary.
- Long text in a `.fees` table: add class `cmp` (`white-space: normal`); a link cell with no `data-col` must not show the phone `": "` label (`.fees td:not([data-col])::before { content: none }`).
- Thai "mainly Thai" test: mark English proper names (school names, campuses, `<option>` school names) `lang="en"`; translate column labels like "Already in Australia" on the Thai page. Titles must be 15–60 characters.
- Add a course = add a spec to `compare_page.SPECS` (slug, codes, WHV schools, caption, EN + TH text); pages, Thai pairs and the "other comparison" link are built from the list. Childcare (`/courses/childcare-certificate-iii`, 26 Nov 2026) is the second spec.
- Same qualification, different codes (Charter CHC30125, Alana Kaye CHC30121): show each school's own code and say "not the same at both schools; your offer letter shows the code". Never call them the same course or say one is "newer" unless an official source says so in the file.
- A school special price (`"A$7,700 (special, was A$12,650)"`) is shown only with its end date from the school's own fee notes (`special prices run until 30 June 2027` → TH `30 มิ.ย. 2027`); no end date in the file = show the plain price. Policy item 7: the first time a discount goes onto the live site, Nora shows Ben once (preview is fine).
- A comparison page with only 2 schools is still worth it (policy item 2): shortest/WHV first, then the CRICOS course, plus one fact line about the next level (Diploma) at an approved school.
- e2e summary order is `School · Course area · Level`: check it with lookaheads (`/^(?=.*School: …)(?=.*Course area: …)/`), not one ordered regex.
