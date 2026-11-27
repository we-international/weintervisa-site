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
import re
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


# Line icons (unslop pass 27 Nov 2026): one set, 24 viewBox, 1.5 stroke, colour = text role. Drawn here, no emoji.
_ICON_PATHS = {
    "badge": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.8 2.8L16 9.5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "chat": '<path d="M4 5h16v11H10l-6 4z"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M12 9v6M9 12h6"/>',
    "home": '<path d="M4 11l8-7 8 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
    "family": '<circle cx="9" cy="7.5" r="3"/><circle cx="17" cy="10" r="2"/><path d="M3.5 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6"/><path d="M15 15.2c.6-.4 1.3-.7 2-.7 2 0 3.5 1.8 3.5 4.5"/>',
    "blocks": '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><circle cx="16.5" cy="16.5" r="3.5"/>',
    "talk": '<path d="M4 5h16v11H10l-6 4z"/><path d="M8 9h8M8 12h5"/>',
    "book": '<path d="M4 5.5c2.7-1.2 5.3-1 8 1 2.7-2 5.3-2.2 8-1V19c-2.7-1.2-5.3-1-8 1-2.7-2-5.3-2.2-8-1z"/><path d="M12 6.5V20"/>',
    "link": '<circle cx="9" cy="12" r="5"/><circle cx="15" cy="12" r="5"/>',
    # fast-track page (27 Nov 2026, replaces its emoji)
    "cap": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5v4c1.6 1.6 3.4 2.3 5.5 2.3s3.9-.7 5.5-2.3v-4"/><path d="M21.5 9.5V15"/>',
    "work": '<rect x="3.5" y="7.5" width="17" height="12" rx="2"/><path d="M9 7.5V6a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 6v1.5"/><path d="M3.5 12.5h17"/>',
    "care": '<circle cx="12" cy="6" r="2.5"/><path d="M12 9.5c-2.5 0-4.5 2-4.5 4.5V16"/><path d="M12 9.5c2.5 0 4.5 2 4.5 4.5V16"/><path d="M5 20c2.5-2.6 4.8-3.5 7-3.5s4.5.9 7 3.5"/>',
    "hospital": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M12 8v8M8 12h8"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.6 9.4a2.5 2.5 0 0 1 4.8.9c0 1.7-2.4 2.1-2.4 3.7"/><path d="M12 17h.01"/>',
    # homestay page (27 Nov 2026)
    "bed": '<path d="M3 18V7"/><path d="M3 14h18v4"/><path d="M21 14v-2.5a2.5 2.5 0 0 0-2.5-2.5H11v5"/><circle cx="7" cy="11" r="1.8"/>',
    "phone": '<path d="M6.5 3.5h3l1.5 4-2 1.5a11 11 0 0 0 6 6l1.5-2 4 1.5v3a2 2 0 0 1-2 2A16.5 16.5 0 0 1 4.5 5.5a2 2 0 0 1 2-2z"/>',
    "bus": '<rect x="5" y="3.5" width="14" height="14" rx="2.5"/><path d="M5 11h14M8 20.5v-3M16 20.5v-3"/><circle cx="8.5" cy="14.2" r=".6"/><circle cx="15.5" cy="14.2" r=".6"/>',
    "meal": '<circle cx="12" cy="13" r="6"/><path d="M3.5 4v5a1.5 1.5 0 0 0 1.5 1.5V20M5 4v4.5M20.5 4c-1.5 1-2 2.8-2 5h2V20"/>',
    "receipt": '<path d="M6 3.5h12v17l-2-1.3-2 1.3-2-1.3-2 1.3-2-1.3-2 1.3z"/><path d="M9 8.5h6M9 12h6M9 15.5h3"/>',
    "map": '<path d="M3.5 6.5l5.5-2 6 2 5.5-2v13l-5.5 2-6-2-5.5 2z"/><path d="M9 4.5v13M15 6.5v13"/>',
    "checklist": '<path d="M4 6.5l1.5 1.5L8 5.5M4 12.5l1.5 1.5L8 11.5M4 18.5l1.5 1.5L8 17.5"/><path d="M11 7h9M11 13h9M11 19h9"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_ICON_PATHS[name]}</svg>')


TRUST_ICONS = ["badge", "pin", "chat"]
_LEAD_EMOJI = re.compile(r"^[^\w(]+", re.U)


# ---------- Home, style A: four doors ----------
def _img(spec_file, alt=""):
    if not spec_file or not (ROOT / "assets/img" / spec_file).exists():
        return f'<span class="door-ico">{icon("link", "ico ico-door")}</span>'
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
           "pick": [("shield", "Compare health cover (OSHC)", "/oshc"), ("home", "Find a homestay with our partner", "/homestay"),
                    ("family", "Came with your family? Help for kids", "/families"),
                    ("blocks", "Take a break: free games", "/take-a-break"),
                    ("talk", "Learn English free", "/english-practice"), ("book", "Read our plain-English guides", "/blog")],
           "visa": ("<strong>Visa questions?</strong> We are an education agency, not a migration agent. "
                    'For visa advice we refer you to a <a href="/migration-support">registered migration agent</a>.'),
           "ctaH": "Not sure where to start?",
           "ctaP": "Tell us your visa and what you'd like to study. We reply with options and a written quote.",
           "ctaB": "Talk to us", "contact": "/contact-us", "replies": "Our team replies in Thai or English."},
    "th": {"kicker": "เอเจนซีการศึกษาใน Sydney", "lead": "บอกเราว่าถือวีซ่าอะไร เราจะหาคอร์สที่เหมาะให้",
           "more": "ดูต่อ →", "howH": "ขั้นตอน", "howP": "3 ขั้นตอน ปรึกษาเรื่องคอร์สไม่มีค่าใช้จ่าย",
           "hereH": "อยู่ออสเตรเลียแล้ว หรือใกล้จะมา?", "hereP": "ประกันสุขภาพ ที่พัก และเรื่องที่ช่วยให้ชีวิตง่ายขึ้น",
           "pick": [("shield", "เทียบประกันสุขภาพนักเรียน (OSHC)", "/th/oshc"), ("home", "หาโฮมสเตย์กับพาร์ตเนอร์ของเรา", "/th/homestay"),
                    ("family", "มากับครอบครัว? กิจกรรมสำหรับลูก", "/th/families"),
                    ("blocks", "พักสมอง: เกมพัซเซิล", "/th/take-a-break"),
                    ("talk", "ฝึกภาษาอังกฤษไม่มีค่าใช้จ่าย", "/th/english-practice"), ("book", "อ่านบทความแนะนำ", "/th/blog")],
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
    trust = "".join(f"<li>{icon(TRUST_ICONS[n % 3])}{e(_LEAD_EMOJI.sub('', x))}</li>" for n, x in enumerate(h["trust"]))
    steps = "".join(f"<li><strong>{e(a)}</strong><span>{e(b)}</span></li>" for a, b in h["steps"])
    pick = "".join(f'<li><a href="{href}">{icon(i)}{e(t)}</a></li>' for i, t, href in L["pick"])
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
