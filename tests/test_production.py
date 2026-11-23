#!/usr/bin/env python3
"""Go-live dry run — run: python3 tests/test_production.py  (exit 1 on any failure).

Builds the site exactly as it will be served on www.weintervisa.com after the owner
switches DNS (`build.py --production`, no preview base path) and checks what changes
on that day: crawlers allowed, canonical / hreflang / sitemap on the real domain,
CNAME, owner-approved schools only, lead forms connect only with the public key, and
every live Wix URL still answers. Rebuilds the normal preview build at the end so the
other tests and local previews are not affected.
"""
import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOMAIN = "https://www.weintervisa.com"
fails, notes = [], []


def check(ok, msg):
    (notes if ok else fails).append(("✓ " if ok else "✗ ") + msg)


def build(*args, base=""):
    env = {k: v for k, v in os.environ.items() if k != "SITE_BASE"}
    if base:
        env["SITE_BASE"] = base
    subprocess.run([sys.executable, str(ROOT / "build.py"), *args], check=True, env=env)


try:
    build("--production", base="/weintervisa-site")  # a preview base path must be ignored in production
    pages = {p.relative_to(SITE).as_posix(): p.read_text() for p in SITE.rglob("*.html")}
    redirect = {k for k, s in pages.items() if 'http-equiv="refresh"' in s}
    real = {k: s for k, s in pages.items() if k not in redirect and k != "404.html"}
    cfg = json.loads((ROOT / "config.json").read_text())
    check(not (SITE / "redesign").exists(), "redesign mockups are not in the production build (preview only)")

    # 1. Indexable on the real domain
    robots = (SITE / "robots.txt").read_text()
    check("Allow: /" in robots and "Disallow" not in robots and f"Sitemap: {DOMAIN}/sitemap.xml" in robots,
          "robots.txt allows crawlers and names the sitemap")
    noindex = sorted(k for k, s in real.items() if 'content="noindex' in s)
    check(not noindex, f"no real page is noindex ({len(real)} pages)" + (f" — {noindex[:5]}" if noindex else ""))
    check(all('content="noindex' in pages[k] for k in redirect), f"redirect pages stay noindex ({len(redirect)})")

    # 2. Canonical, og:url and hreflang point at www.weintervisa.com, never the preview host
    def url_for(rel):
        rel = rel[:-5] if rel.endswith(".html") else rel
        rel = "" if rel == "index" else rel
        rel = rel[:-6] if rel.endswith("/index") else rel
        return DOMAIN + ("/" + rel if rel else "") + ("/" if rel == "th" else "")
    bad_canon = [k for k, s in real.items()
                 if f'<link rel="canonical" href="{url_for(k)}">' not in s]
    check(not bad_canon, "every page's canonical is its own www.weintervisa.com URL"
          + (f" — {bad_canon[:5]}" if bad_canon else ""))
    alt = set(u for s in real.values() for u in re.findall(r'hreflang="[a-z-]+" href="([^"]+)"', s))
    check(alt and all(u.startswith(DOMAIN) for u in alt), f"hreflang links use the real domain ({len(alt)})")
    leaks = sorted(k for k, s in pages.items() if re.search(r"weintervisa-site|github\.io", s))
    check(not leaks, "no preview host or /weintervisa-site path in any page" + (f" — {leaks[:5]}" if leaks else ""))
    assets = [p for p in SITE.rglob("*") if p.suffix in (".css", ".js")]
    check(not any("/weintervisa-site" in p.read_text() for p in assets), "CSS/JS have no preview base path")

    # 3. Sitemap: absolute URLs on the real domain, each one a real page
    locs = re.findall(r"<loc>([^<]+)</loc>", (SITE / "sitemap.xml").read_text())
    def served(u):
        rel = u[len(DOMAIN):].strip("/")
        return not rel or (SITE / f"{rel}.html").exists() or (SITE / rel / "index.html").exists()
    gone = [u for u in locs if not u.startswith(DOMAIN + "/") and u != DOMAIN or not served(u)]
    check(locs and not gone, f"sitemap: {len(locs)} URLs, all on {DOMAIN} and all built" + (f" — {gone[:5]}" if gone else ""))
    check(DOMAIN + "/post/" in (SITE / "blog-feed.xml").read_text(), "blog feed links use the real domain")

    # 4. Custom domain file (GitHub Pages) matches config
    check((SITE / "CNAME").read_text().strip() == cfg["cname"] == "www.weintervisa.com", "CNAME = www.weintervisa.com")

    # 5. Every URL in the live Wix sitemap still answers (page or redirect)
    live = [x["path"] for x in json.loads((ROOT / "tests/wix-live-urls.json").read_text())["paths"]]
    miss = [p for p in live if not served(DOMAIN + p)]
    check(not miss, f"all {len(live)} live Wix URLs answer on the production build" + (f" — {miss}" if miss else ""))
    posts = json.loads((ROOT / "tests/wix-post-slugs.json").read_text())
    check(all((SITE / "post" / f"{s}.html").exists() for s in posts), f"all {len(posts)} blog posts keep /post/<slug>")

    # 6. Only owner-approved school pages go live
    schools = json.loads((ROOT / "content/schools.json").read_text())["schools"]
    def slug_built(sc):
        return (SITE / "schools" / f"{sc['slug']}.html").exists()
    check(all(slug_built(sc) == bool(sc.get("approved")) for sc in schools),
          f"school pages built = approved schools ({sum(bool(s.get('approved')) for s in schools)} of {len(schools)})")

    # 7. Lead forms: connected only when the public anon key is set (owner adds it on DNS day)
    form = pages["contact-us.html"]
    if cfg.get("getwec_anon_key"):
        check("getwec-key" in form and cfg["getwec_endpoint"] in form, "contact form connected to GetWec (key set)")
    else:
        check("getwec-key" not in form, "contact form not connected yet (anon key empty — add on DNS day)")
        notes.append("• reminder: set getwec_anon_key in config.json in the go-live PR (docs/go-live.md step 3)")
    check(cfg["getwec_endpoint"].startswith("https://") and ".supabase.co/functions/v1/mia" in cfg["getwec_endpoint"],
          "GetWec endpoint is the Sydney mia function")

    # 8. Rules still hold in production
    check(not any(re.search(r"jarinrit|gmail\.com|\bBen\b", s, re.I) for s in pages.values()), "no personal name/email")
    check(not any(re.search(r"googletagmanager|google-analytics|gtag\(|fbq\(|document\.cookie", s, re.I)
                  for s in pages.values()), "no trackers or cookies")
    check("not a migration agent" in pages["index.html"], "footer: not a migration agent")
finally:
    build()  # back to the preview build

print("\n".join(notes + fails))
print(f"\n{len(notes) - sum(n.startswith('•') for n in notes)} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
