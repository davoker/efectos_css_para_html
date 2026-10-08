# Manual operativo para OpenCode
## Repositorio `efectos_css_para_html`

> **Propósito:** este documento define la arquitectura, convenciones y procedimiento operativo para añadir, modificar, reorganizar y mantener efectos de texto en este repositorio sin tener que volver a analizar todo el proyecto en cada petición.
>
> **Regla principal:** antes de modificar código existente, utiliza este documento como fuente principal de arquitectura. Solo lee los archivos concretamente indicados en cada operación cuando necesites comprobar una implementación existente o copiar un patrón.

---

# 1. Objetivo del repositorio

Este proyecto es una biblioteca/showcase de **efectos visuales aplicados a texto HTML**.

Actualmente existen tres tecnologías principales:

1. **Efectos CSS**
   - CSS puro.
   - Cada efecto es portable.
   - El efecto principal está en un archivo `.css`.
   - Cada efecto dispone de un showcase independiente.
   - Cada efecto dispone de un `.zip`.
   - Cada efecto dispone de instrucciones de instalación.

2. **Efectos SVG**
   - CSS + filtros SVG.
   - Los filtros pueden utilizar primitivas SVG como `feTurbulence`, `feDisplacementMap`, `feSpecularLighting`, `feColorMatrix`, etc.
   - Cada efecto tiene su showcase y su paquete `.zip`.
   - La página principal puede contener los filtros necesarios para mostrar las muestras.

3. **Efectos WebGL**
   - Efectos renderizados mediante WebGL/GLSL.
   - El efecto real suele estar en `<id>.html`.
   - El `index.html` del efecto es el showcase.
   - Los showcases WebGL utilizan una plantilla visual diferente de CSS/SVG.
   - Existe infraestructura compartida en:
     - `efectos_webgl/showcase.css`
     - `efectos_webgl/showcase.js`
     - `efectos_webgl/temas.js`

La portada principal es:

```text
index.html
```

---

# 2. Estructura general del repositorio

La estructura relevante es:

```text
/
├── index.html
├── i18n.js
├── transicion.html
├── transicion.css
│
├── efectos_css/
│   ├── miscelanea/
│   ├── matrix/
│   ├── monster_hunter/
│   ├── harry_potter/
│   ├── star_wars/
│   ├── stalker/
│   └── the_division/
│
├── efectos_svg/
│   ├── Matrix/
│   ├── marvel/
│   ├── ucm/
│   ├── cp2077/
│   ├── dot/
│   ├── mm/
│   └── miscelanea/
│
├── efectos_webgl/
│   ├── Matrix/
│   ├── miscelanea/
│   ├── showcase.css
│   ├── showcase.js
│   └── temas.js
│
└── zmds_update/
    ├── Directrices.txt
    └── prompts_open_code_efectos_webgl_v2.md
```

No reorganices estas carpetas arbitrariamente.

Cuando se cree una nueva categoría, debe respetarse esta jerarquía:

```text
efectos_css/<categoria>/<efecto>/
efectos_svg/<categoria>/<efecto>/
efectos_webgl/<categoria>/<efecto>/
```

La carpeta de categoría pertenece a una tecnología concreta. No mezclar efectos CSS, SVG y WebGL dentro de la misma carpeta.

---

# 3. Conceptos fundamentales

Hay tres niveles diferentes que no deben confundirse.

## 3.1. Tecnología

Es una de:

```text
efectos_css
efectos_svg
efectos_webgl
```

Determina cómo funciona técnicamente el efecto.

---

## 3.2. Categoría o temática

Ejemplos actuales:

```text
miscelanea
matrix
stalker
monster_hunter
harry_potter
star_wars
the_division
```

En SVG existen categorías como:

```text
Matrix
marvel
ucm
cp2077
dot
mm
miscelanea
```

En WebGL existen actualmente categorías como:

```text
Matrix
miscelanea
```

La categoría determina dónde aparece agrupado el efecto dentro del navegador lateral de `index.html`.

---

## 3.3. Efecto individual

Ejemplo:

```text
efectos_css/stalker/solitarios/
```

El identificador del efecto es:

```text
solitarios
```

Ese identificador debe mantenerse coherente en:

- nombre de carpeta;
- archivo principal;
- clase CSS;
- `id` HTML cuando corresponda;
- enlaces;
- ZIP;
- showcase;
- transición;
- datos de WebGL;
- traducciones.

---

# 4. Regla de oro para nombres

Los identificadores internos deben ser simples y estables.

Preferir:

```text
solitarios
mercurio
matrix2
cielodespejado
the_division
```

Evitar:

```text
Efecto Solitarios
efecto nuevo!!!
Mercurio líquido
Matrix 2 Cine
```

El nombre visible puede contener:

- mayúsculas;
- espacios;
- tildes;
- emojis;
- descripciones.

El identificador de archivos y rutas no.

Ejemplo:

```text
ID interno:
solitarios

Nombre visible:
🎒 Solitarios

Título:
EFECTO SOLITARIOS
```

---

# 5. Estructura de un efecto CSS

Cada efecto CSS sigue esta estructura:

```text
efectos_css/
└── <categoria>/
    └── <efecto>/
        ├── <efecto>.css
        ├── index.html
        ├── installation-instalacion-<efecto>.txt
        └── <efecto>.zip
```

Ejemplo real:

```text
efectos_css/stalker/solitarios/
├── solitarios.css
├── index.html
├── installation-instalacion-solitarios.txt
└── solitarios.zip
```

---

# 6. Qué contiene cada archivo CSS

El archivo:

```text
<efecto>.css
```

es el **efecto portable**.

Debe poder copiarse a otro proyecto.

La regla general es:

```html
<link rel="stylesheet" href="efecto.css">
```

y después:

```html
<span class="efecto-<id>">Texto</span>
```

Por ejemplo:

```html
<span class="efecto-solitarios">SOLITARIOS</span>
```

### Importante

El CSS del efecto debe contener exclusivamente lo necesario para el efecto.

No introducir en el CSS portable:

