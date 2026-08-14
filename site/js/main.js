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
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var get = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ''; };
      var body =
        'Name: ' + get('name') + '\n' +
        'Phone: ' + get('phone') + '\n' +
        'Email: ' + get('email') + '\n' +
        'Service: ' + get('service') + '\n\n' +
        get('message');
      var subject = 'Free estimate request' + (get('name') ? ' — ' + get('name') : '');
      window.location.href =
        'mailto:office@excelpest-lawncontrol.com' +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);
      var note = form.querySelector('[data-form-note]');
      if (note) {
        note.textContent = 'Opening your email app… if nothing happens, call (737) 201-3059.';
      }
    });
  }
})();
