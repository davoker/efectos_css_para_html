# -*- coding: utf-8 -*-
"""
_gen_webgl.py · generador de los efectos WebGL nuevos
-----------------------------------------------------
Añade 18 efectos a efectos_webgl/Matrix y 19 a efectos_webgl/miscelanea
(20 + 20 con los ya existentes). Cada efecto genera:

    efectos_webgl/<cat>/<nombre>/<nombre>.html          el efecto
    efectos_webgl/<cat>/<nombre>/index.html             showcase
    efectos_webgl/<cat>/<nombre>/installation-...txt    instalación ES+EN
    efectos_webgl/<cat>/<nombre>/<nombre>.zip           zip (html+txt+LICENSE)

y parchea:
    transicion.html   → escena propia del efecto (#nombre)
    transicion.css    → .tema-<nombre> + partes + keyframes
    index.html        → tarjetas, lista lateral, contadores, .wg-<nombre>
    i18n.js           → claves ES→EN de todo lo nuevo

Uso:  py -3 _gen_webgl.py   (idempotente: lo ya generado se omite)
"""
import io
import os
import re
import json
import zipfile
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_webgl_data import EFFECTS, FIXED_I18N

BASE = os.path.dirname(os.path.abspath(__file__))
LF = '\n'

ENGINE_TPL = rd = None  # se cargan abajo


def rd(path, raw=False):
    """Lee en UTF-8. raw=True conserva los CRLF tal cual (index.html)."""
    with io.open(path, encoding='utf-8', newline=('', None)[0 if raw else 1]) as f:
        return f.read()


