#!/usr/bin/env python3
"""Build the static weintervisa.com site into ./site (GitHub Pages ready).

Content:  content/posts/<slug>.md  (meta JSON in an HTML comment + Markdown body)
Output:   site/  — keep Wix URLs exactly: /post/<slug> is site/post/<slug>.html
          (GitHub Pages serves /post/<slug> from post/<slug>.html, no trailing slash,
          so every old Wix link keeps working).

PREVIEW = True adds noindex + robots Disallow until the owner approves the DNS switch.
No cookies, analytics or trackers (privacy policy must be updated first).
"""
import html, json, re, shutil, sys
from datetime import datetime
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).parent
OUT = ROOT / "site"
SITE = "https://www.weintervisa.com"
PREVIEW = "--production" not in sys.argv
COMPANY = "We International Education &amp; Visa Pty Ltd"
CONFIG = json.loads((ROOT / "config.json").read_text())

NAV = [  # (label, path) — Games removed from the menu (now weintergames.com)
    ("Courses", "/courses"),
    ("Fast-track", "/fast-track-courses"),
    ("Student services", "/student-services"),
    ("Blog", "/blog"),
    ("Contact", "/contact-us"),
]


def esc(s):
    return html.escape(s or "", quote=True)


def load_posts():
    posts = []
    for f in sorted((ROOT / "content/posts").glob("*.md")):
        raw = f.read_text()
        m = re.match(r"<!--meta\n(.*?)\nmeta-->\n", raw, re.S)
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():]
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def internalise(md):
    # Links to our own domain become site-relative so they work on the preview host too.
    return re.sub(r"\]\(https?://(?:www\.)?weintervisa\.com(/[^)]*)?\)",
                  lambda m: "](" + (m.group(1) or "/") + ")", md)


def youtube(md):
    def rep(m):
        vid = m.group(1)
        return (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" '
                f'title="Video" loading="lazy" allowfullscreen '
                f'allow="accelerometer; encrypted-media; picture-in-picture"></iframe></div>')
    return re.sub(r"\{\{youtube ([\w-]{6,20})\}\}", rep, md)


def render_md(md):
    out = markdown.markdown(youtube(internalise(md)), extensions=["tables", "sane_lists"])
    # External links open in a new tab, safely.
    return re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)


def lang_links(path, lang):
    """hreflang alternates + the header language switch (owner 20 Nov 2026: English + Thai on every page)."""
    import thai_pages as tp
    en = tp.EN_OF.get(path, path) if lang == "th" else path
    th = tp.TH_OF.get(en)
    head = ""
    if th:
        head = (f'<link rel="alternate" hreflang="en" href="{SITE}{"" if en == "/" else en}">'
                f'<link rel="alternate" hreflang="th" href="{SITE}{th}">'
                f'<link rel="alternate" hreflang="x-default" href="{SITE}{"" if en == "/" else en}">')
    if lang == "th":
        switch = f'<a class="lang" href="{en}" hreflang="en" lang="en">English</a>'
    else:  # no Thai version yet → Thai home
        switch = f'<a class="lang" href="{th or "/th/"}" hreflang="th" lang="th">ไทย</a>'
    return head, switch