- estilos globales del showcase;
- navegación;
- botones;
- fondos de la página;
- HUD;
- paneles de instalación;
- código específico de `index.html`.

---

# 7. Showcase de un efecto CSS

El archivo:

```text
efectos_css/<categoria>/<efecto>/index.html
```

es la página de demostración.

Su función es:

1. mostrar el efecto;
2. mostrar diferentes tamaños de texto;
3. mostrar diferentes usos cuando sea necesario;
4. explicar cómo utilizarlo;
5. proporcionar navegación de vuelta a la portada;
6. proporcionar el botón `Descarga`;
7. cargar `i18n.js`.

La estructura actual utiliza:

```html
<nav class="barra-volver">
    <a class="btn-volver" href="../../../transicion.html#<efecto>">
        ← Portada
    </a>

    <a class="btn-volver" href="<efecto>.zip" download>
        Descarga
    </a>
</nav>
```

## Nombre del botón

El botón de descarga de los showcases debe llamarse:

```text
Descarga
```

No utilizar:

```text
ZIP
Descargar ZIP
Descargar efecto
Download ZIP
```

La traducción al inglés se realiza mediante `i18n.js`.

---

# 8. Qué debe mostrar un showcase CSS

Como mínimo:

```text
Portada
Descarga

Título del efecto

Descripción

Demo grande

Demo mediana

Demo pequeña

Varias palabras / párrafo / variante adicional

Cómo aplicarlo a cualquier archivo CSS

Notas de uso, si son necesarias
```

No es obligatorio copiar literalmente la misma cantidad de demos si el efecto necesita otra estructura.

Lo importante es demostrar correctamente:

- tamaño grande;
- tamaño pequeño;
- comportamiento con varias palabras;
- comportamiento con párrafos cuando proceda;
- limitaciones del efecto.

---

# 9. Archivo de instalación CSS

Nombre:

```text
installation-instalacion-<efecto>.txt
```

Debe explicar:

- qué hace el efecto;
- qué archivo copiar;
- cómo enlazar el CSS;
- qué clase utilizar;
- ejemplo HTML;
- requisitos;
- limitaciones;
- variantes disponibles.

Si el efecto utiliza una clase diferente a:

```text
.efecto-<id>
```

debe documentarse explícitamente.

---

# 10. ZIP de un efecto CSS

Cada efecto CSS debe tener:

```text
<efecto>.zip
```

En la estructura estándar actual:

```text
<efecto>.css
index.html
installation-instalacion-<efecto>.txt
```

Ejemplo:

```text
solitarios.zip
├── solitarios.css
├── index.html
└── installation-instalacion-solitarios.txt
```

## Regla crítica

**Siempre que se modifique el CSS, el HTML o las instrucciones, hay que regenerar el ZIP.**

Nunca dejar:

```text
solitarios.css actualizado
solitarios.zip antiguo
```

El botón:

```html
<a href=".../solitarios.zip" download>
```

debe apuntar al ZIP existente.

---

# 11. Estructura de un efecto SVG

La estructura sigue el mismo concepto:

```text
efectos_svg/
└── <categoria>/
    └── <efecto>/
        ├── <efecto>.css
        ├── index.html
        ├── installation-instalacion-<efecto>.txt
        └── <efecto>.zip
```

Ejemplo real:

```text
efectos_svg/Matrix/matrix/
├── matrix.css
├── index.html
├── installation-instalacion-matrix.txt
└── matrix.zip
```

---

# 12. Diferencia fundamental de SVG respecto a CSS

Un efecto SVG puede necesitar:

- CSS;
- filtros SVG;
- `<svg>`;
- `<defs>`;
- `<filter>`;
- referencias `filter: url(#...)`;
- animaciones SVG.

Por tanto, **no asumir que SVG es solamente CSS**.

Cuando se añada un efecto SVG, revisar qué necesita realmente el efecto.

Si el filtro está embebido en el showcase, determinar qué debe incluirse en el paquete para que el efecto sea portable.

El archivo de instalación debe indicar claramente si el usuario necesita un bloque SVG adicional o cualquier otro recurso.

---

# 13. Filtros SVG en `index.html`

La portada principal contiene una gran colección de filtros SVG para las muestras.

Estos filtros suelen utilizar IDs como:

```text
ef-mercurio
ef-glitch
ef-repulsor
ef-telarana
...
```

Para un efecto SVG nuevo que necesite un filtro en la portada:

1. crear el filtro;
2. utilizar un ID único;
3. añadirlo al `<svg>` oculto de `index.html`;
4. utilizarlo desde la muestra;
5. evitar colisiones de IDs.

Regla:

```text
ID del filtro = único en todo index.html
```

No reutilizar un ID de filtro existente para otro efecto.

---

# 14. Muestra de la portada

Las tarjetas de efectos utilizan una muestra circular.

CSS general:

```text
.muestra
```

Características actuales:

- 200 × 200 px;
- `border-radius: 50%`;
- `overflow: hidden`;
- fondo oscuro;
- el efecto se muestra dentro;
- texto centrado.

SVG y WebGL también utilizan muestras circulares equivalentes.

Por tanto, un efecto nuevo **no debe introducir una tarjeta cuadrada diferente** salvo que la petición lo solicite expresamente.

---

# 15. Tarjeta de efecto en `index.html`

Una tarjeta CSS sigue esencialmente esta estructura:

```html
<section
    id="<efecto>"
    class="tarjeta"
    data-cat="<categoria>"
>
    <div class="muestra">
        <span class="efecto-<efecto>">
            NOMBRE
        </span>
    </div>

    <h2 class="c-<efecto>">
        <span>Nombre visible</span>
        <small>Descripción corta</small>
    </h2>

    <a
        class="btn"
        href="efectos_css/<categoria>/<efecto>/index.html"
    >
        Showcase completo
    </a>

    <a
        class="btn btn-descarga"
        href="efectos_css/<categoria>/<efecto>/<efecto>.zip"
        download
    >
        Descargar efecto (.zip)
    </a>

    <!-- escena temática correspondiente -->
</section>
```

