"""/courses/aged-care-certificate-iii (+ /th pair): one course, four schools, side by side.

policy-wei-enrolment-focus-20261126 items 1-3: most pages are about courses and enrolling; push short courses
like Charter first; "finish fast" only as facts (length, placement, fees). CHC33021 Certificate III in
Individual Support is the one course that every school we work with sent us: Charter + KCA (Working Holiday
Study and Work Program) and Alana Kaye College + Frontier Education (CRICOS courses, owner-approved
22 Nov 2026). Every number is read from content/working-holiday.json and content/schools.json, so this page
can never disagree with the school pages. Shortest first. No commission, no promise of a job, visa or PR,
and no per-person visa answer: "Check your visa conditions on homeaffairs.gov.au or with a registered
migration agent". Schools that are not approved stay out of the production build (schools.SCHOOLS).

Since 26 Nov 2026 the page is one spec per course (SPECS): aged care (CHC33021, 4 schools) and childcare
(CHC30125 at Charter, CHC30121 at Alana Kaye College; each school's own code is shown, never called "the same").
Add a course = add a spec. A school special price is shown only with its end date from the school file.
"""
import re
import html
import json
from pathlib import Path

import schools

ROOT = Path(__file__).resolve().parent
e = html.escape
WHV = {s["slug"]: s for s in json.loads((ROOT / "content/working-holiday.json").read_text())["schools"]}
CHECK_URL = "https://immi.homeaffairs.gov.au"

