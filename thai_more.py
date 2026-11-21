"""Thai pages, third set (21 Nov 2026): /th/courses, /th/blog, /th/schools and /th/schools/<slug>.

Same facts as the English pages, in plain Thai written for people. Names that are English proper names
(course titles, blog post titles, campus names) stay English and are marked lang="en" so screen readers
read them right; the "body mainly Thai" test ignores lang="en" parts.
School pages follow the school rules (schools.py): only schools that replied, only what they sent,
"approved": false = preview only (production leaves them out until the owner approves).
/th/privacy-policy: Thai copy of the owner-approved English notice (owner said go ahead, 21 Nov 2026); English applies if they differ.
"""
import html
import json
from pathlib import Path

import schools

ROOT = Path(__file__).resolve().parent
e = html.escape

GROUP_TH = {
    "Business & Technology": "ธุรกิจและเทคโนโลยี",
    "Care & Community": "งานดูแลและชุมชน",
    "Creative & Other Studies": "งานสร้างสรรค์และสาขาอื่น",
    "English & Pathways": "ภาษาอังกฤษและเส้นทางต่อยอด",
    "Hospitality & Lifestyle": "การโรงแรมและไลฟ์สไตล์",
    "Trades & Built Environment": "งานช่างและก่อสร้าง",
}

