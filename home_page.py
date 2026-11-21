"""Home page (/) of the new weintervisa.com.

Source: the LIVE Wix home page (custom embed) as visitors see it on 21 Nov 2026 — text + markup
saved by the workflow "Live Wix vs new site" → content/home.json — plus the study areas in
content/study-areas.json and the latest blog posts. Rules: no promised prices, reply times,
places, visas or jobs; visa questions go to a registered migration agent; no tracking parameters;
an image is shown only when its local copy is in assets/img (never loaded from Wix).
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
e = html.escape
HOME = json.loads((ROOT / "content/home.json").read_text())
AREAS = json.loads((ROOT / "content/study-areas.json").read_text())


def group_anchor(g):  # same ids as the h2s on /courses
    return g.lower().replace(" & ", "-").replace(" ", "-")


def img(spec, cls="", lazy=True, w=None, h=None):
    """<img> for a local copy of a live-site image, or "" while the copy is not in the repo yet."""
    if not spec or not (ROOT / "assets/img" / spec["file"]).exists():
        return ""
    # inline max-width: the width/height attributes (no layout shift) must never widen the page, even before site.css loads
    size = f' width="{w}" height="{h}" style="max-width:100%;height:auto"' if w else ""
    return (f'<img src="/assets/img/{e(spec["file"])}" alt="{e(spec["alt"])}"{size}'
            f'{" loading=\"lazy\"" if lazy else ""}{f" class=\"{cls}\"" if cls else ""}>')


def ext(href):
    return ' target="_blank" rel="noopener"' if href.startswith("http") else ""


def render(posts, fmt_date):
    h = HOME
    groups = {}
    for a in AREAS:
        groups.setdefault(a["group"], []).append(a)
    chips = "".join(f'<li><a href="/courses#{e(group_anchor(g))}">{e(g)} <span>{len(items)}</span></a></li>'
                    for g, items in groups.items())
    points = "".join(f"<li><span aria-hidden=\"true\">{i}</span>{e(t)}</li>" for i, t in h["heroPoints"])
    trust = "".join(f"<li>{e(t)}</li>" for t in h["trust"])
    hero_img = img(h["heroImage"], "hero-img", lazy=False, w=1200, h=750)
    hs = h["homestay"]
    paths = "".join(f"""<li class="path"><span class="ico" aria-hidden="true">{p['icon']}</span>
<span class="tag">{e(p['tag'])}</span><h3>{e(p['title'])}</h3><p>{e(p['body'])}</p>
<a href="{e(p['href'])}">{e(p['link'])} →</a></li>""" for p in h["paths"])
    popular = "".join(f"""<li class="course">{img(c['img'], w=1536, h=1024)}<div>
<span class="code">{e(c['code'])}</span><h3>{e(c['title'])}</h3><p>{e(c['body'])}</p>
<p class="links"><a class="btn" href="/contact-us">Get fees &amp; intakes</a> <a href="{e(c['more'][1])}"{ext(c['more'][1])}>{e(c['more'][0])}</a></p>
</div></li>""" for c in h["popular"])
    dream = "".join(f"""<li class="area"><span class="ico" aria-hidden="true">{d['icon']}</span><h3>{e(d['title'])}</h3>
