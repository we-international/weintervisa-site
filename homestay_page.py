"""/homestay — rebuilt on 21 Nov 2026 from the LIVE Wix page (content/homestay.json): homestay with our
partner AHN, scam warning, why homestay first, steps, AHN's published prices (dated, with source),
house rules, FAQ. AHN sets its own prices and terms; we link to them and never take payment.
"""
import html
import json
from pathlib import Path

from group_pages import icon

ROOT = Path(__file__).resolve().parent
e = html.escape
HS = json.loads((ROOT / "content/homestay.json").read_text())


# Fixed page words; a Thai copy (content/th/homestay.json "ui") overrides them key by key.
UI_EN = {
    "find": "Find a homestay with AHN", "how": "How it works", "scamK": "Avoid accommodation scams", "tipB": "Kenji's tip",
    "whyK": "Why homestay first", "whyH": "A safe, simple landing in a new country", "howH": "From sign-up to your first night",
    "applyP": "Apply through the button on this page", "start": "Start my homestay application", "tip": "Tip:",
    "pricesK": "Prices", "pricesH": "What it costs (Sydney example)",
    "caption": "AHN homestay, Sydney, over 18 (AUD per week: private / shared)", "pkg": "Package (over 18)",
    "knowK": "Good to know", "knowH": "Living with a host family", "faqH": "Common questions",
    "endP": "Book your first home in Australia", "endS": "Apply through the button below — it only takes a few minutes.",
    "ask": "Ask us a question", "endNote": "You'll be taken to AHN's website · Opens a new tab", "contact": "/contact-us",
}


def render(d=None):
    d = d or HS
    L = {**UI_EN, **d.get("ui", {})}
    a = e(d["apply"])
    btn = lambda t: f'<a class="btn" href="{a}" target="_blank" rel="noopener">{e(t)} ↗</a>'
    points = "".join(f'<li>{icon(i)}{e(t)}</li>' for i, t in d["points"])
    s = d["scams"]
    scam = "".join(f"<li>{e(x)}</li>" for x in s["items"])
    why = "".join(f'<li>{icon(i, "ico ico-help")}<strong>{e(t)}</strong><span>{e(b)}</span></li>' for i, t, b in d["why"])
    steps = "".join(f"<li>{e(x)}</li>" for x in d["steps"])
    ab = d["applyBox"]
    abl = "".join(f"<li>{e(x)}</li>" for x in ab["items"])
    p = d["prices"]
    rows = "".join(f'<tr><th scope="row">{e(n)}</th><td data-col="2026">{e(x)}</td><td data-col="2027">{e(y)}</td></tr>' for n, x, y in p["rows"])
    know = "".join(f'<li class="path"><h3>{e(t)}</h3><ul class="list">{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></li>' for t, items in d["know"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(ans)}</p></details>' for q, ans in d["faq"])
    return f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<ul class="points two-col">{points}</ul>
<p class="actions">{btn(L["find"])} <a class="btn ghost" href="#how">{e(L["how"])}</a></p>
<p class="small">{e(d["applyNote"])}</p>
</div></section>
<section class="wrap">
<p class="kicker">{e(L["scamK"])}</p>
<h2>{e(s["h2"])}</h2>
<p>{e(s["body"])}</p>
<ul class="list">{scam}</ul>
<aside class="tip"><strong>{e(L["tipB"])}</strong> {e(s["tip"])}</aside>
</section>
<section class="wrap">
<p class="kicker">{e(L["whyK"])}</p>
<h2>{e(L["whyH"])}</h2>
<ul class="help">{why}</ul>
<p class="small">{e(d["endorsed"])}</p>
</section>
<section class="wrap narrow" id="how">
<p class="kicker">{e(L["how"])}</p>
<h2>{e(L["howH"])}</h2>
<ol class="steps">{steps}</ol>
<aside class="cta"><p>{e(L["applyP"])}</p><span class="small">{e(ab["body"])}</span>
<ul class="list">{abl}</ul>
{btn(L["start"])}
<p class="small"><strong>{e(L["tip"])}</strong> {e(ab["tip"])}</p></aside>
</section>
<section class="wrap narrow">
<p class="kicker">{e(L["pricesK"])}</p>
<h2>{e(L["pricesH"])}</h2>
<p>{e(p["intro"])}</p>
<div class="fees all"><table><caption>{e(L["caption"])}</caption>
<thead><tr><th scope="col">{e(L["pkg"])}</th><th scope="col">2026</th><th scope="col">2027</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="small">{e(p["note"])}</p>
<p class="small">{e(p["source"])}</p>
</section>
<section class="wrap">
<p class="kicker">{e(L["knowK"])}</p>
<h2>{e(L["knowH"])}</h2>
<ul class="paths">{know}</ul>
</section>
<section class="wrap narrow">
<h2>{e(L["faqH"])}</h2>
{faq}
<p class="small">{e(d["faqNote"])}</p>
</section>
<section class="wrap narrow">
<aside class="cta"><p>{e(L["endP"])}</p><span class="small">{e(L["endS"])}</span><br>
{btn(L["find"])} <a class="btn ghost" href="{L["contact"]}">{e(L["ask"])}</a>
<p class="small">{e(L["endNote"])}</p></aside>
</section>"""
