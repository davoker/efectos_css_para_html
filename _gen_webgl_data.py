# -*- coding: utf-8 -*-
"""
_gen_webgl_data.py · datos de los 37 efectos WebGL nuevos
  · 18 en efectos_webgl/Matrix      (tematica saga de peliculas)
  · 19 en efectos_webgl/miscelanea  (tematica libre)

Cada entrada genera: efecto HTML (shader propio), showcase, instalacion
ES+EN, zip, escena de transicion y tarjeta en la portada.
"""

# claves fijas: contadores nuevos de la portada
FIXED_I18N = {
    '40 disponibles': '40 available',
    '40 en tiempo real': '40 in real time',
}

EFFECTS = [

# ===================================================== MATRIX (18) ==========
dict(
    nombre='arquitecto', cat='matrix',
    word='ARQUITECTO', word_en='ARQUITECT', emoji='\U0001F3DB',
    titulo='Arquitecto', titulo_en='Architect',
    sub='Muro de pantallas', sub_en='Wall of screens',
    descr='Un muro de monitores parpadea dentro de las letras y una grieta de luz marca la bifurcacion.',
    descr_en='A wall of monitors flickers inside the letters and a crack of light marks the fork.',
    acento='90, 190, 255', bg='#04060c', fg='#9fd0ff',
    hint='mueve el raton para recorrer el muro &middot; clic para abrir la grieta &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #071426, #02050b 70%)',
    escena=('ring', '#5ac8ff', {'n': 3, 'palabra': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'rejilla de pantallas', 'grieta de eleccion',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el muro '
          'parpadeando solo. Dentro del efecto el raton recorre las pantallas y el clic abre '
          'la grieta de luz.',
    que_hace='Las letras son un muro de monitores: cada celda enciende y apaga su canal con '
             'un hash estable, y por el centro corre una grieta de luz blanca que late. El '
             'raton recorre el muro y el clic abre la grieta con un anillo.',
    que_hace_en='The letters are a wall of monitors: every cell blinks its channel on and off '
                'with a stable hash, and a crack of white light pulses along the middle. The '
                'mouse roams the wall and the click opens the crack with a ring.',
    tecnica='&middot; Rejilla por <code>fract</code> sobre la UV del texto, con hash por celda\n'
            '&middot; Flicker temporal: piso del tiempo multiplica el hash de cada pantalla\n'
            '&middot; La grieta es un <code>smoothstep</code> sobre |x-0.5| modulado por seno',
    tecnica_en='&middot; Grid built with <code>fract</code> over the text UV, hashed per cell\n'
               '&middot; Temporal flicker: the time floor multiplies every screen hash\n'
               '&middot; The crack is a <code>smoothstep</code> over |x-0.5| driven by a sine',
    ajustes='&middot; Nº de pantallas: el <code>9.0, 5.0</code> de <code>tuv*vec2(9,5)</code>\n'
            '&middot; Flicker: el <code>t*4.0</code> del piso temporal (mas rapido = mas nervioso)\n',
    ajustes_en='&middot; Screen count: the <code>9.0, 5.0</code> in <code>tuv*vec2(9,5)</code>\n'
               '&middot; Flicker: the <code>t*4.0</code> time floor (faster = more nervous)\n',
    shader=r'''
vec2 sg = fract(tuv * vec2(9.0, 5.0) + vec2(0.0, floor(t * 2.0) * 0.07));
vec2 idg = floor(tuv * vec2(9.0, 5.0));
float flick = hash21(idg + floor(t * 4.0));
float marco = step(.08, sg.x) * step(sg.x, .92) * step(.10, sg.y) * step(sg.y, .90);
float lado = step(idg.x, 4.0);
vec3 pan = mix(vec3(.10, .28, .55), vec3(.55, .14, .16), lado);
float on = mix(step(.55, flick), .6 + .4 * sin(t * 9.0 + flick * 30.0), .5);
vec3 fill = pan * marco * on * 1.6 + vec3(.03, .05, .08);
float split = smoothstep(.012, .0, abs(tuv.x - .5 - .02 * sin(tuv.y * 9.0 + t * 2.0)));
fill += vec3(1.0, .95, .75) * split * (.5 + .5 * sin(t * 6.0));
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(.012, .018, .030);
vec3 col = mix(bgc, fill, mask);
col += vec3(.35, .7, 1.0) * rim * .7;
col += vec3(.5, .8, 1.0) * ring * .5;
col += vec3(.6, .8, 1.0) * mBoost * mask * .3;
'''),

dict(
    nombre='smith', cat='matrix',
    word='SMITH', word_en='SMITH', emoji='\U0001F576',
    titulo='Smith', titulo_en='Smith',
    sub='La replica se multiplica', sub_en='The replica multiplies',
    descr='Manchas negras de traje devoran el verde del texto y las gafas destellan.',
    descr_en='Black suit blotches devour the green text and the sunglasses flare.',
    acento='40, 230, 120', bg='#02060a', fg='#8ff0b8',
    hint='el raton espanta las manchas &middot; clic para forzar la replica &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #04160c, #010604 70%)',
    escena=('halo', '#2bff77', {'palabra': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'replica viral', 'gafas con destello',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la replica '
          'crecer sola. El raton espanta las manchas y el clic fuerza otra replica.',
    que_hace='El texto verde va siendo devorado por manchas negras que se multiplican sobre '
             'ruido en movimiento; por el centro, la banda de las gafas deja un destello '
             'blanco que sigue el pulso del efecto.',
    que_hace_en='The green text is devoured by black blotches multiplying over moving noise; '
                'across the middle, the sunglasses band leaves a white flare that follows the '
                'effect pulse.',
    tecnica='&middot; Ruido <code>vnoise</code> desplazado en Y que cruza la máscara\n'
            '&middot; Umbral doble: mancha oscura + borde verde que resplandece\n'
            '&middot; Destello de gafas con gaussiana sobre un punto animado',
    tecnica_en='&middot; <code>vnoise</code> scrolled in Y crossing the mask\n'
               '&middot; Double threshold: dark blotch + glowing green edge\n'
               '&middot; Sunglass flare as a gaussian over an animated point',
    ajustes='&middot; Velocidad: el <code>t*0.35</code> del ruido\n'
            '&middot; Mancha: umbrales <code>0.55, 0.78</code>\n',
    ajustes_en='&middot; Speed: the <code>t*0.35</code> noise scroll\n'
               '&middot; Blotch: the <code>0.55, 0.78</code> thresholds\n',
    shader=r'''
float vor = vnoise(tuv * 7.0 + vec2(0.0, t * 0.35));
float blot = smoothstep(0.55, 0.78, vor);
vec3 fill = mix(vec3(0.06, 0.55, 0.24), vec3(0.015, 0.02, 0.018), blot);
fill += vec3(0.10, 1.0, 0.45) * pow(1.0 - blot, 3.0) * 0.8;
float gp = step(abs(tuv.y - 0.5 + 0.02 * sin(t)), 0.045);
fill = mix(fill, vec3(0.0), gp * 0.7);
vec2 ojo = tuv - vec2(0.42 + 0.05 * sin(t * 1.3), 0.5);
fill += vec3(1.0) * exp(-60.0 * dot(ojo, ojo)) * 0.9;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.010, 0.016, 0.012);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.2, 1.0, 0.5) * rim * 0.6;
col += vec3(0.3, 1.0, 0.5) * ring * 0.4;
'''),

dict(
    nombre='constructo', cat='matrix',
    word='CONSTRUCTO', word_en='CONSTRUCT', emoji='\u2B1C',
    titulo='Constructo', titulo_en='Construct',
    sub='Espacio de carga', sub_en='Loading space',
    descr='Rejilla de alambre en perspectiva y un portal que respira dentro del texto.',
    descr_en='Wireframe grid in perspective with a breathing portal inside the text.',
    acento='200, 230, 255', bg='#07080a', fg='#dfe8f2',
    hint='arrastra el raton para inclinar la rejilla &middot; clic para abrir el portal &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #161a20, #05070a 70%)',
    escena=('malla', '#cfe6ff', {'palabra': False}),
    datos=['GLSL ES 1.00', '1 pasada', 'rejilla en perspectiva', 'portal',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la rejilla '
          'correr sola. El raton inclina el espacio y el clic abre el portal.',
    que_hace='Dentro de las letras corre una rejilla de alambre clasica del espacio de carga, '
             'con una barrida de escaneo descendente y un portal circular que se abre y se '
             'cierra con el clic.',
    que_hace_en='Inside the letters runs the classic loading-space wireframe grid, with a '
                'downward scan sweep and a circular portal that opens and closes on click.',
    tecnica='&middot; Rejilla con <code>fract</code> y <code>smoothstep</code> en ambos ejes\n'
            '&middot; Barrida: seno desplazado en Y recortado a una banda estrecha\n'
            '&middot; Portal: distancia eliptica al centro con umbral animado',
    tecnica_en='&middot; Grid via <code>fract</code> + <code>smoothstep</code> on both axes\n'
               '&middot; Sweep: a sine scrolled in Y clipped to a narrow band\n'
               '&middot; Portal: elliptic distance to centre with an animated threshold',
    ajustes='&middot; Densidad: el <code>12.0, 7.0</code> de la rejilla\n'
            '&middot; Barrida: la velocidad <code>t*0.30</code> del escaner\n',
    ajustes_en='&middot; Density: the <code>12.0, 7.0</code> grid scale\n'
               '&middot; Sweep: the <code>t*0.30</code> scanner speed\n',
    shader=r'''
vec2 gr = fract(tuv * vec2(12.0, 7.0));
float wire = clamp(smoothstep(0.07, 0.0, gr.x) + smoothstep(0.07, 0.0, gr.y), 0.0, 1.0);
float scan = smoothstep(0.03, 0.0, abs(fract(tuv.y + t * 0.30) - 0.5) * 2.0 - 0.94);
float persp = 1.0 / (0.35 + tuv.y * 1.4);
float riel = smoothstep(0.06, 0.0, abs(fract(tuv.x * persp * 4.0) - 0.5) * 2.0 - 0.92);
vec3 fill = vec3(0.05, 0.06, 0.08)
          + vec3(0.65, 0.85, 1.0) * wire * 0.55
          + vec3(0.8, 0.95, 1.0) * riel * 0.35
          + vec3(1.0) * scan * 0.9;
float pr = length((tuv - vec2(0.5, 0.48)) * (uPlane / min(uPlane.x, uPlane.y)));
float portal = smoothstep(0.30, 0.26, pr + 0.05 * sin(t * 2.4));
float anillo = smoothstep(0.05, 0.0, abs(pr - 0.28 - 0.05 * sin(t * 2.4)));
fill += vec3(0.35, 0.75, 1.0) * portal * 0.35 + vec3(0.9, 0.98, 1.0) * anillo;
vec3 bgc = vec3(0.03, 0.033, 0.038);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.6, 0.85, 1.0) * pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5) * 0.7;
col += vec3(0.8, 0.9, 1.0) * ring * 0.5;
'''),

dict(
    nombre='dojo', cat='matrix',
    word='DOJO', word_en='DOJO', emoji='\U0001F94B',
    titulo='Dojo', titulo_en='Dojo',
    sub='Descarga de kung fu', sub_en='Kung fu download',
    descr='Estelas de velocidad cruzan el texto y un sello rojo estampa la palabra.',
    descr_en='Speed streaks cross the text and a red stamp seals the word.',
    acento='255, 90, 70', bg='#0a0406', fg='#ffc9be',
    hint='el raton gira las estelas &middot; clic para estampar el sello &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #220a08, #080305 70%)',
    escena=('estelas', '#ff5a46', {'n': 6, 'ang': 20, 'palabra': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'estelas diagonales', 'sello rojo',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja las estelas '
          'correr solas. El raton gira las lineas y el clic estampa el sello.',
    que_hace='El texto se llena de estelas diagonales que rayan el fondo como un entrenamiento '
             'a maxima velocidad, y un sello circular rojo late sobre la palabra con cada clic.',
    que_hace_en='The text fills with diagonal streaks that scratch the background like training '
                'at full speed, and a circular red seal beats over the word on every click.',
    tecnica='&middot; Estelas: seno de <code>dot(tuv, dir)</code> desplazado en el tiempo\n'
            '&middot; Sello: dos distancias elipticas (disco y anillo) con umbral\n'
            '&middot; Direccion girada por <code>uMouse.x</code> solo con el raton activo',
    tecnica_en='&middot; Streaks: sine of <code>dot(tuv, dir)</code> scrolled in time\n'
               '&middot; Seal: two elliptic distances (disc and ring) with thresholds\n'
               '&middot; Direction rotated by <code>uMouse.x</code> only while the mouse is live',
    ajustes='&middot; Angulo base: el <code>0.5</code> de la direccion\n'
            '&middot; Frecuencia: el <code>70.0</code> del seno (mas rayas)\n',
    ajustes_en='&middot; Base angle: the direction constant <code>0.5</code>\n'
               '&middot; Frequency: the <code>70.0</code> sine (more scratches)\n',
    shader=r'''
float ang = 0.5 + 0.6 * uMouse.x * uAmp;
vec2 dir = vec2(cos(ang), sin(ang));
float stripe = sin(dot(tuv, dir) * 70.0 - t * 26.0);
float estela = smoothstep(0.55, 1.0, stripe) * 0.85;
vec2 ds = (tuv - vec2(0.5, 0.5)) * (uPlane / min(uPlane.x, uPlane.y));
float rr = length(ds);
float disco = smoothstep(0.34, 0.30, rr);
float aro = smoothstep(0.03, 0.0, abs(rr - 0.32));
float golpe = exp(-4.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float lat = clamp(0.55 + 0.45 * sin(t * 7.0) + 2.5 * golpe, 0.0, 1.6);
vec3 fill = vec3(0.30, 0.04, 0.04) * lat
          + vec3(1.0, 0.85, 0.7) * estela;
fill = mix(fill, vec3(0.85, 0.12, 0.09), disco * 0.55 * lat);
fill += vec3(1.0, 0.9, 0.85) * aro * lat;
vec3 bgc = vec3(0.04, 0.015, 0.012);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.5, 0.3) * ring * 0.5;
col += vec3(1.0, 0.7, 0.6) * pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5) * 0.6;
'''),

dict(
    nombre='cables', cat='matrix',
    word='CABLES', word_en='CABLES', emoji='\U0001F50C',
    titulo='Cables', titulo_en='Cables',
    sub='Pulsos de datos', sub_en='Data pulses',
    descr='Pulsos de luz recorren los cables horizontales que cruzan las letras.',
    descr_en='Light pulses run across the horizontal cables crossing the letters.',
    acento='60, 255, 200', bg='#02080a', fg='#9ffce6',
    hint='el raton acelera los pulsos &middot; clic para lanzar un pulso &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #04201b, #010607 70%)',
    escena=('barrido', '#3cffc8', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'cables en paralelo', 'pulsos viajeros',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja los pulsos '
          'viajar solos. El raton acelera el flujo y el clic lanza un pulso nuevo.',
    que_hace='Cinco cables horizontales atraviesan el texto y por ellos viajan pulsos claros '
             'a velocidades distintas; el raton acelera el flujo y el clic dispara un pulso '
             'extra que sale despedido.',
    que_hace_en='Five horizontal cables cross the text and bright pulses travel along them at '
                'different speeds; the mouse speeds up the flow and the click fires an extra '
                'pulse that shoots away.',
    tecnica='&middot; Banda por <code>fract(tuv.y*5.0)</code> con borde suave\n'
            '&middot; Pulso: gaussiana sobre <code>fract(x*vel - t)</code> por carril\n'
            '&middot; Aceleracion: <code>uAmp</code> modula la velocidad efectiva',
    tecnica_en='&middot; Lane from <code>fract(tuv.y*5.0)</code> with a soft edge\n'
               '&middot; Pulse: gaussian over <code>fract(x*speed - t)</code> per lane\n'
               '&middot; Acceleration: <code>uAmp</code> modulates the effective speed',
    ajustes='&middot; Nº de cables: el <code>5.0</code> de la banda\n'
            '&middot; Grosor: el <code>0.16</code> del umbral de borde\n',
    ajustes_en='&middot; Cable count: the <code>5.0</code> lane scale\n'
               '&middot; Thickness: the <code>0.16</code> edge threshold\n',
    shader=r'''
float lane = fract(tuv.y * 5.0 + 0.15);
float cable = smoothstep(0.30, 0.16, abs(lane - 0.5));
float fila = floor(tuv.y * 5.0 + 0.15);
float vel = 0.25 + 0.5 * hash21(vec2(fila, 3.0));
vel *= 1.0 + 2.0 * uAmp;
float fase = fract(tuv.x * 1.4 - t * vel + hash21(vec2(fila, 9.0)));
float pulso = exp(-40.0 * pow(fase - 0.5, 2.0));
float fase2 = fract(tuv.x * 1.4 - t * vel + 0.5 + hash21(vec2(fila, 9.0)));
pulso += 0.6 * exp(-40.0 * pow(fase2 - 0.5, 2.0));
float clic = exp(-60.0 * pow(fract(tuv.x - (t - uClickT) * 1.6) - 0.5, 2.0))
           * exp(-1.2 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec3 fill = vec3(0.01, 0.04, 0.05)
          + vec3(0.10, 0.45, 0.40) * cable * 0.7
          + vec3(0.35, 1.0, 0.85) * cable * (pulso * 2.2 + clic * 1.6);
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.006, 0.020, 0.024);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.3, 1.0, 0.8) * rim * 0.55;
col += vec3(0.3, 1.0, 0.8) * ring * 0.5;
'''),

dict(
    nombre='tunel', cat='matrix',
    word='TUNEL', word_en='TUNNEL', emoji='\U0001F687',
    titulo='Tunel', titulo_en='Tunnel',
    sub='Huida en el metro', sub_en='Subway escape',
    descr='Estelas radiales huyen del centro: el texto viaja por el tunel a toda velocidad.',
    descr_en='Radial streaks flee the centre: the text travels through the tunnel at full speed.',
    acento='255, 170, 60', bg='#0a0704', fg='#ffd9a0',
    hint='el raton apunta la salida &middot; clic para acelerar la huida &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #241505, #070401 70%)',
    escena=('rayos', '#ffa63a', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'estelas radiales', 'velocidad del metro',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el tunel '
          'correr solo. El raton apunta la salida y el clic acelera la huida.',
    que_hace='Lineas radiales brotan del centro del texto y se disparan hacia fuera como si '
             'el metro saliera del tunel; el clic lanza una acelerada con anillo de onda.',
    que_hace_en='Radial lines burst from the centre of the text and shoot outward as if the '
                'subway left the tunnel; the click fires a burst with a ring wave.',
    tecnica='&middot; Coordenada radial <code>atan</code> + distancia al centro\n'
            '&middot; Fase por <code>fract(r*4.0 - t)</code> para el vuelo de las lineas\n'
            '&middot; Ancho de estela con <code>smoothstep</code> sobre el angulo',
    tecnica_en='&middot; Radial coordinate via <code>atan</code> + distance to centre\n'
               '&middot; Phase from <code>fract(r*4.0 - t)</code> drives the line flight\n'
               '&middot; Streak width via <code>smoothstep</code> over the angle',
    ajustes='&middot; Nº de estelas: el <code>18.0</code> del seno angular\n'
            '&middot; Velocidad: el <code>4.0</code> de la fase radial\n',
    ajustes_en='&middot; Streak count: the angular <code>18.0</code> sine\n'
               '&middot; Speed: the <code>4.0</code> radial phase\n',
    shader=r'''
vec2 d = (tuv - vec2(0.5, 0.5)) * (uPlane / min(uPlane.x, uPlane.y));
float rr = length(d) + 1e-4;
float ari = atan(d.y, d.x);
float rayo = 0.5 + 0.5 * sin(ari * 18.0 + t * 1.5);
rayo = pow(rayo, 6.0);
float fase = fract(rr * 4.0 - t * (1.5 + 2.5 * uAmp));
float viaje = smoothstep(0.0, 0.25, fase) * smoothstep(1.0, 0.55, fase);
float centro = exp(-14.0 * rr);
vec3 fill = vec3(0.05, 0.03, 0.02)
          + vec3(1.0, 0.65, 0.20) * rayo * viaje * 1.6
          + vec3(1.0, 0.9, 0.7) * centro;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.03, 0.02, 0.012);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.7, 0.3) * rim * 0.6;
col += vec3(1.0, 0.6, 0.3) * ring * 0.6;
'''),

dict(
    nombre='alarma', cat='matrix',
    word='ALARMA', word_en='ALARM', emoji='\U0001F6A8',
    titulo='Alarma', titulo_en='Alarm',
    sub='Codigo rojo', sub_en='Red code',
    descr='El codigo rojo barre el texto y las franjas de peligro laten con el clic.',
    descr_en='Red code sweeps the text and hazard stripes pulse with the click.',
    acento='255, 60, 60', bg='#0c0204', fg='#ffb3b3',
    hint='el raton frena el barrido &middot; clic para disparar la alarma &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2a0508, #0a0103 70%)',
    escena=('chispas', '#ff3b3b', {'n': 14}),
    datos=['GLSL ES 1.00', '1 pasada', 'codigo rojo', 'franjas de peligro',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la alarma '
          'sonando sola. El raton frena el barrido y el clic dispara otra rafaga.',
    que_hace='Una linea de codigo rojo barre las letras de arriba abajo sin parar y las '
             'franjas diagonales de peligro laten a golpe de clic, como un sistema en alerta.',
    que_hace_en='A red code line sweeps the letters top to bottom forever and the diagonal '
                'hazard stripes pulse with every click, like a system on alert.',
    tecnica='&middot; Barrido: <code>fract(tuv.y - t)</code> recortado a una banda fina\n'
            '&middot; Franjas: <code>fract((x+y)*6.0)</code> con paso para rayar\n'
            '&middot; Latido: envolvente exponencial del tiempo del clic',
    tecnica_en='&middot; Sweep: <code>fract(tuv.y - t)</code> clipped to a thin band\n'
               '&middot; Stripes: <code>fract((x+y)*6.0)</code> with a hard step\n'
               '&middot; Pulse: exponential envelope of the click time',
    ajustes='&middot; Nº de franjas: el <code>6.0</code> de la diagonal\n'
            '&middot; Velocidad del barrido: el <code>t*0.6</code> del fract\n',
    ajustes_en='&middot; Stripe count: the diagonal <code>6.0</code>\n'
               '&middot; Sweep speed: the <code>t*0.6</code> fract scroll\n',
    shader=r'''
float banda = smoothstep(0.10, 0.0, abs(fract(tuv.y - t * 0.6) - 0.5) * 2.0 - 0.9);
float franja = step(0.5, fract((tuv.x + tuv.y) * 6.0));
float golpe = exp(-3.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float lat = clamp(0.4 + 0.3 * sin(t * 9.0) + 1.6 * golpe, 0.0, 1.5);
vec3 fill = vec3(0.16, 0.01, 0.02) * lat
          + vec3(1.0, 0.15, 0.12) * banda * lat * 1.6
          + vec3(1.0, 0.55, 0.2) * franja * 0.16 * lat;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.045, 0.008, 0.012);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.3, 0.25) * rim * lat * 0.7;
col += vec3(1.0, 0.2, 0.2) * ring * 0.6;
'''),

dict(
    nombre='merovingio', cat='matrix',
    word='MEROVINGIO', word_en='MEROVINGIAN', emoji='\U0001F451',
    titulo='Merovingio', titulo_en='Merovingian',
    sub='Filigrana dorada', sub_en='Golden filigree',
    descr='Filos de oro se enroscan por dentro de las letras como un barroco vivo.',
    descr_en='Gold threads curl inside the letters like living baroque ornament.',
    acento='255, 200, 80', bg='#0b0803', fg='#ffe0a3',
    hint='el raton abre el deseo &middot; clic para encender la filigrana &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #241a05, #080501 70%)',
    escena=('ring', '#ffc850', {'n': 4}),
    datos=['GLSL ES 1.00', '1 pasada', 'filigrana en espiral', 'brillo barroco',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la filigrana '
          'dibujarse sola. El raton abre el deseo y el clic enciende mas hilos de oro.',
    que_hace='Hilos de oro se enroscan dentro de las letras con ruido curvilíneo, brillando '
             'como joyeria barroca; el clic enciende una onda de brillo que recorre la palabra.',
    que_hace_en='Gold threads curl inside the letters with curvy noise, shining like baroque '
                'jewellery; the click sends a shine wave across the word.',
    tecnica='&middot; Ruido de dominio <code>fbm</code> doble para enroscar los filos\n'
            '&middot; Filo: potencia alta del seno del ruido = lineas finas\n'
            '&middot; Onda del clic atenua la potencia para el destello',
    tecnica_en='&middot; Double <code>fbm</code> domain noise to curl the threads\n'
               '&middot; Thread: high power of the noise sine = thin lines\n'
               '&middot; The click wave lowers the power for the flare',
    ajustes='&middot; Nº de hilos: el <code>10.0</code> de la potencia\n'
            '&middot; Espesor: baja el exponente <code>6.0</code>\n',
    ajustes_en='&middot; Thread count: the <code>10.0</code> frequency\n'
               '&middot; Thickness: lower the <code>6.0</code> exponent\n',
    shader=r'''
vec2 q = vec2(fbm(tuv * 3.0 + vec2(0.0, t * 0.10)),
              fbm(tuv * 3.0 + vec2(4.7, 1.3) - t * 0.08));
float hilo = sin((q.x + q.y) * 10.0 * 3.1416 + t * 1.2);
float filo = pow(0.5 + 0.5 * hilo, 6.0);
float brillo = exp(-25.0 * length(fract(q * 2.0) - 0.5)) * 0.6;
float onda = 1.0 + 1.4 * exp(-6.0 * abs(fract(tuv.x - (t - uClickT) * 0.8) - 0.5) * 2.0)
           * exp(-1.5 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec3 fill = vec3(0.10, 0.07, 0.02)
          + vec3(1.0, 0.78, 0.30) * filo * 1.5 * onda
          + vec3(1.0, 0.9, 0.6) * brillo;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.035, 0.026, 0.010);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.8, 0.35) * rim * 0.7;
col += vec3(1.0, 0.8, 0.4) * ring * 0.5;
'''),

dict(
    nombre='gemelos', cat='matrix',
    word='GEMELOS', word_en='TWINS', emoji='\U0001F46F',
    titulo='Gemelos', titulo_en='Twins',
    sub='Fase fantasma', sub_en='Ghost phase',
    descr='Dos imagenes fantasma del texto se desfasan y se funden en aceite iridiscente.',
    descr_en='Two ghost copies of the text drift apart and melt into iridescent oil.',
    acento='150, 255, 220', bg='#03080a', fg='#c9fff2',
    hint='el raton separa los gemelos &middot; clic para cruzar las fases &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #06201c, #010607 70%)',
    escena=('estelas', '#96ffd8', {'n': 4, 'ang': 60}),
    datos=['GLSL ES 1.00', '1 pasada', 'doble fantasma', 'fase iridiscente',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja las fases '
          'cruzarse solas. El raton separa los gemelos y el clic los vuelve a cruzar.',
    que_hace='La palabra existe dos veces con un desfase que crece y decrece; donde las dos '
             'copias chocan aparece un aceite iridiscente que cambia de color con el tiempo.',
    que_hace_en='The word exists twice with an offset that grows and shrinks; where the two '
                'copies clash an iridescent oil appears, shifting colour over time.',
    tecnica='&middot; Dos muestras de <code>uText</code> con desplazamiento opuesto\n'
            '&middot; Iridiscencia: coseno del desfase con desplazamiento de fase RGB\n'
            '&middot; El desfase baja con <code>uAmp</code> cuando el raton se para',
    tecnica_en='&middot; Two <code>uText</code> samples with opposite offsets\n'
               '&middot; Iridescence: cosine of the offset with an RGB phase shift\n'
               '&middot; The offset shrinks with <code>uAmp</code> when the mouse rests',
    ajustes='&middot; Amplitud maxima: el <code>0.035</code> del desfase\n'
            '&middot; Ciclo: el <code>t*1.3</code> del cruce\n',
    ajustes_en='&middot; Max offset: the <code>0.035</code> shift\n'
               '&middot; Cycle: the <code>t*1.3</code> crossing\n',
    shader=r'''
float des = (0.006 + 0.030 * uAmp) * sin(t * 1.3);
float mA = maskAt(tuv + vec2(des, des * 0.6));
float mB = maskAt(tuv - vec2(des, des * 0.6));
float fase = (mA - mB);
vec3 aceite = 0.5 + 0.5 * cos(6.2831 * (tuv.x * 2.0 + tuv.y * 3.0 + t * 0.4)
                              + vec3(0.0, 2.1, 4.2));
vec3 fill = vec3(0.02, 0.05, 0.05);
fill += vec3(0.55, 1.0, 0.85) * mA * 0.7;
fill += vec3(0.35, 0.65, 1.0) * mB * 0.7;
fill += aceite * abs(fase) * 2.2;
vec3 bgc = vec3(0.010, 0.020, 0.022);
vec3 col = mix(bgc, fill, max(mA, mB));
col += aceite * ring * 0.5;
col += vec3(0.6, 1.0, 0.9) * pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5) * 0.5;
'''),

dict(
    nombre='eleccion', cat='matrix',
    word='ELECCION', word_en='CHOICE', emoji='\U0001F7E1',
    titulo='Eleccion', titulo_en='Choice',
    sub='Rojo o azul', sub_en='Red or blue',
    descr='La palabra se parte en rojo y azul con una costura de luz que tiembla.',
    descr_en='The word splits into red and blue with a trembling seam of light.',
    acento='180, 120, 255', bg='#07040e', fg='#e0cdff',
    hint='el raton marea la costura &middot; clic para lanzar la moneda &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #170a2a, #05020a 70%)',
    escena=('halo', '#b478ff', {'palabra': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'bicolor partido', 'costura de luz',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la costura '
          'temblando sola. El raton marea la division y el clic lanza la moneda al aire.',
    que_hace='La mitad izquierda de las letras arde en rojo y la derecha en azul, con una '
             'costura de luz blanca que serpentea entre las dos; el clic invierte las mitades.',
    que_hace_en='The left half of the letters burns red and the right half blue, with a white '
                'seam of light snaking between them; the click swaps the halves.',
    tecnica='&middot; Umbral en X con ruido vertical para la costura serpenteante\n'
            '&middot; Mezcla <code>mix</code> de dos tintas con el umbral\n'
            '&middot; Giro de la costura con <code>floor(t)</code> para la moneda',
    tecnica_en='&middot; X threshold with vertical noise for the snaking seam\n'
               '&middot; <code>mix</code> of two inks driven by the threshold\n'
               '&middot; Seam flip via <code>floor(t)</code> for the coin toss',
    ajustes='&middot; Serpenteo: el <code>7.0</code> del ruido vertical\n'
            '&middot; Giro: el <code>0.5</code> de la velocidad de la moneda\n',
    ajustes_en='&middot; Meander: the <code>7.0</code> vertical noise\n'
               '&middot; Flip: the <code>0.5</code> coin speed\n',
    shader=r'''
float giro = floor(t * 0.5) * 3.1416;
float x0 = 0.5 + 0.10 * sin(tuv.y * 7.0 + t * 2.0) + 0.16 * sin(giro);
float lado = step(x0, tuv.x);
float voltea = mod(floor(t * 0.5), 2.0);
vec3 tintA = mix(vec3(0.95, 0.15, 0.20), vec3(0.20, 0.40, 1.0), voltea);
vec3 tintB = mix(vec3(0.20, 0.40, 1.0), vec3(0.95, 0.15, 0.20), voltea);
vec3 fill = mix(tintB, tintA, lado) * 0.9;
float costura = smoothstep(0.020, 0.0, abs(tuv.x - x0));
fill += vec3(1.0, 0.98, 0.92) * costura * 1.6;
float brillo = pow(1.0 - abs(2.0 * hb - 1.0), 2.0);
fill += vec3(1.0) * brillo * 0.10;
vec3 bgc = mix(vec3(0.05, 0.01, 0.03), vec3(0.01, 0.02, 0.07), lado);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.9, 0.9) * costura * mask * 0.8;
col += vec3(0.8, 0.6, 1.0) * ring * 0.5;
'''),

dict(
    nombre='red', cat='matrix',
    word='RED', word_en='NET', emoji='\U0001F578',
    titulo='Red', titulo_en='Net',
    sub='Nodos y enlaces', sub_en='Nodes and links',
    descr='Nodos encendidos se enlazan en malla sobre la superficie de las letras.',
    descr_en='Lit nodes link into a mesh over the surface of the letters.',
    acento='80, 255, 160', bg='#020a06', fg='#a8ffd0',
    hint='el raton enciende nodos cerca &middot; clic para enviar el paquete &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #052015, #010604 70%)',
    escena=('malla', '#4dff9f', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'malla de nodos', 'paquete viajero',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la red '
          'pulsando sola. El raton enciende nodos y el clic envia un paquete.',
    que_hace='Una malla de nodos verdes se enciende y se apaga en oleada dentro del texto, '
             'unidos por enlaces que parpadean; el clic envia un paquete de luz por la red.',
    que_hace_en='A mesh of green nodes lights up in waves inside the text, joined by blinking '
                'links; the click sends a light packet travelling across the net.',
    tecnica='&middot; Rejilla de celdas con hash que decide si el nodo existe\n'
            '&middot; Enlaces: banda fina entre centros de celda vecinos\n'
            '&middot; Paquete: gaussiana recorriendo la diagonal de la malla',
    tecnica_en='&middot; Cell grid with a hash deciding whether each node exists\n'
               '&middot; Links: thin band between neighbouring cell centres\n'
               '&middot; Packet: gaussian travelling along the mesh diagonal',
    ajustes='&middot; Nº de nodos: el <code>8.0</code> de la rejilla\n'
            '&middot; Oleada: el <code>t*2.0</code> del pulso\n',
    ajustes_en='&middot; Node count: the <code>8.0</code> grid scale\n'
               '&middot; Wave: the <code>t*2.0</code> pulse\n',
    shader=r'''
vec2 cg = tuv * (uPlane / min(uPlane.x, uPlane.y)) * 8.0;
vec2 id = floor(cg);
vec2 fr = fract(cg) - 0.5;
float existe = step(0.35, hash21(id));
float pulso = 0.5 + 0.5 * sin(t * 2.0 + hash21(id + 7.0) * 6.2831);
float nodo = smoothstep(0.16, 0.10, length(fr)) * existe;
float eX = smoothstep(0.04, 0.0, abs(fr.y)) * step(abs(fr.x), 0.5) * existe;
float eY = smoothstep(0.04, 0.0, abs(fr.x)) * step(abs(fr.y), 0.5) * existe;
float viaje = fract((tuv.x + tuv.y) * 0.5 - t * 0.6);
float paq = exp(-60.0 * pow(viaje - 0.5, 2.0)) * exp(-1.0 * max(t - uClickT, 0.0))
          * step(-9000.0, uClickT);
float cerca = exp(-14.0 * length(tuv - (0.5 + uMouse * 0.6)));
vec3 fill = vec3(0.01, 0.05, 0.03)
          + vec3(0.15, 0.75, 0.45) * (eX + eY) * (0.4 + 0.6 * pulso)
          + vec3(0.35, 1.0, 0.6) * nodo * (0.5 + 0.9 * pulso) * (1.0 + 2.0 * cerca)
          + vec3(1.0, 1.0, 0.9) * paq * 1.4;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.006, 0.022, 0.014);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.3, 1.0, 0.6) * rim * 0.55;
col += vec3(0.3, 1.0, 0.6) * ring * 0.5;
'''),

dict(
    nombre='descarga', cat='matrix',
    word='DESCARGA', word_en='UPLOAD', emoji='\U0001F4E4',
    titulo='Descarga', titulo_en='Upload',
    sub='El conocimiento baja', sub_en='Knowledge downloading',
    descr='Columnas de glyphos caen por dentro de las letras hasta completar la palabra.',
    descr_en='Glyph columns fall inside the letters until the word is complete.',
    acento='120, 255, 90', bg='#030a04', fg='#c6ffbb',
    hint='el raton empuja la lluvia &middot; clic para completar la descarga &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #0a2208, #020603 70%)',
    escena=('chispas', '#78ff5a', {'n': 16, 'up': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'columnas cayendo', 'relleno de datos',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la lluvia '
          'caer sola. El raton la empuja y el clic completa la descarga de golpe.',
    que_hace='Trazos de datos caen en columnas dentro del texto y van rellenando las letras '
             'desde abajo hasta que la palabra queda cargada por completo.',
    que_hace_en='Data dashes fall in columns inside the text and fill the letters from below '
                'until the word is fully loaded.',
    tecnica='&middot; Lluvia: <code>fract</code> de columna con hash de glifo por celda\n'
            '&middot; Relleno: umbral en Y que sube con el tiempo\n'
            '&middot; Empujon del raton: <code>uMouse.y</code> desplaza el umbral',
    tecnica_en='&middot; Rain: column <code>fract</code> with a per-cell glyph hash\n'
               '&middot; Fill: a Y threshold rising over time\n'
               '&middot; Mouse shove: <code>uMouse.y</code> shifts the threshold',
    ajustes='&middot; Velocidad de caida: el <code>2.2</code> del tiempo\n'
            '&middot; Nº de columnas: el <code>26.0</code> de la escala X\n',
    ajustes_en='&middot; Fall speed: the <code>2.2</code> time factor\n'
               '&middot; Column count: the <code>26.0</code> X scale\n',
    shader=r'''
float ncol = floor(tuv.x * 26.0);
float gota = fract(tuv.y * 6.0 + t * (1.4 + 1.6 * hash21(vec2(ncol, 1.0))));
float trazo = smoothstep(0.42, 0.5, fract(gota * 4.0)) * step(fract(gota * 4.0), 0.86);
float brilloG = step(0.75, fract(gota * 4.0 + 0.25));
float nivel = fract(t * 0.22 - uMouse.y * 0.3);
float lleno = step(1.0 - nivel, 1.0 - tuv.y);
float clic = clamp((t - uClickT) * 3.0, 0.0, 1.0) * step(-9000.0, uClickT);
float umbral = max(lleno, clic);
vec3 fill = vec3(0.01, 0.05, 0.02);
fill += vec3(0.25, 0.9, 0.35) * trazo * (1.0 - umbral * 0.7);
fill += vec3(0.7, 1.0, 0.6) * brilloG * trazo * 0.8;
fill += vec3(0.35, 1.0, 0.45) * umbral * (0.55 + 0.25 * sin(t * 5.0 + tuv.y * 9.0));
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.008, 0.026, 0.010);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.4, 1.0, 0.5) * rim * 0.55;
col += vec3(0.4, 1.0, 0.5) * ring * 0.5;
'''),

dict(
    nombre='helicoptero', cat='matrix',
    word='HELICOPTERO', word_en='HELICOPTER', emoji='\U0001F681',
    titulo='Helicoptero', titulo_en='Helicopter',
    sub='Foco de busqueda', sub_en='Searchlight',
    descr='Un haz de helicoptero barre el texto y levanta polvo donde cae.',
    descr_en='A helicopter beam sweeps the text and raises dust where it lands.',
    acento='255, 230, 140', bg='#08090c', fg='#fff2c9',
    hint='el raton maneja el haz &middot; clic para un barrido rapido &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #1d1c10, #06060a 70%)',
    escena=('barrido', '#ffe68c', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'haz giratorio', 'polvo levantado',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el haz '
          'barrer solo. El raton lo maneja y el clic dispara un barrido rapido.',
    que_hace='Un haz blanco cónico gira sobre el texto iluminando las letras por rotacion y '
             'levantando un polvo dorado en el borde; el raton fija hacia donde mira.',
    que_hace_en='A white conic beam rotates over the text, lighting the letters as it turns '
                'and raising golden dust at its edge; the mouse aims the searchlight.',
    tecnica='&middot; Angulo <code>atan</code> del punto respecto al centro del texto\n'
            '&middot; Haz: <code>smoothstep</code> angosto sobre la diferencia de angulo\n'
            '&middot; Polvo: ruido fino modulado por el propio haz',
    tecnica_en='&middot; Point angle via <code>atan</code> from the text centre\n'
               '&middot; Beam: narrow <code>smoothstep</code> on the angle difference\n'
               '&middot; Dust: fine noise modulated by the beam itself',
    ajustes='&middot; Ancho: baja el <code>0.16</code> del <code>smoothstep</code>\n'
            '&middot; Vuelta: el <code>t*1.1</code> de la velocidad\n',
    ajustes_en='&middot; Width: lower the <code>0.16</code> smoothstep\n'
               '&middot; Rotation: the <code>t*1.1</code> speed\n',
    shader=r'''
vec2 c = vec2(0.5, 0.15);
vec2 d = (tuv - c) * (uPlane / min(uPlane.x, uPlane.y));
float objetivo = atan(uMouse.y * 1.6 - 0.3, uMouse.x * 1.6 + 0.001);
float giro = t * 1.1 + 1.1 * sin(t * 0.6);
float mezcla = mix(giro, objetivo + t * 0.4, clamp(uAmp, 0.0, 1.0));
float ang = atan(d.y, d.x);
float dif = abs(mod(ang - mezcla + 3.1416, 6.2831) - 3.1416);
float golpe = exp(-6.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float ancho = 0.16 + 0.10 * golpe;
float haz = smoothstep(ancho, 0.0, dif) * smoothstep(1.1, 0.1, length(d));
float polvo = vnoise(tuv * 30.0 + vec2(0.0, -t * 1.4)) * haz;
vec3 fill = vec3(0.04, 0.045, 0.06)
          + vec3(1.0, 0.95, 0.75) * haz * 1.5
          + vec3(1.0, 0.8, 0.4) * polvo * 0.9;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.022, 0.025, 0.034);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.9, 0.6) * rim * (0.4 + haz);
col += vec3(1.0, 0.9, 0.7) * ring * 0.5;
'''),

dict(
    nombre='vagon', cat='matrix',
    word='VAGON', word_en='CARRIAGE', emoji='\U0001F689',
    titulo='Vagon', titulo_en='Carriage',
    sub='Ventanas que pasan', sub_en='Passing windows',
    descr='Las ventanas del vagon se disparan de lado a lado dentro de las letras.',
    descr_en='Carriage windows shoot from side to side inside the letters.',
    acento='255, 210, 120', bg='#07070a', fg='#ffe9c0',
    hint='el raton cambia de asiento &middot; clic para frenar el vagon &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #1d1a12, #06060a 70%)',
    escena=('barrido', '#ffd278', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'ventanas en fuga', 'freno del clic',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el vagon '
          'correr solo. El raton cambia de asiento y el clic frena el vagon.',
    que_hace='Rectangulos de luz —las ventanas del vagon— se disparan de izquierda a derecha '
             'dentro del texto con reflejo intermitente, como viajar de noche en el tren.',
    que_hace_en='Rectangles of light —the carriage windows— shoot from left to right inside '
                'the text with intermittent reflections, like travelling by night train.',
    tecnica='&middot; Columna periodica con <code>fract(x*3 - t*vel)</code>\n'
            '&middot; Ventana: umbral doble en X e Y con esquinas suavizadas\n'
            '&middot; Freno: <code>uClickT</code> enlentece la velocidad con amortiguacion',
    tecnica_en='&middot; Periodic column via <code>fract(x*3 - t*speed)</code>\n'
               '&middot; Window: double X/Y threshold with softened corners\n'
               '&middot; Brake: <code>uClickT</code> slows the speed with damping',
    ajustes='&middot; Nº de ventanas: el <code>3.0</code> de la escala\n'
            '&middot; Marcha: el <code>1.5</code> de la velocidad base\n',
    ajustes_en='&middot; Window count: the <code>3.0</code> scale\n'
               '&middot; Pace: the <code>1.5</code> base speed\n',
    shader=r'''
float frena = exp(-1.8 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float vel = (1.5 + 1.5 * uAmp) * (1.0 - 0.85 * frena);
float cx = fract(tuv.x * 3.0 - t * vel * 0.5);
float cy = fract(tuv.y * 3.0 + 0.5);
float win = smoothstep(0.10, 0.22, cx) * smoothstep(0.90, 0.78, cx)
          * smoothstep(0.14, 0.30, cy) * smoothstep(0.86, 0.70, cy);
float brillo = 0.55 + 0.45 * sin(t * 6.0 + floor(tuv.x * 3.0) * 2.3);
vec3 fill = vec3(0.03, 0.03, 0.045)
          + vec3(1.0, 0.86, 0.55) * win * brillo * 1.4
          + vec3(0.5, 0.6, 0.8) * win * 0.10;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.018, 0.018, 0.026);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.85, 0.6) * rim * 0.55;
col += vec3(1.0, 0.8, 0.5) * ring * 0.5;
'''),

dict(
    nombre='sistema', cat='matrix',
    word='SISTEMA', word_en='SYSTEM', emoji='\U0001F5A5',
    titulo='Sistema', titulo_en='System',
    sub='Hay un error', sub_en='There is an error',
    descr='Bloques de interfaz parpadean y un destello de error recorre la palabra.',
    descr_en='Interface blocks blink and an error flash crosses the word.',
    acento='255, 120, 180', bg='#0a0509', fg='#ffc6e0',
    hint='el raton barre la interfaz &middot; clic para provocar el error &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #260a18, #070306 70%)',
    escena=('malla', '#ff78b4', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'bloques de interfaz', 'destello de error',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la interfaz '
          'parpadeando sola. El raton barre bloques y el clic provoca el error.',
    que_hace='Bloques rectangulares de interfaz se encienden dentro del texto como ventanas '
             'de sistema, y un destello magenta de error salta a golpe de clic.',
    que_hace_en='Rectangular interface blocks light up inside the text like system windows, '
                'and a magenta error flash jumps on every click.',
    tecnica='&middot; Rejilla 2D con hash por bloque y parpadeo temporal\n'
            '&middot; Borde interior: diferencia de dos <code>smoothstep</code>\n'
            '&middot; Error: barrido horizontal con envolvente del clic',
    tecnica_en='&middot; 2D grid with per-block hash and temporal blinking\n'
               '&middot; Inner border: difference of two <code>smoothstep</code>s\n'
               '&middot; Error: horizontal sweep with the click envelope',
    ajustes='&middot; Nº de bloques: el <code>5.0</code> de la rejilla\n'
            '&middot; Parpadeo: el <code>t*3.0</code> del hash temporal\n',
    ajustes_en='&middot; Block count: the <code>5.0</code> grid scale\n'
               '&middot; Blink: the <code>t*3.0</code> temporal hash\n',
    shader=r'''
vec2 bg2 = tuv * vec2(5.0, 4.0);
vec2 idb = floor(bg2);
vec2 fb = fract(bg2);
float existe = step(0.30, hash21(idb + 3.0));
float on = step(0.5, hash21(idb + floor(t * 3.0)));
float caja = smoothstep(0.06, 0.12, fb.x) * smoothstep(0.94, 0.88, fb.x)
           * smoothstep(0.08, 0.16, fb.y) * smoothstep(0.92, 0.84, fb.y);
float interior = smoothstep(0.14, 0.24, fb.x) * smoothstep(0.86, 0.76, fb.x)
               * smoothstep(0.16, 0.26, fb.y) * smoothstep(0.84, 0.74, fb.y);
float marco = caja * (1.0 - interior);
float err = exp(-5.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float barrido = smoothstep(0.12, 0.0, abs(fract(tuv.x - t * 1.2) - 0.5) * 2.0 - 0.88);
vec3 fill = vec3(0.05, 0.02, 0.04);
fill += vec3(1.0, 0.5, 0.75) * caja * existe * on * 0.85;
fill += vec3(1.0, 0.9, 0.95) * marco * existe * 1.1;
fill += vec3(1.0, 0.25, 0.7) * barrido * err * 1.8;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.030, 0.014, 0.026);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.5, 0.8) * rim * (0.5 + err);
col += vec3(1.0, 0.4, 0.75) * ring * 0.5;
'''),

dict(
    nombre='despertar', cat='matrix',
    word='DESPERTAR', word_en='AWAKENING', emoji='\U0001F305',
    titulo='Despertar', titulo_en='Awakening',
    sub='Primera luz', sub_en='First light',
    descr='La palabra se enciende con la primera luz del despertar tras la neblina.',
    descr_en='The word lights up with the first dawn light after the mist.',
    acento='255, 190, 120', bg='#0a0a10', fg='#ffe6c8',
    hint='el raton levanta la niebla &middot; clic para abrir los ojos &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2a2116, #07070c 70%)',
    escena=('halo', '#ffbe78', {'palabra': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'amanece dentro', 'niebla que se retira',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el sol '
          'subir solo. El raton levanta la niebla y el clic abre los ojos de golpe.',
    que_hace='Una luz calida sube por dentro de las letras despues de una neblina que se '
             'retira; el texto parece despertar poco a poco con el amanecer.',
    que_hace_en='A warm light rises inside the letters after a retreating mist; the text seems '
                'to wake up slowly with the sunrise.',
    tecnica='&middot; Gradiente vertical del amanecer modulado por <code>fbm</code> de niebla\n'
            '&middot; Niebla que se disipa: umbral de ruido que sube con el tiempo\n'
            '&middot; Destello del clic: gaussiana sobre el centro con amortiguacion',
    tecnica_en='&middot; Sunrise vertical gradient modulated by <code>fbm</code> mist\n'
               '&middot; Retreating mist: a noise threshold rising over time\n'
               '&middot; Click flash: gaussian over the centre with damping',
    ajustes='&middot; Subida del sol: el <code>t*0.18</code> del gradiente\n'
            '&middot; Densidad de niebla: el <code>2.5</code> de la escala fbm\n',
    ajustes_en='&middot; Sunrise: the <code>t*0.18</code> gradient scroll\n'
               '&middot; Mist density: the <code>2.5</code> fbm scale\n',
    shader=r'''
float niebla = fbm(tuv * 2.5 + vec2(t * 0.15, -t * 0.10));
float retira = smoothstep(0.2, 0.9, tuv.y + t * 0.18 + niebla * 0.6);
float sol = smoothstep(1.0, 0.0, length((tuv - vec2(0.5, 0.1 + fract(t * 0.1) * 0.4))
                    * vec2(1.3, 1.0)));
float abrir = 1.0 - exp(-1.5 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec3 auge = mix(vec3(0.10, 0.10, 0.16), vec3(1.0, 0.75, 0.42), clamp(sol * (0.4 + 0.6 * abrir), 0.0, 1.0));
vec3 fill = mix(auge * 0.35, auge, retira);
fill += vec3(1.0, 0.9, 0.7) * pow(sol, 3.0) * 0.8 * abrir;
fill += vec3(0.9, 0.8, 1.0) * niebla * (1.0 - retira) * 0.25;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = mix(vec3(0.03, 0.03, 0.05), vec3(0.10, 0.07, 0.05), tuv.y * 0.5);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.85, 0.6) * rim * (0.5 + sol);
col += vec3(1.0, 0.8, 0.55) * ring * 0.5;
'''),

dict(
    nombre='vuelo', cat='matrix',
    word='VUELO', word_en='FLIGHT', emoji='\U0001F680',
    titulo='Vuelo', titulo_en='Flight',
    sub='A ras de los tejados', sub_en='Over the rooftops',
    descr='Nubes y estelas cruzan el texto como si volaras por encima de la ciudad.',
    descr_en='Clouds and streaks cross the text as if you flew over the city.',
    acento='150, 210, 255', bg='#050a12', fg='#cfe8ff',
    hint='el raton ala el vuelo &middot; clic para un derrape &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #0d1d33, #03060c 70%)',
    escena=('estelas', '#96d2ff', {'n': 7, 'ang': 8}),
    datos=['GLSL ES 1.00', '1 pasada', 'estelas de nubes', 'derrape del clic',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el vuelo '
          'solo. El raton ala la trayectoria y el clic lanza un derrape.',
    que_hace='Bandas de nube y estelas horizontales cruzan las letras a gran velocidad con '
             'parallax, como volando a ras de los tejados; el clic lanza un derrape lateral.',
    que_hace_en='Bands of cloud and horizontal streaks cross the letters at high speed with '
                'parallax, like flying over the rooftops; the click drifts sideways.',
    tecnica='&middot; Dos capas de <code>fbm</code> con velocidades distintas (parallax)\n'
            '&middot; Estelas: seno horizontal de alta frecuencia atenuado en Y\n'
            '&middot; Derrape: desplazamiento de la UV con envolvente del clic',
    tecnica_en='&middot; Two <code>fbm</code> layers at different speeds (parallax)\n'
               '&middot; Streaks: high frequency horizontal sine attenuated in Y\n'
               '&middot; Drift: UV shift driven by the click envelope',
    ajustes='&middot; Rapidez: el <code>t*0.9</code> de la capa de nubes\n'
            '&middot; Derrape: el <code>0.12</code> del desplazamiento\n',
    ajustes_en='&middot; Speed: the <code>t*0.9</code> cloud scroll\n'
               '&middot; Drift: the <code>0.12</code> shift amount\n',
    shader=r'''
float derr = exp(-3.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec2 uv2 = tuv + vec2(derr * 0.12 * sin(t * 20.0), 0.0);
float capa1 = fbm(vec2(uv2.x * 3.0 - t * 0.9, uv2.y * 6.0));
float capa2 = fbm(vec2(uv2.x * 6.0 - t * 1.8, uv2.y * 9.0 + 3.0));
float estela = 0.5 + 0.5 * sin(uv2.y * 90.0 + t * 6.0);
estela = pow(estela, 8.0) * smoothstep(0.0, 0.35, 1.0 - abs(uv2.y - 0.5) * 2.0);
vec3 fill = mix(vec3(0.10, 0.16, 0.30), vec3(0.75, 0.85, 1.0), capa1 * 0.8);
fill += vec3(0.9, 0.95, 1.0) * capa2 * 0.35;
fill += vec3(1.0) * estela * 0.5;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = mix(vec3(0.02, 0.04, 0.08), vec3(0.05, 0.10, 0.20), capa1);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.7, 0.85, 1.0) * rim * 0.6;
col += vec3(0.6, 0.8, 1.0) * ring * 0.5;
'''),

dict(
    nombre='muelle', cat='matrix',
    word='MUELLE', word_en='DOCK', emoji='⚓',
    titulo='Muelle', titulo_en='Dock',
    sub='Orillas del sistema', sub_en='Shore of the system',
    descr='Oleaje de datos sube y baja por las letras como marea en el muelle.',
    descr_en='Tides of data rise and fall through the letters like a dock tide.',
    acento='90, 190, 255', bg='#030810', fg='#bfe6ff',
    hint='el raton agita la marea &middot; clic para lanzar una ola &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #081a2c, #02050a 70%)',
    escena=('ring', '#5ab4ff', {'n': 3}),
    datos=['GLSL ES 1.00', '1 pasada', 'marea de datos', 'ola del clic',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la marea '
          'subir sola. El raton agita el agua y el clic lanza una ola desde el centro.',
    que_hace='Una marea de bandas oscuras y claras sube y baja por dentro de las letras, con '
             'espuma brillante en la cresta; el clic lanza una ola circular que recorre el texto.',
    que_hace_en='A tide of dark and light bands rises and falls inside the letters, with '
                'bright foam on the crest; the click sends a circular wave across the text.',
    tecnica='&middot; Marea: seno vertical lento con dos armónicos\n'
            '&middot; Espuma: umbral alto del ruido sobre la cresta\n'
            '&middot; Ola: anillo del clic sumado al desplazamiento de la UV',
    tecnica_en='&middot; Tide: slow vertical sine with two harmonics\n'
               '&middot; Foam: high noise threshold on the crest\n'
               '&middot; Wave: the click ring added to the UV displacement',
    ajustes='&middot; Periodo: el <code>t*0.7</code> de la marea\n'
            '&middot; Espuma: baja el umbral <code>0.72</code>\n',
    ajustes_en='&middot; Period: the <code>t*0.7</code> tide\n'
               '&middot; Foam: lower the <code>0.72</code> threshold\n',
    shader=r'''
float marea = sin(tuv.y * 12.0 - t * (0.7 + 0.5 * uAmp))
            + 0.5 * sin(tuv.y * 23.0 - t * 1.4 + 1.0);
float cresta = smoothstep(0.6, 1.4, marea);
float espuma = smoothstep(0.72, 0.95, vnoise(tuv * vec2(40.0, 20.0) + vec2(0.0, -t)))
             * cresta;
float ola = ring;
vec2 uv2 = tuv + vec2(0.0, ola * 0.05);
float m2 = sin(uv2.y * 12.0 - t * (0.7 + 0.5 * uAmp))
         + 0.5 * sin(uv2.y * 23.0 - t * 1.4 + 1.0);
vec3 fill = mix(vec3(0.01, 0.05, 0.10), vec3(0.10, 0.45, 0.70),
                0.5 + 0.5 * sin(m2 * 1.2));
fill += vec3(0.8, 0.95, 1.0) * espuma * 1.3;
fill += vec3(0.4, 0.8, 1.0) * ola * 0.8;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.010, 0.026, 0.045);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.5, 0.8, 1.0) * rim * 0.55;
col += vec3(0.5, 0.8, 1.0) * ring * 0.6;
'''),

# =============================================== MISCELANEA (19) ============
dict(
    nombre='medusa', cat='miscelanea',
    word='MEDUSA', word_en='JELLYFISH', emoji='\U0001FA7A',
    titulo='Medusa', titulo_en='Jellyfish',
    sub='Bioluminiscencia', sub_en='Bioluminescence',
    descr='La medusa respira dentro de las letras con un brillo azul que sube y baja.',
    descr_en='The jellyfish breathes inside the letters with a rising blue glow.',
    acento='110, 190, 255', bg='#02060e', fg='#bfe0ff',
    hint='el raton acaricia la medusa &middot; clic para un latido fuerte &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #071730, #02050c 70%)',
    escena=('halo', '#6ec2ff', {'palabra': False}),
    datos=['GLSL ES 1.00', '1 pasada', 'campana pulsante', 'brillo frio',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la medusa '
          'respirar sola. El raton la acaricia y el clic fuerza un latido fuerte.',
    que_hace='Una campana de luz azul se contrae y se relaja dentro del texto como una medusa '
             'nadando, con filamentos suaves que ondean bajo ella.',
    que_hace_en='A bell of blue light contracts and relaxes inside the text like a swimming '
                'jellyfish, with soft filaments waving beneath it.',
    tecnica='&middot; Radio eliptico con contraccion periodica (la campana)\n'
            '&middot; Filamentos: senos verticales con desfase por columna\n'
            '&middot; Brillo: gaussiana central modulada por el pulso',
    tecnica_en='&middot; Elliptic radius with periodic contraction (the bell)\n'
               '&middot; Filaments: vertical sines phase-shifted per column\n'
               '&middot; Glow: central gaussian modulated by the pulse',
    ajustes='&middot; Respiracion: el <code>t*2.2</code> del pulso\n'
            '&middot; Nº de filamentos: el <code>14.0</code> del seno\n',
    ajustes_en='&middot; Breathing: the <code>t*2.2</code> pulse\n'
               '&middot; Filament count: the <code>14.0</code> sine\n',
    shader=r'''
float pulso = 0.5 + 0.5 * sin(t * 2.2);
float golpe = exp(-4.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec2 k = uPlane / min(uPlane.x, uPlane.y);
vec2 cc = (tuv - vec2(0.5, 0.42)) * k;
float campana = smoothstep(0.45 + 0.06 * pulso, 0.30 + 0.06 * pulso, length(cc));
float fil = sin(tuv.x * 14.0 + sin(tuv.y * 6.0 + t * 1.6) * 1.6);
fil = smoothstep(0.7, 1.0, abs(fil)) * smoothstep(0.9, 0.45, tuv.y);
float halo = exp(-6.0 * length(cc));
vec3 fill = vec3(0.01, 0.03, 0.07)
          + vec3(0.30, 0.65, 1.0) * campana * (0.55 + 0.6 * pulso + 1.4 * golpe)
          + vec3(0.45, 0.85, 1.0) * fil * 0.7
          + vec3(0.25, 0.5, 1.0) * halo * 0.5;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.006, 0.016, 0.038);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.5, 0.8, 1.0) * rim * 0.55;
col += vec3(0.4, 0.7, 1.0) * ring * 0.6;
'''),

dict(
    nombre='coral', cat='miscelanea',
    word='CORAL', word_en='CORAL', emoji='\U0001FAB8',
    titulo='Coral', titulo_en='Coral',
    sub='Arrecife que crece', sub_en='Growing reef',
    descr='Bifurcaciones de coral trepan por las letras con zooides que parpadean.',
    descr_en='Coral branches climb the letters with blinking polyps.',
    acento='255, 130, 110', bg='#0d0406', fg='#ffc9be',
    hint='el raton alimenta el arrecife &middot; clic para florecer &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2c0d10, #0b0305 70%)',
    escena=('chispas', '#ff8268', {'n': 12, 'up': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'bifurcaciones', 'zooides que laten',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el coral '
          'crecer solo. El raton lo alimenta y el clic hace florecer todos los zooides.',
    que_hace='Ramas de coral trepan por el texto siguiendo ruido de difusión y sus zooides '
             'florecen en secuencia con un punteo cálido naranja y rosa.',
    que_hace_en='Coral branches climb the text following diffusion noise and their polyps '
                'bloom in sequence with warm orange and pink speckle.',
    tecnica='&middot; Rama: <code>fbm</code> con umbral estrecho = lineas de crecimiento\n'
            '&middot; Zooides: hash por celda con retardo en el tiempo\n'
            '&middot; Floracion del clic: envolvente que sube el umbral global',
    tecnica_en='&middot; Branch: <code>fbm</code> with a narrow threshold = growth lines\n'
               '&middot; Polyps: per-cell hash with time delay\n'
               '&middot; Click bloom: envelope raising the global threshold',
    ajustes='&middot; Estrechez de la rama: el rango <code>0.46, 0.54</code>\n'
            '&middot; Nº de zooides: el <code>22.0</code> de la rejilla\n',
    ajustes_en='&middot; Branch thinness: the <code>0.46, 0.54</code> range\n'
               '&middot; Polyp count: the <code>22.0</code> grid\n',
    shader=r'''
float rama = fbm(tuv * 4.0 + vec2(0.0, -t * 0.05));
float linea = smoothstep(0.46, 0.50, rama) * smoothstep(0.58, 0.54, rama);
float flor = exp(-3.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec2 zc = tuv * (uPlane / min(uPlane.x, uPlane.y)) * 22.0;
float zoide = step(0.62, hash21(floor(zc)) + flor * 0.6);
float lat = 0.5 + 0.5 * sin(t * 3.0 + hash21(floor(zc) + 5.0) * 6.2831);
float punto = smoothstep(0.36, 0.30, length(fract(zc) - 0.5)) * zoide;
vec3 fill = vec3(0.05, 0.015, 0.02)
          + vec3(1.0, 0.45, 0.35) * linea * 1.3
          + vec3(1.0, 0.75, 0.45) * punto * lat * 1.4;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.030, 0.010, 0.016);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.6, 0.5) * rim * 0.6;
col += vec3(1.0, 0.55, 0.45) * ring * 0.5;
'''),

dict(
    nombre='humo', cat='miscelanea',
    word='HUMO', word_en='SMOKE', emoji='\U0001F4A8',
    titulo='Humo', titulo_en='Smoke',
    sub='Remolinos etereos', sub_en='Ethereal wisps',
    descr='Cintas de humo se enroscan dentro de las letras y se dispersan al tacto.',
    descr_en='Ribbons of smoke curl inside the letters and disperse on touch.',
    acento='190, 190, 210', bg='#08080a', fg='#dcdce6',
    hint='el raton sopla el humo &middot; clic para un remolinon &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #1d1d24, #07070a 70%)',
    escena=('chispas', '#c6c6d6', {'n': 12, 'up': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'cintas de humo', 'remolinon del clic',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el humo '
          'subir solo. El raton sopla las cintas y el clic abre un gran remolinon.',
    que_hace='Cintas de humo gris se enroscan y suben dentro del texto con turbulencia, '
             'diluyendose arriba; el raton las empuja y el clic abre un remolinon nuevo.',
    que_hace_en='Grey smoke ribbons curl and rise inside the text with turbulence, dissolving '
                'at the top; the mouse pushes them and the click opens a new swirl.',
    tecnica='&middot; Turbulencia: <code>fbm3</code> con dominio desplazado en Y\n'
            '&middot; Densidad: umbral suave del ruido multiplicado por la máscara\n'
            '&middot; Remolinon: giro de la UV alrededor del punto del clic',
    tecnica_en='&middot; Turbulence: <code>fbm3</code> with Y-shifted domain\n'
               '&middot; Density: soft noise threshold multiplied by the mask\n'
               '&middot; Swirl: UV rotation around the click point',
    ajustes='&middot; Ascenso: el <code>-t*0.35</code> del dominio\n'
            '&middot; Escala del humo: el <code>3.0</code> del fbm\n',
    ajustes_en='&middot; Rise: the <code>-t*0.35</code> domain scroll\n'
               '&middot; Smoke scale: the <code>3.0</code> fbm scale\n',
    shader=r'''
float remo = exp(-2.5 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec2 dc = tuv - (0.5 + uClickPos * 0.5);
float an = remo * 3.0 * exp(-8.0 * length(dc));
vec2 uv2 = tuv + vec2(-dc.y, dc.x) * an;
float h = fbm3(vec2(uv2.x * 3.0 + sin(uv2.y * 4.0 + t * 0.6) * 0.4,
                    uv2.y * 3.0 - t * 0.35));
float dens = smoothstep(0.35, 0.85, h);
vec3 fill = mix(vec3(0.05, 0.05, 0.07), vec3(0.78, 0.78, 0.86), dens);
fill += vec3(0.9, 0.9, 1.0) * pow(dens, 3.0) * 0.5;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.024, 0.024, 0.030);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.8, 0.8, 0.9) * rim * 0.5;
col += vec3(0.7, 0.7, 0.85) * ring * 0.5;
'''),

dict(
    nombre='escarcha', cat='miscelanea',
    word='ESCARCHA', word_en='FROST', emoji='❄️',
    titulo='Escarcha', titulo_en='Frost',
    sub='Cristales que trepan', sub_en='Climbing crystals',
    descr='Cristales de escarcha trepan por el contorno de las letras desde los bordes.',
    descr_en='Frost crystals climb the outline of the letters from the edges.',
    acento='200, 240, 255', bg='#040810', fg='#dff4ff',
    hint='el raton congela el cristal &middot; clic para que crezca toda la escarcha &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #0d1e2e, #03060c 70%)',
    escena=('ring', '#c4ecff', {'n': 4}),
    datos=['GLSL ES 1.00', '1 pasada', 'cristales ramificados', 'escarcha viva',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la escarcha '
          'trepar sola. El raton la congela y el clic hace crecer todos los cristales.',
    que_hace='Agujas de escarcha crecen desde el borde de cada letra hacia dentro, con un '
             'brillo de esquirlas que parpadea; el clic acelera el crecimiento completo.',
    que_hace_en='Frost needles grow from the edge of every letter inward, with a sparkling '
                'glint; the click speeds up the full growth.',
    tecnica='&middot; Crecimiento: distancia al borde de la máscara contra el tiempo\n'
            '&middot; Agujas: ruido de alta frecuencia cortado en cuña\n'
            '&middot; Chispa: hash temporal con <code>pow</code> agudo',
    tecnica_en='&middot; Growth: distance to the mask edge against time\n'
               '&middot; Needles: high frequency noise cut into wedges\n'
               '&middot; Sparkle: temporal hash sharpened with <code>pow</code>',
    ajustes='&middot; Velocidad de crecimiento: el <code>t*0.25</code>\n'
            '&middot; Densidad de agujas: el <code>40.0</code> de la escala\n',
    ajustes_en='&middot; Growth speed: the <code>t*0.25</code>\n'
               '&middot; Needle density: the <code>40.0</code> scale\n',
    shader=r'''
float borde = clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0);
float crece = fract(t * 0.25 + uAmp * 0.3);
float flor = exp(-2.5 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float nivel = min(1.0, crece + flor);
float ang = atan(fract(hb * 6.0) - 0.5, fract(mask * 7.0) - 0.5);
float aguja = 0.5 + 0.5 * sin(ang * 24.0 + hash21(floor(tuv * 40.0)) * 6.2831);
aguja = smoothstep(0.75, 1.0, aguja);
float cristal = smoothstep(nivel, nivel - 0.25, 1.0 - borde) * aguja * mask;
float chispa = pow(hash21(floor(tuv * 40.0) + floor(t * 8.0)), 24.0);
vec3 fill = vec3(0.03, 0.06, 0.10)
          + vec3(0.75, 0.92, 1.0) * cristal * 1.5
          + vec3(1.0) * chispa * mask * 1.6;
vec3 bgc = vec3(0.014, 0.026, 0.045);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.8, 0.95, 1.0) * borde * 0.8;
col += vec3(0.7, 0.9, 1.0) * ring * 0.5;
'''),

dict(
    nombre='prisma', cat='miscelanea',
    word='PRISMA', word_en='PRISM', emoji='🔺',
    titulo='Prisma', titulo_en='Prism',
    sub='Espectro que gira', sub_en='Spinning spectrum',
    descr='Un espectro giratorio refracta la palabra en todos los colores del arcoiris.',
    descr_en='A spinning spectrum refracts the word into rainbow colours.',
    acento='255, 255, 255', bg='#06060a', fg='#f2f2ff',
    hint='el raton gira el prisma &middot; clic para dispersar el espectro &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #191a26, #05050a 70%)',
    escena=('rayos', '#ff9ecf', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'dispersion espectral', 'giro del raton',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el espectro '
          'girar solo. El raton gira el prisma y el clic dispersa todos los colores.',
    que_hace='Un abanico de colores gira dentro de las letras como luz atravesando un prisma, '
             'descomponiendose en bandas espectrales que barren la palabra.',
    que_hace_en='A fan of colour spins inside the letters like light through a prism, breaking '
                'into spectral bands that sweep across the word.',
    tecnica='&middot; HSV a RGB: angulo del raton + tiempo dentro del hue\n'
            '&middot; Bandas: seno de alta frecuencia sobre el angulo\n'
            '&middot; Dispersion del clic: ampliacion temporal del rango de tono',
    tecnica_en='&middot; HSV to RGB: mouse angle plus time across the hue\n'
               '&middot; Bands: high frequency sine over the angle\n'
               '&middot; Click dispersion: temporary widening of the hue range',
    ajustes='&middot; Nº de bandas: el <code>24.0</code> del seno\n'
            '&middot; Rapidez de giro: el <code>t*0.5</code> del tono\n',
    ajustes_en='&middot; Band count: the <code>24.0</code> sine\n'
               '&middot; Spin speed: the <code>t*0.5</code> hue drive\n',
    shader=r'''
float disp = exp(-2.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec2 kp = uPlane / min(uPlane.x, uPlane.y);
float ang = atan((tuv.y - 0.5) * kp.y, (tuv.x - 0.5) * kp.x);
float hue = ang / 6.2831 + t * 0.5 + uMouse.x * uAmp;
vec3 espe = 0.5 + 0.5 * cos(6.2831 * (hue + vec3(0.0, 0.33, 0.67)));
float bandas = 0.5 + 0.5 * sin(ang * 24.0 + t * 3.0);
vec3 fill = mix(espe * 0.85, vec3(1.0), 0.15);
fill *= 0.55 + 0.45 * bandas;
fill += espe * disp * 0.8;
float brillo = pow(1.0 - abs(2.0 * hb - 1.0), 2.0);
fill += vec3(1.0) * brillo * 0.15;
vec3 bgc = vec3(0.020, 0.020, 0.030);
vec3 col = mix(bgc, fill, mask);
col += espe * pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5) * 0.9;
col += espe * ring * 0.7;
'''),

dict(
    nombre='abismo', cat='miscelanea',
    word='ABISMO', word_en='ABYSS', emoji='\U0001F30A',
    titulo='Abismo', titulo_en='Abyss',
    sub='Fondo marino', sub_en='Seabed',
    descr='Presion y oscuridad envuelven el texto con motas que suben desde el fondo.',
    descr_en='Pressure and darkness wrap the text with motes rising from below.',
    acento='70, 140, 255', bg='#01040a', fg='#a9c8ff',
    hint='el raton enciende la linterna &middot; clic para subir una burbuja &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #041229, #01040a 70%)',
    escena=('chispas', '#468cff', {'n': 14, 'up': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'mota marina', 'presion profunda',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja las motas '
          'subir solas. El raton enciende la linterna y el clic sube una burbuja.',
    que_hace='El texto vive en el fondo marino: un gradiente de presion oscurece las letras y '
             'motonas brillantes suben despacio; la linterna del raton revela el color real.',
    que_hace_en='The text lives on the seabed: a pressure gradient darkens the letters and '
                'glowing motes drift upward; the mouse lantern reveals the true colour.',
    tecnica='&middot; Gradiente vertical de presion multiplicado por la altura\n'
            '&middot; Motas: hash por celda con velocidad vertical aleatoria\n'
            '&middot; Lantern: gaussiana alrededor de <code>uMouse</code>',
    tecnica_en='&middot; Vertical pressure gradient multiplied by depth\n'
               '&middot; Motes: per-cell hash with random vertical speed\n'
               '&middot; Lantern: gaussian around <code>uMouse</code>',
    ajustes='&middot; Nº de motas: el <code>28.0</code> de la rejilla\n'
            '&middot; Oscuridad: el <code>0.55</code> del gradiente\n',
    ajustes_en='&middot; Mote count: the <code>28.0</code> grid\n'
               '&middot; Darkness: the <code>0.55</code> gradient depth\n',
    shader=r'''
float presion = mix(1.0, 0.35, smoothstep(0.0, 1.0, tuv.y));
vec2 mc = tuv * 28.0;
float vel = 0.2 + 0.5 * hash21(floor(mc));
float mota = smoothstep(0.90, 0.97,
            hash21(floor(mc) + floor(vec2(0.0, (t * vel)))));
mota *= 0.5 + 0.5 * sin(t * 3.0 + hash21(floor(mc)) * 6.2831);
float lint = exp(-10.0 * length(tuv - (0.5 + uMouse * 0.5)));
float burbuja = exp(-6.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT)
              * smoothstep(0.4, 0.0, abs(fract(tuv.x - uClickPos.x * 0.5) - 0.5) * 2.0 - 0.85);
vec3 base = mix(vec3(0.02, 0.10, 0.22), vec3(0.005, 0.02, 0.06), tuv.y);
vec3 fill = base * presion
          + vec3(0.55, 0.8, 1.0) * mota * (0.6 + 2.0 * lint)
          + vec3(0.6, 0.85, 1.0) * burbuja;
fill += vec3(0.3, 0.5, 1.0) * lint * 0.35;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.004, 0.012, 0.032);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.4, 0.6, 1.0) * rim * (0.4 + lint);
col += vec3(0.4, 0.7, 1.0) * ring * 0.5;
'''),

dict(
    nombre='latido', cat='miscelanea',
    word='LATIDO', word_en='HEARTBEAT', emoji='\U0001F493',
    titulo='Latido', titulo_en='Heartbeat',
    sub='Pulso que bombea', sub_en='Pumping pulse',
    descr='El corazon late dentro de las letras con un brillo rojo que se expande.',
    descr_en='The heart beats inside the letters with an expanding red glow.',
    acento='255, 90, 110', bg='#0c0205', fg='#ffc2c9',
    hint='el raton acelera el corazon &middot; clic para un latido doble &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2b0710, #0a0204 70%)',
    escena=('halo', '#ff5a6e', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'pulso sistolico', 'brillo que bombea',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el corazon '
          'latir solo. El raton lo acelera y el clic fuerza un latido doble.',
    que_hace='Un pulso sistolico recorre las letras con doble golpe clasico, expandiendo un '
             'brillo rojo desde el centro del texto y devolviendolo a la calma.',
    que_hace_en='A systolic pulse crosses the letters with the classic double beat, expanding '
                'a red glow from the text centre and settling back to calm.',
    tecnica='&middot; Funcion de golpe: dos gaussianas temporales desfasadas\n'
            '&middot; Expansion: radio del brillo ligado a la amplitud del golpe\n'
            '&middot; Frecuencia modulada por <code>uAmp</code> del raton',
    tecnica_en='&middot; Beat function: two time-shifted gaussians\n'
               '&middot; Expansion: glow radius tied to the beat amplitude\n'
               '&middot; Rate modulated by the mouse <code>uAmp</code>',
    ajustes='&middot; Frecuencia: el <code>1.1</code> de la funcion de golpe\n'
            '&middot; Fuerza: el <code>0.62</code> de la gaussiana secundaria\n',
    ajustes_en='&middot; Rate: the <code>1.1</code> beat drive\n'
               '&middot; Strength: the <code>0.62</code> secondary gaussian\n',
    shader=r'''
float f = fract(t * (0.9 + 0.9 * uAmp));
float golpe1 = exp(-30.0 * pow(f - 0.12, 2.0));
float golpe2 = 0.62 * exp(-30.0 * pow(f - 0.34, 2.0));
float golpe3 = exp(-30.0 * pow(f - 0.62, 2.0)) * step(-9000.0, uClickT)
             * exp(-1.5 * max(t - uClickT, 0.0));
float amp = golpe1 + golpe2 + golpe3;
float rr = length((tuv - vec2(0.5, 0.5)) * (uPlane / min(uPlane.x, uPlane.y)));
float halo = exp(-7.0 * rr) * amp;
vec3 fill = vec3(0.10, 0.015, 0.03) * (0.6 + amp)
          + vec3(1.0, 0.20, 0.30) * amp * (0.8 + 0.6 * (1.0 - rr));
fill += vec3(1.0, 0.5, 0.55) * halo * 0.9;
float eco = smoothstep(0.9, 1.0, sin(rr * 30.0 - t * 6.0)) * amp;
fill += vec3(1.0, 0.3, 0.4) * eco * 0.5;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.035, 0.008, 0.014);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.4, 0.5) * rim * (0.4 + amp);
col += vec3(1.0, 0.3, 0.4) * ring * 0.5;
'''),

dict(
    nombre='laberinto', cat='miscelanea',
    word='LABERINTO', word_en='MAZE', emoji='\U0001F9ED',
    titulo='Laberinto', titulo_en='Maze',
    sub='Paredes que giran', sub_en='Turning walls',
    descr='Paredes de laberinto se giran dentro de las letras buscando la salida.',
    descr_en='Maze walls turn inside the letters looking for the way out.',
    acento='255, 200, 90', bg='#0b0803', fg='#ffe6b0',
    hint='el raton empuja una pared &middot; clic para girar todo el laberinto &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #241b06, #080602 70%)',
    escena=('malla', '#ffc85a', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'paredes giratorias', 'giro del clic',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja las paredes '
          'girar solas. El raton empuja una pared y el clic gira todo el laberinto.',
    que_hace='Paredes cuadradas se giran 90 grados por tandas dentro del texto como un '
             'laberinto mecanico, con una luz que recorre los pasillos buscando la salida.',
    que_hace_en='Square walls rotate 90 degrees in batches inside the text like a mechanical '
                'maze, with a light running the corridors looking for the exit.',
    tecnica='&middot; Rejilla con paredes por lado y fase temporal por celda\n'
            '&middot; Giro: <code>floor(t)</code> con mezcla de angulo continuo\n'
            '&middot; Luz: gaussiana que sigue al raton por los pasillos',
    tecnica_en='&middot; Grid with per-side walls and per-cell time phase\n'
               '&middot; Turn: <code>floor(t)</code> blended with a continuous angle\n'
               '&middot; Light: gaussian following the mouse along the corridors',
    ajustes='&middot; Tamaño de celda: el <code>7.0</code> de la rejilla\n'
            '&middot; Cadencia: el <code>0.5</code> del giro temporal\n',
    ajustes_en='&middot; Cell size: the <code>7.0</code> grid scale\n'
               '&middot; Cadence: the <code>0.5</code> temporal turn\n',
    shader=r'''
vec2 g = tuv * (uPlane / min(uPlane.x, uPlane.y)) * 7.0;
vec2 id2 = floor(g);
vec2 f2 = fract(g);
float fase = hash21(id2) * 6.2831 + floor(t * 0.5 + hash21(id2 + 2.0)) * 1.5708;
float c = cos(fase), s = sin(fase);
vec2 r2 = vec2(f2.x * c - f2.y * s, f2.x * s + f2.y * c) + 0.5;
float paredX = smoothstep(0.10, 0.04, abs(fract(r2.x * 1.0 + 0.5) - 0.5));
float paredY = smoothstep(0.10, 0.04, abs(fract(r2.y * 1.0 + 0.5) - 0.5));
float pasillo = max(paredX, paredY);
float luz = exp(-9.0 * length(tuv - (0.5 + uMouse * 0.5)));
vec3 fill = vec3(0.05, 0.035, 0.01)
          + vec3(1.0, 0.80, 0.35) * pasillo * (0.5 + luz * 1.6)
          + vec3(1.0, 0.9, 0.6) * luz * 0.25;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.030, 0.022, 0.008);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.8, 0.4) * rim * 0.55;
col += vec3(1.0, 0.75, 0.3) * ring * 0.5;
'''),

dict(
    nombre='cometa', cat='miscelanea',
    word='COMETA', word_en='COMET', emoji='☄️',
    titulo='Cometa', titulo_en='Comet',
    sub='Estela de fuego', sub_en='Fiery trail',
    descr='Un cometa cruza el texto dejando una estela de fuego que se apaga detras.',
    descr_en='A comet crosses the text leaving a fiery trail that fades behind it.',
    acento='255, 170, 80', bg='#060409', fg='#ffd9ad',
    hint='el raton aparta el cometa &middot; clic para encender la estela &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #201207, #05040a 70%)',
    escena=('estelas', '#ffaa50', {'n': 5, 'ang': 35}),
    datos=['GLSL ES 1.00', '1 pasada', 'cabeza incandescente', 'estela que se apaga',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el cometa '
          'vagar solo. El raton lo aparta y el clic enciende la estela.',
    que_hace='Un cometa con cabeza incandescente cruza las letras en diagonal y su estela de '
             'fuego se apaga detras, sembrando chispas que se desvanecen.',
    que_hace_en='A comet with an incandescent head crosses the letters diagonally and its '
                'fiery trail fades behind, sowing sparks that vanish.',
    tecnica='&middot; Posicion: <code>fract</code> del tiempo en diagonal\n'
            '&middot; Estela: distancia a la trayectoria con caida exponencial\n'
            '&middot; Chispas: hash temporal atenuado por la distancia',
    tecnica_en='&middot; Position: time <code>fract</code> along the diagonal\n'
               '&middot; Trail: distance to the path with exponential falloff\n'
               '&middot; Sparks: temporal hash attenuated by distance',
    ajustes='&middot; Nº de pasadas: el <code>0.13</code> de la velocidad\n'
            '&middot; Largo de estela: el <code>4.0</code> del decaimiento\n',
    ajustes_en='&middot; Pass count: the <code>0.13</code> speed\n'
               '&middot; Trail length: the <code>4.0</code> falloff\n',
    shader=r'''
float enciende = 1.0 + 2.0 * exp(-2.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float paso = fract(t * 0.13);
vec2 pos = mix(vec2(-0.1, 1.1), vec2(1.1, -0.1), paso);
vec2 k = uPlane / min(uPlane.x, uPlane.y);
vec2 dv = (tuv - pos) * k;
float dHead = length(dv);
float cabeza = exp(-90.0 * dHead * dHead) + 0.5 * exp(-250.0 * dHead * dHead);
float dTr = abs(dv.x + dv.y) * 0.7071;
float atras = clamp(-(dv.x - dv.y) * 0.7071, 0.0, 1.0);
float estela = exp(-18.0 * dTr) * exp(-3.0 * atras) * enciende;
float chis = pow(hash21(floor(tuv * 60.0) + floor(t * 12.0)), 18.0) * estela;
vec3 fill = vec3(0.03, 0.02, 0.05)
          + vec3(1.0, 0.55, 0.15) * estela * 1.2
          + vec3(1.0, 0.9, 0.7) * cabeza * 1.8
          + vec3(1.0, 0.8, 0.5) * chis * 2.0;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.022, 0.014, 0.032);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.7, 0.4) * rim * (0.4 + estela);
col += vec3(1.0, 0.6, 0.3) * ring * 0.5;
'''),

dict(
    nombre='singularidad', cat='miscelanea',
    word='SINGULARIDAD', word_en='SINGULARITY', emoji='\U0001F539',
    titulo='Singularidad', titulo_en='Singularity',
    sub='Lente gravitatoria', sub_en='Gravitational lens',
    descr='El texto se curva alrededor de un punto que traga la luz como un agujero negro.',
    descr_en='The text bends around a point that swallows light like a black hole.',
    acento='190, 120, 255', bg='#050308', fg='#e3ccff',
    hint='el raton mueve la singularidad &middot; clic para intensificar la atraccion &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #180c26, #040208 70%)',
    escena=('ring', '#be78ff', {'n': 4}),
    datos=['GLSL ES 1.00', '1 pasada', 'distorsion gravitatoria', 'horizonte negro',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja girar la '
          'singularidad sola. El raton la mueve y el clic intensifica la atraccion.',
    que_hace='Un punto negro en el centro curva la imagen de las letras a su alrededor, como '
             'luz doblada por la gravedad, con un disco de acrecion que gira a su alrededor.',
    que_hace_en='A black point at the centre bends the image of the letters around it, like '
                'light bent by gravity, with an accretion disc spinning around it.',
    tecnica='&middot; Distorsion: la UV se desplaza hacia el centro con <code>1/d</code>\n'
            '&middot; Disco: anillo eliptico con color rotando por <code>atan</code>\n'
            '&middot; Horizonte: negro puro dentro del radio critico',
    tecnica_en='&middot; Distortion: UV shifted toward the centre with <code>1/d</code>\n'
               '&middot; Disc: elliptic ring coloured by <code>atan</code>\n'
               '&middot; Horizon: pure black inside the critical radius',
    ajustes='&middot; Fuerza: el <code>0.06</code> del desplazamiento\n'
            '&middot; Radio del horizonte: el <code>0.05</code>\n',
    ajustes_en='&middot; Strength: the <code>0.06</code> shift\n'
               '&middot; Horizon radius: the <code>0.05</code>\n',
    shader=r'''
vec2 centro = 0.5 + uMouse * 0.35 * uAmp + vec2(0.06 * sin(t * 0.7), 0.05 * cos(t * 0.9));
vec2 kas = uPlane / min(uPlane.x, uPlane.y);
vec2 dd = (tuv - centro) * kas;
float d = length(dd) + 1e-4;
float fuerza = 0.06 * (1.0 + 2.5 * exp(-3.0 * max(t - uClickT, 0.0))
             * step(-9000.0, uClickT));
vec2 uv2 = centro + (dd / kas) * (1.0 + fuerza / d);
float m2 = maskAt(uv2);
float h2 = blurAt(uv2);
float disco = smoothstep(0.11, 0.075, d) * smoothstep(0.045, 0.065, d);
float rot = atan(dd.y, dd.x) + t * 2.0;
vec3 dcolor = 0.5 + 0.5 * cos(rot + vec3(0.0, 2.1, 4.2));
float horizonte = smoothstep(0.052, 0.042, d);
vec3 fill = mix(vec3(0.04, 0.02, 0.07), vec3(0.55, 0.30, 0.9), m2 * 0.9);
fill += dcolor * disco * 1.6;
fill = mix(fill, vec3(0.0), horizonte);
vec3 bgc = vec3(0.020, 0.012, 0.036);
vec3 col = mix(bgc, fill, m2);
col += vec3(0.7, 0.5, 1.0) * pow(clamp(h2 * (1.0 - h2) * 4.0, 0.0, 1.0), 1.5) * 0.6;
col += vec3(0.7, 0.5, 1.0) * ring * 0.5;
'''),

dict(
    nombre='aura', cat='miscelanea',
    word='AURA', word_en='AURA', emoji='\U0001F52E',
    titulo='Aura', titulo_en='Aura',
    sub='Campo que respira', sub_en='Breathing field',
    descr='Un campo de luz que respira envuelve las letras y cambia de color lentamente.',
    descr_en='A breathing field of light wraps the letters and slowly shifts colour.',
    acento='220, 150, 255', bg='#07040c', fg='#eed9ff',
    hint='el raton carga el aura &middot; clic para expandir el campo &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #1e0f2e, #06030b 70%)',
    escena=('halo', '#dc96ff', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'campo que respira', 'cambio de tono',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja el aura '
          'respirar sola. El raton carga el campo y el clic lo expande de golpe.',
    que_hace='Un halo de luz serena rodea y atraviesa las letras, respirando con un pulso '
             'lento mientras deriva por toda la rueda de colores.',
    que_hace_en='A serene halo of light surrounds and passes through the letters, breathing '
                'with a slow pulse while drifting around the colour wheel.',
    tecnica='&middot; Halo: gaussiana sobre la distancia a la máscara difuminada\n'
            '&middot; Respiracion: seno lento que modula intensidad y radio\n'
            '&middot; Deriva de tono: tiempo dentro del coseno RGB',
    tecnica_en='&middot; Halo: gaussian over distance to the blurred mask\n'
               '&middot; Breathing: slow sine modulating intensity and radius\n'
               '&middot; Hue drift: time across the RGB cosine',
    ajustes='&middot; Respiracion: el <code>t*0.8</code> del pulso\n'
            '&middot; Anchura: el <code>6.0</code> de la gaussiana\n',
    ajustes_en='&middot; Breathing: the <code>t*0.8</code> pulse\n'
               '&middot; Width: the <code>6.0</code> gaussian\n',
    shader=r'''
float respira = 0.5 + 0.5 * sin(t * 0.8);
float expand = exp(-2.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float carga = 1.0 + 1.2 * uAmp;
vec3 tono = 0.5 + 0.5 * cos(6.2831 * (t * 0.06 + vec3(0.0, 0.33, 0.67)));
float halo = exp(-(6.0 - 2.0 * expand) * abs(1.0 - hb * 2.0));
float pulso = respira * carga * (1.0 + expand);
vec3 fill = vec3(0.04, 0.02, 0.07)
          + tono * halo * (0.5 + 0.7 * pulso)
          + tono * mask * (0.30 + 0.35 * pulso);
float onda = smoothstep(0.9, 1.0, sin(abs(1.0 - hb * 2.0) * 14.0 - t * 3.0));
fill += tono * onda * 0.25 * pulso;
vec3 bgc = mix(vec3(0.024, 0.014, 0.040), tono * 0.10, 0.5 + 0.5 * sin(t * 0.4));
vec3 col = mix(bgc, fill, max(mask, halo * 0.7));
col += tono * ring * 0.6;
col += tono * pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5) * 0.7;
'''),

dict(
    nombre='melodia', cat='miscelanea',
    word='MELODIA', word_en='MELODY', emoji='\U0001F3B5',
    titulo='Melodia', titulo_en='Melody',
    sub='Ondas sonoras', sub_en='Sound waves',
    descr='Ondas de sonido recorren las letras como si la palabra fuera una cancion.',
    descr_en='Sound waves run through the letters as if the word were a song.',
    acento='255, 160, 220', bg='#0b0410', fg='#ffd4ee',
    hint='el raton cambia la tonada &middot; clic para un acorde &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2a0c22, #08030c 70%)',
    escena=('estelas', '#ffa0dc', {'n': 5, 'ang': 45}),
    datos=['GLSL ES 1.00', '1 pasada', 'onda senoidal', 'acorde del clic',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la tonada '
          'sonar sola. El raton cambia la melodía y el clic toca un acorde.',
    que_hace='Varias ondas senoidales de distinta frecuencia se superponen dentro del texto '
             'como notas de una melodía, dejando estelas de color donde coinciden.',
    que_hace_en='Several sines of different frequency overlap inside the text like notes of a '
                'melody, leaving colour trails where they meet.',
    tecnica='&middot; Suma de tres senos con frecuencias primas entre si\n'
            '&middot; Color: producto de las ondas mapeado a RGB\n'
            '&middot; Acordo: el clic añade una cuarta onda con envolvente',
    tecnica_en='&middot; Sum of three sines at mutually prime frequencies\n'
               '&middot; Colour: the wave product mapped to RGB\n'
               '&middot; Chord: the click adds a fourth enveloped wave',
    ajustes='&middot; Nº de notas: añade otro seno al sumatorio\n'
            '&middot; Tempo: multiplica <code>t</code> por mas de <code>2.0</code>\n',
    ajustes_en='&middot; Note count: add another sine to the sum\n'
               '&middot; Tempo: multiply <code>t</code> by more than <code>2.0</code>\n',
    shader=r'''
float o1 = sin(tuv.x * 18.0 - t * 3.0);
float o2 = sin(tuv.x * 27.0 - t * 4.5 + 1.7);
float o3 = sin(tuv.x * 33.0 - t * 6.0 + 3.4);
float acorde = exp(-2.5 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
float o4 = sin(tuv.x * 45.0 - t * 9.0) * acorde;
float suma = (o1 + o2 + o3 + o4) / 3.0;
float banda = 0.5 + 0.5 * sin(tuv.y * 60.0 + suma * 6.0 + t * 2.0);
vec3 tono = vec3(1.0, 0.45, 0.75) * (0.5 + 0.5 * o1)
          + vec3(0.45, 0.65, 1.0) * (0.5 + 0.5 * o2)
          + vec3(1.0, 0.85, 0.4) * (0.5 + 0.5 * o3);
vec3 fill = vec3(0.05, 0.02, 0.06) + tono * banda * 0.55;
fill += vec3(1.0) * pow(abs(suma), 6.0) * 0.35;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.030, 0.012, 0.036);
vec3 col = mix(bgc, fill, mask);
col += tono * 0.5 * rim;
col += vec3(1.0, 0.6, 0.85) * ring * 0.5;
'''),

dict(
    nombre='burbuja', cat='miscelanea',
    word='BURBUJA', word_en='BUBBLE', emoji='\U0001FAE7',
    titulo='Burbuja', titulo_en='Bubble',
    sub='Jabon que sube', sub_en='Rising soap',
    descr='Burbujas de jabon suben dentro de las letras con irisaciones que giran.',
    descr_en='Soap bubbles rise inside the letters with spinning iridescence.',
    acento='150, 230, 255', bg='#03080c', fg='#cdf3ff',
    hint='el raton revienta burbujas &middot; clic para llenar de burbujas &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #0a1e26, #02060a 70%)',
    escena=('chispas', '#96e6ff', {'n': 16, 'up': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'irisaciones girando', 'revienta con el raton',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja subir las '
          'burbujas solas. El raton las revienta y el clic las llena todas.',
    que_hace='Burbujas esfericas suben por dentro del texto con una pelicula irisada que gira '
             'y estalla al pasar el raton, dejando un aro breve.',
    que_hace_en='Spherical bubbles rise inside the text with a spinning iridescent film that '
                'pops as the mouse passes, leaving a brief ring.',
    tecnica='&middot; Rejilla de burbujas con deriva vertical y hash por celda\n'
            '&middot; Irisacion: coseno de la distancia con desfase RGB\n'
            '&middot; Reventon: gaussiana alrededor del raton sobre la burbuja',
    tecnica_en='&middot; Bubble grid with vertical drift and per-cell hash\n'
               '&middot; Iridescence: cosine of distance with RGB phase\n'
               '&middot; Pop: gaussian around the mouse over the bubble',
    ajustes='&middot; Nº de burbujas: el <code>7.0</code> de la rejilla\n'
            '&middot; Ascenso: el <code>t*0.5</code> de la deriva\n',
    ajustes_en='&middot; Bubble count: the <code>7.0</code> grid\n'
               '&middot; Rise: the <code>t*0.5</code> drift\n',
    shader=r'''
vec2 kg = uPlane / min(uPlane.x, uPlane.y);
vec2 g = tuv * kg * 7.0 + vec2(0.0, -t * 0.5);
vec2 idb2 = floor(g);
vec2 fb2 = fract(g) - 0.5;
vec2 off = (vec2(hash21(idb2), hash21(idb2 + 4.0)) - 0.5) * 0.5;
float rb = 0.16 + 0.14 * hash21(idb2 + 9.0);
float dd = length(fb2 - off);
float piel = smoothstep(rb, rb - 0.03, dd) - smoothstep(rb - 0.05, rb - 0.08, dd);
piel = max(piel, 0.0);
float dentro = smoothstep(rb - 0.02, rb - 0.06, dd);
vec2 mrat = (0.5 + uMouse * 0.5);
vec2 gRat = mrat * kg * 7.0 + vec2(0.0, -t * 0.5);
float revienta = exp(-60.0 * length(fract(gRat) - 0.5 - off)) * uAmp;
revienta = smoothstep(0.35, 0.9, revienta);
piel *= (1.0 - revienta);
float llena = exp(-2.5 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec3 iri = 0.5 + 0.5 * cos(6.2831 * (dd * 14.0 + t * 0.8) + vec3(0.0, 2.1, 4.2));
vec3 fill = vec3(0.03, 0.06, 0.09)
          + iri * piel * 1.7
          + vec3(0.5, 0.75, 0.9) * dentro * 0.18 * (1.0 + 2.0 * llena)
          + iri * revienta * 0.8;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.012, 0.026, 0.038);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.6, 0.9, 1.0) * rim * 0.55;
col += iri * ring * 0.6;
'''),

dict(
    nombre='algodon', cat='miscelanea',
    word='ALGODON', word_en='COTTON', emoji='\U0001F36C',
    titulo='Algodon', titulo_en='Cotton candy',
    sub='Nube de azucar', sub_en='Sugar cloud',
    descr='Nubes de algodon de azucar esponjan el texto en tonos pastel.',
    descr_en='Clouds of cotton candy fluff up the text in pastel tones.',
    acento='255, 190, 230', bg='#0d0710', fg='#ffd9f0',
    hint='el raton aprieta la nube &middot; clic para esponjarlo todo &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2c1526, #0b0610 70%)',
    escena=('halo', '#ffbee6', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'esponja pastel', 'tacto mullido',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la nube '
          'mecerse sola. El raton aprieta el algodon y el clic lo esponja todo.',
    que_hace='El texto se vuelve una nube de algodon de azucar: bultos suaves rosas y azules '
             'que se mecen y cambian de densidad con un tacto mullido.',
    que_hace_en='The text becomes a cloud of cotton candy: soft pink and blue tufts that sway '
                'and shift density with a fluffy touch.',
    tecnica='&middot; Bultos: <code>fbm</code> suave con dominio que se mece\n'
            '&middot; Pastel: mezcla rosa-azul por el propio ruido\n'
            '&middot; Apriete: el raton comprime el umbral de densidad',
    tecnica_en='&middot; Tufts: soft <code>fbm</code> with a swaying domain\n'
               '&middot; Pastel: pink-blue mix driven by the noise itself\n'
               '&middot; Squeeze: the mouse compresses the density threshold',
    ajustes='&middot; Tamaño de bulto: el <code>3.5</code> del fbm\n'
            '&middot; Mecida: la amplitud <code>0.5</code> del seno\n',
    ajustes_en='&middot; Tuft size: the <code>3.5</code> fbm scale\n'
               '&middot; Sway: the <code>0.5</code> sine amplitude\n',
    shader=r'''
float mece = sin(t * 0.9) * 0.5;
float n = fbm(tuv * 3.5 + vec2(mece, -t * 0.12));
float dens = smoothstep(0.30, 0.75 - 0.15 * uAmp, n);
vec3 pastel = mix(vec3(1.0, 0.68, 0.86), vec3(0.62, 0.78, 1.0),
                  0.5 + 0.5 * sin(n * 8.0 + t * 0.7));
float relieve = pow(dens, 2.0);
vec3 fill = vec3(0.08, 0.05, 0.10)
          + pastel * dens * 0.95
          + vec3(1.0, 0.95, 1.0) * relieve * 0.55;
fill += pastel * smoothstep(0.62, 0.78, n) * 0.6;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.040, 0.026, 0.048);
vec3 col = mix(bgc, fill, mask);
col += pastel * rim * 0.7;
col += pastel * ring * 0.55;
'''),

dict(
    nombre='nieve', cat='miscelanea',
    word='NIEVE', word_en='SNOW', emoji='⛄',
    titulo='Nieve', titulo_en='Snow',
    sub='Copos que caen', sub_en='Falling flakes',
    descr='Copos de nieve caen dentro de las letras y se acumulan suavemente en la base.',
    descr_en='Snowflakes fall inside the letters and gently pile up at the base.',
    acento='220, 240, 255', bg='#050810', fg='#e6f4ff',
    hint='el raton levanta el ventisco &middot; clic para una nevada fuerte &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #121c2c, #04060c 70%)',
    escena=('chispas', '#dceeff', {'n': 18, 'up': True}),
    datos=['GLSL ES 1.00', '1 pasada', 'copos en caida', 'acumulacion suave',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja nevar solo. '
          'El raton levanta el ventisco y el clic provoca una nevada fuerte.',
    que_hace='Copos blancos caen en varias capas de velocidad dentro del texto y una nieve '
             'suave se acumula en el borde inferior de las letras.',
    que_hace_en='White flakes fall at several speed layers inside the text and soft snow '
                'piles up along the bottom edge of the letters.',
    tecnica='&middot; Tres capas de copos con hash y velocidades distintas (parallax)\n'
            '&middot; Acumulacion: umbral vertical sobre el mapa difuminado\n'
            '&middot; Ventisco: el raton desplaza horizontalmente las capas',
    tecnica_en='&middot; Three flake layers with different hashes and speeds (parallax)\n'
               '&middot; Piling: vertical threshold over the blurred map\n'
               '&middot; Drift: the mouse shifts the layers sideways',
    ajustes='&middot; Densidad: el <code>34.0</code> de la rejilla de copos\n'
            '&middot; Acumulacion: el umbral <code>0.78</code>\n',
    ajustes_en='&middot; Density: the <code>34.0</code> flake grid\n'
               '&middot; Piling: the <code>0.78</code> threshold\n',
    shader=r'''
float vent = uMouse.x * 0.4 * uAmp;
float nevar = 1.0 + 2.0 * exp(-2.5 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec2 k = uPlane / min(uPlane.x, uPlane.y);
vec2 g1 = tuv * k * 24.0 + vec2(vent * 5.0, t * 2.4 * nevar);
vec2 id1 = floor(g1);
vec2 f1 = fract(g1) - 0.5;
float ex1 = step(0.62, hash21(id1));
vec2 off1 = (vec2(hash21(id1 + 3.1), hash21(id1 + 7.7)) - 0.5) * 0.5;
float r1 = 0.11 + 0.09 * hash21(id1 + 11.0);
float d1 = length(f1 - off1);
float gota1 = ex1 * (1.0 - smoothstep(r1 * 0.35, r1, d1));
vec2 g2 = tuv * k * 13.0 + vec2(vent * 11.0, t * 1.3 * nevar);
vec2 id2b = floor(g2);
vec2 f2b = fract(g2) - 0.5;
float ex2 = step(0.72, hash21(id2b + 5.0));
vec2 off2 = (vec2(hash21(id2b + 13.1), hash21(id2b + 17.7)) - 0.5) * 0.5;
float r2 = 0.13 + 0.11 * hash21(id2b + 21.0);
float d2 = length(f2b - off2);
float gota2 = ex2 * (1.0 - smoothstep(r2 * 0.45, r2, d2));
float brillo = 0.7 + 0.3 * sin(t * 4.0 + hash21(id1) * 6.2831);
float copos = gota1 * 0.75 * brillo + gota2;
float acum = smoothstep(0.55, 0.90, hb) * smoothstep(0.55, 0.10, tuv.y);
vec3 fill = mix(vec3(0.05, 0.08, 0.14), vec3(0.16, 0.22, 0.34), tuv.y * 0.5);
fill += vec3(0.95, 0.98, 1.0) * copos * 1.5;
fill += vec3(0.92, 0.96, 1.0) * acum * 1.4;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.020, 0.030, 0.055);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.85, 0.93, 1.0) * rim * 0.6;
col += vec3(0.8, 0.9, 1.0) * ring * 0.5;
'''),

dict(
    nombre='ambar', cat='miscelanea',
    word='AMBAR', word_en='AMBER', emoji='\U0001F7E2',
    titulo='Ambar', titulo_en='Amber',
    sub='Resina con inclusiones', sub_en='Resin inclusions',
    descr='El texto se solidifica en ambar con inclusiones atrapadas que brillan por dentro.',
    descr_en='The text solidifies into amber with trapped inclusions glowing inside.',
    acento='255, 180, 60', bg='#0d0801', fg='#ffdf9e',
    hint='el raton calienta la resina &middot; clic para atrapar una inclusion &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2b1c04, #0a0601 70%)',
    escena=('ring', '#ffb43c', {'n': 3}),
    datos=['GLSL ES 1.00', '1 pasada', 'resina dorada', 'inclusiones vivas',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la resina '
          'curar sola. El raton la calienta y el clic atrapa una inclusion nueva.',
    que_hace='Las letras se vuelven ambar dorado: una resina interna que ondea muy despacio '
             'con inclusiones oscuras atrapadas que brillan cuando el raton calienta la resina.',
    que_hace_en='The letters become golden amber: an internal resin waving very slowly with '
                'trapped dark inclusions that glow when the mouse warms the resin.',
    tecnica='&middot; Ondulacion lenta: <code>fbm</code> de baja frecuencia en la UV\n'
            '&middot; Inclusiones: hash disperso con umbral agudo\n'
            '&middot; Calor: gaussiana del raton que sube la temperatura del tinte',
    tecnica_en='&middot; Slow ripple: low frequency <code>fbm</code> over the UV\n'
               '&middot; Inclusions: sparse hash with a sharp threshold\n'
               '&middot; Heat: mouse gaussian raising the tint temperature',
    ajustes='&middot; Nº de inclusiones: el umbral <code>0.965</code>\n'
            '&middot; Ondulacion: la escala <code>2.0</code> del fbm\n',
    ajustes_en='&middot; Inclusion count: the <code>0.965</code> threshold\n'
               '&middot; Ripple: the <code>2.0</code> fbm scale\n',
    shader=r'''
float resina = fbm(tuv * 2.0 + vec2(t * 0.05, -t * 0.04));
float calor = exp(-8.0 * length(tuv - (0.5 + uMouse * 0.5))) * uAmp;
float incl = step(0.965, hash21(floor(tuv * 26.0) + floor(resina * 3.0)));
float brilloIncl = 0.5 + 0.5 * sin(t * 2.0 + hash21(floor(tuv * 26.0)) * 6.2831);
vec3 base = mix(vec3(0.55, 0.28, 0.04), vec3(0.95, 0.62, 0.14), resina);
base += vec3(1.0, 0.75, 0.25) * calor * 0.7;
float trampa = exp(-3.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec3 fill = base
          + vec3(0.35, 0.16, 0.03) * incl * (0.8 + 0.4 * brilloIncl)
          + vec3(1.0, 0.85, 0.4) * pow(resina, 4.0) * 0.6
          + vec3(1.0, 0.8, 0.35) * trampa * 0.5;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.036, 0.022, 0.006);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.8, 0.4) * rim * 0.75;
col += vec3(1.0, 0.75, 0.3) * ring * 0.5;
'''),

dict(
    nombre='miel', cat='miscelanea',
    word='MIEL', word_en='HONEY', emoji='\U0001F36F',
    titulo='Miel', titulo_en='Honey',
    sub='Goteo dorado', sub_en='Golden drip',
    descr='Miel dorada gotea y se estira por dentro de las letras con brillo viscoso.',
    descr_en='Golden honey drips and stretches inside the letters with viscous shine.',
    acento='255, 200, 60', bg='#0c0901', fg='#ffe9a8',
    hint='el raton arrastra la miel &middot; clic para soltar un hilo &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #2e2204, #0b0801 70%)',
    escena=('chispas', '#ffc83c', {'n': 10, 'up': False}),
    datos=['GLSL ES 1.00', '1 pasada', 'goteo viscoso', 'hilos que se estiran',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja gotear la '
          'miel sola. El raton la arrastra y el clic suelta un hilo nuevo.',
    que_hace='Gotas de miel se estiran entre las letras y se deslizan hacia abajo con un '
             'brillo ambar viscoso; el hilo se corta y vuelve a unirse con cada interaccion.',
    que_hace_en='Drops of honey stretch between the letters and slide down with a viscous '
                'amber shine; the thread cuts and rejoins with every interaction.',
    tecnica='&middot; Goteo: mascara desplazada en Y con onda lenta\n'
            '&middot; Viscosidad: <code>fbm</code> de baja frecuencia para el borde\n'
            '&middot; Hilo: banda vertical estrecha que se estira con el tiempo',
    tecnica_en='&middot; Drip: mask scrolled in Y with a slow wave\n'
               '&middot; Viscosity: low frequency <code>fbm</code> on the edge\n'
               '&middot; Thread: narrow vertical band stretching over time',
    ajustes='&middot; Rapidez del goteo: el <code>t*0.35</code> en Y\n'
            '&middot; Espesor del hilo: el <code>0.05</code> de la banda\n',
    ajustes_en='&middot; Drip speed: the <code>t*0.35</code> in Y\n'
               '&middot; Thread thickness: the <code>0.05</code> band\n',
    shader=r'''
float gota = 0.5 + 0.5 * sin(tuv.y * 14.0 + t * 1.4 + fbm(tuv * 3.0) * 3.0);
float hilo = smoothstep(0.05, 0.0, abs(fract(tuv.x * 3.0 + fbm(tuv * 2.0) * 0.6) - 0.5)
            * 2.0 - 0.9);
float estira = smoothstep(0.0, 0.6, gota);
float brilloV = pow(gota, 6.0);
float hiloNuevo = exp(-4.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT)
                * hilo;
vec3 base = mix(vec3(0.55, 0.34, 0.03), vec3(1.0, 0.78, 0.22), estira);
vec3 fill = base * (0.75 + 0.45 * brilloV)
          + vec3(1.0, 0.9, 0.55) * brilloV * 0.7
          + vec3(1.0, 0.85, 0.4) * hilo * 0.9
          + vec3(1.0, 0.9, 0.6) * hiloNuevo * 1.2;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.034, 0.026, 0.006);
vec3 col = mix(bgc, fill, mask);
col += vec3(1.0, 0.85, 0.4) * rim * 0.7;
col += vec3(1.0, 0.8, 0.35) * ring * 0.5;
'''),

dict(
    nombre='marmol', cat='miscelanea',
    word='MARMOL', word_en='MARBLE', emoji='\U0001F5FF',
    titulo='Marmol', titulo_en='Marble',
    sub='Vetas que fluyen', sub_en='Flowing veins',
    descr='Vetas de marmol fluyen lentamente por el interior de las letras.',
    descr_en='Marble veins flow slowly through the inside of the letters.',
    acento='210, 215, 230', bg='#0a0a0c', fg='#e8eaf2',
    hint='el raton pulsa la piedra &middot; clic para abrir una nueva veta &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #1d1f26, #08080a 70%)',
    escena=('malla', '#d2d7e6', {}),
    datos=['GLSL ES 1.00', '1 pasada', 'vetas fluidas', 'piedra pulida',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja las vetas '
          'fluir solas. El raton pulsa la piedra y el clic abre una veta nueva.',
    que_hace='El texto es una losa de marmol blanco con vetas grises que fluyen despacio como '
             'si la piedra estuviera viva, con un pulido que responde a la luz del raton.',
    que_hace_en='The text is a slab of white marble with grey veins flowing slowly as if the '
                'stone were alive, with a polish that answers the mouse light.',
    tecnica='&middot; Veta: <code>fbm</code> de dominio warpeado recortado en franja fina\n'
            '&middot; Flujo: desplazamiento lento del dominio en el tiempo\n'
            '&middot; Pulido: gaussiana del raton que sube el contraste local',
    tecnica_en='&middot; Vein: domain-warped <code>fbm</code> clipped to a thin band\n'
               '&middot; Flow: slow domain scroll over time\n'
               '&middot; Polish: mouse gaussian raising local contrast',
    ajustes='&middot; Nº de vetas: el <code>7.0</code> de la frecuencia\n'
            '&middot; Flujo: el <code>t*0.06</code> del dominio\n',
    ajustes_en='&middot; Vein count: the <code>7.0</code> frequency\n'
               '&middot; Flow: the <code>t*0.06</code> domain scroll\n',
    shader=r'''
vec2 w = vec2(fbm(tuv * 2.5 + vec2(0.0, t * 0.06)),
              fbm(tuv * 2.5 + vec2(5.2, 1.3) - t * 0.05));
float veta = fbm(tuv * 4.0 + w * 2.6);
float linea = smoothstep(0.44, 0.50, veta) * smoothstep(0.58, 0.52, veta);
float pulido = exp(-7.0 * length(tuv - (0.5 + uMouse * 0.5))) * uAmp;
float fisura = exp(-3.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec3 piedra = mix(vec3(0.82, 0.83, 0.87), vec3(0.62, 0.64, 0.70),
                  fbm(tuv * 6.0) * 0.5);
piedra *= 0.85 + 0.35 * pulido + 0.25 * fisura;
vec3 fill = piedra
          - vec3(0.30, 0.30, 0.34) * linea * 0.9
          + vec3(0.9, 0.95, 1.0) * pow(linea, 3.0) * 0.5;
float rim = pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5);
vec3 bgc = vec3(0.030, 0.030, 0.036);
vec3 col = mix(bgc, fill, mask);
col += vec3(0.9, 0.93, 1.0) * rim * 0.55;
col += vec3(0.8, 0.85, 0.95) * ring * 0.5;
'''),

dict(
    nombre='origami', cat='miscelanea',
    word='ORIGAMI', word_en='ORIGAMI', emoji='\U0001F4CE',
    titulo='Origami', titulo_en='Origami',
    sub='Pliegues de papel', sub_en='Paper folds',
    descr='El papel se pliega en facetas que cambian de tono al girar la luz.',
    descr_en='Paper folds into facets that shift tone as the light turns.',
    acento='240, 235, 220', bg='#0b0a08', fg='#f5f1e6',
    hint='el raton gira la luz &middot; clic para plegar de nuevo &middot; escribe tu palabra',
    preview='radial-gradient(120% 140% at 50% 0%, #26231b, #0a0906 70%)',
    escena=('estelas', '#f0ebdc', {'n': 6, 'ang': 50}),
    datos=['GLSL ES 1.00', '1 pasada', 'facetado angular', 'giro de luz',
           'canvas 2D + shaders'],
    paso3='palabra inicial (<code>+</code> = espacio) y <code>?demo=1</code> deja la luz girar '
          'sola. El raton la gira y el clic vuelve a plegar el papel.',
    que_hace='Las letras se facetan como papel plegado: triangulos de distinto tono que '
             'cambian de sombra cuando la luz gira, con un doblez visible en cada arista.',
    que_hace_en='The letters facet like folded paper: triangles of different shade that change '
                'shadow as the light turns, with a visible crease on every edge.',
    tecnica='&middot; Facetado: triángulos por <code>floor</code> de la UV con hash\n'
            '&middot; Sombra: producto escalar simulado con el hash de la cara\n'
            '&middot; Luz giratoria: angulo del raton o del tiempo sobre las caras',
    tecnica_en='&middot; Faceting: UV <code>floor</code> triangles hashed per face\n'
               '&middot; Shade: simulated dot product from the face hash\n'
               '&middot; Turning light: mouse or time angle over the faces',
    ajustes='&middot; Nº de pliegues: el <code>6.0</code> de la escala\n'
            '&middot; Contraste: el rango <code>0.45, 1.0</code> del sombreado\n',
    ajustes_en='&middot; Fold count: the <code>6.0</code> scale\n'
               '&middot; Contrast: the <code>0.45, 1.0</code> shading range\n',
    shader=r'''
vec2 g3 = tuv * (uPlane / min(uPlane.x, uPlane.y)) * 6.0;
vec2 id3 = floor(g3);
float tri = step(1.0, fract(g3.x + g3.y));
float cara = hash21(id3 + tri);
float luz = atan(uMouse.y, uMouse.x + 0.001) * uAmp + t * 0.6;
float sombra = 0.45 + 0.55 * (0.5 + 0.5 * sin(cara * 6.2831 + luz));
float doblez = smoothstep(0.03, 0.0, abs(fract(g3.x + g3.y) - 0.5) * 2.0 - 0.94);
float pliegue = exp(-3.0 * max(t - uClickT, 0.0)) * step(-9000.0, uClickT);
vec3 papel = vec3(0.94, 0.92, 0.86) * sombra;
papel += vec3(1.0, 0.98, 0.9) * doblez * 0.55;
papel *= 0.9 + 0.35 * pliegue;
papel -= vec3(0.18) * (1.0 - sombra) * 0.6;
vec3 bgc = vec3(0.034, 0.032, 0.028);
vec3 fill = papel;
vec3 col = mix(bgc, fill, mask);
col += vec3(0.95, 0.93, 0.85) * pow(clamp(hb * (1.0 - hb) * 4.0, 0.0, 1.0), 1.5) * 0.6;
col += vec3(0.9, 0.88, 0.8) * ring * 0.5;
'''),
]
