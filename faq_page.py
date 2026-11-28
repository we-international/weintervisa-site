"""/frequently-asked-questions and /th/frequently-asked-questions — one help page for every question (22 Nov 2026).

The Wix FAQ had 7 questions in 4 topics. This page keeps the general answers and gathers the FAQ of every
rebuilt page (home, Working Holiday, nursing, homestay, OSHC, referral partners) by topic, with a jump bar and a
link to the full page under each topic. Answers are read from the same JSON as those pages (content/*.json and
content/th/*.json), so a fact changes in one place only. Answers from home and Working Holiday may hold links
(trusted HTML from our own JSON); the others are escaped like on their own pages.
"""
import html
import json
import re
from pathlib import Path

e = html.escape
ROOT = Path(__file__).resolve().parent

GENERAL = {
    "en": [
        ("Can I apply for every study area on this site?", "Not yet. Some areas are ones we are preparing to support. We tell you which courses are confirmed."),
        ("Will I get three options?", "We aim to compare at least three suitable schools for your study area and city when they are available. We tell you if fewer are confirmed."),
        ("Is a place, a visa or a job guaranteed?", "No. The school decides admission, the government decides visas, and jobs are not guaranteed."),
        ("Do you give visa advice?", "No. We are not a migration agent. For visa advice we refer you to a registered migration agent."),
        ("Can I visit Australia first and switch to a student visa onshore?",
         "In general, not if your visitor visa application was lodged on or after 28 Nov 2026: it carries condition 8503 \"No Further Stay\". Plan to apply for a Student visa from outside Australia. This is general information, not visa advice; for your own case we refer you to a registered migration agent. "
         '<a href="/post/can-i-switch-from-a-visitor-visa-to-a-student-visa-in-australia">Read more (English and Thai)</a>'),
        ("Can I visit your office?", "We work online. Send us a message and we will arrange a time to talk."),
        ("Can I send my documents now?", "Please start with a short message. Send passports or other private documents only when we give you a secure way to do it."),
        ("Can I talk in my own language?", "Yes, with Mia, our AI assistant: she can chat in many languages. Our team speaks Thai and English, so a reply from a person will be in Thai or English."),
        ("Is the chat assistant a person?", "Our website assistant is an AI. It answers general questions and passes your message to our team."),
    ],
    "th": [
        ("สมัครเรียนได้ทุกสาขาที่อยู่ในเว็บไหม", "ยังไม่ทุกสาขา บางสาขาเรากำลังเตรียมความพร้อม เราจะบอกคุณว่าคอร์สไหนยืนยันแล้ว"),
        ("จะได้ตัวเลือก 3 ที่ไหม", "เราตั้งใจเทียบสถาบันที่เหมาะอย่างน้อย 3 แห่งตามสาขาและเมืองที่คุณเลือก ถ้ามีให้เลือก ถ้ายืนยันได้น้อยกว่านั้น เราจะบอกตรงๆ"),
        ("มีใครรับประกันว่าจะได้ที่เรียน วีซ่า หรืองานไหม", "ไม่มี สถาบันเป็นผู้ตัดสินการรับเข้าเรียน รัฐบาลเป็นผู้ตัดสินเรื่องวีซ่า และเรื่องงานก็ไม่มีใครรับประกันได้"),
        ("ให้คำแนะนำเรื่องวีซ่าไหม", "ไม่ เราไม่ใช่ migration agent เรื่องคำแนะนำวีซ่า เราจะแนะนำ registered migration agent ให้"),
        ("มาเที่ยวออสเตรเลียก่อน แล้วเปลี่ยนเป็นวีซ่านักเรียนในประเทศได้ไหม",
         "โดยทั่วไปไม่ได้ ถ้ายื่นวีซ่าท่องเที่ยวตั้งแต่ 28 พ.ย. 2026 เพราะจะมีเงื่อนไข 8503 \"No Further Stay\" ควรวางแผนยื่นวีซ่านักเรียนจากนอกออสเตรเลีย ข้อมูลนี้เป็นข้อมูลทั่วไป ไม่ใช่คำแนะนำวีซ่า กรณีของคุณ เราจะแนะนำ registered migration agent ให้ "
         '<a href="/post/can-i-switch-from-a-visitor-visa-to-a-student-visa-in-australia">อ่านต่อ (ไทยและอังกฤษ)</a>'),
        ("ไปที่ออฟฟิศได้ไหม", "เราทำงานออนไลน์ ส่งข้อความมา แล้วเราจะนัดเวลาคุยกัน"),
        ("ส่งเอกสารตอนนี้เลยได้ไหม", "เริ่มจากส่งข้อความสั้นๆ ก่อน ส่งพาสปอร์ตหรือเอกสารส่วนตัวเมื่อเราให้ช่องทางที่ปลอดภัยแล้วเท่านั้น"),
        ("คุยเป็นภาษาของฉันได้ไหม", "ได้ กับ Mia ผู้ช่วย AI ของเรา ซึ่งคุยได้หลายภาษา ทีมงานของเราพูดภาษาไทยและอังกฤษ คำตอบจากทีมงานจึงเป็นภาษาไทยหรืออังกฤษ"),
        ("ผู้ช่วยในแชทเป็นคนจริงไหม", "ผู้ช่วยบนเว็บไซต์ของเราเป็น AI ตอบคำถามทั่วไป และส่งข้อความของคุณต่อให้ทีมงาน"),
    ],
}