No copiar literalmente este bloque si el efecto pertenece a SVG o WebGL.

---

# 16. `id` del efecto en la portada

El `id` de la tarjeta debe coincidir con el identificador utilizado para la navegación.

Ejemplo:

```html
<section id="solitarios" ...>
```

y:

```html
<a href="#solitarios">🎒 Solitarios</a>
```

Esto permite saltar directamente a la tarjeta.

---

# 17. `data-cat`

Las tarjetas CSS utilizan:

```html
data-cat="miscelanea"
```

o:

```html
data-cat="stalker"
```

etc.

Debe coincidir con la categoría lógica.

No utilizar aleatoriamente el nombre visible.

Correcto:

```html
data-cat="monster_hunter"
```

---

# 18. Categorías plegables

Las categorías del índice lateral utilizan:

```html
<details class="grupo" id="g-<categoria>" data-cat="<categoria>">
    <summary class="grupo-titulo">
        Nombre
        <span class="grupo-n">N</span>
    </summary>

    <ol class="lista">
        ...
    </ol>
</details>
```

Ejemplo actual:

```html
<details class="grupo" id="g-stalker" data-cat="stalker">
```

La categoría debe estar plegada inicialmente.

---

# 19. Lista de efectos de una categoría

Dentro del `<details>`:

```html
<ol class="lista">
    <li data-cat="stalker">
        <a href="#solitarios">🎒 Solitarios</a>
    </li>
</ol>
```

Para SVG/WebGL, los enlaces actuales apuntan normalmente al showcase:

```html
<a href="efectos_svg/Matrix/matrix/index.html">
```

o:

```html
<a href="efectos_webgl/Matrix/matrix/index.html">
```

Mantener el patrón utilizado por la tecnología correspondiente.

---

# 20. Contador de categoría

El contador:

```html
<span class="grupo-n">20</span>
```

debe representar el número real de efectos de esa categoría.

Nunca poner un número aproximado.

Si se añaden 40 efectos:

```text
20 → 60
```

si la categoría tenía inicialmente 20.

---

# 21. Añadir un efecto a una categoría existente

Cuando la petición sea:

> Añade 10 efectos a Stalker.

El procedimiento correcto es:

### Paso 1 — Crear las carpetas

```text
efectos_css/stalker/nuevo1/
efectos_css/stalker/nuevo2/
...
```

### Paso 2 — Crear el efecto portable

Por cada efecto:

```text
<id>.css
```

### Paso 3 — Crear showcase

```text
index.html
```

### Paso 4 — Crear documentación

```text
installation-instalacion-<id>.txt
```

### Paso 5 — Crear ZIP

```text
<id>.zip
```

### Paso 6 — Registrar CSS en `index.html`

Añadir:

```html
<link rel="stylesheet"
      href="efectos_css/stalker/<id>/<id>.css">
```

### Paso 7 — Añadir al índice lateral

```html
<li data-cat="stalker">
    <a href="#<id>">ICONO Nombre</a>
</li>
```

### Paso 8 — Actualizar contador

Actualizar el `<span class="grupo-n">`.

### Paso 9 — Añadir tarjeta

Añadir:

```html
<section id="<id>" class="tarjeta" data-cat="stalker">
```

### Paso 10 — Añadir estilo del título

Si se utiliza el sistema actual:

```css
.c-<id> {
    color: ...;
}
```

### Paso 11 — Añadir escena de transición

Si el sistema de transición requiere una escena individual:

- `transicion.css`;
- `transicion.html`;
- copia de la escena dentro de la tarjeta de portada.

### Paso 12 — Añadir traducciones

Añadir los textos nuevos a `i18n.js`.

### Paso 13 — Regenerar ZIP si se ha cambiado posteriormente algún archivo.

---

# 22. Crear una categoría nueva dentro de una tecnología

Ejemplo:

> Crea una categoría `cyberpunk` dentro de CSS.

Crear:

```text
efectos_css/cyberpunk/
```

Después:

```text
efectos_css/cyberpunk/efecto1/
efectos_css/cyberpunk/efecto2/
...
```

En `index.html` hay que hacer **todas** estas operaciones:

1. registrar los CSS;
2. crear el `<details>` de la categoría;
3. añadir la lista;
4. crear las reglas CSS de filtrado para la categoría;
5. añadir las tarjetas con `data-cat`;
6. actualizar contador;
7. integrar las escenas si corresponden;
8. añadir traducciones;
9. comprobar la muestra aleatoria.

---

# 23. Regla importante al crear categorías

No basta con crear:

```html
<details id="g-nueva">
```

La lógica de `index.html` actualmente tiene reglas específicas que controlan qué tarjetas permanecen visibles cuando una categoría está abierta.

Por tanto, una categoría nueva requiere también integrar su identificador en las reglas correspondientes.

Patrón actual:

```css
body:has(.grupo[open]):not(:has(#g-miscelanea[open]))
    .galeria .tarjeta[data-cat="miscelanea"] {
    display: none;
}
```

Para una categoría nueva debe existir la regla equivalente con su `id` y `data-cat`.

---

# 24. Crear una sección tecnológica completamente nueva

Si la petición es:

> Crea un nuevo apartado del menú principal llamado Efectos Canvas.

Esto es diferente de crear una categoría.

Una **sección** es un apartado de primer nivel. Actualmente:

```text
Efectos CSS
Efectos SVG
Efectos WebGL
```

La sección utiliza:

```html
<details
    class="seccion-indice"
    id="s-<id>"
    name="secciones"
>
```

Ejemplo actual:

```html
<details class="seccion-indice" id="s-svg" name="secciones">
```

Una sección nueva debe tener:

```html
<details
    class="seccion-indice"
    id="s-canvas"
    name="secciones"
>
    <summary class="seccion-titulo">
        Efectos Canvas
        <span class="contador">N disponibles</span>
    </summary>

    ...
</details>
```

---

# 25. Una nueva sección necesita su propio bloque de contenido

No colocar efectos de una nueva tecnología dentro de `.galeria` sin una razón clara.

Crear una estructura equivalente a:

