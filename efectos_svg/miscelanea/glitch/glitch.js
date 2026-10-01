/* =============================================================
   GLITCH (SVG) · glitch.js — capa JS OPCIONAL
   -------------------------------------------------------------
   · Sin este JS el efecto funciona igual: glitch suave base,
     ráfaga y hover fuerte van solo con CSS+SVG.
   · Con él: mientras el texto está en hover/focus añade
     "cortes" aleatorios (parpadeos breves al texto normal)
     además de las ráfagas del propio filtro SVG.
   · Respeta prefers-reduced-motion: en ese modo NO hay
     cortes ni ráfagas (el texto queda con su estado suave).
   · ?glitch=1 en la URL fuerza el efecto en todos los
     ejemplos (para capturas/pruebas sin pasar el ratón).
   ============================================================= */
(function () {
    'use strict';

    var reduce = !!(window.matchMedia
        && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

    /* movimiento reducido: pausar las ondas SMIL del filtro */
    if (reduce) {
        var svgs = document.querySelectorAll('svg');
        for (var s = 0; s < svgs.length; s++) {
            if (svgs[s].pauseAnimations) svgs[s].pauseAnimations();
        }
    }

    function rand(a, b) { return a + Math.random() * (b - a); }

    /* --- cortes: texto con glitch ↔ texto normal --- */
    var activos = [];
    var temporizador = null;

    function tic() {
        temporizador = null;
        if (reduce || !activos.length) return;
        var cortar = Math.random() < 0.35;
        for (var i = 0; i < activos.length; i++) {
            activos[i].classList.toggle('sin-glitch', cortar);
        }
        temporizador = setTimeout(tic, cortar ? rand(40, 110) : rand(90, 260));
    }

    function activar(el) {
        if (activos.indexOf(el) < 0) activos.push(el);
        if (!temporizador) temporizador = setTimeout(tic, 60);
    }

    function desactivar(el) {
        var i = activos.indexOf(el);
        if (i >= 0) activos.splice(i, 1);
        el.classList.remove('sin-glitch');
    }

    var nodos = document.querySelectorAll('.ef-glitch');
    for (var n = 0; n < nodos.length; n++) {
        (function (el) {
            el.addEventListener('mouseenter', function () { activar(el); });
            el.addEventListener('mouseleave', function () { desactivar(el); });
            el.addEventListener('focus', function () { activar(el); });
            el.addEventListener('blur', function () { desactivar(el); });
        })(nodos[n]);
    }

    /* --- ráfaga periódica: cada 3-4 s el glitch salta a fuerte --- */
    if (!reduce && nodos.length) {
        (function () {
            function programar() {
                setTimeout(function () {
                    var i;
                    for (i = 0; i < nodos.length; i++) nodos[i].classList.add('rafaga');
                    setTimeout(function () {
                        for (i = 0; i < nodos.length; i++) nodos[i].classList.remove('rafaga');
                        programar();
                    }, 180 + Math.random() * 220);   /* ráfaga de 180-400 ms */
                }, 3000 + Math.random() * 1000);     /* cada 3-4 s */
            }
            programar();
        })();
    }

    /* --- modo demo por URL: ?glitch=1 --- */
    if (/[?&]glitch=1/.test(location.search)) {
        for (var k = 0; k < nodos.length; k++) {
            nodos[k].classList.add('forzado');
            activar(nodos[k]);
        }
    }
})();
