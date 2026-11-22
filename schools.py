"""School pages (/schools and /schools/<slug>) — WEI-SCHOOL-BACKLOG-1120 step 4.

Owner rule (20 Nov 2026): promote only schools that replied to us, and only with what they sent us
(fee list, course list, marketing material). Add a school = add one object to content/schools.json.
"approved": false keeps a school on the preview only; the production build leaves it out until the
owner approves. No logos or photos unless the school gave them to us. No owner names.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
e = html.escape
PRODUCTION = "--production" in sys.argv

ALL = json.loads((ROOT / "content/schools.json").read_text())["schools"]
SCHOOLS = [s for s in ALL if s.get("approved") or not PRODUCTION]

NOTE = ("<p class=\"note-box\"><strong>About these details.</strong> They come from the school's own files. "
        "Fees and dates can change, so the school confirms the final fee and start date in your offer letter. "
        "Visa questions go to a registered migration agent.</p>")


def money(n):
    return f"A${n:,}"


def facts(s):
    rows = [("Campuses", " · ".join(e(c) for c in s["campuses"])), ("Intakes", e(s.get("intakes") or "")),
            ("CRICOS provider", e(s["cricos"])), ("RTO", e(s.get("rto") or "")),
            ("Courses", str(len(s["courses"])) if s["courses"] else "")]
    return "<dl>" + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows if v) + "</dl>"


def card(s):
    return (f'<li class="agent school"><h3>{e(s["name"])}</h3><p>{e(s["summary"])}</p>{facts(s)}'
            f'<a class="btn" href="/schools/{e(s["slug"])}">{"Courses and fees" if s["courses"] else "School details"}</a></li>')


def fee_table(s):
    if not s["courses"]:
        return ""
    cols = s["fee_columns"]
    head = "".join(f'<th scope="col">{e(c)}</th>' for c in cols)
    body = "".join(
        f'<tr><th scope="row">{e(c["name"])}<span>{e(c["code"])}{" · CRICOS " + e(c["cricos"]) if c.get("cricos") else ""}</span></th>'
        f'<td data-col="Length">{c["weeks"]} weeks</td>'
        + "".join(f'<td data-col="{e(col)}">{money(c["fees"][col]) if c["fees"].get(col) else "Ask us"}</td>' for col in cols) + "</tr>"
        for c in s["courses"])
    return (f'<div class="fees"><table><caption>{e(s["source"]["year"])} course fees (AUD)</caption>'
            f'<thead><tr><th scope="col">Course</th><th scope="col">Length</th>{head}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def detail(s):
    src = s["source"]
    return f"""<section class="wrap narrow"><p class="small"><a href="/schools">All schools</a></p>
<h1>{e(s["name"])}</h1><p class="lead">{e(s["summary"])}</p>
<div class="agent">{facts(s)}</div>
<h2>Courses and fees</h2>{fee_table(s)}<p>{e(s["fee_note"])}</p>
<p class="small">Source: {e(src["file"])}, sent to us by the school ({e(src["received"])}).
School website: <a href="{e(s["website"])}" target="_blank" rel="noopener">{e(s["website"].split("//")[1])}</a></p>
{NOTE}<aside class="cta"><p>Want to study at {e(s["name"])}? Tell us the course, campus and when you want to start.</p>
<a class="btn" href="/charter-application">Apply to study</a> <a class="btn ghost" href="/contact-us">Ask a question</a></aside></section>"""


index_body = f"""<section class="wrap narrow"><h1>Schools</h1>
<p class="lead">Schools that work with students like you. Each page shows the courses, campuses and fees the school sent us.</p>
{"<ul class='agents'>" + "".join(card(s) for s in SCHOOLS) + "</ul>" if SCHOOLS else
 '<p class="note-box"><strong>Coming soon.</strong> Until then, <a href="/contact-us">ask us about schools</a>.</p>'}
<p>Looking for something else? See all <a href="/courses">study areas</a>.</p>{NOTE}</section>"""

PAGES = {} if not SCHOOLS else {"schools": ("Schools and fees | We International",
                     "Courses, campuses and fees from schools in Australia, sent to us by each school. Ask We International to help you apply.",
                     index_body)}
for s in SCHOOLS:  # empty in production until the owner approves a school
    PAGES[f"schools/{s['slug']}"] = (
        f"{s['name']} courses and fees | We International",
        f"{s['name']}: campuses, intakes and course fees from the school's own files. Ask We International to help you apply.",
        detail(s))