```html
<section class="seccion-canvas">
    <h2 class="titulo-canvas">
        Efectos Canvas
    </h2>

    <p class="sub-canvas">
        Descripción específica de la tecnología.
    </p>

    <div class="galeria-canvas">
        ...
    </div>
</section>
```

La clase exacta puede adaptarse a la tecnología, pero debe mantener la arquitectura:

```text
sección
→ descripción
→ categorías
→ tarjetas
```

---

# 26. Descripción de cada sección

Cada tecnología debe tener su **propio texto explicativo**.

No mezclar las explicaciones.

### Efectos CSS

Debe explicar:

```text
Cada tarjeta es una muestra circular del efecto.
El botón showcase muestra ejemplos aplicados a textos
de diferentes tamaños.
El botón de descarga contiene el CSS, HTML e instrucciones.
```

### Efectos SVG

Debe explicar que utiliza:

```text
filtros SVG
CSS
efectos sobre el texto
```

### Efectos WebGL

Debe explicar:

```text
WebGL
GLSL
renderizado en tiempo real
shaders
```

Si se crea una tecnología nueva, su descripción debe explicar **su propia técnica**, no repetir la descripción de CSS.

---

# 27. Orden de las secciones

El orden actual del navegador principal es:

```text
Efectos CSS
Efectos SVG
Efectos WebGL
```

No cambiar este orden salvo que la petición lo solicite.

---

# 28. Sistema de 12 efectos aleatorios

`index.html` tiene un script de selección aleatoria.

Utiliza:

```javascript
var N = 12;
```

y agrupa:

```javascript
tarjetasCss
tarjetasSvg
tarjetasWebgl
```

Después selecciona:

- 12 entre todas las tecnologías cuando no hay sección abierta;
- 12 de CSS si está abierta CSS;
- 12 de SVG si está abierta SVG;
- 12 de WebGL si está abierta WebGL.

## Regla

Al añadir una tecnología nueva:

**no olvidar integrarla en este algoritmo.**

No asumir que el algoritmo la detectará automáticamente.

---

# 29. Secciones de primer nivel: comportamiento plegable

Las secciones utilizan:

```html
name="secciones"
```

y JavaScript adicional para garantizar que solo haya una sección abierta.

Cuando se abre:

```text
Efectos CSS
```

deben plegarse:

```text
Efectos SVG
Efectos WebGL
```

y viceversa.

Si se crea una nueva sección, debe incorporarse al mismo sistema.

---

# 30. Categorías dentro de cada sección

La jerarquía lógica es:

```text
SECCIÓN
│
├── CATEGORÍA
│   ├── efecto
│   ├── efecto
│   └── efecto
│
├── CATEGORÍA
│   ├── efecto
│   └── efecto
│
└── ...
```

No confundir:

```text
sección ≠ categoría
```

---

# 31. Efectos WebGL

Los efectos WebGL tienen una estructura diferente a CSS/SVG.

Ejemplo:

```text
efectos_webgl/Matrix/matrix/
├── index.html
├── matrix.html
├── installation-instalacion-matrix.txt
└── matrix.zip
```

El archivo:

```text
index.html
```

es el **showcase**.

El archivo:

```text
matrix.html
```

es el **efecto WebGL real**.

---

# 32. Showcase WebGL

Los showcases WebGL utilizan recursos compartidos:

```text
efectos_webgl/showcase.css
efectos_webgl/showcase.js
```

No crear una plantilla visual independiente para cada efecto salvo que se solicite expresamente.

La plantilla actual utiliza:

- efecto a pantalla completa mediante `<iframe>`;
- HUD;
- placa de identidad;
- botón `Portada`;
- botón `Descarga`;
- datos técnicos;
- panel lateral de instalación;
- canvas ambiental;
- controles de teclado.

Ejemplo:

```html
<iframe
    class="escenario"
    src="matrix.html?demo=1"
    title="Efecto MATRIX en marcha">
</iframe>
```

---

# 33. Archivo real del efecto WebGL

El efecto debe estar en:

```text
<id>.html
```

Puede contener:

- HTML;
- CSS;
- JavaScript;
- GLSL;
- shaders;
- atlas;
- recursos necesarios.

Siempre que sea posible, mantener el efecto autocontenido.

No introducir dependencias externas innecesarias.

---

# 34. Parámetro `?demo=1`

Muchos efectos WebGL utilizan:

```text
?demo=1
```

para controlar la demostración automática.

Si el efecto necesita movimiento automático en las muestras de la portada, debe soportarlo de manera compatible con el sistema actual.

No asumir que todos los efectos WebGL funcionan igual.

---

# 35. `showcase.js`

Archivo:

```text
efectos_webgl/showcase.js
```

es código compartido.

Actualmente controla, entre otras cosas:

- panel de instalación;
- tecla `I`;
- tecla `ESC`;
- canvas ambiental;
- `prefers-reduced-motion`;
- visibilidad de pestaña;
- animación ambiental.

## Regla

Si una funcionalidad debe funcionar para **todos los showcases WebGL**, modificar:

```text
showcase.js
```

No copiar el mismo JavaScript dentro de 40 showcases.

Si solo afecta a un efecto, mantenerlo dentro del efecto correspondiente.

---

# 36. `showcase.css`

Archivo:

```text
efectos_webgl/showcase.css
```

contiene el diseño común de los showcases WebGL.

Antes de modificarlo para un solo efecto, comprobar si el cambio afectará a todos.

Preferir atributos del `<body>` como:

```html
<body
    class="showcase"
    data-tema="matrix"
    data-efecto="matrix"
    style="--acento-rgb: 0, 255, 65">
```

para configurar diferencias por efecto.

---

# 37. `temas.js`

Archivo:

```text
efectos_webgl/temas.js
```

es el manifiesto de efectos WebGL agrupados por temática.

Actualmente existe:

```javascript
window.TEMAS = {
    matrix: [...],
    miscelanea: [...]
};
```

Cada efecto se registra con la función `ruta()`.

La función genera automáticamente las rutas de:

