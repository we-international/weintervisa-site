#!/usr/bin/env python3
"""Site checks — run: python3 tests/test_site.py  (exit 1 on any failure)."""
import json, re, subprocess, sys
from html import unescape as html_unescape
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
fails, notes = [], []

def check(ok, msg):
    (notes if ok else fails).append(("✓ " if ok else "✗ ") + msg)

subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)
pages = {p: p.read_text() for p in SITE.rglob("*.html")}

# 1. Every live Wix post (export list) is at the same URL /post/<slug>
slugs = json.loads((ROOT / "tests/wix-post-slugs.json").read_text())
missing = [s for s in slugs if not (SITE / "post" / f"{s}.html").exists()]
check(not missing, f"all {len(slugs)} Wix post URLs exist" + (f" — missing {missing}" if missing else ""))

# 1b. Every URL in the live Wix sitemap (CI snapshot: tools/live_urls.py) is a page or redirect here,
#     except the Wix app pages still waiting for an owner decision (tests/pending-pages.json).
live = [x["path"] for x in json.loads((ROOT / "tests/wix-live-urls.json").read_text())["paths"]]
_pending = set(json.loads((ROOT / "tests/pending-pages.json").read_text()))
def _served(p):
    rel = p.lstrip("/")
    return p == "/" or (SITE / f"{rel}.html").exists() or (SITE / rel / "index.html").exists()
gap = [p for p in live if not _served(p) and p not in _pending]
check(not gap, f"all {len(live)} live Wix sitemap URLs are served ({len([p for p in live if p in _pending])} waiting for owner)" + (f" — missing {gap}" if gap else ""))

# 2. Internal links resolve (pages still to build are listed in tests/pending-pages.json)
pending = set(json.loads((ROOT / "tests/pending-pages.json").read_text()))
def resolves(path):
    path = path.split("#")[0].split("?")[0].rstrip("/") or "/"
    if path == "/":
        return (SITE / "index.html").exists()
    rel = path.lstrip("/")
    return (SITE / rel).exists() or (SITE / f"{rel}.html").exists() or (SITE / rel / "index.html").exists()
broken, waiting = set(), set()
for p, s in pages.items():
    for href in re.findall(r'href="(/[^"]*)"', s):
        if resolves(href):
            continue
        clean = href.split("#")[0].split("?")[0].rstrip("/")
        (waiting if clean in pending else broken).add(clean)
check(not broken, "no broken internal links" + (f" — broken: {sorted(broken)}" if broken else ""))
notes.append(f"• links to pages not built yet (from migration map): {len(waiting)} — {sorted(waiting)}")

