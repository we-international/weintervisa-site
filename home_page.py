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


# Fixed page words; the Thai home (content/th/home.json "ui") overrides them key by key.
UI_EN = {
    "fees": "Get fees &amp; intakes", "topnote": "🏡 New to Australia? Stay with a screened host family first —",
    "findHs": "Find a homestay →", "startBtn": "Start here: which visa are you on?", "talk": "Talk to our team",
    "mayaN": "Maya:", "kenjiN": "Kenji:", "hsHow": "How homestay works",
    "startK": "Start here", "startH": "Which one sounds like you?",
    "startP": "Choose your situation. Each path shows what you can usually study and how we can help.",
    "tipB": "Kenji's tip", "tip": ('Not sure what your visa allows? Check your conditions for free in\n<a href="{}" target="_blank" rel="noopener">VEVO ↗</a>. '
                                  "We're an education agency working with registered\nmigration partners, so for visa advice we can refer you to a registered migration agent."),
    "popK": "Popular courses", "popH": "Practical courses that lead somewhere",
    "popP": "Hands-on Certificate III courses with work placement, plus English and other study areas.", "allCourses": "See all courses",
    "areasK": "Study areas", "areasH": "Dream bigger: degrees, trades and tech",
    "areasP": "From a Bachelor's or Master's to hands-on trades and AI, tell us your goal and we'll find courses, providers and intakes that fit your visa and budget.",
    "browse": "Browse all study areas", "areasNote": "Course availability, entry requirements and fees vary by provider. Ask us for current options.",
    "helpK": "How we help", "helpH": "Everything for your first months, in one place", "watchK": "Watch",
    "yt": "▶ Watch on YouTube", "channel": "More videos on our YouTube channel",
    "engK": "Free English practice", "engH": "Want to practise your English?",
    "engP": "We have helpers to make you a little better every day. Learn the English Australians really use, one small mistake at a time.",
    "engBtn": "Start practising", "tryK": "Try one now", "notQuite": "Not quite:", "which": "Which is correct?", "show": "Show the answer",
    "more": "More questions, videos and games are waiting.", "goEng": "Go to English practice",
    "howK": "How it works", "howH": "Three simple steps", "mayaB": "Maya says", "faqH": "Common questions", "moreQ": "More questions",
    "blogH": "Latest from the blog", "allPosts": "All {} posts", "readyH": "Ready when you are", "choose": "Choose my path",
    "qeac": "QEAC-certified counsellor (PIER), QEAC No. 11964 · Based in Sydney, Australia",
    "contact": "/contact-us", "courses": "/courses", "homestay": "/homestay", "english": "/english-practice",
    "faqPage": "/frequently-asked-questions", "blog": "/blog",
    "en": "",  # Thai home: ' lang="en"' on English course titles, quiz sentences and post titles
}


