#!/usr/bin/env python3
"""Site checks — run: python3 tests/test_site.py  (exit 1 on any failure)."""
import json, re, subprocess, sys
from pathlib import Path

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
check(emails <= {"info@weintervisa.com"}, f"only info@weintervisa.com appears (found {sorted(emails)})")

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
check((SITE / "sitemap.xml").read_text().count("<loc>") == len(slugs) + 2, "sitemap lists home, blog and every post")

print("\n".join(notes + fails))
print(f"\n{len(notes) - 1} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
