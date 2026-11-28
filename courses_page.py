"""/courses — rebuilt on 22 Nov 2026 from the LIVE Wix course catalogue (content/courses.json, 97 courses,
made by tools/courses_from_live.py from the embed's inline data). Interest chips jump to a topic, city lists
link to courses, each study-area group and each course opens with <details> (27 Nov 2026: 49 → ~10 phone
screens; assets/reveal.js opens the folds round a #link where the browser does not do it itself). Neutral listing — no college names;
we compare colleges with the student. Durations are approximate; nothing is promised.
render(..., th=True) builds /th/courses from the same catalogue with the Thai words in content/th/courses.json
(22 Nov 2026): same groups, topics, courses and anchors; course titles and codes stay English (lang="en").
"""
import html
import json
import re
from pathlib import Path

from group_pages import icon
from home_page import img

ROOT = Path(__file__).resolve().parent
e = html.escape
CD = json.loads((ROOT / "content/courses.json").read_text())
COURSES, TOPICS, IMAGES = CD["courses"], CD["topics"], CD["images"]
TH = json.loads((ROOT / "content/th/courses.json").read_text())


def th_missing():
    """English values in content/courses.json that have no Thai words in content/th/courses.json."""
    miss = [f"group:{g}" for g in GROUP_ORDER if g not in TH["groups"]]
    miss += [f"topic:{t}.{k}" for t, i in TOPICS.items() for k in ("about", "suit", "skills", "use", "jobs")
             if i.get(k) and not TH["topics"].get(t, {}).get(k)]
    miss += [f"{k}:{c[k]}" for c in COURSES for k in ("focus", "duration", "studyNote", "campuses")
             if c.get(k) and c[k] not in TH[k]]
    miss += [f"city:{x}" for c in COURSES for x in c.get("cities") or [] if x not in TH["city_names"]]
    miss += [f"interest:{t}" for _, _, t in INTERESTS if t not in TH["interests"]]
    return sorted(set(miss))

GROUP_ORDER = ["Care & Community", "English & Nursing Preparation", "Business & Technology", "Hospitality & Tourism",
               "Trades & Engineering", "Degrees & Research", "Short Courses"]
INTERESTS = [("care", "Helping people", "care"), ("blocks", "Working with kids", "child"), ("hospital", "Health & nursing", "nursingprep"),
             ("work", "Business", "business"), ("chip", "AI & tech", "ai"), ("lock", "Cyber security", "cyberlead"),
             ("meal", "Cooking & food", "cookery"), ("tool", "Building & trades", "carpentry"), ("car", "Cars", "auto-mechanical"),
             ("talk", "English first", "english")]
CITIES = [("pin", "Sydney", "Biggest city, harbour lifestyle, lots of part-time work options"),
          ("pin", "Melbourne", "Café culture, arts and sport, big student community"),
          ("pin", "Brisbane", "Sunny, relaxed and close to the beaches"),
          ("pin", "Gold Coast", "Beach life and a busy hospitality and tourism scene"),
          ("pin", "Adelaide", "Calm, friendly and easy to get around"),
          ("pin", "Hobart", "Small, scenic and close to nature"),
          ("pin", "Wagga Wagga", "Regional New South Wales"),
          ("laptop", "Online", "Start some study online, depending on the course and your visa")]


def slug(s):
    return "c-" + re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def topic_anchor(t):
    return "t-" + re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def course_card(c, th=False):
    U = TH["ui"]
    tr = (lambda k: TH[k].get(c.get(k, ""), "")) if th else (lambda k: c.get(k, ""))
    cities = [TH["city_names"][x] for x in c.get("cities") or []] if th else (c.get("cities") or [])
    opts = c.get("options", 0)
    if th:
        opt_txt = U["opts_many"].format(n=opts) if opts > 1 else U["opts_one"] if opts == 1 else ""
        labels = (U["where"], U["length"], U["focus"], U["campuses"])
    else:
        opt_txt = (f"{opts} partner-college options — we compare them with you." if opts > 1
                   else "Offered by one of our partner colleges — we confirm the details with you." if opts == 1 else "")
        labels = ("Where", "Length", "Focus", "Campuses")
    rows = zip(labels, (", ".join(cities), tr("duration"), tr("focus"), tr("campuses")))
    dl = "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in rows if v)
    la = ' lang="en"' if th else ""
    code = f'<span class="code"{la}>{e(c["code"])}</span> ' if c.get("code") else ""
    note = f"<p>{e(tr('studyNote'))}</p>" if c.get("studyNote") else ""
    opt = f'<p class="small">{e(opt_txt)}</p>' if opt_txt else ""
    pre = "/th" if th else ""
    ask, comp = (U["ask_btn"], U["compare_link"]) if th else ("Ask about this course", "Compare colleges with us →")
    return (f'<details class="faq course-item" id="{e(c["id"])}"><summary>{code}'
            f'<strong{la}>{e(c["title"])}</strong> <span class="small">· {e(", ".join(cities))} · ◷ {e(tr("duration"))}</span></summary>'
            f'<dl>{dl}</dl>{note}{opt}'
            f'<p><a class="btn" href="{pre}/charter-application">{e(ask)}</a> <a href="{pre}/contact-us">{e(comp)}</a></p></details>')


