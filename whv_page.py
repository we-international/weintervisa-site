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

# Page words. The Thai page (/th/working-holiday/<slug>, 26 Nov 2026) passes UI_TH + content/th/working-holiday.json.
UI_EN = {
    "pre": "", "en": "", "back": "Working Holiday courses", "kicker": "Working Holiday visa 417 / 462",
    "h1": "Study at {name} on your Working Holiday", "enrol_btn": "Enrol with us ↓", "get": "What you get",
    "where": "Where", "fees_h": "Courses and fees", "caption": "Fees in AUD", "source": "Source",
    "time_h": "Your study time", "rule": RULE, "warn_b": "Check your study time.", "how_h": "How enrolling with us works",
    "steps": ["Send the form below.", "We email you the next start dates and a written quote from {name}.",
              "You choose, and we send your application to {name} for you.", "{name} sends your offer letter."],
    "visa_note": VISA_NOTE, "qeac": "We are an education agency (QEAC No. 11964). We do not promise a place, a job or a visa.",
    "other_h": "Another option", "see": "See {name} →",
    "f_h": "Enrol with us", "f_name": "Full name *", "f_email": "Email *", "f_visa": "Your visa", "f_choose": "Choose…",
    "f_visas": ["Working Holiday 417", "Work and Holiday 462", "Other visa"], "f_end": "When does your visa end?",
    "f_course": "Course you like", "f_unsure": "Not sure yet", "f_msg": "Anything else? (optional)",
    "f_hint": "Please don't send passport numbers, visa grant numbers or bank details here.", "consent": CONSENT,
    "f_btn": "Enrol with us", "en_cols": [],
}


def opt(value, label):
    # The value stays English ("Charter: CHC33021 …"): GetWec reads the school and course code from it.
    return f"<option>{e(value)}</option>" if value == label else f'<option value="{e(value)}">{e(label)}</option>'


def form(slug, L=UI_EN, labels=None):
    labels = labels or {}
    own = BY[slug]["options"]  # this school's courses first, then the other school's
    opts = "".join(opt(o, labels.get(o, o)) for o in own + [o for o in OPTIONS if o not in own])
    visas = "".join(opt(v, l) for v, l in zip(UI_EN["f_visas"], L["f_visas"]))
    return f"""<form class="lead" data-lead-form="whv_enrol" novalidate>
<h2>{L["f_h"]}</h2>
<div class="field"><label for="w-name">{L["f_name"]}</label>
  <input id="w-name" name="full_name" autocomplete="name" required maxlength="120"><span class="err" data-err="full_name"></span></div>
<div class="field"><label for="w-email">{L["f_email"]}</label>
  <input id="w-email" name="email" type="email" autocomplete="email" required maxlength="200"><span class="err" data-err="email"></span></div>
<div class="row2">
  <div class="field"><label for="w-visa">{L["f_visa"]}</label>
    <select id="w-visa" name="visa" data-summary="Visa"><option value="">{L["f_choose"]}</option>
    {visas}</select></div>
  <div class="field"><label for="w-end">{L["f_end"]}</label>
    <input id="w-end" name="visa_end" type="month" data-summary="Visa ends"></div>
</div>
<div class="field"><label for="w-course">{L["f_course"]}</label>
  <select id="w-course" name="course" data-summary="Course">{opts}{opt("Not sure yet", L["f_unsure"])}</select></div>
<div class="field"><label for="w-msg">{L["f_msg"]}</label>
  <textarea id="w-msg" name="message" rows="3" maxlength="800"></textarea></div>
<input type="hidden" name="location" value="australia">
<p class="hint">{L["f_hint"]}</p>
{L["consent"]}
<button class="btn" type="submit">{L["f_btn"]}</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>"""


def fee_table(s, L=UI_EN):
    en = set(L["en_cols"])  # columns that stay English (course titles) on the Thai page
    head = "".join(f'<th scope="col">{e(h)}</th>' for h in s["fee_head"])
    rows = "".join("<tr>" + f'<th scope="row">{e(r[0])}</th>'
                   + "".join(f'<td data-col="{e(h)}"{' lang="en"' if i in en else ''}>{e(v)}</td>'
                             for i, (h, v) in enumerate(zip(s["fee_head"][1:], r[1:]), 1)) + "</tr>"
                   for r in s["fees"])
    return (f'<div class="fees"><table><caption>{L["caption"]}</caption><thead><tr>{head}</tr></thead>'
            f"<tbody>{rows}</tbody></table></div>")


