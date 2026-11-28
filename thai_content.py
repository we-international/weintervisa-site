"""Thai versions of the content pages (second set, 21 Nov 2026).

Same facts as content_pages.py, written in plain Thai for people (not raw machine translation).
Same rules: no promised prices, reply times, places, visas or jobs; visa questions go to a registered
migration agent; our team speaks Thai and English only; we receive no commission from listed agents.
Links point to the Thai page when one exists (TH), else to the English page.
"""
import html
import json
from pathlib import Path

import about_page
import content_pages as cp
import englishpractice_page
import fasttrack_page
import homestay_page
import nursing_page
import oshc_page

e = html.escape


def th_json(name):
    """Thai copy of a rebuilt page's content (content/th/<name>.json): same keys as the English JSON, plus "ui"."""
    return json.loads((Path(__file__).resolve().parent / "content/th" / f"{name}.json").read_text())

# English path → Thai path for this set (merged into thai_pages.TH_OF)
PAIRS = {p: "/th" + p for p in (
    "/about-we-international", "/courses/nursing-pathways-australia", "/fast-track-courses", "/english-practice",
    "/student-services", "/homestay", "/oshc", "/migration-support", "/referral-partners", "/frequently-asked-questions")}

VISA_NOTE_TH = """<p class="note-box"><strong>มีคำถามเรื่องวีซ่า?</strong> เราเป็นเอเจนซีการศึกษา ไม่ใช่ migration agent
คำแนะนำเรื่องวีซ่าของคุณ เราจะแนะนำ registered migration agent ให้ ไม่มีใครรับประกันผลวีซ่าได้</p>"""


def cta(text, second=None):
    extra = f' <a class="btn ghost" href="{second[1]}">{second[0]}</a>' if second else ""
    return f'<div class="cta"><p>{text}</p><a class="btn" href="/th/contact-us">ส่งข้อความ</a>{extra}</div>'


def simple(h1, lead, items, *, note=False, cta_text="มีคำถามไหม ทีมงานอ่านทุกข้อความ", second=None):
    body = "".join(f"<h2>{e(h)}</h2><p>{b}</p>" for h, b in items)
    return (f'<section class="wrap narrow"><h1>{e(h1)}</h1><p class="lead">{lead}</p>'
            f'{body}{VISA_NOTE_TH if note else ""}{cta(cta_text, second)}</section>')


nursing = nursing_page.render(th_json("nursing"))  # full page, same layout as the English one (22 Nov 2026)

fast_track = fasttrack_page.render(th_json("fast-track"))  # full page, same layout as the English one (22 Nov 2026)

english = englishpractice_page.render(th_json("english-practice"))  # full page, same layout as the English one (22 Nov 2026)

