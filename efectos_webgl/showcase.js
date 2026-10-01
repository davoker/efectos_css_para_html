/* =============================================================
   efectos_webgl · SHOWCASE - comportamiento compartido
   La maquetación vive en showcase.css; aquí solo la lógica:

   · Cada página es el showcase de UN SOLO efecto: aquí solo
     vive su escena (iframe), su HUD y su cajón de instalación.
   · "Portada"  → enlaza con transicion.html#…: allí estalla la
                  escena de la MISMA temática del efecto y, tras
                  ~1,6 s (meta refresh), se llega a la portada
                  (el mismo camino que el botón de volver de
                  los showcases CSS).
   · "Instalar" → cajón lateral con los pasos y el snippet.
   · Capa ambiental en canvas 2D: retícula, barrido y
                  retículas-drift sobre el efecto (sutil).
   · Teclado: I instalar · Esc cierra.
   · Respeta prefers-reduced-motion (dibujo estático) y la
     visibilidad de la pestaña (detiene el bucle).

   Atajo de URL para verificar: index.html#instalar
   ============================================================= */
(function () {
  'use strict';

  var cuerpo = document.body;
  var reduce = !!(window.matchMedia
                  && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var acento = (window.getComputedStyle(cuerpo)
                .getPropertyValue('--acento-rgb') || '0,255,65').trim();
  var $ = function (s) { return document.querySelector(s); };

  var cajon = $('#cajon');
  var velo  = $('#velo');
  var cajonAbierto = false, ultimoFoco = null;

  /* ============================================================
     1) CAJÓN "INSTALAR"
     ============================================================ */
  function abrirCajon() {
    if (!cajon || cajonAbierto) return;
    cajonAbierto = true;
    ultimoFoco = document.activeElement;
    cajon.hidden = false;
    if (velo) { velo.hidden = false; requestAnimationFrame(function () { velo.classList.add('abierto'); }); }
    requestAnimationFrame(function () { cajon.classList.add('abierto'); });
    var cierra = cajon.querySelector('.cierra');
    if (cierra) cierra.focus();
    var btn = $('#btn-instalar');
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }

  function cerrarCajon() {
    if (!cajon || !cajonAbierto) return;
    cajonAbierto = false;
    cajon.classList.remove('abierto');
    if (velo) velo.classList.remove('abierto');
    setTimeout(function () {
      if (!cajonAbierto) cajon.hidden = true;
      if (velo && !cajonAbierto) velo.hidden = true;
    }, 360);
    var btn = $('#btn-instalar');
    if (btn) { btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
    else if (ultimoFoco) ultimoFoco.focus();
  }

  if ($('#btn-instalar')) {
    $('#btn-instalar').addEventListener('click', function () {
      cajonAbierto ? cerrarCajon() : abrirCajon();
    });
  }
  if ($('#cerrar-instalar')) $('#cerrar-instalar').addEventListener('click', cerrarCajon);
  if (velo) velo.addEventListener('click', cerrarCajon);

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA'
              || t.tagName === 'SELECT' || t.isContentEditable)) return;
    if (e.key === 'Escape') { cerrarCajon(); return; }
    if (e.key.toLowerCase() === 'i') { cajonAbierto ? cerrarCajon() : abrirCajon(); }
  });

  /* ============================================================
     2) CAPA AMBIENTAL (canvas 2D): retícula cacheada, barrido
        y3 retículas a la deriva con su coordenada
     ============================================================ */
  var ambiente = (function () {
    var cv = $('.ambiental');
    if (!cv) return null;
    var ctx = cv.getContext('2d');
    var dpr = 1, w = 0, h = 0, reticula = null;
    var deriva = [
      { x: .2,  y: .3,  tx: .7,  ty: .55, v: .00022 },
      { x: .78, y: .68, tx: .28, ty: .22, v: .00017 },
      { x: .55, y: .2,  tx: .42, ty: .78, v: .00013 }
    ];

    function medir() {
      dpr = Math.min(2, window.devicePixelRatio || 1);
      w = window.innerWidth; h = window.innerHeight;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      cv.style.width = w + 'px'; cv.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      /* retícula de puntos: se dibuja una vez por redimensionado */
      reticula = document.createElement('canvas');
      reticula.width = cv.width; reticula.height = cv.height;
      var r = reticula.getContext('2d');
      r.setTransform(dpr, 0, 0, dpr, 0, 0);
      r.fillStyle = 'rgba(' + acento + ',0.11)';
      var paso = 48;
      for (var x = paso / 2; x < w; x += paso) {
        for (var y = paso / 2; y < h; y += paso) r.fillRect(x, y, 1.5, 1.5);
      }
    }

    function marcar(p, x, y) {
      ctx.strokeStyle = 'rgba(' + acento + ',0.30)';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(x, y, 9, 0, 6.2832); ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x - 15, y); ctx.lineTo(x - 11, y);
      ctx.moveTo(x + 11, y); ctx.lineTo(x + 15, y);
      ctx.moveTo(x, y - 15); ctx.lineTo(x, y - 11);
      ctx.moveTo(x, y + 11); ctx.lineTo(x, y + 15);
      ctx.stroke();
      ctx.fillStyle = 'rgba(' + acento + ',0.45)';
      ctx.font = '9px ui-monospace, Consolas, monospace';
      ctx.fillText('x ' + p.x.toFixed(2) + ' / y ' + p.y.toFixed(2),
                   x + 20, y + 3);
    }

    function paso(dt, t) {
      ctx.clearRect(0, 0, w, h);
      if (reticula) ctx.drawImage(reticula, 0, 0, w, h);

      if (!reduce) {                          /* barrido de escaneo */
        var s = (t / 9000) % 1;
        var g = ctx.createLinearGradient(s * w - 90, 0, s * w + 90, 0);
        g.addColorStop(0, 'rgba(' + acento + ',0)');
        g.addColorStop(.5, 'rgba(' + acento + ',0.10)');
        g.addColorStop(1, 'rgba(' + acento + ',0)');
        ctx.fillStyle = g;
        ctx.fillRect(s * w - 90, 0, 180, h);
      }

      for (var i = 0; i < deriva.length; i++) {
        var p = deriva[i];
        if (!reduce) {
          if (Math.abs(p.x - p.tx) < .004 && Math.abs(p.y - p.ty) < .004) {
            p.tx = .12 + Math.random() * .76;
            p.ty = .14 + Math.random() * .7;
          }
          var k = Math.min(1, dt * p.v);
          p.x += (p.tx - p.x) * k;
          p.y += (p.ty - p.y) * k;
        }
        marcar(p, p.x * w, p.y * h);
      }
    }

    medir();
    window.addEventListener('resize', medir);
    return { paso: paso };
  })();

  /* ============================================================
     3) BÚCLE ÚNICO (se detiene al ocultar la pestaña)
     ============================================================ */
  var corriendo = false, ultimo = 0;

  function bucle(ts) {
    if (document.hidden) { corriendo = false; ultimo = 0; return; }
    var dt = ultimo ? Math.min(64, ts - ultimo) : 16;
    ultimo = ts;

    if (ambiente) ambiente.paso(dt, ts);
    requestAnimationFrame(bucle);
  }

  function arrancar() {
    if (reduce) {                      /* modo estático: un solo dibujo */
      if (ambiente) ambiente.paso(0, 0);
      return;
    }
    if (!corriendo && !document.hidden) {
      corriendo = true;
      requestAnimationFrame(bucle);
    }
  }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { corriendo = false; ultimo = 0; }
    else arrancar();
  });
  window.addEventListener('resize', function () {
    if (reduce) { if (ambiente) ambiente.paso(0, 0); }
  });

  /* ============================================================
     4) ARRANQUE (+ deep-link #instalar)
     ============================================================ */
  if (location.hash === '#instalar') abrirCajon();
  arrancar();
})();
