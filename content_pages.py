"""Content pages of the new weintervisa.com, at the same paths as Wix.

Source: the company's prepared page drafts in the Wix CMS collection "WEIWebsitePages" and the study
areas in "WEICourseCategories" (read-only export, 19 Nov 2026), rewritten in short, plain English.
Rules: no promised prices, reply times, places, visas or jobs; visa questions go to a registered
migration agent; no partner is named until the agreement is verified.
"""
import html
import json
import re
from pathlib import Path

import schools

ROOT = Path(__file__).resolve().parent
e = html.escape

VISA_NOTE = """<p class="note-box"><strong>Visa questions?</strong> We are an education agency, not a migration agent.
For advice about your visa, we refer you to a registered migration agent. No visa outcome is guaranteed.</p>"""


def cta(text="Ask our team", href="/contact-us", second=None):
    extra = f' <a class="btn ghost" href="{second[1]}">{second[0]}</a>' if second else ""
    return f'<div class="cta"><p>{text}</p><a class="btn" href="{href}">Send a message</a>{extra}</div>'


def sections(items):
    return "".join(f"<h2>{e(h)}</h2><p>{b}</p>" for h, b in items)


def simple(h1, lead, items, *, note=False, cta_text="Have a question? Our team reads every message.", second=None):
    return (f'<section class="wrap narrow"><h1>{e(h1)}</h1><p class="lead">{lead}</p>'
            f'{sections(items)}{VISA_NOTE if note else ""}{cta(cta_text, second=second)}</section>')


# /courses — study areas from the CMS, grouped
areas = json.loads((ROOT / "content/study-areas.json").read_text())
groups = {}
for a in areas:
    groups.setdefault(a["group"], []).append(a)
area_html = "".join(
    f'<details class="area-fold"><summary><h2 id="{e(g.lower().replace(" & ", "-").replace(" ", "-"))}">{e(g)} '
    f'<span class="small">({len(items)})</span></h2></summary><ul class="areas">'
    + "".join(f'<li><strong>{e(a["title"])}</strong><span>{e(a.get("description") or "")}</span></li>' for a in items)
    + "</ul></details>" for g, items in groups.items())
import courses_page  # noqa: E402 — /courses rebuilt from the live Wix catalogue (22 Nov 2026)
courses_body = courses_page.render(
    f"""<section class="wrap">
<p class="kicker">All study areas</p>
<h2>Browse {len(areas)} study areas</h2>
<p>From English to care, business, trades and more. These are study areas, not a promise that every course is open through us.
We share a course name, CRICOS code, fees, campus and start date only after we check them with the school.</p>
<h2>Study levels</h2>
<ul class="list">
<li><strong>English and pathways</strong> — language study or a foundation course before your next qualification.</li>
<li><strong>Vocational study</strong> — practical Certificate, Diploma and Advanced Diploma courses. Entry and placement rules depend on the course.</li>
<li><strong>University</strong> — bachelor, master and research study. Each university sets its own entry and English rules.</li>
</ul>
{area_html}
{cta("Not sure which area fits? Tell us your interests, past study, city and budget.", "/contact-us")}
</section>""",
    '<p>See courses and fees from <a href="/schools">schools that sent us their details</a>.</p>' if schools.SCHOOLS else "")

import nursing_page  # noqa: E402 — rebuilt from the live Wix page (22 Nov 2026)
nursing_body = nursing_page.render()

import fasttrack_page  # noqa: E402 — rebuilt from the live Wix page (21 Nov 2026)
fast_track_body = fasttrack_page.render()

import englishpractice_page  # noqa: E402 — rebuilt from the live Wix page (21 Nov 2026)
english_body = englishpractice_page.render()

