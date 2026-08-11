# Contexto para claude.ai — construir el Dashboard con tablas dinámicas

> **Cómo usar este archivo:** abrir una conversación nueva en claude.ai, adjuntar o
> pegar este documento completo, y empezar. Es autocontenido: no hace falta más
> contexto. El `.xlsx` no se sube (contiene datos financieros reales); todo lo que la
> IA necesita saber de su estructura está descrito aquí.

---

## Quién soy y qué quiero

Soy eldaniels, ingeniero mecánico con Python y C# funcionales. Aprendo haciendo:
prefiero ejemplos ejecutables y pasos concretos sobre teoría abstracta.

**Quiero aprender a construir tablas dinámicas en LibreOffice Calc**, no que me
entreguen el archivo hecho. Explícame el porqué de cada paso para poder repetirlo y
modificarlo solo después.

**Objetivo concreto:** un Dashboard donde pueda filtrar por semana, mes o año, elegir
categoría, y cambiar el tipo de gráfico — lo más fácil posible de configurar y
personalizar.

Sé crítico con mis ideas. Si algo que propongo es mala idea, dímelo directamente con
la razón; prefiero eso a que me sigas la corriente.

---

## Entorno

- **Arch Linux**, escritorio COSMIC
- **LibreOffice Calc** (no Excel). Importa: los nombres de menú, los atajos y las
  limitaciones de las tablas dinámicas difieren de Excel. Si algo solo existe en
  Excel, dímelo en lugar de darme pasos que no puedo seguir.
- El archivo es `.xlsx`. **Las fórmulas deben escribirse en inglés**
  (`SUMIFS`, `IFERROR`) — ya me pasó que al guardar en `.xlsx` las funciones
  localizadas (`sumar.si.conjunto`, `si.error`) se rompen y todo queda en `#ref!`.

---

## Estructura del libro

Cinco hojas: `Transacciones` · `Saldos` · `Inversiones` · `Dashboard` · `Listas`

### `Transacciones` — la fuente de datos (~500 filas, ene–ago 2026)

| Col | Campo | Contenido |
|---|---|---|
| A | `Monto` | Número, **siempre positivo**. El signo lo determina `Tipo`. |
| B | `Tipo` | Exactamente tres valores: `Ingreso`, `Egreso`, `Transferencia` |
| C | `Categoria` | Texto desde dropdown (~24 categorías: comida, transporte, recreación, internet/movil, sueldo, etc.) |
| D | `Tarjeta` | Cuenta. En transferencias trae `Origen->Destino` en una sola celda |
| E | `Fecha` | Fecha real, formato `DD-MM-YY` |
| F | `Descripción` | Texto libre |

Encabezados en la fila 1, datos desde la fila 2.

**No existen columnas Mes, Año ni Semana.** Las eliminé a propósito: eran derivables
de `Fecha` y quiero que la tabla dinámica agrupe por fecha automáticamente. Esta
decisión ya está tomada — si crees que es un error, dilo, pero el punto de partida es
sin columnas auxiliares.

### `Saldos`

Una fila por cuenta desde la 30, con saldo calculado, saldo real y una columna de
diferencia que debe dar 0 (semáforo verde/rojo). Esta hoja ya está terminada y
conciliada. **El Dashboard no debe tocarla.**

El bloque `A1:D28` de esa hoja tiene KPIs viejos que quiero migrar al Dashboard y
luego borrar de ahí.

---

## Reglas de negocio que el Dashboard debe respetar

1. **`Transferencia` no es gasto ni ingreso.** Son movimientos entre mis propias
   cuentas. Si se cuentan, inflan los totales por partida doble. Todo cálculo de gasto
   o ingreso debe excluir `Tipo = "Transferencia"`.

2. **El literal correcto es `"Egreso"`, no `"Gasto"`.** Ya me quemé con esto: el
   Dashboard filtraba `"Gasto"` y todos los totales salían en cero.

3. **Las categorías deben salir de los datos reales**, no inventarse. Otro error
   pasado: el Dashboard usaba nombres de categoría que no existían en `Transacciones`
   y nunca hacían match.

---

## Qué quiero ver en el Dashboard

Del diseño que ya había esbozado:

- **Cuatro tarjetas KPI arriba:** Ingreso del mes · Egreso del mes · **Ahorro** ·
  Saldo líquido total
- **Tabla dinámica debajo**, filtrable por periodo y categoría
- Gráfico configurable conectado a la dinámica

El número que más me importa es el **ahorro** (ingreso real menos egreso real,
excluyendo transferencias). Tengo una nota de una sesión pasada que quiero respetar:

> *"El número que importa estaba enterrado en la fila 44 de otra hoja, no en el
> Dashboard. Una buena hoja lo pone al frente."*

---

## Lo que necesito aprender, en orden

1. **Cómo se crea una tabla dinámica en LibreOffice Calc** partiendo de un rango con
   encabezados. Qué es campo de fila, de columna, de datos y de filtro, y cómo decidir
   qué va en cada zona.

2. **Agrupamiento automático por fecha.** Esta es la parte clave. Quiero poder ver los
   mismos datos por año, por mes o por semana sin agregar columnas auxiliares.
   Necesito saber si LibreOffice agrupa por semana igual que por mes, y qué hacer si
   no.

3. **Filtros interactivos.** Qué equivalente hay en LibreOffice a los segmentadores
   (slicers) de Excel, y cómo dejar el filtro de categoría cómodo de usar.

4. **Conectar un gráfico a la dinámica** para que se actualice al cambiar el filtro, y
   cómo cambiar el tipo de gráfico sin rehacerlo.

5. **Las tarjetas KPI.** Si conviene sacarlas de la tabla dinámica con `GETPIVOTDATA`,
   o calcularlas aparte con `SUMIFS` — con las ventajas y desventajas de cada opción.

6. **Cuándo se actualiza una tabla dinámica.** Entiendo que no es automática al
   agregar filas nuevas. Quiero saber cómo refrescarla y cómo hacer que el rango
   crezca solo cuando capturo movimientos nuevos.

---

## Cómo prefiero que me respondas

- Una cosa a la vez. Espera mi confirmación antes de pasar al siguiente paso.
- Pasos concretos con nombres reales de menú de LibreOffice.
- Cuando haya una decisión de diseño, dame la recomendación y el porqué, no un
  catálogo de opciones.
- No me pidas los datos reales del archivo. Trabaja con la estructura descrita aquí;
  si necesitas saber un valor concreto, pregúntame y yo lo verifico en mi máquina.

---

## Al terminar

Resume las decisiones tomadas en bullets que pueda pegar de vuelta en Claude Code
(donde tengo el archivo y las herramientas de edición) para aplicar lo que no se pueda
hacer a mano. Aviso: openpyxl **no puede crear tablas dinámicas** — solo leerlas y
conservarlas. Así que la construcción es manual en LibreOffice, que es justo lo que
quiero aprender.
