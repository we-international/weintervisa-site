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


# Fixed page words; Thai copies (content/th/about.json, content/th/referral-partners.json "ui") override them key by key.
UI_EN = {
    "guideK": "What guides us", "guideH": "Student first, every time", "howK": "How we work", "howH": "From first message to first class",
    "notH": "What we don't do", "peopleH": "People and AI", "follow": "Follow us:",
    "ctaP": "Your next step starts with a conversation.", "ctaS": "Tell us what you want to study. We'll help you understand the options.",
    "talk": "Talk to our team", "explore": "Explore courses", "contact": "/contact-us", "courses": "/courses",
}
UI_RP = {
    "listFree": "List your practice for free", "emailUs": "Email us", "mailSubject": "Partnership enquiry | {}",
    "applySubject": "Referral partner application",
    "applyBody": ("Hello We International team,\n\nI would like to apply to become a referral partner.\n\n"
                  "Full name:\nEmail:\nPhone (optional):\nCountry / region:\nMy background and student connections:\n\n"
                  "(No student personal information in this email.)"),
    "applyNow": "Apply now", "login": "Already a partner? Log in", "howK": "How it works", "howH": "Your role, made simpler",
    "getK": "What you get", "getH": "Support you can work with", "applyK": "Tell us a little about yourself",
    "applyH": "Let's start with a conversation", "applyBtn": "Email my partner application",
    "applyNote": "This opens your email app; nothing is sent until you press send.",
    "carefulK": "A partnership built carefully", "carefulH": "Start small. Build trust together.", "faqH": "Common questions",
    "provK": "Schools and service providers", "provH": "Other ways to work with us",
    "visa": ('<strong>Visa questions?</strong> We are an education agency, not a migration agent. For advice about a visa,\n'
             'we refer students to a registered migration agent. No visa outcome is guaranteed.'),
}


def about(d=None):
    d = d or AB
    L = {**UI_EN, **d.get("ui", {})}
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
<p class="kicker">{e(L["guideK"])}</p>
<h2>{e(L["guideH"])}</h2>
<ul class="paths">{princ}</ul>
</section>
<section class="wrap narrow">
<p class="kicker">{e(d["storyKicker"])}</p>
<h2>{e(d["storyH2"])}</h2>
{story}
<ul class="why">{facts}</ul>
</section>
<section class="wrap">
<p class="kicker">{e(L["howK"])}</p>
<h2>{e(L["howH"])}</h2>
<ol class="flow">{how}</ol>
</section>
<section class="wrap narrow">
<h2>{e(L["notH"])}</h2>
<ul class="list">{nots}</ul>
<h2>{e(L["peopleH"])}</h2>
<p>{e(d["people"])}</p>
<p>{e(L["follow"])} {social}</p>
<p class="small">{e(d["disclaimer"])}</p>
<aside class="cta"><p>{e(L["ctaP"])}</p><span class="small">{e(L["ctaS"])}</span><br>
<a class="btn" href="{L["contact"]}">{e(L["talk"])}</a> <a class="btn ghost" href="{L["courses"]}">{e(L["explore"])}</a></aside>
</section>"""


def partners(d=None):
    d = d or RP
    L = {**UI_RP, **d.get("ui", {})}
    role = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in d["role"])
    sup = "".join(f'<li class="path"><span class="small">{e(k)}</span><h3>{e(t)}</h3><p>{e(b)}</p></li>' for k, t, b in d["support"])
    fields = "".join(f"<li>{e(x)}</li>" for x in d["fields"])
    careful = "".join(f"<p>{e(x)}</p>" for x in d["careful"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    prov = "".join(f'<li class="path"><h3>{e(t)}</h3><p>{e(b)}</p>'
                   + (f'<a href="{MIG_FORM}"{OUT}>{e(L["listFree"])} ↗</a>' if "migration" in t.lower()
                      else f'<a href="mailto:info@weintervisa.com?subject={quote(L["mailSubject"].format(t))}">{e(L["emailUs"])} →</a>')
                   + "</li>" for t, b in d["providers"])
    body = quote(L["applyBody"])
    apply = f"mailto:info@weintervisa.com?subject={quote(L['applySubject'])}&amp;body={body}"
    return f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<p class="actions"><a class="btn" href="#apply">{e(L["applyNow"])} →</a> <a class="btn ghost" href="/partner-portal">{e(L["login"])} →</a></p>
<p class="small">{e(d["small"])}</p>
</div></section>
<section class="wrap">
<p class="kicker">{e(L["howK"])}</p>
<h2>{e(L["howH"])}</h2>
<ol class="flow flow3">{role}</ol>
</section>
<section class="wrap">
<p class="kicker">{e(L["getK"])}</p>
<h2>{e(L["getH"])}</h2>
<ul class="paths">{sup}</ul>
</section>
<section class="wrap narrow" id="apply">
<p class="kicker">{e(L["applyK"])}</p>
<h2>{e(L["applyH"])}</h2>
<p>{e(d["applyIntro"])}</p>
<ul class="list">{fields}</ul>
<p><a class="btn" href="{apply}">{e(L["applyBtn"])}</a></p>
<p class="small">{e(L["applyNote"])} {e(d["applyWarn"])}</p>
</section>
<section class="wrap narrow">
<p class="kicker">{e(L["carefulK"])}</p>
<h2>{e(L["carefulH"])}</h2>
{careful}
<h2>{e(L["faqH"])}</h2>
{faq}
</section>
<section class="wrap">
<p class="kicker">{e(L["provK"])}</p>
<h2>{e(L["provH"])}</h2>
<ul class="paths">{prov}</ul>
<p class="note-box">{L["visa"]}</p>
</section>"""
