"""Working Holiday schools: /working-holiday/charter and /working-holiday/kca (WEI-WHV-CHARTER-1125).

Owner 25 Nov 2026: help Working Holiday Makers (417/462) enrol with us, then we send the application
to Charter Australia; KCA Education is the second option. Facts come only from the schools' own files
(content/working-holiday.json). One button: "Enrol with us" → a short form that goes to GetWec
(form kind "whv_enrol"). No commission figures, no visa advice (→ registered migration agent),
no passport or visa grant numbers on the form.
"""
import html
import json
from pathlib import Path

from pages import CONSENT, VISA_NOTE

ROOT = Path(__file__).resolve().parent
e = html.escape
DATA = json.loads((ROOT / "content/working-holiday.json").read_text())["schools"]
BY = {s["slug"]: s for s in DATA}
OPTIONS = [o for s in DATA for o in s["options"]]

RULE = ("Home Affairs says Working Holiday Makers can study or train for up to 4 months on each visa "
        "(condition 8548). Check your own conditions in "
        '<a href="https://immi.homeaffairs.gov.au/visas/already-have-a-visa/check-visa-details-and-conditions/check-conditions-online" '
        'target="_blank" rel="noopener">VEVO ↗</a> before you pick a start date.')


def form(slug):
    own = BY[slug]["options"]  # this school's courses first, then the other school's
    opts = "".join(f"<option>{e(o)}</option>" for o in own + [o for o in OPTIONS if o not in own])
    return f"""<form class="lead" data-lead-form="whv_enrol" novalidate>
<h2>Enrol with us</h2>
<div class="field"><label for="w-name">Full name *</label>
  <input id="w-name" name="full_name" autocomplete="name" required maxlength="120"><span class="err" data-err="full_name"></span></div>
<div class="field"><label for="w-email">Email *</label>
  <input id="w-email" name="email" type="email" autocomplete="email" required maxlength="200"><span class="err" data-err="email"></span></div>
<div class="row2">
  <div class="field"><label for="w-visa">Your visa</label>
    <select id="w-visa" name="visa" data-summary="Visa"><option value="">Choose…</option>
    <option>Working Holiday 417</option><option>Work and Holiday 462</option><option>Other visa</option></select></div>
  <div class="field"><label for="w-end">When does your visa end?</label>
    <input id="w-end" name="visa_end" type="month" data-summary="Visa ends"></div>
</div>
<div class="field"><label for="w-course">Course you like</label>
  <select id="w-course" name="course" data-summary="Course">{opts}<option>Not sure yet</option></select></div>
<div class="field"><label for="w-msg">Anything else? (optional)</label>
  <textarea id="w-msg" name="message" rows="3" maxlength="800"></textarea></div>
<input type="hidden" name="location" value="australia">
<p class="hint">Please don't send passport numbers, visa grant numbers or bank details here.</p>
{CONSENT}
<button class="btn" type="submit">Enrol with us</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>"""


def fee_table(s):
    head = "".join(f'<th scope="col">{e(h)}</th>' for h in s["fee_head"])
    rows = "".join("<tr>" + f'<th scope="row">{e(r[0])}</th>'
                   + "".join(f'<td data-col="{e(h)}">{e(v)}</td>' for h, v in zip(s["fee_head"][1:], r[1:])) + "</tr>"
                   for r in s["fees"])
    return (f'<div class="fees"><table><caption>Fees in AUD</caption><thead><tr>{head}</tr></thead>'
            f"<tbody>{rows}</tbody></table></div>")


def other(slug):
    o = next(s for s in DATA if s["slug"] != slug)
    return (f'<li class="path"><h3>{e(o["name"])}</h3><p>{e(o["summary"])}</p>'
            f'<a href="/working-holiday/{o["slug"]}">See {e(o["name"])} →</a></li>')


