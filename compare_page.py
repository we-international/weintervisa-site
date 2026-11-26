"""/courses/aged-care-certificate-iii (+ /th pair): one course, four schools, side by side.

policy-wei-enrolment-focus-20261126 items 1-3: most pages are about courses and enrolling; push short courses
like Charter first; "finish fast" only as facts (length, placement, fees). CHC33021 Certificate III in
Individual Support is the one course that every school we work with sent us: Charter + KCA (Working Holiday
Study and Work Program) and Alana Kaye College + Frontier Education (CRICOS courses, owner-approved
22 Nov 2026). Every number is read from content/working-holiday.json and content/schools.json, so this page
can never disagree with the school pages. Shortest first. No commission, no promise of a job, visa or PR,
and no per-person visa answer: "Check your visa conditions on homeaffairs.gov.au or with a registered
migration agent". Schools that are not approved stay out of the production build (schools.SCHOOLS).
"""
import html
import json
from pathlib import Path

import schools

ROOT = Path(__file__).resolve().parent
e = html.escape
CODE = "CHC33021"
WHV = {s["slug"]: s for s in json.loads((ROOT / "content/working-holiday.json").read_text())["schools"]}
CHECK_URL = "https://immi.homeaffairs.gov.au"

UI = {
    "en": {
        "pre": "", "kicker": "Aged care and disability support",
        "h1": "Certificate III in Individual Support: compare 4 schools",
        "lead": ("CHC33021 is the course for aged care and disability support work. "
                 "Four schools sent us their dates and fees. Here they are side by side, shortest first."),
        "btn": "Enrol with us ↓",
        "th": ["School", "Who it is for", "Length", "Where", "Fees (AUD)", ""],
        "whv": "Working Holiday 417 / 462 (Study and Work Program)",
        "cricos": "International students (CRICOS course {c})",
        "kca_len": "16 weeks: 12 weeks of class + 4 weeks of placement (at least 120 hours)",
        "charter_len": "Up to 12 months (your offer letter shows the real dates). Charter arranges the placement.",
        "weeks": "{w} weeks",
        "kca_fee": "{t} total (tuition, materials and enrolment)",
        "charter_fee": "{t} tuition + {m} materials + A$300 application fee",
        "two_fees": "{a}: {x} · {b}: {y} (total course fee)",
        "more": "Details →",
        "why_h": "What the course is",
        "why": ["You learn to support older people and people with disability in their daily life.",
                "Every school includes supervised work placement in a real workplace.",
                "It is a nationally recognised Certificate III, the same course code at every school."],
        "fit_h": "Which one fits your visa?",
        "fit": ("The Working Holiday programs are for 417 and 462 visa holders. The CRICOS courses are for "
                "international students. On a Working Holiday visa, study is limited to 4 months on each visa "
                "(condition 8548), so check your dates before you choose."),
        "check": (f'Check your visa conditions on <a href="{CHECK_URL}" target="_blank" rel="noopener">homeaffairs.gov.au ↗</a> '
                  "or with a registered migration agent."),
        "src": "Fees and dates come from each school's own files. The school's offer letter is final.",
        "offers": "Ask us about current scholarships and offers. We only tell you about one when the school has put it in writing.",
        "form_h": "Enrol with us",
        "form_p": "Pick a school, or choose \"Not sure yet\" and we help you compare. We reply by email.",
        "school_l": "School you like", "unsure": "Not sure yet",
        "field_opt": "<option>Aged care / individual support</option>",
        "qeac": "We are an education agency (QEAC No. 11964). We do not promise a place, a job or a visa.",
    },
    "th": {
        "pre": "/th", "kicker": "ดูแลผู้สูงอายุและผู้พิการ",
        "h1": "Certificate III in Individual Support: เทียบ 4 โรงเรียน",
        "lead": ("CHC33021 คือคอร์สสำหรับงานดูแลผู้สูงอายุและผู้พิการ "
                 "4 โรงเรียนส่งวันเรียนและค่าเรียนมาให้เรา เราเรียงให้ดูเทียบกัน คอร์สสั้นสุดอยู่บนสุด"),
        "btn": "สมัครกับเรา ↓",
        "th": ["โรงเรียน", "เหมาะกับใคร", "ระยะเวลา", "เรียนที่ไหน", "ค่าเรียน (AUD)", ""],
        "whv": "ผู้ถือวีซ่า Working Holiday 417 / 462",
        "cricos": "นักเรียนต่างชาติ (คอร์ส CRICOS {c})",
        "kca_len": "16 สัปดาห์: เรียน 12 สัปดาห์ + ฝึกงาน 4 สัปดาห์ (อย่างน้อย 120 ชั่วโมง)",
        "charter_len": "ไม่เกิน 12 เดือน (วันเรียนจริงอยู่ใน offer letter) Charter จัดที่ฝึกงานให้",
        "weeks": "{w} สัปดาห์",
        "kca_fee": "รวม {t} (ค่าเรียน ค่าอุปกรณ์ ค่าสมัคร)",
        "charter_fee": "ค่าเรียน {t} + ค่าอุปกรณ์ {m} + ค่าสมัคร A$300",
        "two_fees": "{a}: {x} · {b}: {y} (ค่าเรียนรวมทั้งคอร์ส)",
        "more": "ดูรายละเอียด →",
        "why_h": "คอร์สนี้เรียนอะไร",
        "why": ["เรียนวิธีดูแลผู้สูงอายุและผู้พิการในชีวิตประจำวัน",
                "ทุกโรงเรียนมีฝึกงานจริงในสถานที่ทำงาน มีคนดูแล",
                "เป็น Certificate III ที่รับรองทั่วประเทศ รหัสคอร์สเดียวกันทุกโรงเรียน"],
        "fit_h": "แบบไหนเหมาะกับวีซ่าของคุณ",
        "fit": ("โปรแกรม Working Holiday สำหรับผู้ถือวีซ่า 417 และ 462 ส่วนคอร์ส CRICOS สำหรับนักเรียนต่างชาติ "
                "วีซ่า Working Holiday เรียนได้ไม่เกิน 4 เดือนต่อวีซ่าหนึ่งใบ (เงื่อนไข 8548) เช็กวันของคุณก่อนเลือก"),
        "check": (f'เช็กเงื่อนไขวีซ่าของคุณที่ <a href="{CHECK_URL}" target="_blank" rel="noopener">homeaffairs.gov.au ↗</a> '
                  "หรือกับ registered migration agent"),
        "src": "ค่าเรียนและวันเรียนมาจากไฟล์ของแต่ละโรงเรียนเอง offer letter ของโรงเรียนคือตัวจริง",
        "offers": "ถามเราเรื่องทุนและข้อเสนอที่มีอยู่ตอนนี้ได้ เราบอกเฉพาะเมื่อโรงเรียนแจ้งเป็นลายลักษณ์อักษรแล้วเท่านั้น",
        "form_h": "สมัครกับเรา",
        "form_p": "เลือกโรงเรียน หรือเลือก \"ยังไม่แน่ใจ\" แล้วเราช่วยเทียบให้ เราตอบทางอีเมล",
        "school_l": "โรงเรียนที่สนใจ", "unsure": "ยังไม่แน่ใจ",
        "field_opt": "<option>งานดูแลผู้สูงอายุ / Individual support</option>",
        "cols": {"Already in Australia": "อยู่ออสเตรเลียแล้ว", "Applying from overseas": "สมัครจากต่างประเทศ"},
        "qeac": "เราเป็นเอเจนซีการศึกษา (QEAC No. 11964) เราไม่สัญญาเรื่องที่เรียน งาน หรือวีซ่า",
    },
}


