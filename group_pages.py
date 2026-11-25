"""Owner decisions of 25 Nov 2026 (WEI-WEB-REDESIGN-1123, map https://claude.ai/artifact/8dC25eV32Hnxr2twANP1xE):

- Home page style A, "four doors": one sentence, four doors, three steps, one button (EN + TH).
- Top menu of 6: Study, Working Holiday, Nursing and care, Student help, Learn English, Contact us.
- Footer: Learn English free, Take a break, Families, partners, and one line for the game studio
  (weintergames.com) — "students get bored; games help".
- New pages /families (students who came with children → KindozaStudio printables, games) and
  /take-a-break (our studio's games + a quick English game).
- One-way rule: this site links out to the games and the kids' shop; nothing here sends student data anywhere.

Rules as everywhere: no promised prices, places, visas or jobs; visa questions go to a registered migration agent;
only links we already know are real (no guessed URLs: Kindoza Kids videos and Solune walk clips are added
when their links are confirmed).
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
e = html.escape
HOME = json.loads((ROOT / "content/home.json").read_text())
HOME_TH = json.loads((ROOT / "content/th/home.json").read_text())
FT = {c["id"]: c for c in json.loads((ROOT / "content/fast-track.json").read_text())["courses"]}
KIDS = json.loads((ROOT / "content/english-practice.json").read_text())["kids"]
STUDIO = "https://weintergames.com/"

NAV = {
    "en": [("Study", "/courses"), ("Working Holiday", "/fast-track-courses"),
           ("Nursing and care", "/courses/nursing-pathways-australia"), ("Student help", "/student-services"),
           ("Learn English", "/english-practice"), ("Contact us", "/contact-us")],
    "th": [("เรียนต่อ", "/th/courses"), ("Working Holiday", "/th/fast-track-courses"),
           ("พยาบาลและงานดูแล", "/th/courses/nursing-pathways-australia"), ("ช่วยนักเรียน", "/th/student-services"),
           ("เรียนอังกฤษ", "/th/english-practice"), ("ติดต่อเรา", "/th/contact-us")],
}


def nav_current(path, items):
    """The one menu item for this page: the longest menu path the page sits under."""
    hits = [p for _, p in items if path == p or path.startswith(p + "/")]
    return max(hits, key=len) if hits else None


def footer_links(lang):
    t = lang == "th"
    p = "/th" if t else ""
    groups = [
        ("เรียนอังกฤษ" if t else "Learn English free", f"{p}/english-practice"),
        ("พักสมองสักนิด" if t else "Take a break", f"{p}/take-a-break"),
        ("มากับครอบครัว" if t else "Families", f"{p}/families"),
        ("บทความ" if t else "Blog", f"{p}/blog"),
        ("คำถามที่พบบ่อย" if t else "FAQ", f"{p}/frequently-asked-questions"),
        ("เกี่ยวกับเรา" if t else "About us", f"{p}/about-we-international"),
        ("สำหรับพาร์ตเนอร์" if t else "For partners", f"{p}/referral-partners"),
    ]
    links = " · ".join(f'<a href="{h}">{l}</a>' for l, h in groups)
    studio = (f'ในเครือ We International: <a href="{STUDIO}" target="_blank" rel="noopener">WE International Game Studio</a> เกมพักสมองสำหรับนักเรียน'
              if t else
              f'Part of the We International group: <a href="{STUDIO}" target="_blank" rel="noopener">WE International Game Studio</a>, free games for a study break')
    return f'<p class="foot-links">{links}</p><p>{studio}</p>'


# ---------- Home, style A: four doors ----------
def _img(spec_file, alt=""):
    if not spec_file or not (ROOT / "assets/img" / spec_file).exists():
        return '<span class="door-ico" aria-hidden="true">🤝</span>'
    return f'<img src="/assets/img/{e(spec_file)}" alt="{e(alt)}" loading="lazy" width="140" height="120">'


DOORS = {
    "en": [("/fast-track-courses", FT["chc33021"]["img"]["file"], "I'm on a Working Holiday visa",
            "Practical Certificate III courses with work placement."),
           ("/courses", FT["chc30125"]["img"]["file"], "I want to study in Australia",
            "Find a course that fits your visa, budget and goals."),
           ("/courses/nursing-pathways-australia", FT["hlt33115"]["img"]["file"], "I'm a nurse, or want to be one",
            "See how registration works and the prep courses."),
           ("/referral-partners", "", "I'm a school or a partner agency", "Work with us and refer students.")],
    "th": [("/th/fast-track-courses", FT["chc33021"]["img"]["file"], "ถือวีซ่า Working Holiday อยู่",
            "คอร์ส Certificate III สายอาชีพ พร้อมฝึกงาน"),
           ("/th/courses", FT["chc30125"]["img"]["file"], "อยากเรียนต่อออสเตรเลีย",
            "หาคอร์สที่เข้ากับวีซ่า งบ และเป้าหมายของคุณ"),
           ("/th/courses/nursing-pathways-australia", FT["hlt33115"]["img"]["file"], "เป็นพยาบาล หรืออยากเป็น",
            "ดูขั้นตอนขึ้นทะเบียนและคอร์สเตรียมตัว"),
           ("/th/referral-partners", "", "เป็นสถาบันหรือเอเจนซีพาร์ตเนอร์", "ร่วมงานและส่งนักเรียนกับเรา")],
}

HOME_UI = {
    "en": {"kicker": "Education agency in Sydney", "lead": "Tell us your visa. We'll show you courses that fit.",
           "more": "See more →", "howH": "How it works", "howP": "Three steps. No cost for course advice.",
           "hereH": "Already here, or nearly?", "hereP": "Health cover, a place to live and the things that make life easier.",
           "pick": [("🩺", "Compare health cover (OSHC)", "/oshc"), ("🏡", "Find a homestay with our partner", "/homestay"),
                    ("👨‍👩‍👧", "Came with your family? Help for kids", "/families"),
                    ("🎮", "Take a break: free games", "/take-a-break"),
                    ("🗣️", "Learn English free", "/english-practice"), ("📚", "Read our plain-English guides", "/blog")],
           "visa": ("<strong>Visa questions?</strong> We are an education agency, not a migration agent. "
                    'For visa advice we refer you to a <a href="/migration-support">registered migration agent</a>.'),
           "ctaH": "Not sure where to start?",
           "ctaP": "Tell us your visa and what you'd like to study. We reply with options and a written quote.",
           "ctaB": "Talk to us", "contact": "/contact-us", "replies": "Our team replies in Thai or English."},
    "th": {"kicker": "เอเจนซีการศึกษาใน Sydney", "lead": "บอกเราว่าถือวีซ่าอะไร เราจะหาคอร์สที่เหมาะให้",
           "more": "ดูต่อ →", "howH": "ขั้นตอน", "howP": "3 ขั้นตอน ปรึกษาเรื่องคอร์สไม่มีค่าใช้จ่าย",
           "hereH": "อยู่ออสเตรเลียแล้ว หรือใกล้จะมา?", "hereP": "ประกันสุขภาพ ที่พัก และเรื่องที่ช่วยให้ชีวิตง่ายขึ้น",
           "pick": [("🩺", "เทียบประกันสุขภาพนักเรียน (OSHC)", "/th/oshc"), ("🏡", "หาโฮมสเตย์กับพาร์ตเนอร์ของเรา", "/th/homestay"),
                    ("👨‍👩‍👧", "มากับครอบครัว? กิจกรรมสำหรับลูก", "/th/families"),
                    ("🎮", "พักสมอง: เกมพัซเซิล", "/th/take-a-break"),
                    ("🗣️", "ฝึกภาษาอังกฤษไม่มีค่าใช้จ่าย", "/th/english-practice"), ("📚", "อ่านบทความแนะนำ", "/th/blog")],
           "visa": ("<strong>มีคำถามเรื่องวีซ่า?</strong> เราเป็นเอเจนซีการศึกษา ไม่ใช่ migration agent "
                    'คำแนะนำเรื่องวีซ่า เราจะแนะนำ <a href="/th/migration-support">registered migration agent</a> ให้'),
           "ctaH": "ไม่รู้จะเริ่มตรงไหน?",
           "ctaP": "บอกเราว่าถือวีซ่าอะไรและอยากเรียนอะไร เราตอบกลับพร้อมตัวเลือกและใบเสนอราคาเป็นลายลักษณ์อักษร",
           "ctaB": "คุยกับเรา", "contact": "/th/contact-us", "replies": "ทีมงานตอบเป็นภาษาไทยหรืออังกฤษ"},
}


def home(lang="en"):
    L, h = HOME_UI[lang], (HOME_TH if lang == "th" else HOME)
    doors = "".join(f'<li class="door"><a href="{href}">{_img(f)}<div><h3>{e(t)}</h3><span>{e(b)}</span><b>{e(L["more"])}</b></div></a></li>'
                    for href, f, t, b in DOORS[lang])
    trust = "".join(f"<li>{e(x)}</li>" for x in h["trust"])
    steps = "".join(f"<li><strong>{e(a)}</strong><span>{e(b)}</span></li>" for a, b in h["steps"])
    pick = "".join(f'<li><a href="{href}"><span aria-hidden="true">{i}</span>{e(t)}</a></li>' for i, t, href in L["pick"])
    replies = f'<p class="small">{e(L["replies"])}</p>' if L["replies"] else ""
    return f"""<section class="hero doors-hero"><div class="wrap">
