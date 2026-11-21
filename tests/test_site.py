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
n_static = len(_p.PAGES) + len(_cp.CONTENT_PAGES) + 2 + len(_tp.TH_PAGES)  # + Thai home, Thai blog and Thai pages
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
# 10. Home page — from the CMS home draft; every study-area group links to its section on /courses
hd = json.loads((ROOT / "content/home.json").read_text())
check(hd["heading"] in html_unescape(home) and home.count("<h1>") == 1, "home uses the CMS heading as its one h1")
check(f'<title>{hd["seoTitle"]}</title>' in html_unescape(home) and hd["seoDescription"] in html_unescape(home), "home has the CMS SEO title + description")
for anchor in set(re.findall(r'href="/courses#([\w-]+)"', home)):
    check(f'id="{anchor}"' in c, f"home chip /courses#{anchor} has a matching section")
check(len(re.findall(r'href="/courses#', home)) == len({a["group"] for a in json.loads((ROOT / "content/study-areas.json").read_text())}), "home links every study-area group")
check("registered migration agent" in home.split("<footer")[0], "home body refers visa questions to a registered migration agent")
check(not re.search(r"\bfree consultation|within (24 hours|one business day)|guarantee(d)? (place|visa|job)|100% |best price", home, re.I), "home makes no unapproved promises")
check('"WebSite"' in home and '"Organization"' in home, "home has Organization + WebSite structured data")
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
        check(all(isinstance(c["fees"][col], int) for col in x["fee_columns"]) and c["cricos"] in s, f"{x['slug']} {c['code']} fee + CRICOS shown")
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
check(tb.count('<li class="card">') == len(slugs) and 'lang="en"' in tb, f"/th/blog lists all {len(slugs)} posts, titles marked lang=en")
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
check('href="/th/courses"' in navth and 'href="/th/blog"' in navth and 'href="/courses"' not in navth, "Thai nav links Thai courses and blog")
tm = (SITE / "th/migration-support.html").read_text()
check("ไม่ได้รับค่าคอมมิชชันหรือผลประโยชน์ใดๆ" in tm and _cp.PARTNER_FORM in tm and "ทะเบียนทางการ" in tm, "/th/migration-support: no commission, MARN check, partner form link")
check("ภาษาไทยหรืออังกฤษ" in (SITE / "th/frequently-asked-questions.html").read_text() and '"FAQPage"' in (SITE / "th/frequently-asked-questions.html").read_text(), "/th/ FAQ: team replies in Thai or English + FAQPage data")
check("Thai and English" in (SITE / "student-services.html").read_text(), "/student-services says our team speaks Thai and English")
check(all('href="/th' + p_ + '"' in (SITE / "th/index.html").read_text() or p_.startswith("/schools") or p_ in ("/about-we-international", "/homestay", "/oshc", "/migration-support", "/frequently-asked-questions")
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
check(all("static.wixstatic.com" not in s_ for s_ in pages.values()) if _wix_imgs == 0 else True,
      f"Wix-hosted post images left: {_wix_imgs} (must be 0 before the DNS switch)")

# The production build connects only when the public key is set
import importlib.util, os
cfg = json.loads((ROOT / "config.json").read_text())
check(cfg.get("getwec_endpoint", "").startswith("https://") and cfg["getwec_endpoint"].endswith("/functions/v1/mia"),
      "GetWec endpoint configured (mia Edge Function)")

print("\n".join(notes + fails))
print(f"\n{len(notes) - 1} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