def other(slug, L=UI_EN, data=None):
    o = next(x for x in (data or DATA) if x["slug"] != slug)
    return (f'<li class="path"><h3{L["en"]}>{e(o["name"])}</h3><p>{e(o["summary"])}</p>'
            f'<a href="{L["pre"]}/working-holiday/{o["slug"]}">{e(L["see"].format(name=o["name"]))}</a></li>')


def detail(s, L=UI_EN, data=None):
    n = s["name"]
    pts = "".join(f"<li>{e(p)}</li>" for p in s["points"])
    notes = "".join(f"<li>{e(x)}</li>" for x in s["fee_notes"])
    warn = f'<p class="note-box"><strong>{L["warn_b"]}</strong> {e(s["warn"])}</p>' if s.get("warn") else ""
    steps = "".join(f"<li>{e(x.format(name=n))}</li>" for x in L["steps"])
    sep = ": " if not L["pre"] else " "
    legal = f'{e(s["legal"])} · RTO {e(s["rto"])} · CRICOS {e(s["cricos"])}'
    if L["en"]:
        legal = f'<span lang="en">{legal}</span>'
    return f"""<section class="wrap narrow">
<p class="small"><a href="{L["pre"]}/fast-track-courses">{L["back"]}</a></p>
<p class="kicker">{L["kicker"]}</p>
<h1>{e(L["h1"].format(name=n))}</h1>
<p class="lead">{e(s["summary"])}</p>
<p class="actions"><a class="btn" href="#enrol">{L["enrol_btn"]}</a></p>
<h2>{L["get"]}</h2>
<ul class="list">{pts}</ul>
<p class="small">{L["where"]}{sep}{e(s["city"])}. {legal} ·
<a href="{e(s["website"])}" target="_blank" rel="noopener">{e(s["website"].split("//")[1])} ↗</a></p>
<h2>{L["fees_h"]}</h2>
{fee_table(s, L)}
<ul class="list">{notes}</ul>
<p class="small">{L["source"]}{sep}{e(s["source"])}</p>
<h2>{L["time_h"]}</h2>
<p>{L["rule"]}</p>
{warn}
<h2>{L["how_h"]}</h2>
<ol class="steps">{steps}</ol>
{L["visa_note"]}
</section>
<section class="wrap narrow" id="enrol">
{form(s["slug"], L, s.get("option_labels"))}
<p class="small">{L["qeac"]}</p>
</section>
<section class="wrap"><h2>{L["other_h"]}</h2><ul class="paths">{other(s["slug"], L, data)}</ul></section>"""


TH_DATA = json.loads((ROOT / "content/th/working-holiday.json").read_text())["schools"]
TH_SUMMARY = {s["slug"]: s["summary"] for s in TH_DATA}


def strip_html(th=False):
    """Section near the top of /fast-track-courses: the two schools, Charter first.
    The Thai page links to the Thai school pages (/th/working-holiday/<slug>, 26 Nov 2026)."""
    if th:
        k, h2, p, link = ("สมัครกับเรา", "2 โรงเรียนสำหรับคนถือวีซ่า Working Holiday",
                          "ดูคอร์สและค่าเรียนจากไฟล์ที่โรงเรียนส่งให้เรา แล้วสมัครกับเรา เราส่งใบสมัครไปที่โรงเรียนให้",
                          "ดูคอร์ส ค่าเรียน และสมัคร →")
        more = "อยู่ออสเตรเลียแล้วด้วยวีซ่าอื่น? เรียนคู่กับวีซ่าที่มีอยู่ →"
    else:
        k, h2, p, link = ("Enrol with us", "Two schools for Working Holiday Makers",
                          "See the courses and fees each school sent us, then enrol with us. We send your application to the school.",
                          "Courses, fees and enrol →")
        more = "Already in Australia on another visa? Study alongside your visa →"
    cards = "".join(f'<li class="path"><h3 lang="en">{e(s["name"])}</h3><p>{e(TH_SUMMARY[s["slug"]] if th else s["summary"])}</p>'
                    f'<a href="{"/th" if th else ""}/working-holiday/{s["slug"]}">{link}</a></li>' for s in DATA)
    return f"""<section class="wrap" id="schools">
<p class="kicker">{k}</p>
<h2>{h2}</h2>
<p>{p}</p>
<ul class="paths">{cards}</ul>
<p><a href="{"/th" if th else ""}/already-in-australia">{more}</a></p>
</section>"""