# 3. No personal names / emails; only the company inbox
bad_words = re.compile(r"jarinrit|gmail\.com|\bBen\b", re.I)
hits = [str(p.relative_to(SITE)) for p, s in pages.items() if bad_words.search(s)]
check(not hits, "no personal name/email in pages" + (f" — {hits}" if hits else ""))
emails = set(e for s in pages.values() for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", s))
partner_emails = {p.get("email") for p in json.loads((ROOT / "content/migration-partners.json").read_text()).get("partners", [])}
check(emails <= {"info@weintervisa.com"} | partner_emails, f"only info@weintervisa.com (and listed agents' own contact emails) appear (found {sorted(emails)})")

# 4. No trackers / cookies
trackers = re.compile(r"googletagmanager|google-analytics|gtag\(|fbq\(|connect\.facebook|hotjar|document\.cookie", re.I)
check(not any(trackers.search(s) for s in pages.values()), "no analytics/trackers/cookies")

# 5. Preview is not indexable; redirects; menu
check(all('name="robots" content="noindex' in s for s in pages.values()), "every page is noindex (preview)")
check("Disallow: /" in (SITE / "robots.txt").read_text(), "robots.txt blocks crawlers (preview)")
check("url=https://weintergames.com/" in (SITE / "games.html").read_text(), "/games → weintergames.com")
check("url=https://getwec.pages.dev/book/" in (SITE / "schedule.html").read_text(), "/schedule → GetWec Book a free consultation (Wix Bookings rebuilt)")
check("url=https://getwec.pages.dev/" in (SITE / "partner-portal.html").read_text(), "/partner-portal → GetWec partner sign-in (Wix portal rebuilt)")
check('url=/"' in (SITE / "welcome.html").read_text(), "/welcome → /")
check(not re.search(r">Games<", (SITE / "index.html").read_text()), "no Games item in the menu")

# 6. Legal footer: not a migration agent; QEAC number only
home = (SITE / "index.html").read_text()
check("not a migration agent" in home and "registered migration agent" in home, "footer says we are not a migration agent")
check(re.search(r"QEAC \d+</p>", home) is not None, "QEAC shows the number only")

# 7. Feed + sitemap
feed = (SITE / "blog-feed.xml").read_text()
check(feed.count("<item>") == len(slugs), f"blog-feed.xml has {len(slugs)} items (same path as Wix)")
import pages as _p, content_pages as _cp
import thai_pages as _tp
import group_pages as _gp0
import whv_page as _wv0
import already_page as _ap0
import compare_page as _cmp0
n_static = len(_p.PAGES) + len(_cp.CONTENT_PAGES) + len(_gp0.PAGES) + len(_wv0.PAGES) + len(_ap0.PAGES) + len(_cmp0.PAGES_EN) + 2 + len(_tp.TH_PAGES)  # + Thai home, Thai blog and Thai pages
n_static += len(json.loads((ROOT / "content/blog-categories.json").read_text())["categories"])  # /blog/categories/<slug>
check((SITE / "sitemap.xml").read_text().count("<loc>") == len(slugs) + 2 + n_static, f"sitemap lists home, blog, {n_static} static pages (EN + TH) and every post")

# 8. Lead forms (→ GetWec "lead" contract) — never connected in a preview build
for rel in ("contact-us", "charter-application"):
    s = (SITE / f"{rel}.html").read_text()
    check('data-lead-form=' in s and '/assets/forms.js' in s, f"/{rel} has a lead form")
    check('name="consent" required' in s and 'href="/privacy-policy"' in s, f"/{rel} asks consent + links privacy")
    check('name="website"' in s, f"/{rel} has the honeypot field")
    check('registered migration agent' in s, f"/{rel} says visa questions go to a registered migration agent")
    check('getwec-key' not in s, f"/{rel} is not connected in preview")
    check(not re.search(r"passport (no|number)\b[^.]*<input|type=\"file\"", s, re.I), f"/{rel} asks for no passport number or uploads")
    check(not re.search(r"\bfree consultation|within (24 hours|one business day)|guarantee", s, re.I), f"/{rel} makes no unapproved promises")
# 9. Content pages (same Wix paths) — honest, no unapproved promises, visa → registered migration agent
for rel in _cp.CONTENT_PAGES:
    f = SITE / f"{rel}.html"
    check(f.exists(), f"/{rel} exists")
    s = f.read_text()
    check(not re.search(r"\bfree consultation|within (24 hours|one business day)|guaranteed (place|visa|job)|100% |best price", s, re.I), f"/{rel} makes no unapproved promises")
    check('<meta name="description" content="' in s and '<meta name="description" content="">' not in s, f"/{rel} has an SEO description")
    check(s.count("<h1>") == 1, f"/{rel} has one h1")
for rel in ("migration-support", "fast-track-courses", "courses/nursing-pathways-australia", "english-practice"):
    check("registered migration agent" in (SITE / f"{rel}.html").read_text(), f"/{rel} refers visa questions to a registered migration agent")
c = (SITE / "courses.html").read_text()
check(c.count("<li><strong>") >= 45, "/courses lists every study area from the CMS export")
check("CRICOS" in c and "not a promise" in c, "/courses explains the list is not a promise")
check('"FAQPage"' in (SITE / "frequently-asked-questions.html").read_text(), "FAQ page has FAQPage structured data")
pv = (SITE / "privacy-policy.html").read_text()
check("Sydney" in pv and "cookies" in pv and "AI" in pv, "privacy notice covers GetWec in Sydney, no cookies, the AI assistant")
check("Draft for owner review" not in pv and "Last updated:" in pv, "privacy notice is the approved version (no draft label, has a date)")
# 10. Home page — content/home.json (live Wix home, 21 Nov 2026); every study-area group links to its section on /courses
hd = json.loads((ROOT / "content/home.json").read_text())
check(hd["heading"] in html_unescape(home) and home.count("<h1>") == 1, "home uses its heading as the one h1")
check(f'<title>{hd["seoTitle"]}</title>' in html_unescape(home) and hd["seoDescription"] in html_unescape(home), "home has its SEO title + description")
check("registered migration agent" in home.split("<footer")[0], "home body refers visa questions to a registered migration agent")
check(not re.search(r"\bfree consultation|within (24 hours|one business day)|guarantee(d)? (place|visa|job)|100% |best price", home, re.I), "home makes no unapproved promises")
check('"WebSite"' in home and '"Organization"' in home, "home has Organization + WebSite structured data")
# 10b. Home style A "four doors" (owner 25 Nov 2026; replaces the long v2 home and its word-count bar, cancelled 23 Nov)
import group_pages as _gp
body_home = home.split("<main")[1].split("</main>")[0]
words_home = len(re.sub(r"<[^>]+>", " ", body_home).split())
check(words_home <= 450, f"home body is short: one sentence, four doors, three steps, one button ({words_home} words ≤ 450)")
check(body_home.count('<li class="door">') == 4 and all(f'href="{d[0]}"' in body_home and resolves(d[0]) for d in _gp.DOORS["en"]),
      "home: four doors, each links a built page")
check(all(f'href="{x[2]}"' in body_home and resolves(x[2]) for x in _gp.HOME_UI["en"]["pick"]), "home: help links (OSHC, homestay, families, take a break, English, blog) go to built pages")
check("utm_" not in home, "home: no tracking parameters")
check("Our team replies in Thai or English" in html_unescape(home), "home: our team replies in Thai or English (owner rule)")
check("Maya" not in body_home or "fictional, AI-generated characters" in home, "home: Maya and Kenji, if shown, are labelled fictional AI characters")
# 10b2. Menu of 6 and footer (owner 25 Nov 2026)
_nav = home.split('<nav class="wide">')[1].split("</nav>")[0]
check(re.findall(r'href="([^"]+)"', _nav) == [p_ for _, p_ in _gp.NAV["en"]], "menu: Study, Working Holiday, Nursing and care, Student help, Learn English, Contact us")
_ft = home.split('<footer')[1]
check('href="https://weintergames.com/"' in _ft and 'rel="noopener"' in _ft and all(f'href="{h}"' in _ft for h in ("/take-a-break", "/families", "/english-practice", "/blog")),
      "footer: game studio line + Learn English, Take a break, Families, Blog")
check((SITE / "courses/nursing-pathways-australia.html").read_text().split('<nav class="wide">')[1].split("</nav>")[0].count("aria-current") == 1,
      "menu marks one item on a sub-page (Nursing, not Study)")
for rel in ("take-a-break", "families", "th/take-a-break", "th/families"):
    s_ = (SITE / f"{rel}.html").read_text()
    check(s_.count("<h1>") == 1 and "weintergames.com" in s_ and "getwec" not in s_.lower().split("<footer")[0], f"/{rel}: one h1, links the game studio, sends nothing to GetWec")
_fam = (SITE / "families.html").read_text()
check(all(i[3] in _fam for i in _gp.KIDS["items"]) and "registered migration agent" in _fam, "/families: every kids' activity links its listing; family visa questions → registered migration agent")
check(all(f"weintergames.com/#{g[0]}" in (SITE / "take-a-break.html").read_text() for g in _gp.GAMES), "/take-a-break: each game links its section on weintergames.com")
check(all(f'id="{g[0]}"' in (ROOT.parent / "weintergames-site/index.html").read_text() for g in _gp.GAMES) if (ROOT.parent / "weintergames-site/index.html").exists() else True,
      "/take-a-break game anchors exist on weintergames.com (when the site repo is next to this one)")
for f_ in re.findall(r'src="/assets/img/([^"]+)"', home):
    check((ROOT / "assets/img" / f_).exists(), f"home image {f_} is in the repo")
# 10c. /fast-track-courses — rebuilt from the live Wix page (21 Nov 2026)
ft = (SITE / "fast-track-courses.html").read_text()
ftd = json.loads((ROOT / "content/fast-track.json").read_text())
words_ft = len(re.sub(r"<[^>]+>", " ", ft.split("<main")[1].split("</main>")[0]).split())
check(words_ft >= 1000, f"/fast-track-courses is as full as the live Wix page ({words_ft} words, live ≈ 1,003)")
check(all(f'id="{c["id"]}"' in ft for c in ftd["courses"]) and all(f'href="{h}"' in ft for _, _, h in ftd["finder"]), "/fast-track-courses: every finder answer jumps to its course (or contact)")
check("condition 8548" in ft and "registered migration agent" in ft and "utm_" not in ft, "/fast-track-courses: 4-month study rule, visa → registered migration agent, no tracking")
for f_ in re.findall(r'src="/assets/img/([^"]+)"', ft):
    check((ROOT / "assets/img" / f_).exists(), f"/fast-track-courses image {f_} is in the repo")
# 10d. /english-practice — rebuilt from the live Wix page (21 Nov 2026)
ep = (SITE / "english-practice.html").read_text()
words_ep = len(re.sub(r"<[^>]+>", " ", ep.split("<main")[1].split("</main>")[0]).split())
check(words_ep >= 746, f"/english-practice is as full as the live Wix page ({words_ep} words, live ≈ 746)")
check(ep.count("Question ") >= 8 and ep.count("<details>") >= 8, "/english-practice: 8 quiz questions, answers in <details> (no script)")
check("Puzora" not in ep and "https://weintergames.com/" in ep, "/english-practice: game studio under its current name (WE International Game Studio), no old name")
check(not re.search(r'<(img|iframe)[^>]+src="https?://', ep), "/english-practice loads no third-party images or embeds")
# 10e. /homestay — rebuilt from the live Wix page (21 Nov 2026)
hs = (SITE / "homestay.html").read_text()
words_hs = len(re.sub(r"<[^>]+>", " ", hs.split("<main")[1].split("</main>")[0]).split())
check(words_hs >= 1157, f"/homestay is as full as the live Wix page ({words_hs} words, live ≈ 1,157)")
check("checked 26 October 2026" in hs and "can change" in hs, "/homestay: AHN prices are dated, sourced and say they can change")
check(hs.count('href="https://au.homestaynetwork.org/guests/signup?affiliate=WeInternationalEducationAndVisa"') >= 3 and 'rel="noopener"' in hs, "/homestay: apply buttons use our AHN partner link, new tab")
check("Don&#x27;t pay a stranger" in hs or "Don't pay a stranger" in hs, "/homestay warns about accommodation scams")
# 10f. Pages rebuilt from the live Wix pages on 22 Nov 2026: main text at least as full as live, links kept
def _main_words(rel):
    s_ = (SITE / f"{rel}.html").read_text()
    return s_, len(re.sub(r"<[^>]+>", " ", s_.split("<main")[1].split("</main>")[0]).split())
for rel, live in (("courses/nursing-pathways-australia", 740), ("oshc", 180), ("about-we-international", 260),
                  ("referral-partners", 390), ("student-services", 120), ("contact-us", 370)):
    s_, n_ = _main_words(rel)
    check(n_ >= live, f"/{rel} is as full as the live Wix page ({n_} words, live main text ≈ {live})")
    check("utm_" not in s_, f"/{rel} has no tracking parameters")
nu, _ = _main_words("courses/nursing-pathways-australia")
check(nu.count('href="https://www.nursingmidwiferyboard.gov.au/') >= 4 and "ahpra.gov.au" in nu, "/nursing: links the official NMBA/Ahpra steps")
check("not an Australian nursing qualification, a registration approval or a visa pathway" in nu, "/nursing: a course is not registration or a visa pathway")
check(nu.count("mailto:info@weintervisa.com?subject=Nursing") >= 5 and "<script" not in nu.split("<main")[1].split("</main>")[0], "/nursing: email enquiry links per course interest, no script")
# Readability pass 27 Nov 2026 (9.6 → 7.9 phone screens): course detail and page notes fold, nothing deleted
for _rel in ("courses/nursing-pathways-australia", "th/courses/nursing-pathways-australia"):
    _nm = (SITE / f"{_rel}.html").read_text().split("<main")[1].split("</main>")[0]
    check(_nm.count('class="faq course-fold"') == 4 and 'class="hero-img wide-only"' in _nm
          and 'class="faq notes"' in _nm and _nm.count("nursingmidwiferyboard.gov.au") >= 4,
          f"/{_rel}: 4 course folds, study picture wide screens only, sources folded but kept")
    check(_nm.split('id="prep"')[1].split('id="study"')[0].count("mailto:") == 0,
          f"/{_rel}: course list has no repeated email link (the email list is in #enquire)")
os_, _ = _main_words("oshc")
check(all(f"oshcstudents.com.au/client/{x}?affiliate=0JCJFK" in os_ for x in ("allianz", "bupa", "medibank", "ahm", "ovhc", "flywire")), "/oshc: same partner links as the live page")
check("never take your payment" in os_ and "registered migration agent" in os_, "/oshc: we never take payment; visa questions → registered migration agent")
ab, _ = _main_words("about-we-international")
check("QEAC No. 11964" in ab and "2023" in ab and "not a migration agent" in ab, "/about: QEAC number, since 2023, not a migration agent")
rp, _ = _main_words("referral-partners")
check('href="/partner-portal"' in rp and "mailto:info@weintervisa.com?subject=Referral%20partner%20application" in rp and "do not include personal information about students" in rp.lower(),
      "/referral-partners: apply by email (no student data), partner login → portal")
cu, _ = _main_words("contact-us")
check("https://m.me/113772648238480" in cu and 'href="/schedule"' in cu, "/contact-us: Messenger and booking links")
co, n_co = _main_words("courses")
_cj = json.loads((ROOT / "content/courses.json").read_text())
check(len(_cj["courses"]) >= 97 and co.count('<details class="faq course-item"') == len(_cj["courses"]), f"/courses lists every course from the live catalogue ({len(_cj['courses'])}), each opens with <details>")
check(n_co >= 950, f"/courses is as full as the live Wix page ({n_co} words, live ≈ 950)")
check(all(f'id="{a}"' in co for a in re.findall(r'href="#([\w-]+)"', co)), "/courses: every in-page link (interests, cities, groups) has a target")
# /courses readability (27 Nov 2026): 49 → ~7 phone screens without deleting a word — each study-area group and each
# study area list folds; topic pictures are wide-screen only; reveal.js opens the folds round a #link (older Safari/Firefox)
for _cf in ("courses", "th/courses"):
    _cm = (SITE / f"{_cf}.html").read_text().split('<main id="main">')[1].split("</main>")[0]
    check(_cm.count('<details class="group-fold"><summary><h2 id="c-') == 7 and '<script src="/assets/reveal.js" defer></script>' in _cm,
          f"/{_cf}: 7 course groups fold, h2 kept inside the summary, reveal.js loaded")
    check(len(re.findall(r'<details class="area-fold"><summary><h2 id="', _cm)) == _cm.count('<ul class="areas">') > 0,
          f"/{_cf}: every study-area list folds under its h2")
    check('<div class="topic"' in _cm and not re.search(r'<div class="topic" id="[^"]+"><img', _cm),
          f"/{_cf}: topic pictures are wide-screen only (wrapped in .wide-only)")
_rv = (ROOT / "assets/reveal.js").read_text()
check("DETAILS" in _rv and "hashchange" in _rv and "fetch" not in _rv and "localStorage" not in _rv, "assets/reveal.js only opens folds (no network, no storage)")
check(not re.search(r"Charter Australia|Rosehill|KCA Education|Danford|Britts College|Brighton College|VIA Education", co), "/courses: neutral listing, no college names (owner rule 26 Oct 2026)")
# 11. Migration agents (WEI-MIG-FORM-1120): cards only from GetWec "listed" data; rules stated
ms = (SITE / "migration-support.html").read_text()
check("We don&#x27;t receive any commission or benefit from listed agents" in ms or "We don't receive any commission or benefit from listed agents" in ms, "/migration-support says we receive no commission or benefit")
check("We are not a migration agent" in ms and "official register" in ms, "/migration-support says we are not a migration agent + check the MARN")
check(_cp.PARTNER_FORM in ms, "/migration-support links the GetWec Migration Partner form")
sample = [{"name": "Harbour <b>Visa</b> (sample)", "marn": "1234567", "url": "https://harbour.example/migration", "email": "a@harbour.example",
           "phone": "+61 2 0000 0000", "city": "Sydney", "online_au": True, "languages": ["English", "Thai"], "markets": "Thailand",
           "visa_types": ["Student (500)"], "intro": "<script>x</script>"},
          {"name": "Bad link (sample)", "marn": "7654321", "url": "javascript:alert(1)"}]
cards = _cp.partner_cards(sample)
check(cards.count('class="agent"') == 1, "agent cards skip entries without an https link")
check("<b>" not in cards and "<script>" not in cards and "&lt;script&gt;" in cards, "agent card text is escaped")
check('rel="noopener nofollow"' in cards and "MARN" in cards and "online across Australia" in cards, "agent card shows MARN, place and a nofollow link")
check("List coming soon" in _cp.partner_cards([]), "empty list shows 'coming soon' + referral link")
# 12. School pages (WEI-SCHOOL-BACKLOG-1120 step 4): only schools that sent us files; preview only until approved
import schools as _sc, subprocess
sd = json.loads((ROOT / "content/schools.json").read_text())["schools"]
check(all(x.get("source", {}).get("file") and x.get("source", {}).get("received") for x in sd), "every school names the file it sent us + date")
check(all(x["website"].startswith("https://") for x in sd), "school websites are https")
for x in sd:
    f = SITE / f"schools/{x['slug']}.html"
    check(f.exists(), f"/schools/{x['slug']} built in preview")
    s = f.read_text()
    check(s.count("<h1>") == 1 and "registered migration agent" in s and "offer letter" in s, f"/schools/{x['slug']} has one h1, visa note and fee caveat")
    check(not re.search(r"\bguarantee|best price|100% |free consultation|<img", s, re.I), f"/schools/{x['slug']} makes no promises and shows no unsupplied images")
    for c in x["courses"]:
        check(all(isinstance(c["fees"][col], int) for col in x["fee_columns"] if col in c["fees"]) and c["fees"]
              and (c.get("cricos") or "") in s and c["code"] in s, f"{x['slug']} {c['code']} fee + code (+ CRICOS when the school gave one) shown")
check(subprocess.run([sys.executable, "-c", "import sys; sys.argv=['x','--production']; import schools; "
                      "sys.exit(0 if all(s.get('approved') for s in schools.SCHOOLS) else 1)"], cwd=ROOT).returncode == 0,
      "production build includes only owner-approved schools")
check(("/schools" in (SITE / "courses.html").read_text()) == bool(_sc.SCHOOLS), "/courses links /schools only when a school is shown")
# 13. Languages (owner 20 Nov 2026): team = Thai + English only; Mia (AI) chats in many languages
for rel in ("index", "frequently-asked-questions"):
    s_ = (SITE / f"{rel}.html").read_text()
    check("Thai and English" in s_ or "Thai or English" in s_, f"/{rel} says our team speaks Thai and English")
check(not any(re.search(r"preferred language so we can arrange|any language you (like|want) with our team", s_, re.I) for s_ in pages.values()), "no page promises human support in other languages")
# 14. Thai pages (owner 20 Nov 2026): /th/..., html lang, hreflang both ways, switch on every page, Thai text
TH_CHARS = re.compile(r"[\u0E00-\u0E7F]")
for en_path, th_path in _tp.TH_OF.items():
    th_file = SITE / (th_path.strip("/") + ("/index.html" if th_path.endswith("/") else ".html"))
    en_file = SITE / ("index.html" if en_path == "/" else en_path.strip("/") + ".html")
    ts, es_ = th_file.read_text(), en_file.read_text()
    check('<html lang="th">' in ts and '<html lang="en">' in es_, f"{th_path} is lang=th, {en_path} is lang=en")
    for s_ in (ts, es_):
        check(f'hreflang="th" href="https://www.weintervisa.com{th_path}"' in s_ and 'hreflang="x-default"' in s_, f"{th_path} ↔ {en_path} hreflang pair")
    check(f'class="lang" href="{en_path}"' in ts and f'class="lang" href="{th_path}"' in es_, f"{th_path} ↔ {en_path} language switch")
    main_ = ts.split('<main id="main">')[1].split("</main>")[0]
    # English proper names (course titles, post titles, campuses) are marked lang="en" and not counted
    visible = re.sub(r"<[^>]+>", " ", re.sub(r'<(\w+)\b[^>]*\blang="en"[^>]*>.*?</\1>', " ", main_, flags=re.S))
    words = re.findall(r"[A-Za-z]{4,}", visible)
    check(len(TH_CHARS.findall(visible)) > 4 * len("".join(words)), f"{th_path} body is mainly Thai")
    check("registered migration agent" in ts and "ไม่ใช่ migration agent" in ts, f"{th_path} refers visa questions to a registered migration agent")
    check(not re.search(r"รับประกัน(ผล|ที่เรียน|วีซ่า|งาน)(?!ได้)|ฟรี|ภายใน 24 ชั่วโมง|ถูกที่สุด", main_.replace("ไม่มีใครรับประกันผลวีซ่าได้", "")), f"{th_path} makes no unapproved promises")
# 15. Thai set 3 (21 Nov 2026): courses, blog, schools in Thai; Thai nav points at Thai pages
import thai_more as _tm
tc = (SITE / "th/courses.html").read_text()
check(tc.count('<ul class="areas">') == len(_tm.GROUP_TH) and all(f'id="{_tm.group_anchor(g)}"' in tc for g in _tm.GROUP_TH),
      "/th/courses has every study-area group with the same anchors as /courses")
tb = (SITE / "th/blog.html").read_text()
check(set(re.findall(r'href="/post/([^"]+)"', tb)) == set(slugs) and 'lang="en"' in tb, f"/th/blog links all {len(slugs)} posts, titles marked lang=en")
check(("/th/schools" in _tp.EN_OF) == bool(_sc.SCHOOLS) and all(f"/th/schools/{s_['slug']}" in _tp.EN_OF for s_ in _sc.SCHOOLS),
      "Thai school pages exist exactly for the schools shown in English (none in production until approved)")
for s_ in _sc.SCHOOLS:
    t_ = (SITE / f"th/schools/{s_['slug']}.html").read_text()
    check(all(f'<td data-col="{c_}">' in t_ for c_ in s_["fee_columns"]) and t_.count('scope="row"') == len(s_["courses"]) and "offer letter" in t_,
          f"/th/schools/{s_['slug']}: same courses and fee columns as English, offer-letter note")
tp_ = (SITE / "th/privacy-policy.html").read_text()
ep_ = (SITE / "privacy-policy.html").read_text()
check(tp_.count("<h2>") == ep_.split('<main id="main">')[1].count("<h2>") and "ให้ถือตามฉบับภาษาอังกฤษ" in tp_ and "OAIC" in tp_ and "ซิดนีย์" in tp_ and "ไม่ใช้คุกกี้" in tp_,
      "/th/privacy-policy: same sections as the approved English notice, English prevails, Sydney, OAIC, no cookies")
check(all('href="/th/privacy-policy"' in (SITE / f"{r}.html").read_text() for r in ("th/index", "th/contact-us", "th/charter-application")), "Thai footer and Thai form consent link the Thai privacy notice")
navth = (SITE / "th/index.html").read_text().split('<nav class="wide">')[1].split("</nav>")[0]
check('href="/th/courses"' in navth and 'href="/th/english-practice"' in navth and 'href="/courses"' not in navth
      and 'href="/th/blog"' in (SITE / "th/index.html").read_text().split("<footer")[1], "Thai nav links Thai pages; Thai footer links the Thai blog")
tm = (SITE / "th/migration-support.html").read_text()
check("ไม่ได้รับค่าคอมมิชชันหรือผลประโยชน์ใดๆ" in tm and _cp.PARTNER_FORM in tm and "ทะเบียนทางการ" in tm, "/th/migration-support: no commission, MARN check, partner form link")
check("ภาษาไทยหรืออังกฤษ" in (SITE / "th/frequently-asked-questions.html").read_text() and '"FAQPage"' in (SITE / "th/frequently-asked-questions.html").read_text(), "/th/ FAQ: team replies in Thai or English + FAQPage data")
check("Thai and English" in (SITE / "student-services.html").read_text(), "/student-services says our team speaks Thai and English")
check(all('href="/th' + p_ + '"' in (SITE / "th/index.html").read_text() or p_.startswith(("/schools", "/working-holiday/", "/already-in-australia", "/courses/")) or p_ in ("/about-we-international", "/homestay", "/oshc", "/migration-support", "/frequently-asked-questions", "/referral-partners")
          for p_ in _tp.TH_OF if p_ != "/" and p_ not in ("/contact-us", "/charter-application")), "Thai home links Thai pages where they exist")
check(all('class="lang"' in s_ for p_, s_ in pages.items() if "http-equiv=\"refresh\"" not in s_), "every page has the language switch")
check(all(f.count('data-lead-form="') == 1 for f in [(SITE / "th/contact-us.html").read_text(), (SITE / "th/charter-application.html").read_text()]), "Thai contact + application pages have the lead form")
check("ภาษาไทยหรืออังกฤษ" in (SITE / "th/index.html").read_text(), "Thai home says our team replies in Thai or English")

# Images: every local image a post uses is in the repo (copied from Wix by the
# "Copy Wix images into the repo" workflow, tools/fetch_images.py); count what still loads from Wix.
_post_txt = "".join(p_.read_text() for p_ in (ROOT / "content/posts").glob("*.md"))
_local_imgs = set(re.findall(r"/assets/img/[\w.-]+", _post_txt))
_missing_imgs = [i for i in _local_imgs if not (ROOT / i.lstrip("/")).exists()]
check(not _missing_imgs, f"every local post image exists ({len(_local_imgs)} local)" + (f" — missing {_missing_imgs}" if _missing_imgs else ""))
_wix_imgs = len(set(re.findall(r"https://static\.wixstatic\.com/media/[\w~.-]+", _post_txt)))
check(_wix_imgs == 0 and all("static.wixstatic.com" not in s_ for s_ in pages.values()),
      f"no page loads images from Wix (Wix-hosted post images left: {_wix_imgs})")

# The production build connects only when the public key is set
import importlib.util, os
cfg = json.loads((ROOT / "config.json").read_text())
check(cfg.get("getwec_endpoint", "").startswith("https://") and cfg["getwec_endpoint"].endswith("/functions/v1/mia"),
      "GetWec endpoint configured (mia Edge Function)")

# 16. Thai copies of the pages rebuilt from live Wix (22 Nov 2026): same JSON keys and list lengths as the English
#     content, and the same sections (h2 count) on the page, so the Thai page never falls behind the English one.
TH_SYNC = {"homestay": "/homestay", "oshc": "/oshc", "nursing": "/courses/nursing-pathways-australia",
           "fast-track": "/fast-track-courses", "english-practice": "/english-practice",
           "about": "/about-we-international", "referral-partners": "/referral-partners"}


def _shape(x):
    if isinstance(x, dict):
        return {k: _shape(v) for k, v in x.items() if not k.startswith("_") and k != "ui"}
    if isinstance(x, list):
        return [_shape(v) for v in x]
    return type(x).__name__


for name_, en_path in TH_SYNC.items():
    en_j = json.loads((ROOT / f"content/{name_}.json").read_text())
    th_j = json.loads((ROOT / f"content/th/{name_}.json").read_text())
    check(_shape(en_j) == _shape(th_j), f"content/th/{name_}.json has the same fields and list lengths as content/{name_}.json")
    main_en = (SITE / (en_path.strip("/") + ".html")).read_text().split('<main id="main">')[1].split("</main>")[0]
    main_th = (SITE / ("th" + en_path + ".html")).read_text().split('<main id="main">')[1].split("</main>")[0]
    check(main_en.count("<h2") == main_th.count("<h2") and main_en.count('class="faq"') == main_th.count('class="faq"'),
          f"/th{en_path} has the same sections and FAQ as {en_path}")
# the Thai home is the English home's layout from content/th/home.json (the English home does not link /referral-partners either)
_he, _ht = (json.loads((ROOT / f).read_text()) for f in ("content/home.json", "content/th/home.json"))
check(_shape(_he) == _shape(_ht), "content/th/home.json has the same fields and list lengths as content/home.json")
_me, _mt = ((SITE / f).read_text().split('<main id="main">')[1].split("</main>")[0] for f in ("index.html", "th/index.html"))
check(_me.count("<h2") == _mt.count("<h2") and _mt.count('<li class="door">') == _me.count('<li class="door">') == 4
      and _mt.count('<li><a href="/th/') == _me.count('<li><a href="/') - _me.count('<li><a href="/th/'),
      "/th/ has the same sections, doors and help links as / (all Thai pages)")

# /th/courses is the same 97-course catalogue as /courses (22 Nov 2026): every English value has Thai words,
# the same course ids, topic and group anchors, Thai group names, course titles kept English (lang="en")
import courses_page as _cpg
from html import escape as e_
check(not _cpg.th_missing(), "content/th/courses.json has Thai words for every topic, focus, length, note, campus, city and group"
      + (f" — missing {_cpg.th_missing()[:5]}" if _cpg.th_missing() else ""))
_ce, _ct = ((SITE / f).read_text().split('<main id="main">')[1].split("</main>")[0] for f in ("courses.html", "th/courses.html"))
_ids = lambda h: re.findall(r'<details class="faq course-item" id="([^"]+)"', h)
_anc = lambda h: re.findall(r'id="((?:t|c)-[^"]+)"', h)
check(_ids(_ct) == _ids(_ce) and len(_ids(_ct)) == len(_cpg.COURSES) and _anc(_ct) == _anc(_ce),
      f"/th/courses lists the same {len(_cpg.COURSES)} courses with the same topic and group anchors as /courses")
check(_ct.count('<strong lang="en">') == len(_cpg.COURSES) and all(f">{e_(_cpg.TH['groups'][g])} <" in _ct for g in _cpg.GROUP_ORDER)
      and 'href="/charter-application"' not in _ct and 'href="/th/charter-application"' in _ct,
      "/th/courses: course titles marked lang=en, Thai group names, buttons go to Thai pages")

# 20. FAQ help page (22 Nov 2026): every page FAQ, by topic, same in Thai; structured data matches the page
import faq_page as _fq
for _lang, _rel in (("en", "frequently-asked-questions.html"), ("th", "th/frequently-asked-questions.html")):
    _fm = (SITE / _rel).read_text().split('<main id="main">')[1].split("</main>")[0]
    _ts = _fq.topics(_lang)
    _n = sum(len(t[4]) for t in _ts)
    check(_fm.count('<details class="faq">') == _n and all(f'id="{t[0]}"' in _fm and f'href="#{t[0]}"' in _fm for t in _ts),
          f"/{_rel[:-5]}: {_n} questions in {len(_ts)} topics, each topic in the jump bar")
    for _name in ("fast-track", "nursing", "homestay", "oshc", "referral-partners"):
        _src = json.loads((ROOT / "content" / ("th" if _lang == "th" else "") / f"{_name}.json").read_text())["faq"]
        check(all(html_unescape(q) in html_unescape(_fm) for q, _ in _src), f"/{_rel[:-5]} has every {_name} FAQ question")
    _ld = json.loads(re.search(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "FAQPage".*?)</script>',
                               (SITE / _rel).read_text(), re.S).group(1))
    check(len(_ld["mainEntity"]) == _n and not any("<" in q["acceptedAnswer"]["text"] for q in _ld["mainEntity"]),
          f"/{_rel[:-5]}: FAQPage data lists all {_n} questions as plain text")
