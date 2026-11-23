"""Redesign mockups for the owner to choose from (task WEI-WEB-REDESIGN-1123, step 3).

Owner 23 Nov 2026: the new site "feels like a report page ... too much pushed in, hard to read;
maybe split the pages differently". These are 2 directions for the home page and the Working
Holiday page (phone + desktop), plus the new sitemap. Preview build only: /redesign/...
(noindex, not in sitemap.xml, never in the production build). Real text from content/*.json,
shortened; nothing new is promised. When the owner picks one, the real pages are rebuilt and
this file goes away.
"""
import json
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).parent
HOME = json.loads((ROOT / "content/home.json").read_text())
FT = json.loads((ROOT / "content/fast-track.json").read_text())
IMG = "/assets/img/"
COMPANY = "We International Education &amp; Visa Pty Ltd"

CSS = """
:root{--ink:#14213d;--muted:#5b6478;--bg:#fbfaf7;--card:#fff;--line:#e8e4da;--brand:#0f5c63;--brand2:#e9f2f1;--accent:#e8a33d;--sand:#f4efe4}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans Thai",sans-serif;color:var(--ink);background:var(--bg)}
img{max-width:100%;height:auto;display:block}a{color:var(--brand)}
.mock{max-width:none;margin:0;background:#14213d;color:#fff;font-size:13px;padding:6px 16px;text-align:center}
.mock a{color:#ffd58a}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:8px;padding:12px 16px;background:rgba(255,255,255,.96);border-bottom:1px solid var(--line)}
.brand{font-weight:800;text-decoration:none;color:var(--ink);font-size:18px;margin-right:auto}
.top .nav{display:none;gap:4px}.top .nav a{padding:8px 10px;text-decoration:none;color:var(--ink);border-radius:8px;font-size:15px}
.top .lang{padding:6px 10px;border:1px solid var(--line);border-radius:8px;text-decoration:none;color:var(--ink);font-weight:700;font-size:14px}
.top .talk{background:var(--brand);color:#fff;padding:8px 14px;border-radius:999px;text-decoration:none;font-weight:700;font-size:15px}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
section{padding:40px 0}
h1{font-size:34px;line-height:1.15;letter-spacing:-.02em;margin:0 0 12px}
h2{font-size:25px;line-height:1.2;letter-spacing:-.01em;margin:0 0 8px}
h3{font-size:19px;line-height:1.3;margin:0 0 4px}
p{margin:0 0 12px;max-width:60ch}
.lead{font-size:19px;color:var(--muted)}
.kicker{font-size:14px;font-weight:700;color:var(--brand);letter-spacing:.04em;text-transform:uppercase;margin:0 0 8px}
.btn{display:inline-flex;align-items:center;min-height:48px;background:var(--brand);color:#fff;padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:700}
.link{font-weight:700;text-decoration:none}
.muted{color:var(--muted)}
.trust{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:16px 0 0}
.trust li{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-size:14px}
.doors{display:grid;gap:14px;list-style:none;padding:0;margin:20px 0 0}
.door a{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:10px;text-decoration:none;color:var(--ink)}
.door img{width:96px;height:96px;object-fit:cover;border-radius:12px}
.door .ico{width:96px;height:96px;border-radius:12px;background:var(--brand2);display:grid;place-items:center;font-size:40px}
.door span{color:var(--muted);font-size:15px;display:block}
.door b{color:var(--brand);font-size:15px}
.steps{display:grid;gap:12px;list-style:none;padding:0;margin:16px 0 0;counter-reset:s}
.steps li{counter-increment:s;display:grid;grid-template-columns:40px 1fr;gap:12px;align-items:start}
.steps li::before{content:counter(s);width:40px;height:40px;border-radius:50%;background:var(--accent);color:#14213d;font-weight:800;display:grid;place-items:center}
.band{background:var(--sand)}
.cta{background:var(--brand);color:#fff;border-radius:20px;padding:28px 20px;text-align:center}
.cta p{color:#e3efee;margin:0 auto 16px}.cta .btn{background:#fff;color:var(--brand)}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:8px 0}
details summary{cursor:pointer;padding:14px 16px;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:12px}
details summary::after{content:"+";font-size:22px;line-height:1;color:var(--brand)}
details[open] summary::after{content:"−"}
details summary::-webkit-details-marker{display:none}
details>div{padding:0 16px 14px;color:var(--muted)}
.cards{display:grid;gap:14px;list-style:none;padding:0;margin:16px 0 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.card img{width:100%;aspect-ratio:16/9;object-fit:cover}
.card .in{padding:14px 16px 16px}
.code{font-size:13px;font-weight:700;color:var(--brand);letter-spacing:.03em}
.foot{border-top:1px solid var(--line);padding:24px 16px 40px;font-size:14px;color:var(--muted);text-align:center}
.foot p{margin:4px auto;max-width:70ch}
/* Variant B pieces */
.ask{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0}
.ask input{position:absolute;opacity:0;pointer-events:none}
.ask label{border:2px solid var(--brand);color:var(--brand);border-radius:999px;padding:10px 16px;font-weight:700;cursor:pointer;min-height:48px;display:inline-flex;align-items:center;background:#fff}
.ask input:checked+label{background:var(--brand);color:#fff}
.ask input:focus-visible+label{outline:3px solid var(--accent)}
.answer{display:none;width:100%;margin-top:14px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px}
#q1:checked~#a1,#q2:checked~#a2,#q3:checked~#a3,#q4:checked~#a4{display:block}
.answer p{margin-bottom:12px}
.hero-b{background:linear-gradient(180deg,var(--brand2),var(--bg))}
.split{display:grid;gap:20px;align-items:center}
.split img{border-radius:20px}
.proof{display:grid;gap:10px;grid-template-columns:1fr 1fr;list-style:none;padding:0;margin:16px 0 0}
.proof li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px}
.proof strong{display:block;font-size:22px;color:var(--brand)}
.proof span{font-size:14px;color:var(--muted)}
.tabs{margin-top:8px}
.tabs>input{position:absolute;opacity:0;pointer-events:none}
.tabbar{display:flex;gap:6px;overflow-x:auto;border-bottom:1px solid var(--line);position:sticky;top:57px;background:var(--bg);z-index:4;padding-top:8px}
.tabbar label{padding:10px 14px;font-weight:700;color:var(--muted);cursor:pointer;white-space:nowrap;border-bottom:3px solid transparent;min-height:44px}
.panel{display:none;padding:20px 0}
#t1:checked~.tabbar label[for=t1],#t2:checked~.tabbar label[for=t2],#t3:checked~.tabbar label[for=t3],#t4:checked~.tabbar label[for=t4]{color:var(--brand);border-color:var(--brand)}
#t1:checked~#p1,#t2:checked~#p2,#t3:checked~#p3,#t4:checked~#p4{display:block}
.sticky{position:sticky;bottom:0;background:rgba(255,255,255,.97);border-top:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;justify-content:space-between;z-index:6}
.sticky span{font-size:14px;color:var(--muted)}
.pick{display:grid;gap:10px;list-style:none;padding:0;margin:14px 0 0}
.pick a{display:flex;gap:12px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;text-decoration:none;color:var(--ink);font-weight:600;min-height:56px}
.pick a span{font-size:24px}
/* Sitemap */
.tree{list-style:none;padding:0;margin:0;display:grid;gap:12px}
.tree>li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.tree ul{margin:6px 0 0;padding-left:18px;color:var(--muted);font-size:15px}
.choose{display:grid;gap:14px;list-style:none;padding:0}
.choose a{display:block;background:var(--card);border:2px solid var(--line);border-radius:16px;padding:16px;text-decoration:none;color:var(--ink)}
.choose a:hover{border-color:var(--brand)}
table{border-collapse:collapse;width:100%;font-size:15px;background:var(--card)}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
@media(min-width:760px){
 h1{font-size:48px}h2{font-size:30px}section{padding:64px 0}
 .top{padding:12px 24px}.top .nav{display:flex}
 .doors{grid-template-columns:1fr 1fr}
 .door a{grid-template-columns:140px 1fr;padding:12px}.door img,.door .ico{width:140px;height:120px}
 .steps{grid-template-columns:repeat(3,1fr)}.steps li{grid-template-columns:1fr}
 .cards{grid-template-columns:repeat(3,1fr)}
 .split{grid-template-columns:1.1fr .9fr}
 .proof{grid-template-columns:repeat(4,1fr)}
 .tree{grid-template-columns:repeat(3,1fr)}
 .choose{grid-template-columns:1fr 1fr}
 .tabbar{top:61px}
 .sticky{display:none}
}
"""

