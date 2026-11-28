"""/oshc — rebuilt on 22 Nov 2026 from the LIVE Wix page (content/oshc.json): the same partner links
(provider pages, OVHC, Flywire) plus plain-English 'what OSHC is' and 'what to check' sections.
We never take payment for cover; insurance questions go to the insurer; visa questions go to a
registered migration agent. No script, no tracking.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
e = html.escape
OS = json.loads((ROOT / "content/oshc.json").read_text())
OUT = ' target="_blank" rel="noopener"'


# Fixed page words; a Thai copy (content/th/oshc.json "ui") overrides them key by key.
UI_EN = {
    "plan": "Explore plans, cover and details with our partner.", "view": "View {} plans",
    "explore": "Explore OSHC plans", "compare": "Compare providers", "cont": "Continues to our partner website · Opens a new tab",
    "howK": "How it works", "howH": "Three steps to your cover", "provK": "Providers", "provH": "Find your OSHC option",
    "provP": "Choose a provider to explore the details.", "all": "View all partner services",
    "basicsK": "The basics", "whatH": "What is OSHC?", "checkH": "Before you buy, check", "typesH": "Types of cover",
    "otherK": "Looking for something else?", "otherH": "Other cover and payments", "faqH": "Common questions",
    "partnerB": "Partner links.", "ctaP": "Planning your study too? We can help you compare courses and schools.",
    "ctaSend": "Send a message", "ctaHome": "Find a homestay", "contact": "/contact-us", "homestay": "/homestay",
}


def render(d=None):
    d = d or OS
    L = {**UI_EN, **d.get("ui", {})}
    p = e(d["partner"])
    steps = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in d["steps"])
    prov = "".join(f'<li class="path"><h3>{e(n)}</h3><p>{e(L["plan"])}</p>'
                   f'<a href="{e(u)}"{OUT}>{e(L["view"].format(n.split()[0]))} ↗</a></li>' for n, u in d["providers"])
    check = "".join(f"<li>{e(x)}</li>" for x in d["check"])
    types = "".join(f"<li><strong>{e(t)}</strong> — {e(b)}</li>" for t, b in d["types"])
    other = "".join(f'<li class="path"><h3>{e(t)}</h3><p>{e(b)}</p><a href="{e(u)}"{OUT}>{e(l)} ↗</a></li>' for t, b, l, u in d["other"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    return f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<p class="actions"><a class="btn" href="{p}"{OUT}>{e(L["explore"])} ↗</a> <a class="btn ghost" href="#options">{e(L["compare"])}</a></p>
<p class="small">{e(L["cont"])}</p>
</div></section>
<section class="wrap">
<p class="kicker">{e(L["howK"])}</p>
<h2>{e(L["howH"])}</h2>
<ol class="flow flow3">{steps}</ol>
</section>
<section class="wrap" id="options">
<p class="kicker">{e(L["provK"])}</p>
<h2>{e(L["provH"])}</h2>
<p>{e(L["provP"])}</p>
<ul class="paths">{prov}</ul>
<p><a class="btn ghost" href="{e(d["all"])}"{OUT}>{e(L["all"])} ↗</a></p>
</section>
<section class="wrap narrow">
<p class="kicker">{e(L["basicsK"])}</p>
<h2>{e(L["whatH"])}</h2>
<p>{e(d["what"])}</p>
<p class="note-box">{e(d["whatNote"])}</p>
<h2>{e(L["checkH"])}</h2>
<ul class="list">{check}</ul>
<h2>{e(L["typesH"])}</h2>
<ul class="list">{types}</ul>
<p class="small">{e(d["typesNote"])}</p>
</section>
<section class="wrap">
<p class="kicker">{e(L["otherK"])}</p>
<h2>{e(L["otherH"])}</h2>
<ul class="paths">{other}</ul>
</section>
<section class="wrap narrow">
<h2>{e(L["faqH"])}</h2>
{faq}
<p class="small"><strong>{e(L["partnerB"])}</strong> {e(d["partnerNote"])}</p>
<div class="cta"><p>{e(L["ctaP"])}</p>
<a class="btn" href="{L["contact"]}">{e(L["ctaSend"])}</a> <a class="btn ghost" href="{L["homestay"]}">{e(L["ctaHome"])}</a></div>
</section>"""