check([t[0] for t in _fq.topics("en")] == [t[0] for t in _fq.topics("th")]
      and [len(t[4]) for t in _fq.topics("en")] == [len(t[4]) for t in _fq.topics("th")], "Thai FAQ has the same topics and question counts as English")
check("IELTS" in (SITE / "frequently-asked-questions.html").read_text(), "FAQ keeps the Wix IELTS / TOEIC question (now answered by /english-practice)")

# Owner 22 Nov 2026: Wix app pages decided (option ก) and the first two schools approved for the live site.
_moves = {"videos": "/blog", "challenges": "/english-practice", "members": "https://getwec.pages.dev/", "file-share": "https://getwec.pages.dev/"}
check(all(f'url={t}"' in (SITE / f"{r}.html").read_text() for r, t in _moves.items()), "Wix app pages /videos /challenges /members /file-share redirect (owner 22 Nov)")
check(json.loads((ROOT / "tests/pending-pages.json").read_text()) == [], "no Wix pages left waiting for an owner decision")
_sch = json.loads((ROOT / "content/schools.json").read_text())["schools"]
check({x["name"] for x in _sch if x.get("approved")} >= {"Alana Kaye College", "Frontier Education"}, "Alana Kaye College and Frontier Education approved for the live site (owner 22 Nov)")