```text
index.html
<id>.html
<id>.zip
installation-instalacion-<id>.txt
```

---

# 38. Añadir un WebGL nuevo a una temática existente

Si se añade:

```text
efectos_webgl/Matrix/nuevo/
```

y pertenece a la temática:

```text
matrix
```

añadirlo a:

```javascript
window.TEMAS.matrix
```

Ejemplo:

```javascript
ruta('Matrix/nuevo/', {
    id: 'nuevo',
    nombre: 'NUEVO',
    linea: 'Descripción corta',
    desc: 'Descripción completa.',
    preview: 'lluvia',
    datos: ['1 pasada', 'GLSL', 'canvas']
})
```

---

# 39. Añadir una temática WebGL nueva

Si el efecto no pertenece a ninguna temática existente:

```javascript
window.TEMAS = {
    matrix: [...],
    miscelanea: [...],

    nueva_temática: [
        ...
    ]
};
```

Después hay que crear la categoría correspondiente en `index.html` y registrar sus tarjetas.

---

# 40. Regla de afinidad temática de WebGL

El botón o mecanismo de navegación de temática debe mostrar efectos afines.

Ejemplo:

```text
Matrix
├── Matrix
├── Matrix 2
├── Arquitecto
├── Smith
└── ...
```

Si se crea un nuevo efecto relacionado con Matrix, debe registrarse en la temática `matrix`.

No crear una temática nueva simplemente porque el efecto tiene un nombre diferente.

---

# 41. ZIP WebGL

El ZIP WebGL debe contener todo lo necesario para utilizar el efecto.

Ejemplo:

```text
matrix.zip
├── matrix.html
├── index.html
└── installation-instalacion-matrix.txt
```

Si el efecto necesita archivos adicionales:

```text
matrix.zip
├── matrix.html
├── shader.glsl
├── textura.png
├── index.html
└── installation-instalacion-matrix.txt
```

No excluir dependencias necesarias.

Después de modificar cualquier archivo incluido en el ZIP:

**regenerar el ZIP.**

---

# 42. Regla especial para rutas WebGL

En `temas.js`, las rutas son relativas a:

```text
efectos_webgl/temas.js
```

Por ejemplo:

```javascript
ruta('Matrix/matrix/', ...)
```

No escribir:

```javascript
ruta('efectos_webgl/Matrix/matrix/', ...)
```

porque se duplicaría la ruta.

---

# 43. Integración de WebGL en `index.html`

Una tarjeta WebGL utiliza:

```html
<section
    class="tarjeta-webgl"
    data-webgl="<categoria>"
>
```

y una muestra:

```html
<div class="wg-muestra">
    ...
</div>
```

La muestra circular debe conservar:

```css
border-radius: 50%;
overflow: hidden;
```

---

# 44. Integración de SVG en `index.html`

Las tarjetas SVG utilizan:

```text
.tarjeta-svg
```

y:

```text
data-svg="<categoria>"
```

La muestra:

```text
.sv-muestra
```

también debe permanecer circular.

Si el efecto necesita JavaScript adicional en la portada, añadirlo de forma controlada.

Actualmente existen scripts específicos para algunos efectos SVG. No añadir JavaScript a todos los efectos si el efecto puede funcionar sin él.

---

# 45. Transiciones de portada

Los showcases vuelven a la portada mediante:

```text
transicion.html#<efecto>
```

El sistema de transición está formado por:

```text
transicion.html
transicion.css
```

La escena de cada efecto debe ser coherente con el efecto.

Si se crea un efecto nuevo y la arquitectura actual requiere escena propia:

1. añadir clase temática en `transicion.css`;
2. añadir la escena correspondiente en `transicion.html`;
3. conectar el showcase;
4. conectar la tarjeta de portada cuando corresponda.

---

# 46. Escena temática dentro de la tarjeta

El `index.html` actual también puede contener una copia de la escena:

```html
<div class="escena tema-<efecto>">
    ...
</div>
```

Esto permite mostrar la animación cuando se pulsa `Descargar efecto`.

No olvidar que la escena de la tarjeta y la escena de `transicion.html` deben representar el mismo efecto.

---

# 47. Regla para el botón de descarga

El botón de descarga no es solamente un enlace.

Actualmente participa en el sistema visual de escenas mediante:

```text
.btn-descarga
```

y selectores que relacionan el botón con la `.escena` siguiente.

Por tanto, si se cambia la estructura HTML de la tarjeta, hay que comprobar que el selector siga siendo válido.

No mover arbitrariamente:

```html
<a class="btn btn-descarga">...</a>
<div class="escena">...</div>
```

sin comprobar las reglas CSS que los relacionan.

---

# 48. Internacionalización

Archivo central:

```text
i18n.js
```

Controla el cambio:

```text
ES ↔ EN
```

El idioma se guarda en `localStorage` con la clave:

```text
efectos-idioma
```

La portada crea el selector de idioma y los showcases aplican el idioma guardado.

---

# 49. No duplicar lógica de idiomas

No crear:

```text
i18n-stalker.js
i18n-webgl.js
```

para efectos individuales.

Utilizar el archivo común:

```html
<script src="../../../i18n.js"></script>
```

con la ruta relativa correcta.

---

# 50. Cuando se añade texto nuevo

Si se añade un efecto nuevo, habrá textos nuevos como:

- nombre;
- descripción;
- título;
- notas;
- botón;
- descripción técnica.

Esos textos deben estar disponibles en `i18n.js`.

El diccionario actual funciona mediante asociaciones:

```javascript
"texto español": "English text"
```

Añadir las entradas necesarias.

## Importante

No traducir automáticamente las clases CSS, IDs, rutas o nombres de archivos.

Se traducen únicamente los textos visibles.

---

# 51. Qué no debe traducirse

No modificar por i18n:

```text
efecto-solitarios
solitarios.css
efectos_css/
data-cat="stalker"
id="solitarios"
```

Sí traducir:

```text
🎒 Solitarios
```

a su equivalente inglés visible.

---

# 52. Cómo añadir muchos efectos de una vez

