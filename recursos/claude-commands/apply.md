---
description: Genera material de aplicación a vacante en ~10 min, evidence-backed y defendible
argument-hint: <ruta-al-JD.pdf|docx|txt | o pega el texto del JD>
allowed-tools: Read, Write, Glob, Grep, Bash(git log:*), Bash(git rev-parse:*), Bash(rg:*), Bash(markitdown:*)
---

# Agente de Aplicación (Loop B — rápido, ~10 min)

## Objetivo
El caso MÁS FUERTE que sea **verdadero y respaldado**, condicionado a que lo pueda sostener en
persona. Para postular rápido a Indeed / LinkedIn / OCC / CompuTrabajo. Reusa claims ya
calibrados; calibra inline lo nuevo y crítico, las preguntas que hagan falta (sin cap fijo).

## Reglas de honestidad (no negociables)
1. Nunca fabricar experiencia, skills, certificaciones, métricas ni logros.
2. **Verdad-pero-engañoso = fabricación** (insinuar profundidad/recencia/propiedad inexistente).
3. Toda métrica traza a una medición real; si no, cualitativo sin número.
4. Solo usa claims con `status: defendible` (o `parcial` con caveat honesto). Nunca uses `gap`.

## Idioma
Detecta el idioma del JD; entregables en ese idioma. La interacción conmigo, en español.

## Presupuesto de tiempo (objetivo suave ~10 min — tú decides al ver el conteo)
```
0:00        pego JD
0:00–1:30   parse JD + ranking de reqs + vocabulario real
1:30–2:00   mapeo JD ↔ EVIDENCE (cacheado); detecta críticos no calibrados/stale
2:00–?      me dice CUÁNTAS preguntas necesita (~tiempo) y elijo: todas o aplazo a /calibrate
?–?         genera entregables del board
último min  bandas de fit + provenance + learn-list
```

## Flujo
### 0 — Ingesta
Si `$ARGUMENTS` es ruta PDF/docx → `markitdown`. Si es texto, directo. Detecta idioma.

### 1 — Análisis del JD
Extrae: requeridos, preferidos, responsabilidades, dominio, seniority, soft/cultural, y el
**vocabulario real del JD** (para reusarlo SOLO en skills reales). Sin mito de "score ATS":
son parsers que un humano consulta.

### 2 — Ranking y mapeo
Lista priorizada de calificaciones. Mapea cada req a `EVIDENCE`. Valida frescura: si el archivo
de evidencia cambió (HEAD ≠ `calibrated_at`), marca el claim `stale`.

### 3 — Calibración inline (sin cap fijo, costo visible)
Identifica TODOS los claims JD-críticos en `sin_calibrar`/`stale`/`parcial`. Cuéntalos y dime
por adelantado: "necesito N preguntas (~M min) para cubrir los críticos". Entonces elijo:
(a) hacerlas todas ahora, o (b) hacer las top-K y aplazar el resto a `/calibrate`. Calibra con
la mecánica de `/calibrate` y escribe TODO resultado a `EVIDENCE` (queda listo para la próxima).

### 4 — Gate (ligero, scoped)
Bloquea SOLO si un claim que de verdad quiero usar en ESTA aplicación sigue sin ser defendible.
Claims no críticos sin calibrar simplemente se omiten (no detienen el flujo). Mantiene la velocidad.

### 5 — Entregables (default board, multi)
Default rápido: **Resume ATS-friendly** (base reusado + ajuste fino) · **respuestas a screening
questions** · **nota corta / mensaje a reclutador**. Opcionales: cover letter, carta de
motivación, mensaje LinkedIn, respuestas a formulario, resumen portafolio, notas de entrevista.
Pregúntame cuáles (con el default ya marcado).

### 6 — Generación
Vocabulario del JD natural y solo en skills reales · usa los `defense_line` como evidencia ·
logros cualitativos o con métrica trazable · matches fuertes primero · quita lo irrelevante ·
consistencia entre todos los documentos.

### 7 — Diferenciación
Contra los REQUISITOS del JD, nunca contra competidores imaginados.

### 8 — Review (bandas, no porcentajes)
Fit en **fuerte / parcial / gap** en: técnico · experiencia · dominio · match-de-vocabulario.
Fortalezas (con evidencia) · riesgos · mitigaciones. Más **learn-list** de lo que salió en la
calibración inline.

### 9 — Salida
- Texto (resume, screening, nota): **bloque copy-paste** por entregable, sin marcas dentro.
- Visual (CV, cover): Canva MCP si está; si no, **prompt-Canva listo para pegar**.
- **Provenance map** en bloque SEPARADO: claim → evidencia → status → "sostenido en entrevista" si aplica.
- Ofrece archivar el match profile en `companies/<empresa>/` siguiendo las convenciones del repo.

## Principios operativos
- Caso más fuerte verdadero y con evidencia, nunca a secas.
- Solo claims `defendible` (o `parcial` con caveat). `gap` jamás entra.
- Cierto-pero-engañoso = fabricación. Todo número traza a medición real.
- Provenance separado del entregable.
- Diferenciar contra el JD, no contra competidores imaginados.
- Fit en bandas cualitativas. Índice primero, detalle solo si hace falta.
- Velocidad: reusar calibración; lo profundo va a `/calibrate`, no a cada aplicación.
