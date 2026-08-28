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
    var hasBackend = !!form.querySelector('input[name="access_key"]');
    var get = function (n) { var el = form.elements[n]; return el ? String(el.value || '').trim() : ''; };

    function setNote(msg) { if (note) note.textContent = msg; }

    function fallbackMailto() {
      var lines = ['Name: ' + get('name'), 'Phone: ' + get('phone'), 'Email: ' + get('email'), 'Service: ' + get('service')];
      if (get('pest')) lines.push('Seeing: ' + get('pest'));
      if (get('city')) lines.push('City: ' + get('city'));
      var body = lines.join('\n') + '\n\n' + get('message');
      var subject = 'Free estimate request' + (get('name') ? ' — ' + get('name') : '');
      window.location.href = 'mailto:' + OFFICE + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      setNote('Opening your email app… if nothing happens, call (737) 201-3059.');
    }

    function showSuccess() {
      form.innerHTML = '<div class="form-success"><strong>Thank you — your request is on its way.</strong>' +
        '<p>A member of our team will get back to you shortly. Need us sooner? Call ' +
        '<a href="tel:+17372013059">(737) 201-3059</a>.</p></div>';
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!get('name') || !get('phone')) {
        setNote('Please add your name and phone number so we can reach you.');
        var miss = form.elements[get('name') ? 'phone' : 'name'];
        if (miss && miss.focus) miss.focus();
        return;
      }
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