def wr(path, text, crlf=False):
    full = os.path.join(BASE, path) if not os.path.isabs(path) else path
    d = os.path.dirname(full)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    nl = '\r\n' if crlf else '\n'
    if crlf:
        text = text.replace('\r\n', '\n').replace('\n', '\r\n')
    with io.open(full, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    return full


# =============================================================================
#  SHADER · preludio compartido + prólogo/epílogo de main()
#  Todas las Variables Uniform son fijas (motor = el de MERCURIO); el cuerpo
#  de cada efecto solo debe dejar `vec3 col` definido.
# =============================================================================
GLSL_PRELUDE = r"""
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
uniform vec2  uRes;
uniform float uTime;
uniform sampler2D uText;
uniform sampler2D uBlur;
uniform vec2  uPlane;
uniform vec2  uTexel;
uniform vec2  uMouse;
uniform vec2  uClickPos;
uniform float uAmp;
uniform float uClickT;

float hash21(vec2 p){
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}
float vnoise(vec2 p){
  vec2 i = floor(p), f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  float a = hash21(i);
  float b = hash21(i + vec2(1.0, 0.0));
  float c = hash21(i + vec2(0.0, 1.0));
  float d = hash21(i + vec2(1.0, 1.0));
  return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
float fbm(vec2 p){
  float v = 0.0, a = 0.5;
  for (int i = 0; i < 5; i++){
    v += a * vnoise(p);
    p = p * 2.03 + vec2(1.7, 9.2);
    a *= 0.5;
  }
  return v;
}
float fbm3(vec2 p){
  float v = 0.0, a = 0.60;
  for (int i = 0; i < 3; i++){
    v += a * vnoise(p);
    p = p * 2.03 + vec2(1.7, 9.2);
    a *= 0.45;
  }
  return v;
}
float inside(vec2 uv){
  return step(0.0, uv.x) * step(uv.x, 1.0) * step(0.0, uv.y) * step(uv.y, 1.0);
}
float maskAt(vec2 uv){
  return texture2D(uText, clamp(uv, 0.0, 1.0)).a * inside(uv);
}
float blurAt(vec2 uv){
  return texture2D(uBlur, clamp(uv, 0.0, 1.0)).a * inside(uv);
}
vec3 normalAt(vec2 uv){
  float hL = texture2D(uBlur, clamp(uv - vec2(uTexel.x, 0.0), 0.0, 1.0)).a;
  float hR = texture2D(uBlur, clamp(uv + vec2(uTexel.x, 0.0), 0.0, 1.0)).a;
  float hD = texture2D(uBlur, clamp(uv - vec2(0.0, uTexel.y), 0.0, 1.0)).a;
  float hU = texture2D(uBlur, clamp(uv + vec2(0.0, uTexel.y), 0.0, 1.0)).a;
  return normalize(vec3((hL - hR) * 2.6, (hD - hU) * 2.6, 0.35));
}
float ringAt(vec2 p){
  vec2 dc = p - uClickPos;
  float cd = length(dc);
  float age = max(uTime - uClickT, 0.0);
  return exp(-pow((cd - age * 0.85) * 7.0, 2.0)) * exp(-age * 1.8);
}
float waveAt(vec2 p){
  float md = length(p - uMouse);
  return sin(md * 36.0 - uTime * 7.0) * exp(-md * 6.0) * uAmp;
}
"""

GLSL_PROLOGUE = r"""
void main(){
  float t   = uTime;
  vec2  p   = (gl_FragCoord.xy - 0.5 * uRes) / uRes.y;
  vec2  tuv = 0.5 + p / (2.0 * uPlane);
  float mask = maskAt(tuv);
  float hb   = blurAt(tuv);
  vec3  N    = normalAt(tuv);
  float wave = waveAt(p);
  float ring = ringAt(p);
  vec2  dm   = p - uMouse;
  float md   = length(dm);
  float mBoost = exp(-9.0 * dot(dm, dm)) * uAmp;
"""

GLSL_EPILOGUE = r"""
  gl_FragColor = vec4(col, 1.0);
}
"""




def full_shader(e):
    return GLSL_PRELUDE + GLSL_PROLOGUE + e['shader'] + GLSL_EPILOGUE


# =============================================================================
#  EFECTO · se genera a partir de mercurio.html (mismo motor, distinto FS)
# =============================================================================
def js_fs_block(glsl):
    """Convierte el GLSL en el bloque `var FS = [ ... ].join('\\n');` de JS."""
    out = []
    for line in glsl.split('\n'):
        s = line.replace('\\', '\\\\').replace("'", "\\'")
        out.append("'" + s + "'")
    return 'var FS = [\n' + ',\n'.join(out) + "\n].join('\\n');"


def build_effect(e):
    src = rd(os.path.join(BASE, 'efectos_webgl', 'miscelanea', 'mercurio',
                          'mercurio.html'))
    # 1) titulo de la pagina
    src = src.replace(
        '<title>Texto líquido metálico — efecto WebGL (MERCURIO)</title>',
        '<title>' + e['titulo_corto'] + ' — efecto WebGL (' + e['word'] + ')</title>')
    # 2) paleta de la caja
    src = src.replace('background:#05060a', 'background:' + e['bg'])
    src = src.replace('color:#9fb4d0', 'color:' + e['fg'])
    src = src.replace('border:1px solid rgba(140,180,255,.28)',
                      'border:1px solid rgba(' + e['acento'] + ',.30)')
    src = src.replace('border-color:rgba(160,220,255,.6); box-shadow:0 0 0 3px rgba(80,160,255,.15)',
                      'border-color:rgba(' + e['acento'] + ',.62); box-shadow:0 0 0 3px rgba(' + e['acento'] + ',.16)')
    # 3) palabra por defecto + pista
    src = src.replace('value="MERCURIO"', 'value="' + e['word'] + '"')
    src = src.replace("if (!str) str = 'MERCURIO';",
                      "if (!str) str = '" + e['word'] + "';")
    i = src.index('<p class="hint">')
    j = src.index('</p>', i)
    src = src[:i + len('<p class="hint">')] + e['hint'] + src[j:]
    # 4) fragment shader nuevo
    a = src.index('var FS = [')
    b = src.index("].join('\\n');", a) + len("].join('\\n');")
    src = src[:a] + js_fs_block(full_shader(e)) + src[b:]
    return src


# =============================================================================
#  SHOWCASE · basado en el de MERCURIO (HUD de laboratorio, chrome flotante)
# =============================================================================
def build_showcase(e):
    src = rd(os.path.join(BASE, 'efectos_webgl', 'miscelanea', 'mercurio',
                          'index.html'))
    N = e['nombre']
    up = e['word']
    # comentario de cabecera
    src = src.replace('SHOWCASE WEBGL · MERCURIO',
                      'SHOWCASE WEBGL · ' + up)
    src = src.replace('ESTE ARCHIVO no es el efecto: el efecto es mercurio.html',
                      'ESTE ARCHIVO no es el efecto: el efecto es ' + N + '.html')
    # head/body
    src = src.replace('<title>MERCURIO · Showcase WebGL</title>',
                      '<title>' + up + ' · Showcase WebGL</title>')
    src = src.replace('data-tema="miscelanea" data-efecto="mercurio"',
                      'data-tema="' + e['cat'] + '" data-efecto="' + N + '"')
    src = src.replace('style="--acento-rgb: 170, 214, 255"',
                      'style="--acento-rgb: ' + e['acento'] + '"')
    # iframe
    src = src.replace('src="mercurio.html?demo=1"',
                      'src="' + N + '.html?demo=1"')
    src = src.replace('title="Efecto MERCURIO en marcha"',
                      'title="Efecto ' + up + ' en marcha"')
    # placa
    src = src.replace('efectos_webgl / mercurio · temática <b>miscelanea</b>',
                      'efectos_webgl / ' + N + ' · temática <b>' + e['cat'] + '</b>')
    src = src.replace('<h1 class="titulo">MERCURIO</h1>',
                      '<h1 class="titulo">' + up + '</h1>')
    src = src.replace('<p class="descr">El texto se funde en mercurio: ondas del ratón y onda expansiva por clic.</p>',
                      '<p class="descr">' + e['descr'] + '</p>')
    # navegacion
    src = src.replace('href="../../../transicion.html#mercurio"',
                      'href="../../../transicion.html#' + e['escena_id'] + '"')
    src = src.replace('href="mercurio.zip"', 'href="' + N + '.zip"')
    # pie: datos tecnicos
    a = src.index('<p class="datos">')
    b = src.index('</p>', a) + len('</p>')
    datos = '<p class="datos">' + ''.join(
        '\n            <span>' + d + '</span>' for d in e['datos']) + '\n        </p>'
    src = src[:a] + datos + src[b:]
    # cajon instalar
    src = src.replace('<code>mercurio.html</code>', '<code>' + N + '.html</code>')
    src = src.replace('ruta/mercurio.html?demo=1', 'ruta/' + N + '.html?demo=1')
    src = src.replace('title="Efecto MERCURIO"', 'title="Efecto ' + up + '"')
    src = src.replace('installation-instalacion-mercurio.txt',
                      'installation-instalacion-' + N + '.txt')
    src = src.replace('href="mercurio.zip"', 'href="' + N + '.zip"')
    # paso 3: texto propio del efecto
    a = src.index('<p><b>Paso 3 — personaliza.</b>')
    b = src.index('</p>', a) + len('</p>')
    src = src[:a] + '<p><b>Paso 3 — personaliza.</b> <code>?t=TU+PALABRA</code> fija el\n            ' + e['paso3'] + '</p>' + src[b:]
    return src


# =============================================================================
#  INSTALACION · ES + EN, mismo formato que installation-instalacion-mercurio.txt
# =============================================================================
INSTALL_TPL = """================================================================
EFECTO {UP} - CÓMO APLICARLO A CUALQUIER ARCHIVO HTML
================================================================

PASO 1 - COPIA EL ARCHIVO DEL EFECTO
------------------------------------
"{n}.html" es autocontenido: CSS, JavaScript y shader GLSL
van dentro; no hay imágenes ni ficheros externos.

    cópialo a tu proyecto, por ejemplo:
        tu-pagina/efectos/{n}.html


PASO 2 - AÑÁDELO A TU PÁGINA
----------------------------
a) Como página completa, enlazándolo:

       <a href="efectos/{n}.html">ver efecto</a>

b) Empotrado con un iframe (recomendado dentro de tu diseño):

       <iframe src="efectos/{n}.html?demo=1"
               title="Efecto {UP}"
               style="display:block;width:100%;height:520px;
                      border:0;background:{bg}"></iframe>

c) Como fondo de una sección: contenedor con position:relative,
   el iframe con position:absolute; inset:0 y tu texto encima
   (z-index mayor).


PARÁMETROS EN LA URL
---------------------
    ?demo=1      la luz recorre el efecto sola (se ve sin mover
                 el ratón)
    ?t={UP}      texto inicial; "+" = espacio: ?t=TEXTO LIQUIDO

Dentro del efecto también hay una caja inferior para escribir
otra palabra en caliente.


QUÉ HACE
--------
{que_hace}


TÉCNICA
-------
· Canvas 2D: el texto se pinta dos veces (máscara nítida +
  versión desenfocada) → mapa de altura.
· Del mapa de altura se deriva la NORMAL (gradiente de las 4
  muestras) y el shader la combina con su propia lógica:
{tecnica}
· Ondas: una onda suave que sigue al ratón + un anillo del clic
  (gaussiana viajera que se amortigua con la edad) desplazan la
  UV de muestreo y alimentan la interacción.


AJUSTES FÁCILES
---------------
· Texto por defecto: value="{UP}" en el <input> o ?t=...
· Fuerza del ratón: la uniforme uAmp (0 = efecto en reposo,
  1 = manda el ratón).
· Onda del clic: la gaussiana "exp(-pow((cd - age * 0.85) * 7.0,
  2.0))" → 7.0 es lo estrecha que es y 1.8 lo rápido que se
  apaga.
{ajustes}
REQUISITOS
----------
· Navegador con WebGL 1 (cualquier navegador actual).
· NO necesita servidor local: el shader va dentro del HTML y no
  se carga con fetch. Si al abrir con doble clic (file://) tu
  navegador bloqueara algo, sirve la carpeta en local:

      py -3 -m http.server 8000

  y abre http://127.0.0.1:8000/{n}.html
· Si en tu proyecto separas el shader a un fichero .glsl, AHÍ SÍ
  necesitarías servidor local (fetch de archivos).


ARCHIVOS
--------
    {n}.html                   el efecto (autocontenido)
    index.html                 showcase (solo presentación)
    installation-instalacion-{n}.txt  este documento
    {n}.zip                    efecto + este documento
"""

INSTALL_EN = """
================================================================
ENGLISH VERSION
================================================================

================================================================
{UP} EFFECT - HOW TO APPLY IT TO ANY HTML FILE
================================================================

STEP 1 - COPY THE EFFECT FILE
-----------------------------
"{n}.html" is self-contained: CSS, JavaScript and GLSL shader
go inside; there are no images or external files.

    copy it to your project, for example:
        your-page/effects/{n}.html


STEP 2 - ADD IT TO YOUR PAGE
----------------------------
a) As a full page, linking to it:

       <a href="efectos/{n}.html">view effect</a>

b) Embedded with an iframe (recommended within your design):

       <iframe src="efectos/{n}.html?demo=1"
               title="Effect {UP}"
               style="display:block;width:100%;height:520px;
                      border:0;background:{bg}"></iframe>

c) As a section background: container with position:relative,
   the iframe with position:absolute; inset:0 and your text on top
   (higher z-index).


URL PARAMETERS
--------------
    ?demo=1      the light crosses the effect by itself (you can
                 watch without moving the mouse)
    ?t={UP}      initial text; "+" = space: ?t=LIQUID TEXT

There is also a box at the bottom to type another word on the fly.


WHAT IT DOES
------------
{que_hace_en}


TECHNIQUE
---------
· Canvas 2D: the text is painted twice (sharp mask +
  blurred version) -> height map.
· From the height map comes the NORMAL (the 4-sample gradient)
  and the shader combines it with its own logic:
{tecnica_en}
· Waves: a soft wave that follows the mouse + a click ring
  (a traveling Gaussian that decays with age) shift the
  sampling UV and drive the interaction.


EASY TWEAKS
-----------
· Default text: value="{UP}" in the <input> or ?t=...
· Mouse strength: the uAmp uniform (0 = effect at rest,
  1 = the mouse takes over).
· Click wave: the Gaussian "exp(-pow((cd - age * 0.85) * 7.0,
  2.0))" -> 7.0 is how narrow it is and 1.8 how fast it fades.
{ajustes_en}
REQUIREMENTS
------------
· A browser with WebGL 1 (any current browser).
· NO local server needed: the shader is inside the HTML and not
  loaded with fetch. If on double-click open (file://) your
  browser blocks something, serve the folder locally:

      py -3 -m http.server 8000

  and open http://127.0.0.1:8000/{n}.html
· If your project splits the shader into a .glsl file, THEN YES
  you'd need a local server (file fetch).


FILES
-----
    {n}.html                   the effect (self-contained)
    index.html                 showcase (presentation only)
    installation-instalacion-{n}.txt  this document
    {n}.zip                    effect + this document
"""




def build_install(e):
    kw = dict(n=e['nombre'], UP=e['word'], bg=e['bg'],
              que_hace=e['que_hace'], tecnica=e['tecnica'],
              ajustes=e['ajustes'], que_hace_en=e['que_hace_en'],
              tecnica_en=e['tecnica_en'], ajustes_en=e['ajustes_en'])
    return INSTALL_TPL.format(**kw) + INSTALL_EN.format(**kw)


# =============================================================================
#  ESCENAS DE TRANSICION · 12 arquetipos parametrizados por color y cuenta
#  Devuelven (hijos_html, css) con clases siempre prefijadas por el nombre
#  completo del efecto → cero colisiones con las 258 escenas existentes.
# =============================================================================
def _ring(p, c1, n=3):
    kids, css = [], []
    for i in range(1, n + 1):
        kids.append('<div class="%s-aro a%d"></div>' % (p, i))
    css.append('.%(p)s-aro {\n    position: absolute; left: 50%%; top: 50%%;\n'
               '    width: 30vmin; height: 30vmin; margin: -15vmin 0 0 -15vmin;\n'
               '    border: .9vmin solid %(c)s; border-radius: 50%%; opacity: 0;\n'
               '    animation: %(p)s-aro 1.6s ease-out both;\n}' % dict(p=p, c=c1))
    for i in range(2, n + 1):
        css.append('.%s-aro.a%d { animation-delay: %.2fs; }' % (p, i, (i - 1) * .2))
    css.append('@keyframes %s-aro {\n    0%%   { opacity: 0; transform: scale(.12); }\n'
               '    14%%  { opacity: 1; }\n'
               '    100%% { opacity: 0; transform: scale(2.7); }\n}' % p)
    return kids, '\n'.join(css)


def _barrido(p, c1):
    kids = ['<div class="' + p + '-barra"></div>',
            '<div class="' + p + '-barra-b"></div>']
    css = """.%(p)s-barra {
    position: absolute; left: -34%; top: 44%;
    width: 30%; height: 10%;
    background: linear-gradient(90deg, transparent, %(c)s, #ffffff, %(c)s, transparent);
    opacity: 0; filter: blur(.5vmin);
    animation: %(p)s-barra 1.55s cubic-bezier(.3,0,.2,1) both;
}
.%(p)s-barra-b {
    position: absolute; left: -34%; top: 62%;
    width: 22%; height: 5%;
    background: linear-gradient(90deg, transparent, %(c)s, transparent);
    opacity: 0; filter: blur(.4vmin);
    animation: %(p)s-barra 1.55s cubic-bezier(.3,0,.2,1) .28s both;
}
@keyframes %(p)s-barra {
    0%   { opacity: 0; transform: translateX(0); }
    12%  { opacity: 1; }
    100% { opacity: 0; transform: translateX(470%); }
}"""
    css = css.replace('%(p)s', p).replace('%(c)s', c1)
    return kids, css


def _estelas(p, c1, n=5, ang=25):
    kids = ['<div class="' + p + '-est%d"></div>' % i for i in range(1, n + 1)]
    css = []
    base = (".%(p)s-est{position:absolute;left:50%;top:50%;width:120vmin;height:.7vmin;"
            "margin:-.35vmin 0 0 -60vmin;background:linear-gradient(90deg,rgba(0,0,0,0),"
            "%(c)s,rgba(0,0,0,0));opacity:0;animation:%(p)s-est 1.5s ease-in both;}")
    css.append(base.replace('%(p)s', p).replace('%(c)s', c1))
    for i in range(1, n + 1):
        rot = ang + (i - 1) * (180.0 / max(n, 2)) / 2
        css.append('.%s-est%d { transform: rotate(%.0fdeg); animation-delay: %.2fs; }'
                   % (p, i, rot, (i - 1) * .12))
    kf = ('@keyframes %(p)s-est {\n    0%   { opacity: 0; transform-origin: 0 50%;'
          ' }\n    18%  { opacity: 1; }\n    100% { opacity: 0; }\n}')
    css.append(kf.replace('%(p)s', p))
    return kids, '\n'.join(css)


def _chispas(p, c1, n=10, up=True):
    kids = ['<div class="' + p + '-chi%d"></div>' % i for i in range(1, n + 1)]
    css = []
    base = ("%(p)s-chiPLACE{position:absolute;width:1.6vmin;height:1.6vmin;"
            "border-radius:50%%;background:%(c)s;box-shadow:0 0 2vmin %(c)s;opacity:0;"
            "animation:%(p)s-chiPLACE 1.6s ease-out both;}")
    base = base.replace('%(p)s-chiPLACE', '.' + p + '-chi')
    base = base.replace('%(p)s', p).replace('%(c)s', c1)
    css.append(base)
    for i in range(1, n + 1):
        x = 6 + (i * 89) % 88
        d = (i % 5) * .13
        css.append('.%s-chi%d { left: %d%%; bottom: -3%%; animation-delay: %.2fs; }'
                   % (p, i, x, d))
    fin = ('@keyframes %(p)s-chi {\n    0%   { opacity: 0; transform: translateY(0) '
           'scale(.4); }\n    15%  { opacity: 1; }\n'
           '    100% { opacity: 0; transform: translateY(-%(v)s) scale(1); }\n}')
    fin = fin.replace('%(p)s', p).replace('%(v)s', '-58vmin' if up else '58vmin')
    css.append(fin)
    return kids, '\n'.join(css)


def _halo(p, c1):
    kids = ['<div class="' + p + '-halo"></div>', '<div class="' + p + '-halo2"></div>']
    tpl = """.%(p)s-halo {
    position: absolute; left: 50%; top: 50%;
    width: 44vmin; height: 44vmin; margin: -22vmin 0 0 -22vmin;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,.9) 0%%, %(c)s 38%%, rgba(0,0,0,0) 70%%);
    opacity: 0; animation: %(p)s-halo 1.6s ease-in-out both;
}
.%(p)s-halo2 {
    position: absolute; left: 50%; top: 50%;
    width: 70vmin; height: 70vmin; margin: -35vmin 0 0 -35vmin;
    border-radius: 50%; border: .5vmin solid %(c)s;
    opacity: 0; animation: %(p)s-halo2 1.6s ease-in-out .18s both;
}
@keyframes %(p)s-halo {
    0%   { opacity: 0; transform: scale(.2); }
    30%  { opacity: 1; transform: scale(1); }
    100% { opacity: 0; transform: scale(1.35); }
}
@keyframes %(p)s-halo2 {
    0%   { opacity: 0; transform: scale(.5); }
    34%  { opacity: .8; transform: scale(1); }
    100% { opacity: 0; transform: scale(1.6); }
}"""
    css = tpl.replace('%(p)s', p).replace('%(c)s', c1)
    return kids, css


def _malla(p, c1):
    kids = ['<div class="' + p + '-malla"></div>', '<div class="' + p + '-barrido"></div>']
    tpl = """.%(p)s-malla {
    position: absolute; inset: -10%;
    background:
        repeating-linear-gradient(0deg, %(c)s22 0 1px, rgba(0,0,0,0) 1px 7vmin),
        repeating-linear-gradient(90deg, %(c)s22 0 1px, rgba(0,0,0,0) 1px 7vmin);
    opacity: 0; animation: %(p)s-malla 1.6s ease-out both;
}
.%(p)s-barrido {
    position: absolute; left: 0; top: -10%; width: 100%; height: 16vmin;
    background: linear-gradient(180deg, rgba(0,0,0,0), %(c)s55, rgba(0,0,0,0));
    opacity: 0; animation: %(p)s-barrido 1.6s cubic-bezier(.4,0,.2,1) both;
}
@keyframes %(p)s-malla {
    0%   { opacity: 0; transform: scale(1.25); }
    22%  { opacity: 1; transform: scale(1); }
    100% { opacity: 0; transform: scale(1); }
}
@keyframes %(p)s-barrido {
    0%   { opacity: 0; transform: translateY(0); }
    16%  { opacity: 1; }
    100% { opacity: 0; transform: translateY(130vmin); }
}"""
    css = tpl.replace('%(p)s', p).replace('%(c)s', c1)
    return kids, css


def _rayos(p, c1):
    kids = ['<div class="' + p + '-rayos"></div>', '<div class="' + p + '-nucleo"></div>']
    tpl = """.%(p)s-rayos {
    position: absolute; left: 50%; top: 50%;
    width: 150vmin; height: 150vmin; margin: -75vmin 0 0 -75vmin;
    background: repeating-conic-gradient(from 0deg,
                %(c)s 0 5deg, rgba(0,0,0,0) 5deg 26deg);
    opacity: 0;
    animation: %(p)s-rayos 1.7s ease-out both;
}
.%(p)s-nucleo {
    position: absolute; left: 50%; top: 50%;
    width: 26vmin; height: 26vmin; margin: -13vmin 0 0 -13vmin;
    border-radius: 50%;
    background: radial-gradient(circle, #ffffff 0%%, %(c)s 42%%, rgba(0,0,0,0) 72%%);
    opacity: 0;
    animation: %(p)s-nucleo 1.7s ease-out both;
}
@keyframes %(p)s-rayos {
    0%   { opacity: 0; transform: rotate(0deg) scale(.15); }
    16%  { opacity: .9; }
    100% { opacity: 0; transform: rotate(78deg) scale(1.35); }
}
@keyframes %(p)s-nucleo {
    0%   { opacity: 0; transform: scale(.1); }
    14%  { opacity: 1; }
    100% { opacity: 0; transform: scale(1.9); }
}"""
    css = tpl.replace('%(p)s', p).replace('%(c)s', c1)
    return kids, css


def build_scene(e):
    p = e['nombre']
    spec = e['escena']
    kind = spec[0]
    c1 = spec[1]
    par = spec[2] if len(spec) > 2 else {}
    kids = []
    css = []
    # fondo propio de la escena + destello teñido con el color del efecto
    css.append('.tema-%s {\n    background: radial-gradient(ellipse at 50%% 55%%,\n'
               '                %s 0%%, rgba(3,6,10,.6) 55%%, #02040a 100%%);\n}'
               % (p, par.get('bg', c1 + '33')))
    css.append('.tema-%s::after {\n    background: radial-gradient(circle at 50%% 55%%,\n'
               '                rgba(255,255,255,.55) 0%%, %s59 30%%,\n'
               '                %s00 72%%);\n}' % (p, c1, c1))
    fn = {'ring': _ring, 'barrido': _barrido, 'rayos': _rayos,
          'estelas': _estelas, 'chispas': _chispas, 'halo': _halo,
          'malla': _malla}[kind]
    # claves de la escena que no son argumentos del arquetipo
    palabra = par.pop('palabra', None)
    bg = par.pop('bg', None)
    k, c = fn(p, c1, **par)
    kids.extend(k)
    css.append(c)
    if palabra:
        kids.insert(0, '<div class="%s-pal">%s</div>' % (p, e['word']))
        css.append(".%(p)s-pal {\n    position: absolute; left: 50%%; top: 50%%;\n"
                   "    transform: translate(-50%%, -50%%);\n"
                   "    font-size: 13vmin; font-weight: bold; letter-spacing: .08em;\n"
                   "    color: #ffffff; text-shadow: 0 0 3vmin %(c)s, 0 0 8vmin %(c)s;\n"
                   "    opacity: 0; animation: %(p)s-pal 1.6s ease-out both;\n}\n"
                   "@keyframes %(p)s-pal {\n"
                   "    0%%   { opacity: 0; transform: translate(-50%%,-50%%) scale(.55); }\n"
                   "    25%%  { opacity: 1; transform: translate(-50%%,-50%%) scale(1); }\n"
                   "    100%% { opacity: 0; transform: translate(-50%%,-50%%) scale(1.2); }\n}"
                   % dict(p=p, c=c1))
    html = '<div class="escena tema-%s" id="%s">\n%s\n</div>\n' % (
        p, p, '\n'.join('        ' + k2 for k2 in kids))
    return html, '\n'.join(css)


MARKER_SETA = '<!-- ===== ESCENA POR DEFECTO (sin fragmento): la seta ===== -->'


def patch_transicion(effs):
    """Inserta las escenas nuevas en transicion.html y transicion.css (LF)."""
    html_path = os.path.join(BASE, 'transicion.html')
    css_path = os.path.join(BASE, 'transicion.css')
    h = rd(html_path)
    c = rd(css_path)
    nums = [int(m) for m in re.findall(r'/\* =+ (\d+)\.', c)]
    num = max(nums) if nums else 0
    n_html, n_css = 0, 0
    add_html, add_css = [], []
    for e in effs:
        if ('id="%s"' % e['nombre']) in h:
            continue
        sc_html, sc_css = build_scene(e)
        num += 1
        head = '/* ============ %d. %s — %s ============ */\n' % (
            num, e['word'], e['sub'])
        add_html.append(sc_html)
        add_css.append(head + sc_css + '\n')
        n_html += 1
    if add_html:
        assert MARKER_SETA in h, 'marcador de escena por defecto no encontrado'
        h = h.replace(MARKER_SETA, ''.join(add_html) + '\n' + MARKER_SETA, 1)
        wr(html_path, h, crlf=False)
    if add_css:
        if not c.endswith('\n'):
            c += '\n'
        c += '\n' + ''.join(add_css)
        wr(css_path, c, crlf=False)
    n_css = len(add_css)
    return n_html, n_css


# =============================================================================
#  PORTADA · index.html (CRLF): lista lateral, contadores, tarjetas, .wg-*
# =============================================================================
CARD_TPL = """
                <!-- ============ W{n}. {WORD} ============ -->
                <article class="tarjeta-webgl" data-webgl="{cat}">
                    <div class="wg-muestra wg-{nombre}">
                        <iframe loading="lazy"
                                title="Vista previa del efecto {TITULO}"
                                src="efectos_webgl/{folder}/{nombre}/{nombre}.html?demo=1"></iframe>
                    </div>
                    <h3>{EMOJI} {TITULO} <small>{sub}</small></h3>
                    <a class="btn" href="efectos_webgl/{folder}/{nombre}/index.html">Showcase completo</a>
                    <a class="btn btn-descarga" href="efectos_webgl/{folder}/{nombre}/{nombre}.zip" download>Descargar efecto (.zip)</a>
                </article>
"""

LI_TPL = ('                <li><a href="efectos_webgl/{folder}/{nombre}/index.html">'
          '>{EMOJI} {TITULO}</a></li>\n')

WG_TPL = """
        /* preview de {WORD}: {sub} */
        .wg-{nombre} {{
            background: {preview};
        }}
"""


def patch_index(effs):
    path = os.path.join(BASE, 'index.html')
    t = rd(path, raw=True)          # conserva los \r\n
    nl = '\r\n' if '\r\n' in t[:4000] else '\n'

    def n(s):                        # normaliza inserciones al EOL del fichero
        return s.replace('\r\n', '\n').replace('\n', nl)

    added_li = added_card = added_wg = 0

    # --- 1) listas laterales + grupo-n ---
    for cat, folder, grupo in (('matrix', 'Matrix', 'g-webgl-matrix'),
                               ('miscelanea', 'miscelanea', 'g-webgl-miscelanea')):
        i = t.index('id="%s"' % grupo)
        j = t.index('</ol>', i)
        lis = ''
        for e in [x for x in effs if x['cat'] == cat]:
            if 'efectos_webgl/%s/%s/index.html' % (folder, e['nombre']) in t:
                continue
            lis += n(LI_TPL.format(folder=folder, nombre=e['nombre'],
                                   EMOJI=e['emoji'], TITULO=e['titulo']))
            added_li += 1
        if lis:
            t = t[:j] + lis + t[j:]
        # contador del grupo (2 -> 20 / 1 -> 20)
        i = t.index('id="%s"' % grupo)
        k = t.index('</summary>', i)
        bloque = t[i:k]
        nuevo = str(sum(1 for x in effs if x['cat'] == cat)
                    + (2 if cat == 'matrix' else 1))
        bloque = re.sub(r'(<span class="grupo-n">)\d+(</span>)',
                        r'\g<1>' + nuevo + r'\g<2>', bloque, count=1)
        t = t[:i] + bloque + t[k:]

    # --- 2) contadores de seccion ---
    total = 3 + len(effs)
    t = t.replace('>3 disponibles<', '>%d disponibles<' % total, 1)
    t = t.replace('3 en tiempo real', '%d en tiempo real' % total, 1)

    # --- 3) tarjetas: al final de la galeria WebGL, por categoria ---
    for cat, folder in (('matrix', 'Matrix'), ('miscelanea', 'miscelanea')):
        for e in [x for x in effs if x['cat'] == cat]:
            # el iframe de la tarjeta es el unico sitio donde aparece esta cadena
            if ('efectos_webgl/%s/%s/%s.html?demo=1'
                    % (folder, e['nombre'], e['nombre'])) in t:
                continue
            pat = 'efectos_webgl/%s/' % folder
            ult = t.rindex(pat)
            fin = t.index('</article>', ult) + len('</article>')
            card = CARD_TPL.format(
                n='', WORD=e['word'], cat=cat, nombre=e['nombre'],
                folder=folder, TITULO=e['titulo'], sub=e['sub'],
                EMOJI=e['emoji'])
            t = t[:fin] + n(card) + t[fin:]
            added_card += 1

    # --- 4) fondos .wg-* de cada tarjeta nueva ---
    i = t.index('.wg-mercurio {')
    j = t.index('}', i) + 1
    bloques = ''
    for e in effs:
        if ('.wg-%s {' % e['nombre']) in t:
            continue
        bloques += n(WG_TPL.format(WORD=e['word'], sub=e['sub'],
                                   nombre=e['nombre'], preview=e['preview']))
        added_wg += 1
    if bloques:
        t = t[:j] + bloques + t[j:]

    wr(path, t, crlf=True)
    return added_li, added_card, added_wg


# =============================================================================
#  i18n · DICC ES->EN (objeto en linea unica; se inserta antes del cierre })
# =============================================================================
def _dicc_span(src):
    i = src.index('var DICC = ') + len('var DICC = ')
    depth, j, instr, esc = 0, i, False, False
    while True:
        c = src[j]
        if instr:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
        j += 1
    return i, j


def patch_i18n(effs):
    path = os.path.join(BASE, 'i18n.js')
    src = rd(path, raw=True)
    i, j = _dicc_span(src)
    dicc = json.loads(src[i:j + 1])
    nuevos = {}
    for e in effs:
        pares = [
            ('%s %s' % (e['emoji'], e['titulo']),
             '%s %s' % (e['emoji'], e['titulo_en'])),
            ('%s %s <small>%s</small>' % (e['emoji'], e['titulo'], e['sub']),
             '%s %s <small>%s</small>' % (e['emoji'], e['titulo_en'], e['sub_en'])),
            (e['sub'], e['sub_en']),
            ('%s · Showcase WebGL' % e['word'],
             '%s · WebGL Showcase' % e['word_en']),
            (e['descr'], e['descr_en']),
        ]
        for k, v in pares:
            if k not in dicc and k not in nuevos:
                nuevos[k] = v
    for k, v in FIXED_I18N.items():
        if k not in dicc and k not in nuevos:
            nuevos[k] = v
    if not nuevos:
        return 0
    frag = ''.join(',\n  %s: %s' % (json.dumps(k, ensure_ascii=False),
                                    json.dumps(v, ensure_ascii=False))
                   for k, v in sorted(nuevos.items()))
    src = src[:j] + frag + src[j:]
    wr(path, src, crlf=False)
    return len(nuevos)


# =============================================================================
#  MAIN
# =============================================================================
def build_zip(e):
    ruta = os.path.join(BASE, 'efectos_webgl', e['folder'], e['nombre'])
    zpath = os.path.join(ruta, e['nombre'] + '.zip')
    lic = os.path.join(BASE, 'LICENSE')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(ruta, e['nombre'] + '.html'), e['nombre'] + '.html')
        z.write(os.path.join(ruta, 'installation-instalacion-' + e['nombre'] + '.txt'),
                'installation-instalacion-' + e['nombre'] + '.txt')
        if os.path.isfile(lic):
            z.write(lic, 'LICENSE')


