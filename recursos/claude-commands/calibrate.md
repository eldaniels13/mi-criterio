---
description: Verifica por comprensión los claims declarativos y los convierte en defendibles o en huecos de estudio
argument-hint: [skill | "auto" para tomar los sin_calibrar/stale | ruta-a-JD para priorizar]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git log:*), Bash(git rev-parse:*), Bash(rg:*)
---

# Calibración por comprensión (Loop A — estudio)

## Objetivo
Convertir claims `declarativo`/`sin_calibrar` en `defendible`, `parcial` o `gap` mediante
preguntas de comprensión. Doble propósito: (1) que solo postule lo que puedo sostener en
entrevista; (2) que descubra qué me falta aprender. NO es time-boxed: es sesión de estudio.

## Selección
- `$ARGUMENTS` vacío o `auto`: toma de `EVIDENCE` los claims `sin_calibrar` o `stale`
  (donde `calibrated_at` ≠ HEAD actual del archivo de evidencia). Dime cuántos hay y cuánto
  tomaría cubrirlos todos; yo elijo cuántos hacer hoy. Sin cap fijo — las que hagan falta.
- `$ARGUMENTS` = skill: calibra ese.
- `$ARGUMENTS` = ruta-JD: prioriza los claims que ese JD vuelve críticos.

## Mecánica (por claim, UNA pregunta a la vez)
1. Formula UNA pregunta de comprensión **al nivel de profundidad que un rol real implica**,
   contestable en 60–90 s. Apunta al *cómo* y a los *tradeoffs*, no a la definición.
2. Espera mi respuesta. Captúrala como `defense_line` en MIS palabras (pulida, no inventada).
3. Califica con honestidad — **no apruebes respuestas flojas** (esto es el pushback que pedí):
   - `defendible`: explico qué + cómo + un detalle/decisión de diseño concreto, sin titubear.
   - `parcial`: conozco el qué pero no el cómo/los tradeoffs → `learn_flag` con el hueco exacto.
   - `gap`: no lo puedo articular → `status: gap`, no se usa en aplicaciones, `learn_flag` con
     qué estudiar primero.
4. Si la evidencia es solo declarativa pero YO la sostengo bien, súbela a `defendible` y anota
   `defense_line`; el respaldo pasa a ser "lo sostengo en entrevista" (válido y defendible).
   Si además aparece un artefacto/commit que lo respalde, anótalo y sube `tipo` a `proyecto`.
5. Escribe de vuelta en `EVIDENCE`: `status`, `defense_line`, `learn_flag`,
   `calibrated_at: <HEAD-corto> (fecha)`. Sugiere commit `update P6: calibrate <claim>`.

## Salida
- Filas actualizadas de `EVIDENCE` (mostrar diff).
- **Learn-list** priorizada: qué estudiar, en qué orden, por qué (atada a los `learn_flag`).
