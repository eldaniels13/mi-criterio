# INSTRUCCIONES PARA GENERAR EXCEL DE CONTROL DE VIÁTICOS Y FACTURAS (MÉXICO)

## DESCRIPCIÓN GENERAL
Este Excel está diseñado para centralizar el registro de gastos de viáticos (gasolina, comidas, hoteles, teléfono) y sus movimientos financieros asociados (anticipos y reembolsos). Está optimizado para la operación en México (RFC, IVA del 16%) y pensado para que el dueño de la empresa y el contador puedan revisar la información en segundos gracias a un panel de resumen ejecutivo, gráficos y formato condicional. La estructura es expandible para incluir proveedores externos en el futuro sin romper las fórmulas existentes.

## OBJETIVOS CLAVE
1. Registrar **ingresos y egresos** (anticipos, reembolsos y gastos reales).
2. Asignar un **folio descriptivo y cronológico** a cada movimiento.
3. Vincular cada registro con su archivo PDF mediante **hipervínculos** funcionales.
4. Evitar errores de tipeo usando **listas desplegables** y **búsquedas automáticas** de RFC.
5. Mostrar un **resumen financiero** (total gastado, IVA recuperable, saldo por reembolsar).
6. Proteger las celdas con fórmulas para que solo se editen los datos de entrada.

---

