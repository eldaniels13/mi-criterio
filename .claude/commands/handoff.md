Genera el documento de handoff de esta sesión en `inbox/`, listo para que `/process-inbox` lo destile después.

## Tu tarea

Escribir `inbox/DD-MM-YY_handoff_tema-corto.md` siguiendo `inbox/_PLANTILLAS/handoff.md`, reconstruido desde lo que realmente pasó en esta sesión.

### 1 · Reunir los hechos (no la narrativa)

Antes de escribir, revisar la sesión y extraer:

- Qué archivos se crearon, modificaron, movieron o borraron — con ruta exacta
- Qué comandos alteraron el sistema fuera del repo (servicios, configs, `~/.config`, paquetes)
- Qué se verificó **corriendo algo** vs. qué sólo se diseñó o se asumió
- Qué falló, con el **error textual**, no parafraseado
- Qué decisiones se tomaron y qué alternativas se descartaron, con su razón
- Cifras medidas, versiones, rutas, hashes, IDs, salidas de comando

Si algo no se puede confirmar desde la sesión, **verificarlo antes de escribirlo**:

```bash
git status --porcelain          # qué cambió de verdad en el repo
git diff --stat                 # magnitud de los cambios
```

### 2 · Escribir el documento

Rellenar las 9 secciones de `inbox/_PLANTILLAS/handoff.md`. Referencia de calidad: `proyectos/P2/HANDOFF_LLM_agentico_local.md`. Reglas:

- **§3 archivos tocados: verificar cada ruta antes de escribirla.** Es el error histórico del repo — dos handoffs previos declararon archivos que no existían (`fuentes_contraste.opml`) o que acabaron en otra ruta (`index.html`). Ruta no comprobada → `[NO VERIFICADO]` o no se lista.
- **§4 evaluado y descartado es la sección más valiosa.** Si no hubo descartes, decirlo; no borrar la sección.
- **Distinguir siempre "diseñado" de "medido".** Nunca reportar como funcionando algo que no se ejecutó.
- **§7 regla de oro:** máximo 4 líneas, lo que evitaría el error más caro al volver.
- **§8 datos duros** captura lo que un resumen destruiría. Ante la duda, incluir.
- **§6 siguientes pasos:** el primero debe ser ejecutable sin leer nada más.
- **No escatimar términos técnicos.** El lector es eldaniels — ingeniero mecánico con C#/Python funcional.
- Estado honesto: si algo quedó a medias, es 🟡, no ✅.
- Sin cortesía conversacional, sin recapitular la conversación. Hechos y decisiones.

### 3 · Nombrar el archivo

`DD-MM-YY_handoff_tema-corto.md` — fecha de hoy, tema en kebab-case, sin espacios ni acentos.

Ejemplos: `13-08-26_handoff_process-inbox.md`, `13-08-26_handoff_restmo-gitignore.md`

### 4 · Cerrar

- Mostrar la ruta del archivo generado
- Señalar qué secciones quedaron vacías o débiles y por qué
- Si la sesión tocó identidad, stack o criterio → señalar el fragmento concreto para `perfil_maestro` (no editarlo)
- Sugerir el commit, **sin ejecutarlo**: `inbox: handoff DD-MM-YY tema`

## Reglas

- **No inventar.** Si un dato no consta en la sesión, se verifica o se marca como `[no verificado]`.
- **No adornar el estado.** Un handoff optimista es peor que no tener handoff.
- Si la sesión fue trivial (una pregunta, un archivo leído), decirlo y **no generar el documento** — el inbox no necesita ruido.
- Si la sesión cubrió temas dispares, proponer partirla en dos handoffs antes de escribir.
- Nunca incluir credenciales, cifras financieras reales, ni nombres de institución financiera. Referirlos como `Cuenta-1..N` o `[redactado]`.
- No commitear. El usuario ejecuta git a mano.

ARGUMENTS: tema o enfoque específico para el handoff (opcional; si se omite, se infiere de la sesión)
