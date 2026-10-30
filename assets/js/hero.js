/* Abertura: sequência de quadros em canvas + oração em brasa + troca para o logo oficial.
   Só roda no desktop com movimento permitido. No celular, com reduced-motion ou sem GSAP,
   a abertura fica estática (CSS): logo, subtítulo e oração inteira visíveis.
   Sem assets/hero/manifest.json a abertura usa o brilho de brasa em CSS no lugar do vídeo. */
(function () {
  'use strict';
  var S = window.SiteDiego;
  var hero = document.getElementById('inicio');
  if (!S || !hero || S.reduced || S.mobile || !window.gsap || !window.ScrollTrigger) return;

  var stage = hero.querySelector('.hero__stage');
  var canvas = document.getElementById('hero-canvas');
  var ctx = canvas.getContext('2d');
  var words = hero.querySelectorAll('.oracao .w');
  var oracao = hero.querySelector('.oracao');
  var logo = hero.querySelector('.hero__logo');
  var sub = hero.querySelector('.hero__sub');
  var frames = [];     // Image[] (null enquanto não carregou)
  var total = 0;
  var atual = -1;

  hero.classList.add('hero--scrub');

  function desenha(i) {
    if (!total) return;
    var f = null;
    for (var k = Math.min(i, total - 1); k >= 0; k--) { if (frames[k]) { f = frames[k]; break; } }
    if (!f) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var w = Math.round(canvas.clientWidth * dpr), h = Math.round(canvas.clientHeight * dpr);
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    var esc = Math.max(w / f.naturalWidth, h / f.naturalHeight);
    var dw = f.naturalWidth * esc, dh = f.naturalHeight * esc;
    ctx.drawImage(f, (w - dw) / 2, (h - dh) / 2, dw, dh);
    atual = i;
  }

  function carregaQuadros(m) {
    total = m.count;
    frames = new Array(total).fill(null);
    var nome = function (i) { return 'assets/hero/' + String(i + 1).padStart(4, '0').replace(/^/, 'frame_') + '.webp'; };
    var proximo = 0;
    function lote() {
      for (var n = 0; n < 6 && proximo < total; n++, proximo++) {
        (function (i) {
          var im = new Image();
          im.onload = function () { frames[i] = im; if (i === 0 || i === atual) desenha(atual < 0 ? 0 : atual); };
          im.src = nome(i);
        })(proximo);
      }
      if (proximo < total) setTimeout(lote, 60);
    }
    lote();
  }

  fetch('assets/hero/manifest.json')
    .then(function (r) { if (!r.ok) throw new Error('sem manifest'); return r.json(); })
    .then(function (m) { if (m && m.count > 1) carregaQuadros(m); })
    .catch(function () { /* sem quadros: fica o brilho CSS */ });

  /* estado inicial */
  window.gsap.set(words, { opacity: 0.16 });
  window.gsap.set([logo, sub], { opacity: 0 });
  window.gsap.set(logo, { scale: 0.96 });
  window.gsap.set(stage, { '--brasa': 0 });

  var tl = window.gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: {
      trigger: hero, start: 'top top', end: 'bottom bottom', scrub: 0.6,
      onUpdate: function (self) {
        var i = Math.round(Math.min(self.progress / 0.85, 1) * (total - 1));
        if (total && i !== atual) desenha(i);
      }
    }
  });
  tl.to(words, { opacity: 1, stagger: 0.035, duration: 0.05 }, 0)             // 0 .. ~0.65 (17 palavras)
    .to(stage, { '--brasa': 1, duration: 0.25 }, 0.45)
    .to(oracao, { opacity: 0, duration: 0.22 }, 0.72)       // fixo, só esmaece devagar
    .to(canvas, { opacity: 0.3, duration: 0.12 }, 0.82)
    .to(logo, { opacity: 1, scale: 1, duration: 0.12 }, 0.84)
    .to(sub, { opacity: 1, duration: 0.08 }, 0.92)
    .to({}, { duration: 0.02 }, 0.98);                                           // fecha em 1.0

  window.addEventListener('resize', function () { desenha(atual < 0 ? 0 : atual); });
  window.ScrollTrigger.refresh();
})();
