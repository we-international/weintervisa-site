"""/already-in-australia and /th/already-in-australia (policy-wei-enrolment-focus-20261126, item 6).

Owner 26 Nov 2026: "Already in Australia? Want to study alongside your current visa?" — invite people who
are already here (Working Holiday 417/462 and others) to add a short course, then "Enrol with us" → GetWec.
Rules: only general official facts (Home Affairs, quoted with the source and date); never say whether one
person's visa allows study; always "Check your visa conditions on homeaffairs.gov.au or with a registered
migration agent"; offers only "Ask us about current scholarships and offers" (no countdowns, no made-up
discounts); no commission, no promise of a job, visa or PR. The form is the Working Holiday form
(whv_enrol: visa + visa end month + course) so GetWec makes the same application case; course starts
on "Not sure yet" because the visitor has not picked a school yet.
"""
import html

import whv_page
from pages import CONSENT, VISA_NOTE

e = html.escape

WC = "https://immi.homeaffairs.gov.au/programs-subsite/Pages/working-holiday-maker/work-conditions.aspx"
VEVO = "https://immi.homeaffairs.gov.au/visas/already-have-a-visa/check-visa-details-and-conditions/check-conditions-online"
CHECK_EN = ('Check your visa conditions on <a href="https://immi.homeaffairs.gov.au" target="_blank" rel="noopener">homeaffairs.gov.au ↗</a> '
            "or with a registered migration agent.")
CHECK_TH = ('เช็กเงื่อนไขวีซ่าของคุณที่ <a href="https://immi.homeaffairs.gov.au" target="_blank" rel="noopener">homeaffairs.gov.au ↗</a> '
            "หรือกับ registered migration agent")

UI = {
    "en": {
        "pre": "", "kicker": "Already in Australia",
        "h1": "Already in Australia? Study a short course alongside your visa",
        "lead": ("Many people on a Working Holiday or another visa add a short course while they are here. "
                 "Tell us your visa and when it ends, and we help you find a course and a start date that fit."),
        "btn": "Enrol with us ↓",
        "facts_h": "What Home Affairs says",
        "facts": [
            "Working Holiday visa (417 or 462): condition 8548 limits study or training to <strong>4 months on each visa</strong>.",
            "Online or correspondence courses from an overseas provider are not counted under condition 8548.",
            "Workplace-based training counts as work, not study, for the Working Holiday program.",
            f'Other visas have their own conditions. You can see yours in <a href="{VEVO}" target="_blank" rel="noopener">VEVO ↗</a>.',
        ],
        "facts_src": (f'Source: <a href="{WC}" target="_blank" rel="noopener">Home Affairs, Working Holiday Maker work conditions ↗</a> '
                      "(page updated 18 November 2026). This is general information, not advice about your visa."),
        "check": CHECK_EN,
        "fast_h": "Short courses that finish fast",
        "fast_p": "Two schools sent us their courses and fees for people already in Australia. Both include work placement.",
        "see": "Courses, fees and enrol →",
        "cmp": "Compare the aged care course CHC33021 at 4 schools →",
        "offers_h": "Scholarships and offers",
        "offers_p": ("Ask us about current scholarships and offers. We only tell you about an offer when the school "
                     "has put it in writing, with its end date and conditions."),
        "how_h": "How it works",
        "steps": ["Send the form below with your visa and the month it ends.",
                  "We look for courses whose dates fit inside the time you told us.",
                  "We email you start dates and a written quote from the school.",
                  "You choose, and we send your application to the school for you."],
        "qeac": "We are an education agency (QEAC No. 11964). We do not promise a place, a job or a visa.",
    },
    "th": {
        "pre": "/th", "kicker": "อยู่ออสเตรเลียแล้ว",
        "h1": "อยู่ออสเตรเลียแล้ว? เรียนคอร์สสั้นคู่กับวีซ่าที่มีอยู่",
        "lead": ("หลายคนที่ถือวีซ่า Working Holiday หรือวีซ่าอื่น เรียนคอร์สสั้นเพิ่มระหว่างอยู่ที่นี่ "
                 "บอกเราว่าคุณถือวีซ่าอะไรและหมดเมื่อไร แล้วเราช่วยหาคอร์สและวันเริ่มเรียนที่ลงตัว"),
        "btn": "สมัครกับเรา ↓",
        "facts_h": "Home Affairs ระบุว่า",
        "facts": [
            "วีซ่า Working Holiday (417 หรือ 462): เงื่อนไข 8548 ให้เรียนหรือฝึกอบรมได้ <strong>ไม่เกิน 4 เดือนต่อวีซ่าหนึ่งใบ</strong>",
            "คอร์สออนไลน์หรือคอร์สทางไปรษณีย์จากสถาบันต่างประเทศ ไม่นับรวมในเงื่อนไข 8548",
            "การฝึกในที่ทำงาน (workplace-based training) โครงการ Working Holiday นับเป็นการทำงาน ไม่ใช่การเรียน",
            f'วีซ่าอื่นมีเงื่อนไขของตัวเอง ดูของคุณได้ใน <a href="{VEVO}" target="_blank" rel="noopener">VEVO ↗</a>',
        ],
        "facts_src": (f'ที่มา: <a href="{WC}" target="_blank" rel="noopener">Home Affairs, Working Holiday Maker work conditions ↗</a> '
                      "(หน้าอัปเดต 18 พฤศจิกายน 2026) ข้อมูลนี้เป็นข้อมูลทั่วไป ไม่ใช่คำแนะนำเรื่องวีซ่าของคุณ"),
        "check": CHECK_TH,
        "fast_h": "คอร์สสั้นที่จบไว",
        "fast_p": "2 โรงเรียนส่งคอร์สและค่าเรียนสำหรับคนที่อยู่ออสเตรเลียแล้วมาให้เรา ทั้งสองคอร์สมีฝึกงาน",
        "see": "ดูคอร์ส ค่าเรียน และสมัคร →",
        "cmp": "เทียบคอร์สดูแลผู้สูงอายุ CHC33021 จาก 4 โรงเรียน →",
        "offers_h": "ทุนและข้อเสนอพิเศษ",
        "offers_p": ("ถามเราเรื่องทุนและข้อเสนอที่มีอยู่ตอนนี้ได้ เราบอกข้อเสนอเฉพาะเมื่อโรงเรียนแจ้งเป็นลายลักษณ์อักษร "
                     "พร้อมวันหมดเขตและเงื่อนไขเท่านั้น"),
        "how_h": "ขั้นตอน",
        "steps": ["ส่งฟอร์มด้านล่าง พร้อมบอกวีซ่าและเดือนที่วีซ่าหมด",
                  "เราหาคอร์สที่วันเรียนอยู่ในช่วงเวลาที่คุณบอกเรา",
                  "เราอีเมลวันเริ่มเรียนและใบเสนอราคาจากโรงเรียนให้คุณ",
                  "คุณเลือก แล้วเราส่งใบสมัครไปที่โรงเรียนให้"],
        "qeac": "เราเป็นเอเจนซีการศึกษา (QEAC No. 11964) เราไม่สัญญาเรื่องที่เรียน งาน หรือวีซ่า",
    },
}