# Redesign mockups for the owner (WEI-WEB-REDESIGN-1123, 24 Nov 2026): preview only, readable, honest.
_rd = {r: (SITE / "redesign" / f"{r}.html").read_text() for r in ["index", "home-a", "home-b", "working-holiday-a", "working-holiday-b"]}
check(all('content="noindex' in s for s in _rd.values()) and "/redesign" not in (SITE / "sitemap.xml").read_text(), "redesign mockups are noindex and not in the sitemap")
check(all("for review only" in s and "registered migration agent" in s and "QEAC 11964" in s for s in _rd.values()), "redesign mockups say 'for review only', keep the migration-agent line and the QEAC number")
check(all(not re.search(r"guarantee|100% |best price|within (24 hours|one business day)", s, re.I) for s in _rd.values()), "redesign mockups make no unapproved promises")
check(all(len(re.sub(r"<[^>]+>", " ", s.split("<main>")[1].split("</main>")[0]).split()) <= 400 for r, s in _rd.items() if r != "index"),
      "redesign mockups stay short (≤ 400 words in the page body)")
check(all("fictional, AI-generated" in s for r, s in _rd.items() if re.search(r'alt="Maya', s)), "mockups that show Maya and Kenji say they are fictional, AI-generated")
check(all(len(html_unescape(re.sub(r"<[^>]+>", "", p_))) <= 320 for s in _rd.values() for p_ in re.findall(r"<p[^>]*>(.*?)</p>", s, re.S)),
      "redesign mockups: no paragraph over 320 characters of text")

