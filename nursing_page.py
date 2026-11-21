"""/courses/nursing-pathways-australia — rebuilt on 22 Nov 2026 from the LIVE Wix page (content/nursing.json,
from the compare run's saved text + markup). Rules: Ahpra/NMBA decide registration, a course is not
registration or a visa pathway, no outcome promises, visa questions → registered migration agent,
no tracking, no script, images only from local copies in assets/img.
"""
import html
import json
from pathlib import Path
from urllib.parse import quote

from home_page import img

ROOT = Path(__file__).resolve().parent
e = html.escape
NU = json.loads((ROOT / "content/nursing.json").read_text())


# Fixed page words; a Thai copy (content/th/nursing.json "ui") overrides them key by key.
UI_EN = {
    "subject": "Nursing pathways enquiry | {}",
    "mailBody": ("Hello We International team,\n\nI would like information about nursing preparation or study.\n\n"
                 "Country where I qualified:\nWhere I am now:\nStage Ahpra has advised (if known):\n"
                 "Course interest: {}\n\nThank you"),
    "feesLink": "Email us for fees and next dates", "notSure": "Not sure yet", "study": "Nursing study",
    "crumb": "Explore courses", "crumbHere": "Nursing pathways", "findStart": "Find my starting point", "askCourses": "Ask about courses",
    "startK": "Start with your situation", "startH": "Where are you on your nursing journey?",
    "mapK": "The registration map", "mapH": "Check your pathway before you book a course", "goodB": "Good to know.",
    "prepK": "Course options · Charter Australia", "prepH": "Prepare for the step that comes next",
    "studyH": "Starting or continuing nursing study?", "studyBtn": "Ask about nursing study",
    "askK": "Ask our team", "askH": "Let's make your next step clearer",
    "askP": ('Pick your course interest below. It opens your email app with a short enquiry ready to fill in; nothing is sent until you press send.\n'
             'No course booking or payment is made on this page. Prefer a form? Use our <a href="/contact-us">contact page</a>.'),
    "tellB": "What to tell us in your first message", "faqH": "Good questions, clear answers", "sources": "Official sources:",
    "visa": ('<strong>Visa questions?</strong> We are an education agency, not a migration agent. For advice about your visa,\n'
             'we refer you to a registered migration agent. No visa outcome is guaranteed.'),
    "ctaP": "Not sure where to start? Tell us your stage and we check the options with you.", "ctaSend": "Send a message",
    "contact": "/contact-us", "courses": "/courses",
}


def mail(interest, L=UI_EN):
    subject = quote(L["subject"].format(interest))
    body = quote(L["mailBody"].format(interest))
    return f"mailto:info@weintervisa.com?subject={subject}&amp;body={body}"


def render(d=None):
    d = d or NU
    L = {**UI_EN, **d.get("ui", {})}
    out = ' target="_blank" rel="noopener"'
    stages = "".join(f'<li class="path"><span class="ico" aria-hidden="true">{n}</span><h3>{e(t)}</h3><p>{e(b)}</p>'
                     f'<a href="{h}">{e(l)} →</a></li>' for n, t, b, l, h in d["stages"])
    road = "".join(f'<li><strong>{e(t)}</strong><span>{e(b)} <a href="{e(u)}"{out}>{e(l)} ↗</a></span></li>'
                   for t, b, l, u in d["map"])
    prep = "".join(f'<li class="path"><span class="small">{e(k)}</span><h3>{e(t)}</h3><p>{e(b)}</p>'
                   f'<a href="{mail(i, L)}">{e(L["feesLink"])} →</a></li>' for k, t, b, i in d["prep"])
    interests = [L["notSure"]] + [p[3] for p in d["prep"]] + [L["study"]]
    mails = "".join(f'<li><a href="{mail(i, L)}">{e(i)}</a></li>' for i in interests)
    check = "".join(f"<li>{e(x)}</li>" for x in d["checklist"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    links = " · ".join(f'<a href="{e(u)}"{out}>{e(t)} ↗</a>' for t, u in d["links"])
    hero = img(d["heroImage"], "hero-img", lazy=False, w=1536, h=1024)
    return f"""<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="small"><a href="{L["courses"]}">{e(L["crumb"])}</a> / {e(L["crumbHere"])}</p>
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<p class="actions"><a class="btn" href="#start">{e(L["findStart"])} ↓</a> <a class="btn ghost" href="#enquire">{e(L["askCourses"])}</a></p>
</div><div class="hero-side">{hero}{f'<p class="small">{e(d["heroNote"])}</p>' if hero else ""}</div></div></section>
<section class="wrap" id="start">
<p class="kicker">{e(L["startK"])}</p>
<h2>{e(L["startH"])}</h2>
<ul class="paths">{stages}</ul>
</section>
<section class="wrap" id="pathway">
<p class="kicker">{e(L["mapK"])}</p>
<h2>{e(L["mapH"])}</h2>
<p>{e(d["mapIntro"])}</p>
<ol class="flow">{road}</ol>
<p class="note-box"><strong>{e(L["goodB"])}</strong> {e(d["mapWarn"])}</p>
</section>
<section class="wrap" id="prep">
<p class="kicker">{e(L["prepK"])}</p>
<h2>{e(L["prepH"])}</h2>
<p>{e(d["prepIntro"])}</p>
<ul class="paths">{prep}</ul>
<p class="small">{e(d["prepNote"])}</p>
</section>
<section class="wrap narrow" id="study">
{img(d["studyImage"], "hero-img", w=1536, h=1024)}
<h2>{e(L["studyH"])}</h2>
<p>{e(d["study"])}</p>
<p class="note-box">{e(d["studyWarn"])}</p>
<p><a class="btn" href="#enquire">{e(L["studyBtn"])} →</a></p>
</section>
<section class="wrap narrow" id="enquire">
<p class="kicker">{e(L["askK"])}</p>
<h2>{e(L["askH"])}</h2>
<p>{L["askP"]}</p>
<ul class="list">{mails}</ul>
<p><strong>{e(L["tellB"])}</strong></p>
<ul class="list">{check}</ul>
<p class="small">{e(d["privacyNote"])}</p>
</section>
<section class="wrap narrow">
<h2>{e(L["faqH"])}</h2>
{faq}
<p class="small">{e(L["sources"])} {links}</p>
<p class="note-box">{L["visa"]}</p>
<p class="small">{e(d["reviewed"])}</p>
<p class="small">{e(d["disclaimer"])}</p>
<aside class="cta"><p>{e(L["ctaP"])}</p>
<a class="btn" href="{L["contact"]}">{e(L["ctaSend"])}</a> <a class="btn ghost" href="{L["courses"]}">{e(L["crumb"])}</a></aside>
</section>"""