services_body = f"""<section class="hero home-hero"><div class="wrap">
<p class="kicker">Student services</p>
<h1>Support for the steps around your study</h1>
<p class="lead">Get help understanding education options, organising your education application and getting ready for your next step.</p>
<p class="actions"><a class="btn" href="/contact-us">Start a conversation</a> <a class="btn ghost" href="/schedule">Book a time to talk</a></p>
</div></section>
<section class="wrap">
<p class="kicker">Support around your study</p>
<h2>More clarity. Less guesswork.</h2>
<ul class="paths">
<li class="path"><h3>Course consultation</h3><p>Clarify your learning goals and compare confirmed education options.</p><a href="/courses">Browse study areas →</a></li>
<li class="path"><h3>Admissions coordination</h3><p>We help you track the education documents you need, your application status and replies from the school.</p><a href="/charter-application">Tell us what you want to study →</a></li>
<li class="path"><h3>Student support</h3><p>Ask us for help with orientation information, school contacts and support referrals.</p><a href="/contact-us">Ask our team →</a></li>
<li class="path"><h3>Language support</h3><p>Mia, our AI assistant, chats in many languages. Our team speaks Thai and English, so a reply from a person is in Thai or English. Important course terms stay in English so nothing is lost.</p><a href="/english-practice">Free English practice →</a></li>
</ul>
</section>
<section class="wrap">
<p class="kicker">Before and after you arrive</p>
<h2>Help with the practical things</h2>
<ul class="paths">
<li class="path"><h3>Homestay</h3><p>Start with a screened host family near your school, with our partner AHN.</p><a href="/homestay">Find a homestay →</a></li>
<li class="path"><h3>Student health cover</h3><p>Compare OSHC providers and buy directly on our partner's website.</p><a href="/oshc">Compare OSHC →</a></li>
<li class="path"><h3>Working Holiday courses</h3><p>Practical Certificate III courses for 417 and 462 visa holders.</p><a href="/fast-track-courses">See the courses →</a></li>
<li class="path"><h3>Nursing pathways</h3><p>Understand registration steps, then English, NCLEX-RN and OSCE preparation.</p><a href="/courses/nursing-pathways-australia">Nursing pathways →</a></li>
<li class="path"><h3>Came with your family?</h3><p>Printable learning activities for kids and study plans that fit family life.</p><a href="/families">Help for families →</a></li>
<li class="path"><h3>Take a break</h3><p>Studying is tiring. Free puzzle games from WE International Game Studio, part of our group, for a five-minute rest.</p><a href="/take-a-break">Play a free game →</a></li>
</ul>
</section>
<section class="wrap narrow">
<h2>How it works</h2>
<ol class="flow flow3"><li><strong>Tell us your plans</strong><span>What you want to study, where you are now and your budget.</span></li>
<li><strong>Compare options</strong><span>We check current courses and details with schools.</span></li>
<li><strong>Apply and get ready</strong><span>We help with the school application and your next steps.</span></li></ol>
{VISA_NOTE}{cta("Your next step starts with a conversation. Tell us what you want to study.")}
</section>"""

import homestay_page  # noqa: E402 — rebuilt from the live Wix page (21 Nov 2026)
homestay_body = homestay_page.render()

import oshc_page  # noqa: E402 — rebuilt from the live Wix page (22 Nov 2026)
oshc_body = oshc_page.render()

PARTNER_FORM = "https://getwec.pages.dev/partners/migration/"


LABELS_EN = {"where": "Where", "languages": "Languages", "markets": "Clients from", "visa": "Visa types", "contact": "Contact",
             "online": " · online across Australia", "visit": "Visit their migration page",
             "empty": ('<p class="note-box"><strong>List coming soon.</strong> We are checking the first agents now. '
                       'Until then, <a href="/contact-us">ask us for a referral</a>.</p>')}


def partner_cards(partners, labels=LABELS_EN):
    """Cards for registered migration agents (GetWec, status 'listed' only). Every value is escaped;
    links must be https; the agent's personal name is never part of the data."""
    out = []
    for p in partners:
        url = p.get("url") or ""
        if not (p.get("name") and p.get("marn") and url.startswith("https://")):
            continue
        langs = ", ".join(p.get("languages") or [])
        L = labels
        where = e(p.get("city") or "") + (L["online"] if p.get("online_au") else "")
        contact = []
        if p.get("email"):
            contact.append(f'<a href="mailto:{e(p["email"])}">{e(p["email"])}</a>')
        if p.get("phone"):
            contact.append(f'<a href="tel:{e(re.sub(r"[^0-9+]", "", p["phone"]))}">{e(p["phone"])}</a>')
        rows = [("MARN", e(p["marn"])), (L["where"], where), (L["languages"], e(langs)), (L["markets"], e(p.get("markets") or "")),
                (L["visa"], e(", ".join(p.get("visa_types") or []))), (L["contact"], " · ".join(contact))]
        dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows if v)
        intro = f'<p>{e(p["intro"])}</p>' if p.get("intro") else ""
        out.append(f'<li class="agent"><h3>{e(p["name"])}</h3>{intro}<dl>{dl}</dl>'
                   f'<a class="btn ghost" href="{e(url)}" target="_blank" rel="noopener nofollow">{L["visit"]}</a></li>')
    if not out:
        return labels["empty"]
    return f'<ul class="agents">{"".join(out)}</ul>'


MIGRATION_PARTNERS = json.loads((ROOT / "content/migration-partners.json").read_text()).get("partners", [])

migration_body = f"""<section class="wrap narrow"><h1>Migration support</h1>
<p class="lead">Study help and visa advice are different jobs. We help with study. For visa questions, choose a registered migration agent.</p>
{sections([("What we do", "Course questions, booking times to talk and handling study documents for your school application."),
           ("Visa advice", "Visa eligibility, visa strategy and visa applications must be handled by a registered migration agent or lawyer. Our AI assistant is not a migration agent.")])}
<h2 id="agents">Registered migration agents</h2>
<p>We are not a migration agent. To give you more choices, we list registered migration agents who do migration work only.
<strong>We don't receive any commission or benefit from listed agents.</strong> Each agent gave us these details and asked to be listed.
We check every MARN on the official register before we list an agent, but please check it yourself too and talk to the agent directly. No visa outcome is guaranteed.</p>
{partner_cards(MIGRATION_PARTNERS)}
<p class="small">Are you a registered migration agent who only does migration work? <a href="{PARTNER_FORM}" target="_blank" rel="noopener">List your practice for free</a>.</p>
{VISA_NOTE}{cta("Not sure who to ask? Send us a message and we point you to a registered migration agent.")}</section>"""