# SEO lengths on every sitemap page (same rule as GetWec #/seo, skill seo-site-check): description 50–160
# characters; title ≤ 60 except blog posts, whose titles stay the same as the live Wix posts.
_bad_desc, _bad_title = [], []
for _loc in re.findall(r"<loc>([^<]+)</loc>", (SITE / "sitemap.xml").read_text()):
    _path = _loc.split("weintervisa.com", 1)[1] or "/"
    _f = SITE / ("index.html" if _path == "/" else _path.strip("/") + ".html")
    if not _f.exists():
        _f = SITE / _path.strip("/") / "index.html"
    _s = _f.read_text()
    _d = html_unescape((re.search(r'<meta name="description" content="([^"]*)"', _s) or [None, ""])[1])
    _t = html_unescape((re.search(r"<title>(.*?)</title>", _s, re.S) or [None, ""])[1]).strip()
    if not 50 <= len(_d) <= 160: _bad_desc.append(f"{_path} ({len(_d)})")
    if not _path.startswith("/post/") and not 15 <= len(_t) <= 60: _bad_title.append(f"{_path} ({len(_t)})")
check(not _bad_desc, "every sitemap page has a 50–160 character description" + (f": {_bad_desc[:5]}" if _bad_desc else ""))
check(not _bad_title, "every sitemap page (not blog posts) has a 15–60 character title" + (f": {_bad_title[:5]}" if _bad_title else ""))

# Working Holiday schools (owner 25 Nov 2026, WEI-WHV-CHARTER-1125): Charter first, then KCA; facts from the
# schools' own files; one "Enrol with us" form → GetWec (whv_enrol); no commission, no visa advice.
_wv = {k: (SITE / "working-holiday" / f"{k}.html").read_text() for k in ("charter", "kca")}
for k, s_ in _wv.items():
    check(s_.count('data-lead-form="whv_enrol"') == 1 and "/assets/forms.js" in s_ and 'name="visa_end"' in s_ and 'name="consent"' in s_,
          f"/working-holiday/{k}: one Enrol with us form (name, email, visa end, course, consent)")
    check("condition 8548" in s_ and "registered migration agent" in s_ and "QEAC No. 11964" in s_, f"/working-holiday/{k}: 4-month rule, migration agent line, QEAC number")
    check(not re.search(r"commission|guarantee|25%", s_, re.I), f"/working-holiday/{k}: no commission or guarantee words")
    check("passport numbers" in s_, f"/working-holiday/{k}: asks people not to send passport numbers")
check("A$6,800" in _wv["charter"] and "A$7,700" in _wv["charter"] and "30 June 2027" in _wv["charter"] and "RTO 41038" in _wv["charter"],
      "/working-holiday/charter: fees from Charter's 2027 SWP fee table")
check("A$5,150" in _wv["kca"] and "16 weeks" in _wv["kca"] and "close to the 4-month study limit" in _wv["kca"], "/working-holiday/kca: KCA fees + 16-week warning")
_ftp = (SITE / "fast-track-courses.html").read_text()
check(_ftp.index('href="/working-holiday/charter"') < _ftp.index('href="/working-holiday/kca"') < _ftp.index('id="finder"'),
      "/fast-track-courses shows Charter first, then KCA, before the course finder")