## ESTRUCTURA DE ARCHIVOS (CARPETA COMPARTIDA)
- Ruta base sugerida: `\\Servidor\Finanzas\Viaticos\`
- Subcarpeta: `PDFs\` (aquí se guardan los archivos con el nuevo formato).
- El Excel debe estar en la raíz de esta carpeta para que los hipervínculos relativos funcionen.

### NUEVO FORMATO PARA NOMBRAR LOS PDF
**Formato sugerido (obligatorio para el hipervínculo):**
`FOLIO_Empleado_Categoria.pdf`
*Ejemplo:* `VIA-2026-001_Daniel_Gasolina.pdf`

*Razón del cambio:* El formato anterior (`FactElect_Daniel_Gasolina1377.22pesos`) no era cronológico ni permitía búsquedas rápidas. El nuevo formato incluye el **Folio exacto** que genera el Excel, lo que garantiza que el hipervínculo siempre encuentre el archivo.

---

## PESTAÑA 1: "Catálogo_Empleados" (Origen de datos)
| Columna | Nombre | Tipo | Descripción |
| :--- | :--- | :--- | :--- |
| A | ID | Número | 1, 2, 3... |
| B | Nombre_Empleado | Texto | Ej. "Daniel", "María" |
| C | RFC | Texto | Ej. "DANI123456ABC" |
| D | Puesto | Texto | Opcional (Ej. "Vendedor") |

**Instrucciones para el agente:**
- Crear 3 filas de ejemplo (Daniel, María, Juan) con RFCs ficticios.
- Esta tabla se usará para el menú desplegable en el Registro.

---

## PESTAÑA 2: "Registro" (Base de datos principal)
**Estructura de columnas (de la A a la L):**

| Col | Encabezado | Fórmula / Validación | Explicación |
| :--- | :--- | :--- | :--- |
| **A** | **Folio** | `="VIA-"&TEXTO(AÑO(B2);"00")&"-"&TEXTO(FILA()-1;"000")` | Autonumérico por año. Ej. VIA-26-001. **Protegida**. |
| **B** | **Fecha** | Formato dd/mm/aaaa | Fecha del gasto o anticipo. |
| **C** | **Empleado** | Validación: Lista desde `Catálogo_Empleados!B:B` | Seleccionar el nombre. |
| **D** | **RFC** | `=XLOOKUP(C2; Catálogo_Empleados!B:B; Catálogo_Empleados!C:C; "No encontrado")` | Se autocompleta al elegir el empleado. **Protegida**. |
| **E** | **Categoría** | Validación: Lista (`Gasolina`, `Comidas`, `Hospedaje`, `Teléfono`, `Otros`, `Proveedor`) | Permite expansión futura (ej. proveedores). |
| **F** | **Tipo_Mov** | Validación: Lista (`Gasto`, `Anticipo`, `Reembolso`) | *Gasto* = comprobante de egreso. *Anticipo* = dinero entregado al empleado (ingreso). *Reembolso* = devolución de dinero sobrante. |
| **G** | **Subtotal** | Número (solo entrada manual) | Base gravable del gasto (sin IVA). Para Anticipos/Reembolsos, escribir 0 o el monto sin IVA. |
| **H** | **IVA** | `=SI(F2="Gasto"; G2*0.16; 0)` | IVA del 16% aplica SOLO a gastos. **Protegida**. |
| **I** | **Total** | `=G2+H2` | Suma total del movimiento. **Protegida**. |
| **J** | **Estatus** | Validación: Lista (`Pendiente`, `Pagado`, `Reembolsado`) | Estado financiero del registro. |
| **K** | **Hipervínculo** | `=HIPERVINCULO("PDFs\"&A2&"_"&C2&"_"&E2&".pdf"; "Ver PDF")` | Busca el archivo en la subcarpeta. **Protegida**. |
| **L** | **Observaciones** | Texto libre | Notas adicionales (ej. "Comida con cliente"). |

**Formato Condicional (Registro):**
- **Fila completa en ROJO** si `Estatus = "Pendiente"` Y `Hoy() > Fecha + 15` (vencido).
- **Fila completa en VERDE** si `Estatus = "Pagado"` o `"Reembolsado"`.
- **Fila completa en AMARILLO** si `Estatus = "Pendiente"` Y `Hoy() <= Fecha + 15` (a tiempo).

---

## PESTAÑA 3: "Resumen_Ejecutivo" (Dashboard para el jefe)
| Indicador | Fórmula / Configuración |
| :--- | :--- |
| **Total Gastos (Egresos)** | `=SUMAR.SI(Registro!F:F; "Gasto"; Registro!I:I)` |
| **Total Anticipos (Ingresos)** | `=SUMAR.SI(Registro!F:F; "Anticipo"; Registro!I:I)` |
| **Total Reembolsos (Ingresos)** | `=SUMAR.SI(Registro!F:F; "Reembolso"; Registro!I:I)` |
| **Saldo por Reembolsar** | `=Total_Anticipos - Total_Gastos` (si es negativo, falta dinero). |
| **IVA Repercutido / Acreditable** | `=SUMAR.SI(Registro!F:F; "Gasto"; Registro!H:H)` |
| **Conteo de Facturas** | `=CONTARA(Registro!A:A)-1` |

**Visualizaciones:**
1. **Gráfico de Barras**: Gastos totales por `Categoría` (usar `SUMAR.SI.CONJUNTO` o tabla dinámica simple).
2. **Gráfico Circular**: Proporción de `Estatus` (Pendiente vs Pagado).

---

## CONFIGURACIÓN DE PROTECCIÓN
- **Desbloquear** solo las columnas de entrada: `Fecha` (B), `Empleado` (C), `Categoría` (E), `Tipo_Mov` (F), `Subtotal` (G), `Estatus` (J), `Observaciones` (L).
- **Bloquear** el resto de columnas (A, D, H, I, K) y toda la hoja de Resumen.
- Activar **Proteger Hoja** con contraseña (opcional, sugerencia: `admin123` para evitar borrados accidentales, aunque el jefe pueda pedirla).

---

## INSTRUCCIONES DE CÓDIGO PARA EL AGENTE (CLAUDE CODE)
1. **Generar el archivo `Control_Viaticos.xlsx`** usando `openpyxl`.
2. **Crear las tres hojas** con los nombres exactos.
3. **Aplicar los estilos**:
   - Encabezados en negrita, fondo gris oscuro (#404040), texto blanco.
   - Ajustar el ancho de columnas automáticamente (especialmente la K para hipervínculos).
   - Aplicar formato de moneda ($) a columnas G, H, I.
4. **Insertar las fórmulas** en las celdas correspondientes de la fila 2 hacia abajo (el agente debe propagarlas al menos hasta la fila 500 usando `copy` o asignación directa).
5. **Configurar las validaciones de datos** (listas desplegables) para las columnas C, E, F, J.
6. **Aplicar el formato condicional** a todo el rango de datos (A2:L500) usando las reglas de colores (Rojo, Verde, Amarillo).
7. **Agregar los gráficos** en la pestaña de Resumen (insertar objetos de gráfico con datos de ejemplo).
8. **Incluir un bloque de notas** en la celda A1 de la pestaña "Registro" que diga: *"Para vincular PDF, guarda los archivos en la carpeta 'PDFs' con el formato: Folio_Empleado_Categoria.pdf"*.

---

## NOTAS ADICIONALES PARA EL USO DIARIO
- **Al agregar un nuevo registro**, el empleado escribe la fecha, elige al empleado (el RFC aparece solo), escribe el subtotal, selecciona la categoría y el tipo. El folio, IVA, total e hipervínculo se generan automáticamente.
- **Para expandir a proveedores externos** en el futuro, solo se añade "Proveedor" a la lista de categorías y se desbloquea una columna adicional "Nombre_Proveedor" sin afectar el resto.
- **Relación Ingresos/Egresos**: El jefe ve en el resumen si los anticipos cubren los gastos. Si el "Saldo por Reembolsar" es positivo, el empleado debe devolver dinero; si es negativo, la empresa debe más dinero al empleado.

---

*Fin de las instrucciones.*