import about_page  # noqa: E402 — about + referral partners rebuilt from the live Wix pages (22 Nov 2026)
partners_body = about_page.partners()

import faq_page  # noqa: E402 — one help page for every question, by topic (22 Nov 2026)
faq_body, faq_ld = faq_page.render("en", VISA_NOTE)

about_body = about_page.about()

privacy_body = f"""<section class="wrap narrow">
<h1>Privacy notice</h1>
<p class="lead">How We International Education &amp; Visa Pty Ltd handles the information you give us. Questions: <a href="mailto:info@weintervisa.com?subject=Privacy">info@weintervisa.com</a>.</p>
<h2>What we collect</h2>
<p>Only what you choose to send: for example your name, email or phone / LINE ID, where you are, what you want to study and your message.
Please do not send passport numbers, identity or money documents in a general message. If we need them, we give you a secure way to share them.</p>
<h2>Why we use it</h2>
<p>To reply to you and to help with the study service you asked for. If you tick the news box, we may also email you course news. You can stop this at any time.</p>
<h2>Where it is kept</h2>
<p>Messages from our website forms and chat go into our own customer system, GetWec, which stores data on servers in Sydney, Australia.
Access is limited to our team, by role. Our email is provided by Google Workspace.</p>
<h2>AI assistant</h2>
<p>Our website chat assistant is an AI. It answers general questions from information our team has approved, and passes your details to our team when you ask it to. It does not give visa advice.</p>
<h2>Sharing</h2>
<p>We share your details with a school, or with a registered migration agent for a referral, only when it is needed for the service you asked for and you agree.</p>
<h2>No tracking</h2>
<p>This website does not use cookies, analytics or advertising trackers.</p>
<h2>See or correct your information</h2>
<p>Email <a href="mailto:info@weintervisa.com?subject=Privacy">info@weintervisa.com</a> to see your information, ask for a correction or deletion, or raise a privacy concern.
If you are not happy with our reply, you can contact the Office of the Australian Information Commissioner (OAIC).</p>
<p class="hint">Last updated: 20 November 2026.</p>
</section>"""

CONTENT_PAGES = {
    "about-we-international": ("About We International | Student first",
        "We International is a Sydney education agency that helps students explore study in Australia, with honest, student-first support.", about_body),
    "courses": ("Australian college and university courses | We International",
        "Explore 97 Australian courses, from Certificate III in care to business, cookery, trades, IT and degrees, by interest or city. Ask us to compare colleges.", courses_body),
    "courses/nursing-pathways-australia": ("Nursing pathways in Australia | English and OBA preparation",
        "Nursing registration pathways in Australia and preparation for English, NCLEX-RN and OSCE. Ask We International about fees, dates and study options.", nursing_body),
    "fast-track-courses": ("Working Holiday courses (417/462) | We International",
        "On a 417 or 462 visa? Study a practical Certificate III in care, health or childcare with work placement, and ask for a free course plan.", fast_track_body),
    "english-practice": ("Free English practice | We International",
        "Practise everyday English for free: an 8-question quiz, Say It Wrong and Wobbi Says videos, games, and help finding an English course in Australia.", english_body),
    "student-services": ("Student services | We International",
        "Help with choosing a course, applying to a school and getting ready to study in Australia.", services_body),
    "homestay": ("Homestay in Australia with AHN | We International",
        "Start with a homestay: a screened host family near your school, meals, bills and 24/7 support with our partner AHN. Steps, 2026/2027 prices and FAQs.", homestay_body),
    "oshc": ("Overseas Student Health Cover (OSHC) | We International",
        "Compare Allianz, Bupa, Medibank and AHM student health cover (OSHC) and buy directly on our partner's website. What OSHC is and what to check before you buy.", oshc_body),
    "migration-support": ("Migration support | We International",
        "We help with study. Find a registered migration agent for visa questions — we receive no commission from listed agents.", migration_body),
    "referral-partners": ("Partner with us | We International",
        "Schools, colleges and student service providers can talk to We International about working together.", partners_body),
    "frequently-asked-questions": ("FAQs | We International",
        "Answers about study, Working Holiday courses, nursing, homestay, health cover (OSHC) and working with We International in Australia.", faq_body),
    "privacy-policy": ("Privacy notice | We International",
        "How We International Education & Visa Pty Ltd collects, uses and protects your information.", privacy_body),
}
CONTENT_PAGES.update(schools.PAGES)
JSONLD = {"frequently-asked-questions": faq_ld}
