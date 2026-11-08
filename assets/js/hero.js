/* Abertura em scroll: oração em brasa + vídeo (ou sequência de quadros) + texto do logo em fade.
   Com assets/hero/manifest.json no formato do codificar_scroll.py ({video, fundo[], count, duration}) a abertura
   usa um <video> all-intra seguido por currentTime, centralizado em 9:16 (sem corte lateral), em desktop e celular.
   Com o manifest antigo do frames_hero.py ({count}) usa canvas, só no desktop.
   Sem manifest, com movimento reduzido ou sem GSAP, a abertura fica estática (CSS): logo, subtítulo e oração.
   Sem manifest no desktop usa o brilho de brasa em CSS no lugar do vídeo. */
(function () {
  'use strict';
  var S = window.SiteDiego;
  var hero = document.getElementById('inicio');
  if (!S || !hero || S.reduced || !window.gsap || !window.ScrollTrigger) { if (hero) hero.classList.remove('hero--scrub'); return; }

  fetch('assets/hero/manifest.json')
    .then(function (r) { if (!r.ok) throw new Error('sem manifest'); return r.json(); })
    .catch(function () { return null; })
    .then(iniciar);

  function iniciar(m) {
    var temVideo = !!(m && m.video && m.fundo && m.fundo.length > 1 && m.duration);
    if (S.mobile && !temVideo) { hero.classList.remove('hero--scrub'); return; }

    var stage = hero.querySelector('.hero__stage');
    var canvas = document.getElementById('hero-canvas');
    var ctx = canvas.getContext('2d');
    var words = hero.querySelectorAll('.oracao .w');
    var oracao = hero.querySelector('.oracao');
    var logo = hero.querySelector('.hero__logo');
    var sub = hero.querySelector('.hero__sub');
    var caixa = document.getElementById('hero-video');
    var wm = caixa ? caixa.querySelector('.hero__wordmark') : null;
    var intro = document.getElementById('hero-intro');
    var cta = document.getElementById('hero-cta');
    var vid = null;
    var frames = [];     // Image[] (null enquanto não carregou), só no modo canvas
    var total = 0;
    var atual = -1;

    hero.classList.add('hero--scrub');

    /* ---- modo vídeo ---- */
    function iniciaVideo() {
      total = m.count || m.fundo.length;
      hero.classList.add('hero--video');
      caixa.hidden = false;
      criaVideo();
      hero.style.setProperty('--fundo', m.fundo[0]);
      if (m.borda) hero.style.setProperty('--borda', m.borda[0]);
      armaToque();
      /* Ao sair para o WhatsApp e voltar, o iPhone deixa o <video> "congelado": continua com readyState 4,
         mas mudar currentTime não pinta mais quadro nenhum, e play/pause não resolve. A saída é trocar o
         elemento por um novo (o arquivo já está no cache) e destravar de novo, também no primeiro toque. */
      var saiu = false;
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) { saiu = true; return; }
        if (saiu) { saiu = false; reanima(); }
      });
      window.addEventListener('pagehide', function () { saiu = true; });
      window.addEventListener('pageshow', function (e) { if (e.persisted || saiu) { saiu = false; reanima(); } });
    }
    function criaVideo() {
      var novo = document.createElement('video');
      novo.muted = true; novo.playsInline = true; novo.preload = 'auto'; novo.tabIndex = -1;
      novo.setAttribute('muted', ''); novo.setAttribute('playsinline', ''); novo.setAttribute('webkit-playsinline', '');
      novo.setAttribute('aria-hidden', 'true');
      /* primeiro quadro enquanto carrega; na troca (quadro do meio) fica sem pôster para não piscar o início */
      if (!vid) novo.poster = 'assets/hero/inicio.webp';
      novo.src = 'assets/hero/' + (S.mobile ? m.video.mobile : m.video.desktop);
      /* iPhone (Safari) não baixa os quadros de um vídeo que nunca tocou: só mudar currentTime não mostra nada.
         Toca (sem som) e pausa na hora para "destravar"; se o aparelho bloquear (modo de pouca energia),
         tenta de novo no primeiro toque na tela. */
      novo.addEventListener('loadedmetadata', posiciona);
      novo.addEventListener('loadeddata', function () {
        posiciona(true);
        if (antigo && antigo.parentNode) {                       // troca sem piscar: o novo cobre o antigo até aqui
          antigo.parentNode.removeChild(antigo); antigo = null;
          novo.style.position = ''; novo.style.inset = '';
        }
      });
      var antigo = vid;
      if (antigo) caixa.insertBefore(novo, antigo.nextSibling); else caixa.insertBefore(novo, caixa.firstChild);
      vid = novo;
      if (antigo) { novo.style.position = 'absolute'; novo.style.inset = '0'; }
      destrava();
      diag('criaVideo');
    }
    function armaToque() {
      ['touchstart', 'click'].forEach(function (ev) {
        window.addEventListener(ev, function () { destrava(); diag('toque'); }, { passive: true, once: true });
      });
    }
    function reanima() {
      if (!vid) return;
      diag('volta');
      criaVideo();
      armaToque();
      setTimeout(function () { window.ScrollTrigger.refresh(); window.ScrollTrigger.update(); posiciona(true); }, 150);
    }
    var tocando = false;   // enquanto o play() de destravar não termina, posiciona() não pausa (senão o play aborta)
    function destrava() {
      var v = vid;
      try {
        tocando = true;
        setTimeout(function () { if (tocando) { tocando = false; v.pause(); posiciona(true); } }, 1200);  // se o play travar
        var p = v.play();
        if (p && p.then) p.then(function () { tocando = false; v.pause(); posiciona(true); diag('play ok'); })
          .catch(function (e) { tocando = false; posiciona(true); diag('play recusado: ' + (e && e.name)); });
        else { tocando = false; v.pause(); posiciona(true); }
      } catch (e) { tocando = false; /* segue com o pôster */ }
    }
    /* Diagnóstico: abrir o site com ?diag mostra o estado do vídeo num canto da tela (para print no celular). */
    var caixaDiag = null, logDiag = [];
    function diag(msg) {
      if (!/[?&]diag/.test(location.search)) return;
      if (!caixaDiag) {
        caixaDiag = document.createElement('pre');
        caixaDiag.style.cssText = 'position:fixed;left:4px;top:70px;z-index:9999;max-width:70vw;margin:0;padding:6px;font:11px/1.3 monospace;color:#0f0;background:rgba(0,0,0,.75);pointer-events:none;white-space:pre-wrap';
        document.body.appendChild(caixaDiag);
        setInterval(function () { diag(''); }, 500);
      }
      if (msg) { logDiag.push(new Date().toTimeString().slice(3, 8) + ' ' + msg); logDiag = logDiag.slice(-8); }
      var v = vid;
      caixaDiag.textContent = (v ? 'rs ' + v.readyState + ' ns ' + v.networkState + ' t ' + v.currentTime.toFixed(2) +
        ' pausa ' + v.paused + ' seek ' + v.seeking + ' err ' + (v.error && v.error.code) + ' qd ' + atual +
        ' vids ' + caixa.querySelectorAll('video').length : '') + '\n' + logDiag.join('\n');
    }
    function posiciona(forca) {
      if (!vid || vid.readyState < 1 || tocando) return;
      var t = (Math.max(atual, 0) + 0.5) / (m.fps || 24);  // meio do quadro: cai sempre no quadro certo
      if (!vid.paused) vid.pause();
      if (forca === true || Math.abs(vid.currentTime - t) > 0.001) vid.currentTime = t;
    }
    function mostraVideo(i) {
      if (i === atual) return;
      atual = i;
      posiciona();
      hero.style.setProperty('--fundo', m.fundo[Math.min(i, m.fundo.length - 1)]);
      if (m.borda) hero.style.setProperty('--borda', m.borda[Math.min(i, m.borda.length - 1)]);
    }

    /* ---- modo canvas (quadros WebP) ---- */
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
    function carregaQuadros() {
      total = m.count;
      frames = new Array(total).fill(null);
      var nome = function (i) { return 'assets/hero/frame_' + String(i + 1).padStart(4, '0') + '.webp'; };
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

    if (temVideo) iniciaVideo();
    else if (m && m.count > 1) carregaQuadros();

    /* estado inicial */
    window.gsap.set(words, { opacity: 0.16 });
    window.gsap.set([logo, sub], { opacity: 0 });
    window.gsap.set(logo, { scale: 0.96 });
    if (wm) window.gsap.set(wm, { opacity: 0 });
    window.gsap.set(stage, { '--brasa': 0 });

    var tl = window.gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: hero, start: 'top top', end: 'bottom bottom', scrub: 0.6,
        onUpdate: function (self) {
          var i = Math.round(Math.min(self.progress / 0.85, 1) * (total - 1));
          if (!total) return;
          if (temVideo) mostraVideo(i); else if (i !== atual) desenha(i);
        }
      }
    });
    if (intro) tl.to(intro, { autoAlpha: 0, duration: 0.07 }, 0.05);              // título some quando o vídeo anda
    if (cta) tl.to(cta, { autoAlpha: 1, duration: 0.05 }, 0.92);                  // botões no último quadro
    tl.to(words, { opacity: 1, stagger: 0.035, duration: 0.05 }, 0)             // 0 .. ~0.65 (17 palavras)
      .to(stage, { '--brasa': 1, duration: 0.25 }, 0.45)
      .to(oracao, { opacity: 0, duration: 0.22 }, 0.72);                         // fixo, só esmaece devagar
    if (temVideo) {                                   // o vídeo termina em p=0.85; o texto do logo entra depois
      tl.to(wm, { opacity: 1, duration: 0.09 }, 0.86)
        .to(sub, { opacity: 1, duration: 0.05 }, 0.94);
    } else {
      tl.to(canvas, { opacity: 0.3, duration: 0.12 }, 0.82)
        .to(logo, { opacity: 1, scale: 1, duration: 0.12 }, 0.84)
        .to(sub, { opacity: 1, duration: 0.08 }, 0.92);
    }
    tl.to({}, { duration: 0.02 }, 0.98);                                          // fecha em 1.0

    window.addEventListener('resize', function () { if (!temVideo) desenha(atual < 0 ? 0 : atual); });
    window.ScrollTrigger.refresh();
  }
})();
