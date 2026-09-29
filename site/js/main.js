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

  // Progressive-enhancement contact form. FormSubmit emails the office and a
  // Google Sheet records a backup copy; a normal POST remains the no-JS fallback.
  var form = document.querySelector('form[data-estimate]');
  if (form) {
    var note = form.querySelector('[data-form-note]');
    var OFFICE = 'office@excelpest-lawncontrol.com';
    // The AJAX endpoint keeps the visitor on-site. The normal form action is a
    // no-JavaScript and network-error fallback that still delivers to the office.
    var ajaxEndpoint = form.getAttribute('data-ajax-endpoint') || '';
    var hasBackend = /^https?:/i.test(ajaxEndpoint);
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
        // Mirror zip into 'city' too, so the currently-deployed sheet script
        // (which logs a City column) captures it without needing a redeploy.
        if (get('zip')) fd.append('city', get('zip'));
        fetch(SHEET, { method: 'POST', mode: 'no-cors', body: fd }).catch(function () {});
      } catch (e) {}
    }

    function fallbackMailto() {
      var lines = ['Name: ' + get('name'), 'Email: ' + get('email'), 'Phone: ' + get('phone'),
                   'Zip: ' + get('zip'), 'Help with: ' + get('service')];
      var body = lines.join('\n') + '\n\n' + get('message');
      var subject = 'Free estimate request' + (get('name') ? ' — ' + get('name') : '');
      window.location.href = 'mailto:' + OFFICE + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      setNote('Opening your email app… if nothing happens, call (512) 291-5900.');
    }

    function showSuccess() {
      // Record only the conversion event — never the visitor's form fields.
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', { method: 'website_form' });
      }
      window.location.href = '/thank-you.html';
    }

    function fallbackPost() {
      if (/^https?:/i.test(form.getAttribute('action') || '')) {
        HTMLFormElement.prototype.submit.call(form);
      } else {
        fallbackMailto();
      }
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // Honeypot: if a bot filled the hidden field, pretend success and stop.
      var hp = form.querySelector('.hp');
      if (hp && hp.value) { showSuccess(); return; }
      if (!get('name') || !get('email') || !get('phone') || !get('zip')) {
        setNote('Please add your name, email, phone and zip code so we can reach you.');
        var miss = form.elements[!get('name') ? 'name' : (!get('email') ? 'email' : (!get('phone') ? 'phone' : 'zip'))];
        if (miss && miss.focus) miss.focus();
        return;
      }
      // Durable capture first — this is the safety net that survives an email error.
      captureToSheet();
      if (hasBackend && window.fetch) {
        setNote('Sending…');
        fetch(ajaxEndpoint, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
          .then(function (r) { return r.json(); })
          .then(function (j) { if (j && j.success) { showSuccess(); } else { fallbackPost(); } })
          .catch(fallbackPost);
      } else {
        fallbackMailto();
      }
    });
  }
})();
