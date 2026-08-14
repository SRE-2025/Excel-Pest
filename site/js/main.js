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
})();
