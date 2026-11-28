"""/english-practice — rebuilt on 21 Nov 2026 from the LIVE Wix page (content/english-practice.json).
Free practice: 8-question quiz (answers in <details>, no script, nothing saved), our English channels,
games, English courses, and the sister brand's kids' printables. No third-party images or embeds.
"""
import html
import json
from pathlib import Path

from group_pages import icon
from home_page import img

ROOT = Path(__file__).resolve().parent
e = html.escape
EP = json.loads((ROOT / "content/english-practice.json").read_text())


# Fixed page words; a Thai copy (content/th/english-practice.json "ui") overrides them key by key.
UI_EN = {
    "q": "Question {} of 8", "notQuite": "Not quite:", "which": "Which is correct?", "show": "Show the answer",
    "sub": "Subscribe on YouTube", "follow": "Follow:", "soon": "Coming soon", "etsy": "View on Etsy",
    "quizBtn": "Try the 1-minute quiz", "watchBtn": "Watch the videos", "mayaN": "Maya:", "kenjiN": "Kenji:",
    "gameK": "Mini game", "gameH": "Say it right: 8 common mistakes",
    "gameP": "Pick the natural way to say it, then open the answer. No sign-up, no score saved, just practice.",
    "watchK": "Watch &amp; listen", "watchH": "Our English channels",
    "watchP": "Every view, like and comment helps us make more free lessons. Thank you for subscribing!",
    "chalB": "Kenji's challenge", "gamesK": "Games", "gamesH": "Play your way to better English",
    "studyP": "Want to study English in Australia?", "seeCourses": "See English courses", "talk": "Talk to our team",
    "studyNote": ("General English, academic English and IELTS or PTE preparation. On a visitor visa? We only look at English courses with no work placement.\n"
                  "Course length, visa conditions and entry rules are checked before you go ahead; for visa advice we refer you to a registered migration agent."),
    "allKids": "See all kids' activities",
    "moreQ": "{} more questions", "kidsFold": "See the {} printables", "courses": "/courses", "contact": "/contact-us",
    "en": "",  # Thai copy: ' lang="en"' on the English sentences of the quiz
}


def quiz_item(n, wrong, options, answer, why, L=UI_EN):
    # rotate so the right answer is not always A (A, B, C, A, ...)
    k = n % len(options)
    order = options[-k:] + options[:-k] if k else list(options)
    letter = "ABC"[order.index(options[answer])]
    en = L["en"]
    opts = "".join(f"<li{en}>{e(o)}</li>" for o in order)
    return f"""<li class="quiz"><p class="kicker">{e(L["q"].format(n + 1))}</p>
<p class="wrong">{e(L["notQuite"])} <s{en}>{e(wrong)}</s></p><p><strong>{e(L["which"])}</strong></p>
<ol type="A">{opts}</ol>
<details><summary>{e(L["show"])}</summary><p><strong>{icon("badge", "ico ico-ok")} {letter}. <span{en}>{e(options[answer])}</span></strong></p><p class="small">{e(why)}</p></details></li>"""


def render(d=None):
    d = d or EP
    L = {**UI_EN, **d.get("ui", {})}
    points = "".join(f'<li>{icon(i)}{e(t)}</li>' for i, t in d["points"])
    # Readability (28 Nov 2026): 3 questions open, the rest in one fold (every question stays in the HTML)
    items = [quiz_item(n, *q, L=L) for n, q in enumerate(d["quiz"])]
    SHOW = 3
    quiz = "".join(items[:SHOW])
    quiz_more = (f'<details class="group-fold quiz-more" id="more-questions"><summary><h3>{e(L["moreQ"].format(len(items) - SHOW))}</h3></summary>'
                 f'<ol class="quizzes">{"".join(items[SHOW:])}</ol></details>') if len(items) > SHOW else ""
    chans = "".join(f"""<li class="path"><h3>{e(c['title'])}</h3><p>{e(c['body'])}</p>
<a href="{e(c['youtube'])}" target="_blank" rel="noopener">{e(L["sub"])} ↗</a>
<p class="small">{e(L['follow'])} {' · '.join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>' for t, u in c['follow'])}</p></li>""" for c in d["channels"])
    games = "".join(f"""<li class="path">{icon(i, "ico ico-path")}<h3>{e(t)}</h3><p>{e(b)}</p>
{f'<a href="{e(u)}"' + (' target="_blank" rel="noopener"' if u.startswith('http') else '') + f'>{e(l)}</a>' if l else f'<span class="tag">{e(L["soon"])}</span>'}</li>"""
                    for i, t, b, l, u in d["games"])
    k = d["kids"]
    kids = "".join(f"""<li class="path"><span class="tag">{e(a)}</span><h3>{e(t)}</h3><p>{e(b)}</p>
<a href="{e(u)}" target="_blank" rel="noopener">{e(L["etsy"])} ↗</a></li>""" for a, t, b, u in k["items"])
    return f"""<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<ul class="points">{points}</ul>
<p class="actions"><a class="btn" href="#quiz">{e(L["quizBtn"])} →</a> <a class="btn ghost" href="#watch">{e(L["watchBtn"])}</a></p>
</div><div class="hero-side">{img(d["heroImage"], "hero-img", lazy=False, w=1200, h=750)}
<p class="bubble wide-only"><strong>{e(L["mayaN"])}</strong> {e(d["maya"])}</p>
<p class="bubble alt wide-only"><strong>{e(L["kenjiN"])}</strong> {e(d["kenji"])}</p>
</div></div></section>
<section class="wrap" id="quiz">
<p class="kicker">{e(L["gameK"])}</p>
<h2>{e(L["gameH"])}</h2>
<p>{e(L["gameP"])}</p>
<ol class="quizzes">{quiz}</ol>
{quiz_more}
</section>
<section class="wrap" id="watch">
<p class="kicker">{L["watchK"]}</p>
<h2>{e(L["watchH"])}</h2>
<p>{e(L["watchP"])}</p>
<ul class="paths two">{chans}</ul>
<div class="tip"><strong>{e(L["chalB"])}</strong> {e(d["challenge"])}</div>
</section>
<section class="wrap">
<p class="kicker">{e(L["gamesK"])}</p>
<h2>{e(L["gamesH"])}</h2>
<ul class="paths">{games}</ul>
</section>
<section class="wrap">
<div class="cta"><p>{e(L["studyP"])}</p><span class="small">{e(d["study"])}</span><br>
<a class="btn" href="{L["courses"]}#english-pathways">{e(L["seeCourses"])} →</a> <a class="btn ghost" href="{L["contact"]}">{e(L["talk"])}</a>
<p class="small">{L["studyNote"]}</p></div>
</section>
<section class="wrap">
<p class="kicker">{e(k["kicker"])}</p>
<h2>{e(k["h2"])}</h2>
<p>{e(k["body"])}</p>
<details class="group-fold kids-fold" id="kids-printables"><summary><h3>{e(L["kidsFold"].format(len(k["items"])))}</h3></summary>
<ul class="paths">{kids}</ul></details>
<p><a href="{e(k["shop"])}" target="_blank" rel="noopener">{e(L["allKids"])} ↗</a></p>
<p class="small">{e(k["note"])}</p>
<p class="small">{e(d["characters"])}</p>
</section>
<script src="/assets/reveal.js" defer></script>"""
