# Sesión de diseño — PlantillaFinanzas2026.xlsx

> **Inicio:** 2026-07-04 · **Última actualización:** 2026-07-18
> **Modo:** voz (móvil) + Claude Code (laptop) · **Archivo base:** `04-07-26_audit_finanzas2026.md`
> **Nota de privacidad:** este doc NO contiene cifras, saldos ni nombres de instituciones
> financieras reales. Cuentas referidas como `Cuenta-1..N` (mapeo real solo en el `.xlsx` local).

---

## 1. Auditoría original — 8 errores (todos cerrados ✅)

| # | Hoja | Falla | Fix aplicado |
|---|------|-------|--------------|
| 1 | Dashboard | Todo `#ref!` | Reconstruido con `IFERROR`/`SUMIFS` en inglés |
| 2 | Dashboard | Gastos en 0 | Literal `"Egreso"` corregido |
| 3 | Dashboard | Categorías sin match | Alineado a 18 categorías reales |
| 4 | Catalogos col D | Promedio mensual mal + `#DIV/0!` enero | `SUMIF / n_meses_con_datos` (hoja `Listas!E2`) |
| 5 | Inversiones | Suma incompleta | Fórmula interés compuesto rellenada en filas faltantes |
| 6 | Transacciones | Filas sin categoría | **Pendiente manual** — usuario categoriza con dropdown |
| 7 | Transacciones | Dropdown Tarjeta incompleto | Rango extendido, dropdown ahora depende de Tipo |
| 8 | Archivo | Riesgo corrupción (lock activo) | Protocolo: cerrar LibreOffice antes de editar con openpyxl |

---

## 2. Modelo de Transferencias — IMPLEMENTADO (corrección vs. diseño original)

**Problema resuelto:** transferencias internas se contaban como ingreso+egreso a la vez,
neutralizadas a mano en fórmulas frágiles.

**Diseño original (sesión voz) proponía** 2 columnas nuevas (`TarjetaOrigen`/`TarjetaDestino`).
**Lo implementado en laptop es más compacto** — sin agregar columnas:

- `Tipo = "Transferencia"` — 3er valor del dropdown existente.
- Columna `Tarjeta` (ya existente) recibe un **código compuesto** `Cuenta-A->Cuenta-B` desde un
  dropdown dependiente (hoja `Listas`, rango `TransCodes` — todas las permutaciones de cuentas +
  "Cuenta Externa").
- Categoría, cuando Tipo=Transferencia, usa named range `CatTrans` (vacío/no aplica) en vez de
  romper el `INDIRECT` con un tercer caso no contemplado.

**Lógica de cálculo (saldo por cuenta, hoja Catalogos):**
```
Interna   (A->B):   Dashboard/gasto la ignora. A −monto, B +monto. Total SIN cambio.
Externa entrada (Cuenta Externa->A): A +monto. Total SUBE.
Externa salida  (A->Cuenta Externa): A −monto. Total BAJA.
```
Fórmula usa wildcard: `SUMIFS(..., Tarjeta, "*->"&cuenta)` = entradas, `SUMIFS(..., Tarjeta,
cuenta&"->*")` = salidas. Funciona igual en PC y móvil (dropdown nativo, sin texto libre).

**Por qué se cambió el diseño:** 2 columnas nuevas movían la posición de columnas existentes y
complicaba las fórmulas de saldo (2 lookups en vez de 1 parseo de string). El código compuesto en
una sola celda logra lo mismo con menos superficie de cambio.

---

## 3. Sesión 2026-07-17 — fixes adicionales

| Bug reportado | Causa | Fix |
|---|---|---|
| Dropdown Categoría no funciona cuando Tipo=Ingreso | `CatIngreso` era **named range multi-área** (2 rangos separados); `INDIRECT` no resuelve uniones | Convertido a rango contiguo |
| Fecha se reordena a mm-dd al teclear | Formato celda era `m/d/yyyy` (US) + configuración regional de LibreOffice en inglés | Formato celda → `DD-MM-YY`; falta cambiar configuración regional de LibreOffice a español (paso manual, ver abajo) |
| Saldo de una cuenta no reflejaba retiro real hacia otra cuenta | Movimiento inter-cuentas capturado como nota de texto, nunca como transacción | Pendiente manual: capturar como fila `Transferencia` con el código compuesto (§2) |
| `.ods` duplicado | — | Usuario confirmó: borrado. `.xlsx` es única fuente de verdad |

## 4. Sesión 2026-07-18 — fixes adicionales

| Cambio | Detalle |
|---|---|
| Resaltado visual Transferencia | Formato condicional: celda `Tipo` se pinta amarillo cuando valor = `Transferencia` (no rompe reglas verde/rojo Ingreso/Egreso ya existentes) |
| Doc de sesión | Reescrito: anonimizado (sin nombres de banco/monto), corregido vs. lo realmente implementado |

---

## 5. Próximos pasos (pendiente manual — son DATOS, no se editan por herramienta)

1. Migrar transferencias viejas capturadas como Ingreso+Egreso duplicado → 1 fila Transferencia
   con código compuesto.
2. Categorizar filas con Categoría vacía (fix #6).
3. Completar datos faltantes en Inversiones (días/tasa) para que la fórmula calcule.
4. Cambiar configuración regional de LibreOffice a español (México) para que el tecleo de fecha
   no reordene día/mes.

## 6. Pendiente de diseño (decisiones abiertas)

- Estructura final de KPIs del Dashboard: ¿agregar tabla presupuesto vs. real?
- Fechas de Inversiones a futuro — ¿proyección intencional o error de captura?
- Fijo vs. Variable por categoría (named ranges `Fijo`/`Variable` existen, sin usar aún).
- Migrar saldos iniciales (sumas manuales embebidas en fórmula) a un log de ajustes con
  fecha+motivo, más auditable.

---

## 7. Principios de operación — privacidad y soberanía de datos

- Datos financieros (cifras, transacciones, saldos, nombres de institución) permanecen
  exclusivamente en el `.xlsx` local de eldaniels — nunca en este doc ni en commits.
- Auditorías y ediciones se trabajan localmente (openpyxl/LibreOffice), sin sincronización a
  nube sin consentimiento explícito.
- Herramienta (Claude Code) edita solo lo técnico: fórmulas, referencias, dropdowns, formato
  condicional, named ranges. Nunca escribe ni modifica valores de transacciones/montos/fechas
  reales — esos los captura eldaniels a mano.
- Todo cambio de fórmula/lógica queda documentado aquí para auditoría posterior.