Si la petición es:

> Haz 40 efectos nuevos en Stalker.

NO hacer una exploración completa del repositorio antes de empezar.

Utilizar este procedimiento:

### Fase A — identificar destino

Solo comprobar:

```text
efectos_css/stalker/
```

y el bloque Stalker de:

```text
index.html
```

### Fase B — elegir identificadores

Crear una lista de:

```text
id
nombre visible
descripción
clase
color
```

### Fase C — generar los 40 efectos

Cada uno debe tener:

```text
<id>.css
index.html
installation-instalacion-<id>.txt
<id>.zip
```

### Fase D — integrar portada

Modificar únicamente `index.html` en los lugares necesarios.

### Fase E — integrar transición

Solo si las escenas forman parte de la petición.

### Fase F — i18n

Añadir únicamente las nuevas cadenas.

### Fase G — validar

Comprobar:

```text
40 carpetas
40 CSS
40 showcases
40 TXT
40 ZIP
40 entradas de navegación
40 tarjetas
40 enlaces válidos
40 traducciones cuando proceda
```

No releer los efectos existentes salvo que haya un problema específico.

---

# 53. Estrategia de consumo mínimo de contexto

OpenCode debe minimizar lecturas innecesarias.

## Si se modifica un efecto CSS existente

Leer solamente:

```text
efectos_css/<categoria>/<efecto>/*
```

y, si hay integración en portada:

```text
index.html
```

No leer todos los efectos.

## Si se añade un efecto CSS

Leer:

```text
1 efecto existente de la misma categoría
index.html
```

y `transicion.css` / `transicion.html` solo si hay escena.

## Si se añade una categoría CSS

Leer:

```text
1 categoría existente
index.html
```

No leer todos los efectos.

## Si se añade un efecto SVG

Leer:

```text
1 efecto SVG equivalente
index.html
```

y los scripts compartidos que sean necesarios.

## Si se añade un efecto WebGL

Leer:

```text
1 showcase WebGL
efectos_webgl/showcase.css
efectos_webgl/showcase.js
efectos_webgl/temas.js
index.html
```

No leer los demás efectos WebGL.

## Si se añade una categoría WebGL

Leer:

```text
1 categoría WebGL
temas.js
index.html
```

## Si se modifica el diseño común WebGL

Leer:

```text
efectos_webgl/showcase.css
efectos_webgl/showcase.js
```

---

# 54. No modificar archivos enormes innecesariamente

`index.html` es un archivo grande y contiene:

- CSS de la portada;
- filtros SVG;
- categorías;
- tarjetas;
- lógica aleatoria;
- lógica de secciones;
- escenas;
- canvas;
- otros componentes.

Por tanto:

**hacer cambios quirúrgicos.**

No reemplazar el archivo completo por una versión generada desde cero.

No borrar accidentalmente:

- filtros;
- tarjetas;
- scripts;
- estilos;
- escenas;
- traducciones embebidas;
- enlaces.

---

# 55. No sobrescribir efectos existentes

Al crear un efecto nuevo:

1. comprobar que la carpeta no existe;
2. comprobar que el `id` no está utilizado;
3. comprobar que la clase no está utilizada;
4. comprobar que el ID de filtro SVG no existe;
5. comprobar que el nombre no colisiona con otro efecto.

Nunca sobrescribir silenciosamente.

---

# 56. Cambios de nombre o movimiento

Si se mueve cualquier archivo o carpeta:

hay que actualizar todas las referencias.

Buscar:

```text
href
src
url(...)
download
data-*
temas.js
i18n.js
transicion.html
transicion.css
```

Si el entorno de trabajo dispone de Git, preferir:

```bash
git mv
```

para mantener historial.

---

# 57. No romper enlaces relativos

Las rutas son especialmente importantes porque los showcases se abren también mediante doble clic.

Ejemplo desde:

```text
efectos_css/stalker/solitarios/index.html
```

la raíz está tres niveles arriba.

Por tanto:

```html
<script src="../../../i18n.js"></script>
```

es correcto.

No cambiarlo sin mover el archivo.

---

# 58. Showcase independiente

Los showcases deben poder abrirse individualmente.

No asumir:

```text
solo funciona desde index.html
```

Debe funcionar:

```text
doble clic → showcase
```

cuando la tecnología lo permita.

Si una tecnología necesita servidor local, documentarlo.

---

# 59. Dependencias WebGL

Un efecto WebGL puede necesitar servidor local si utiliza:

```javascript
fetch(...)
```

para cargar:

- shaders;
- JSON;
- texturas;
- recursos externos.

Si el efecto es autocontenido y no necesita `fetch`, indicarlo en las instrucciones.

No introducir `fetch` innecesariamente en efectos que puedan ser autocontenidos.

---

# 60. `prefers-reduced-motion`

Los efectos compartidos y showcases que tengan animación de interfaz deben respetar:

```css
@media (prefers-reduced-motion: reduce)
```

o su equivalente JavaScript.

No eliminar esta compatibilidad al crear nuevas animaciones.

---

# 61. Rendimiento

Al crear efectos:

- evitar bucles JS innecesarios;
- evitar múltiples `requestAnimationFrame` independientes si pueden compartirse;
- evitar canvas enormes;
- detener animaciones cuando no sean visibles;
- respetar `document.hidden`;
- respetar `prefers-reduced-motion`;
- no cargar recursos externos innecesarios.

Especialmente importante para WebGL.

---

# 62. Reglas para colores de tarjetas

El sistema actual utiliza clases:

```text
.c-glitch
.c-matrix
.c-solitarios
...
```

Cuando se cree un efecto nuevo:

```css
.c-nuevo {
    color: ...;
}
```

La clase debe coincidir con el identificador.

No modificar accidentalmente los colores de otros efectos.

---

# 63. Añadir 40 efectos no significa solamente crear 40 CSS

Una petición masiva se considera terminada solamente cuando cada efecto está completamente integrado.

Para cada efecto:

