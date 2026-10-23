/* A real Austin flyover: poster first, one responsive video, no third-party media. */
(function () {
  'use strict';
  var video = document.querySelector('#austin-flyover');
  var toggle = document.querySelector('.hero-motion-toggle');
  var poster = document.querySelector('.hero-poster img');
  if (!video || !toggle || !poster) return;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  var restricted = reduced.matches || (connection && (connection.saveData || /(^|-)2g$/.test(connection.effectiveType)));
  var wantsPlayback = !restricted;
  var inView = true;
  var failed = false;
  var ready = false;
  toggle.hidden = false;

  function label() {
    toggle.textContent = video.paused ? 'Play Austin flyover' : 'Pause Austin flyover';
  }
  function play() {
    if (failed || !ready || !wantsPlayback || document.hidden || !inView) return;
    if (!video.getAttribute('src')) {
      var mobile = window.matchMedia('(max-width: 700px)').matches;
      video.src = mobile ? video.dataset.videoMobile : video.dataset.videoDesktop;
      video.muted = true;
    }
    var attempt = video.play();
    if (attempt && attempt.catch) attempt.catch(function () { label(); });
  }
  video.addEventListener('playing', function () { video.classList.add('is-playing'); label(); });
  video.addEventListener('pause', label);
  video.addEventListener('error', function () {
    failed = true;
    video.classList.remove('is-playing');
    video.removeAttribute('src');
    video.load();
    toggle.hidden = true;
  });
  toggle.addEventListener('click', function () {
    wantsPlayback = video.paused;
    if (wantsPlayback) play(); else video.pause();
  });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) video.pause(); else play();
  });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      inView = entries[0].isIntersecting;
      if (inView) play(); else video.pause();
    }, {threshold: 0}).observe(video.closest('.hero'));
  }
  function changedMotion() {
    if (reduced.matches) { wantsPlayback = false; video.pause(); }
  }
  if (reduced.addEventListener) reduced.addEventListener('change', changedMotion);
  function posterReady() {
    // Let the still and primary content paint before the optional video request.
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { ready = true; play(); });
    });
  }
  if (poster.decode) poster.decode().catch(function () {}).then(posterReady);
  else if (poster.complete) posterReady();
  else { poster.addEventListener('load', posterReady, {once: true}); poster.addEventListener('error', posterReady, {once: true}); }
}());
