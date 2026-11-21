"""/courses — rebuilt on 22 Nov 2026 from the LIVE Wix course catalogue (content/courses.json, 97 courses,
made by tools/courses_from_live.py from the embed's inline data). No script: interest chips jump to a
group, city lists link to courses, each course opens with <details>. Neutral listing — no college names;
we compare colleges with the student. Durations are approximate; nothing is promised.
"""
import html
import json
import re
from pathlib import Path

from home_page import img

ROOT = Path(__file__).resolve().parent
e = html.escape
CD = json.loads((ROOT / "content/courses.json").read_text())
COURSES, TOPICS, IMAGES = CD["courses"], CD["topics"], CD["images"]

GROUP_ORDER = ["Care & Community", "English & Nursing Preparation", "Business & Technology", "Hospitality & Tourism",
               "Trades & Engineering", "Degrees & Research", "Short Courses"]
INTERESTS = [("🤝", "Helping people", "care"), ("🧸", "Working with kids", "child"), ("🩺", "Health & nursing", "nursingprep"),
             ("💼", "Business", "business"), ("🤖", "AI & tech", "ai"), ("🔐", "Cyber security", "cyberlead"),
             ("🍳", "Cooking & food", "cookery"), ("🔨", "Building & trades", "carpentry"), ("🚗", "Cars", "auto-mechanical"),
             ("💬", "English first", "english")]
CITIES = [("🌉", "Sydney", "Biggest city, harbour lifestyle, lots of part-time work options"),
          ("☕", "Melbourne", "Café culture, arts and sport, big student community"),
          ("☀️", "Brisbane", "Sunny, relaxed and close to the beaches"),
          ("🏄", "Gold Coast", "Beach life and a busy hospitality and tourism scene"),
          ("🍷", "Adelaide", "Calm, friendly and easy to get around"),
          ("🏔️", "Hobart", "Small, scenic and close to nature"),
          ("🌾", "Wagga Wagga", "Regional New South Wales"),
          ("💻", "Online", "Start some study online, depending on the course and your visa")]


def slug(s):
    return "c-" + re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def topic_anchor(t):
    return "t-" + re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def course_card(c):
    opts = c.get("options", 0)
    opt_txt = (f"{opts} partner-college options — we compare them with you." if opts > 1
               else "Offered by one of our partner colleges — we confirm the details with you." if opts == 1 else "")
    rows = [("Where", ", ".join(c.get("cities") or [])), ("Length", c.get("duration", "")),
            ("Focus", c.get("focus", "")), ("Campuses", c.get("campuses", ""))]
    dl = "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in rows if v)
    code = f'<span class="code">{e(c["code"])}</span> ' if c.get("code") else ""
    note = f"<p>{e(c['studyNote'])}</p>" if c.get("studyNote") else ""
    opt = f'<p class="small">{e(opt_txt)}</p>' if opt_txt else ""
    return (f'<details class="faq course-item" id="{e(c["id"])}"><summary>{code}'
            f'<strong>{e(c["title"])}</strong> <span class="small">· {e(", ".join(c.get("cities") or []))} · ◷ {e(c.get("duration", ""))}</span></summary>'
            f'<dl>{dl}</dl>{note}{opt}'
            f'<p><a class="btn" href="/charter-application">Ask about this course</a> <a href="/contact-us">Compare colleges with us →</a></p></details>')