def detail(s):
    pts = "".join(f"<li>{e(p)}</li>" for p in s["points"])
    notes = "".join(f"<li>{e(n)}</li>" for n in s["fee_notes"])
    warn = f'<p class="note-box"><strong>Check your study time.</strong> {e(s["warn"])}</p>' if s.get("warn") else ""
    return f"""<section class="wrap narrow">
<p class="small"><a href="/fast-track-courses">Working Holiday courses</a></p>
<p class="kicker">Working Holiday visa 417 / 462</p>
<h1>Study at {e(s["name"])} on your Working Holiday</h1>
<p class="lead">{e(s["summary"])}</p>
<p class="actions"><a class="btn" href="#enrol">Enrol with us ↓</a></p>
<h2>What you get</h2>
<ul class="list">{pts}</ul>
<p class="small">Where: {e(s["city"])}. {e(s["legal"])} · RTO {e(s["rto"])} · CRICOS {e(s["cricos"])} ·
<a href="{e(s["website"])}" target="_blank" rel="noopener">{e(s["website"].split("//")[1])} ↗</a></p>
<h2>Courses and fees</h2>
{fee_table(s)}
<ul class="list">{notes}</ul>
<p class="small">Source: {e(s["source"])}</p>
<h2>Your study time</h2>
<p>{RULE}</p>
{warn}
<h2>How enrolling with us works</h2>
<ol class="steps"><li>Send the form below.</li><li>We email you the next start dates and a written quote from {e(s["name"])}.</li>
<li>You choose, and we send your application to {e(s["name"])} for you.</li><li>{e(s["name"])} sends your offer letter.</li></ol>
{VISA_NOTE}
</section>
<section class="wrap narrow" id="enrol">
{form(s["slug"])}
<p class="small">We are an education agency (QEAC No. 11964). We do not promise a place, a job or a visa.</p>
</section>
<section class="wrap"><h2>Another option</h2><ul class="paths">{other(s["slug"])}</ul></section>"""


TH_SUMMARY = {
    "charter": "คอร์ส Certificate III สายดูแลผู้สูงอายุ ผู้ช่วยในโรงพยาบาล และดูแลเด็ก ในโปรแกรม Study and Work ของ Charter สำหรับวีซ่า 417/462 พร้อมฝึกงานที่ Charter จัดให้",
    "kca": "คอร์สดูแลผู้สูงอายุและผู้พิการ 16 สัปดาห์ (เรียน 12 + ฝึกงาน 4 สัปดาห์) ที่บริสเบนหรือเรียนออนไลน์",
}


def strip_html(th=False):
    """Section near the top of /fast-track-courses: the two schools, Charter first.
    The school pages are English only for now; the Thai page links to them with lang="en"."""
    if th:
        k, h2, p, link = ("สมัครกับเรา", "2 โรงเรียนสำหรับคนถือวีซ่า Working Holiday",
                          "ดูคอร์สและค่าเรียนจากไฟล์ที่โรงเรียนส่งให้เรา แล้วสมัครกับเรา เราส่งใบสมัครไปที่โรงเรียนให้ (หน้าโรงเรียนเป็นภาษาอังกฤษ)",
                          "ดูคอร์ส ค่าเรียน และสมัคร →")
    else:
        k, h2, p, link = ("Enrol with us", "Two schools for Working Holiday Makers",
                          "See the courses and fees each school sent us, then enrol with us. We send your application to the school.",
                          "Courses, fees and enrol →")
    cards = "".join(f'<li class="path"><h3 lang="en">{e(s["name"])}</h3><p>{e(TH_SUMMARY[s["slug"]] if th else s["summary"])}</p>'
                    f'<a href="/working-holiday/{s["slug"]}"{' hreflang="en"' if th else ''}>{link}</a></li>' for s in DATA)
    return f"""<section class="wrap" id="schools">
<p class="kicker">{k}</p>
<h2>{h2}</h2>
<p>{p}</p>
<ul class="paths">{cards}</ul>
</section>"""


PAGES = {
    f"working-holiday/{s['slug']}": (
        f"{s['name']} for Working Holiday | We International",
        f"{s['name']} courses and fees for Working Holiday Makers (417/462), from the school's own files. Enrol with We International.",
        detail(s))
    for s in DATA
}
