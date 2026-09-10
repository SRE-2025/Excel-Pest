/* Small, dependency-free site scripts. */
(function () {
  // Mobile navigation toggle
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Auto-fill the current year in the footer
  var yr = document.querySelectorAll('[data-year]');
  var now = new Date().getFullYear();
  yr.forEach(function (el) { el.textContent = now; });

  // Progressive-enhancement contact form.
  // Until a server-side handler is wired up (Part 1, Sec 5 of the brief, or
  // API Gateway + SES), this composes an email to the office so the form is
  // never a dead end. Swap this for a POST handler when the backend is ready.
  var form = document.querySelector('form[data-estimate]');
  if (form) {
    var note = form.querySelector('[data-form-note]');
    var OFFICE = 'office@excelpest-lawncontrol.com';
    // A real endpoint = any http(s) action (FormSubmit). mailto: is the fallback only.
    var hasBackend = /^https?:/i.test(form.getAttribute('action') || '');
    var SHEET = form.getAttribute('data-lead-sheet') || '';   // durable backup store
    var get = function (n) { var el = form.elements[n]; return el ? String(el.value || '').trim() : ''; };

    function setNote(msg) { if (note) note.textContent = msg; }

    // Durable safety net: log every valid submission to the owner's Google Sheet
    // in parallel with the email, so no lead is lost if email delivery errors.
    // Fire-and-forget (no-cors) — never blocks or breaks the visitor's flow.
    function captureToSheet() {
      if (!SHEET || !window.fetch) return;
      try {
        var fd = new FormData(form);
        fd.append('_page', location.pathname);
        fd.append('_ts', new Date().toISOString());
        fetch(SHEET, { method: 'POST', mode: 'no-cors', body: fd }).catch(function () {});
      } catch (e) {}
    }

    function fallbackMailto() {
      var lines = ['Name: ' + get('name'), 'Phone: ' + get('phone'), 'Email: ' + get('email'), 'Service: ' + get('service')];
      if (get('pest')) lines.push('Seeing: ' + get('pest'));
      if (get('city')) lines.push('City: ' + get('city'));
      var body = lines.join('\n') + '\n\n' + get('message');
      var subject = 'Free estimate request' + (get('name') ? ' — ' + get('name') : '');
      window.location.href = 'mailto:' + OFFICE + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      setNote('Opening your email app… if nothing happens, call (512) 291-5900.');
    }

    function showSuccess() {
      // Redirect to a real thank-you page (conversion goal for analytics).
      window.location.href = '/thank-you.html';
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // Honeypot: if a bot filled the hidden field, pretend success and stop.
      var hp = form.querySelector('.hp');
      if (hp && hp.value) { showSuccess(); return; }
      if (!get('name') || !get('phone') || !get('email')) {
        setNote('Please add your name, phone and email so we can reach you.');
        var miss = form.elements[!get('name') ? 'name' : (!get('phone') ? 'phone' : 'email')];
        if (miss && miss.focus) miss.focus();
        return;
      }
      // Durable capture first — this is the safety net that survives an email error.
      captureToSheet();
      if (hasBackend && window.fetch) {
        setNote('Sending…');
        fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
          .then(function (r) { return r.json(); })
          .then(function (j) { if (j && j.success) { showSuccess(); } else { fallbackMailto(); } })
          .catch(fallbackMailto);
      } else {
        fallbackMailto();
      }
    });
  }
})();
