/*! weintervisa.com lead forms → GetWec (no cookies, no tracking, nothing stored in the browser).
 * A form with data-lead-form="<kind>" posts once to the GetWec "mia" Edge Function, action "lead"
 * (same contract as the Mia web chat: full_name, email, phone, location, interest, consent,
 * marketing, transcript, lang, page, website=honeypot).
 * Endpoint + public anon key come from <meta name="getwec-endpoint"> / <meta name="getwec-key">.
 * If either is missing (preview build), the form is checked but NOT sent; it says so on screen.
 */
(function () {
  'use strict';
  var meta = function (n) { var m = document.querySelector('meta[name="' + n + '"]'); return m ? m.content : ''; };
  var endpoint = meta('getwec-endpoint');
  var key = meta('getwec-key');
  var live = !!(endpoint && key);
  var EMAIL_RE = /^[^@\s]{1,64}@[^@\s]{1,190}\.[a-z]{2,}$/i; // same as GetWec validateLead

  function val(f, name) {
    var el = f.elements[name];
    if (!el) return '';
    if (el.type === 'checkbox') return el.checked;
    return String(el.value || '').trim();
  }

  // Build the GetWec payload. interest ≤ 300 chars (short subject); the full message goes in the transcript.
  function payload(f) {
    var kind = f.getAttribute('data-lead-form');
    var parts = [];
    var label = { enquiry: 'Enquiry', application: 'Study application' }[kind] || 'Website form';
    var fields = f.querySelectorAll('[data-summary]');
    for (var i = 0; i < fields.length; i++) {
      var v = val(f, fields[i].name);
      if (v) parts.push(fields[i].getAttribute('data-summary') + ': ' + v);
    }
    var interest = (label + (parts.length ? ' · ' + parts.join(' · ') : '')).slice(0, 300);
    var lines = ['[' + label + ' form on ' + location.pathname + ']'].concat(parts);
    var msg = val(f, 'message');
    if (msg) lines.push('Message: ' + msg);
    return {
      action: 'lead',
      form: kind, // GetWec saves the contact as source "form:<kind>" (not chat)
      full_name: val(f, 'full_name'),
      email: val(f, 'email').toLowerCase(),
      phone: val(f, 'phone'),
      location: val(f, 'location') || undefined,
      interest: interest,
      consent: val(f, 'consent') === true,
      marketing: val(f, 'marketing') === true,
      website: val(f, 'website'),
      lang: 'en',
      page: location.pathname,
      transcript: [{ role: 'user', text: lines.join('\n').slice(0, 1000) }],
    };
  }

  // Same rules as GetWec validateLead, so people see problems before sending.
  function check(p) {
    var e = {};
    if (p.full_name.length < 2) e.full_name = 'Please add your name.';
    if (p.email && !EMAIL_RE.test(p.email)) e.email = 'Please check your email address.';
    if (!p.email && p.phone.length < 5) e.email = 'Please add an email, or a phone / LINE we can use.';
    if (!p.consent) e.consent = 'Please tick the box so we can contact you.';
    return e;
  }

  function show(f, errors) {
    var boxes = f.querySelectorAll('[data-err]');
    for (var i = 0; i < boxes.length; i++) boxes[i].textContent = errors[boxes[i].getAttribute('data-err')] || '';
    var first = Object.keys(errors)[0];
    if (first && f.elements[first]) f.elements[first].focus();
  }

  function status(f, cls, text) {
    var s = f.querySelector('.form-status');
    s.className = 'form-status ' + cls;
    s.textContent = text;
  }

  function bind(f) {
    if (!live) status(f, 'note', 'Preview: this form is not connected yet. Nothing will be sent.');
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var p = payload(f);
      var errors = check(p);
      show(f, errors);
      if (Object.keys(errors).length) return;
      if (p.website) { status(f, 'ok', 'Thanks! We will contact you soon.'); return; } // bot: pretend
      window.__lastLeadPayload = p; // for tests only; never stored
      if (!live) { status(f, 'ok', 'Preview check passed. In the live site this goes to our team.'); return; }
      var btn = f.querySelector('button[type="submit"]');
      btn.disabled = true;
      status(f, 'note', 'Sending…');
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: key, Authorization: 'Bearer ' + key },
        body: JSON.stringify(p),
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, d: d }; });
      }).then(function (res) {
        if (res.ok && res.d.ok) {
          f.reset();
          status(f, 'ok', 'Thanks! We got your details. Our team will contact you soon.');
        } else if (res.d.errors && res.d.errors.rate) {
          status(f, 'bad', 'Too many tries. Please email info@weintervisa.com instead.');
        } else {
          status(f, 'bad', 'Something was missing. Please check the form and try again.');
        }
      }).catch(function () {
        status(f, 'bad', 'Could not send. Please try again, or email info@weintervisa.com.');
      }).then(function () { btn.disabled = false; });
    });
  }

  var forms = document.querySelectorAll('form[data-lead-form]');
  for (var i = 0; i < forms.length; i++) bind(forms[i]);
})();