# slug → (Thai name, Thai one-liner). Same meaning as the CMS description, no new promises.
AREA_TH = {
    "general-english": ("ภาษาอังกฤษทั่วไป", "ฝึกภาษาอังกฤษสำหรับการเรียน การทำงาน และชีวิตประจำวัน"),
    "ielts-preparation": ("เตรียมสอบ IELTS", "เตรียมตัวสอบ IELTS และวางแผนการเรียนขั้นต่อไป"),
    "pte-preparation": ("เตรียมสอบ PTE", "เตรียมตัวสอบภาษาอังกฤษและดูตัวเลือกการเรียน"),
    "academic-english": ("ภาษาอังกฤษเพื่อการเรียน", "เตรียมภาษาให้พร้อมสำหรับการเรียนต่อ"),
    "foundation-university-pathways": ("Foundation และเส้นทางเข้ามหาวิทยาลัย", "คอร์สเตรียมตัวและเส้นทางก่อนเรียนปริญญา"),
    "business-leadership": ("ธุรกิจและภาวะผู้นำ", "การบริหารงาน การจัดการ และภาวะผู้นำ"),
    "accounting-finance": ("บัญชีและการเงิน", "บัญชี การทำบัญชี และการเงิน"),
    "marketing-digital-media": ("การตลาดและสื่อดิจิทัล", "การตลาด การสื่อสาร และแคมเปญออนไลน์"),
    "project-management": ("การบริหารโครงการ", "การวางแผนและประสานงานโครงการ"),
    "human-resources": ("ทรัพยากรบุคคล", "งานบุคคล การสรรหา และการจัดการในที่ทำงาน"),
    "information-technology": ("เทคโนโลยีสารสนเทศ", "คอมพิวเตอร์ เครือข่าย และงานซัพพอร์ตไอที"),
    "software-web-development": ("พัฒนาซอฟต์แวร์และเว็บ", "การเขียนโปรแกรม ซอฟต์แวร์ และเว็บไซต์"),
    "cybersecurity": ("ความปลอดภัยไซเบอร์", "ความปลอดภัยของข้อมูลและการป้องกันภัยไซเบอร์"),
    "data-artificial-intelligence": ("ข้อมูลและปัญญาประดิษฐ์", "การวิเคราะห์ข้อมูล วิทยาการข้อมูล และ AI"),
    "supply-chain-logistics": ("ซัพพลายเชนและโลจิสติกส์", "การขนส่ง การจัดซื้อ และการจัดการซัพพลายเชน"),
    "early-childhood-education": ("การศึกษาปฐมวัย", "การเรียนรู้และการดูแลเด็กเล็ก"),
    "individual-support": ("งานดูแลบุคคล (Individual Support)", "ดูแลผู้คนในสถานดูแลและในชุมชน"),
    "ageing-support": ("งานดูแลผู้สูงอายุ", "บริการและการดูแลผู้สูงอายุ"),
    "disability-support": ("งานดูแลผู้พิการ", "การดูแลผู้พิการโดยให้ความสำคัญกับตัวบุคคล"),
    "community-services": ("งานบริการชุมชน", "งานช่วยเหลือชุมชน ประสานเคส และให้บริการ"),
    "health-services-assistance": ("ผู้ช่วยงานบริการสุขภาพ", "งานผู้ช่วยและการเรียนรู้ในสถานบริการสุขภาพ"),
    "nursing": ("พยาบาล", "การเรียนพยาบาล ต้องเช็กเกณฑ์รับเข้าและการขึ้นทะเบียนของแต่ละคอร์ส"),
    "allied-health": ("สหเวชศาสตร์", "การเรียนสาขาต่างๆ ในกลุ่มสหเวชศาสตร์"),
    "social-work-counselling": ("สังคมสงเคราะห์และการให้คำปรึกษา", "งานสังคมสงเคราะห์ สุขภาวะ และการให้คำปรึกษา"),
    "education-teaching": ("การศึกษาและการสอน", "การศึกษาและวุฒิครู"),
    "commercial-cookery": ("การทำอาหาร (Commercial Cookery)", "การทำอาหารและการทำงานในครัวแบบลงมือจริง"),
    "patisserie-baking": ("ขนมอบและเบเกอรี", "ขนมอบ เบเกอรี และการผลิตอาหาร"),
    "hospitality-management": ("การจัดการการโรงแรม", "งานโรงแรม การดูแลแขก และการบริหาร"),
    "tourism-events": ("การท่องเที่ยวและอีเวนต์", "การท่องเที่ยวและการจัดงานอีเวนต์"),
    "beauty-hairdressing": ("ความงามและทำผม", "งานบริการความงาม ทำผม และงานซาลอน"),
    "fitness-sport": ("ฟิตเนสและกีฬา", "ฟิตเนส กีฬา และนันทนาการ"),
    "massage-wellness": ("นวดและเวลเนส", "ตัวเลือกการเรียนด้านการนวดและเวลเนส"),
    "automotive": ("ยานยนต์", "เทคโนโลยียานยนต์ การบริการ และการซ่อม"),
    "carpentry-construction": ("งานไม้และก่อสร้าง", "งานก่อสร้าง งานไม้ และการสร้างอาคาร"),
    "electrical-engineering-trades": ("ช่างไฟฟ้าและช่างวิศวกรรม", "งานช่างไฟฟ้าและงานช่างด้านวิศวกรรม"),
    "engineering": ("วิศวกรรม", "สาขาวิศวกรรมและการเรียนด้านเทคนิค"),
    "architecture-design": ("สถาปัตยกรรมและการออกแบบ", "สถาปัตยกรรม การออกแบบอาคาร และงานภายใน"),
    "arts-creative-design": ("ศิลปะและการออกแบบ", "ทัศนศิลป์ กราฟิกดีไซน์ และงานสร้างสรรค์"),
    "film-animation-games": ("ภาพยนตร์ แอนิเมชัน และเกม", "ภาพยนตร์ แอนิเมชัน สื่อโต้ตอบ และการทำเกม"),
    "music-performing-arts": ("ดนตรีและศิลปะการแสดง", "ดนตรี การแสดง และงานโปรดักชัน"),
    "science-environment": ("วิทยาศาสตร์และสิ่งแวดล้อม", "วิทยาศาสตร์ ความยั่งยืน และสิ่งแวดล้อม"),
    "agriculture-animal-care": ("เกษตรและการดูแลสัตว์", "เกษตร พืชสวน และงานที่เกี่ยวกับสัตว์"),
    "law-social-sciences": ("กฎหมายและสังคมศาสตร์", "กฎหมาย สังคม และสังคมศาสตร์"),
    "research-postgraduate-study": ("วิจัยและบัณฑิตศึกษา", "การเรียนระดับสูงและเส้นทางงานวิจัย"),
    "schools-other-study-options": ("โรงเรียนและตัวเลือกอื่น", "ถามเรื่องการเรียนระดับโรงเรียน คอร์สเฉพาะทาง หรือสาขาที่ไม่มีในรายการ"),
}

