"""/english-practice — rebuilt on 21 Nov 2026 from the LIVE Wix page (content/english-practice.json).
Free practice: 8-question quiz (answers in <details>, no script, nothing saved), our English channels,
games, English courses, and the sister brand's kids' printables. No third-party images or embeds.
"""
import html
import json
from pathlib import Path

from home_page import img

ROOT = Path(__file__).resolve().parent
e = html.escape
EP = json.loads((ROOT / "content/english-practice.json").read_text())


def quiz_item(n, wrong, options, answer, why):
    # rotate so the right answer is not always A (A, B, C, A, ...)
    k = n % len(options)
    order = options[-k:] + options[:-k] if k else list(options)
    letter = "ABC"[order.index(options[answer])]
    opts = "".join(f"<li>{e(o)}</li>" for o in order)
    return f"""<li class="quiz"><p class="kicker">Question {n + 1} of 8</p>
<p class="wrong">Not quite: <s>{e(wrong)}</s></p><p><strong>Which is correct?</strong></p>
<ol type="A">{opts}</ol>
<details><summary>Show the answer</summary><p><strong>✓ {letter}. {e(options[answer])}</strong></p><p class="small">{e(why)}</p></details></li>"""


def render():
    d = EP
    points = "".join(f'<li><span aria-hidden="true">{i}</span>{e(t)}</li>' for i, t in d["points"])
    quiz = "".join(quiz_item(n, *q) for n, q in enumerate(d["quiz"]))
    chans = "".join(f"""<li class="path"><h3>{e(c['title'])}</h3><p>{e(c['body'])}</p>
<a href="{e(c['youtube'])}" target="_blank" rel="noopener">▶ Subscribe on YouTube ↗</a>
<p class="small">Follow: {' · '.join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>' for t, u in c['follow'])}</p></li>""" for c in d["channels"])
    games = "".join(f"""<li class="path"><span class="ico" aria-hidden="true">{i}</span><h3>{e(t)}</h3><p>{e(b)}</p>
{f'<a href="{e(u)}"' + (' target="_blank" rel="noopener"' if u.startswith('http') else '') + f'>{e(l)}</a>' if l else '<span class="tag">Coming soon</span>'}</li>"""
                    for i, t, b, l, u in d["games"])
    k = d["kids"]
    kids = "".join(f"""<li class="path"><span class="tag">{e(a)}</span><h3>{e(t)}</h3><p>{e(b)}</p>
<a href="{e(u)}" target="_blank" rel="noopener">View on Etsy ↗</a></li>""" for a, t, b, u in k["items"])
    return f"""<section class="hero home-hero"><div class="wrap hero-grid"><div>
<p class="kicker">{e(d["kicker"])}</p>
<h1>{e(d["h1"])}</h1>
<p class="lead">{e(d["lead"])}</p>
<ul class="points">{points}</ul>
<p class="actions"><a class="btn" href="#quiz">Try the 1-minute quiz →</a> <a class="btn ghost" href="#watch">Watch the videos</a></p>
</div><div class="hero-side">{img(d["heroImage"], "hero-img", lazy=False, w=1200, h=750)}
<p class="bubble"><strong>Maya:</strong> {e(d["maya"])}</p>
<p class="bubble alt"><strong>Kenji:</strong> {e(d["kenji"])}</p>
</div></div></section>
<section class="wrap" id="quiz">
<p class="kicker">Mini game</p>
<h2>Say it right: 8 common mistakes</h2>
<p>Pick the natural way to say it, then open the answer. No sign-up, no score saved, just practice.</p>
<ol class="quizzes">{quiz}</ol>
</section>
<section class="wrap" id="watch">
<p class="kicker">Watch &amp; listen</p>
<h2>Our English channels</h2>
<p>Every view, like and comment helps us make more free lessons. Thank you for subscribing!</p>
<ul class="paths two">{chans}</ul>
<aside class="tip"><strong>Kenji's challenge</strong> {e(d["challenge"])}</aside>
</section>
<section class="wrap">
<p class="kicker">Games</p>
<h2>Play your way to better English</h2>
<ul class="paths">{games}</ul>
</section>
<section class="wrap">
<aside class="cta"><p>Want to study English in Australia?</p><span class="small">{e(d["study"])}</span><br>
<a class="btn" href="/courses#english-pathways">See English courses →</a> <a class="btn ghost" href="/contact-us">Talk to our team</a>
<p class="small">General English, academic English and IELTS or PTE preparation. On a visitor visa? We only look at English courses with no work placement.
Course length, visa conditions and entry rules are checked before you go ahead; for visa advice we refer you to a registered migration agent.</p></aside>
</section>
<section class="wrap">
<p class="kicker">{e(k["kicker"])}</p>
<h2>{e(k["h2"])}</h2>
<p>{e(k["body"])}</p>
<ul class="paths">{kids}</ul>
<p><a href="{e(k["shop"])}" target="_blank" rel="noopener">See all kids' activities ↗</a></p>
<p class="small">{e(k["note"])}</p>
<p class="small">{e(d["characters"])}</p>
</section>"""
