/* Site Dr. Diego Aires - núcleo: rolagem suave, revelações e falhas seguras.
   A abertura vive em hero.js. Sem JS (ou se algo falhar) todo o conteúdo continua visível. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = window.matchMedia('(max-width: 768px)').matches;
  var S = (window.SiteDiego = { reduced: reduced, mobile: mobile, lenis: null });
  var temGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  if (temGsap) window.gsap.registerPlugin(window.ScrollTrigger);

  function initSmooth() {
    if (reduced || typeof window.Lenis === 'undefined') return;
    var lenis = new window.Lenis({ duration: 1.1, smoothWheel: true });
    S.lenis = lenis;
    if (temGsap) {
      lenis.on('scroll', window.ScrollTrigger.update);
      window.gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      window.gsap.ticker.lagSmoothing(0);
    } else {
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0);
    }
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var alvo = document.querySelector(a.getAttribute('href'));
        if (!alvo || a.getAttribute('aria-disabled') === 'true') return;
        e.preventDefault();
        lenis.scrollTo(alvo, { offset: -64 });
      });
    });
  }

  /* Revelação por scroll sem IntersectionObserver/rAF (não disparam no painel embutido): listener + getBoundingClientRect. */
  function sweepReveals() {
    var h = window.innerHeight || document.documentElement.clientHeight;
    document.querySelectorAll('.reveal:not(.in-view)').forEach(function (el) {
      if (el.getBoundingClientRect().top < h * 0.9) el.classList.add('in-view');
    });
  }

  function initReveals() {
    if (reduced) {
      document.querySelectorAll('.reveal').forEach(function (e) { e.classList.add('in-view'); });
      return;
    }
    var pendente = false;
    function agenda() {
      if (pendente) return;
      pendente = true;
      setTimeout(function () { pendente = false; sweepReveals(); }, 60);
    }
    window.addEventListener('scroll', agenda, { passive: true });
    window.addEventListener('resize', agenda);
    sweepReveals();
  }

  /* O mapa do Google só carrega ao clique (sem cookies de terceiros por conta própria). */
  function initMapa() {
    var box = document.getElementById('mapa');
    if (!box) return;
    var f = document.createElement('iframe');
    f.src = box.getAttribute('data-src');
    f.title = 'Localização da Medicina Cardeal';
    f.loading = 'lazy';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    box.appendChild(f);
  }

  S.initSmooth = initSmooth;
  S.initReveals = initReveals;
  S.sweepReveals = sweepReveals;

  try { initReveals(); } catch (e) { document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in-view'); }); }
  try { initMapa(); } catch (e) { /* o link para o Google Maps continua */ }
  try { initSmooth(); } catch (e) { /* rolagem nativa */ }
})();
