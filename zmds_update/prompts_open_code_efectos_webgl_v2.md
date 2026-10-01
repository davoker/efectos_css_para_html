# Prompts para Open Code: reorganización del proyecto `efectos_css_para_html` (v2)

**Directorio de trabajo:** `C:\Users\David\Documents\GitHub\efectos_css_para_html`

Ejecuta los prompts **en orden**, uno por sesión o mensaje. Espera a que termine cada uno y revisa el resultado antes de lanzar el siguiente, porque cada fase depende de la anterior.

**Novedades de esta versión:** las páginas showcase de `efectos_webgl` deben tener un diseño completamente distinto al de `efectos_css`, y el botón "todos los efectos" debe mostrar efectos de la misma temática de cada efecto nuevo.

---

## Instrucciones generales (pegar al inicio de la sesión)

```text
Vas a trabajar en el repositorio ubicado en:
C:\Users\David\Documents\GitHub\efectos_css_para_html

Reglas para toda la sesión:
- Antes de modificar nada, explora la estructura actual de carpetas y archivos y resúmemela.
- Usa operaciones de renombrado/movimiento que conserven el historial de Git (git mv) siempre que sea posible.
- Tras mover o renombrar cualquier carpeta o archivo, actualiza TODAS las rutas relativas, enlaces, imports, src/href y referencias en HTML, CSS, JS, scripts y documentación que queden rotas.
- No elimines ni sobrescribas contenido existente sin avisarme antes.
- Trabaja por fases y al terminar cada una muéstrame un resumen de los cambios realizados y una comprobación de que no hay enlaces rotos.
- Si algo es ambiguo (por ejemplo, un nombre de archivo que no encuentres), pregúntame antes de asumir.
```

---

## Fase 1: Renombrado y reorganización de carpetas

```text
Objetivo: reorganizar las carpetas del proyecto.

Tareas, en este orden:

1. Renombra la carpeta "efectos" a "efectos_css".
2. Renombra la carpeta "prueba" a "efectos_webgl".
3. Dentro de "efectos_webgl", crea una carpeta llamada "Matrix" y mueve dentro los dos efectos "matrix" y "matrix2".
4. Dentro de "efectos_webgl", renombra el efecto "index" a "mercurio".
5. Dentro de "efectos_webgl", crea una carpeta llamada "miscelanea" y mueve dentro el efecto "mercurio" que acabas de renombrar.

Requisitos:
- Actualiza todas las rutas relativas y referencias afectadas por estos cambios (incluido el index principal del proyecto y cualquier script o documento que apunte a "efectos" o "prueba").
- Si el efecto "index" tiene archivos asociados (CSS, JS, assets), muévelos y renómbralos de forma coherente.
- Al terminar, muéstrame el árbol de carpetas resultante y la lista de referencias que has corregido.
```

---

## Fase 2: Estructura de `efectos_webgl` basada en `efectos_css`, con showcases de diseño propio

