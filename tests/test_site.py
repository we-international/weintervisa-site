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
n_static = len(_p.PAGES) + len(_cp.CONTENT_PAGES)
check((SITE / "sitemap.xml").read_text().count("<loc>") == len(slugs) + 2 + n_static, f"sitemap lists home, blog, {n_static} static pages and every post")

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
# The production build connects only when the public key is set
import importlib.util, os
cfg = json.loads((ROOT / "config.json").read_text())
check(cfg.get("getwec_endpoint", "").startswith("https://") and cfg["getwec_endpoint"].endswith("/functions/v1/mia"),
      "GetWec endpoint configured (mia Edge Function)")

print("\n".join(notes + fails))
print(f"\n{len(notes) - 1} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
