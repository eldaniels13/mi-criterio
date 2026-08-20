# Guía de captura cross-AI — mi-criterio

> **Documento canónico del formato de `inbox/`.** Vendor-neutral: sirve para Claude, ChatGPT,
> DeepSeek, Ollama o cualquier LLM.
>
> **Uso:** pegar la sección «BLOQUE PARA PEGAR» en una conversación nueva de `claude.ai/new`
> (o en las instrucciones de un proyecto). Al cerrar la sesión, pedir *"genera el handoff"*
> y la IA devolverá un archivo con el formato exacto que `/process-inbox` espera.
>
> Sustituye a `inbox/25-05-26_cross_ai_memory_integration_guide.md` (mayo 2026), cuyo formato
> —*Key Insights / Artifacts / Integration Hint*— quedó superado.

---

## 1 · Cómo funciona el sistema

```
Capa 1  inbox/          captura sin clasificar   ← aquí escriben las IAs
   │                    /process-inbox
Capa 2  proyectos/P#/   criterio consolidado por lente
   │
Capa 3  perfil_maestro  identidad, stack, criterio
```

Los ocho lentes: **P1** CNC/manufactura · **P2** programación · **P3** energía/sostenibilidad ·
**P4** finanzas · **P5** geopolítica · **P6** carrera/futuro · **P7** filosofía · **P8** ingeniería/soberanía.

## 2 · Dos formatos, un inbox

| Tipo | Nombre de archivo | Cuándo | Quién |
|---|---|---|---|
| **Handoff** | `DD-MM-YY_handoff_tema-corto.md` | Cierre de sesión de trabajo | la IA |
| **Captura** | `DD-MM-YY_captura_tema-corto.md` | Idea, link, fragmento suelto | eldaniels, en 30 s |

Plantillas completas en `inbox/_PLANTILLAS/`. Tema en kebab-case, sin espacios ni acentos.

## 3 · Qué hace que un handoff sirva

- **Rutas verificadas.** Error histórico del repo: dos handoffs declararon archivos que no
  existían o vivían en otra ruta. Ruta no comprobada → `[NO VERIFICADO]`.
- **"Diseñado" ≠ "medido".** Nada se reporta funcionando si no se ejecutó.
- **Lo descartado vale tanto como lo adoptado.** Evitar repetir un callejón sin salida es
  la mitad del valor del documento.
- **Datos duros íntegros.** Cifras, comandos, versiones, hashes, IDs, errores textuales.
- **Estado honesto.** A medias es 🟡, no ✅.

## 4 · Qué nunca entra

Credenciales, API keys, `local_key`, cifras financieras reales, nombres de institución
financiera, rutas con datos personales de terceros. Anonimizar como `Cuenta-1..N` o `[redactado]`.

---

# BLOQUE PARA PEGAR EN `claude.ai/new`

```markdown
## Contexto del sistema de conocimiento (mi-criterio)

Trabajo con un repositorio personal de conocimiento llamado `mi-criterio`, organizado en
tres capas: `inbox/` (captura) → `proyectos/P1..P8/` (criterio consolidado por lente) →
`perfil_maestro` (identidad y stack). Los lentes son: P1 CNC/manufactura, P2 programación,
P3 energía/sostenibilidad, P4 finanzas, P5 geopolítica, P6 carrera/futuro, P7 filosofía,
P8 ingeniería/soberanía de datos.

**Al cerrar esta sesión, cuando yo diga "genera el handoff", devuélveme un solo bloque de
código markdown con este formato exacto, listo para guardar como
`inbox/DD-MM-YY_handoff_tema-corto.md`:**

# DD-MM-YY — [Título]

**Fecha de corte:** YYYY-MM-DD · **Herramienta:** claude.ai
**Lente(s):** P# principal × P# secundarios
**Estado global:** ✅ completado / 🟡 parcial / 🔴 bloqueado / ❄️ congelado

## 1 · Objetivo y motivación
Qué se buscaba y **por qué** — qué duele si esto no existe.

## 2 · Estado real verificado al cerrar
Tabla: Componente | Estado | Verificado cómo.
Distingue **"lo diseñamos"** de **"lo medimos corriendo"**. Nada se reporta funcionando
si no se ejecutó. Lista aparte lo que NO quedó resuelto, sin suavizar.

## 3 · Archivos tocados — con ruta verificada
Tabla: Ruta | Acción (creado/modificado/movido/borrado) | Qué cambió y por qué.
Si no puedes comprobar que una ruta existe, márcala `[NO VERIFICADO]`.
Incluye cambios fuera del repo (configs, servicios, paquetes).

## 4 · Evaluado y descartado
Tabla: Opción o intento | Veredicto (✅ adoptado / 🔶 evaluado, no adoptado /
❌ descartado / ⚠️ bloqueado) | Razón, con el error textual si lo hubo.
Añade las suposiciones que resultaron falsas.

## 5 · Decisiones tomadas
Cada una con su razón, para no re-litigarlas. Marca las que quedan abiertas y qué falta.

## 6 · Siguientes pasos
Numerados. El primero, ejecutable sin leer nada más.
Añade bloqueadores y **riesgo mayor** (el paso que más probablemente falle, y por qué).

## 7 · Regla de oro para quien retome esto
Máximo 4 líneas: lo que evitaría el error más caro al volver.

## 8 · Datos duros a preservar
En bloque de código: cifras medidas, rutas, versiones, hashes, IDs, salidas de comando,
valores de configuración. Todo lo que un resumen destruiría.

## 9 · Destino sugerido
Doc canónico propuesto en `proyectos/P#/`; si actualiza `perfil_maestro` y qué §;
código a extraer a repo propio; insight cross-lens si lo hay.

**Reglas de escritura:**
- Sin cortesía conversacional ni recapitulación de la charla. Hechos y decisiones.
- No escatimes términos técnicos: soy ingeniero mecánico con Python y C# funcionales.
- Nunca incluyas credenciales, API keys ni cifras financieras reales — usa `[redactado]`.
- Si la sesión fue trivial, dilo y no generes el documento.
```

---

## 5 · Qué pasa después

1. Guardas el bloque como `inbox/DD-MM-YY_handoff_tema.md`
2. Corres `/process-inbox` en Claude Code
3. Se reconcilia disco↔índice, se propone `FUSIONAR / UNIFICAR / MOVER / EXTRAER /
   ARCHIVAR / DESCARTAR / MANTENER` por archivo, y esperas aprobación
4. Lo aprobado se destila hacia su doc canónico — **sin perder datos duros** — y los
   pendientes accionables caen en `ToDo_global_eldaniels.md`

**Objetivo:** un inbox, muchas IAs, cero vendor lock-in.