def body(lang, consent, visa_note):
    t = UI[lang]
    th = lang == "th"
    L = {**(whv_page.UI_TH if th else whv_page.UI_EN), "consent": consent}
    data = whv_page.TH_DATA if th else whv_page.DATA
    labels = {k: v for s in data for k, v in (s.get("option_labels") or {}).items()}
    # Course select starts on "Not sure yet": the visitor has not picked a school on this page.
    form = whv_page.form("charter", L, labels).replace(
        '<option value="Not sure yet">', '<option value="Not sure yet" selected>').replace(
        "<option>Not sure yet</option>", "<option selected>Not sure yet</option>")
    facts = "".join(f"<li>{f}</li>" for f in t["facts"])
    cards = "".join(f'<li class="path"><h3 lang="en">{e(s["name"])}</h3><p>{e(s["summary"])}</p>'
                    f'<a href="{t["pre"]}/working-holiday/{s["slug"]}">{t["see"]}</a></li>' for s in data)
    steps = "".join(f"<li>{e(x)}</li>" for x in t["steps"])
    return f"""<section class="wrap narrow">
<p class="kicker">{t["kicker"]}</p>
<h1>{t["h1"]}</h1>
<p class="lead">{t["lead"]}</p>
<p class="actions"><a class="btn" href="#enrol">{t["btn"]}</a></p>
<h2>{t["facts_h"]}</h2>
<ul class="list">{facts}</ul>
<p class="small">{t["facts_src"]}</p>
<p class="note-box"><strong>{t["check"]}</strong></p>
</section>
<section class="wrap" id="schools">
<h2>{t["fast_h"]}</h2>
<p>{t["fast_p"]}</p>
<ul class="paths">{cards}</ul>
<p><a href="{t["pre"]}/courses/aged-care-certificate-iii">{t["cmp"]}</a></p>
</section>
<section class="wrap narrow">
<h2>{t["offers_h"]}</h2>
<p>{t["offers_p"]}</p>
<h2>{t["how_h"]}</h2>
<ol class="steps">{steps}</ol>
{visa_note}
</section>
<section class="wrap narrow" id="enrol">
{form}
<p class="small">{t["qeac"]}</p>
</section>"""


PAGES = {"already-in-australia": (
    "Study alongside your visa in Australia | We International",
    "Already in Australia on a Working Holiday or another visa? Find a short course that fits your visa dates and enrol with We International.",
    body("en", CONSENT, VISA_NOTE))}


def th_pages(consent, visa_note):
    return {"th/already-in-australia": (
        "เรียนคู่กับวีซ่าที่มีอยู่ในออสเตรเลีย | We International",
        "อยู่ออสเตรเลียแล้วด้วยวีซ่า Working Holiday หรือวีซ่าอื่น? หาคอร์สสั้นที่ลงตัวกับวันวีซ่าของคุณ แล้วสมัครกับ We International",
        body("th", consent, visa_note))}


PAIRS = {"/already-in-australia": "/th/already-in-australia"}