<p class="kicker">{e(L["kicker"])}</p>
<h1>{e(h["heading"])}</h1>
<p class="lead">{e(L["lead"])}</p>
<ul class="doors">{doors}</ul>
<ul class="trust">{trust}</ul>
</div></section>
<section class="wrap band">
<h2>{e(L["howH"])}</h2>
<p>{e(L["howP"])}</p>
<ol class="flow flow3">{steps}</ol>
<p class="actions"><a class="btn" href="{L["contact"]}">{e(L["ctaB"])}</a></p>
</section>
<section class="wrap">
<h2>{e(L["hereH"])}</h2>
<p>{e(L["hereP"])}</p>
<ul class="pick">{pick}</ul>
<p class="note-box">{L["visa"]}</p>
<aside class="cta"><h2>{e(L["ctaH"])}</h2><p>{e(L["ctaP"])}</p><a class="btn" href="{L["contact"]}">{e(L["ctaB"])}</a>{replies}</aside>
</section>"""


# ---------- /take-a-break ----------
GAMES = [  # from weintergames.com (studio's own page); each card links to its section there
    ("swapscape", "Swapscape", "🃏", "A picture cut into cards and shuffled. Swap the cards back.",
     "ภาพถูกตัดเป็นการ์ดแล้วสลับกัน สลับกลับให้ครบภาพ"),
    ("blockscape", "Blockscape", "🧱", "Drop wooden blocks, clear rows, and a hidden painting peeks through.",
     "วางบล็อกไม้ เคลียร์แถว แล้วภาพที่ซ่อนอยู่จะค่อยๆ โผล่"),
    ("haulers", "Tiny Haulers", "📦", "Tap a crate and tiny haulers carry it to the picture.",
     "แตะกล่อง แล้วทีมขนของตัวจิ๋วจะขนไปเติมภาพ"),
    ("brickbloom", "Brickbloom", "🎯", "Aim, let go, and break glazed tiles to show a painting.",
     "เล็งแล้วปล่อยลูก ทุบกระเบื้องเพื่อเผยภาพวาด"),
]

BREAK_UI = {
    "en": {"title": "Take a break | Free games for students | We International",
           "desc": "Study is hard work. Rest your brain for a few minutes with free puzzle games from our group's game studio and a quick English game.",
           "kicker": "Student help", "h1": "Take a break",
           "lead": "Study is hard work. Rest your brain for five minutes, then go back fresh.",
           "gamesH": "Puzzle games from our game studio",
           "gamesP": "Calm puzzle games made by WE International Game Studio, part of the We International group.",
           "see": "See the game ↗", "all": "All our games ↗",
           "engH": "A quick English game", "engP": "Eight everyday mistakes. Pick the natural way to say it, then check the answer.",
           "engB": "Play Say it right", "eng": "/english-practice#quiz",
           "small": "The games open on weintergames.com in a new tab. Nothing you do here is shared with the games.",
           "ctaP": "Need a hand with your course or your next step?", "ctaB": "Talk to us", "contact": "/contact-us"},
    "th": {"title": "พักสมองสักนิด | เกมสำหรับนักเรียน | We International",
           "desc": "เรียนหนักมาทั้งวัน พักสมองสักครู่กับเกมพัซเซิลจากสตูดิโอเกมในเครือของเรา และเกมฝึกภาษาอังกฤษสั้นๆ",
           "kicker": "ช่วยนักเรียน", "h1": "พักสมองสักนิด",
           "lead": "การเรียนเหนื่อยนะ พักสมองสัก 5 นาที แล้วกลับไปเรียนต่อแบบสดชื่น",
           "gamesH": "เกมพัซเซิลจากสตูดิโอเกมของเรา",
           "gamesP": "เกมพัซเซิลสบายๆ จาก WE International Game Studio ในเครือ We International",
           "see": "ดูเกม ↗", "all": "ดูเกมทั้งหมด ↗",
           "engH": "เกมภาษาอังกฤษสั้นๆ", "engP": "ข้อผิดที่เจอบ่อย 8 ข้อ เลือกแบบที่คนพูดจริง แล้วเปิดดูคำตอบ",
           "engB": "เล่น Say it right", "eng": "/th/english-practice#quiz",
           "small": "เกมเปิดที่ weintergames.com ในแท็บใหม่ สิ่งที่คุณทำบนหน้านี้ไม่ถูกส่งไปที่เกม",
           "ctaP": "อยากให้ช่วยเรื่องคอร์สหรือขั้นต่อไป?", "ctaB": "คุยกับเรา", "contact": "/th/contact-us"},
}


def take_a_break(lang="en"):
    L = BREAK_UI[lang]
    th = lang == "th"
    cards = "".join(f"""<li class="path"><span class="ico" aria-hidden="true">{i}</span><h3 lang="en">{e(n)}</h3><p>{e(dth if th else den)}</p>
