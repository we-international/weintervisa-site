"""/fast-track-courses — Working Holiday (417/462) page, rebuilt on 21 Nov 2026 from the LIVE Wix page
(content/fast-track.json, from the compare run's saved text + markup). Same rules as home_page.py:
no reply-time or outcome promises, visa questions → registered migration agent, no tracking,
images only from local copies in assets/img.
"""
import html
import json
from pathlib import Path

from home_page import img, ext

ROOT = Path(__file__).resolve().parent
e = html.escape
FT = json.loads((ROOT / "content/fast-track.json").read_text())


def render():
    d = FT
    points = "".join(f'<li><span aria-hidden="true">{i}</span>{e(t)}</li>' for i, t in d["points"])
    finder = "".join(f'<li><a href="{e(h)}"><span class="ico" aria-hidden="true">{i}</span>{e(t)}</a></li>' for i, t, h in d["finder"])
    steps = "".join(f"<li><strong>{e(t)}</strong><span>{b}</span></li>" for t, b in d["steps"])
    courses = "".join(f"""<li class="course" id="{c['id']}">{img(c['img'], w=1536, h=1024)}<div>
<span class="code">{e(c['code'])}</span><h3>{e(c['title'])}</h3><p>{e(c['for'])}</p>
<ul class="list">{''.join(f'<li>{e(x)}</li>' for x in c['learn'])}</ul>
<p class="links"><a class="btn" href="/contact-us">Get a course plan</a> <a href="{e(c['more'][1])}">{e(c['more'][0])}</a></p>
</div></li>""" for c in d["courses"])
    leads = "".join(f'<li><strong>{e(t)}</strong><span>{e(b)} <a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a></span></li>'
                    for t, b, l, u in d["lead_to"])
    roles = "".join(f"<li>{e(r)}</li>" for r in d["roles"])
    settle = "".join(f"""<li class="path"><span class="ico" aria-hidden="true">{i}</span><h3>{e(t)}</h3><p>{e(b)}</p>
<a href="{e(u)}"{ext(u)}>{e(l)}</a>{f'<a class="second" href="{e(u2)}">{e(l2)}</a>' if l2 else ''}</li>"""
                     for i, t, b, l, u, l2, u2 in d["settle"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in d["faq"])
    n = d["whmNews"]
    news = "".join(f"<li><strong>{e(dt)}</strong> {e(t)}</li>" for dt, t in n["items"])
    guides = "".join(f'<li><a href="{e(u)}">{e(t)}</a></li>' for t, u in d["guides"])
    v = d["video"]
    return f"""<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<ul class="points">{points}</ul>
<p class="actions"><a class="btn" href="#finder">Find my course (30 seconds) →</a> <a class="btn ghost" href="#video">▶ Watch the course video</a></p>
</div><div class="hero-side">{img(d["heroImage"], "hero-img", lazy=False, w=1200, h=750)}
<p class="bubble"><strong>Maya:</strong> {e(d["maya"])}</p>
<p class="bubble alt"><strong>Kenji:</strong> {e(d["kenji"])}</p>
</div></div></section>
<section class="wrap" id="finder">
<p class="kicker">Course finder</p>
<h2>Which course suits you?</h2>
<p>No sign-up. Pick what sounds good and we'll show you the course. Then ask us for a free course plan.</p>
<p><strong>What kind of work sounds good to you?</strong></p>
<ul class="finder">{finder}</ul>
</section>
<section class="wrap">
<p class="kicker">How it works</p>
<h2>From "I'm curious" to your first class</h2>
<ol class="flow flow3">{steps}</ol>
<aside class="tip"><strong>Kenji's tip</strong> {d["tip"]}</aside>
<aside class="cta"><p>Ready? Ask for your free course plan</p><span class="small">{e(d["plan"])}</span><br>
<a class="btn" href="/contact-us">Get my free course plan</a> <a class="btn ghost" href="mailto:info@weintervisa.com?subject=Working%20Holiday%20course%20plan">Email info@weintervisa.com</a>
<p class="small">Please don't send passport numbers, visa grant numbers or bank details.</p></aside>
</section>
<section class="wrap">
<p class="kicker">Courses</p>
<h2>Three courses Working Holiday Makers love</h2>
<p>Each one has a fast-track option for Working Holiday visa holders. Weeks, placement and intakes vary by provider.</p>
<ul class="courses">{courses}</ul>
<p class="small">Fees, materials and placement costs depend on the course, provider and intake. Ask us for a free written quote.</p>
</section>
<section class="wrap" id="video">
<p class="kicker">Watch</p>
<h2>{e(v["title"])}</h2>
<p>{e(v["body"])}</p>
<p class="actions"><a class="btn" href="{e(v["url"])}" target="_blank" rel="noopener">▶ Watch on YouTube ↗</a> <a href="{e(d["courses"][0]["more"][1])}">Read the CHC33021 guide</a></p>
</section>
<section class="wrap">
<p class="kicker">Where it can lead</p>
<h2>Skills that Australia needs</h2>
<ul class="help leads">{leads}</ul>
<h3>Possible roles after Cert III</h3>
<ul class="tags roles">{roles}</ul>
<aside class="tip maya"><strong>Maya says</strong> {e(d["news"])} <a href="{e(d["newsPost"])}">Read our summary</a></aside>
<p class="small">No course can promise a job, a visa or PR. Employers set their own requirements and checks.</p>
</section>
<section class="wrap">
<p class="kicker">Settle in</p>
<h2>A place to stay, health cover and your first week</h2>
<ul class="paths">{settle}</ul>
<p class="small">The homestay button opens AHN's website in a new tab, where you sign up. AHN is our homestay partner.</p>
</section>
<section class="wrap narrow">
<h2>Questions Working Holiday Makers ask us</h2>
{faq}
<details class="faq"><summary>Latest Working Holiday news (Home Affairs)</summary><ul class="list">{news}</ul>
<p class="small">Source: <a href="{e(n["source"])}" target="_blank" rel="noopener">Home Affairs WHM latest news ↗</a>. Checked {e(n["checked"])}.</p></details>
<details class="faq"><summary>More Working Holiday guides</summary><ul class="list">{guides}</ul></details>
</section>
<section class="wrap ready">{img(d["readyImage"], "ready-img", w=900, h=563)}<div>
<h2>Let's plan your course together</h2>
<p>{e(d["ready"])}</p>
<p class="actions"><a class="btn" href="/contact-us">Get my free course plan</a> <a class="btn ghost" href="#finder">Try the course finder</a></p>
<p class="small">QEAC-certified counsellor (PIER), QEAC No. 11964 · Based in Sydney, Australia · <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></p>
<p class="small">{e(d["disclaimer"])}</p>
</div></section>"""
