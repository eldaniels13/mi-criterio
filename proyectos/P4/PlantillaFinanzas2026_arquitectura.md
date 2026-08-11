# PlantillaFinanzas2026.xlsx — arquitectura, decisiones e historial

> **Documento único.** Consolida `inbox/04-07-26_audit_finanzas2026.md` y
> `inbox/04-07-26_sesion_diseno_finanzas.md` (jul 2026) más la sesión de conciliación
> del 10-ago-2026. Actualizar **en su sitio**, no crear documentos nuevos por sesión.
>
> **Privacidad:** este doc no contiene cifras, saldos, ni nombres de instituciones
> financieras. Las cuentas se refieren por su posición (`Saldos!B30`, `B31`…) o como
> `Cuenta-A`, `Cuenta-B`. El mapeo real vive **solo** en el `.xlsx`, que está
> gitignored. Este archivo sí se versiona.
>
> **Para retomar con cualquier IA:** este `.md` + el `.xlsx` son suficientes. El `.md`
> explica el modelo, los invariantes y el porqué de cada decisión; el `.xlsx` aporta
> los nombres y las cifras. No hace falta precargar más contexto.

---

## 1. Qué es

Libro de finanzas personales en LibreOffice Calc. Registro manual de todos los
movimientos de dinero desde ene-2026, con conciliación contra los saldos reales que
eldaniels ve en las apps de sus bancos.

No es un proyecto de software. La hoja **es** el producto; los scripts solo la auditan.

**Hojas:** `Transacciones` · `Saldos` · `Inversiones` · `Dashboard` · `Listas`

---

## 2. Protocolo de trabajo (leer antes de tocar el archivo)

1. **Cerrar LibreOffice antes de escribir con openpyxl.** Si existe un `.~lock…#`, el
   archivo está abierto y escribir encima lo corrompe.
2. **Respaldar antes de editar**, fuera del repo:
   `~/Documents/Dineros/Finanzas personales/PlantillaFinanzas2026.bak-AAAAMMDD_HHMM.xlsx`
3. **Parchear en vivo, nunca regenerar.** Hay datos reales tecleados a mano; ningún
   script debe reconstruir el libro desde cero.
4. **openpyxl escribe fórmulas pero no las evalúa.** Tras guardar, hay que abrir el
   archivo en LibreOffice para que recalcule. Leer con `data_only=True` devuelve el
   último valor cacheado — `None` para fórmulas recién escritas.
5. **La herramienta edita solo lo técnico**: fórmulas, referencias, dropdowns, formato
   condicional, named ranges. **Nunca inventa ni modifica montos, fechas o
   descripciones reales** — esos los captura eldaniels a mano.
6. **Principio no negociable: no inventar nada.** Un hueco sin explicar se marca como
   hueco. No se cierra con un ajuste de conciliación salvo autorización explícita.
7. `proyectos/P4/audit_finanzas.py` es el auditor. Solo lectura, versionado, sin
   nombres de institución (los lee del `.xlsx`).

---

## 3. Modelo de datos

### `Transacciones` — una fila por movimiento físico

| Col | Campo | Notas |
|---|---|---|
| A | `Monto` | Siempre positivo. El signo lo da `Tipo`. |
| B | `Tipo` | `Ingreso` · `Egreso` · `Transferencia` |
| C | `Categoria` | Dropdown dependiente de `Tipo` (named ranges `CatIngreso`/`CatEgreso`/`CatTrans`) |
| D | `Tarjeta` | Cuenta. En transferencias, código compuesto `Origen->Destino` |
| E | `Fecha` | Formato `DD-MM-YY` |
| F | `Descripción` | Texto libre |

**Principio de diseño (explícito y defendido):** *un movimiento físico es exactamente
un renglón.* Las columnas `Mes`, `Año` y `Semana` se eliminaron — eran derivables de
`Fecha` y el Dashboard las obtendrá por agrupamiento automático de tabla dinámica.

### `Saldos` (antes `Catalogos`, renombrada 10-ago-2026)

Una fila por cuenta desde la 30. Encabezados en la fila 29.

| Col | Campo | Origen |
|---|---|---|
| C | Balance calculado | Fórmula (ver §4) |
| D | Saldo inicial | Dinero anterior a 2026 **únicamente** |
| E | Rendimientos | **Manual** — lo que la app del banco reporta como interés |
| F | Balance real actual | **Manual** — la verdad, tecleada desde la app |
| G | Diferencia | `=ROUND(C−F,2)` — debe ser 0 |