<a href="{STUDIO}#{gid}" target="_blank" rel="noopener">{e(L["see"])}</a></li>""" for gid, n, i, den, dth in GAMES)
    return f"""<section class="hero"><div class="wrap">
<p class="kicker">{e(L["kicker"])}</p>
<h1>{e(L["h1"])}</h1>
<p class="lead">{e(L["lead"])}</p>
</div></section>
<section class="wrap">
<h2>{e(L["gamesH"])}</h2>
<p>{e(L["gamesP"])}</p>
<ul class="paths">{cards}</ul>
<p class="actions"><a class="btn ghost" href="{STUDIO}" target="_blank" rel="noopener">{e(L["all"])}</a></p>
<p class="small">{e(L["small"])}</p>
</section>
<section class="wrap band">
<h2>{e(L["engH"])}</h2>
<p>{e(L["engP"])}</p>
<p class="actions"><a class="btn" href="{L["eng"]}">{e(L["engB"])}</a></p>
</section>
<section class="wrap"><aside class="cta"><p>{e(L["ctaP"])}</p><a class="btn" href="{L["contact"]}">{e(L["ctaB"])}</a></aside></section>"""


# ---------- /families ----------
KIDS_TH = [  # same order as content/english-practice.json "kids.items"
    ("อายุ 3–7 · อ่านภาษาอังกฤษ", "Learn to Read Bundle", "ตัวอักษร เสียง คำ CVC และ sight words 92 คำแรก รวม 4 เล่ม 140 หน้า"),
    ("อายุ 3–6 · หัดเขียน", "Alphabet Tracing Book", "หน้าละ 1 ตัวอักษร A–Z ทั้งตัวพิมพ์ใหญ่และเล็ก พร้อมสมุดระบายสี ABC 2 เล่ม"),
    ("อายุ 5–8 · คณิต", "Australian Money Worksheets", "เหรียญและธนบัตรออสเตรเลีย การทอนเงินและการซื้อของ เหมาะกับเด็กที่เพิ่งมาออสเตรเลีย"),
    ("อายุ 4–8 · คณิต", "Kindergarten Maths Bundle", "บวกลบ ตัวเลขถึง 100 รูปทรงและการวัด รวม 3 เล่ม 99 หน้า"),
    ("อายุ 4–8 · ระบายสี", "Aussie Animals Colouring", "โคอาล่า จิงโจ้ วอมแบต และเพื่อนๆ ได้เรียนชื่อสัตว์เป็นภาษาอังกฤษ"),
    ("อายุ 4–8 · งานประดิษฐ์", "Origami for Kids", "พับกระดาษง่ายๆ 12 แบบ มีเส้นพับพิมพ์ไว้ ไม่ต้องใช้กาว"),
]

FAM_UI = {
    "en": {"title": "Studying with your family | We International",
           "desc": "Came to Australia with your children? Printable learning activities for kids, free games for a quiet break, and study plans that fit family life.",
           "kicker": "Student help · Families", "h1": "Studying with your family",
           "lead": "Some students come to Australia with a partner or children. Here are a few things that help at home while you study.",
           "kidsH": "Learning activities for kids",
           "kidsP": "Printable activity books for ages 3–8, with Australian animals, Aussie money and Australian spelling. Print at home, as many pages as you need.",
           "etsy": "View on Etsy ↗", "shop": "See all kids' activities ↗",
           "kidsNote": "From KindozaStudio, a sister brand of We International. Opens Etsy in a new tab. Digital downloads, nothing is posted.",
           "gamesH": "Free games for a quiet moment",
           "gamesP": "Calm puzzle games from WE International Game Studio, part of the We International group. Good for older kids, and for you after class.",
           "gamesB": "Take a break page", "games": "/take-a-break",
           "planH": "Study that fits family life",
           "planP": "Tell us your class days, the area you live in and when you can start. We look for courses and campuses that fit around your family.",
           "visa": ("<strong>Visa questions for your family?</strong> Questions about a partner's or child's visa go to a "
                    '<a href="/migration-support">registered migration agent</a>. We are an education agency, not a migration agent.'),
           "ctaP": "Planning study with your family? Tell us what you need.", "ctaB": "Talk to us", "contact": "/contact-us"},
    "th": {"title": "มาเรียนพร้อมครอบครัว | We International",
           "desc": "มาออสเตรเลียพร้อมลูก? กิจกรรมการเรียนรู้แบบพิมพ์ได้สำหรับเด็ก เกมไว้พักสมอง และแผนการเรียนที่เข้ากับชีวิตครอบครัว",
           "kicker": "ช่วยนักเรียน · ครอบครัว", "h1": "มาเรียนพร้อมครอบครัว",
           "lead": "นักเรียนบางคนมาออสเตรเลียพร้อมคู่หรือลูก นี่คือสิ่งที่ช่วยได้ที่บ้านระหว่างที่คุณเรียน",
           "kidsH": "กิจกรรมการเรียนรู้สำหรับเด็ก",
           "kidsP": "สมุดกิจกรรมแบบพิมพ์ได้สำหรับเด็ก 3–8 ขวบ มีสัตว์ออสเตรเลีย เงินออสเตรเลีย และการสะกดแบบออสเตรเลีย พิมพ์ที่บ้านได้ไม่จำกัดหน้า",
           "etsy": "ดูบน Etsy ↗", "shop": "ดูกิจกรรมสำหรับเด็กทั้งหมด ↗",
           "kidsNote": "จาก KindozaStudio แบรนด์ในเครือ We International เปิด Etsy ในแท็บใหม่ เป็นไฟล์ดาวน์โหลด ไม่มีการส่งของ",
           "gamesH": "เกมไว้พักสมอง",
           "gamesP": "เกมพัซเซิลสบายๆ จาก WE International Game Studio ในเครือ We International เหมาะกับเด็กโต และกับคุณหลังเลิกเรียน",
           "gamesB": "ไปหน้าพักสมอง", "games": "/th/take-a-break",
           "planH": "เรียนให้เข้ากับชีวิตครอบครัว",
           "planP": "บอกเราว่าเรียนได้วันไหน อยู่แถวไหน และเริ่มได้เมื่อไหร่ เราจะหาคอร์สและวิทยาเขตที่เข้ากับครอบครัวของคุณ",
           "visa": ("<strong>มีคำถามเรื่องวีซ่าของครอบครัว?</strong> คำถามเรื่องวีซ่าของคู่หรือลูก ขอให้ถาม "
                    '<a href="/th/migration-support">registered migration agent</a> เราเป็นเอเจนซีการศึกษา ไม่ใช่ migration agent'),
           "ctaP": "วางแผนเรียนพร้อมครอบครัว? บอกเราว่าต้องการอะไร", "ctaB": "คุยกับเรา", "contact": "/th/contact-us"},
}


def families(lang="en"):
    L = FAM_UI[lang]
    th = lang == "th"
    items = []
    for n, (age, title, body, url) in enumerate(KIDS["items"]):
        if th:
            age, _, body = KIDS_TH[n]
        items.append(f"""<li class="path"><span class="tag">{e(age)}</span><h3 lang="en">{e(title)}</h3><p>{e(body)}</p>