check('href="/th/working-holiday/charter"' in (SITE / "th/fast-track-courses.html").read_text(), "/th/fast-track-courses links the Thai Working Holiday school pages")
# Thai school pages (26 Nov 2026): same facts as English, same form (option values English for GetWec), Thai words.
import json as _json, html
_whe = _json.loads((ROOT / "content/working-holiday.json").read_text())["schools"]
_wht = _json.loads((ROOT / "content/th/working-holiday.json").read_text())["schools"]
check([s_["slug"] for s_ in _whe] == [s_["slug"] for s_ in _wht] and all(
      a["fees"] and len(a["fees"]) == len(b["fees"]) and len(a["points"]) == len(b["points"])
      and len(a["fee_notes"]) == len(b["fee_notes"]) and a["options"] == b["options"] and bool(a.get("warn")) == bool(b.get("warn"))
      and [re.findall(r"A\$[\d,]+", c) for r in a["fees"] for c in r] == [re.findall(r"A\$[\d,]+", c) for r in b["fees"] for c in r]
      and [re.findall(r"A\$[\d,]+", c) for c in a["fee_notes"]] == [re.findall(r"A\$[\d,]+", c) for c in b["fee_notes"]]
      and set(b["option_labels"]) == set(o for s_ in _whe for o in s_["options"])
      for a, b in zip(_whe, _wht)), "Thai Working Holiday JSON: same schools, rows, prices and option values as the English JSON")
for k in ("charter", "kca"):
    t_ = (SITE / "th/working-holiday" / f"{k}.html").read_text()
    check('<html lang="th"' in t_ and 'hreflang="en" href=' in t_ and f'/working-holiday/{k}"' in t_, f"/th/working-holiday/{k}: Thai page paired with English")
    check(t_.count('data-lead-form="whv_enrol"') == 1 and 'value="Charter: CHC33021 Individual Support (aged care)"' in t_ and 'value="Not sure yet"' in t_
          and "/th/privacy-policy" in t_, f"/th/working-holiday/{k}: one form, English option values for GetWec, Thai consent")
    check("เงื่อนไข 8548" in t_ and "QEAC No. 11964" in t_ and "ไม่ใช่ migration agent" in t_ and not re.search(r"commission|ค่าคอม|25%", t_, re.I),
          f"/th/working-holiday/{k}: 4-month rule, QEAC, not a migration agent, no commission")
check("A$5,150" in (SITE / "th/working-holiday/kca.html").read_text() and "16 สัปดาห์ใกล้กับเพดานเรียน 4 เดือน" in (SITE / "th/working-holiday/kca.html").read_text(), "/th/working-holiday/kca: price + 16-week warning")


# 26 Nov 2026 (policy-wei-enrolment-focus, item 6): "Already in Australia? Study alongside your visa" (EN + TH).
# Only general Home Affairs facts with the source, the exact check line, no per-person visa answer,
# no commission / countdown / promised job, visa or PR; Working Holiday form with "Not sure yet" first.
_aa = (SITE / "already-in-australia.html").read_text()
_at = (SITE / "th/already-in-australia.html").read_text()
check("Check your visa conditions on" in _aa and "homeaffairs.gov.au" in _aa and "or with a registered migration agent" in _aa,
      "/already-in-australia: 'Check your visa conditions on homeaffairs.gov.au or with a registered migration agent'")
check("condition 8548" in _aa and "4 months on each visa" in _aa and "work-conditions.aspx" in _aa and "not advice about your visa" in _aa,
      "/already-in-australia: 4-month rule (8548) with the Home Affairs source, general information only")
check(_aa.count('data-lead-form="whv_enrol"') == 1 and 'name="visa"' in _aa and 'name="visa_end"' in _aa
      and '<option selected>Not sure yet</option>' in _aa and 'name="consent"' in _aa,
      "/already-in-australia: one Enrol with us form (visa, visa end, course starts on Not sure yet, consent)")
check(_aa.index('href="/working-holiday/charter"') < _aa.index('href="/working-holiday/kca"'), "/already-in-australia: Charter first, then KCA")
check("Ask us about current scholarships and offers" in _aa and not re.search(r"commission|guarantee|countdown|% off|you can study|you are eligible|\bPR\b", _aa, re.I),
      "/already-in-australia: offers only on request; no commission, guarantee, countdown or per-person visa answer")
check('<html lang="th"' in _at and 'hreflang="en"' in _at and "เงื่อนไข 8548" in _at and "registered migration agent" in _at
      and 'value="Not sure yet" selected' in _at and "/th/privacy-policy" in _at and 'href="/th/working-holiday/charter"' in _at,
      "/th/already-in-australia: Thai pair, 8548, migration agent line, English option values, Thai consent")
check('href="/already-in-australia"' in (SITE / "fast-track-courses.html").read_text()
      and 'href="/th/already-in-australia"' in (SITE / "th/fast-track-courses.html").read_text(),
      "/fast-track-courses (EN + TH) link the Already in Australia page")

# 15. /courses/aged-care-certificate-iii (policy-wei-enrolment-focus-20261126 items 1-3): one course, 4 schools
_ce = (SITE / "courses/aged-care-certificate-iii.html").read_text()
_ct = (SITE / "th/courses/aged-care-certificate-iii.html").read_text()
_rows = _ce.split("<tbody>")[1].split("</tbody>")[0]
_order = [n for n in ("KCA Education", "Charter Australia", "Alana Kaye College", "Frontier Education") if n in _rows]
check(len(_order) == 4 and [_rows.index(n) for n in _order] == sorted(_rows.index(n) for n in _order),
      "/courses/aged-care-certificate-iii: 4 schools, shortest first (KCA 16 weeks, Charter, then 52-week CRICOS courses)")
_whv = {x["slug"]: x for x in json.loads((ROOT / "content/working-holiday.json").read_text())["schools"]}
_sch = {x["slug"]: x for x in json.loads((ROOT / "content/schools.json").read_text())["schools"]}
_need = [dict(_whv["kca"]["fees"])["Total"], next(r for r in _whv["charter"]["fees"] if r[1].startswith("CHC33021"))[3]]
for _sl in ("alana-kaye-college", "frontier-education"):
    _c = next(c for c in _sch[_sl]["courses"] if c["code"] == "CHC33021")
    _need += [f"A${v:,}" for v in _c["fees"].values()]
check(all(a in _rows for a in _need) and all(a in _ct for a in _need),
      "/courses/aged-care-certificate-iii (EN + TH): every A$ amount matches the school data files")
check(all(h in _ce for h in ('href="/working-holiday/kca"', 'href="/working-holiday/charter"', 'href="/schools/alana-kaye-college"', 'href="/schools/frontier-education"'))
      and 'href="/th/schools/frontier-education"' in _ct, "/courses/aged-care-certificate-iii: each row links the school page (Thai links Thai)")
check(_ce.count('data-lead-form="application"') == 1 and 'name="school"' in _ce and 'value="Not sure yet" selected' in _ce
      and "<option selected>Aged care / individual support</option>" in _ce and 'name="consent"' in _ce
      and _ct.count('data-lead-form="application"') == 1 and "<option selected>งานดูแลผู้สูงอายุ / Individual support</option>" in _ct,
      "/courses/aged-care-certificate-iii: one application form set to aged care + School choice (Not sure yet) + consent")
check("or with a registered migration agent" in _ce and "หรือกับ registered migration agent" in _ct and "8548" in _ce and "8548" in _ct
      and not re.search(r"commission|guarantee|guaranteed|get a job|permanent residency|\bPR\b", re.sub(r"<[^>]+>", " ", _ce), re.I),
      "/courses/aged-care-certificate-iii: visa check line + 8548, no commission / job / PR promises")
check('href="/courses/aged-care-certificate-iii"' in (SITE / "fast-track-courses.html").read_text()
      and 'href="/th/courses/aged-care-certificate-iii"' in (SITE / "th/fast-track-courses.html").read_text()
      and 'href="/courses/aged-care-certificate-iii"' in _aa, "/fast-track-courses + /already-in-australia link the comparison (EN + TH)")

# 16. /courses/childcare-certificate-iii (policy-wei-enrolment-focus items 1-3, 7): Charter CHC30125 + Alana Kaye CHC30121
_he = (SITE / "courses/childcare-certificate-iii.html").read_text()
_ht = (SITE / "th/courses/childcare-certificate-iii.html").read_text()
_hrows = _he.split("<tbody>")[1].split("</tbody>")[0]
_hrows_t = _ht.split("<tbody>")[1].split("</tbody>")[0]
check(_hrows.count("<tr>") == 2 and _hrows.index("Charter Australia") < _hrows.index("Alana Kaye College")
      and "Frontier" not in _hrows and "KCA" not in _hrows,
      "/courses/childcare-certificate-iii: 2 schools that sent a childcare course (Charter, then Alana Kaye), no others")