```text
[ ] carpeta
[ ] CSS / recurso principal
[ ] showcase
[ ] documentación
[ ] ZIP
[ ] enlace de navegación
[ ] tarjeta
[ ] clase visual
[ ] traducción
[ ] transición si corresponde
[ ] dependencia registrada si corresponde
```

---

# 64. Contadores

Existen contadores de dos niveles.

## Sección

Ejemplo:

```html
<span class="contador">
    119 disponibles
</span>
```

## Categoría

Ejemplo:

```html
<span class="grupo-n">
    20
</span>
```

Si se añaden efectos:

1. actualizar contador de categoría;
2. actualizar contador de sección;
3. comprobar que los números coinciden con los efectos reales.

No confiar en números antiguos.

---

# 65. Validación de una incorporación

Después de añadir un efecto, comprobar:

### Archivos

```text
¿Existe la carpeta?
¿Existe el archivo principal?
¿Existe index.html?
¿Existe installation-instalacion-...txt?
¿Existe ZIP?
```

### Portada

```text
¿Existe <link>?
¿Existe entrada del menú?
¿Existe tarjeta?
¿El data-cat es correcto?
¿El href es correcto?
¿El ZIP apunta al archivo correcto?
```

### Showcase

```text
¿Carga el efecto?
¿Funciona el botón Portada?
¿Funciona Descarga?
¿Carga i18n.js?
```

### ZIP

```text
¿Está actualizado?
¿Contiene todas las dependencias?
```

### Traducción

```text
¿Los textos nuevos tienen EN?
¿El cambio EN → ES restaura correctamente el español?
```

---

# 66. Validación de una categoría nueva

Comprobar:

```text
[ ] carpeta creada
[ ] categoría visible en el índice
[ ] categoría plegada inicialmente
[ ] contador correcto
[ ] lista correcta
[ ] reglas CSS de filtrado añadidas
[ ] tarjetas con data-cat correcto
[ ] selección aleatoria compatible
[ ] enlaces correctos
[ ] traducciones
```

---

# 67. Validación de una nueva sección

Comprobar:

```text
[ ] <details class="seccion-indice">
[ ] id único s-...
[ ] name="secciones"
[ ] contador
[ ] descripción propia
[ ] categorías
[ ] tarjetas
[ ] CSS de visibilidad
[ ] sistema de 12 aleatorios
[ ] cierre de las otras secciones
[ ] responsive
[ ] idioma
[ ] navegación
```

---

# 68. Búsqueda de errores antes de finalizar

Después de una modificación grande, buscar referencias al identificador nuevo.

Por ejemplo:

```text
solitarios
```

debe aparecer donde corresponda en:

```text
carpeta
CSS
showcase
ZIP
index.html
transicion.*
i18n.js
```

No debe aparecer en lugares que no correspondan.

---

# 69. Errores comunes que deben evitarse

## Error 1

Crear el CSS pero no el showcase.

**Incorrecto.**

## Error 2

Crear el showcase pero no el ZIP.

**Incorrecto.**

## Error 3

Actualizar el CSS pero no regenerar el ZIP.

**Incorrecto.**

## Error 4

Añadir la tarjeta pero olvidar el enlace del menú.

**Incorrecto.**

## Error 5

Añadir el enlace pero olvidar la tarjeta.

**Incorrecto.**

## Error 6

Añadir una categoría sin añadir sus reglas de filtrado.

**Incorrecto.**

## Error 7

Crear un WebGL nuevo pero olvidar `temas.js`.

**Incorrecto.**

## Error 8

Crear texto nuevo y olvidar `i18n.js`.

**Incorrecto.**

## Error 9

Cambiar una ruta y romper los `href/src` relativos.

**Incorrecto.**

## Error 10

Rehacer `index.html` entero para añadir un efecto.

**Evitar siempre.**

---

# 70. Procedimiento recomendado para una petición del usuario

Cuando el usuario diga:

> Haz 20 efectos nuevos de Matrix en SVG.

interpretar automáticamente:

```text
tecnología = SVG
categoría = Matrix
cantidad = 20
```

y ejecutar:

```text
1. crear 20 efectos
2. crear 20 showcases
3. crear 20 TXT
4. crear 20 ZIP
5. registrar CSS/filtros
6. registrar entradas
7. registrar tarjetas
8. actualizar contador
9. actualizar i18n
10. actualizar transición si procede
11. comprobar enlaces
12. comprobar ZIP
```

No preguntar innecesariamente qué archivos tocar.

---

# 71. Si el usuario dice "añade una sección"

Interpretar:

```text
sección de primer nivel
```

No:

```text
categoría
```

Ejemplo:

> Añade una sección de efectos Canvas.

requiere:

```text
s-canvas
```

más:

```text
contenido-canvas
categorías-canvas
tarjetas-canvas
lógica aleatoria
filtrado
contador
descripción
```

---

# 72. Si el usuario dice "añade una categoría"

Interpretar:

```text
grupo dentro de una sección tecnológica
```

Ejemplo:

> Añade una categoría Cyberpunk a SVG.

requiere:

```text
efectos_svg/cyberpunk/
```

y:

```text
g-svg-cyberpunk
```

No crear:

```text
s-cyberpunk
```

---

# 73. Si el usuario dice "añade un efecto"

Determinar la tecnología y categoría a partir del contexto.

Ejemplo:

> Añade "Blackwall" a CP2077 SVG.

significa:

```text
efectos_svg/cp2077/blackwall/
```

---

# 74. Arquitectura de referencia rápida

## CSS

```text
efectos_css/
└── categoria/
    └── efecto/
        ├── efecto.css
        ├── index.html
        ├── installation-instalacion-efecto.txt
        └── efecto.zip
```

## SVG

```text
efectos_svg/
└── categoria/
    └── efecto/
        ├── efecto.css
        ├── index.html
        ├── installation-instalacion-efecto.txt
        └── efecto.zip
```

## WebGL

```text
efectos_webgl/
└── categoria/
    └── efecto/
        ├── index.html
        ├── efecto.html
        ├── installation-instalacion-efecto.txt
        └── efecto.zip
```

---

# 75. Archivos globales y su función

