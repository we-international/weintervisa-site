#!/usr/bin/env python3
"""List every URL the live Wix site publishes in its sitemap and check the new build has it.

Run where www.weintervisa.com is reachable (the CI runner; the cloud team's sandbox is blocked):
    python3 build.py && python3 tools/live_urls.py [--write tests/wix-live-urls.json]

Read-only: only GETs the public sitemap files. Prints a Markdown report (for the job summary)
and exits 0; the offline test (tests/test_site.py) enforces the committed snapshot.
"""
import json, pathlib, re, sys, urllib.request
from urllib.parse import urlparse

LIVE = "https://www.weintervisa.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


def get(url):
    req = urllib.request.Request(url, headers={"user-agent": "weintervisa-site-check/1.0 (read-only)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def sitemap_paths(url, seen=None):
    seen = seen if seen is not None else set()
    if url in seen:
        return {}
    seen.add(url)
    xml = get(url)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    out = {}
    if "<sitemapindex" in xml:
        for loc in locs:
            for p, src in sitemap_paths(loc.replace("&amp;", "&"), seen).items():
                out.setdefault(p, src)
    else:
        name = urlparse(url).path.rsplit("/", 1)[-1]
        for loc in locs:
            p = urlparse(loc.replace("&amp;", "&")).path.rstrip("/") or "/"
            out.setdefault(p, name)
    return out


def built(path):
    """True when the new site serves this path (page or redirect), like GitHub Pages does."""
    if path == "/":
        return (SITE / "index.html").exists()
    rel = path.lstrip("/")
    return (SITE / f"{rel}.html").exists() or (SITE / rel / "index.html").exists()


def main():
    found = sitemap_paths(LIVE + "/sitemap.xml")
    rows = sorted(found.items())
    missing = [p for p, _ in rows if not built(p)]
    print(f"## Live Wix sitemap vs new build\n\nLive URLs: **{len(rows)}** · in the new build: **{len(rows) - len(missing)}** · missing: **{len(missing)}**\n")
    if missing:
        print("| Missing path | Wix sitemap |\n|---|---|")
        for p in missing:
            print(f"| `{p}` | {found[p]} |")
    if "--write" in sys.argv:
        out = ROOT / sys.argv[sys.argv.index("--write") + 1]
        out.write_text(json.dumps({"_note": "Paths in the live Wix sitemap (read by CI, tools/live_urls.py). "
                                   "Every one must be a page or a redirect in the new site.",
                                   "paths": [{"path": p, "sitemap": s} for p, s in rows]}, indent=1) + "\n")


if __name__ == "__main__":
    main()
