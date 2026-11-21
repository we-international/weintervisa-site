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
    return f'<aside class="cta"><p>{text}</p><a class="btn" href="{href}">Send a message</a>{extra}</aside>'


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
    f'<h2 id="{e(g.lower().replace(" & ", "-").replace(" ", "-"))}">{e(g)}</h2><ul class="areas">'
    + "".join(f'<li><strong>{e(a["title"])}</strong><span>{e(a.get("description") or "")}</span></li>' for a in items)
    + "</ul>" for g, items in groups.items())
courses_body = f"""<section class="wrap">
<h1>Find a study area that feels like you</h1>
<p class="lead">Browse {len(areas)} study areas, from English to care, business, trades and more. Tell us what you like and we look at current options with you.</p>
<p class="note-box"><strong>About this list.</strong> These are study areas, not a promise that every course is open through us.
We share a course name, CRICOS code, fees, campus and start date only after we check them with the school.</p>
<p><a class="btn" href="/charter-application">Tell us what you want to study</a> <a class="btn ghost" href="/courses/nursing-pathways-australia">Nursing pathways</a></p>
{'<p>See courses and fees from <a href="/schools">schools that sent us their details</a>.</p>' if schools.SCHOOLS else ""}
<h2>Study levels</h2>
<ul class="list">
<li><strong>English and pathways</strong> — language study or a foundation course before your next qualification.</li>
<li><strong>Vocational study</strong> — practical Certificate, Diploma and Advanced Diploma courses. Entry and placement rules depend on the course.</li>
<li><strong>University</strong> — bachelor, master and research study. Each university sets its own entry and English rules.</li>
</ul>
{area_html}
{cta("Not sure which area fits? Tell us your interests, past study, city and budget.", "/contact-us")}
</section>"""

nursing_body = simple(
    "Nursing pathways in Australia",
    "Are you a nurse trained outside Australia? Learn the main steps to work as a nurse here, and ask us about preparation courses.",
    [("Who decides registration", "Nurses in Australia must be registered with the Nursing and Midwifery Board of Australia (NMBA) through Ahpra. "
      "They decide if you can register. We help with study and course choices, not with the registration decision."),
     ("English first", "Most pathways need a recognised English test result. We can help you find English or test preparation courses."),
     ("Outcomes-based assessment", "Many internationally qualified nurses take the NMBA outcomes-based assessment: the NCLEX-RN exam and then the OSCE. "
      "Ask us about preparation options that fit your timeline."),
     ("Check the official rules", "Rules change. Always check your own pathway on the official Ahpra and NMBA websites before you pay for a course.")],
    note=True, cta_text="Ask us about fees, dates and study options for nursing preparation.")

import fasttrack_page  # noqa: E402 — rebuilt from the live Wix page (21 Nov 2026)
fast_track_body = fasttrack_page.render()

import englishpractice_page  # noqa: E402 — rebuilt from the live Wix page (21 Nov 2026)
english_body = englishpractice_page.render()

services_body = simple(
    "Student services",
    "Help with the steps around your study: choosing a course, applying to a school and getting ready to start.",
    [("Course advice", "Talk through your goals and compare checked course options."),
     ("Application help", "We help you track your documents, your application status and replies from the school."),
     ("Student support", "Ask us for help with orientation information, school contacts and support referrals."),
     ("Your language", "Chat with Mia, our AI assistant, in many languages. Our team speaks Thai and English, so a reply from a person is in Thai or English."),
     ("More help", "<a href=\"/homestay\">Homestay and places to live</a> · <a href=\"/oshc\">Student health cover (OSHC)</a> · <a href=\"/english-practice\">English study</a>")],
    cta_text="Start a conversation with our team.")

homestay_body = simple(
    "Homestay and places to live",
    "Find a place that works for your routine. Here is what to think about while we prepare checked accommodation links.",
    [("Homestay", "Live with a local host. Ask about location, meals, house rules, price and the terms from the homestay provider."),
     ("Student accommodation", "Check the exact address, what is included, the lease terms and if a room is free."),
     ("Shared rental", "Think about transport, who you live with, your budget and the lease."),
     ("Location matters", "Live close to your campus or good transport. This page does not mean a room is available.")],
    cta_text="Ask about homestay or accommodation.")

oshc_body = simple(
    "Student health cover (OSHC)",
    "Most student visa holders need Overseas Student Health Cover. Plan it alongside your study.",
    [("Ask us about options", "We are preparing checked referral links. Until then, ask the team about current options."),
     ("Read the policy", "Before you buy, compare the start and end dates, who is covered, what is not covered and the terms in the insurer's documents.")],
    cta_text="Ask about health cover.")

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

