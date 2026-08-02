# Auditoría + Diseño — PlantillaFinanzas2026.xlsx

> **Fecha:** 2026-07-04 · **Archivo:** `proyectos/P4/PlantillaFinanzas2026.xlsx`
> **⚠️ SENSIBLE:** contiene cifras financieras reales. NO commitear sin filtrar. Vive en `inbox/`.
> **Objetivo:** auditar la hoja, abrir conversación de diseño, y dejar un prompt para continuar por voz en el celular.

---

## 1. Contexto

Hoja de finanzas personales (subproyecto Excel activo, P4↔P2). 4 hojas, **465 transacciones
reales** (ene–jul 2026). El motor de captura (dropdowns dependientes) funciona; el **Dashboard
está 100% roto** y hay inconsistencias de modelo de datos que hacen que varios totales mientan.

**Snapshot actual (valores cacheados):**

| Métrica | Valor |
|---|---|
| Ingresos Real (sin transferencias) | [redactado] |
| Egresos Real (sin transferencias) | [redactado] |
| **Gasto Real (Ing − Egr)** | **[redactado]** ← gastas más de lo que entra |
| Inversiones (MontoInicial → Final) | [redactado] |

Saldos por tarjeta: [cifras y nombres de institución redactados — datos de sesión, no permanentes]

> [!] Punto ciego financiero: el número que importa (gasto real neto) estaba enterrado en la fila 44 de
> `Catalogos`, no en el Dashboard. Una buena hoja lo pone al frente.

---

## 2. Auditoría — 8 errores (qué falla · por qué · fix)

| # | Hoja | Qué falla | Por qué | Fix |
|---|------|-----------|---------|-----|
| 1 | **Dashboard** | Toda fórmula da `#ref!` | Se escribió en LibreOffice con funciones localizadas (`si.error`, `sumar.si.conjunto`); al guardar como `.xlsx` los nombres ES no migran y la referencia de semana se rompió | Reconstruir en inglés: `IFERROR` + `SUMIFS` |
| 2 | **Dashboard** | Todos los gastos salen 0 | Filtra `Tipo = "Gasto"`, pero los datos usan `"Egreso"` | Cambiar literal a `"Egreso"` |
| 3 | **Dashboard** | Categorías nunca hacen match | Usa nombres fantasma (`Internet`, `Celular – movil`, `cerro`, `ropa`, `calzado`) que no existen en los datos (`internet/movil`, `cerro camping`; no hay ropa/calzado) | Alinear a las 24 categorías reales |
| 4 | **Catalogos** col D | "Promedio Mensual" mal + `#DIV/0!` en enero | `AVERAGEIF(...)/(MONTH(TODAY())−1)`: AVERAGEIF ya promedia por transacción, dividir otra vez no da promedio mensual; y en enero `MONTH−1 = 0` | `SUMIF(...) / nº_meses_con_datos` |
| 5 | **Inversiones** | SUMA de MontoFinal incompleta | Filas `[cripto]` (5) y `[cuenta-app]` (6) no tienen fórmula G/H de interés compuesto | Rellenar `MontoFinal`/`InterésGanado` o excluir de la suma |
| 6 | **Transacciones** | 16 filas sin categoría | Captura sin seleccionar del dropdown | Categorizar (o marcar `otros`) |
| 7 | **Transacciones** | Dropdown Tarjeta no ofrece [cripto]/[broker] | La validación apunta a `Catalogos!B30:B35`; [cripto] y [broker] están en B36:B37 (fuera de rango) | Extender rango a `B37` |
| 8 | **Archivo** | Riesgo de corrupción al editar | Lock `.~lock…#` activo = abierto en LibreOffice; escribir con openpyxl encima corrompe | **Cerrar LibreOffice antes de aplicar fixes** |

---

## 3. Conversación de diseño (preguntas → sugerencia)

Para pasar de "hoja que registra" a "hoja que te dice qué hacer". Responde por voz; cada bloque
tiene mi recomendación por defecto.

### A. Modelo de datos
1. **Tipo:** ¿mantener `Ingreso`/`Egreso` como texto, o migrar a **monto con signo** (+/−)?
   *Sugerencia:* mantener texto (los dropdowns ya dependen de él), pero fijar el vocabulario en un
   solo lugar. Nunca volver a escribir "Gasto".
2. **Transferencias:** hoy 66 filas `transferencia` inflan ingresos y egresos, y las restas a mano
   en `Catalogos` C42/C43. ¿Quieres una **hoja/columna aparte de movimientos internos** que nunca
   entre al cálculo de gasto? *Sugerencia:* sí — un flag `EsTransferencia` limpia todo el ruido.

### B. Categorías (24 actuales)
3. ¿Consolidamos duplicados/typos? (`internet/movil` aparece con varios nombres entre hojas).
4. ¿Formalizamos **Fijo vs Variable**? Ya existen los named ranges `Fijo`/`Variable` sin usar.
   *Sugerencia:* etiquetar cada categoría como Fijo/Variable → permite presupuesto y % automático.