PAGES = {
    f"working-holiday/{s['slug']}": (
        f"{s['name']} for Working Holiday | We International",
        f"{s['name']} courses and fees for Working Holiday Makers (417/462), from the school's own files. Enrol with We International.",
        detail(s))
    for s in DATA
}


# Thai pages (26 Nov 2026): same facts from content/th/working-holiday.json (test: same shape as the English JSON).
UI_TH = {**UI_EN,
    "pre": "/th", "en": ' lang="en"', "back": "คอร์สสำหรับ Working Holiday", "kicker": "วีซ่า Working Holiday 417 / 462",
    "h1": "เรียนที่ {name} ระหว่าง Working Holiday", "enrol_btn": "สมัครกับเรา ↓", "get": "สิ่งที่คุณได้",
    "where": "ที่เรียน:", "fees_h": "คอร์สและค่าเรียน", "caption": "ค่าเรียนเป็นเหรียญออสเตรเลีย (AUD)", "source": "ที่มา:",
    "time_h": "ระยะเวลาเรียนของคุณ",
    "rule": ("กระทรวงมหาดไทยออสเตรเลีย (Home Affairs) ระบุว่าผู้ถือวีซ่า Working Holiday เรียนหรือฝึกอบรมได้ไม่เกิน 4 เดือนต่อวีซ่าหนึ่งใบ "
             "(เงื่อนไข 8548) เช็กเงื่อนไขของคุณเองใน "
             '<a href="https://immi.homeaffairs.gov.au/visas/already-have-a-visa/check-visa-details-and-conditions/check-conditions-online" '
             'target="_blank" rel="noopener">VEVO ↗</a> ก่อนเลือกวันเริ่มเรียน'),
    "warn_b": "เช็กระยะเวลาเรียน", "how_h": "ขั้นตอนสมัครกับเรา",
    "steps": ["ส่งฟอร์มด้านล่าง", "เราอีเมลวันเปิดเรียนรอบถัดไป และใบเสนอราคาจาก {name} ให้คุณ",
              "คุณเลือก แล้วเราส่งใบสมัครไปที่ {name} ให้", "{name} ส่ง Offer letter ให้คุณ"],
    "qeac": "เราเป็นเอเจนซีการศึกษา (QEAC No. 11964) เราไม่สัญญาเรื่องที่เรียน งาน หรือวีซ่า",
    "other_h": "อีกตัวเลือก", "see": "ดู {name} →",
    "f_h": "สมัครกับเรา", "f_name": "ชื่อ-นามสกุล *", "f_email": "อีเมล *", "f_visa": "วีซ่าของคุณ", "f_choose": "เลือก…",
    "f_visas": ["Working Holiday 417", "Work and Holiday 462", "วีซ่าอื่น"], "f_end": "วีซ่าหมดอายุเมื่อไร",
    "f_course": "คอร์สที่สนใจ", "f_unsure": "ยังไม่แน่ใจ", "f_msg": "มีอะไรเพิ่มเติมไหม (ไม่บังคับ)",
    "f_hint": "กรุณาอย่าส่งเลขพาสปอร์ต เลขวีซ่า หรือข้อมูลบัญชีธนาคารในฟอร์มนี้", "f_btn": "สมัครกับเรา", "en_cols": [1],
}


def th_pages(consent, visa_note):
    L = {**UI_TH, "consent": consent, "visa_note": visa_note}
    return {
        f"th/working-holiday/{s['slug']}": (
            f"{s['name']} สำหรับ Working Holiday | We International",
            f"คอร์สและค่าเรียนของ {s['name']} สำหรับผู้ถือวีซ่า Working Holiday (417/462) จากไฟล์ของโรงเรียนเอง สมัครกับ We International",
            detail(s, L, TH_DATA))
        for s in TH_DATA
    }


PAIRS = {f"/working-holiday/{s['slug']}": f"/th/working-holiday/{s['slug']}" for s in DATA}