partners_body = simple(
    "Partner with us",
    "Schools, colleges and student service providers can talk to us about working together.",
    [("Schools and colleges", "Send your school name, website, study areas and a partnership contact. We check the agreement and marketing permissions before we list anyone."),
     ("Service providers", "Tell us what you do, where, and your credentials. Referral arrangements need checking first."),
     ("How to reach us", "Email <a href=\"mailto:info@weintervisa.com?subject=Partnership%20enquiry\">info@weintervisa.com</a> with \"Partnership\" in the subject, or use the contact form and choose \"Partnership\".")],
    cta_text="Ask about a partnership.")

faq = [
    ("Can I apply for every study area on this site?", "Not yet. Some areas are ones we are preparing to support. We tell you which courses are confirmed."),
    ("Will I get three options?", "We aim to compare at least three suitable schools for your study area and city when they are available. We tell you if fewer are confirmed."),
    ("Is a place, a visa or a job guaranteed?", "No. The school decides admission, the government decides visas, and jobs are not guaranteed."),
    ("Do you give visa advice?", "No. We are not a migration agent. For visa advice we refer you to a registered migration agent."),
    ("Can I visit your office?", "We work online. Send us a message and we will arrange a time to talk."),
    ("Can I send my documents now?", "Please start with a short message. Send passports or other private documents only when we give you a secure way to do it."),
    ("Can I talk in my own language?", "Yes, with Mia, our AI assistant: she can chat in many languages. Our team speaks Thai and English, so a reply from a person will be in Thai or English."),
    ("Is the chat assistant a person?", "Our website assistant is an AI. It answers general questions and passes your message to our team."),
]
faq_body = (f'<section class="wrap narrow"><h1>Frequently asked questions</h1>'
            f'<p class="lead">Quick answers about our study support.</p>'
            + "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
            + cta("Still have a question?") + "</section>")
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

about_body = simple(
    "About We International",
    "Honest advice, and a choice that is yours. We International Education &amp; Visa Pty Ltd is a Sydney education agency that helps students explore study in Australia.",
    [("Student first", "Your goals, your situation and your questions lead the conversation."),
     ("Clear and honest", "We check information, explain what is not yet confirmed, and the choice stays with you."),
     ("Online service", "We work online. Send us a message to arrange a time to talk."),
     ("People and AI", "AI may help our team with research, admin and messages. Important decisions stay with a person."),
     ("Registered education agent", "We are listed as a Qualified Education Agent Counsellor (QEAC number in the footer). We are not a migration agent.")],
    cta_text="Meet us through a conversation.")

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
        "Browse study areas in Australia, from English to care, business and trades, and ask our team about checked options, fees and start dates.", courses_body),
    "courses/nursing-pathways-australia": ("Nursing pathways in Australia | English and OBA preparation",
        "Nursing registration pathways in Australia and preparation for English, NCLEX-RN and OSCE. Ask We International about fees, dates and study options.", nursing_body),
    "fast-track-courses": ("Working Holiday courses (417/462) | We International",
        "On a 417 or 462 visa? Study a practical Certificate III in care, health or childcare with work placement, and ask for a free course plan.", fast_track_body),
    "english-practice": ("Free English practice | We International",
        "Practise everyday English for free: an 8-question quiz, Say It Wrong and Wobbi Says videos, games, and help finding an English course in Australia.", english_body),
    "student-services": ("Student services | We International",
        "Help with choosing a course, applying to a school and getting ready to study in Australia.", services_body),
    "homestay": ("Homestay and student accommodation | We International",
        "What to check when choosing homestay, student accommodation or a shared rental in Australia.", homestay_body),
    "oshc": ("Overseas Student Health Cover (OSHC) | We International",
        "Plan your Overseas Student Health Cover and ask our team about current options.", oshc_body),
    "migration-support": ("Migration support | We International",
        "We help with study. Find a registered migration agent for visa questions — we receive no commission from listed agents.", migration_body),
    "referral-partners": ("Partner with us | We International",
        "Schools, colleges and student service providers can talk to We International about working together.", partners_body),
    "frequently-asked-questions": ("FAQs | We International",
        "Quick answers about our study support in Australia.", faq_body),
    "privacy-policy": ("Privacy notice | We International",
        "How We International Education & Visa Pty Ltd collects, uses and protects your information.", privacy_body),
}
CONTENT_PAGES.update(schools.PAGES)
JSONLD = {"frequently-asked-questions": faq_ld}