NAV = [("Study", "/courses"), ("Working Holiday", "/fast-track-courses"), ("Nursing", "/courses/nursing-pathways-australia"),
       ("Guides", "/blog"), ("About", "/about-we-international")]


def shell(title, body, *, variant, sticky=""):
    nav = "".join(f'<a href="{h}">{l}</a>' for l, h in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="Design mockup for the owner to review (not a live page).">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>{CSS}</style>
</head>
<body>
<p class="mock">Design mockup {esc(variant)} · for review only · <a href="/redesign/">all options</a></p>
<header class="top">
  <a class="brand" href="/redesign/">We International</a>
  <nav class="nav">{nav}</nav>
  <a class="lang" href="/th/">ไทย</a>
  <a class="talk" href="/contact-us">Talk to us</a>
</header>
<main>
{body}
</main>
{sticky}
<footer class="foot">
  <p><strong>{COMPANY}</strong> · QEAC 11964</p>
  <p>We help with study and courses in Australia. We are not a migration agent: for visa advice we refer you to a registered migration agent.</p>
  <p><a href="/contact-us">Contact</a> · <a href="/privacy-policy">Privacy</a> · <a href="/frequently-asked-questions">Help centre</a> · <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></p>
</footer>
</body>
</html>
"""


def img(file, alt, extra=""):
    return f'<img src="{IMG}{file}" alt="{esc(alt)}" loading="lazy"{extra}>'


C = {c["id"]: c for c in FT["courses"]}
DOORS = [
    ("/fast-track-courses", C["chc33021"]["img"]["file"], "", "I'm on a Working Holiday visa",
     "Learn a practical skill in up to 4 months of study."),
    ("/courses", C["chc30125"]["img"]["file"], "", "I want to study in Australia",
     "Find a course that fits your visa, budget and goals."),
    ("/courses/nursing-pathways-australia", C["hlt33115"]["img"]["file"], "", "I'm a nurse, or want to be one",
     "See how registration works and the prep courses."),
    ("/referral-partners", "", "🤝", "I'm a school or a partner agency", "Work with us and refer students."),
]


def doors():
    out = []
    for href, f, ico, title, body in DOORS:
        pic = img(f, "") if f else f'<div class="ico" aria-hidden="true">{ico}</div>'
        out.append(f'<li class="door"><a href="{href}">{pic}<div><h3>{esc(title)}</h3><span>{esc(body)}</span><b>See more →</b></div></a></li>')
    return '<ul class="doors">' + "".join(out) + "</ul>"


STEPS3 = [(a, b) for a, b in HOME["steps"]]


def steps(items):
    return '<ol class="steps">' + "".join(f"<li><div><h3>{esc(a)}</h3><p class=muted>{esc(b)}</p></div></li>" for a, b in items) + "</ol>"


def faq(items):
    return "".join(f"<details><summary>{esc(q)}</summary><div><p>{a}</p></div></details>" for q, a in items)


TRUST = ["QEAC certified counsellor · No. 11964", "Office in Sydney · help online Australia-wide", "Course advice is free"]


def trust():
    return '<ul class="trust">' + "".join(f"<li>✓ {esc(t)}</li>" for t in TRUST) + "</ul>"


def cta(text, button="Talk to us", href="/contact-us"):
    return f'<section><div class="wrap"><div class="cta"><h2>Not sure where to start?</h2><p>{esc(text)}</p><a class="btn" href="{href}">{esc(button)}</a></div></div></section>'


# ---------- Home A: "Calm doors" ----------
def home_a():
    body = f"""
<section class="hero-a"><div class="wrap">
  <p class="kicker">Education agency in Sydney</p>
  <h1>Study in Australia, your way.</h1>
  <p class="lead">Tell us your visa. We'll show you courses that fit.</p>
  {doors()}
  {trust()}
</div></section>
<section class="band"><div class="wrap">
  <h2>How it works</h2>
  <p class="muted">Three steps. No cost for course advice.</p>
  {steps(STEPS3)}
</div></section>
<section><div class="wrap">
  <h2>New to Australia?</h2>
  <p class="muted">Health cover, a homestay and your first week, in one place.</p>
  <ul class="pick">
    <li><a href="/oshc"><span aria-hidden="true">🩺</span>Compare health cover (OSHC)</a></li>
    <li><a href="/homestay"><span aria-hidden="true">🏡</span>Find a homestay with our partner</a></li>
    <li><a href="/blog"><span aria-hidden="true">📚</span>Read our free plain-English guides</a></li>
  </ul>
</div></section>
{cta("Tell us your visa and what you'd like to study. We reply with options and a written quote.")}
"""
    return shell("Home · option A · We International", body, variant="Home A (calm doors)")


# ---------- Home B: "Ask first" ----------
ANSWERS = [
    ("Working Holiday (417/462)", "You can study for up to 4 months on each visa. A Certificate III in care, health or childcare fits well.",
     "/fast-track-courses", "See Working Holiday courses"),
    ("Student visa (500)", "You need a CRICOS course and health cover (OSHC). We help you compare schools and apply.",
     "/courses", "Explore courses"),
    ("Nursing", "Trained overseas, or planning to study nursing? See how registration works and the prep courses.",
     "/courses/nursing-pathways-australia", "See nursing pathways"),
    ("Something else", "Visitor, graduate, partner or other visa? Your visa decides what you can study. Tell us and we'll check options.",
     "/contact-us", "Tell us your situation"),
]


def home_b():
    radios = ""
    answers = ""
    for i, (label, text, href, btn) in enumerate(ANSWERS, 1):
        chk = " checked" if i == 1 else ""
        radios += f'<input type="radio" name="q" id="q{i}"{chk}><label for="q{i}">{esc(label)}</label>'
        answers += f'<div class="answer" id="a{i}"><p>{esc(text)}</p><a class="btn" href="{href}">{esc(btn)} →</a></div>'
    hero = HOME["heroImage"]
    body = f"""
<section class="hero-b"><div class="wrap split">
  <div>
    <p class="kicker">Hi, we're We International</p>
    <h1>What brings you to Australia?</h1>
    <p class="lead">Pick one. We'll point you to the right page.</p>
    <div class="ask">{radios}{answers}</div>
  </div>
  <figure style="margin:0">{img(hero["file"], hero["alt"])}<figcaption class="muted" style="font-size:13px;margin-top:6px">Maya and Kenji are fictional, AI-generated characters.</figcaption></figure>
</div></section>
<section><div class="wrap">
  <h2>Why students choose us</h2>
  <ul class="proof">
    <li><strong>QEAC</strong><span>Certified counsellor · No. 11964</span></li>
    <li><strong>Free</strong><span>Course advice and a written quote</span></li>
    <li><strong>EN · ไทย</strong><span>Our team replies in English or Thai</span></li>
    <li><strong>{len(list((ROOT / "content/posts").glob("*.md")))} guides</strong><span>Plain-English tips on life in Australia</span></li>
  </ul>
</div></section>
<section class="band"><div class="wrap">
  <h2>From first question to first week</h2>
  {steps(STEPS3)}
  <p style="margin-top:16px"><a class="link" href="/student-services">See everything we help with →</a></p>
</div></section>
{cta("Ask us anything about courses. Visa questions go to a registered migration agent.", "Talk to us")}
"""
    return shell("Home · option B · We International", body, variant="Home B (ask first)")


# ---------- Working Holiday A: one short page, details folded ----------
def course_cards(short=True):
    out = []
    for c in FT["courses"]:
        out.append(f"""<li class="card">{img(c["img"]["file"], c["img"]["alt"])}<div class="in">
<p class="code">{esc(c["code"])}</p><h3>{esc(c["title"].replace("Certificate III in ", "Cert III · "))}</h3>
<p class="muted">{esc(c["for"])}</p><a class="link" href="{c["more"][1]}">Read the guide →</a></div></li>""")
    return '<ul class="cards">' + "".join(out) + "</ul>"


WHV_STEPS = [("Check your visa", "Look up your dates and conditions for free in VEVO."),
             ("Pick a course", "Choose what you enjoy, or ask us to suggest one."),
             ("Get your course plan", "We send the timetable, intake dates and a written quote.")]

GOOD = [
    ("How long can I study?", FT["tip"]),
    ("Where will I live?", "Many students start with a homestay. Our partner, the Australian Homestay Network (AHN), screens hosts. <a href=\"/homestay\">How homestay works →</a>"),
    ("Do I need health cover?", "Home Affairs strongly recommends private health insurance for visitors not covered by Medicare. <a href=\"/oshc\">Compare cover →</a>"),
    ("What do I do in my first week?", "TFN, bank, phone, super and VEVO, step by step. <a href=\"/post/first-week-on-a-working-holiday-visa-a-checklist\">Open the checklist →</a>"),
]


def whv_a():
    body = f"""
<section class="hero-a"><div class="wrap">
  <p class="kicker">Working Holiday visa 417 / 462</p>
  <h1>Turn your Working Holiday into a new skill.</h1>
  <p class="lead">Study a practical Certificate III while you travel.</p>
  <a class="btn" href="#courses">See the 3 courses</a>
</div></section>
<section class="band" id="courses"><div class="wrap">
  <h2>Pick what you enjoy</h2>
  <p class="muted">Each course has a real work placement.</p>
  {course_cards()}
</div></section>
<section><div class="wrap">
  <h2>How it works</h2>
  {steps(WHV_STEPS)}
</div></section>
<section class="band"><div class="wrap">
  <h2>Good to know</h2>
  {faq(GOOD)}
  <p style="margin-top:14px"><a class="link" href="/frequently-asked-questions">More questions in the help centre →</a></p>
</div></section>
{cta("Send us your visa dates and the course you like. We reply with intake dates and a written quote.", "Get my course plan")}
"""
    return shell("Working Holiday · option A · We International", body, variant="Working Holiday A (one short page)")


# ---------- Working Holiday B: tabs + sticky button ----------
def whv_b():
    picks = "".join(f'<li><a href="{h}"><span aria-hidden="true">{i}</span>{esc(t)}</a></li>' for i, t, h in FT["finder"])
    cards = "".join(f"""<li class="card" id="{c["id"]}"><div class="in"><p class="code">{esc(c["code"])}</p><h3>{esc(c["title"])}</h3>
<p class="muted">{esc(c["for"])}</p><a class="link" href="{c["more"][1]}">Read the guide →</a></div></li>""" for c in FT["courses"])
    hero = FT["heroImage"]
    body = f"""
<section class="hero-b" style="padding-bottom:16px"><div class="wrap split">
  <div>
    <p class="kicker">Working Holiday visa 417 / 462</p>
    <h1>Learn a skill on your Working Holiday.</h1>
    <p class="lead">What would you enjoy most?</p>
    <ul class="pick">{picks}</ul>
  </div>
  <figure style="margin:0">{img(hero["file"], hero["alt"])}<figcaption class="muted" style="font-size:13px;margin-top:6px">Maya and Kenji are fictional, AI-generated characters.</figcaption></figure>
</div></section>
<section style="padding-top:0"><div class="wrap tabs">
  <input type="radio" name="t" id="t1" checked><input type="radio" name="t" id="t2"><input type="radio" name="t" id="t3"><input type="radio" name="t" id="t4">
  <div class="tabbar" role="tablist"><label for="t1">Courses</label><label for="t2">How it works</label><label for="t3">Stay &amp; cover</label><label for="t4">Questions</label></div>
  <div class="panel" id="p1"><ul class="cards">{cards}</ul></div>
  <div class="panel" id="p2">{steps(WHV_STEPS)}</div>
  <div class="panel" id="p3"><ul class="pick">
    <li><a href="/homestay"><span aria-hidden="true">🏡</span>Live with a local host (AHN homestay)</a></li>
    <li><a href="/oshc"><span aria-hidden="true">🩺</span>Compare health cover</a></li>
    <li><a href="/post/first-week-on-a-working-holiday-visa-a-checklist"><span aria-hidden="true">✅</span>First-week checklist</a></li></ul></div>
  <div class="panel" id="p4">{faq([(q, a) for q, a in FT["faq"][:4]])}<p><a class="link" href="/frequently-asked-questions">All questions →</a></p></div>
</div></section>
"""
    sticky = '<div class="sticky"><span>Free course plan + quote</span><a class="btn" href="/contact-us">Get my plan</a></div>'
    return shell("Working Holiday · option B · We International", body, variant="Working Holiday B (tabs)", sticky=sticky)


# ---------- Index: how to choose + sitemap ----------
SITEMAP = [
    ("Home", "/", ["1 sentence + 4 doors (Working Holiday · Study · Nursing · Partners)", "3 trust points, 3 steps, 1 button"]),
    ("Working Holiday", "/fast-track-courses", ["3 courses · how it works · good to know (folded) · 1 button",
                                               "Long parts move to: help centre, guides, /homestay, /oshc"]),
    ("Study", "/courses", ["Course finder first (interest / city)", "97 courses + 45 study areas folded below",
                           "Schools → /schools (approved schools only)"]),
    ("Nursing", "/courses/nursing-pathways-australia", ["Registration in 4 steps · prep courses · questions folded"]),
    ("New to Australia", "/student-services", ["Health cover /oshc · Homestay /homestay · English practice", "One question per page"]),
    ("Guides", "/blog", ["38 posts, 6 topics · latest 3 on top"]),
    ("Partners", "/referral-partners", ["Schools & agencies · Migration support (registered agents) · Partner sign-in (GetWec)"]),
    ("About", "/about-we-international", ["Who we are · QEAC 11964 · contact"]),
    ("Help centre", "/frequently-asked-questions", ["All questions in one place (39 now), by topic"]),
]


def index():
    tree = "".join(f'<li><h3><a href="{h}">{esc(t)}</a></h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in xs) + "</ul></li>"
                   for t, h, xs in SITEMAP)
    rows = [("Home page (phone)", "16.8 screens, ~1,370 words", "≈ 4 screens", "≈ 4 screens"),
            ("Working Holiday (phone)", "10.8 screens, ~960 words", "≈ 5 screens", "≈ 3 screens (tabs)"),
            ("Main button", "many per screen", "1 per screen", "1, always at the bottom on phones"),
            ("Long content", "all on the page", "folded (tap to open) + own pages", "tabs + own pages")]
    table = "<table><tr><th></th><th>Now</th><th>Option A</th><th>Option B</th></tr>" + "".join(
        f"<tr><th>{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td></tr>" for a, b, c, d in rows) + "</table>"
    body = f"""
<section><div class="wrap">
  <p class="kicker">For the owner · task WEI-WEB-REDESIGN-1123</p>
  <h1>Two ways to make the site easier to read</h1>
  <p class="lead">Open each one on your phone. Pick A or B (or mix: "home A + Working Holiday B").</p>
  <ul class="choose">
    <li><a href="/redesign/home-a"><h3>Home · A · Calm doors</h3><p class="muted">One sentence, 4 big doors with photos, 3 steps, one button. Quiet and simple.</p></a></li>
    <li><a href="/redesign/home-b"><h3>Home · B · Ask first</h3><p class="muted">"What brings you to Australia?" Tap your visa, get one short answer and one button. Friendlier, with Maya and Kenji.</p></a></li>
    <li><a href="/redesign/working-holiday-a"><h3>Working Holiday · A · One short page</h3><p class="muted">3 course cards, 3 steps, questions folded. Scroll once, done.</p></a></li>
    <li><a href="/redesign/working-holiday-b"><h3>Working Holiday · B · Tabs</h3><p class="muted">Pick what you enjoy, then tabs: Courses · How it works · Stay &amp; cover · Questions. Button stays at the bottom.</p></a></li>
  </ul>
</div></section>
<section class="band"><div class="wrap">
  <h2>Now vs the options</h2>
  {table}
  <p class="muted" style="margin-top:12px">Nothing is deleted: long text moves to its own page or folds away. All 60 old Wix addresses keep working.</p>
</div></section>
<section><div class="wrap">
  <h2>New sitemap</h2>
  <p class="muted">Each page answers one question. The menu has 5 items + "Talk to us".</p>
  <ul class="tree">{tree}</ul>
</div></section>
"""
    return shell("Redesign options · We International", body, variant="index")


PAGES = {"redesign/index.html": index, "redesign/home-a.html": home_a, "redesign/home-b.html": home_b,
         "redesign/working-holiday-a.html": whv_a, "redesign/working-holiday-b.html": whv_b}


def build(write):
    for rel, fn in PAGES.items():
        write(rel, fn())