VISA_NOTE_TH = """<p class="note-box"><strong>มีคำถามเรื่องวีซ่า?</strong> เราเป็นเอเจนซีการศึกษา ไม่ใช่ migration agent
คำแนะนำเรื่องวีซ่าของคุณ เราจะแนะนำ registered migration agent ให้ ไม่มีใครรับประกันผลวีซ่าได้</p>"""


def en(s):
    return f'<span lang="en">{e(s)}</span>'


def group_anchor(g):  # same ids as the English /courses page, so /courses#<group> links keep working
    return g.lower().replace(" & ", "-").replace(" ", "-")


def courses_body():
    areas = json.loads((ROOT / "content/study-areas.json").read_text())
    missing = [a["slug"] for a in areas if a["slug"] not in AREA_TH]
    if missing:
        raise SystemExit(f"thai_more.AREA_TH is missing study areas: {missing}")
    groups = {}
    for a in areas:
        groups.setdefault(a["group"], []).append(a)
    area_html = "".join(
        f'<h2 id="{e(group_anchor(g))}">{e(GROUP_TH[g])}</h2><ul class="areas">'
        + "".join(f'<li><strong>{e(AREA_TH[a["slug"]][0])}</strong><span>{e(AREA_TH[a["slug"]][1])}</span></li>' for a in items)
        + "</ul>" for g, items in groups.items())
    school_link = ('<p>ดูคอร์สและค่าเรียนจาก<a href="/th/schools">สถาบันที่ส่งข้อมูลให้เรา</a></p>' if schools.SCHOOLS else "")
    return f"""<section class="wrap">
<h1>หาสาขาที่ใช่สำหรับคุณ</h1>
<p class="lead">ดู {len(areas)} สาขา ตั้งแต่ภาษาอังกฤษ งานดูแล ธุรกิจ ไปจนถึงงานช่าง บอกเราว่าคุณสนใจอะไร แล้วเราจะดูตัวเลือกที่เปิดรับตอนนี้ไปด้วยกัน</p>
<p class="note-box"><strong>เกี่ยวกับรายการนี้</strong> นี่คือสาขาการเรียน ไม่ได้แปลว่าทุกคอร์สสมัครผ่านเราได้
เราจะส่งชื่อคอร์ส รหัส CRICOS ค่าเรียน วิทยาเขต และวันเริ่มเรียน หลังจากเช็กกับสถาบันแล้วเท่านั้น</p>
<p class="actions"><a class="btn" href="/th/charter-application">บอกเราว่าอยากเรียนอะไร</a> <a class="btn ghost" href="/th/courses/nursing-pathways-australia">เส้นทางสายพยาบาล</a></p>
{school_link}
<h2>ระดับการเรียน</h2>
<ul class="list">
<li><strong>ภาษาอังกฤษและเส้นทางต่อยอด</strong> เรียนภาษา หรือคอร์ส foundation ก่อนเรียนวุฒิถัดไป</li>
<li><strong>สายอาชีพ</strong> คอร์ส Certificate, Diploma และ Advanced Diploma ที่เน้นลงมือจริง เกณฑ์รับเข้าและการฝึกงานขึ้นกับแต่ละคอร์ส</li>
<li><strong>มหาวิทยาลัย</strong> ปริญญาตรี โท และงานวิจัย แต่ละมหาวิทยาลัยกำหนดเกณฑ์รับเข้าและภาษาอังกฤษเอง</li>
</ul>
{area_html}
{VISA_NOTE_TH}
<aside class="cta"><p>ยังไม่แน่ใจว่าสาขาไหนเหมาะ บอกเราเรื่องความสนใจ สิ่งที่เรียนมา เมืองที่อยากอยู่ และงบประมาณ</p><a class="btn" href="/th/contact-us">ส่งข้อความ</a></aside>
</section>"""


def blog_body(posts, fmt_date):
    cards = "".join(f"""<li class="card"><a href="/post/{p['slug']}" lang="en">
{f'<img src="{e(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else '<div class="noimg"></div>'}
<span class="date">{fmt_date(p["date"])}</span><strong>{e(p["title"])}</strong></a></li>""" for p in posts)
    return f"""<section class="wrap"><h1>บทความ</h1>
<p class="lead">คู่มือเรื่องคอร์สเรียน Working Holiday และชีวิตในออสเตรเลีย ตอนนี้บทความเป็นภาษาอังกฤษ มีคำถามเป็นภาษาไทย ส่งมาถามทีมงานได้เลย</p>
<ul class="cards">{cards}</ul>
{VISA_NOTE_TH}
<aside class="cta"><p>อ่านแล้วมีคำถาม ทีมงานตอบเป็นภาษาไทยหรืออังกฤษ</p><a class="btn" href="/th/contact-us">ส่งข้อความ</a></aside>
</section>"""