_cr = next(r for r in _whv["charter"]["fees"] if r[1].startswith("CHC30125"))
_now, _was = re.fullmatch(r"(A\$[\d,]+) \(special, was (A\$[\d,]+)\)", _cr[3]).groups()
_end = re.search(r"until (\d+ \w+ \d{4})", " ".join(_whv["charter"]["fee_notes"])).group(1)
_ak = next(c for c in _sch["alana-kaye-college"]["courses"] if c["code"] == "CHC30121")
_hneed = [_now, _was, _cr[4]] + [f"A${v:,}" for v in _ak["fees"].values()]
check(all(a in _hrows and a in _hrows_t for a in _hneed) and f"special price until {_end}" in _hrows and "30 มิ.ย. 2027" in _hrows_t,
      "/courses/childcare-certificate-iii (EN + TH): every A$ matches the school files; the special price shows its real end date")
check("CHC30125" in _he and "CHC30121" in _he and "not the same at both schools" in _he and "same course code" not in _he
      and "ไม่เหมือนกัน" in _ht, "/courses/childcare-certificate-iii: each school's own course code, never called the same")
check(_he.count('data-lead-form="application"') == 1 and 'value="Not sure yet" selected' in _he
      and "<option selected>Early childhood education</option>" in _he and "<option selected>Certificate III</option>" in _he
      and 'value="Charter Australia"' in _he and 'value="Alana Kaye College"' in _he
      and "<option selected>การศึกษาปฐมวัย</option>" in _ht and 'value="Alana Kaye College"' in _ht and "/th/privacy-policy" in _ht,
      "/courses/childcare-certificate-iii: one application form set to early childhood + Cert III + School choice (EN values on TH)")
check("or with a registered migration agent" in _he and "หรือกับ registered migration agent" in _ht and "8548" in _he and "8548" in _ht
      and not re.search(r"commission|guarantee|guaranteed|get a job|permanent residency|\bPR\b|countdown|% off", re.sub(r"<[^>]+>", " ", _he), re.I),
      "/courses/childcare-certificate-iii: visa check line + 8548, no commission / job / PR / countdown")
check('<html lang="th"' in _ht and 'hreflang="en"' in _ht and 'href="/th/schools/alana-kaye-college"' in _ht
      and 'href="/th/working-holiday/charter"' in _ht and "CHC50121" in _he,
      "/th/courses/childcare-certificate-iii: Thai pair links Thai school pages; Diploma shown as a fact")
check(all('href="/courses/childcare-certificate-iii"' in (SITE / f).read_text() for f in ("fast-track-courses.html", "already-in-australia.html", "courses/aged-care-certificate-iii.html"))
      and all('href="/th/courses/childcare-certificate-iii"' in (SITE / f).read_text() for f in ("th/fast-track-courses.html", "th/already-in-australia.html", "th/courses/aged-care-certificate-iii.html"))
      and 'href="/courses/aged-care-certificate-iii"' in _he,
      "/fast-track-courses, /already-in-australia and the aged care page link the childcare comparison (EN + TH), and back")

# 17. /courses/health-services-assistance-certificate-iii (policy items 1-3): Charter HLT33115, 2 ways in
_se = (SITE / "courses/health-services-assistance-certificate-iii.html").read_text()
_st = (SITE / "th/courses/health-services-assistance-certificate-iii.html").read_text()
_srows = _se.split("<tbody>")[1].split("</tbody>")[0]
_srows_t = _st.split("<tbody>")[1].split("</tbody>")[0]
check(_srows.count("<tr>") == 2 and _srows_t.count("<tr>") == 2 and _srows.index("IELTS 5.5") < _srows.index("IELTS 4.5")
      and "KCA" not in _srows and "Alana" not in _srows and "Frontier" not in _srows,
      "/courses/health-services-assistance-certificate-iii: Charter only, start HLT33115 (IELTS 5.5) then English first (IELTS 4.5)")
_hl = [r for r in _whv["charter"]["fees"] if "HLT33115" in r[1]]
_sneed = [a for r in _hl for a in [r[3]] + re.findall(r"A\$[\d,]+", r[4])]
check(len(_hl) == 2 and all(a in _srows and a in _srows_t for a in _sneed) and "placement fee" in _srows and "ค่าฝึกงาน" in _srows_t,
      "/courses/health-services-assistance-certificate-iii (EN + TH): every A$ (tuition, materials, placement) matches Charter's file")
check(_se.count('data-lead-form="application"') == 1 and 'value="Not sure yet" selected' in _se and _se.count('value="Charter Australia"') == 1
      and "<option selected>Health services assistance</option>" in _se and "<option selected>Certificate III</option>" in _se
      and "<option selected>ผู้ช่วยงานบริการสุขภาพ</option>" in _st and 'value="Charter Australia"' in _st,
      "/courses/health-services-assistance-certificate-iii: one application form set to health services + Cert III + one Charter choice")
check("or with a registered migration agent" in _se and "หรือกับ registered migration agent" in _st and "8548" in _se and "8548" in _st
      and not re.search(r"commission|guarantee|guaranteed|get a job|permanent residency|\bPR\b|countdown|% off", re.sub(r"<[^>]+>", " ", _se), re.I),
      "/courses/health-services-assistance-certificate-iii: visa check line + 8548, no commission / job / PR / countdown")
_sp = "courses/health-services-assistance-certificate-iii"
check(all(f'href="/{_sp}"' in (SITE / f).read_text() for f in ("fast-track-courses.html", "already-in-australia.html", "courses/aged-care-certificate-iii.html", "courses/childcare-certificate-iii.html"))
      and all(f'href="/th/{_sp}"' in (SITE / f).read_text() for f in ("th/fast-track-courses.html", "th/already-in-australia.html", "th/courses/childcare-certificate-iii.html"))
      and 'href="/courses/aged-care-certificate-iii"' in _se and 'href="/courses/childcare-certificate-iii"' in _se
      and '<html lang="th"' in _st and 'href="/th/working-holiday/charter"' in _st,
      "hospital comparison linked from fast-track, already-in-australia and both other comparisons (EN + TH), and links back")

