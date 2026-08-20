# PLANTILLA — Handoff de sesión

> Copiar a `inbox/DD-MM-YY_handoff_tema-corto.md`. Normalmente la genera `/handoff`.
> Derivada de `proyectos/P2/HANDOFF_LLM_agentico_local.md` — el mejor handoff del repo.
> Regla: **quien lea esto en 3 meses retoma sin preguntar nada.**
> Sin escatimar términos técnicos. Borrar esta cabecera al usar.

---

# DD-MM-YY — [Título de la sesión]

**Fecha de corte:** YYYY-MM-DD · **Herramienta:** Claude Code / claude.ai / ChatGPT / DeepSeek
**Lente(s):** P# principal × P#, P# secundarios
**Estado global:** ✅ completado · 🟡 parcial · 🔴 bloqueado · ❄️ congelado

---

## 1 · Objetivo y motivación

**Objetivo:** qué se buscaba lograr.

**Motivación — por qué, no sólo qué:** qué duele hoy si esto no existe.

| Driver | Detalle |
|---|---|
| | |

---

## 2 · Estado real verificado al cerrar

Distinguir siempre **"lo diseñamos"** de **"lo medimos corriendo"**. Nada se reporta
como funcionando si no se ejecutó.

| Componente | Estado | Verificado cómo |
|---|---|---|
| | ✅ / 🟡 / 🔴 | comando exacto + salida observada |

**Lo que NO quedó resuelto:** listado honesto, sin suavizar.

---

## 3 · Archivos tocados — con ruta verificada

> ⚠️ **Verificar antes de escribir esta tabla.** Es el error histórico del repo:
> dos handoffs previos declararon archivos que no existían o vivían en otra ruta.
> ```bash
> git status --porcelain && git diff --stat
> ls -la <cada ruta declarada>
> ```
> Un archivo sin ruta comprobada se marca `[NO VERIFICADO]` o no se lista.

| Ruta | Acción | Qué cambió y por qué |
|---|---|---|
| `ruta/real/archivo.md` | creado / modificado / movido / borrado | cambio concreto + razón |

**Cambios fuera del repo** (servicios, `~/.config`, paquetes, unidades systemd):

---

## 4 · Evaluado y descartado

Las dos caras del mismo ahorro: herramientas que se consideraron, y caminos que se
intentaron y fallaron. **Evitar repetir un callejón sin salida vale tanto como el acierto.**

| Opción / intento | Veredicto | Razón |
|---|---|---|
| | ✅ adoptado · 🔶 evaluado, no adoptado · ❌ descartado · ⚠️ bloqueado | evidencia concreta, error textual si lo hubo |

**Suposiciones que resultaron falsas:** lo que dábamos por hecho y no era cierto.

---

## 5 · Decisiones tomadas

Con su razón, para no re-litigarlas.

- [x] Decisión — *porque* …
- [ ] Decisión abierta — falta *qué* para cerrarla

**Punto ciego `[!]`** *(si aplica)*: sesgo del perfil que apareció en esta sesión.

---

## 6 · Siguientes pasos

En orden. El primero debe ser ejecutable sin leer nada más.

1. [ ] Acción concreta — comando o archivo exacto
2. [ ] …

**Bloqueadores:** qué impide avanzar y de qué depende.
**Riesgo mayor:** el paso que más probablemente falle, y por qué. Probarlo antes de
invertir en lo que depende de él.

---

## 7 · Regla de oro para quien retome esto

Máximo 4 líneas. Lo que evitaría el error más caro al volver.

1.
2.

---

## 8 · Datos duros a preservar

Todo lo que un resumen destruiría: cifras medidas, rutas, versiones, hashes, IDs,
salidas de comando, valores de config. `/process-inbox` los conserva íntegros.

```
```

---

## 9 · Destino sugerido

**Doc canónico:** `proyectos/P#/nombre.md` — ¿fusionar ahí o crear nuevo?
**Actualiza `perfil_maestro`:** sí / no — si sí, qué §
**Código a extraer:** repo propio en `~/Codes/`, si aplica
**Insight cross-lens** *(opcional)*: conexión no obvia entre lentes que esta sesión reveló.