SCHOOL_NOTE_TH = ("<p class=\"note-box\"><strong>เกี่ยวกับข้อมูลนี้</strong> มาจากไฟล์ของสถาบันเอง ค่าเรียนและวันเริ่มเรียนเปลี่ยนได้ "
                  "สถาบันจะยืนยันค่าเรียนและวันเริ่มเรียนจริงใน offer letter ของคุณ "
                  "คำถามเรื่องวีซ่า เราจะแนะนำ registered migration agent ให้ เพราะเราไม่ใช่ migration agent</p>")

SUMMARY_TH = {  # Thai summary per school (same meaning as the English summary from the school's files)
    "alana-kaye-college": "คอร์สงานดูแล การศึกษาปฐมวัย บริการชุมชน ธุรกิจ และก่อสร้าง มี 2 วิทยาเขต",
    "frontier-education": "วิทยาลัยสายอาชีพ มีวิทยาเขตที่บริสเบนและแคนส์",
}
INTAKES_TH = {
    "alana-kaye-college": "วันจันทร์ที่ 3 ของทุกเดือน",
    "frontier-education": "เปิดรับรอบพฤศจิกายน 2026 (สถาบันแจ้งเมื่อ 17 พ.ย. 2026)",
}
FEE_NOTE_TH = {
    "alana-kaye-college": "ค่าเรียนรวมทั้งคอร์สเป็นเงินดอลลาร์ออสเตรเลีย รวมค่าสมัคร A$300 และค่าอุปกรณ์การเรียน A$200 แล้ว "
                          "ผ่อนจ่ายได้ (งวดแรก A$1,500 แล้วจ่ายเป็นรายเทอม)",
    "frontier-education": "ค่าเรียนปี 2027 จะประกาศเร็วๆ นี้ ถามเราเรื่องรายการคอร์สและค่าเรียนปี 2026 ได้",
}


def school_th(s, table, key):
    v = table.get(s["slug"])
    if v is None:
        raise SystemExit(f"thai_more: add the Thai {key} for school {s['slug']}")
    return v


def facts(s):
    rows = [("วิทยาเขต", " · ".join(en(c) for c in s["campuses"])),
            ("รอบเปิดเรียน", e(school_th(s, INTAKES_TH, "intakes")) if s.get("intakes") else ""),
            ("CRICOS provider", e(s["cricos"])), ("RTO", e(s.get("rto") or "")),
            ("จำนวนคอร์ส", str(len(s["courses"])) if s["courses"] else "")]
    return "<dl>" + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows if v) + "</dl>"


def card(s):
    return (f'<li class="agent school"><h3 lang="en">{e(s["name"])}</h3><p>{e(school_th(s, SUMMARY_TH, "summary"))}</p>{facts(s)}'
            f'<a class="btn" href="/th/schools/{e(s["slug"])}">{"คอร์สและค่าเรียน" if s["courses"] else "ข้อมูลสถาบัน"}</a></li>')


