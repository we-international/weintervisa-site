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


def mail(interest):
    subject = quote(f"Nursing pathways enquiry | {interest}")
    body = quote("Hello We International team,\n\nI would like information about nursing preparation or study.\n\n"
                 "Country where I qualified:\nWhere I am now:\nStage Ahpra has advised (if known):\n"
                 f"Course interest: {interest}\n\nThank you")
    return f"mailto:info@weintervisa.com?subject={subject}&amp;body={body}"


def render():
    d = NU
    out = ' target="_blank" rel="noopener"'
    stages = "".join(f'<li class="path"><span class="ico" aria-hidden="true">{n}</span><h3>{e(t)}</h3><p>{e(b)}</p>'
                     f'<a href="{h}">{e(l)} →</a></li>' for n, t, b, l, h in d["stages"])
    road = "".join(f'<li><strong>{e(t)}</strong><span>{e(b)} <a href="{e(u)}"{out}>{e(l)} ↗</a></span></li>'
                   for t, b, l, u in d["map"])
    prep = "".join(f'<li class="path"><span class="small">{e(k)}</span><h3>{e(t)}</h3><p>{e(b)}</p>'
                   f'<a href="{mail(i)}">Email us for fees and next dates →</a></li>' for k, t, b, i in d["prep"])
    interests = ["Not sure yet"] + [p[3] for p in d["prep"]] + ["Nursing study"]
    mails = "".join(f'<li><a href="{mail(i)}">{e(i)}</a></li>' for i in interests)
    check = "".join(f"<li>{e(x)}</li>" for x in d["checklist"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    links = " · ".join(f'<a href="{e(u)}"{out}>{e(t)} ↗</a>' for t, u in d["links"])
    hero = img(d["heroImage"], "hero-img", lazy=False, w=1536, h=1024)
    return f"""<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="small"><a href="/courses">Explore courses</a> / Nursing pathways</p>
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<p class="actions"><a class="btn" href="#start">Find my starting point ↓</a> <a class="btn ghost" href="#enquire">Ask about courses</a></p>
</div><div class="hero-side">{hero}{f'<p class="small">{e(d["heroNote"])}</p>' if hero else ""}</div></div></section>
<section class="wrap" id="start">
<p class="kicker">Start with your situation</p>
<h2>Where are you on your nursing journey?</h2>
<ul class="paths">{stages}</ul>
</section>
<section class="wrap" id="pathway">
<p class="kicker">The registration map</p>
<h2>Check your pathway before you book a course</h2>
<p>{e(d["mapIntro"])}</p>
<ol class="flow">{road}</ol>
<p class="note-box"><strong>Good to know.</strong> {e(d["mapWarn"])}</p>
</section>
<section class="wrap" id="prep">
<p class="kicker">Course options · Charter Australia</p>
<h2>Prepare for the step that comes next</h2>
<p>{e(d["prepIntro"])}</p>
<ul class="paths">{prep}</ul>
<p class="small">{e(d["prepNote"])}</p>
</section>
<section class="wrap narrow" id="study">
{img(d["studyImage"], "hero-img", w=1536, h=1024)}
<h2>Starting or continuing nursing study?</h2>
<p>{e(d["study"])}</p>
<p class="note-box">{e(d["studyWarn"])}</p>
<p><a class="btn" href="#enquire">Ask about nursing study →</a></p>
</section>
<section class="wrap narrow" id="enquire">
<p class="kicker">Ask our team</p>
<h2>Let's make your next step clearer</h2>
<p>Pick your course interest below. It opens your email app with a short enquiry ready to fill in; nothing is sent until you press send.
No course booking or payment is made on this page. Prefer a form? Use our <a href="/contact-us">contact page</a>.</p>
<ul class="list">{mails}</ul>
<p><strong>What to tell us in your first message</strong></p>
<ul class="list">{check}</ul>
<p class="small">{e(d["privacyNote"])}</p>
</section>
<section class="wrap narrow">
<h2>Good questions, clear answers</h2>
{faq}
<p class="small">Official sources: {links}</p>
<p class="note-box"><strong>Visa questions?</strong> We are an education agency, not a migration agent. For advice about your visa,
we refer you to a registered migration agent. No visa outcome is guaranteed.</p>
<p class="small">{e(d["reviewed"])}</p>
<p class="small">{e(d["disclaimer"])}</p>
<aside class="cta"><p>Not sure where to start? Tell us your stage and we check the options with you.</p>
<a class="btn" href="/contact-us">Send a message</a> <a class="btn ghost" href="/courses">Explore courses</a></aside>
</section>"""