<p>{e(d['body'])}</p><ul class="tags">{''.join(f'<li>{e(t)}</li>' for t in d['tags'])}</ul>
<a href="/contact-us">{e(d['ask'])} →</a></li>""" for d in h["dream"])
    helpcards = "".join(f'<li><span class="ico" aria-hidden="true">{i}</span><strong>{e(t)}</strong><span>{e(b)}</span></li>' for i, t, b in h["help"])
    helpers = "".join(f'<li><span class="ico" aria-hidden="true">{i}</span><strong>{e(t)}</strong><span>{e(b)}</span></li>' for i, t, b in h["english"]["helpers"])
    q = h["english"]["quiz"]
    opts = "".join(f"<li>{e(o)}</li>" for o in q["options"])
    right = "ABC"[q["answer"]] + ". " + q["options"][q["answer"]]
    steps = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in h["steps"])
    faq = "".join(f'<details class="faq"><summary>{e(qq)}</summary><p>{a}</p></details>' for qq, a in h["faq"])
    v = h["video"]
    cards = "".join(f"""<li class="card"><a href="/post/{p['slug']}">
{f'<img src="{e(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else '<div class="noimg"></div>'}
<span class="date">{fmt_date(p["date"])}</span><strong>{e(p["title"])}</strong></a></li>""" for p in posts[:3])
    ready_img = img(h["readyImage"], "ready-img", w=900, h=563)
    return f"""<p class="topnote">🏡 New to Australia? Stay with a screened host family first — <a href="#homestay">Find a homestay →</a></p>
<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="kicker">{e(h["title"])}</p>
<h1>{e(h["heading"])}</h1>
<p class="lead">{e(h["intro"])}</p>
<ul class="points">{points}</ul>
<p class="actions"><a class="btn" href="#paths">Start here: which visa are you on? →</a> <a class="btn ghost" href="/contact-us">Talk to our team</a></p>
</div><div class="hero-side">{hero_img}
<p class="bubble"><strong>Maya:</strong> {e(h["guides"]["maya"])}</p>
<p class="bubble alt"><strong>Kenji:</strong> {e(h["guides"]["kenji"])}</p>
</div></div>
<div class="wrap trust-wrap"><ul class="trust">{trust}</ul></div></section>
<section class="wrap band" id="homestay">
<p class="kicker">{e(hs["kicker"])}</p>
<h2>{e(hs["heading"])}</h2>
<p>{e(hs["body"])}</p>
<p class="actions"><a class="btn" href="{e(hs["url"])}" target="_blank" rel="noopener">{e(hs["button"])}</a> <a class="btn ghost" href="/homestay">How homestay works</a></p>
<p class="small">{e(hs["note"])}</p>
</section>
<section class="wrap" id="paths">
<p class="kicker">Start here</p>
<h2>Which one sounds like you?</h2>
<p>Choose your situation. Each path shows what you can usually study and how we can help.</p>
<ul class="paths">{paths}</ul>
<aside class="tip"><strong>Kenji's tip</strong> Not sure what your visa allows? Check your conditions for free in
<a href="{e(h["vevo"])}" target="_blank" rel="noopener">VEVO ↗</a>. We're an education agency working with registered
migration partners, so for visa advice we can refer you to a registered migration agent.</aside>
</section>
<section class="wrap">
<p class="kicker">Popular courses</p>
<h2>Practical courses that lead somewhere</h2>
<p>Hands-on Certificate III courses with work placement, plus English and other study areas.</p>
<ul class="courses">{popular}</ul>
<p><a href="/courses">See all courses →</a></p>
</section>
<section class="wrap">
<p class="kicker">Study areas</p>
<h2>Dream bigger: degrees, trades and tech</h2>
<p>From a Bachelor's or Master's to hands-on trades and AI, tell us your goal and we'll find courses, providers and intakes that fit your visa and budget.</p>
<ul class="dream">{dream}</ul>
<h3>Browse all study areas</h3>
<ul class="chips">{chips}</ul>
<p class="small">Course availability, entry requirements and fees vary by provider. Ask us for current options.</p>
</section>
<section class="wrap">
<p class="kicker">How we help</p>
<h2>Everything for your first months, in one place</h2>
<ul class="help">{helpcards}</ul>
</section>
<section class="wrap" id="video">
<p class="kicker">Watch</p>
<h2>{e(v["title"])}</h2>
<p>{e(v["body"])}</p>
<p class="actions"><a class="btn" href="{e(v["url"])}" target="_blank" rel="noopener">▶ Watch on YouTube ↗</a>
<a href="{e(v["channel"])}" target="_blank" rel="noopener">More videos on our YouTube channel ↗</a></p>
</section>
<section class="wrap english">
<div><p class="kicker">Free English practice</p>
<h2>Want to practise your English?</h2>
<p>We have helpers to make you a little better every day. Learn the English Australians really use, one small mistake at a time.</p>
<ul class="help">{helpers}</ul>
<p><a class="btn" href="/english-practice">Start practising →</a></p></div>
<div class="quiz"><p class="kicker">Try one now</p>
<p class="wrong">Not quite: <s>{e(q["wrong"])}</s></p>
<p><strong>Which is correct?</strong></p>
<ol type="A">{opts}</ol>
<details><summary>Show the answer</summary><p><strong>✓ {e(right)}</strong></p><p class="small">{e(q["why"])}</p></details>
<p class="small">More questions, videos and games are waiting. <a href="/english-practice">Go to English practice →</a></p></div>
</section>
<section class="wrap">
<p class="kicker">How it works</p>
<h2>Three simple steps</h2>
<ol class="flow flow3">{steps}</ol>
<aside class="tip maya"><strong>Maya says</strong> {e(h["maya"])}</aside>
</section>
<section class="wrap narrow">
<h2>Common questions</h2>
{faq}
<p><a href="/frequently-asked-questions">More questions →</a></p>
</section>
<section class="wrap">
<h2>Latest from the blog</h2>
<ul class="cards">{cards}</ul>
<p><a href="/blog">All {len(posts)} posts</a></p>
</section>
<section class="wrap ready">{ready_img}<div>
<h2>Ready when you are</h2>
<p>{e(h["ready"])}</p>
<p class="actions"><a class="btn" href="/contact-us">Talk to our team</a> <a class="btn ghost" href="#paths">Choose my path</a></p>
<p class="small">QEAC-certified counsellor (PIER), QEAC No. 11964 · Based in Sydney, Australia · <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></p>
<p class="small">{e(h["characters"])}</p>
</div></section>"""


def jsonld(site, company, posts):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": site + "/#org", "name": company, "url": site, "email": "info@weintervisa.com"},
        {"@type": "WebSite", "@id": site + "/#site", "url": site, "name": "We International", "publisher": {"@id": site + "/#org"}},
    ]}