# The Wix FAQ also answered IELTS / TOEIC practice; our English practice page is open now.
ENGLISH = {
    "en": [("Can I practise English or IELTS / TOEIC here?",
            'You can practise everyday English for free on our <a href="/english-practice">English practice page</a>: '
            "an 8-question quiz, short videos and games. We do not run IELTS or TOEIC tests, but we can help you find an English course in Australia.")],
    "th": [("ฝึกภาษาอังกฤษ หรือเตรียม IELTS / TOEIC ที่นี่ได้ไหม",
            'ฝึกภาษาอังกฤษในชีวิตประจำวันได้โดยไม่มีค่าใช้จ่ายที่<a href="/th/english-practice">หน้าฝึกภาษาอังกฤษ</a> '
            "มีแบบทดสอบ 8 ข้อ วิดีโอสั้น และเกม เราไม่ได้จัดสอบ IELTS หรือ TOEIC แต่ช่วยหาคอร์สภาษาอังกฤษในออสเตรเลียให้ได้")],
}

# From the home FAQ, only the questions the general list does not already answer (visa, language and
# Working Holiday are answered in their own topics).
HOME_KEEP = (0, 3)

# (anchor, JSON name or None, raw HTML answers?, page link)
TOPICS = [
    ("start", None, True, "/contact-us"),
    ("working-holiday", "fast-track", True, "/fast-track-courses"),
    ("nursing", "nursing", False, "/courses/nursing-pathways-australia"),
    ("homestay", "homestay", False, "/homestay"),
    ("health-cover", "oshc", False, "/oshc"),
    ("english", None, True, "/english-practice"),
    ("partners", "referral-partners", False, "/referral-partners"),
]

UI = {
    "en": {
        "h1": "Frequently asked questions", "kicker": "Help centre",
        "lead": "Clear answers about study, Working Holiday courses, nursing, homestay and health cover in Australia. Tap a question to open it.",
        "jump": "Jump to a topic",
        "names": {"start": "Getting started", "working-holiday": "Working Holiday courses", "nursing": "Nursing",
                  "homestay": "Homestay", "health-cover": "Health cover (OSHC)", "english": "English practice",
                  "partners": "For partners"},
        "intros": {"start": "How we work, what we can and cannot do, and how to reach us.",
                   "working-holiday": "On a 417 or 462 visa and thinking about a short course.",
                   "nursing": "Overseas nurses and people who want to start a nursing pathway.",
                   "homestay": "Living with a host family when you first arrive.",
                   "health-cover": "Overseas Student Health Cover: what it is and how to buy it.",
                   "english": "Free practice made by our team.",
                   "partners": "Schools, colleges and service providers who want to work with us."},
        "more": "Read the full page", "moreStart": "Contact us",
        "count": "{n} questions", "still": "Still have a question? Our team reads every message.",
        "book": "Book a time to talk", "bookHref": "/schedule",
        "top": "Back to topics",
    },
    "th": {
        "h1": "คำถามที่พบบ่อย", "kicker": "ศูนย์ช่วยเหลือ",
        "lead": "คำตอบชัดๆ เรื่องเรียนต่อ คอร์สสำหรับ Working Holiday พยาบาล โฮมสเตย์ และประกันสุขภาพในออสเตรเลีย แตะที่คำถามเพื่อเปิดอ่าน",
        "jump": "ไปที่หัวข้อ",
        "names": {"start": "เริ่มต้น", "working-holiday": "คอร์สสำหรับ Working Holiday", "nursing": "พยาบาล",
                  "homestay": "โฮมสเตย์", "health-cover": "ประกันสุขภาพ (OSHC)", "english": "ฝึกภาษาอังกฤษ",
                  "partners": "สำหรับพาร์ตเนอร์"},
        "intros": {"start": "เราทำงานอย่างไร ทำอะไรได้และไม่ได้ และติดต่อเราอย่างไร",
                   "working-holiday": "ถือวีซ่า 417 หรือ 462 และกำลังคิดเรื่องคอร์สสั้น",
                   "nursing": "พยาบาลจากต่างประเทศ และคนที่อยากเริ่มเส้นทางสายพยาบาล",
                   "homestay": "อยู่กับครอบครัวเจ้าของบ้านช่วงที่มาถึงใหม่ๆ",
                   "health-cover": "ประกันสุขภาพนักเรียนต่างชาติ คืออะไร และซื้ออย่างไร",
                   "english": "แบบฝึกที่ทีมเราทำ ไม่มีค่าใช้จ่าย",
                   "partners": "โรงเรียน วิทยาลัย และผู้ให้บริการที่อยากทำงานร่วมกับเรา"},
        "more": "อ่านหน้าเต็ม", "moreStart": "ติดต่อเรา",
        "count": "{n} คำถาม", "still": "ยังมีคำถามอยู่ไหม ทีมงานอ่านทุกข้อความ",
        "book": "นัดเวลาคุย", "bookHref": "https://getwec.pages.dev/book/?lang=th",
        "top": "กลับไปที่หัวข้อ",
    },
}

