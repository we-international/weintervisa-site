"""/fast-track-courses — Working Holiday (417/462) page, rebuilt on 21 Nov 2026 from the LIVE Wix page
(content/fast-track.json, from the compare run's saved text + markup). Same rules as home_page.py:
no reply-time or outcome promises, visa questions → registered migration agent, no tracking,
images only from local copies in assets/img.
"""
import html
import json
from pathlib import Path

from home_page import img, ext
from group_pages import icon

ROOT = Path(__file__).resolve().parent
e = html.escape
FT = json.loads((ROOT / "content/fast-track.json").read_text())


# Fixed page words; a Thai copy (content/th/fast-track.json "ui") overrides them key by key.
UI_EN = {
    "plan": "Get a course plan", "find": "Find my course (30 seconds)", "watch": "Watch the course video",
    "finderK": "Course finder", "finderH": "Which course suits you?",
    "finderP": "No sign-up. Pick what sounds good and we'll show you the course. Then ask us for a free course plan.",
    "finderQ": "What kind of work sounds good to you?", "howK": "How it works", "howH": "From \"I'm curious\" to your first class",
    "tipB": "Kenji's tip", "readyP": "Ready? Ask for your free course plan", "getPlan": "Get my free course plan",
    "mailSubject": "Working%20Holiday%20course%20plan", "email": "Email info@weintervisa.com",
    "noIds": "Please don't send passport numbers, visa grant numbers or bank details.",
    "coursesK": "Courses", "coursesH": "Three courses Working Holiday Makers love",
    "coursesP": "Each one has a fast-track option for Working Holiday visa holders. Weeks, placement and intakes vary by provider.",
    "feesNote": "Fees, materials and placement costs depend on the course, provider and intake. Ask us for a free written quote.",
    "watchK": "Watch", "yt": "Watch on YouTube", "guide": "Read the CHC33021 guide",
    "leadK": "Where it can lead", "leadH": "Skills that Australia needs", "rolesH": "Possible roles after Cert III",
    "mayaB": "Maya says", "summary": "Read our summary",
    "noPromise": "No course can promise a job, a visa or PR. Employers set their own requirements and checks.",
    "settleK": "Settle in", "settleH": "A place to stay, health cover and your first week",
    "settleNote": "The homestay button opens AHN's website in a new tab, where you sign up. AHN is our homestay partner.",
    "faqH": "Questions Working Holiday Makers ask us", "newsS": "Latest Working Holiday news (Home Affairs)",
    "source": "Source:", "newsLink": "Home Affairs WHM latest news", "checked": "Checked {}.", "guidesS": "More Working Holiday guides",
    "readyH": "Let's plan your course together", "tryFinder": "Try the course finder",
    "qeac": "QEAC-certified counsellor (PIER), QEAC No. 11964 · Based in Sydney, Australia",
    "mayaN": "Maya:", "kenjiN": "Kenji:", "contact": "/contact-us",
    "inNews": "care worker visa news", "leadsS": "Why these jobs are in demand (2 official sources)",
    "en": "",  # Thai copy: ' lang="en"' on English course titles
}


