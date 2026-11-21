"""/homestay — rebuilt on 21 Nov 2026 from the LIVE Wix page (content/homestay.json): homestay with our
partner AHN, scam warning, why homestay first, steps, AHN's published prices (dated, with source),
house rules, FAQ. AHN sets its own prices and terms; we link to them and never take payment.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
e = html.escape
HS = json.loads((ROOT / "content/homestay.json").read_text())


def render():
    d = HS
    a = e(d["apply"])
    btn = lambda t: f'<a class="btn" href="{a}" target="_blank" rel="noopener">{e(t)} ↗</a>'
    points = "".join(f'<li><span aria-hidden="true">{i}</span>{e(t)}</li>' for i, t in d["points"])
    s = d["scams"]
    scam = "".join(f"<li>{e(x)}</li>" for x in s["items"])
    why = "".join(f'<li><span class="ico" aria-hidden="true">{i}</span><strong>{e(t)}</strong><span>{e(b)}</span></li>' for i, t, b in d["why"])
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
<p class="actions">{btn("Find a homestay with AHN")} <a class="btn ghost" href="#how">How it works</a></p>
<p class="small">{e(d["applyNote"])}</p>
</div></section>
<section class="wrap">
<p class="kicker">Avoid accommodation scams</p>
<h2>{e(s["h2"])}</h2>
<p>{e(s["body"])}</p>
<ul class="list">{scam}</ul>
<aside class="tip"><strong>Kenji's tip</strong> {e(s["tip"])}</aside>
</section>
<section class="wrap">
<p class="kicker">Why homestay first</p>
<h2>A safe, simple landing in a new country</h2>
<ul class="help">{why}</ul>
<p class="small">{e(d["endorsed"])}</p>
</section>
<section class="wrap narrow" id="how">
<p class="kicker">How it works</p>
<h2>From sign-up to your first night</h2>
<ol class="steps">{steps}</ol>
<aside class="cta"><p>Apply through the button on this page</p><span class="small">{e(ab["body"])}</span>
<ul class="list">{abl}</ul>
{btn("Start my homestay application")}
<p class="small"><strong>Tip:</strong> {e(ab["tip"])}</p></aside>
</section>
<section class="wrap narrow">
<p class="kicker">Prices</p>
<h2>What it costs (Sydney example)</h2>
<p>{e(p["intro"])}</p>
<div class="fees all"><table><caption>AHN homestay, Sydney, over 18 (AUD per week: private / shared)</caption>
<thead><tr><th scope="col">Package (over 18)</th><th scope="col">2026</th><th scope="col">2027</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="small">{e(p["note"])}</p>
<p class="small">{e(p["source"])}</p>
</section>
<section class="wrap">
<p class="kicker">Good to know</p>
<h2>Living with a host family</h2>
<ul class="paths">{know}</ul>
</section>
<section class="wrap narrow">
<h2>Common questions</h2>
{faq}
<p class="small">{e(d["faqNote"])}</p>
</section>
<section class="wrap narrow">
<aside class="cta"><p>Book your first home in Australia</p><span class="small">Apply through the button below — it only takes a few minutes.</span><br>
{btn("Find a homestay with AHN")} <a class="btn ghost" href="/contact-us">Ask us a question</a>
<p class="small">You'll be taken to AHN's website · Opens a new tab</p></aside>
</section>"""