def fee_table(s):
    if not s["courses"]:
        return ""
    cols = s["fee_columns"]
    head = "".join(f'<th scope="col" lang="en">{e(c)}</th>' for c in cols)
    body = "".join(
        f'<tr><th scope="row" lang="en">{e(c["name"])}<span>{e(c["code"])} · CRICOS {e(c["cricos"])}</span></th>'
        f'<td data-col="ระยะเวลา">{c["weeks"]} สัปดาห์</td>'
        + "".join(f'<td data-col="{e(col)}">{schools.money(c["fees"][col])}</td>' for col in cols) + "</tr>"
        for c in s["courses"])
    return (f'<div class="fees"><table><caption>ค่าเรียนปี {e(s["source"]["year"])} (AUD)</caption>'
            f'<thead><tr><th scope="col">คอร์ส</th><th scope="col">ระยะเวลา</th>{head}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def detail(s):
    src = s["source"]
    return f"""<section class="wrap narrow"><p class="small"><a href="/th/schools">สถาบันทั้งหมด</a></p>
<h1 lang="en">{e(s["name"])}</h1><p class="lead">{e(school_th(s, SUMMARY_TH, "summary"))}</p>
<div class="agent">{facts(s)}</div>
<h2>คอร์สและค่าเรียน</h2>{fee_table(s)}<p>{e(school_th(s, FEE_NOTE_TH, "fee note"))}</p>
<p class="small">ที่มา: <span lang="en">{e(src["file"])}</span> สถาบันส่งให้เรา ({e(src["received"])})
เว็บไซต์สถาบัน: <a href="{e(s["website"])}" target="_blank" rel="noopener">{e(s["website"].split("//")[1])}</a></p>
{SCHOOL_NOTE_TH}<aside class="cta"><p>อยากเรียนที่ <span lang="en">{e(s["name"])}</span>? บอกเราว่าอยากเรียนคอร์สไหน วิทยาเขตไหน และอยากเริ่มเมื่อไหร่</p>
<a class="btn" href="/th/charter-application">สมัครเรียน</a> <a class="btn ghost" href="/th/contact-us">ถามคำถาม</a></aside></section>"""


def schools_index():
    return f"""<section class="wrap narrow"><h1>สถาบันการศึกษา</h1>
<p class="lead">สถาบันที่ทำงานกับนักเรียนอย่างคุณ แต่ละหน้าแสดงคอร์ส วิทยาเขต และค่าเรียนที่สถาบันส่งให้เรา</p>
<ul class="agents">{"".join(card(s) for s in schools.SCHOOLS)}</ul>
<p>หาอย่างอื่นอยู่ใช่ไหม ดู<a href="/th/courses">สาขาการเรียนทั้งหมด</a></p>{SCHOOL_NOTE_TH}</section>"""


# English path → Thai path, and Thai pages (rel → title, description, body). Blog is built in build.py (needs posts).
PAIRS = {"/courses": "/th/courses", "/blog": "/th/blog"}
PAGES = {"th/courses": ("คอร์สเรียนในออสเตรเลีย | We International",
                        "ดูสาขาการเรียนในออสเตรเลีย ตั้งแต่ภาษาอังกฤษ งานดูแล ธุรกิจ ไปจนถึงงานช่าง แล้วถามทีมงานเรื่องตัวเลือก ค่าเรียน และวันเริ่มเรียน",
                        courses_body())}
if schools.SCHOOLS:  # same rule as English: empty in production until the owner approves a school
    PAIRS["/schools"] = "/th/schools"
    PAGES["th/schools"] = ("สถาบันและค่าเรียน | We International",
                           "คอร์ส วิทยาเขต และค่าเรียนจากสถาบันในออสเตรเลีย ข้อมูลจากสถาบันเอง ให้ We International ช่วยสมัครได้",
                           schools_index())
    for s in schools.SCHOOLS:
        PAIRS[f"/schools/{s['slug']}"] = f"/th/schools/{s['slug']}"
        PAGES[f"th/schools/{s['slug']}"] = (
            f"{s['name']} คอร์สและค่าเรียน | We International",
            f"{s['name']}: วิทยาเขต รอบเปิดเรียน และค่าเรียนจากไฟล์ของสถาบันเอง ให้ We International ช่วยสมัครได้",
            detail(s))

# /th/privacy-policy — owner said go ahead (21 Nov 2026). Same content as the owner-approved English notice
# (content_pages.privacy_body, 20 Nov 2026); if the two differ, the English version applies.
PRIVACY_TH = """<section class="wrap narrow">
<h1>นโยบายความเป็นส่วนตัว</h1>
<p class="lead">วิธีที่ We International Education &amp; Visa Pty Ltd ดูแลข้อมูลที่คุณให้เรา มีคำถามส่งมาที่ <a href="mailto:info@weintervisa.com?subject=Privacy">info@weintervisa.com</a></p>
<h2>ข้อมูลที่เราเก็บ</h2>
<p>เฉพาะข้อมูลที่คุณเลือกส่งมาเอง เช่น ชื่อ อีเมล หรือเบอร์โทร / LINE ID ตอนนี้อยู่ที่ไหน อยากเรียนอะไร และข้อความของคุณ
กรุณาอย่าส่งเลขพาสปอร์ต เอกสารยืนยันตัวตน หรือเอกสารการเงินมาในข้อความทั่วไป ถ้าเราต้องใช้ เราจะส่งช่องทางที่ปลอดภัยให้</p>
<h2>เราใช้ข้อมูลทำอะไร</h2>
<p>เพื่อตอบคุณ และช่วยเรื่องบริการด้านการเรียนที่คุณขอ ถ้าคุณติ๊กช่องรับข่าว เราอาจส่งข่าวคอร์สทางอีเมลด้วย ยกเลิกได้ทุกเมื่อ</p>
<h2>เก็บข้อมูลไว้ที่ไหน</h2>
<p>ข้อความจากฟอร์มและแชทบนเว็บไซต์ของเรา เข้าสู่ระบบลูกค้าของเราเองชื่อ GetWec ซึ่งเก็บข้อมูลบนเซิร์ฟเวอร์ในซิดนีย์ ออสเตรเลีย
เฉพาะทีมงานของเราเข้าถึงได้ ตามหน้าที่ของแต่ละคน อีเมลของเราใช้บริการ Google Workspace</p>
<h2>ผู้ช่วย AI</h2>
<p>ผู้ช่วยแชทบนเว็บไซต์ของเราเป็น AI ตอบคำถามทั่วไปจากข้อมูลที่ทีมงานอนุมัติแล้ว และส่งข้อมูลของคุณให้ทีมงานเมื่อคุณขอ ผู้ช่วย AI ไม่ให้คำแนะนำเรื่องวีซ่า</p>
<h2>การส่งต่อข้อมูล</h2>
<p>เราส่งข้อมูลของคุณให้สถาบันการศึกษา หรือให้เอเจนต์ด้านวีซ่าที่ขึ้นทะเบียน (registered migration agent) เพื่อแนะนำต่อ เฉพาะเมื่อจำเป็นต่อบริการที่คุณขอ และคุณยินยอมแล้วเท่านั้น
เราเป็นเอเจนซีการศึกษา ไม่ใช่ migration agent</p>
<h2>ไม่มีการติดตาม</h2>
<p>เว็บไซต์นี้ไม่ใช้คุกกี้ เครื่องมือวิเคราะห์ หรือตัวติดตามโฆษณา</p>
<h2>ดูหรือแก้ไขข้อมูลของคุณ</h2>
<p>ส่งอีเมลมาที่ <a href="mailto:info@weintervisa.com?subject=Privacy">info@weintervisa.com</a> เพื่อขอดูข้อมูลของคุณ ขอแก้ไขหรือลบ หรือแจ้งข้อกังวลเรื่องความเป็นส่วนตัว
ถ้าไม่พอใจคำตอบของเรา ติดต่อสำนักงานคณะกรรมการข้อมูลแห่งออสเตรเลีย (<span lang="en">Office of the Australian Information Commissioner</span>, OAIC) ได้</p>
<p class="note-box">นี่คือฉบับภาษาไทยของ <a href="/privacy-policy">Privacy notice</a> ถ้าฉบับภาษาไทยกับภาษาอังกฤษมีข้อความต่างกัน ให้ถือตามฉบับภาษาอังกฤษ</p>
<p class="hint">ปรับปรุงล่าสุด: 20 พฤศจิกายน 2026</p>
</section>"""
PAIRS["/privacy-policy"] = "/th/privacy-policy"
PAGES["th/privacy-policy"] = ("นโยบายความเป็นส่วนตัว | We International",
                              "We International Education & Visa Pty Ltd เก็บ ใช้ และดูแลข้อมูลของคุณอย่างไร",
                              PRIVACY_TH)

BLOG_TITLE = "บทความเรื่องเรียนต่อและชีวิตในออสเตรเลีย | We International"
BLOG_DESC = "คู่มือเรื่องคอร์สเรียน Working Holiday และชีวิตนักเรียนในออสเตรเลีย (บทความภาษาอังกฤษ) ทีมงานตอบคำถามเป็นภาษาไทยหรืออังกฤษ"