def render(posts, fmt_date, h=None, group_label=lambda g: g):
    h = h or HOME
    L = {**UI_EN, **h.get("ui", {})}
    en = L["en"]
    groups = {}
    for a in AREAS:
        groups.setdefault(a["group"], []).append(a)
    chips = "".join(f'<li><a href="{L["courses"]}#{e(group_anchor(g))}">{e(group_label(g))} <span>{len(items)}</span></a></li>'
                    for g, items in groups.items())
    points = "".join(f"<li><span aria-hidden=\"true\">{i}</span>{e(t)}</li>" for i, t in h["heroPoints"])
    trust = "".join(f"<li>{e(t)}</li>" for t in h["trust"])
    hero_img = img(h["heroImage"], "hero-img", lazy=False, w=1200, h=750)
    hs = h["homestay"]
    paths = "".join(f"""<li class="path"><span class="ico" aria-hidden="true">{p['icon']}</span>
<span class="tag">{e(p['tag'])}</span><h3>{e(p['title'])}</h3><p>{e(p['body'])}</p>
<a href="{e(p['href'])}">{e(p['link'])} →</a></li>""" for p in h["paths"])
    popular = "".join(f"""<li class="course">{img(c['img'], w=1536, h=1024)}<div>
<span class="code">{e(c['code'])}</span><h3{en}>{e(c['title'])}</h3><p>{e(c['body'])}</p>
<p class="links"><a class="btn" href="{L["contact"]}">{L["fees"]}</a> <a href="{e(c['more'][1])}"{ext(c['more'][1])}>{e(c['more'][0])}</a></p>
</div></li>""" for c in h["popular"])
    dream = "".join(f"""<li class="area"><span class="ico" aria-hidden="true">{d['icon']}</span><h3>{e(d['title'])}</h3>
<p>{e(d['body'])}</p><ul class="tags">{''.join(f'<li>{e(t)}</li>' for t in d['tags'])}</ul>
<a href="{L["contact"]}">{e(d['ask'])} →</a></li>""" for d in h["dream"])
    helpcards = "".join(f'<li><span class="ico" aria-hidden="true">{i}</span><strong>{e(t)}</strong><span>{e(b)}</span></li>' for i, t, b in h["help"])
    helpers = "".join(f'<li><span class="ico" aria-hidden="true">{i}</span><strong>{e(t)}</strong><span>{e(b)}</span></li>' for i, t, b in h["english"]["helpers"])
    q = h["english"]["quiz"]
    opts = "".join(f"<li{en}>{e(o)}</li>" for o in q["options"])
    right = "ABC"[q["answer"]] + ". " + q["options"][q["answer"]]
    steps = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in h["steps"])
    faq = "".join(f'<details class="faq"><summary>{e(qq)}</summary><p>{a}</p></details>' for qq, a in h["faq"])
    v = h["video"]
    cards = "".join(f"""<li class="card"><a href="/post/{p['slug']}">
{f'<img src="{e(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else '<div class="noimg"></div>'}
<span class="date">{fmt_date(p["date"])}</span><strong{en}>{e(p["title"])}</strong></a></li>""" for p in posts[:3])
    ready_img = img(h["readyImage"], "ready-img", w=900, h=563)
    return f"""<p class="topnote">{e(L["topnote"])} <a href="#homestay">{e(L["findHs"])}</a></p>
<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="kicker">{e(h["title"])}</p>
<h1>{e(h["heading"])}</h1>
<p class="lead">{e(h["intro"])}</p>
<ul class="points">{points}</ul>
<p class="actions"><a class="btn" href="#paths">{e(L["startBtn"])} →</a> <a class="btn ghost" href="{L["contact"]}">{e(L["talk"])}</a></p>
</div><div class="hero-side">{hero_img}
<p class="bubble"><strong>{e(L["mayaN"])}</strong> {e(h["guides"]["maya"])}</p>
<p class="bubble alt"><strong>{e(L["kenjiN"])}</strong> {e(h["guides"]["kenji"])}</p>
</div></div>
<div class="wrap trust-wrap"><ul class="trust">{trust}</ul></div></section>
<section class="wrap band" id="homestay">
<p class="kicker">{e(hs["kicker"])}</p>
<h2>{e(hs["heading"])}</h2>
<p>{e(hs["body"])}</p>
<p class="actions"><a class="btn" href="{e(hs["url"])}" target="_blank" rel="noopener">{e(hs["button"])}</a> <a class="btn ghost" href="{L["homestay"]}">{e(L["hsHow"])}</a></p>
<p class="small">{e(hs["note"])}</p>
</section>
<section class="wrap" id="paths">
<p class="kicker">{e(L["startK"])}</p>
<h2>{e(L["startH"])}</h2>
<p>{e(L["startP"])}</p>
<ul class="paths">{paths}</ul>
<div class="tip"><strong>{e(L["tipB"])}</strong> {L["tip"].format(e(h["vevo"]))}</div>
</section>
<section class="wrap">
<p class="kicker">{e(L["popK"])}</p>
<h2>{e(L["popH"])}</h2>
<p>{e(L["popP"])}</p>
<ul class="courses">{popular}</ul>
<p><a href="{L["courses"]}">{e(L["allCourses"])} →</a></p>
</section>
<section class="wrap">
<p class="kicker">{e(L["areasK"])}</p>
<h2>{e(L["areasH"])}</h2>
<p>{e(L["areasP"])}</p>
<ul class="dream">{dream}</ul>
<h3>{e(L["browse"])}</h3>
<ul class="chips">{chips}</ul>
<p class="small">{e(L["areasNote"])}</p>
</section>
<section class="wrap">
<p class="kicker">{e(L["helpK"])}</p>
<h2>{e(L["helpH"])}</h2>
<ul class="help">{helpcards}</ul>
</section>
<section class="wrap" id="video">
<p class="kicker">{e(L["watchK"])}</p>
<h2>{e(v["title"])}</h2>
<p>{e(v["body"])}</p>
<p class="actions"><a class="btn" href="{e(v["url"])}" target="_blank" rel="noopener">{e(L["yt"])} ↗</a>
<a href="{e(v["channel"])}" target="_blank" rel="noopener">{e(L["channel"])} ↗</a></p>
</section>
<section class="wrap english">
<div><p class="kicker">{e(L["engK"])}</p>
<h2>{e(L["engH"])}</h2>
<p>{e(L["engP"])}</p>
<ul class="help">{helpers}</ul>
<p><a class="btn" href="{L["english"]}">{e(L["engBtn"])} →</a></p></div>
<div class="quiz"><p class="kicker">{e(L["tryK"])}</p>
<p class="wrong">{e(L["notQuite"])} <s{en}>{e(q["wrong"])}</s></p>
<p><strong>{e(L["which"])}</strong></p>
<ol type="A">{opts}</ol>
<details><summary>{e(L["show"])}</summary><p><strong{en}>✓ {e(right)}</strong></p><p class="small">{e(q["why"])}</p></details>
<p class="small">{e(L["more"])} <a href="{L["english"]}">{e(L["goEng"])} →</a></p></div>
</section>
<section class="wrap">
<p class="kicker">{e(L["howK"])}</p>
<h2>{e(L["howH"])}</h2>
<ol class="flow flow3">{steps}</ol>
<div class="tip maya"><strong>{e(L["mayaB"])}</strong> {e(h["maya"])}</div>
</section>
<section class="wrap narrow">
<h2>{e(L["faqH"])}</h2>
{faq}
<p><a href="{L["faqPage"]}">{e(L["moreQ"])} →</a></p>
</section>
<section class="wrap">
<h2>{e(L["blogH"])}</h2>
<ul class="cards">{cards}</ul>
<p><a href="{L["blog"]}">{e(L["allPosts"].format(len(posts)))}</a></p>
</section>
<section class="wrap ready">{ready_img}<div>
<h2>{e(L["readyH"])}</h2>
<p>{e(h["ready"])}</p>
<p class="actions"><a class="btn" href="{L["contact"]}">{e(L["talk"])}</a> <a class="btn ghost" href="#paths">{e(L["choose"])}</a></p>
<p class="small">{e(L["qeac"])} · <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></p>
<p class="small">{e(h["characters"])}</p>
</div></section>"""


def jsonld(site, company, posts):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": site + "/#org", "name": company, "url": site, "email": "info@weintervisa.com"},
        {"@type": "WebSite", "@id": site + "/#site", "url": site, "name": "We International", "publisher": {"@id": site + "/#org"}},
    ]}