def page(title, body, *, path, description="", og_image="", jsonld=None, extra_head="", lang="en"):
    if 'data-lead-form' in body:  # lead forms → GetWec; connected only in production with the public key
        if not PREVIEW and CONFIG.get("getwec_endpoint") and CONFIG.get("getwec_anon_key"):
            extra_head += (f'<meta name="getwec-endpoint" content="{esc(CONFIG["getwec_endpoint"])}">'
                           f'<meta name="getwec-key" content="{esc(CONFIG["getwec_anon_key"])}">')
        body += '<script src="/assets/forms.js" defer></script>'

    import thai_pages as tp
    canonical = SITE + ("" if path == "/" else path)
    robots = '<meta name="robots" content="noindex, nofollow">' if PREVIEW else ""
    nav_items = tp.NAV_TH if lang == "th" else NAV
    nav = "".join(f'<a href="{p}"{" aria-current=page" if path.startswith(p) else ""}>{l}</a>' for l, p in nav_items)
    alt_head, switch = lang_links(path, lang)
    extra_head = alt_head + extra_head
    th = lang == "th"
    home_href = "/th/" if th else "/"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    og = f'<meta property="og:image" content="{esc(og_image)}">' if og_image else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
{og}
<link rel="alternate" type="application/rss+xml" title="We International blog" href="/blog-feed.xml">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
{ld}{extra_head}
</head>
<body>
<a class="skip" href="#main">{"ข้ามไปที่เนื้อหา" if th else "Skip to content"}</a>
<header class="top">
  <a class="brand" href="{home_href}">We International</a>
  {switch}
  <details class="menu"><summary aria-label="{"เมนู" if th else "Menu"}">{"เมนู" if th else "Menu"}</summary><nav>{nav}</nav></details>
  <nav class="wide">{nav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <p><strong>{COMPANY}</strong>{(" · ABN " + esc(CONFIG["abn"])) if CONFIG.get("abn") else ""} · QEAC {esc(CONFIG["qeac"])}</p>
  <p>{tp.FOOT_TH if th else "We help with study and courses in Australia. We are not a migration agent: for visa advice we refer you to a registered migration agent."}</p>
  <p><a href="{"/th/contact-us" if th else "/contact-us"}">{"ติดต่อเรา" if th else "Contact"}</a> · <a href="{"/th/privacy-policy" if th else "/privacy-policy"}">{"ความเป็นส่วนตัว" if th else "Privacy"}</a> · <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></p>
</footer>
</body>
</html>
"""


def fmt_date(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%-d %b %Y")


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "post").mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    posts = load_posts()
    urls_extra = []
    def write(rel, s):
        (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
        (OUT / rel).write_text(s)

    # Posts — exact Wix path /post/<slug>
    for p in posts:
        cover = f'<img class="cover" src="{esc(p["cover"])}" alt="" loading="eager">' if p.get("cover") else ""
        body = f"""<article class="post">
<p class="meta"><a href="/blog">Blog</a> · {fmt_date(p["date"])} · {p.get("minutesToRead") or 2} min read</p>
<h1>{esc(p["title"])}</h1>
{cover}
<div class="prose">{render_md(p["body"])}</div>
<aside class="cta"><p>Questions about studying in Australia?</p><a class="btn" href="/contact-us">Talk to our team</a></aside>
</article>"""
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
              "datePublished": p["date"], "dateModified": p.get("updated") or p["date"],
              "image": p.get("cover") or None, "mainEntityOfPage": f"{SITE}/post/{p['slug']}",
              "publisher": {"@type": "Organization", "name": html.unescape(COMPANY)}}
        write(f"post/{p['slug']}.html", page(p.get("seoTitle") or p["title"], body, path=f"/post/{p['slug']}",
              description=p.get("seoDescription") or p.get("excerpt"), og_image=p.get("cover", ""), jsonld=ld))

    # Blog index
    cards = "".join(f"""<li class="card"><a href="/post/{p['slug']}">
{f'<img src="{esc(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else '<div class="noimg"></div>'}
<span class="date">{fmt_date(p["date"])}</span><strong>{esc(p["title"])}</strong>
<span class="ex">{esc(p.get("excerpt"))}</span></a></li>""" for p in posts)
    write("blog.html", page("Blog | We International", f'<section class="wrap"><h1>Blog</h1>'
          f'<p class="lead">Plain-English guides on courses, working holidays and life in Australia.</p>'
          f'<ul class="cards">{cards}</ul></section>', path="/blog",
          description="Guides on courses, working holidays and student life in Australia."))

    # Home — from the CMS home draft (content/home.json), see home_page.py
    import home_page
    write("index.html", page(home_page.HOME["seoTitle"], home_page.render(posts, fmt_date), path="/",
          description=home_page.HOME["seoDescription"],
          jsonld=home_page.jsonld(SITE, html.unescape(COMPANY), posts)))

    # Redirects (static: meta refresh + canonical). /welcome was the Wix home; /games moved.
    redirects = {"welcome": "/", "games": "https://weintergames.com/",
                 # dead link already on the live Wix blog (post no longer exists) → blog index
                 "post/what-s-on-in-october-2026-sydney-melbourne-events": "/blog"}
    for rel, target in redirects.items():
        write(f"{rel}.html", f'<!doctype html><meta charset="utf-8"><title>Moved</title>'
              f'<link rel="canonical" href="{target}"><meta name="robots" content="noindex">'
              f'<meta http-equiv="refresh" content="0; url={target}"><a href="{target}">{target}</a>')

    import pages, content_pages
    for rel, (title, desc, body) in {**pages.PAGES, **content_pages.CONTENT_PAGES}.items():
        write(f"{rel}.html", page(title, body, path="/" + rel, description=desc, jsonld=content_pages.JSONLD.get(rel)))
        urls_extra.append("/" + rel)

    # Thai pages (/th/...) — see thai_pages.py
    import thai_pages
    write("th/index.html", page(thai_pages.HOME_TITLE, thai_pages.home(posts, fmt_date), path="/th/",
          description=thai_pages.HOME_DESC, lang="th"))
    urls_extra.append("/th/")
    import thai_more
    write("th/blog.html", page(thai_more.BLOG_TITLE, thai_more.blog_body(posts, fmt_date), path="/th/blog",
          description=thai_more.BLOG_DESC, lang="th"))
    urls_extra.append("/th/blog")
    for rel, (title, desc, body) in thai_pages.TH_PAGES.items():
        write(f"{rel}.html", page(title, body, path="/" + rel, description=desc, lang="th", jsonld=thai_pages.JSONLD.get(rel)))
        urls_extra.append("/" + rel)

    write("404.html", page("Page not found | We International", '<section class="wrap"><h1>Page not found</h1>'
          '<p>This page has moved or no longer exists.</p><p><a class="btn" href="/">Home</a> '
          '<a class="btn ghost" href="/blog">Blog</a></p></section>', path="/404"))

    # Same feed path as Wix (/blog-feed.xml) so existing subscribers keep working.
    items = "".join(f"""<item><title>{esc(p['title'])}</title><link>{SITE}/post/{p['slug']}</link>
<guid>{SITE}/post/{p['slug']}</guid><pubDate>{datetime.fromisoformat(p['date'].replace('Z', '+00:00')).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
<description>{esc(p.get('excerpt'))}</description></item>""" for p in posts)
    write("blog-feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
          f'<title>We International blog</title><link>{SITE}/blog</link>'
          f'<description>Guides on study and life in Australia</description>{items}</channel></rss>')

    urls = ["/", "/blog"] + urls_extra + [f"/post/{p['slug']}" for p in posts]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{SITE}{'' if u == '/' else u}</loc></url>" for u in urls) + "</urlset>")
    write("robots.txt", "User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    if CONFIG.get("cname") and not PREVIEW:
        write("CNAME", CONFIG["cname"] + "\n")
    write(".nojekyll", "")
    print(f"built {len(posts)} posts → {OUT} ({'preview/noindex' if PREVIEW else 'production'})")


def apply_base_path():
    """Preview host is a project page (we-international.github.io/weintervisa-site/), so
    root-relative links like /assets/site.css need the repo path in front. Set SITE_BASE
    (e.g. /weintervisa-site) only for that preview deploy; local tests and the production
    build (custom domain at the root) leave it empty and nothing changes."""
    import os
    base = os.environ.get("SITE_BASE", "").rstrip("/")
    if not base or not PREVIEW:
        return
    pat = re.compile(r'((?:href|src|action)=["\'])/(?!/)')
    for f in OUT.rglob("*"):
        if f.suffix in (".html", ".js", ".css") and f.is_file():
            t = f.read_text()
            t2 = pat.sub(lambda m: m.group(1) + base + "/", t)
            if f.suffix in (".js", ".css"):
                t2 = re.sub(r'url\(\s*(["\']?)/(?!/)', lambda m: "url(" + m.group(1) + base + "/", t2)
            if t2 != t:
                f.write_text(t2)
    print(f"preview base path {base} applied")


if __name__ == "__main__":
    build()
    apply_base_path()
