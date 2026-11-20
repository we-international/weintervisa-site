"""Static pages of the new weintervisa.com (same paths as Wix).

Only facts we can stand behind: no promised reply times, prices or "free" claims until the owner
approves them (see GetWec KB questions). Visa questions always go to a registered migration agent.
Each entry: path (no leading slash) → (title, description, body HTML).
"""

CONSENT = """<div class="field check">
  <label><input type="checkbox" name="consent" required> <span>I agree that We International Education &amp; Visa Pty Ltd may keep these details to contact me about my enquiry (<a href="/privacy-policy">privacy policy</a>).</span></label>
  <span class="err" data-err="consent"></span>
</div>
<div class="field check">
  <label><input type="checkbox" name="marketing"> <span>Send me course news and offers by email (optional, stop any time).</span></label>
</div>
<div class="hp" aria-hidden="true"><label>Leave this empty <input name="website" tabindex="-1" autocomplete="off"></label></div>"""

CONTACT_FIELDS = """<div class="field"><label for="{k}-name">Full name *</label>
  <input id="{k}-name" name="full_name" autocomplete="name" required maxlength="120"><span class="err" data-err="full_name"></span></div>
<div class="row2">
  <div class="field"><label for="{k}-email">Email</label>
    <input id="{k}-email" name="email" type="email" autocomplete="email" maxlength="200"><span class="err" data-err="email"></span></div>
  <div class="field"><label for="{k}-phone">Phone or LINE ID</label>
    <input id="{k}-phone" name="phone" autocomplete="tel" maxlength="60"></div>
</div>
<p class="hint">Email or phone / LINE: one is enough.</p>
<div class="field"><label for="{k}-loc">Where are you now?</label>
  <select id="{k}-loc" name="location" data-summary="Now in"><option value="">Choose…</option>
  <option value="australia">In Australia</option><option value="thailand">In Thailand</option><option value="other">Somewhere else</option></select></div>"""

VISA_NOTE = """<p class="note-box"><strong>Visa questions?</strong> We are an education agency, not a migration agent.
We can give general information about courses and study. For advice about your visa, we refer you to a
registered migration agent.</p>"""

contact_form = f"""<form class="lead" data-lead-form="enquiry" novalidate>
<h2>Send us a message</h2>
{CONTACT_FIELDS.format(k="c")}
<div class="field"><label for="c-topic">What is it about?</label>
  <select id="c-topic" name="topic" data-summary="Topic"><option value="">Choose…</option>
  <option>Courses and schools</option><option>Fast-track courses</option><option>Homestay</option>
  <option>OSHC (student health cover)</option><option>Partnership (school or agent)</option><option>Something else</option></select></div>
<div class="field"><label for="c-msg">Your message</label>
  <textarea id="c-msg" name="message" rows="5" maxlength="800"></textarea></div>
{CONSENT}
<button class="btn" type="submit">Send message</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>"""

contact_body = f"""<section class="wrap narrow">
<h1>Contact us</h1>
<p class="lead">Ask about courses, schools, homestay or student health cover. Our team reads every message.</p>
<ul class="contact-list">
  <li><strong>Email</strong> <a href="mailto:info@weintervisa.com">info@weintervisa.com</a></li>
  <li><strong>Blog</strong> <a href="/blog">Plain-English guides</a> on courses and life in Australia</li>
</ul>
{VISA_NOTE}
{contact_form}
</section>"""

apply_form = f"""<form class="lead" data-lead-form="application" novalidate>
<h2>Your details</h2>
{CONTACT_FIELDS.format(k="a")}
<h2>What you want to study</h2>
<div class="field"><label for="a-field">Course area</label>
  <select id="a-field" name="field" data-summary="Course area"><option value="">Choose…</option>
  <option>Aged care / individual support</option><option>Nursing pathway</option><option>Early childhood education</option>
  <option>Health services assistance</option><option>English</option><option>Business / other</option><option>Not sure yet</option></select></div>
<div class="row2">
  <div class="field"><label for="a-level">Level</label>
    <select id="a-level" name="level" data-summary="Level"><option value="">Choose…</option>
    <option>Short course</option><option>Certificate III</option><option>Certificate IV</option><option>Diploma</option>
    <option>Bachelor or higher</option><option>Not sure yet</option></select></div>
  <div class="field"><label for="a-start">When do you want to start?</label>
    <input id="a-start" name="start" type="month" data-summary="Start"></div>
</div>
<div class="row2">
  <div class="field"><label for="a-city">Preferred city</label>
    <select id="a-city" name="city" data-summary="City"><option value="">Choose…</option>
    <option>Sydney</option><option>Melbourne</option><option>Brisbane</option><option>Perth</option><option>Adelaide</option>
    <option>Online</option><option>Any</option></select></div>
  <div class="field"><label for="a-eng">Your English</label>
    <select id="a-eng" name="english" data-summary="English"><option value="">Choose…</option>
    <option>Beginner</option><option>Can talk about daily life</option><option>Good / work level</option>
    <option>Have a test score (IELTS, PTE…)</option></select></div>
</div>
<div class="field"><label for="a-visa">If you are in Australia: your current visa (optional)</label>
  <input id="a-visa" name="visa" maxlength="60" placeholder="e.g. Working Holiday 417" data-summary="Current visa"></div>
<div class="field"><label for="a-msg">Anything else we should know?</label>
  <textarea id="a-msg" name="message" rows="4" maxlength="800"></textarea></div>
<p class="hint">Please do not send passport numbers or documents here. If we need them, we will send you a secure way to share them.</p>
{CONSENT}
<button class="btn" type="submit">Send application</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>"""

apply_body = f"""<section class="wrap narrow">
<h1>Study application</h1>
<p class="lead">Tell us what you want to study. Our team checks course options and entry needs with you, then helps with the school application.</p>
<ol class="steps"><li>Send this form</li><li>We contact you to talk about courses</li><li>You choose a course and we help you apply to the school</li></ol>
{VISA_NOTE}
{apply_form}
</section>"""

PAGES = {
    "contact-us": ("Contact us | We International",
                   "Ask We International about courses, schools, homestay or student health cover in Australia.",
                   contact_body),
    "charter-application": ("Study application | We International",
                            "Tell us what you want to study in Australia and our team will contact you about course options.",
                            apply_body),
}
