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


def render():
    d = OS
    p = e(d["partner"])
    steps = "".join(f"<li><strong>{e(t)}</strong><span>{e(b)}</span></li>" for t, b in d["steps"])
    prov = "".join(f'<li class="path"><h3>{e(n)}</h3><p>Explore plans, cover and details with our partner.</p>'
                   f'<a href="{e(u)}"{OUT}>View {e(n.split()[0])} plans ↗</a></li>' for n, u in d["providers"])
    check = "".join(f"<li>{e(x)}</li>" for x in d["check"])
    types = "".join(f"<li><strong>{e(t)}</strong> — {e(b)}</li>" for t, b in d["types"])
    other = "".join(f'<li class="path"><h3>{e(t)}</h3><p>{e(b)}</p><a href="{e(u)}"{OUT}>{e(l)} ↗</a></li>' for t, b, l, u in d["other"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d["faq"])
    return f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<p class="actions"><a class="btn" href="{p}"{OUT}>Explore OSHC plans ↗</a> <a class="btn ghost" href="#options">Compare providers</a></p>
<p class="small">Continues to our partner website · Opens a new tab</p>
</div></section>
<section class="wrap">
<p class="kicker">How it works</p>
<h2>Three steps to your cover</h2>
<ol class="flow flow3">{steps}</ol>
</section>
<section class="wrap" id="options">
<p class="kicker">Providers</p>
<h2>Find your OSHC option</h2>
<p>Choose a provider to explore the details.</p>
<ul class="paths">{prov}</ul>
<p><a class="btn ghost" href="{e(d["all"])}"{OUT}>View all partner services ↗</a></p>
</section>
<section class="wrap narrow">
<p class="kicker">The basics</p>
<h2>What is OSHC?</h2>
<p>{e(d["what"])}</p>
<p class="note-box">{e(d["whatNote"])}</p>
<h2>Before you buy, check</h2>
<ul class="list">{check}</ul>
<h2>Types of cover</h2>
<ul class="list">{types}</ul>
<p class="small">{e(d["typesNote"])}</p>
</section>
<section class="wrap">
<p class="kicker">Looking for something else?</p>
<h2>Other cover and payments</h2>
<ul class="paths">{other}</ul>
</section>
<section class="wrap narrow">
<h2>Common questions</h2>
{faq}
<p class="small"><strong>Partner links.</strong> {e(d["partnerNote"])}</p>
<aside class="cta"><p>Planning your study too? We can help you compare courses and schools.</p>
<a class="btn" href="/contact-us">Send a message</a> <a class="btn ghost" href="/homestay">Find a homestay</a></aside>
</section>"""
