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
import thai_more

TH_OF = {"/": "/th/", "/contact-us": "/th/contact-us", "/charter-application": "/th/charter-application", **thai_content.PAIRS, **thai_more.PAIRS}
EN_OF = {v: k for k, v in TH_OF.items()}

NAV_TH = [  # Thai labels; link to the Thai page when it exists, else the English one
    ("คอร์สเรียน", "/th/courses"),
    ("Fast-track", "/th/fast-track-courses"),
    ("บริการนักเรียน", "/th/student-services"),
    ("บทความ", "/th/blog"),
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
    """Thai home: the same layout as the English home (rebuilt from live Wix), from content/th/home.json (22 Nov 2026)."""
    import home_page
    th = json.loads((ROOT / "content/th/home.json").read_text())
    return home_page.render(posts, fmt_date, th, group_label=lambda g: GROUP_TH.get(g, g))


CONSENT_TH = """<div class="field check">
  <label><input type="checkbox" name="consent" required> <span>ฉันยินยอมให้ We International Education &amp; Visa Pty Ltd เก็บข้อมูลนี้ไว้เพื่อติดต่อกลับเรื่องที่สอบถาม (<a href="/th/privacy-policy">นโยบายความเป็นส่วนตัว</a>)</span></label>
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

BOOK_TH = "https://getwec.pages.dev/book/?lang=th"  # GetWec booking page in Thai (replaces Wix /schedule)

# Same sections as the English /contact-us (rebuilt 22 Nov 2026), in Thai
contact_body = f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">ติดต่อทีมงาน</p>
<h1>มาคุยเรื่องบทต่อไปของคุณกัน</h1>
<p class="lead">เริ่มจากคำถามก็ได้ บอกเราว่าอยากเรียนอะไร ตอนนี้อยู่ที่ไหน และสะดวกคุยภาษาไหน (ไทยหรืออังกฤษ)</p>
<p class="actions"><a class="btn" href="#enquiry">ส่งคำถาม ↓</a> <a class="btn ghost" href="{BOOK_TH}">นัดเวลาคุย</a></p>
</div></section>
<section class="wrap">
<h2>ช่องทางติดต่อเรา</h2>
<ul class="paths">
<li class="path"><h3>ส่งข้อความ</h3><p>ใช้ฟอร์มในหน้านี้ เขียนเป็นภาษาไทยหรืออังกฤษก็ได้</p><a href="#enquiry">ไปที่ฟอร์ม ↓</a></li>
<li class="path"><h3>แชทผ่าน Messenger</h3><p>ส่งข้อความหาเพจ Facebook ของเรา</p><a href="https://m.me/113772648238480" target="_blank" rel="noopener">เปิด Messenger ↗</a></li>
<li class="path"><h3>เริ่มทางอีเมล</h3><p>เขียนหาเราได้ทุกเมื่อ</p><a href="mailto:info@weintervisa.com">info@weintervisa.com</a></li>
<li class="path"><h3>นัดเวลาคุย</h3><p>เลือกหัวข้อ วิธีคุย (โทรศัพท์ วิดีโอ LINE หรืออีเมล) และวันที่สะดวก แล้วเราจะยืนยันเวลากับคุณ</p><a href="{BOOK_TH}">นัดเวลาคุย →</a></li>
</ul>
<p><strong>ออนไลน์ ไม่ว่าคุณอยู่ที่ไหน</strong> เราทำงานออนไลน์ และจะยืนยันช่องทางติดต่อกับเวลานัดกับคุณ
Mia ผู้ช่วย AI ของเราคุยได้หลายภาษา ทีมงานของเราพูดภาษาไทยและอังกฤษ คำตอบจากทีมงานจึงเป็นภาษาไทยหรืออังกฤษ</p>
</section>
<section class="wrap narrow" id="enquiry">
<p class="kicker">คุยกับทีมงาน</p>
<p>เล่าแผนของคุณให้เราฟัง กรุณาอย่าแนบพาสปอร์ต รายการเดินบัญชี หรือเอกสารวีซ่า เพราะนี่คือการสอบถามเรื่องเรียนหรือบริการ ไม่ใช่การยื่นวีซ่า
ข้อความจะถูกส่งเมื่อคุณกดส่งฟอร์มและเห็นข้อความยืนยันเท่านั้น อ่าน<a href="/th/privacy-policy">นโยบายความเป็นส่วนตัว</a>ว่าเราดูแลข้อมูลของคุณอย่างไร</p>
{contact_form}
{VISA_NOTE_TH}
</section>
<section class="wrap">
<h2>เลือกจุดเริ่มต้น</h2>
<ul class="paths">
<li class="path"><h3>มีคำถามเรื่องเรียน?</h3><p>เราช่วยคุณสำรวจตัวเลือกการเรียนได้</p><a href="/th/courses">ดูสาขาที่เรียน →</a></li>
<li class="path"><h3>ถือวีซ่า Working Holiday?</h3><p>คอร์ส Certificate III สายอาชีพสำหรับผู้ถือวีซ่า 417/462</p><a href="/th/fast-track-courses">ดูคอร์สสำหรับ Working Holiday →</a></li>
<li class="path"><h3>เป็นสถาบันหรือผู้ให้บริการ?</h3><p>เล่าเรื่องสถาบันหรือบริการของคุณให้เราฟัง</p><a href="/th/referral-partners">ร่วมงานกับเรา →</a></li>
<li class="path"><h3>อยากได้คำตอบก่อน?</h3><p>เริ่มจากคำถามที่พบบ่อย</p><a href="/th/frequently-asked-questions">ดูคำถามที่พบบ่อย →</a></li>
</ul>
<ul class="contact-list">
  <li><strong>อีเมล</strong> <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></li>
  <li><strong>บทความ</strong> <a href="/th/blog">คู่มือเรื่องคอร์สและชีวิตในออสเตรเลีย</a> (ภาษาอังกฤษ)</li>
</ul>
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
    **thai_more.PAGES,
}
JSONLD = thai_content.JSONLD

HOME_TITLE = "เรียนต่อออสเตรเลีย | We International Education & Visa"
HOME_DESC = "ไม่ว่าคุณถือวีซ่าอะไร เราช่วยหาคอร์สที่เหมาะ เทียบตัวเลือก และช่วยให้คุณตั้งหลักในออสเตรเลีย ปรึกษากับที่ปรึกษา QEAC ใน Sydney โดยไม่มีค่าใช้จ่าย ทีมงานตอบภาษาไทยหรืออังกฤษ"
