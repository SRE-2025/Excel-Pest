/* Small, dependency-free site scripts. */
(function () {
  var base = window.__BASE__ || '';
  var pagePath = location.pathname.slice(base.length) || '/';
  var production = /^(www\.)?excelpest-lawncontrol\.com$/.test(location.hostname);
  function track(name, extra) {
    if (!production || typeof window.gtag !== 'function') return false;
    var params = { page_path: pagePath, transport_type: 'beacon' };
    Object.keys(extra || {}).forEach(function (key) { params[key] = extra[key]; });
    window.gtag('event', name, params);
    return true;
  }
  // Interaction counts are not completed calls or booked jobs. Never read user
  // contact fields, free text, or an arbitrary URL query into analytics events.
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var href = link.getAttribute('href');
    var eventName = /^tel:/i.test(href) ? 'phone_click' : /^sms:/i.test(href) ? 'sms_click' : /^mailto:/i.test(href) ? 'email_click' : '';
    var placement = link.closest('.mobile-actionbar, .mobile-bar') ? 'mobile_bar' : link.closest('header') ? 'header' : link.closest('footer') ? 'footer' : 'content';
    if (eventName) track(eventName, { link_placement: placement });
    else if (link.pathname === base + '/contact.html') track('estimate_cta_click', { link_placement: placement });
  });
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
    var serviceLabels = {
      'pest-control': 'General Pest Control (ants, roaches, spiders, scorpions, crickets)',
      'ant-control': 'General Pest Control (ants, roaches, spiders, scorpions, crickets)',
      'cockroach-control': 'General Pest Control (ants, roaches, spiders, scorpions, crickets)',
      'scorpion-control': 'General Pest Control (ants, roaches, spiders, scorpions, crickets)',
      'cricket-control': 'General Pest Control (ants, roaches, spiders, scorpions, crickets)',
      'spider-control': 'General Pest Control (ants, roaches, spiders, scorpions, crickets)',
      'rodent-removal': 'Rodents & Wildlife', 'rodent-exclusion': 'Rodents & Wildlife',
      'wildlife-live-trapping': 'Rodents & Wildlife', 'mosquito-misting': 'Mosquitoes',
      'flea-tick-control': 'Flea & Tick', 'lawn-pest-control': 'Lawn Pest Control'
    };
    var requestedService = new URLSearchParams(location.search).get('service');
    if (Object.prototype.hasOwnProperty.call(serviceLabels, requestedService) && form.elements.service) {
      form.elements.service.value = serviceLabels[requestedService];
    }
    var started = false;
    var submitting = false;
    form.addEventListener('input', function () {
      if (!started) { started = true; track('estimate_form_start'); }
    });
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

    function showSuccess(confirmed) {
      var redirected = false;
      function next() {
        if (redirected) return;
        redirected = true;
        window.location.href = base + '/thank-you.html';
      }
      if (!confirmed) { next(); return; }
      var selected = get('service');
      var categories = ['pest-control', 'rodents-wildlife', 'mosquito-misting', 'flea-tick-control', 'lawn-pest-control'];
      var labels = [serviceLabels['pest-control'], serviceLabels['rodent-removal'], serviceLabels['mosquito-misting'], serviceLabels['flea-tick-control'], serviceLabels['lawn-pest-control']];
      var category = categories[labels.indexOf(selected)] || 'unspecified';
      if (Object.prototype.hasOwnProperty.call(serviceLabels, requestedService) && serviceLabels[requestedService] === selected) category = requestedService;
      // Only the successful email-backend response counts as a confirmed form
      // lead. The callback/timeout gives analytics time without blocking users.
      if (!track('generate_lead', { method: 'website_form', service_category: category, event_callback: next, event_timeout: 800 })) next();
      else window.setTimeout(next, 900);
    }

    function fallbackPost() {
      track('estimate_form_fallback');
      if (/^https?:/i.test(form.getAttribute('action') || '')) {
        HTMLFormElement.prototype.submit.call(form);
      } else {
        fallbackMailto();
        submitting = false;
      }
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (submitting) return;
      // Honeypot: if a bot filled the hidden field, pretend success and stop.
      var hp = form.querySelector('.hp');
      if (hp && hp.value) { showSuccess(false); return; }
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      if (!get('name') || !get('email') || !get('phone') || !get('zip')) {
        setNote('Please add your name, email, phone and zip code so we can reach you.');
        var miss = form.elements[!get('name') ? 'name' : (!get('email') ? 'email' : (!get('phone') ? 'phone' : 'zip'))];
        if (miss && miss.focus) miss.focus();
        return;
      }
      submitting = true;
      // Durable capture first — this is the safety net that survives an email error.
      captureToSheet();
      if (hasBackend && window.fetch) {
        setNote('Sending…');
        fetch(ajaxEndpoint, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error('Estimate request failed'); return r.json(); })
          .then(function (j) { if (j && (j.success === true || j.success === 'true')) { showSuccess(true); } else { fallbackPost(); } })
          .catch(fallbackPost);
      } else {
        fallbackMailto();
        submitting = false;
      }
    });
  }
})();