def render(study_areas_html, schools_link=""):
    by_topic = {}
    for c in COURSES:
        by_topic.setdefault(c["topic"], []).append(c)
    groups = []
    for g in GROUP_ORDER:
        blocks = []
        for t, info in TOPICS.items():
            if info["group"] != g or t not in by_topic:
                continue
            cs = by_topic[t]
            pic = img(IMAGES.get(info.get("image") or ""), w=1536, h=1024) if not t.startswith("short-") else ""
            facts = "".join(f"<li><strong>{lab}</strong> {e(info[k])}</li>" for lab, k in
                            (("Who it suits:", "suit"), ("Skills:", "skills"), ("Where you can use it:", "use"), ("Jobs it can lead to:", "jobs"))
                            if info.get(k))
            if t.startswith("short-"):
                blocks.append("".join(course_card(c) for c in cs))
            else:
                blocks.append(f'<div class="topic" id="{topic_anchor(t)}">{pic}<p>{e(info.get("about", ""))}</p>'
                              f'<ul class="list">{facts}</ul>{"".join(course_card(c) for c in cs)}</div>')
        n = sum(len(by_topic[t]) for t, i in TOPICS.items() if i["group"] == g and t in by_topic)
        if n:
            intro = ('<p>Single-unit workplace skills courses, such as first aid and safety tickets. '
                     'Ask our team about entry requirements and the next class.</p>' if g == "Short Courses" else "")
            groups.append(f'<section class="wrap narrow"><h2 id="{slug(g)}">{e(g)} <span class="small">({n} courses)</span></h2>{intro}{"".join(blocks)}</section>')
    chips = "".join(f'<li><a href="#{topic_anchor(t)}"><span class="ico" aria-hidden="true">{i}</span>{e(lab)}</a></li>'
                    for i, lab, t in INTERESTS if t in by_topic)
    group_nav = " · ".join(f'<a href="#{slug(g)}">{e(g)}</a>' for g in GROUP_ORDER)
    cities = []
    for ico, city, blurb in CITIES:
        cs = [c for c in COURSES if city in (c.get("cities") or [])]
        if not cs:
            continue
        links = "".join(f'<li><a href="#{e(c["id"])}">{e(c["title"])}</a></li>' for c in cs)
        cities.append(f'<details class="faq"><summary><span aria-hidden="true">{ico}</span> <strong>{e(city)}</strong> '
                      f'<span class="small">· {len(cs)} courses · {e(blurb)}</span></summary><ul class="list">{links}</ul></details>')
    total = len(COURSES)
    return f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">Explore your next chapter</p>
<h1>Find a course. Picture your future.</h1>
<p class="lead">Explore what you will learn, who each course suits and where it could take you. Start with your interests — we will help with the details.</p>
<ul class="points"><li><span aria-hidden="true">📚</span>{total} courses to explore</li><li><span aria-hidden="true">🎓</span>Certificates to postgraduate study</li></ul>
<p class="actions"><a class="btn" href="#interests">Find my course ↓</a> <a class="btn ghost" href="#{slug("Degrees & Research")}">Explore degrees</a></p>
</div></section>
<section class="wrap" id="interests">
<p class="kicker">Two ways to start</p>
<h2>Not sure what to study yet?</h2>
<p class="bubble"><strong>Maya:</strong> Tap what you enjoy. I'll take you to matching courses.</p>
<ul class="finder">{chips}</ul>
<h2>Already have a course in mind?</h2>
<p class="bubble alt"><strong>Kenji:</strong> Jump to its study area below, or tell us the course name or code and we'll compare colleges for you.</p>
<p>{group_nav}</p>
<p><a class="btn ghost" href="/contact-us">Ask us to compare colleges for you →</a></p>
</section>
<section class="wrap narrow" id="cities">
<p class="kicker">Pick a city</p>
<h2>Each city feels different</h2>
<p>Open a city to see the courses there.</p>
{"".join(cities)}
<aside class="tip"><strong>Wally's tip</strong> Rent and living costs change a lot between cities. Ask us for a simple cost check before you choose.</aside>
</section>
{"".join(groups)}
<section class="wrap narrow">
<p class="note-box"><strong>About this list.</strong> Durations are approximate and depend on your study plan, credit and delivery mode.
We confirm the college, campus, intake, fees and full schedule with you before you apply. No place, visa or job is promised.</p>
<aside class="cta"><p>Already qualified as a nurse overseas?</p><span class="small">Explore English, NCLEX-RN and OSCE preparation and understand your next step.</span><br>
<a class="btn" href="/courses/nursing-pathways-australia">Explore nursing pathways →</a></aside>
{schools_link}
</section>
{study_areas_html}"""