def render(d=None):
    d = d or FT
    L = {**UI_EN, **d.get("ui", {})}
    c_ = L["contact"]
    points = "".join(f'<li>{icon(i)}{e(t)}</li>' for i, t in d["points"])
    finder = "".join(f'<li><a href="{e(h)}">{icon(i)}{e(t)}</a></li>' for i, t, h in d["finder"])
    steps = "".join(f"<li><strong>{e(t)}</strong><span>{b}</span></li>" for t, b in d["steps"])
    # Readability (28 Nov 2026): each course folds (code + title + who it suits in the summary); the photo shows on
    # wide screens only. The id sits on the <details>, so a finder link (#chc33021) opens it (assets/reveal.js).
    courses = "".join(f"""<li class="course">{img(c['img'], "wide-only", w=1536, h=1024)}<div>
<details class="group-fold ft-fold" id="{c['id']}"><summary><div><span class="code">{e(c['code'])}</span><h3{L["en"]}>{e(c['title'])}</h3><p>{e(c['for'])}</p></div></summary>
<ul class="list">{''.join(f'<li>{e(x)}</li>' for x in c['learn'])}</ul>
<p class="links"><a class="btn ghost" href="{c_}">{e(L["plan"])}</a> <a href="{e(c['more'][1])}">{e(c['more'][0])}</a></p>
</details></div></li>""" for c in d["courses"])
    leads = "".join(f'<li><strong>{e(t)}</strong><span>{e(b)} <a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a></span></li>'
                    for t, b, l, u in d["lead_to"])
    roles = "".join(f"<li>{e(r)}</li>" for r in d["roles"])
    settle = "".join(f"""<li class="path"><details class="group-fold ft-fold"><summary><div>{icon(i, "ico ico-path")}<h3>{e(t)}</h3></div></summary><p>{e(b)}</p>
<a href="{e(u)}"{ext(u)}>{e(l)}</a>{f'<a class="second" href="{e(u2)}">{e(l2)}</a>' if l2 else ''}</details></li>"""
                     for i, t, b, l, u, l2, u2 in d["settle"])
    faq = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in d["faq"])
    n = d["whmNews"]
    news = "".join(f"<li><strong>{e(dt)}</strong> {e(t)}</li>" for dt, t in n["items"])
    guides = "".join(f'<li><a href="{e(u)}">{e(t)}</a></li>' for t, u in d["guides"])
    v = d["video"]
    schools = __import__("whv_page").strip_html(th=bool(L["en"]))
    return f"""<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<ul class="points ft-points">{points}</ul>
<p class="actions"><a class="btn" href="#finder">{e(L["find"])} →</a> <a class="btn ghost" href="#video">{e(L["watch"])}</a></p>
</div><div class="hero-side">{img(d["heroImage"], "hero-img", lazy=False, w=1200, h=750)}
<p class="bubble wide-only"><strong>{e(L["mayaN"])}</strong> {e(d["maya"])}</p>
<p class="bubble alt wide-only"><strong>{e(L["kenjiN"])}</strong> {e(d["kenji"])}</p>
</div></div></section>
{schools}<section class="wrap" id="finder">
<p class="kicker">{e(L["finderK"])}</p>
<h2>{e(L["finderH"])}</h2>
<p>{e(L["finderP"])}</p>
<p><strong>{e(L["finderQ"])}</strong></p>
<ul class="finder">{finder}</ul>
</section>
<section class="wrap">
<p class="kicker">{e(L["howK"])}</p>
<h2>{e(L["howH"])}</h2>
<ol class="flow flow3">{steps}</ol>
<aside class="tip"><strong>{e(L["tipB"])}</strong> {d["tip"]}</aside>
<aside class="cta"><p>{e(L["readyP"])}</p><span class="small">{e(d["plan"])}</span><br>
<a class="btn" href="{c_}">{e(L["getPlan"])}</a> <a class="btn ghost" href="mailto:info@weintervisa.com?subject={L["mailSubject"]}">{e(L["email"])}</a>
<p class="small">{e(L["noIds"])}</p></aside>
</section>
<section class="wrap">
<p class="kicker">{e(L["coursesK"])}</p>
<h2>{e(L["coursesH"])}</h2>
<p>{e(L["coursesP"])}</p>
<ul class="courses">{courses}</ul>
<p class="small">{e(L["feesNote"])}</p>
</section>
<section class="wrap" id="video">
<p class="kicker">{e(L["watchK"])}</p>
<h2>{e(v["title"])}</h2>
<p>{e(v["body"])}</p>
<p class="actions"><a class="btn" href="{e(v["url"])}" target="_blank" rel="noopener">{e(L["yt"])} ↗</a> <a href="{e(d["courses"][0]["more"][1])}">{e(L["guide"])}</a></p>
</section>
<section class="wrap">
<p class="kicker">{e(L["leadK"])}</p>
<h2>{e(L["leadH"])}</h2>
<details class="faq"><summary>{e(L["leadsS"])}</summary><ul class="help leads">{leads}</ul></details>
<h3>{e(L["rolesH"])}</h3>
<ul class="tags roles">{roles}</ul>
<details class="faq maya-news"><summary>{e(L["mayaB"])}: {e(L["inNews"])}</summary><p>{e(d["news"])} <a href="{e(d["newsPost"])}">{e(L["summary"])}</a></p></details>
<p class="small">{e(L["noPromise"])}</p>
</section>
<section class="wrap">
<p class="kicker">{e(L["settleK"])}</p>
<h2>{e(L["settleH"])}</h2>
<ul class="paths">{settle}</ul>
<p class="small">{e(L["settleNote"])}</p>
</section>
<section class="wrap narrow">
<h2>{e(L["faqH"])}</h2>
{faq}
<details class="faq"><summary>{e(L["newsS"])}</summary><ul class="list">{news}</ul>
<p class="small">{e(L["source"])} <a href="{e(n["source"])}" target="_blank" rel="noopener">{e(L["newsLink"])} ↗</a>. {e(L["checked"].format(n["checked"]))}</p></details>
<details class="faq"><summary>{e(L["guidesS"])}</summary><ul class="list">{guides}</ul></details>
</section>
<section class="wrap ready">{img(d["readyImage"], "ready-img wide-only", w=900, h=563)}<div>
<h2>{e(L["readyH"])}</h2>
<p>{e(d["ready"])}</p>
<p class="actions"><a class="btn" href="{c_}">{e(L["getPlan"])}</a> <a class="btn ghost" href="#finder">{e(L["tryFinder"])}</a></p>
<p class="small">{e(L["qeac"])} · <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></p>
<p class="small">{e(d["disclaimer"])}</p>
</div></section>
<script src="/assets/reveal.js" defer></script>"""