```text
Objetivo: que "efectos_webgl" siga la misma estructura de archivos que "efectos_css", pero con páginas showcase de diseño completamente diferente.

Primero, analiza "efectos_css" y describe brevemente cómo está organizada (páginas showcase, botón "todos los efectos", zips, documentación de instalación, nomenclatura, archivos compartidos).

Después, aplica la misma estructura a cada efecto de "efectos_webgl" (Matrix/matrix, Matrix/matrix2 y miscelanea/mercurio):

1. Página showcase completa para cada efecto. IMPORTANTE: el diseño de estas páginas debe ser COMPLETAMENTE DIFERENTE al de las showcase de efectos_css (distinta maquetación, composición, tipografía, paleta, componentes y estilo visual). No reutilices la plantilla visual de efectos_css. Propón primero una dirección de diseño para los showcase de WebGL (por ejemplo, más inmersiva, con el efecto a pantalla completa y controles flotantes) y espera mi conformidad antes de implementarla.
2. Botón "todos los efectos" en cada showcase: al pulsarlo debe mostrar los efectos de la misma temática que el efecto actual (por ejemplo, en Matrix deben verse matrix y matrix2 juntos). Para cada efecto nuevo que se añada en el futuro, este botón debe incluir sus efectos de temática afín.
3. Un archivo .zip por efecto que contenga los archivos necesarios para aplicar el efecto (HTML, CSS, JS, shaders, assets).
4. Un documento de instalación/uso que explique cómo aplicar estos nuevos efectos WebGL en un proyecto HTML, siguiendo el mismo formato y estructura que los documentos de efectos_css.
5. En general, la misma estructura de carpetas y nomenclatura que en efectos_css, pero dentro de efectos_webgl.

Requisitos:
- Reutiliza la lógica común y los scripts compartidos de efectos_css cuando sea razonable, pero NO el diseño visual de los showcase.
- Verifica que los efectos WebGL funcionan al abrirse desde su showcase y que los zips generados contienen todas las dependencias.
- Si un efecto WebGL requiere algo especial (por ejemplo, un servidor local por restricciones de carga de shaders), indícalo en su documento de instalación.
- Al terminar, muéstrame el árbol de efectos_webgl y un resumen por efecto de los archivos generados.
```

---

## Fase 3: Dividir el index en dos secciones

```text
Objetivo: reestructurar el index principal en dos secciones.

Tareas:

1. La sección actual de EFECTOS, que contiene todos los efectos CSS, pasa a llamarse "EFECTOS CSS".
2. Crea una segunda sección nueva llamada "EFECTOS WEBGL", situada DEBAJO de la primera. Debe tener su propio contador de número de efectos, calculado a partir de los efectos reales de efectos_webgl.
3. En el panel lateral izquierdo de navegación, las dos secciones deben aparecer una debajo de la otra, con el mismo estilo y comportamiento (scroll, resaltado de sección activa, etc.).
4. Las tarjetas/enlaces de la sección WEBGL deben llevar a los showcases creados en la Fase 2.

Requisitos:
- Mantén intactos el diseño, filtros, buscador y demás funcionalidades existentes.
- Cada contador debe reflejar únicamente los efectos de su sección.
- Comprueba que todos los enlaces del index funcionan tras los cambios.
```

---

## Fase 4: Separador animado entre secciones

```text
Objetivo: crear un separador visual entre "EFECTOS CSS" y "EFECTOS WEBGL".

Tareas:

1. Diseña un separador vistoso con una animación en bucle, con temática de "conexiones de neuronas": nodos que se mueven suavemente y se enlazan con líneas cuando están cerca unos de otros.
2. Colócalo entre las dos secciones del index, ocupando el ancho completo de la página, con una altura moderada.
3. Debe integrarse con la paleta de colores y la estética actuales del index.

Requisitos técnicos:
- Implementación ligera (canvas o SVG/CSS) sin dependencias externas nuevas, con buen rendimiento.
- Animación fluida y continua en bucle, que se pause cuando no sea visible (IntersectionObserver) para ahorrar recursos.
- Responsive: debe adaptarse a móvil y escritorio.
- Respeta `prefers-reduced-motion`, mostrando una versión estática cuando esté activo.
- Al terminar, indícame en qué archivos has añadido el código y cómo ajustar densidad, velocidad y colores.
```

---

## Verificación final (opcional)

```text
Haz una revisión completa del proyecto:
- Recorre todos los enlaces del index, de los showcases y de los documentos, y lista cualquiera que esté roto.
- Confirma que los contadores de ambas secciones coinciden con el número real de efectos.
- Comprueba que cada zip se abre y contiene los archivos necesarios.
- Confirma que los showcase de efectos_webgl tienen un diseño claramente distinto al de efectos_css.
- Resume todos los cambios realizados en las cuatro fases y propón un mensaje de commit por fase.
```