def main():
    effs = EFFECTS
    # saneo de claves derivadas
    for e in effs:
        e.setdefault('escena_id', e['nombre'])
        e.setdefault('word_en', e['word'])
        e.setdefault('titulo_corto', e['titulo'])
        e['folder'] = 'Matrix' if e['cat'] == 'matrix' else 'miscelanea'

    n_eff = n_show = n_txt = 0
    for e in effs:
        ruta = os.path.join(BASE, 'efectos_webgl', e['folder'], e['nombre'])
        f_eff = os.path.join(ruta, e['nombre'] + '.html')
        f_show = os.path.join(ruta, 'index.html')
        f_txt = os.path.join(ruta, 'installation-instalacion-' + e['nombre'] + '.txt')
        if not os.path.isfile(f_eff):
            wr(f_eff, build_effect(e))
            n_eff += 1
        if not os.path.isfile(f_show):
            wr(f_show, build_showcase(e))
            n_show += 1
        if not os.path.isfile(f_txt):
            wr(f_txt, build_install(e))
            n_txt += 1
        build_zip(e)   # el zip siempre se (re)genera: barato y queda al dia

    n_h, n_c = patch_transicion(effs)
    n_li, n_card, n_wg = patch_index(effs)
    n_i18n = patch_i18n(effs)

    print('efectos nuevos      : %d' % n_eff)
    print('showcases nuevos    : %d' % n_show)
    print('instalaciones nuevas: %d' % n_txt)
    print('escenas html/css    : %d / %d' % (n_h, n_c))
    print('portada li/tarjetas/wg: %d / %d / %d' % (n_li, n_card, n_wg))
    print('claves i18n nuevas  : %d' % n_i18n)
    print('zips regenerados    : %d' % len(effs))


if __name__ == '__main__':
    main()
