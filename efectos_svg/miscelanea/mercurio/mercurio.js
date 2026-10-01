/* =============================================================
   MERCURIO (SVG) · mercurio.js — capa JS OPCIONAL
   -------------------------------------------------------------
   · Sin este JS el efecto funciona igual: ondulación SMIL y
     brillo al pasar el ratón van solo con CSS+SVG.
   · Con él, al interactuar la onda crece SUAVE (tween del
     atributo scale del filtro compartido, 11 → 18 en 600 ms
     con ease-out): sin el salto instantáneo de cambiar de
     filtro en frío.
   · Respeta prefers-reduced-motion: en ese modo no hay tween
     y se pausan las ondas SMIL de los filtros.
   ============================================================= */
(function () {
    'use strict';

    var reduce = !!(window.matchMedia
        && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

    /* movimiento reducido: pausar las ondas SMIL */
    if (reduce) {
        var svgs = document.querySelectorAll('svg');
        for (var s = 0; s < svgs.length; s++) {
            if (svgs[s].pauseAnimations) svgs[s].pauseAnimations();
        }
    }

    /* --- la onda crece SUAVE al interactuar (sin salto)
           tween del atributo scale del filtro compartido 11 → 18 --- */
    var filtroLiq = document.getElementById('ef-mercurio');
    var dispLiq = filtroLiq && filtroLiq.querySelector('feDisplacementMap');
    if (dispLiq && !reduce) {
        var liquidos = document.querySelectorAll('.ef-mercurio');
        var escalaTween = null;
        function crecerOnda(haciaArriba) {
            if (escalaTween) clearInterval(escalaTween);
            var desde = parseFloat(dispLiq.getAttribute('scale'));
            if (isNaN(desde)) desde = 11;
            var hasta = haciaArriba ? 18 : 11;
            if (Math.abs(desde - hasta) < 0.01) {
                dispLiq.setAttribute('scale', hasta);
                return;
            }
            var t0 = performance.now();
            escalaTween = setInterval(function () {
                /* k acotado a [0,1]: ease-out de 600 ms, sin salto */
                var k = Math.max(0, Math.min(1, (performance.now() - t0) / 600));
                var e = 1 - Math.pow(1 - k, 3);
                dispLiq.setAttribute('scale', (desde + (hasta - desde) * e).toFixed(2));
                if (k >= 1) {
                    clearInterval(escalaTween);
                    escalaTween = null;
                }
            }, 16);
        }
        for (var q = 0; q < liquidos.length; q++) {
            (function (el) {
                el.addEventListener('mouseenter', function () { crecerOnda(true); });
                el.addEventListener('mouseleave', function () { crecerOnda(false); });
                el.addEventListener('focus', function () { crecerOnda(true); });
                el.addEventListener('blur', function () { crecerOnda(false); });
            })(liquidos[q]);
        }
    }
})();