Filas 41-43: leyenda del semáforo. Fila 40: dinero total.

---

## 4. El invariante de conciliación (el corazón del libro)

```
C = D + Σ Ingresos − Σ Egresos + E + Σ transferencias_entrantes − Σ transferencias_salientes
G = ROUND(C − F, 2)   →   debe ser 0
```

**Semáforo en `G30:G39`:**

| Color | Condición | Diagnóstico |
|---|---|---|
| 🟢 Verde | `G = 0` | La cuenta cuadra con el banco |
| 🔴 Rojo claro | `G > 0` | El libro cree que hay **más** dinero del que existe → falta registrar un egreso, o hay un ingreso/transferencia duplicado |
| 🔴 Rojo fuerte | `G < 0` | El libro cree que hay **menos** dinero del que existe → falta registrar un ingreso o rendimiento, o hay un egreso duplicado |

Cualquier rojo es error de registro. La meta permanente es toda la columna en verde.
Explicación completa en el comentario de `Saldos!G29`.

**`G40` es la excepción semántica:** no es un descuadre sino `=ROUND(SUM(F30:F39),2)`,
el dinero total. Verde si es positivo, rojo fuerte si es negativo (deber más de lo que
se tiene = problema crítico).

### Por qué `E` (rendimientos) es manual y debe seguir siéndolo

Se propuso calcular los rendimientos con fórmulas de interés compuesto, alimentadas
por las tasas de cada banco y la trayectoria de la tasa de referencia de Banxico.
**Se descartó, y la razón importa:**

> Los bancos capitalizan diario con su propio redondeo, cambian tasa sin avisar y
> aplican retención de ISR. Cualquier modelo de tasa da un número *parecido* pero
> nunca *igual*, y eso rompería el invariante `G = 0`.

En cambio, teclear lo que la app reporta hace que `G = 0` funcione como **doble
verificación**: valida el registro de movimientos *y* que el rendimiento observado
coincida con el esperado. El rendimiento se deriva por resta, exacto, sin modelar nada.

Corolario útil: la *tasa implícita* (`rendimiento ÷ capital × 365/días`) mide sola la
caída de tasas de Banxico sin necesidad de investigarla. Pendiente de agregar a
`Inversiones`.

### Regla del saldo inicial

**`D` contiene únicamente dinero anterior a 2026.** Si una fila de `Transacciones`
de 2026 aporta ese capital, ponerlo también en `D` lo cuenta dos veces. Esta fue la
causa de dos descuadres reales (§6). Excepción legítima: una inversión hecha en 2025
que no tiene fila en este libro — ahí `D` es su saldo de apertura al 01-01-26.

---

## 5. Modelo de transferencias

`Tipo = "Transferencia"` y la columna `Tarjeta` recibe el código compuesto
`Cuenta-A->Cuenta-B` desde un dropdown (named range `TransCodes` en `Listas`, con
todas las permutaciones más `Cuenta Externa`).

```
Interna         (A->B)               A −monto, B +monto.  Total sin cambio.
Entrada externa (Cuenta Externa->A)  A +monto.            Total sube.
Salida externa  (A->Cuenta Externa)  A −monto.            Total baja.
```

Las fórmulas usan comodín:
`SUMIFS(…, Tarjeta, "*->"&cuenta)` = entradas · `SUMIFS(…, Tarjeta, cuenta&"->*")` = salidas.

**Por qué código compuesto en vez de dos columnas `Origen`/`Destino`:** dos columnas
nuevas desplazaban las existentes y obligaban a dos lookups en vez de un parseo. El
código compuesto logra lo mismo con menos superficie de cambio y funciona igual en
móvil (dropdown nativo, sin texto libre).

**Riesgo conocido y aceptado:** una transferencia escrita sin `->` es **ignorada en
silencio** por el comodín — la hoja miente sin avisar. `audit_finanzas.py` detecta
este caso y también las transferencias hacia cuentas no dadas de alta.

**Mejora pendiente (aprobada, no construida):** migrar a columnas `Origen` + `Destino`
con validación por dropdown contra la lista de cuentas. Elimina el riesgo de typo y
el matching por comodín. Requiere reescribir las fórmulas de `Saldos`.