def render(study_areas_html, schools_link="", th=False):
    U = TH["ui"]
    pre = "/th" if th else ""
    G = (lambda g: TH["groups"][g]) if th else (lambda g: g)
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
            ti = TH["topics"][t] if th else info
            pic = (f'<div class="wide-only">{img(IMAGES.get(info.get("image") or ""), w=1536, h=1024)}</div>'
                   if not t.startswith("short-") else "")  # the topic picture adds nothing on a phone (readability 27 Nov 2026)
            labs = ((U["suit"], "suit"), (U["skills"], "skills"), (U["use"], "use"), (U["jobs"], "jobs")) if th else \
                (("Who it suits:", "suit"), ("Skills:", "skills"), ("Where you can use it:", "use"), ("Jobs it can lead to:", "jobs"))
            facts = "".join(f"<li><strong>{lab}</strong> {e(ti[k])}</li>" for lab, k in labs if info.get(k))
            if t.startswith("short-"):
                blocks.append("".join(course_card(c, th) for c in cs))
            else:
                blocks.append(f'<div class="topic" id="{topic_anchor(t)}">{pic}<p>{e(ti.get("about", ""))}</p>'
                              f'<ul class="list">{facts}</ul>{"".join(course_card(c, th) for c in cs)}</div>')
        n = sum(len(by_topic[t]) for t, i in TOPICS.items() if i["group"] == g and t in by_topic)
        if n:
            if g == "Short Courses":
                intro = f"<p>{U['short_intro']}</p>" if th else ('<p>Single-unit workplace skills courses, such as first aid and safety tickets. '
                                                                'Ask our team about entry requirements and the next class.</p>')
            else:
                intro = ""
            cnt = U["n_courses"].format(n=n) if th else f"{n} courses"
            groups.append(f'<section class="wrap narrow group-wrap"><details class="group-fold"><summary><h2 id="{slug(g)}">{e(G(g))} '
                          f'<span class="small">({cnt})</span></h2></summary>{intro}{"".join(blocks)}</details></section>')
    chips = "".join(f'<li><a href="#{topic_anchor(t)}">{icon(i)}{e(TH["interests"][t] if th else lab)}</a></li>'
                    for i, lab, t in INTERESTS if t in by_topic)
    group_nav = " · ".join(f'<a href="#{slug(g)}">{e(G(g))}</a>' for g in GROUP_ORDER)
    cities = []
    for ico, city, blurb in CITIES:
        cs = [c for c in COURSES if city in (c.get("cities") or [])]
        if not cs:
            continue
        la = ' lang="en"' if th else ""
        links = "".join(f'<li><a href="#{e(c["id"])}"{la}>{e(c["title"])}</a></li>' for c in cs)
        name, bl, cnt = (TH["city_names"][city], TH["cities"][city], U["n_courses"].format(n=len(cs))) if th else (city, blurb, f"{len(cs)} courses")
        cities.append(f'<details class="faq"><summary>{icon(ico)} <strong>{e(name)}</strong> '
                      f'<span class="small">· {cnt} · {e(bl)}</span></summary><ul class="list">{links}</ul></details>')
    total = len(COURSES)
    if th:
        top = f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">{U["kicker"]}</p>
<h1>{U["h1"]}</h1>
<p class="lead">{U["lead"]}</p>
<ul class="points"><li>{icon("book")}{U["points_total"].format(n=total)}</li><li>{icon("cap")}{U["points_levels"]}</li></ul>
<p class="actions"><a class="btn" href="#interests">{U["find_btn"]}</a> <a class="btn ghost" href="#{slug("Degrees & Research")}">{U["degrees_btn"]}</a></p>
</div></section>
<section class="wrap" id="interests">
<p class="kicker">{U["two_ways"]}</p>
<h2>{U["not_sure"]}</h2>
<p class="bubble">{U["maya"]}</p>
<ul class="finder">{chips}</ul>
<h2>{U["in_mind"]}</h2>
<p class="bubble alt">{U["kenji"]}</p>
<p>{group_nav}</p>
<p><a class="btn ghost" href="/th/contact-us">{U["compare_btn"]}</a></p>
</section>
<section class="wrap narrow" id="cities">
<p class="kicker">{U["pick_city"]}</p>
<h2>{U["cities_h2"]}</h2>
<p>{U["cities_p"]}</p>
{"".join(cities)}
<div class="tip">{U["wally"]}</div>
</section>"""
        bottom = f"""<p class="note-box">{U["about_list"]}</p>
<div class="cta"><p>{U["nurse_q"]}</p><span class="small">{U["nurse_p"]}</span><br>
<a class="btn" href="/th/courses/nursing-pathways-australia">{U["nurse_btn"]}</a></div>"""
    else:
        top = f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">Explore your next chapter</p>
<h1>Find a course. Picture your future.</h1>
<p class="lead">Explore what you will learn, who each course suits and where it could take you. Start with your interests — we will help with the details.</p>
<ul class="points"><li>{icon("book")}{total} courses to explore</li><li>{icon("cap")}Certificates to postgraduate study</li></ul>
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
<div class="tip"><strong>Wally's tip</strong> Rent and living costs change a lot between cities. Ask us for a simple cost check before you choose.</div>
</section>"""
        bottom = """<p class="note-box"><strong>About this list.</strong> Durations are approximate and depend on your study plan, credit and delivery mode.
We confirm the college, campus, intake, fees and full schedule with you before you apply. No place, visa or job is promised.</p>
<div class="cta"><p>Already qualified as a nurse overseas?</p><span class="small">Explore English, NCLEX-RN and OSCE preparation and understand your next step.</span><br>
<a class="btn" href="/courses/nursing-pathways-australia">Explore nursing pathways →</a></div>"""
    return f"""{top}
{"".join(groups)}
<section class="wrap narrow">
{bottom}
{schools_link}
</section>
{study_areas_html}
<script src="/assets/reveal.js" defer></script>"""
