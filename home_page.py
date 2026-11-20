"""Home page (/) of the new weintervisa.com.

Source: the company's home draft in the Wix CMS collection "WEIWebsitePages" (slug "home",
read-only export 20 Nov 2026 → content/home.json) + the study areas in content/study-areas.json.
Rules: no promised prices, reply times, places, visas or jobs; visa questions go to a registered
migration agent; no partner is named until the agreement is verified.
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


def render(posts, fmt_date):
    h = HOME
    groups = {}
    for a in AREAS:
        groups.setdefault(a["group"], []).append(a)
    chips = "".join(f'<li><a href="/courses#{e(group_anchor(g))}">{e(g)} <span>{len(items)}</span></a></li>'
                    for g, items in groups.items())
    why = "".join(f'<li><strong>{e(s["heading"])}</strong><span>{e(s["body"])}</span></li>' for s in h["sections"][:3])
    paths = [
        ("/courses", "Courses", "English, care, business, trades, IT and more."),
        ("/fast-track-courses", "Fast-track for working holiday makers", "Short study plans that fit a 417 or 462 visa. Check the rules first."),
        ("/courses/nursing-pathways-australia", "Nursing pathways", "The main steps for nurses trained outside Australia."),
        ("/english-practice", "English study", "Build English for study, work and daily life."),
        ("/student-services", "Student services", "Homestay, health cover and help while you study."),
        ("/referral-partners", "Referral partners", "Work with us to refer students."),
    ]
    tiles = "".join(f'<a class="tile" href="{p}"><strong>{e(t)}</strong><span>{e(d)}</span></a>' for p, t, d in paths)
    cards = "".join(f"""<li class="card"><a href="/post/{p['slug']}">
{f'<img src="{e(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else '<div class="noimg"></div>'}
<span class="date">{fmt_date(p["date"])}</span><strong>{e(p["title"])}</strong></a></li>""" for p in posts[:3])
    return f"""<section class="hero"><div class="wrap">
<p class="kicker">{e(h["title"])}</p>
<h1>{e(h["heading"])}</h1>
<p class="lead">{e(h["intro"])}</p>
<p class="actions"><a class="btn" href="/{e(h["ctaTarget"])}">{e(h["cta"])}</a> <a class="btn ghost" href="/contact-us">Ask us a question</a></p>
</div></section>
<section class="wrap">
<h2>Start with a study area</h2>
<p>Pick a group to see the study areas in it. We check the current course details with the school before we share them.</p>
<ul class="chips">{chips}</ul>
</section>
<section class="wrap">
<h2>How we help</h2>
<ul class="why">{why}</ul>
</section>
<section class="wrap">
<h2>{e(h["sections"][3]["heading"])}</h2>
<ol class="flow">
<li><strong>Explore</strong><span>Look at a study area that interests you.</span></li>
<li><strong>Ask</strong><span>Send us a message about current options.</span></li>
<li><strong>Compare</strong><span>See the course, fees, campus and start date side by side.</span></li>
<li><strong>Decide</strong><span>Go ahead only when you are ready. It is your choice.</span></li>
</ol>
</section>
<section class="wrap">
<h2>Popular pages</h2>
<div class="grid3">{tiles}</div>
<p class="note-box"><strong>Visa questions?</strong> We are an education agency, not a migration agent.
For advice about your visa, we refer you to a registered migration agent. No visa outcome is guaranteed.</p>
</section>
<section class="wrap">
<h2>Latest from the blog</h2>
<ul class="cards">{cards}</ul>
<p><a href="/blog">All {len(posts)} posts</a></p>
<aside class="cta"><p>{e(h["sections"][2]["body"])}</p><a class="btn" href="/contact-us">Send a message</a></aside>
</section>"""


def jsonld(site, company, posts):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": site + "/#org", "name": company, "url": site, "email": "info@weintervisa.com"},
        {"@type": "WebSite", "@id": site + "/#site", "url": site, "name": "We International", "publisher": {"@id": site + "/#org"}},
    ]}