---

## 6. Clases de error encontradas (catálogo de diagnóstico)

Cada una causó un descuadre real. Sirven como checklist cuando `G ≠ 0`.

| # | Clase | Síntoma | Cómo se detecta |
|---|---|---|---|
| 1 | Transferencia sin `->` | Desaparece de ambos lados | `audit_finanzas.py` |
| 2 | Doble registro por método antiguo | Un movimiento anotado como "desde X" *y* "a Y", ambos convertidos a formato flecha | Buscar mismo monto + misma fecha entre dos cuentas |
| 3 | Sub-cuenta fantasma | El padre parece retener dinero que ya movió a un instrumento no dado de alta | Transferencia hacia cuenta inexistente |
| 4 | Saldo inicial duplicado | `D` incluye capital que también entra por una fila de 2026 | Comparar `D` contra las transferencias de entrada |
| 5 | Origen mal atribuido | Transferencia marcada desde el padre cuando salió de la sub-cuenta | Solo por memoria del usuario / app |
| 6 | Match parcial de nombre | Una cuenta absorbe los movimientos de su sub-cuenta (`X` capturando `X Plus`) | Usar comparación exacta, nunca `in` |
| 7 | Residuo de punto flotante | `G` se ve como 0 pero vale ~1e-12, el semáforo lo pinta rojo | Resuelto en la raíz con `ROUND(…,2)` |
| 8 | Columna `E` mal cableada | Solo una fila sumaba `E` en su fórmula `C` | Comparar las fórmulas `C` entre filas |

**Errores históricos ya cerrados (jul-2026):** Dashboard con `#ref!` por funciones
localizadas de LibreOffice (`si.error`, `sumar.si.conjunto`) que no migran al guardar
como `.xlsx`; Dashboard filtrando `"Gasto"` cuando los datos dicen `"Egreso"`;
categorías fantasma sin match; promedio mensual mal calculado con `#DIV/0!` en enero;
named range multi-área que `INDIRECT` no resuelve; fecha reordenada a mm-dd por
formato US + configuración regional en inglés.

---

## 7. Estado al 10-ago-2026

- **Conciliación cerrada.** Las 9 cuentas con saldo real conocido dan `G = 0`.
- `Catalogos` renombrada a `Saldos` (27 fórmulas y 4 named ranges actualizados).
- Semáforo y leyenda funcionando; `G40` con su propia regla de signo.
- Efectivo **deliberadamente fuera del control**: el volumen es bajo y difícil de
  rastrear, así que el dinero que sale a efectivo se considera gastado en el momento.
  Sus filas históricas se conservan como registro; su balance se ignora (`C = 0`).
- `audit_finanzas.py` reescrito: sin nombres de institución, detecta transferencias
  malformadas y cuentas huérfanas, deriva la lista de cuentas del propio libro.

### Pendientes

1. **Dashboard** — siguiente etapa. Ver `contexto_dashboard_claude_web.md`.
2. Borrar el bloque `Saldos!A1:D28` (KPIs que pertenecen al Dashboard) **después** de
   verificar que el Dashboard reproduce esas métricas.
3. `Inversiones`: agregar columna de tasa implícita; incorporar todos los instrumentos.
4. Migrar `Tarjeta` a `Origen` + `Destino` con dropdown (§5).
5. Migrar los saldos iniciales (hoy sumas manuales embebidas en la fórmula, tipo
   `=1234+56+78`) a un log de ajustes con fecha y motivo, más auditable.
6. Formalizar Fijo vs Variable por categoría (los named ranges existen, sin usar).
7. Categorizar las filas con `Categoria` vacía.
8. Configuración regional de LibreOffice a español (México) para que el tecleo de
   fecha no reordene día/mes.

---

## 8. Soberanía de datos

- Cifras, transacciones, saldos y nombres de institución viven **exclusivamente** en el
  `.xlsx` local. Está gitignored (`.gitignore:133`) y no debe salir del equipo.
- Los respaldos van fuera del repo, en `~/Documents/Dineros/Finanzas personales/`.
- Este documento y `audit_finanzas.py` sí se versionan, y deben permanecer libres de
  información sensible o rastreable. Antes de commitear, verificar que no se colaron
  nombres de banco ni montos.
- Sin sincronización a la nube sin consentimiento explícito.