| Archivo | Función |
|---|---|
| `index.html` | Portada, navegación, tarjetas, muestras y lógica general |
| `i18n.js` | ES/EN global |
| `transicion.html` | Escenas de transición |
| `transicion.css` | Estilos/animaciones de transición |
| `efectos_webgl/showcase.css` | Diseño común WebGL |
| `efectos_webgl/showcase.js` | Comportamiento común WebGL |
| `efectos_webgl/temas.js` | Manifiesto/agrupación temática WebGL |
| `zmds_update/Directrices.txt` | Directrices de modificaciones anteriores |
| `zmds_update/prompts_open_code_efectos_webgl_v2.md` | Historial de instrucciones específicas de WebGL |

---

# 76. Qué archivos leer según la tarea

| Tarea | Archivos mínimos |
|---|---|
| Nuevo CSS | 1 CSS existente + `index.html` |
| Nuevo showcase CSS | 1 showcase CSS existente |
| Nueva categoría CSS | 1 categoría existente + `index.html` |
| Nuevo SVG | 1 SVG existente + `index.html` |
| Nueva categoría SVG | 1 categoría SVG + `index.html` |
| Nuevo WebGL | 1 WebGL + `showcase.css` + `showcase.js` + `temas.js` |
| Nueva categoría WebGL | 1 categoría + `temas.js` + `index.html` |
| Nueva sección | `index.html` + 1 sección existente |
| Traducciones | `i18n.js` |
| Transiciones | `transicion.html` + `transicion.css` |
| Cambiar diseño WebGL global | `showcase.css` + `showcase.js` |
| Cambiar navegación global | `index.html` |
| Cambiar idioma global | `i18n.js` |

---

# 77. Regla de no exploración innecesaria

**No leer todo el repositorio por defecto.**

La existencia de cientos de efectos no significa que haya que inspeccionarlos todos.

Utilizar un efecto existente como plantilla representativa.

Por ejemplo:

```text
Nuevo CSS → leer un CSS existente
Nuevo SVG → leer un SVG existente
Nuevo WebGL → leer un WebGL existente
```

Solo ampliar la búsqueda si:

- el patrón no está claro;
- existen implementaciones diferentes;
- aparece un error;
- el usuario pide mantener una característica concreta;
- se detecta una inconsistencia.

---

# 78. Regla de conservación

Al modificar una parte del proyecto:

**preservar todo lo que no forme parte de la petición.**

No:

- eliminar efectos;
- cambiar nombres;
- reorganizar carpetas;
- rediseñar showcases;
- cambiar colores globales;
- cambiar navegación;
- eliminar traducciones;
- eliminar escenas;

salvo que el usuario lo haya solicitado.

---

# 79. Regla de consistencia

Un efecto nuevo debe parecer parte del mismo repositorio.

Eso significa:

- misma estructura de archivos;
- misma nomenclatura;
- misma navegación;
- mismo sistema de ZIP;
- misma documentación;
- misma internacionalización;
- mismo comportamiento de portada;
- misma filosofía de showcases.

La tecnología puede ser diferente, pero la integración debe ser coherente.

---

# 80. Regla de calidad para efectos generados

Cuando se solicite una cantidad elevada de efectos:

> "Haz 40 efectos nuevos"

no crear 40 variaciones casi idénticas cambiando únicamente el color.

Cada efecto debe representar una idea visual diferenciada.

Debe variar, cuando sea apropiado:

- movimiento;
- textura;
- composición;
- animación;
- iluminación;
- deformación;
- interacción;
- técnica;
- ritmo;
- dirección;
- profundidad.

La reutilización de una técnica interna es aceptable, pero el resultado visual debe ser distinguible.

---

# 81. Checklist final obligatorio

Antes de informar de que una tarea está terminada:

```text
[ ] Los archivos nuevos existen.
[ ] Las rutas son correctas.
[ ] Los enlaces del índice funcionan.
[ ] Los showcases funcionan.
[ ] Los botones Portada funcionan.
[ ] Los botones Descarga apuntan al ZIP correcto.
[ ] Los ZIP están actualizados.
[ ] Los ZIP contienen las dependencias necesarias.
[ ] Los contadores son correctos.
[ ] Las categorías son plegables.
[ ] La selección aleatoria sigue funcionando.
[ ] Las nuevas cadenas están en i18n.js.
[ ] Las rutas relativas funcionan desde los showcases.
[ ] No se han eliminado efectos existentes.
[ ] No se han sobrescrito archivos sin motivo.
[ ] No se han introducido nombres duplicados.
[ ] No se han roto las escenas de transición.
[ ] WebGL está registrado en temas.js cuando corresponda.
[ ] SVG tiene sus filtros/recursos registrados cuando corresponda.
[ ] Se respeta el comportamiento responsive.
[ ] No hay errores obvios de HTML/CSS/JS.
```

---

# 82. Regla final para OpenCode

Cuando el usuario pida una modificación, piensa en términos de **integración completa**, no solamente de creación del archivo.

Un efecto no está terminado cuando existe:

```text
efecto.css
```

Está terminado cuando existe y está conectado a todo su ecosistema:

```text
EFECTO
│
├── archivo portable
├── showcase
├── documentación
├── ZIP
├── categoría
├── navegación
├── tarjeta
├── contador
├── traducción
├── transición
└── infraestructura específica
```

Para WebGL:

```text
EFECTO
├── index.html
├── efecto.html
├── documentación
├── ZIP
├── showcase compartido
├── temas.js
├── categoría
├── navegación
├── tarjeta
└── traducción
```

Para SVG:

```text
EFECTO
├── CSS
├── filtros SVG
├── showcase
├── documentación
├── ZIP
├── categoría
├── navegación
├── tarjeta
├── traducción
└── scripts adicionales si son necesarios
```

**El objetivo de este documento es que OpenCode pueda realizar peticiones masivas y modificaciones estructurales utilizando la arquitectura conocida, leyendo únicamente los archivos estrictamente necesarios y sin tener que volver a descubrir el funcionamiento completo del repositorio en cada sesión.**