### C. Dashboard (lo reconstruimos de cero)
5. ¿Qué KPIs quieres ver primero al abrir? Opciones: gasto semana actual · gasto mes actual ·
   **presupuesto vs real por categoría** · saldo total líquido · tasa de ahorro · top-5 gastos.
   *Sugerencia:* 4 tarjetas arriba (Ingreso mes, Egreso mes, Ahorro, Saldo líquido) + tabla
   presupuesto-vs-real debajo.
6. ¿Semana natural (WEEKNUM ya está en col H) o últimos 7 días rodantes?

### D. Inversiones
7. Fechas de inicio en **nov-2026** (futuro) — ¿son proyecciones o error de captura?
8. ¿Agregar columna de **liquidez** (fecha en que puedes retirar)? Encaja con tu criterio
   "aversión a activos sin liquidez <2 años".

### E. Saldos por tarjeta
9. Los saldos iniciales están como **sumas manuales embebidas** (ej. `=<cifras>+…`) en la
   col D → frágiles e imposibles de auditar. ¿Migramos a un **log de ajustes** con fecha y motivo?

### F. Higiene
10. Fórmulas basura arrastradas hasta la fila 3021 (datos reales hasta 466) → inflan el archivo.
    ¿Limpio el arrastre y uso rango dinámico? *Sugerencia:* sí.
11. Existe un `.ods` duplicado del mismo archivo. ¿Cuál es la fuente de verdad, `.xlsx` o `.ods`?

---

## 4. Sugerencias concretas (para cuando editemos)

- Reconstruir Dashboard con `SUMIFS`/`IFERROR` en inglés, categorías reales, `"Egreso"`.
- Añadir hoja `Presupuesto` (categoría → tope mensual) y comparar vs real.
- Columna `EsTransferencia` para excluir movimientos internos del gasto.
- Poner el número clave (Ahorro del mes) como primer KPI visible.
- Limpiar arrastre de fórmulas > fila 466; extender dropdown Tarjeta a B37.
- Rellenar fórmulas de interés en Inversiones filas 5–6.

---

## 5. 📋 PROMPT VOZ — pegar/dictar en IA móvil

> Copia este bloque a Claude/ChatGPT del celular para seguir el diseño por voz. Es autocontenido.

```
Soy eldaniels, ingeniero mecánico. Estoy rediseñando mi hoja de finanzas personales
"PlantillaFinanzas2026.xlsx" (LibreOffice/openpyxl). Tú me guías por voz con preguntas
y sugerencias; no des recomendaciones de inversión, solo marcos.

ESTRUCTURA: 4 hojas.
- Transacciones: Monto, Tipo (Ingreso/Egreso), Categoria, Tarjeta, Fecha, Mes, Año, Semana,
  Descripción. 465 filas reales (ene-jul 2026). Dropdowns dependientes: Categoria depende de
  Tipo vía named ranges CatIngreso/CatEgreso.
- Catalogos: SUMIF por categoría (24 cats) + saldos por tarjeta + resumen gasto real.
- Inversiones: interés compuesto EA/NA.
- Dashboard: ROTO.

SNAPSHOT: [cifras redactadas — gasto real neto negativo, gasto más de lo que entra].
Una cuenta con saldo negativo [cifra redactada].

8 BUGS: (1) Dashboard todo #ref por funciones localizadas LibreOffice. (2) Dashboard filtra
"Gasto" pero datos usan "Egreso". (3) categorías fantasma no hacen match. (4) Catalogos promedio
mensual mal calculado + div/0 en enero. (5) Inversiones filas [cripto]/[app] sin fórmula.
(6) 16 filas sin categoría. (7) dropdown Tarjeta excluye [cripto]/[broker]. (8) editar con archivo
abierto corrompe.

DECISIONES ABIERTAS que quiero resolver hablando:
- Transferencias (66 filas) inflan los totales: ¿columna/flag para excluirlas?
- ¿Formalizo Fijo vs Variable por categoría para presupuesto?
- ¿Qué KPIs pongo en el Dashboard nuevo (ahorro del mes, presupuesto vs real, saldo líquido)?
- Saldos de tarjeta son sumas manuales frágiles: ¿migrar a log de ajustes?
- Fechas de inversión en nov-2026: ¿proyección o error?

Hazme UNA pregunta a la vez, empezando por el modelo de datos (transferencias). Al final
resume mis decisiones en bullets que pueda pegar de vuelta en mi laptop para codear los cambios
con openpyxl.
```

---

## 6. Continuar codeando aquí (laptop)

Al retomar en Claude Code:
1. **Cerrar LibreOffice** (borrar/liberar `.~lock…#`) antes de tocar el `.xlsx`.
2. Leer con `markitdown` (valores) + `openpyxl` (fórmulas), escribir con `openpyxl`, guardar
   (regla [[feedback-excel-tools]]).
3. Aplicar fixes en orden: #8 (cerrar) → #2/#3/#1 (Dashboard) → #7 (dropdown) → #4 (promedio)
   → #5 (inversiones) → #6 (categorizar).
4. **Pedir permiso antes de cada edición del `.xlsx`.**
5. Al terminar el diseño, actualizar `proyectos/P4/P4_finanzas_inversiones.txt` y NO commitear
   cifras: filtrar este doc primero.
