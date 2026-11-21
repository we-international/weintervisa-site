"""/about-we-international and /referral-partners — rebuilt on 22 Nov 2026 from the LIVE Wix pages
(content/about.json, content/referral-partners.json). QEAC shows the number only; no personal names;
no outcome or reply-time promises; partner applications by email until the form opens (no student data).
"""
import html
import json
from pathlib import Path
from urllib.parse import quote

from home_page import img

ROOT = Path(__file__).resolve().parent
e = html.escape
AB = json.loads((ROOT / "content/about.json").read_text())
RP = json.loads((ROOT / "content/referral-partners.json").read_text())
OUT = ' target="_blank" rel="noopener"'
MIG_FORM = "https://getwec.pages.dev/partners/migration/"


def link(u):
    return f' href="{e(u)}"' + (OUT if u.startswith("http") else "")


def about():
    d = AB
    values = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in d["values"])
    princ = "".join(f'<li class="path"><h3>{e(t)}</h3><p>{e(b)}</p></li>' for t, b in d["principles"])
    story = "".join(f"<p>{e(p)}</p>" for p in d["story"])
    facts = "".join(f'<li><strong>{f"<a{link(u)}>{e(t)}</a>" if u else e(t)}</strong><span>{e(b)}</span></li>' for t, b, u in d["facts"])
    how = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in d["how"])
    nots = "".join(f"<li>{e(x)}</li>" for x in d["not"])
    social = " · ".join(f'<a href="{e(u)}"{OUT}>{e(n)}</a>' for n, u in d["social"])
    pic = img(d["image"], "hero-img", lazy=False, w=1536, h=1024)
    return f"""<section class="hero home-hero"><div class="wrap{' hero-grid' if pic else ''}"><div>
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<ul class="why">{values}</ul>
</div>{f'<div class="hero-side">{pic}</div>' if pic else ''}</div></section>
<section class="wrap">
<p class="kicker">What guides us</p>
<h2>Student first, every time</h2>
<ul class="paths">{princ}</ul>
</section>
<section class="wrap narrow">
<p class="kicker">{e(d["storyKicker"])}</p>
<h2>{e(d["storyH2"])}</h2>
{story}
<ul class="why">{facts}</ul>
</section>
<section class="wrap">
<p class="kicker">How we work</p>
<h2>From first message to first class</h2>
<ol class="flow">{how}</ol>
</section>
<section class="wrap narrow">
<h2>What we don't do</h2>
<ul class="list">{nots}</ul>
<h2>People and AI</h2>
<p>{e(d["people"])}</p>
<p>Follow us: {social}</p>
<p class="small">{e(d["disclaimer"])}</p>
<aside class="cta"><p>Your next step starts with a conversation.</p><span class="small">Tell us what you want to study. We'll help you understand the options.</span><br>
<a class="btn" href="/contact-us">Talk to our team</a> <a class="btn ghost" href="/courses">Explore courses</a></aside>
</section>"""


def partners():
    d = RP
    role = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in d["role"])
    sup = "".join(f'<li class="path"><span class="small">{e(k)}</span><h3>{e(t)}</h3><p>{e(b)}</p></li>' for k, t, b in d["support"])
    fields = "".join(f"<li>{e(x)}</li>" for x in d["fields"])
    careful = "".join(f"<p>{e(x)}</p>" for x in d["careful"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    prov = "".join(f'<li class="path"><h3>{e(t)}</h3><p>{e(b)}</p>'
                   + (f'<a href="{MIG_FORM}"{OUT}>List your practice for free ↗</a>' if "migration" in t
                      else f'<a href="mailto:info@weintervisa.com?subject={quote("Partnership enquiry | " + t)}">Email us →</a>')
                   + "</li>" for t, b in d["providers"])
    body = quote("Hello We International team,\n\nI would like to apply to become a referral partner.\n\n"
                 "Full name:\nEmail:\nPhone (optional):\nCountry / region:\nMy background and student connections:\n\n"
                 "(No student personal information in this email.)")
    apply = f"mailto:info@weintervisa.com?subject={quote('Referral partner application')}&amp;body={body}"
    return f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<p class="actions"><a class="btn" href="#apply">Apply now →</a> <a class="btn ghost" href="/partner-portal">Already a partner? Log in →</a></p>
<p class="small">{e(d["small"])}</p>
</div></section>
<section class="wrap">
<p class="kicker">How it works</p>
<h2>Your role, made simpler</h2>
<ol class="flow flow3">{role}</ol>
</section>
<section class="wrap">
<p class="kicker">What you get</p>
<h2>Support you can work with</h2>
<ul class="paths">{sup}</ul>
</section>
<section class="wrap narrow" id="apply">
<p class="kicker">Tell us a little about yourself</p>
<h2>Let's start with a conversation</h2>
<p>{e(d["applyIntro"])}</p>
<ul class="list">{fields}</ul>
<p><a class="btn" href="{apply}">Email my partner application</a></p>
<p class="small">This opens your email app; nothing is sent until you press send. {e(d["applyWarn"])}</p>
</section>
<section class="wrap narrow">
<p class="kicker">A partnership built carefully</p>
<h2>Start small. Build trust together.</h2>
{careful}
<h2>Common questions</h2>
{faq}
</section>
<section class="wrap">
<p class="kicker">Schools and service providers</p>
<h2>Other ways to work with us</h2>
<ul class="paths">{prov}</ul>
<p class="note-box"><strong>Visa questions?</strong> We are an education agency, not a migration agent. For advice about a visa,
we refer students to a registered migration agent. No visa outcome is guaranteed.</p>
</section>"""