<a href="{e(url)}" target="_blank" rel="noopener">{e(L["etsy"])}</a></li>""")
    return f"""<section class="hero"><div class="wrap">
<p class="kicker">{e(L["kicker"])}</p>
<h1>{e(L["h1"])}</h1>
<p class="lead">{e(L["lead"])}</p>
</div></section>
<section class="wrap">
<h2>{e(L["kidsH"])}</h2>
<p>{e(L["kidsP"])}</p>
<ul class="paths">{"".join(items)}</ul>
<p class="actions"><a class="btn ghost" href="{e(KIDS["shop"])}" target="_blank" rel="noopener">{e(L["shop"])}</a></p>
<p class="small">{e(L["kidsNote"])}</p>
</section>
<section class="wrap band">
<h2>{e(L["gamesH"])}</h2>
<p>{e(L["gamesP"])}</p>
<p class="actions"><a class="btn" href="{L["games"]}">{e(L["gamesB"])}</a></p>
</section>
<section class="wrap">
<h2>{e(L["planH"])}</h2>
<p>{e(L["planP"])}</p>
<p class="note-box">{L["visa"]}</p>
<aside class="cta"><p>{e(L["ctaP"])}</p><a class="btn" href="{L["contact"]}">{e(L["ctaB"])}</a></aside>
</section>"""


PAGES = {
    "take-a-break": (BREAK_UI["en"]["title"], BREAK_UI["en"]["desc"], take_a_break("en")),
    "families": (FAM_UI["en"]["title"], FAM_UI["en"]["desc"], families("en")),
}
TH_PAGES = {
    "th/take-a-break": (BREAK_UI["th"]["title"], BREAK_UI["th"]["desc"], take_a_break("th")),
    "th/families": (FAM_UI["th"]["title"], FAM_UI["th"]["desc"], families("th")),
}
PAIRS = {"/take-a-break": "/th/take-a-break", "/families": "/th/families"}