# Thai pages exist for every topic page except none (all rebuilt pages have a /th twin).
def _href(path, lang):
    return "/th" + path if lang == "th" else path


def _json(name, lang):
    base = ROOT / "content" / ("th" if lang == "th" else "") / f"{name}.json"
    return json.loads(base.read_text())


def topics(lang="en"):
    """[(anchor, name, intro, link, [(q, answer_html)])] for the page and the tests."""
    ui = UI[lang]
    out = []
    for anchor, src, raw, link in TOPICS:
        if anchor == "start":
            home = _json("home", lang)["faq"]
            items = [(q, a if a.endswith("</a>") else e(a)) for q, a in GENERAL[lang]]  # trusted link only at the end + [(home[i][0], home[i][1]) for i in HOME_KEEP]
        elif anchor == "english":
            items = list(ENGLISH[lang])
        else:
            items = [(q, a if raw else e(a)) for q, a in _json(src, lang)["faq"]]
        out.append((anchor, ui["names"][anchor], ui["intros"][anchor], _href(link, lang), items))
    return out


def _text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def render(lang="en", visa_note="", cta=None):
    ui = UI[lang]
    ts = topics(lang)
    jump = "".join(f'<li><a href="#{a}">{e(n)} <span>{len(items)}</span></a></li>' for a, n, _, _, items in ts)
    blocks = []
    for a, n, intro, link, items in ts:
        qs = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{ans}</p></details>' for q, ans in items)
        more = ui["moreStart"] if a == "start" else ui["more"]
        blocks.append(
            f'<section class="faq-topic" id="{a}" aria-labelledby="{a}-h"><h2 id="{a}-h">{e(n)}</h2>'
            f'<p class="small">{e(intro)} · {e(ui["count"].format(n=len(items)))}</p>{qs}'
            f'<p class="faq-more"><a href="{link}">{e(more)} →</a> · <a href="#topics">{e(ui["top"])} ↑</a></p></section>')
    body = (f'<section class="wrap narrow"><p class="kicker">{e(ui["kicker"])}</p><h1>{e(ui["h1"])}</h1>'
            f'<p class="lead">{e(ui["lead"])}</p>'
            f'<nav id="topics" aria-label="{e(ui["jump"])}"><p class="small"><strong>{e(ui["jump"])}</strong></p>'
            f'<ul class="chips">{jump}</ul></nav>'
            + "".join(blocks) + visa_note
            + f'<div class="cta"><p>{e(ui["still"])}</p><a class="btn" href="{_href("/contact-us", lang)}">'
            + ("ส่งข้อความ" if lang == "th" else "Send a message")
            + f'</a> <a class="btn ghost" href="{ui["bookHref"]}">{e(ui["book"])}</a></div></section>')
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _text(ans)}}
        for _, _, _, _, items in ts for q, ans in items]}
    if lang == "th":
        ld["inLanguage"] = "th"
    return body, ld