def money(n):
    return f"A${n:,}"


def rows(lang):
    """One dict per school, shortest first. Numbers come straight from the content files."""
    t = UI[lang]
    out = []
    kca = WHV.get("kca")
    if kca:
        total = dict(kca["fees"])["Total"]
        out.append({"name": kca["name"], "who": t["whv"], "len": t["kca_len"], "where": kca["city"],
                    "fee": t["kca_fee"].format(t=total), "href": f'{t["pre"]}/working-holiday/kca', "weeks": 16})
    ch = WHV.get("charter")
    if ch:
        r = next(r for r in ch["fees"] if r[1].startswith(CODE))
        out.append({"name": ch["name"], "who": t["whv"], "len": t["charter_len"], "where": ch["city"],
                    "fee": t["charter_fee"].format(t=r[3], m=r[4]), "href": f'{t["pre"]}/working-holiday/charter', "weeks": 52})
    rest = []
    for s in schools.SCHOOLS:  # production: owner-approved schools only
        c = next((c for c in s["courses"] if c["code"] == CODE), None)
        if not c:
            continue
        a, b = s["fee_columns"][:2]
        rest.append({"name": s["name"], "who": t["cricos"].format(c=c.get("cricos", "")),
                     "len": t["weeks"].format(w=c["weeks"]), "where": " · ".join(s["campuses"]),
                     "fee": t["two_fees"].format(a=t.get("cols", {}).get(a, a), x=money(c["fees"][a]), b=b, y=money(c["fees"][b])),
                     "href": f'{t["pre"]}/schools/{s["slug"]}', "weeks": c["weeks"],
                     "low": min(c["fees"].values())})
    out += sorted(rest, key=lambda r: (r["weeks"], r["low"]))
    return out


