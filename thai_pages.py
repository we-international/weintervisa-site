"""Thai pages of the new weintervisa.com (owner, 20 Nov 2026: every page needs English + Thai,
/th/... + hreflang, Thai written for people, not raw machine translation).

First set (21 Nov 2026): home /th/, contact /th/contact-us, study application /th/charter-application.
Pages without a Thai version yet keep a "ไทย" link to /th/ in the header, and Thai pages link to the
English page where no Thai page exists. Add a page here = add an entry to TH_PAGES (Thai path → English path).

Same rules as English: no promised prices, reply times, places, visas or jobs; visa questions go to
a registered migration agent; our team speaks Thai and English only.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
e = html.escape

# English path → Thai path, for pages that exist in both languages.
import thai_content

TH_OF = {"/": "/th/", "/contact-us": "/th/contact-us", "/charter-application": "/th/charter-application", **thai_content.PAIRS}
EN_OF = {v: k for k, v in TH_OF.items()}

NAV_TH = [  # Thai labels; link to the Thai page when it exists, else the English one
    ("คอร์สเรียน", "/courses"),
    ("Fast-track", "/th/fast-track-courses"),
    ("บริการนักเรียน", "/th/student-services"),
    ("บทความ", "/blog"),
    ("ติดต่อเรา", "/th/contact-us"),
]

GROUP_TH = {
    "Business & Technology": "ธุรกิจและเทคโนโลยี",
    "Care & Community": "งานดูแลและชุมชน",
    "Creative & Other Studies": "งานสร้างสรรค์และสาขาอื่น",
    "English & Pathways": "ภาษาอังกฤษและเส้นทางต่อยอด",
    "Hospitality & Lifestyle": "การโรงแรมและไลฟ์สไตล์",
    "Trades & Built Environment": "งานช่างและก่อสร้าง",
}

FOOT_TH = ("เราช่วยเรื่องการเรียนและคอร์สในออสเตรเลีย เราไม่ใช่ migration agent "
           "เรื่องคำแนะนำวีซ่า เราจะแนะนำ registered migration agent ให้")


def group_anchor(g):  # same ids as the h2s on /courses
    return g.lower().replace(" & ", "-").replace(" ", "-")


VISA_NOTE_TH = """<p class="note-box"><strong>มีคำถามเรื่องวีซ่า?</strong> เราเป็นเอเจนซีการศึกษา ไม่ใช่ migration agent
เราให้ข้อมูลทั่วไปเรื่องคอร์สและการเรียนได้ ส่วนคำแนะนำเรื่องวีซ่าของคุณ เราจะแนะนำ registered migration agent ให้</p>"""


def home(posts, fmt_date):
    areas = json.loads((ROOT / "content/study-areas.json").read_text())
    groups = {}
    for a in areas:
        groups.setdefault(a["group"], []).append(a)
    chips = "".join(f'<li><a href="/courses#{e(group_anchor(g))}">{e(GROUP_TH.get(g, g))} <span>{len(items)}</span></a></li>'
                    for g, items in groups.items())
    why = [
        ("คอร์สที่ใช่สำหรับคุณ", "เริ่มจากสิ่งที่คุณสนใจ วุฒิที่เรียนมา เมืองที่อยากอยู่ และงบประมาณ เราช่วยเทียบตัวเลือกที่เหมาะ เมื่อมีข้อมูลล่าสุดจากสถาบัน"),
        ("ตัวเลือกชัด ดูแลตรงไปตรงมา", "รู้ว่าอะไรยืนยันแล้ว อะไรต้องเช็กเพิ่ม และขั้นต่อไปคืออะไร คุณเป็นคนตัดสินใจเรื่องการเรียนเองเสมอ"),
        ("คุยในภาษาของคุณ", "คุยกับ Mia ผู้ช่วย AI ของเราได้ทุกภาษา ตลอดเวลา ส่วนทีมงานของเราตอบเป็นภาษาไทยหรืออังกฤษ"),
    ]
    why_html = "".join(f"<li><strong>{e(h)}</strong><span>{e(b)}</span></li>" for h, b in why)
    tiles = [
        ("/courses", "คอร์สเรียน", "ภาษาอังกฤษ งานดูแล ธุรกิจ งานช่าง ไอที และอื่นๆ"),
        ("/th/fast-track-courses", "Fast-track สำหรับ Working Holiday", "แผนเรียนสั้นที่เข้ากับวีซ่า 417 หรือ 462 เช็กเงื่อนไขก่อนเสมอ"),
        ("/th/courses/nursing-pathways-australia", "เส้นทางสายพยาบาล", "ขั้นตอนหลักสำหรับพยาบาลที่เรียนจบจากนอกออสเตรเลีย"),
        ("/th/english-practice", "เรียนภาษาอังกฤษ", "เสริมภาษาอังกฤษสำหรับการเรียน การทำงาน และชีวิตประจำวัน"),
        ("/th/student-services", "บริการนักเรียน", "โฮมสเตย์ ประกันสุขภาพ และการดูแลระหว่างเรียน"),
        ("/th/referral-partners", "พาร์ตเนอร์แนะนำนักเรียน", "ร่วมงานกับเราเพื่อแนะนำนักเรียน"),
    ]
    tiles_html = "".join(f'<a class="tile" href="{p}"><strong>{e(t)}</strong><span>{e(d)}</span></a>' for p, t, d in tiles)
    cards = "".join(f"""<li class="card"><a href="/post/{p['slug']}">
{f'<img src="{e(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else '<div class="noimg"></div>'}
<span class="date">{fmt_date(p["date"])}</span><strong>{e(p["title"])}</strong></a></li>""" for p in posts[:3])
    return f"""<section class="hero"><div class="wrap">
<p class="kicker">เรียนต่อออสเตรเลีย</p>
<h1>บทใหม่ของคุณ เริ่มจากการเลือกที่ดีกว่า</h1>
<p class="lead">ดูสาขาที่น่าสนใจ เข้าใจตัวเลือกของคุณ แล้วก้าวต่อไปอย่างมั่นใจ กับทีมที่คิดถึงนักเรียนก่อน</p>
<p class="actions"><a class="btn" href="/courses">ดูคอร์สเรียน</a> <a class="btn ghost" href="/th/contact-us">ถามทีมงาน</a></p>
</div></section>
<section class="wrap">
<h2>เริ่มจากสาขาที่สนใจ</h2>
<p>เลือกกลุ่มเพื่อดูสาขาในกลุ่มนั้น (หน้ารายละเอียดเป็นภาษาอังกฤษ) เราเช็กรายละเอียดคอร์สล่าสุดกับสถาบันก่อนส่งให้คุณเสมอ</p>
<ul class="chips">{chips}</ul>
</section>
<section class="wrap">
<h2>เราช่วยอะไรได้บ้าง</h2>
<ul class="why">{why_html}</ul>
</section>
<section class="wrap">
<h2>ขั้นตอนง่ายๆ</h2>
<ol class="flow">
<li><strong>สำรวจ</strong><span>ดูสาขาที่คุณสนใจ</span></li>
<li><strong>ถาม</strong><span>ส่งข้อความถามตัวเลือกที่เปิดรับตอนนี้</span></li>
<li><strong>เทียบ</strong><span>ดูคอร์ส ค่าเรียน วิทยาเขต และวันเริ่มเรียนเทียบกัน</span></li>
<li><strong>ตัดสินใจ</strong><span>ไปต่อเมื่อคุณพร้อมเท่านั้น เป็นการตัดสินใจของคุณ</span></li>
</ol>
</section>
<section class="wrap">
<h2>หน้าที่คนดูบ่อย</h2>
<div class="grid3">{tiles_html}</div>
<p class="note-box"><strong>มีคำถามเรื่องวีซ่า?</strong> เราเป็นเอเจนซีการศึกษา ไม่ใช่ migration agent
คำแนะนำเรื่องวีซ่า เราจะแนะนำ registered migration agent ให้ ไม่มีใครรับประกันผลวีซ่าได้</p>
</section>
<section class="wrap">
<h2>บทความล่าสุด (ภาษาอังกฤษ)</h2>
<ul class="cards">{cards}</ul>
<p><a href="/blog">บทความทั้งหมด {len(posts)} เรื่อง</a></p>
<aside class="cta"><p>คุยกับ Mia ผู้ช่วย AI ได้ทุกภาษา ทีมงานของเราตอบเป็นภาษาไทยหรืออังกฤษ</p><a class="btn" href="/th/contact-us">ส่งข้อความ</a></aside>
</section>"""


CONSENT_TH = """<div class="field check">
  <label><input type="checkbox" name="consent" required> <span>ฉันยินยอมให้ We International Education &amp; Visa Pty Ltd เก็บข้อมูลนี้ไว้เพื่อติดต่อกลับเรื่องที่สอบถาม (<a href="/privacy-policy">นโยบายความเป็นส่วนตัว</a>)</span></label>
  <span class="err" data-err="consent"></span>
</div>
<div class="field check">
  <label><input type="checkbox" name="marketing"> <span>ส่งข่าวคอร์สและข้อเสนอทางอีเมล (ไม่บังคับ ยกเลิกได้ทุกเมื่อ)</span></label>
</div>
<div class="hp" aria-hidden="true"><label>เว้นช่องนี้ว่างไว้ <input name="website" tabindex="-1" autocomplete="off"></label></div>"""

CONTACT_FIELDS_TH = """<div class="field"><label for="{k}-name">ชื่อ-นามสกุล *</label>
  <input id="{k}-name" name="full_name" autocomplete="name" required maxlength="120"><span class="err" data-err="full_name"></span></div>
<div class="row2">
  <div class="field"><label for="{k}-email">อีเมล</label>
    <input id="{k}-email" name="email" type="email" autocomplete="email" maxlength="200"><span class="err" data-err="email"></span></div>
  <div class="field"><label for="{k}-phone">เบอร์โทร หรือ LINE ID</label>
    <input id="{k}-phone" name="phone" autocomplete="tel" maxlength="60"></div>
</div>
<p class="hint">ใส่อีเมล หรือเบอร์โทร / LINE อย่างใดอย่างหนึ่งก็พอ</p>
<div class="field"><label for="{k}-loc">ตอนนี้คุณอยู่ที่ไหน</label>
  <select id="{k}-loc" name="location" data-summary="Now in"><option value="">เลือก…</option>
  <option value="australia">อยู่ออสเตรเลีย</option><option value="thailand">อยู่ไทย</option><option value="other">ที่อื่น</option></select></div>"""

contact_form = f"""<form class="lead" data-lead-form="enquiry" novalidate>
<h2>ส่งข้อความถึงเรา</h2>
{CONTACT_FIELDS_TH.format(k="c")}
<div class="field"><label for="c-topic">เรื่องที่อยากถาม</label>
  <select id="c-topic" name="topic" data-summary="Topic"><option value="">เลือก…</option>
  <option>คอร์สและสถาบัน</option><option>คอร์ส Fast-track</option><option>โฮมสเตย์</option>
  <option>OSHC (ประกันสุขภาพนักเรียน)</option><option>พาร์ตเนอร์ (สถาบันหรือเอเจนต์)</option><option>เรื่องอื่น</option></select></div>
<div class="field"><label for="c-msg">ข้อความของคุณ</label>
  <textarea id="c-msg" name="message" rows="5" maxlength="800"></textarea></div>
{CONSENT_TH}
<button class="btn" type="submit">ส่งข้อความ</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>"""

contact_body = f"""<section class="wrap narrow">
<h1>ติดต่อเรา</h1>
<p class="lead">ถามเรื่องคอร์ส สถาบัน โฮมสเตย์ หรือประกันสุขภาพนักเรียนได้เลย ทีมงานอ่านทุกข้อความ และตอบเป็นภาษาไทยหรืออังกฤษ</p>
<ul class="contact-list">
  <li><strong>อีเมล</strong> <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></li>
  <li><strong>บทความ</strong> <a href="/blog">คู่มือเรื่องคอร์สและชีวิตในออสเตรเลีย</a> (ภาษาอังกฤษ)</li>
</ul>
{VISA_NOTE_TH}
{contact_form}
</section>"""

apply_form = f"""<form class="lead" data-lead-form="application" novalidate>
<h2>ข้อมูลของคุณ</h2>
{CONTACT_FIELDS_TH.format(k="a")}
<h2>อยากเรียนอะไร</h2>
<div class="field"><label for="a-field">สาขา</label>
  <select id="a-field" name="field" data-summary="Course area"><option value="">เลือก…</option>
  <option>งานดูแลผู้สูงอายุ / Individual support</option><option>เส้นทางพยาบาล</option><option>การศึกษาปฐมวัย</option>
  <option>ผู้ช่วยงานบริการสุขภาพ</option><option>ภาษาอังกฤษ</option><option>ธุรกิจ / สาขาอื่น</option><option>ยังไม่แน่ใจ</option></select></div>
<div class="row2">
  <div class="field"><label for="a-level">ระดับ</label>
    <select id="a-level" name="level" data-summary="Level"><option value="">เลือก…</option>
    <option>คอร์สสั้น</option><option>Certificate III</option><option>Certificate IV</option><option>Diploma</option>
    <option>ปริญญาตรีขึ้นไป</option><option>ยังไม่แน่ใจ</option></select></div>
  <div class="field"><label for="a-start">อยากเริ่มเรียนเมื่อไหร่</label>
    <input id="a-start" name="start" type="month" data-summary="Start"></div>
</div>
<div class="row2">
  <div class="field"><label for="a-city">เมืองที่อยากเรียน</label>
    <select id="a-city" name="city" data-summary="City"><option value="">เลือก…</option>
    <option>Sydney</option><option>Melbourne</option><option>Brisbane</option><option>Perth</option><option>Adelaide</option>
    <option>เรียนออนไลน์</option><option>ที่ไหนก็ได้</option></select></div>
  <div class="field"><label for="a-eng">ภาษาอังกฤษของคุณ</label>
    <select id="a-eng" name="english" data-summary="English"><option value="">เลือก…</option>
    <option>เริ่มต้น</option><option>คุยเรื่องทั่วไปได้</option><option>ดี / ใช้ทำงานได้</option>
    <option>มีผลสอบ (IELTS, PTE…)</option></select></div>
</div>
<div class="field"><label for="a-visa">ถ้าอยู่ออสเตรเลีย: วีซ่าปัจจุบันของคุณ (ไม่บังคับ)</label>
  <input id="a-visa" name="visa" maxlength="60" placeholder="เช่น Working Holiday 417" data-summary="Current visa"></div>
<div class="field"><label for="a-msg">มีอะไรอยากบอกเราเพิ่มไหม</label>
  <textarea id="a-msg" name="message" rows="4" maxlength="800"></textarea></div>
<p class="hint">กรุณาอย่าส่งเลขพาสปอร์ตหรือเอกสารในฟอร์มนี้ ถ้าต้องใช้ เราจะส่งช่องทางที่ปลอดภัยให้</p>
{CONSENT_TH}
<button class="btn" type="submit">ส่งใบสมัคร</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>"""

apply_body = f"""<section class="wrap narrow">
<h1>สมัครเรียน</h1>
<p class="lead">บอกเราว่าอยากเรียนอะไร ทีมงานจะเช็กตัวเลือกคอร์สและเงื่อนไขการรับเข้าเรียนกับคุณ แล้วช่วยสมัครกับสถาบัน</p>
<ol class="steps"><li>ส่งฟอร์มนี้</li><li>เราติดต่อกลับเพื่อคุยเรื่องคอร์ส</li><li>คุณเลือกคอร์ส แล้วเราช่วยสมัครกับสถาบัน</li></ol>
{VISA_NOTE_TH}
{apply_form}
</section>"""

# Thai path (no leading slash, file name) → (title, description, body)
TH_PAGES = {
    "th/contact-us": ("ติดต่อเรา | We International",
                      "ถาม We International เรื่องคอร์ส สถาบัน โฮมสเตย์ หรือประกันสุขภาพนักเรียนในออสเตรเลีย ทีมงานตอบภาษาไทยหรืออังกฤษ",
                      contact_body),
    "th/charter-application": ("สมัครเรียน | We International",
                               "บอกเราว่าอยากเรียนอะไรในออสเตรเลีย ทีมงานจะติดต่อกลับเรื่องตัวเลือกคอร์ส",
                               apply_body),
    **thai_content.PAGES,
}
JSONLD = thai_content.JSONLD

HOME_TITLE = "เรียนต่อออสเตรเลีย | We International Education & Visa"
HOME_DESC = "ดูสาขาที่น่าสนใจ เข้าใจตัวเลือกของคุณ แล้วก้าวต่อไปอย่างมั่นใจ กับทีมที่คิดถึงนักเรียนก่อน ทีมงานตอบภาษาไทยหรืออังกฤษ"
