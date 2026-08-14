/* =========================================================================
   Austin Excel Pest & Lawn Control — interactive + motion engine
   Vanilla JS, no dependencies. Decorative motion respects reduced-motion.
   ========================================================================= */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Scroll progress bar ---------- */
  var bar = $(".scroll-progress");
  /* ---------- Header shrink ---------- */
  var header = $(".site-header");
  /* ---------- Back to top ---------- */
  var toTop = $(".to-top");

  function onScroll() {
    var st = window.pageYOffset || document.documentElement.scrollTop;
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (st / h) * 100 : 0) + "%";
    }
    if (header) header.classList.toggle("is-stuck", st > 10);
    if (toTop) toTop.classList.toggle("show", st > 600);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealSel = ".section > .container > .grid > *, .card, .review-card, .stat, .offer-strip, " +
                  ".crosslink, .spotlight, .flow .step, .pest-panel, .checker, .section-head, .prose";
  if (!reduce && "IntersectionObserver" in window) {
    var targets = $$(revealSel).filter(function (el) { return !el.closest(".site-footer"); });
    targets.forEach(function (el, i) {
      el.classList.add("reveal");
      if (el.parentElement && el.parentElement.matches(".grid, .flow, .pest-grid")) {
        el.classList.add("d" + ((i % 4) + 1));
      }
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (el) { io.observe(el); });
    // Safety: reveal everything after 4s in case something is missed
    setTimeout(function () { targets.forEach(function (el) { el.classList.add("in"); }); }, 4000);
  }

  /* ---------- Count-up stats ---------- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var decimals = (el.getAttribute("data-decimals") | 0);
    var suffix = el.getAttribute("data-suffix") || "";
    var dur = 1400, start = null;
    if (reduce) { el.textContent = target.toFixed(decimals) + suffix; return; }
    function tick(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * eased).toFixed(decimals) + suffix;
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = target.toFixed(decimals) + suffix;
    }
    requestAnimationFrame(tick);
  }
  var counters = $$("[data-count]");
  if (counters.length) {
    if ("IntersectionObserver" in window) {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { animateCount(e.target); cio.unobserve(e.target); }
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { cio.observe(el); });
    } else {
      counters.forEach(animateCount);
    }
  }

  /* ---------- Pest identifier ---------- */
  var pestGrid = $("[data-pest-grid]");
  var pestPanel = $("[data-pest-panel]");
  if (pestGrid && pestPanel) {
    var buttons = $$(".pest-btn", pestGrid);
    function showPest(btn) {
      buttons.forEach(function (b) { b.classList.remove("active"); b.setAttribute("aria-pressed", "false"); });
      btn.classList.add("active"); btn.setAttribute("aria-pressed", "true");
      pestPanel.innerHTML =
        '<div class="fade-swap">' +
          '<div class="emo-lg">' + btn.getAttribute("data-emo") + '</div>' +
          '<h3>' + btn.getAttribute("data-name") + '</h3>' +
          '<p><strong>Signs:</strong> ' + btn.getAttribute("data-signs") + '</p>' +
          '<p>' + btn.getAttribute("data-desc") + '</p>' +
          '<a class="btn btn--primary" href="' + btn.getAttribute("data-href") + '">' +
            btn.getAttribute("data-cta") + ' →</a>' +
        '</div>';
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () { showPest(b); });
    });
    if (buttons[0]) showPest(buttons[0]);
  }

  /* ---------- Service-area checker ---------- */
  var checker = $("[data-checker]");
  if (checker) {
    var input = $("input", checker);
    var result = $(".checker__result", checker);
    var cities = JSON.parse(checker.getAttribute("data-cities") || "[]");   // [{name, slug}]
    var zipHint = /^\d{5}$/;
    function normalize(s) { return s.toLowerCase().replace(/[^a-z0-9]/g, ""); }
    function check(e) {
      if (e) e.preventDefault();
      var raw = (input.value || "").trim();
      if (!raw) { result.className = "checker__result"; result.textContent = ""; return; }
      var n = normalize(raw);
      var match = null;
      for (var i = 0; i < cities.length; i++) {
        if (normalize(cities[i].name) === n || normalize(cities[i].name).indexOf(n) === 0) { match = cities[i]; break; }
      }
      if (match && match.slug) {
        result.className = "checker__result hit";
        result.innerHTML = '✓ Yes — we\'ve served <span class="chip">' + match.name +
          '</span> since 1998. <a href="/locations/' + match.slug + '.html">See your local page →</a>';
      } else if (match) {
        result.className = "checker__result hit";
        result.innerHTML = '✓ Yes — <span class="chip">' + match.name +
          '</span> is in our service area. <a href="/contact.html">Get a free estimate →</a>';
      } else if (zipHint.test(raw)) {
        result.className = "checker__result miss";
        result.innerHTML = 'We serve much of Central Texas around Buda, Kyle &amp; San Marcos. ' +
          'Give us your ZIP by phone: <a href="tel:+17372013059">(737) 201-3059</a>.';
      } else {
        result.className = "checker__result miss";
        result.innerHTML = 'We may reach you — we cover 27 Central Texas cities. ' +
          '<a href="/service-area.html">See the full area</a> or <a href="/contact.html">ask us</a>.';
      }
    }
    checker.addEventListener("submit", check);
    var go = $("[data-checker-go]", checker);
    if (go) go.addEventListener("click", check);
  }

  /* ---------- Testimonial spotlight ---------- */
  var spot = $("[data-spotlight]");
  if (spot) {
    var slides = $$(".spotlight__slide", spot);
    var dotsWrap = $(".spotlight__dots", spot);
    var idx = 0, timer = null;
    slides.forEach(function (_, i) {
      var d = document.createElement("button");
      d.setAttribute("aria-label", "Show review " + (i + 1));
      d.addEventListener("click", function () { go(i); rearm(); });
      dotsWrap.appendChild(d);
    });
    var dots = $$("button", dotsWrap);
    function go(i) {
      slides[idx].classList.remove("on"); dots[idx].classList.remove("on");
      idx = (i + slides.length) % slides.length;
      slides[idx].classList.add("on"); dots[idx].classList.add("on");
    }
    function rearm() {
      if (reduce || slides.length < 2) return;
      clearInterval(timer);
      timer = setInterval(function () { go(idx + 1); }, 6000);
    }
    go(0); rearm();
  }

  /* ---------- FAQ accordion ---------- */
  $$(".acc-item").forEach(function (item) {
    var head = $(".acc-head", item);
    var body = $(".acc-body", item);
    if (!head || !body) return;
    head.setAttribute("aria-expanded", "false");
    head.addEventListener("click", function () {
      var open = item.classList.toggle("open");
      head.setAttribute("aria-expanded", open ? "true" : "false");
      body.style.maxHeight = open ? body.scrollHeight + "px" : null;
    });
  });
})();