# Security (WEI-SEC-1126, skill security-basics): no keys or tokens anywhere in the repo files (public repo)
_SECRET = re.compile("|".join([r"sk-ant-[A-Za-z0-9-]{10,}", r"sb_secret_[A-Za-z0-9_-]{10,}", r"service_role\s*[:=]\s*['\"]ey",
    r"sk_live_[A-Za-z0-9]{10,}", r"ghp_[A-Za-z0-9]{30,}", r"github_pat_[A-Za-z0-9_]{30,}", r"gh[ousr]_[A-Za-z0-9]{30,}",
    r"AKIA[0-9A-Z]{16}", r"AIza[0-9A-Za-z_-]{35}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"xox[bap]-[0-9A-Za-z-]{10,}"]))
_tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
_leaks = []
for _f in _tracked + [str(p.relative_to(ROOT)) for p in pages]:
    _p = ROOT / _f
    if _p.is_file() and _p.suffix.lower() in {".py", ".js", ".mjs", ".json", ".html", ".css", ".md", ".yml", ".yaml", ".txt", ".xml", ".toml"}:
        if _SECRET.search(_p.read_text(errors="ignore")):
            _leaks.append(_f)
check(not _leaks, "no keys or tokens in repo files or built pages" + (f" — {sorted(set(_leaks))}" if _leaks else ""))

# unslop polish (WEI-SKILL-UNSLOP-1126): forms carry class "lead" like the intro paragraph; the form must not inherit
# the intro's muted colour and 19px size, and WHV prices use tabular figures
_css = (ROOT / "assets/site.css").read_text()
check("form.lead { color: var(--ink); font-size: 17px; }" in _css and "font-variant-numeric: tabular-nums" in _css,
      "lead forms use ink text at body size (not the muted .lead intro style); fee prices use tabular figures")
check(all('id="enrol"' in (SITE / f).read_text() and "wrap narrow join" in (SITE / f).read_text()
          for f in ("working-holiday/charter.html", "working-holiday/kca.html", "th/working-holiday/charter.html", "th/working-holiday/kca.html")),
      "Working Holiday school pages (EN + TH): enrol form joins the page without an extra section gap")

# Charter fee table grouped by stream (27 Nov 2026): one heading per stream, jump links, every fee row and amount kept
import json as _json, html
for _lang, _jf, _hf in (("EN", "content/working-holiday.json", "working-holiday/charter.html"), ("TH", "content/th/working-holiday.json", "th/working-holiday/charter.html")):
    _cs = next(s for s in _json.loads((ROOT / _jf).read_text())["schools"] if s["slug"] == "charter")
    _ch = (SITE / _hf).read_text()
    _tb = _ch[_ch.index('<div class="fees grouped">'):]
    _tb = _tb[:_tb.index("</table>")]
    _streams = list(dict.fromkeys(r[0] for r in _cs["fees"]))
    check(_tb.count('<tr class="grp"') == len(_streams) == _ch.count('<ul class="fee-jump">') * len(_streams)
          and all(f'href="#{_wv0.group_id(g)}"' in _ch and f'id="{_wv0.group_id(g)}"' in _tb for g in _streams)
          and _tb.count('<th scope="row"') == len(_cs["fees"]) and _tb.count('class="amt"') == len(_cs["fees"])
          and all(html.escape(v) in _tb for r in _cs["fees"] for v in r[1:]),
          f"Charter fees ({_lang}): grouped by stream ({len(_streams)} headings + jump links), all {len(_cs['fees'])} rows and every amount kept")
check('<ul class="fee-jump">' not in (SITE / "working-holiday/kca.html").read_text(), "KCA fee table (no repeated stream) stays a plain table")

# unslop polish of /fast-track-courses (27 Nov 2026): no emoji in <main> (line icons instead), and a <strong> inside a tip stays inline
import re as _re
_EMO = _re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u25B6]")
for _f, _n in (("fast-track-courses.html", 10), ("th/fast-track-courses.html", 10), ("homestay.html", 10), ("th/homestay.html", 10)):
    _h = (SITE / _f).read_text()
    _m = _h[_h.index("<main"):_h.index("</main>")]
    check(not _EMO.findall(_m) and _m.count('<svg class="ico') >= _n, f"{_f}: no emoji in main, line icons instead (≥{_n})")
for _f, _n in (("courses.html", 20), ("th/courses.html", 20), ("english-practice.html", 14), ("th/english-practice.html", 14),
               ("take-a-break.html", 4), ("th/take-a-break.html", 4)):
    _h = (SITE / _f).read_text()
    _m = _h[_h.index("<main"):_h.index("</main>")]
    check(_m.count('<svg class="ico') >= _n, f"{_f}: line icons in place of emoji (≥{_n})")
# whole site (27 Nov 2026, 16:13 run): no emoji in any page's <main> (redesign mock-ups excluded)
_EMO2 = _re.compile("[\U0001F0A0-\U0001F0FF\U0001F300-\U0001FAFF\u2600-\u27BF\u25B6]")
_emo_pages = []
for _p in SITE.rglob("*.html"):
    if "redesign" in _p.parts:
        continue
    _h = _p.read_text()
    if "<main" in _h and _EMO2.search(_h[_h.index("<main"):_h.index("</main>")]):
        _emo_pages.append(str(_p.relative_to(SITE)))
check(not _emo_pages, f"no emoji in <main> on any page (found: {_emo_pages[:5]})")
check(".tip > strong:first-child { display: block" in _css and ".tip strong { display: block" not in _css,
      "tip title is the only block <strong> (\"up to 4 months\" stays in the sentence)")

# one solid button per screen on /fast-track-courses (27 Nov 2026, 16:13 run): the three course cards use a ghost button
for _f in ("fast-track-courses.html", "th/fast-track-courses.html"):
    _h = (SITE / _f).read_text()
    _m = _h[_h.index("<main"):_h.index("</main>")]
    _links = _re.findall(r'<p class="links">(.*?)</p>', _m, _re.S)
    check(len(_links) == 3 and all('class="btn ghost"' in l and 'class="btn"' not in l for l in _links),
          f"{_f}: course cards use a ghost button (one solid button per screen)")

# /blog readability (27 Nov 2026, 22:13 run): 6 newest as picture cards, the rest as title + date rows folded by topic;
# every post still linked from /blog, /th/blog and its topic page (crawl + old links)
_bc = json.loads((ROOT / "content/blog-categories.json").read_text())["categories"]
for _f in ("blog.html", "th/blog.html"):
    _h = (SITE / _f).read_text()
    _m = _h[_h.index("<main"):_h.index("</main>")]
    check(_m.count('<li class="card">') == 6 and set(_re.findall(r'href="/post/([^"]+)"', _m)) == set(slugs)
          and _m.count('<details class="group-fold">') == len(_bc) and all(f'id="{c_["slug"]}"' in _m for c_ in _bc)
          and "/assets/reveal.js" in _h, f"{_f}: 6 latest cards + every post in a topic fold ({len(slugs)} posts)")
for c_ in _bc:
    _h = (SITE / f"blog/categories/{c_['slug']}.html").read_text()
    _m = _h[_h.index("<main"):_h.index("</main>")]
    check(set(_re.findall(r'href="/post/([^"]+)"', _m)) >= set(c_["posts"]) and _m.count('<li class="card">') == min(6, len(c_["posts"])),
          f"/blog/categories/{c_['slug']}: ≤6 cards, every topic post linked")
check(".post-rows a {" in _css and "min-height: 44px" in _css.split(".post-rows a {")[1].split("}")[0], "blog rows are ≥44 px tap targets")

# /fast-track-courses readability (28 Nov 2026, 08:13 run): 12.1 -> 9.0 phone screens, no words deleted.
# Each course folds (id on the <details> so the finder opens it via reveal.js), photos wide screens only,
# settle-in cards fold, the compare links and "why in demand" sources fold; every link stays in the HTML.
for _f, _pre in (("fast-track-courses.html", ""), ("th/fast-track-courses.html", "/th")):
    _fd = json.loads((ROOT / ("content/th/fast-track.json" if _pre else "content/fast-track.json")).read_text())
    _h = (SITE / _f).read_text()
    _m = _h[_h.index("<main"):_h.index("</main>")]
    check(all(f'<details class="group-fold ft-fold" id="{c["id"]}">' in _m for c in ftd["courses"])
          and _m.count('class="wide-only"') >= 3 and "/assets/reveal.js" in _h,
          f"{_f}: courses fold with their finder id, course photos wide screens only, reveal.js loaded")
    check(_m.count('<li class="path"><details class="group-fold ft-fold">') == len(_fd["settle"])
          and all(f'href="{u}"' in _m.replace("&amp;", "&") for _i, _t, _b, _l, u, _l2, _u2 in _fd["settle"]),
          f"{_f}: settle-in cards fold, every link kept")
    check(all(f'href="{_pre}/courses/{_c}"' in _m for _c in ("aged-care-certificate-iii", "childcare-certificate-iii", "health-services-assistance-certificate-iii"))
          and f'href="{_pre}/already-in-australia"' in _m and _m.count("jobsandskills") + _m.count("Jobs and Skills") >= 1,
          f"{_f}: compare links + already-in-Australia + official job sources still linked")
check(words_ft >= 1000, f"/fast-track-courses keeps every word in the HTML after folding ({words_ft})")
check(".ft-fold { scroll-margin-top: 72px; }" in _css, "course folds land below the sticky header")

# /homestay readability (28 Nov 2026, 08:13 run): 9.8 -> 8.5 phone screens, no words deleted; every price row,
# both years, the matching fee, the "can change" note and the source stay visible; house-rule cards fold.
for _f, _j in (("homestay.html", "content/homestay.json"), ("th/homestay.html", "content/th/homestay.json")):
    _hd = json.loads((ROOT / _j).read_text())
    _h = (SITE / _f).read_text()
    _m = _h[_h.index("<main"):_h.index("</main>")]
    _tb = _m[_m.index('<div class="fees all compact">'):]
    _tb = _tb[:_tb.index("</table>")]
    check(all(html.escape(v) in _tb for r in _hd["prices"]["rows"] for v in r) and html.escape(_hd["prices"]["note"]) in _m
          and html.escape(_hd["prices"]["source"]) in _m and "<details" not in _tb,
          f"{_f}: every price row and year visible (not folded), note + source kept")
    check(_m.count('<li class="path"><details class="group-fold ft-fold">') == len(_hd["know"])
          and all(html.escape(x) in _m for _t, items in _hd["know"] for x in items)
          and all(html.escape(x) in _m for x in _hd["applyBox"]["items"]),
          f"{_f}: good-to-know cards fold, every rule and apply reason kept")

print("\n".join(notes + fails))
print(f"\n{len(notes) - 1} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
