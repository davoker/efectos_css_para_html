/* =============================================================
   efectos_webgl · TEMAS
   Manifiesto compartido por todos los showcases WebGL.
   Al pulsar "Temática", cada showcase lista los efectos afines
   declarados aquí (misma temática = misma clave).

   ¿AÑADIR UN EFECTO NUEVO?
     1) crea su carpeta:  <categoria>/<id>/<id>.html
        con su index.html (showcase), <id>.zip y
        installation-instalacion-<id>.txt
     2) añade su objeto a la temática correspondiente (o crea
        una clave nueva). El showcase que lleve
        data-tema="<clave>" lo mostrará solo, sin tocar nada más.

   Las rutas se resuelven contra la raíz de ESTE archivo, así que
   valen igual dentro de subcarpetas y al abrir con doble clic.
   ============================================================= */
(function () {
  'use strict';

  var BASE = (document.currentScript && document.currentScript.src) || location.href;

  function ruta(carpeta, datos) {
    datos.showcase = new URL(carpeta + 'index.html', BASE).href;
    datos.efecto   = new URL(carpeta + datos.id + '.html', BASE).href;
    datos.zip      = new URL(carpeta + datos.id + '.zip', BASE).href;
    datos.doc      = new URL(carpeta + 'installation-instalacion-' + datos.id + '.txt', BASE).href;
    return datos;
  }

  window.TEMAS = {
    matrix: [
      ruta('Matrix/matrix/', {
        id: 'matrix',
        nombre: 'MATRIX',
        linea: 'Lluvia de código',
        desc: 'El texto es una ventana: la lluvia de glifos cae dentro de las letras, con parallax y una onda expansiva por clic.',
        preview: 'lluvia',
        datos: ['1 pasada', 'atlas 16×8', 'canvas 2D + GLSL']
      }),
      ruta('Matrix/matrix2/', {
        id: 'matrix2',
        nombre: 'MATRIX 2 · CINE',
        linea: 'Cine digital',
        desc: 'La versión cinematográfica: bloom multipasada, aberración cromática, tonemap ACES y borde nítido sobre fondo plano.',
        preview: 'lluvia',
        datos: ['4 pasadas', 'bloom + ACES', 'GLSL multipasada']
      })
    ],
    miscelanea: [
      ruta('miscelanea/mercurio/', {
        id: 'mercurio',
        nombre: 'MERCURIO',
        linea: 'Metal líquido',
        desc: 'El texto se funde en mercurio: ondulación constante, brillos especulares y onda expansiva al hacer clic.',
        preview: 'metal',
        datos: ['1 pasada', 'refracción', 'canvas 2D + GLSL']
      })
    ]
  };

  window.TEMAS_BASE = BASE;
})();