# Same sections as the English /student-services (22 Nov 2026), in Thai
services = f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">บริการนักเรียน</p>
<h1>ช่วยทุกขั้นตอนรอบๆ การเรียนของคุณ</h1>
<p class="lead">ช่วยให้เข้าใจตัวเลือกการเรียน จัดการใบสมัครเข้าสถาบัน และเตรียมตัวสำหรับก้าวต่อไป</p>
<p class="actions"><a class="btn" href="/th/contact-us">เริ่มคุยกับเรา</a> <a class="btn ghost" href="https://getwec.pages.dev/book/?lang=th">นัดเวลาคุย</a></p>
</div></section>
<section class="wrap">
<p class="kicker">ความช่วยเหลือรอบการเรียน</p>
<h2>ชัดเจนขึ้น ไม่ต้องเดา</h2>
<ul class="paths">
<li class="path"><h3>ปรึกษาเรื่องคอร์ส</h3><p>คุยให้ชัดว่าอยากเรียนเพื่ออะไร แล้วเทียบตัวเลือกการเรียนที่ยืนยันแล้ว</p><a href="/th/courses">ดูสาขาที่เรียน →</a></li>
<li class="path"><h3>ประสานงานการสมัคร</h3><p>เราช่วยติดตามเอกสารการเรียนที่ต้องใช้ สถานะใบสมัคร และคำตอบจากสถาบัน</p><a href="/th/charter-application">บอกเราว่าอยากเรียนอะไร →</a></li>
<li class="path"><h3>ดูแลนักเรียน</h3><p>ถามเราได้เรื่องข้อมูลปฐมนิเทศ ช่องทางติดต่อสถาบัน และการส่งต่อความช่วยเหลือ</p><a href="/th/contact-us">ถามทีมงาน →</a></li>
<li class="path"><h3>เรื่องภาษา</h3><p>Mia ผู้ช่วย AI ของเราคุยได้หลายภาษา ทีมงานของเราพูดภาษาไทยและอังกฤษ คำตอบจากทีมงานจึงเป็นภาษาไทยหรืออังกฤษ ศัพท์สำคัญของคอร์สเราคงเป็นภาษาอังกฤษไว้ จะได้ไม่คลาดเคลื่อน</p><a href="/th/english-practice">ฝึกภาษาอังกฤษ →</a></li>
</ul>
</section>
<section class="wrap">
<p class="kicker">ก่อนและหลังมาถึง</p>
<h2>ช่วยเรื่องที่ต้องจัดการจริง</h2>
<ul class="paths">
<li class="path"><h3>โฮมสเตย์</h3><p>เริ่มต้นกับครอบครัวเจ้าของบ้านที่ผ่านการคัดกรอง ใกล้สถาบันของคุณ กับพาร์ตเนอร์ของเรา AHN</p><a href="/th/homestay">หาโฮมสเตย์ →</a></li>
<li class="path"><h3>ประกันสุขภาพนักเรียน</h3><p>เทียบบริษัท OSHC แล้วซื้อได้เองบนเว็บไซต์ของพาร์ตเนอร์</p><a href="/th/oshc">เทียบ OSHC →</a></li>
<li class="path"><h3>คอร์สสำหรับ Working Holiday</h3><p>คอร์ส Certificate III สายอาชีพสำหรับผู้ถือวีซ่า 417 และ 462</p><a href="/th/fast-track-courses">ดูคอร์ส →</a></li>
<li class="path"><h3>เส้นทางสายพยาบาล</h3><p>เข้าใจขั้นตอนการขึ้นทะเบียน แล้วเตรียมภาษาอังกฤษ NCLEX-RN และ OSCE</p><a href="/th/courses/nursing-pathways-australia">เส้นทางสายพยาบาล →</a></li>
<li class="path"><h3>มากับครอบครัว?</h3><p>กิจกรรมการเรียนรู้แบบพิมพ์ได้สำหรับลูก และแผนการเรียนที่เข้ากับชีวิตครอบครัว</p><a href="/th/families">สำหรับครอบครัว →</a></li>
<li class="path"><h3>พักสมองสักนิด</h3><p>เรียนเหนื่อยแล้วพักสัก 5 นาทีกับเกมพัซเซิลจาก WE International Game Studio ในเครือของเรา</p><a href="/th/take-a-break">เล่นเกม →</a></li>
</ul>
</section>
<section class="wrap narrow">
<h2>ขั้นตอน</h2>
<ol class="flow flow3"><li><strong>บอกแผนของคุณ</strong><span>อยากเรียนอะไร ตอนนี้อยู่ที่ไหน และงบประมาณ</span></li>
<li><strong>เทียบตัวเลือก</strong><span>เราเช็กคอร์สที่เปิดอยู่และรายละเอียดกับสถาบัน</span></li>
<li><strong>สมัครและเตรียมตัว</strong><span>เราช่วยเรื่องใบสมัครเข้าสถาบันและขั้นต่อไป</span></li></ol>
{VISA_NOTE_TH}{cta("ขั้นต่อไปของคุณเริ่มจากการพูดคุย บอกเราว่าอยากเรียนอะไร")}
</section>"""

homestay = homestay_page.render(th_json("homestay"))  # full page, same layout as the English one (22 Nov 2026)

oshc = oshc_page.render(th_json("oshc"))  # full page, same layout as the English one (22 Nov 2026)

LABELS_TH = {"where": "ที่ตั้ง", "languages": "ภาษา", "markets": "ลูกค้าจาก", "visa": "ประเภทวีซ่า", "contact": "ติดต่อ",
             "online": " · ให้บริการออนไลน์ทั่วออสเตรเลีย", "visit": "ไปที่หน้า migration ของเขา",
             "empty": ('<p class="note-box"><strong>รายชื่อกำลังจะมา</strong> ตอนนี้เรากำลังตรวจสอบเอเจนต์ชุดแรก '
                       'ระหว่างนี้ <a href="/th/contact-us">ส่งข้อความขอให้เราแนะนำได้</a></p>')}

migration = f"""<section class="wrap narrow"><h1>ความช่วยเหลือเรื่องวีซ่าและการย้ายถิ่นฐาน</h1>
<p class="lead">การช่วยเรื่องเรียนกับการให้คำแนะนำวีซ่าเป็นคนละงานกัน เราช่วยเรื่องการเรียน ส่วนคำถามวีซ่า ให้เลือกเอเจนต์ด้านวีซ่าที่ขึ้นทะเบียน (registered migration agent)</p>
<h2>สิ่งที่เราทำ</h2><p>ตอบคำถามเรื่องคอร์ส นัดเวลาคุย และจัดการเอกสารการเรียนสำหรับใบสมัครเข้าสถาบัน</p>
<h2>คำแนะนำเรื่องวีซ่า</h2><p>การประเมินสิทธิ์ วางแผน และยื่นวีซ่า ต้องทำโดยเอเจนต์ด้านวีซ่าที่ขึ้นทะเบียนหรือทนายความเท่านั้น ผู้ช่วย AI ของเราก็ไม่ได้ให้คำแนะนำเรื่องวีซ่า</p>
<h2 id="agents">รายชื่อเอเจนต์ด้านวีซ่าที่ขึ้นทะเบียน</h2>
<p>เราไม่ได้ให้คำแนะนำเรื่องวีซ่า เพื่อให้คุณมีตัวเลือกมากขึ้น เราจึงลงรายชื่อเอเจนต์ด้านวีซ่าที่ขึ้นทะเบียน และทำงานด้านวีซ่าและการย้ายถิ่นฐานอย่างเดียว
<strong>เราไม่ได้รับค่าคอมมิชชันหรือผลประโยชน์ใดๆ จากเอเจนต์ในรายชื่อ</strong> เอเจนต์แต่ละรายกรอกข้อมูลและขอลงรายชื่อเอง
เราตรวจเลข MARN ทุกรายในทะเบียนทางการก่อนลงรายชื่อ แต่ขอให้คุณเช็กด้วยตัวเองอีกครั้ง และคุยกับเอเจนต์โดยตรง ไม่มีใครรับประกันผลวีซ่าได้</p>
{cp.partner_cards(cp.MIGRATION_PARTNERS, LABELS_TH)}
<p class="small">เป็นเอเจนต์ด้านวีซ่าที่ขึ้นทะเบียน และทำงานด้านวีซ่าอย่างเดียวใช่ไหม <a href="{cp.PARTNER_FORM}" target="_blank" rel="noopener">ลงรายชื่อสำนักงานของคุณ</a> (ไม่มีค่าใช้จ่าย ฟอร์มเป็นภาษาอังกฤษ)</p>
{VISA_NOTE_TH}{cta("ไม่แน่ใจว่าควรถามใคร ส่งข้อความมา เราจะแนะนำเอเจนต์ด้านวีซ่าที่ขึ้นทะเบียนให้")}</section>"""

partners = about_page.partners(th_json("referral-partners"))  # full page, same layout as the English one (22 Nov 2026)

import faq_page  # noqa: E402 — same topics and answers as the English help page (22 Nov 2026)
faq_body, faq_ld = faq_page.render("th", VISA_NOTE_TH)

about = about_page.about(th_json("about"))  # full page, same layout as the English one (22 Nov 2026)

PAGES = {
    "th/about-we-international": ("เกี่ยวกับเรา | We International",
        "We International เป็นเอเจนซีการศึกษาในซิดนีย์ ช่วยนักเรียนวางแผนเรียนต่อออสเตรเลียอย่างตรงไปตรงมา โดยคิดถึงนักเรียนก่อน", about),
    "th/courses/nursing-pathways-australia": ("เส้นทางสายพยาบาลในออสเตรเลีย | ภาษาอังกฤษและเตรียมสอบ",
        "ขั้นตอนขึ้นทะเบียนพยาบาลในออสเตรเลีย และการเตรียมตัวเรื่องภาษาอังกฤษ NCLEX-RN และ OSCE ถาม We International เรื่องค่าเรียนและวันเริ่มเรียน", nursing),
    "th/fast-track-courses": ("เรียนระหว่าง Working Holiday | We International",
        "ถือวีซ่า 417 หรือ 462 อยู่ใช่ไหม เรียน Certificate III สายดูแล ผู้ช่วยงานสุขภาพ หรือปฐมวัย พร้อมฝึกงาน และจัดการโฮมสเตย์กับประกันสุขภาพในที่เดียว", fast_track),
    "th/english-practice": ("ฝึกภาษาอังกฤษ ไม่มีค่าใช้จ่าย | We International",
        "ฝึกภาษาอังกฤษไม่มีค่าใช้จ่าย: ควิซข้อผิดที่เจอบ่อย 8 ข้อ ช่อง Say It Wrong และ Wobbi Says เกม และคอร์สภาษาอังกฤษในออสเตรเลีย", english),
    "th/student-services": ("บริการนักเรียน | We International",
        "ช่วยเลือกคอร์ส สมัครกับสถาบัน และเตรียมตัวก่อนเริ่มเรียนในออสเตรเลีย ทีมงานตอบภาษาไทยหรืออังกฤษ", services),
    "th/homestay": ("โฮมสเตย์และที่พักนักเรียน | We International",
        "เริ่มชีวิตในออสเตรเลียกับโฮมสเตย์ของ AHN: บ้านที่ผ่านการตรวจ อาหาร ค่าน้ำค่าไฟ และสายด่วน 24 ชั่วโมง พร้อมราคา 2026/2027 และขั้นตอนสมัคร", homestay),
    "th/oshc": ("ประกันสุขภาพนักเรียน (OSHC) | We International",
        "เทียบประกันสุขภาพนักเรียน OSHC จาก Allianz, Bupa, Medibank และ AHM แล้วซื้อบนเว็บไซต์พาร์ตเนอร์ พร้อมเรื่องที่ต้องเช็กก่อนซื้อ", oshc),
    "th/migration-support": ("ความช่วยเหลือเรื่องวีซ่า | We International",
        "เราช่วยเรื่องการเรียน คำถามวีซ่าให้เลือกเอเจนต์ด้านวีซ่าที่ขึ้นทะเบียน เราไม่ได้รับค่าคอมมิชชันจากเอเจนต์ในรายชื่อ", migration),
    "th/referral-partners": ("ร่วมงานกับเรา | We International",
        "สถาบันการศึกษา วิทยาลัย และผู้ให้บริการนักเรียน คุยกับ We International เรื่องการทำงานร่วมกันได้", partners),
    "th/frequently-asked-questions": ("คำถามที่พบบ่อย | We International",
        "คำตอบเรื่องเรียนต่อ คอร์ส Working Holiday พยาบาล โฮมสเตย์ ประกันสุขภาพ (OSHC) และการทำงานกับ We International ในออสเตรเลีย", faq_body),
}
JSONLD = {"th/frequently-asked-questions": faq_ld}