AGED = {
    "slug": "aged-care-certificate-iii", "codes": ["CHC33021"], "whv": ["kca", "charter"],
    "caption": "CHC33021 Certificate III in Individual Support",
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


AGED["en"].update({"title": "Aged care Cert III: compare 4 schools | We International",
                   "desc": "CHC33021 aged care course in Australia: length, campuses and fees from 4 schools side by side. Enrol with We International."})
AGED["th"].update({"title": "เทียบคอร์สดูแลผู้สูงอายุ 4 โรงเรียน | We International",
                   "desc": "คอร์สดูแลผู้สูงอายุ CHC33021 ในออสเตรเลีย: ระยะเวลา วิทยาเขต และค่าเรียนจาก 4 โรงเรียน เทียบกันในหน้าเดียว สมัครกับ We International"})

CHILD = {
    "slug": "childcare-certificate-iii", "codes": ["CHC30125", "CHC30121"], "whv": ["charter"],
    "caption": "Certificate III in Early Childhood Education and Care (CHC30125 / CHC30121)",
    "en": {
        "pre": "", "kicker": "Childcare and early childhood",
        "h1": "Certificate III in Early Childhood Education and Care: compare 2 schools",
        "lead": ("This is the course for childcare work. Two schools we work with sent us their dates and fees. "
                 "Here they are side by side."),
        "title": "Childcare Cert III: compare 2 schools | We International",
        "desc": "Childcare Certificate III in Australia: length, campuses and fees from 2 schools side by side. Enrol with We International.",
        "btn": AGED["en"]["btn"], "th": AGED["en"]["th"], "whv": AGED["en"]["whv"],
        "cricos": "International students ({k}, CRICOS course {c})",
        "charter_len": "Up to 12 months (your offer letter shows the real dates). Charter arranges 160 hours of placement.",
        "weeks": "{w} weeks",
        "charter_fee": "{t} tuition + {m} materials + A$300 application fee",
        "special": "{now} tuition (special price until {end}; was {was})",
        "two_fees": "{a}: {x} · {b}: {y} (total course fee)",
        "more": "Details →",
        "codes_note": ("The course code is not the same at both schools: Charter teaches CHC30125 and Alana Kaye College "
                       "lists CHC30121. Your offer letter shows the code you will study."),
        "why_h": "What the course is",
        "why": ["You learn to care for babies and young children and to support their play and learning.",
                "It includes work placement in a real early childhood service (Charter lists 160 hours).",
                "It is a nationally recognised Certificate III. A related job is early childhood educator."],
        "next_h": "Want to go further?",
        "next": "Alana Kaye College also teaches the {n} ({c}, {w} weeks, from {f}).",
        "fit_h": AGED["en"]["fit_h"],
        "fit": ("The Charter program is for 417 and 462 visa holders. The Alana Kaye College course is a CRICOS course "
                "for international students. On a Working Holiday visa, study is limited to 4 months on each visa "
                "(condition 8548), so check your dates before you choose."),
        "check": AGED["en"]["check"], "src": AGED["en"]["src"], "offers": AGED["en"]["offers"],
        "form_h": AGED["en"]["form_h"], "form_p": AGED["en"]["form_p"],
        "school_l": AGED["en"]["school_l"], "unsure": AGED["en"]["unsure"],
        "field_opt": "<option>Early childhood education</option>",
        "qeac": AGED["en"]["qeac"],
        "back": "← Fast-track courses", "other": "Compare the aged care course (CHC33021) at 4 schools →",
    },
    "th": {
        "pre": "/th", "kicker": "งานดูแลเด็กและการศึกษาปฐมวัย",
        "h1": "Certificate III in Early Childhood Education and Care: เทียบ 2 โรงเรียน",
        "lead": "คอร์สนี้สำหรับงานดูแลเด็ก (childcare) 2 โรงเรียนที่ทำงานกับเราส่งวันเรียนและค่าเรียนมาให้ เราเรียงให้ดูเทียบกัน",
        "title": "เทียบคอร์สดูแลเด็ก (childcare) 2 โรงเรียน | We International",
        "desc": "คอร์สดูแลเด็ก (childcare) Certificate III ในออสเตรเลีย: ระยะเวลา วิทยาเขต และค่าเรียนจาก 2 โรงเรียน เทียบกันในหน้าเดียว สมัครกับ We International",
        "btn": AGED["th"]["btn"], "th": AGED["th"]["th"], "whv": AGED["th"]["whv"],
        "cricos": "นักเรียนต่างชาติ ({k}, คอร์ส CRICOS {c})",
        "charter_len": "ไม่เกิน 12 เดือน (วันเรียนจริงอยู่ใน offer letter) Charter จัดที่ฝึกงานให้ 160 ชั่วโมง",
        "weeks": "{w} สัปดาห์",
        "charter_fee": "ค่าเรียน {t} + ค่าอุปกรณ์ {m} + ค่าสมัคร A$300",
        "special": "ค่าเรียน {now} (ราคาพิเศษถึง {end} ปกติ {was})",
        "two_fees": "{a}: {x} · {b}: {y} (ค่าเรียนรวมทั้งคอร์ส)",
        "more": "ดูรายละเอียด →",
        "codes_note": ("รหัสคอร์สของ 2 โรงเรียนไม่เหมือนกัน: Charter สอน CHC30125 ส่วน Alana Kaye College ระบุ CHC30121 "
                       "รหัสที่คุณจะเรียนจริงอยู่ใน offer letter"),
        "why_h": "คอร์สนี้เรียนอะไร",
        "why": ["เรียนวิธีดูแลเด็กเล็กและเด็กทารก และช่วยให้เด็กได้เล่นและเรียนรู้",
                "มีฝึกงานจริงในสถานที่ดูแลเด็ก (Charter ระบุ 160 ชั่วโมง)",
                "เป็น Certificate III ที่รับรองทั่วประเทศ อาชีพที่เกี่ยวข้องคือครูปฐมวัย (early childhood educator)"],
        "next_h": "อยากเรียนต่อให้สูงขึ้น",
        "next": "Alana Kaye College มีคอร์ส {n} ด้วย ({c}, {w} สัปดาห์, เริ่มที่ {f})",
        "fit_h": AGED["th"]["fit_h"],
        "fit": ("โปรแกรมของ Charter สำหรับผู้ถือวีซ่า 417 และ 462 ส่วนคอร์สของ Alana Kaye College เป็นคอร์ส CRICOS "
                "สำหรับนักเรียนต่างชาติ วีซ่า Working Holiday เรียนได้ไม่เกิน 4 เดือนต่อวีซ่าหนึ่งใบ (เงื่อนไข 8548) เช็กวันของคุณก่อนเลือก"),
        "check": AGED["th"]["check"], "src": AGED["th"]["src"], "offers": AGED["th"]["offers"],
        "form_h": AGED["th"]["form_h"], "form_p": AGED["th"]["form_p"],
        "school_l": AGED["th"]["school_l"], "unsure": AGED["th"]["unsure"],
        "field_opt": "<option>การศึกษาปฐมวัย</option>",
        "cols": AGED["th"]["cols"],
        "qeac": AGED["th"]["qeac"],
        "back": "← คอร์สจบไว", "other": "เทียบคอร์สดูแลผู้สูงอายุ (CHC33021) 4 โรงเรียน →",
    },
}
AGED["en"].update({"back": "← Fast-track courses", "other": "Compare the childcare course at 2 schools →"})
AGED["th"].update({"back": "← คอร์สจบไว", "other": "เทียบคอร์สดูแลเด็ก (childcare) 2 โรงเรียน →"})
SPECS = [AGED, CHILD]
OTHER = {AGED["slug"]: CHILD["slug"], CHILD["slug"]: AGED["slug"]}
TH_MONTHS = {"January": "ม.ค.", "February": "ก.พ.", "March": "มี.ค.", "April": "เม.ย.", "May": "พ.ค.", "June": "มิ.ย.",
             "July": "ก.ค.", "August": "ส.ค.", "September": "ก.ย.", "October": "ต.ค.", "November": "พ.ย.", "December": "ธ.ค."}


def money(n):
    return f"A${n:,}"


def special_end(school, lang):
    """End date of a school special price, read from the school's own fee notes (None if there is none)."""
    for n in school.get("fee_notes", []):
        m = re.search(r"special prices run until (\d{1,2} \w+ \d{4})", n)
        if m:
            d, mo, y = m.group(1).split()
            return m.group(1) if lang == "en" else f"{d} {TH_MONTHS[mo]} {y}"
    return None


def tuition(t, school, raw, lang):
    """'A$7,700 (special, was A$12,650)' → special price with its end date; no end date in the file = no special shown."""
    m = re.fullmatch(r"(A\$[\d,]+) \(special, was (A\$[\d,]+)\)", raw)
    if not m:
        return raw
    end = special_end(school, lang)
    return t["special"].format(now=m.group(1), was=m.group(2), end=end) if end else m.group(1)


def rows(spec, lang):
    """One dict per school: Working Holiday programs first, then CRICOS courses shortest first. Numbers come
    straight from the content files."""
    t = spec[lang]
    out = []
    for slug in spec["whv"]:
        w = WHV.get(slug)
        if not w:
            continue
        href = f'{t["pre"]}/working-holiday/{slug}'
        if slug == "kca":
            total = dict(w["fees"])["Total"]
            out.append({"name": w["name"], "who": t["whv"], "len": t["kca_len"], "where": w["city"],
                        "fee": t["kca_fee"].format(t=total), "href": href, "weeks": 16})
            continue
        r = next((r for r in w["fees"] if r[1].split()[0] in spec["codes"]), None)
        if not r:
            continue
        tf = tuition(t, w, r[3], lang)
        fee = t["charter_fee"].format(t=r[3], m=r[4])
        if tf != r[3]:  # special price: "<tuition with end date> + materials + application fee"
            fee = tf + " + " + fee.split(" + ", 1)[1]
        out.append({"name": w["name"], "who": t["whv"], "len": t["charter_len"], "where": w["city"],
                    "fee": fee, "href": href, "weeks": 52})
    rest = []
    for s in schools.SCHOOLS:  # production: owner-approved schools only
        c = next((c for c in s["courses"] if c["code"] in spec["codes"]), None)
        if not c:
            continue
        a, b = s["fee_columns"][:2]
        who = t["cricos"].format(c=c.get("cricos", ""), k=c["code"])
        rest.append({"name": s["name"], "who": who,
                     "len": t["weeks"].format(w=c["weeks"]), "where": " · ".join(s["campuses"]),
                     "fee": t["two_fees"].format(a=t.get("cols", {}).get(a, a), x=money(c["fees"][a]), b=b, y=money(c["fees"][b])),
                     "href": f'{t["pre"]}/schools/{s["slug"]}', "weeks": c["weeks"],
                     "low": min(c["fees"].values())})
    out += sorted(rest, key=lambda r: (r["weeks"], r["low"]))
    return out


def table(spec, lang):
    t = spec[lang]
    head = "".join(f'<th scope="col">{e(h)}</th>' for h in t["th"])
    body = "".join(
        f'<tr><th scope="row" lang="en">{e(r["name"])}</th>'
        + "".join(f'<td data-col="{e(h)}"{' lang="en"' if h == t["th"][3] and lang == "th" else ""}>{e(v)}</td>'
                  for h, v in zip(t["th"][1:5], (r["who"], r["len"], r["where"], r["fee"])))
        + f'<td><a href="{r["href"]}">{t["more"]}</a></td></tr>' for r in rows(spec, lang))
    return (f'<div class="fees cmp"><table><caption lang="en">{e(spec["caption"])}</caption>'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")


def form(spec, lang, apply_form):
    """The study application form, set to this course, plus a 'School you like' choice (English values for staff)."""
    t = spec[lang]
    opts = "".join(f'<option value="{e(r["name"])}" lang="en">{e(r["name"])}</option>' for r in rows(spec, lang))
    school = (f'<div class="field"><label for="a-school">{t["school_l"]}</label>\n'
              f'  <select id="a-school" name="school" data-summary="School">{opts}'
              f'<option value="Not sure yet" selected>{t["unsure"]}</option></select></div>\n')
    f = apply_form.replace(t["field_opt"], t["field_opt"].replace("<option>", "<option selected>"), 1)
    f = f.replace("<option>Certificate III</option>", "<option selected>Certificate III</option>", 1)
    anchor = '<div class="row2">'
    assert t["field_opt"] in apply_form and anchor in f, "application form changed: update compare_page.form"
    return f.replace(anchor, school + anchor, 1)


def further(spec, lang):
    """Childcare only: the Diploma at an approved school, as a plain fact with its lowest fee."""
    t = spec[lang]
    if "next" not in t:
        return ""
    for s in schools.SCHOOLS:
        c = next((c for c in s["courses"] if c["code"] == "CHC50121"), None)
        if c:
            return (f'<h2>{t["next_h"]}</h2><p>{e(t["next"].format(n=c["name"], c=c["code"], w=c["weeks"], f=money(min(c["fees"].values()))))} '
                    f'<a href="{t["pre"]}/schools/{s["slug"]}">{t["more"]}</a></p>')
    return ""


def body(spec, lang, apply_form, visa_note):
    t = spec[lang]
    why = "".join(f"<li>{e(x)}</li>" for x in t["why"])
    codes = f'<p class="small">{e(t["codes_note"])}</p>' if "codes_note" in t else ""
    return f"""<section class="wrap narrow">
<p class="small"><a href="{t["pre"]}/fast-track-courses">{t["back"]}</a></p>
<p class="kicker">{t["kicker"]}</p>
<h1>{e(t["h1"])}</h1>
<p class="lead">{e(t["lead"])}</p>
<p class="actions"><a class="btn" href="#enrol">{t["btn"]}</a></p>
</section>
<section class="wrap" id="compare">
{table(spec, lang)}
<p class="small">{e(t["src"])}</p>
{codes}
</section>
<section class="wrap narrow">
<h2>{t["why_h"]}</h2>
<ul class="list">{why}</ul>
{further(spec, lang)}
<h2>{t["fit_h"]}</h2>
<p>{e(t["fit"])}</p>
<p class="note-box"><strong>{t["check"]}</strong></p>
<p>{e(t["offers"])}</p>
{visa_note}
<p><a href="{t["pre"]}/courses/{OTHER[spec["slug"]]}">{t["other"]}</a></p>
</section>
<section class="wrap narrow" id="enrol">
<h2>{t["form_h"]}</h2>
<p>{e(t["form_p"])}</p>
{form(spec, lang, apply_form)}
<p class="small">{t["qeac"]}</p>
</section>"""


def pages(apply_form, visa_note):
    return {f'courses/{s["slug"]}': (s["en"]["title"], s["en"]["desc"], body(s, "en", apply_form, visa_note)) for s in SPECS}


def th_pages(apply_form, visa_note):
    return {f'th/courses/{s["slug"]}': (s["th"]["title"], s["th"]["desc"], body(s, "th", apply_form, visa_note)) for s in SPECS}


PAGES_EN = [f'courses/{s["slug"]}' for s in SPECS]
PAIRS = {f'/courses/{s["slug"]}': f'/th/courses/{s["slug"]}' for s in SPECS}