def table(lang):
    t = UI[lang]
    head = "".join(f'<th scope="col">{e(h)}</th>' for h in t["th"])
    body = "".join(
        f'<tr><th scope="row" lang="en">{e(r["name"])}</th>'
        + "".join(f'<td data-col="{e(h)}"{' lang="en"' if h == t["th"][3] and lang == "th" else ""}>{e(v)}</td>'
                  for h, v in zip(t["th"][1:5], (r["who"], r["len"], r["where"], r["fee"])))
        + f'<td><a href="{r["href"]}">{t["more"]}</a></td></tr>' for r in rows(lang))
    return (f'<div class="fees cmp"><table><caption lang="en">{CODE} Certificate III in Individual Support</caption>'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")


def form(lang, apply_form):
    """The study application form, set to this course, plus a 'School you like' choice (English values for staff)."""
    t = UI[lang]
    opts = "".join(f'<option value="{e(r["name"])}" lang="en">{e(r["name"])}</option>' for r in rows(lang))
    school = (f'<div class="field"><label for="a-school">{t["school_l"]}</label>\n'
              f'  <select id="a-school" name="school" data-summary="School">{opts}'
              f'<option value="Not sure yet" selected>{t["unsure"]}</option></select></div>\n')
    f = apply_form.replace(t["field_opt"], t["field_opt"].replace("<option>", "<option selected>"), 1)
    f = f.replace("<option>Certificate III</option>", "<option selected>Certificate III</option>", 1)
    anchor = '<div class="row2">'
    assert t["field_opt"] in apply_form and anchor in f, "application form changed: update compare_page.form"
    return f.replace(anchor, school + anchor, 1)


def body(lang, apply_form, visa_note):
    t = UI[lang]
    why = "".join(f"<li>{e(x)}</li>" for x in t["why"])
    return f"""<section class="wrap narrow">
<p class="small"><a href="{t["pre"]}/fast-track-courses">{"← Fast-track courses" if lang == "en" else "← คอร์สจบไว"}</a></p>
<p class="kicker">{t["kicker"]}</p>
<h1>{e(t["h1"])}</h1>
<p class="lead">{e(t["lead"])}</p>
<p class="actions"><a class="btn" href="#enrol">{t["btn"]}</a></p>
</section>
<section class="wrap" id="compare">
{table(lang)}
<p class="small">{e(t["src"])}</p>
</section>
<section class="wrap narrow">
<h2>{t["why_h"]}</h2>
<ul class="list">{why}</ul>
<h2>{t["fit_h"]}</h2>
<p>{e(t["fit"])}</p>
<p class="note-box"><strong>{t["check"]}</strong></p>
<p>{e(t["offers"])}</p>
{visa_note}
</section>
<section class="wrap narrow" id="enrol">
<h2>{t["form_h"]}</h2>
<p>{e(t["form_p"])}</p>
{form(lang, apply_form)}
<p class="small">{t["qeac"]}</p>
</section>"""


def pages(apply_form, visa_note):
    return {"courses/aged-care-certificate-iii": (
        "Aged care Cert III: compare 4 schools | We International",
        "CHC33021 aged care course in Australia: length, campuses and fees from 4 schools side by side. Enrol with We International.",
        body("en", apply_form, visa_note))}


def th_pages(apply_form, visa_note):
    return {"th/courses/aged-care-certificate-iii": (
        "เทียบคอร์สดูแลผู้สูงอายุ 4 โรงเรียน | We International",
        "คอร์สดูแลผู้สูงอายุ CHC33021 ในออสเตรเลีย: ระยะเวลา วิทยาเขต และค่าเรียนจาก 4 โรงเรียน เทียบกันในหน้าเดียว สมัครกับ We International",
        body("th", apply_form, visa_note))}


PAGES_EN = ["courses/aged-care-certificate-iii"]
PAIRS = {"/courses/aged-care-certificate-iii": "/th/courses/aged-care-certificate-iii"}
