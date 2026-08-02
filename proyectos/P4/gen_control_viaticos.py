#!/usr/bin/env python3
"""Genera Control_Viaticos.xlsx desde cero (bootstrap / referencia).
NOTA: correrlo sobre el archivo en uso borra los registros ya capturados.
Para editar el archivo real usar un patch dirigido (load_workbook + guardar),
no este generador. Ver historial de la sesion 16-07-26 en mi-criterio."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.marker import DataPoint
from openpyxl.chart.shapes import GraphicalProperties

OUT = "/home/eldaniels/Codes/mi-criterio/proyectos/P4/Control_Viaticos.xlsx"

HEADER_FILL = PatternFill(start_color="404040", end_color="404040", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF")
THIN = Side(style="thin", color="B0B0B0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CURRENCY_FMT = '"$"#,##0.00'
RED_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
GREEN_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

DATA_FIRST_ROW = 3
DATA_LAST_ROW = 500
PDF_PATH = "Z:\\DANIEL\\Facturas"
EMPLEADOS = ["Daniel", "Mathias", "Karla", "Noa", "Sacha", "Louis", "Raphael"]

# Columnas Registro: A Folio, B Fecha, C Empleado, D Categoría, E Tipo_Mov,
# F Subtotal, G IVA, H Total (INPUT), I Responsable_Pago, J Hipervínculo,
# K Observaciones, L Archivo_Manual (override de nombre de PDF/imagen)
LAST_COL = 12  # L

wb = Workbook()

# ---------- Sheet 1 (order): Registro ----------
ws2 = wb.active
ws2.title = "Registro"

note = (f"Para vincular PDF, guarda los archivos en '{PDF_PATH}' con el formato: "
        "Folio_Empleado_Categoria.pdf — o llena 'Archivo_Manual' si el nombre real "
        "no sigue esa convención (ej. capturas de Louis tipo 14-07-2026 14_38_919.jpg)"
        " | ⚠ Contraseña de protección removida: cualquiera puede desproteger la hoja"
        " sin pedir clave. Verifica antes de editar columnas bloqueadas (fórmulas).")
ws2.merge_cells("A1:L1")
note_cell = ws2["A1"]
note_cell.value = note
note_cell.font = Font(italic=True, color="404040")
note_cell.alignment = Alignment(wrap_text=True, vertical="center")
ws2.row_dimensions[1].height = 30

headers2 = ["Folio", "Fecha", "Empleado", "Categoría", "Tipo_Mov",
            "Subtotal", "IVA", "Total", "Responsable_Pago", "Hipervínculo", "Observaciones",
            "Archivo_Manual (opcional)"]
for c, h in enumerate(headers2, start=1):
    cell = ws2.cell(row=2, column=c, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.border = BORDER
    cell.alignment = Alignment(horizontal="center")

for r in range(DATA_FIRST_ROW, DATA_LAST_ROW + 1):
    ws2.cell(row=r, column=1,
              value=f'="VIA-"&TEXT(MOD(YEAR(B{r}),100),"00")&"-"&TEXT(ROW()-2,"000")')
    ws2.cell(row=r, column=6, value=f'=IF(E{r}="Gasto",H{r}/1.16,H{r})')       # Subtotal (derivado de Total)
    ws2.cell(row=r, column=7, value=f'=H{r}-F{r}')                             # IVA
    ws2.cell(row=r, column=10,                                                 # Hipervínculo
              value=(f'=HYPERLINK("{PDF_PATH}\\"&IF(L{r}="",A{r}&"_"&C{r}&"_"&D{r}&".pdf",L{r}),'
                     f'"Ver PDF")'))
    for c in range(1, LAST_COL + 1):
        ws2.cell(row=r, column=c).border = BORDER
    ws2.cell(row=r, column=2).number_format = "dd/mm/yyyy"
    for c in (6, 7, 8):
        ws2.cell(row=r, column=c).number_format = CURRENCY_FMT

widths2 = [14, 12, 16, 14, 12, 12, 12, 12, 14, 12, 28, 30]
for c, w in zip("ABCDEFGHIJKL", widths2):
    ws2.column_dimensions[c].width = w

# Data validations
dv_empleado = DataValidation(type="list", formula1=f'"{",".join(EMPLEADOS)}"', allow_blank=True)
dv_categoria = DataValidation(type="list",
    formula1='"Gasolina,Comidas,Hospedaje,Teléfono,Otros,Reembolso,Aporte_Louis"',
    allow_blank=True)
dv_tipo = DataValidation(type="list", formula1='"Gasto,Ingreso"', allow_blank=True)
dv_responsable = DataValidation(type="list", formula1='"Personal,Empresa"', allow_blank=True)

dv_empleado.add(f"C{DATA_FIRST_ROW}:C{DATA_LAST_ROW}")
dv_categoria.add(f"D{DATA_FIRST_ROW}:D{DATA_LAST_ROW}")
dv_tipo.add(f"E{DATA_FIRST_ROW}:E{DATA_LAST_ROW}")
dv_responsable.add(f"I{DATA_FIRST_ROW}:I{DATA_LAST_ROW}")
for dv in (dv_empleado, dv_categoria, dv_tipo, dv_responsable):
    ws2.add_data_validation(dv)

# Conditional formatting (fila completa): rojo Gasto / verde Ingreso
cf_range = f"A{DATA_FIRST_ROW}:L{DATA_LAST_ROW}"
ws2.conditional_formatting.add(
    cf_range, FormulaRule(formula=[f'$E{DATA_FIRST_ROW}="Gasto"'], fill=RED_FILL))
ws2.conditional_formatting.add(
    cf_range, FormulaRule(formula=[f'$E{DATA_FIRST_ROW}="Ingreso"'], fill=GREEN_FILL))

# Protection — unlock input columns, lock formula columns + headers + note
# B Fecha, C Empleado, D Categoría, E Tipo_Mov, H Total, I Responsable_Pago, K Observaciones, L Archivo_Manual
# Sin password: "Desproteger hoja" funciona con un clic, sin pedir clave (ver nota A1).
UNLOCKED = {2, 3, 4, 5, 8, 9, 11, 12}
for r in range(DATA_FIRST_ROW, DATA_LAST_ROW + 1):
    for c in range(1, LAST_COL + 1):
        cell = ws2.cell(row=r, column=c)
        cell.protection = cell.protection.copy(locked=(c not in UNLOCKED))
ws2.protection.sheet = True
ws2.freeze_panes = "A3"

# ---------- Sheet 2 (order): Resumen_Ejecutivo ----------
ws3 = wb.create_sheet("Resumen_Ejecutivo")
ws3.protection.sheet = True

ws3.merge_cells("A1:C1")
title = ws3["A1"]
title.value = "Resumen Ejecutivo — Control de Viáticos"
title.font = Font(bold=True, size=14)

kpi_headers = ["Indicador", "Valor"]
for c, h in enumerate(kpi_headers, start=1):
    cell = ws3.cell(row=3, column=c, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL

# Todos los SUMIFS de Gasto filtran Responsable_Pago="Empresa": lo Personal
# (multas, etc.) no debe aparecer en el balance que revisa el jefe.
kpis = [
    ("Total Gastos (Egresos)",
     '=SUMIFS(Registro!H:H,Registro!E:E,"Gasto",Registro!I:I,"Empresa")', True),
    ("Total Reembolsos (Ingresos)",
     '=SUMIFS(Registro!H:H,Registro!E:E,"Ingreso",Registro!D:D,"Reembolso")', True),
    ("Total Aportes Louis (Ingresos)",
     '=SUMIFS(Registro!H:H,Registro!E:E,"Ingreso",Registro!D:D,"Aporte_Louis")', True),
    ("Saldo por Reembolsar", "=B5+B6-B4", True),
    ("IVA Repercutido / Acreditable",
     '=SUMIFS(Registro!G:G,Registro!E:E,"Gasto",Registro!I:I,"Empresa")', True),
    ("Conteo de Facturas", "=COUNTA(Registro!H3:H500)", False),
]
for i, (label, formula, is_currency) in enumerate(kpis, start=4):
    ws3.cell(row=i, column=1, value=label)
    vcell = ws3.cell(row=i, column=2, value=formula)
    vcell.number_format = CURRENCY_FMT if is_currency else "0"

# Saldo por Reembolsar (B7): negativo = gastaste de más = te deben (rojo); positivo/cero = verde
ws3.conditional_formatting.add(
    "B7", CellIsRule(operator="lessThan", formula=["0"],
                      font=Font(color="9C0006"), fill=RED_FILL))
ws3.conditional_formatting.add(
    "B7", CellIsRule(operator="greaterThanOrEqual", formula=["0"],
                      font=Font(color="006100"), fill=GREEN_FILL))

ws3.column_dimensions["A"].width = 32
ws3.column_dimensions["B"].width = 16

# Aviso fijo: sin password de protección
ws3.merge_cells("A11:C11")
warn_cell = ws3["A11"]
warn_cell.value = "⚠ Hoja desprotegida sin contraseña — verifica antes de editar fórmulas de columnas bloqueadas."
warn_cell.font = Font(color="9C5700", italic=True, size=9)
warn_cell.fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
warn_cell.alignment = Alignment(horizontal="left", vertical="center")

# Categoria breakdown table (chart source) — solo categorías de Gasto
ws3.cell(row=13, column=1, value="Gastos por Categoría").font = Font(bold=True)
ws3.cell(row=14, column=1, value="Categoría").font = HEADER_FONT
ws3.cell(row=14, column=1).fill = HEADER_FILL
ws3.cell(row=14, column=2, value="Total").font = HEADER_FONT
ws3.cell(row=14, column=2).fill = HEADER_FILL
categorias_gasto = ["Gasolina", "Comidas", "Hospedaje", "Teléfono", "Otros"]
for i, cat in enumerate(categorias_gasto, start=15):
    ws3.cell(row=i, column=1, value=cat)
    ws3.cell(row=i, column=2,
              value=f'=SUMIFS(Registro!H:H,Registro!E:E,"Gasto",Registro!D:D,"{cat}",Registro!I:I,"Empresa")').number_format = CURRENCY_FMT

# Balance Louis vs Gastos (chart source)
ws3.cell(row=22, column=1, value="Balance: Aportes Louis vs Mis Gastos").font = Font(bold=True)
ws3.cell(row=23, column=1, value="Concepto").font = HEADER_FONT
ws3.cell(row=23, column=1).fill = HEADER_FILL
ws3.cell(row=23, column=2, value="Total").font = HEADER_FONT
ws3.cell(row=23, column=2).fill = HEADER_FILL
ws3.cell(row=24, column=1, value="Aportes Louis")
ws3.cell(row=24, column=2, value='=SUMIF(Registro!E:E,"Ingreso",Registro!H:H)').number_format = CURRENCY_FMT
ws3.cell(row=25, column=1, value="Mis Gastos")
ws3.cell(row=25, column=2,
          value='=SUMIFS(Registro!H:H,Registro!E:E,"Gasto",Registro!I:I,"Empresa")').number_format = CURRENCY_FMT

# Bar chart: gastos por categoria
bar = BarChart()
bar.title = "Gastos por Categoría"
bar.y_axis.title = "MXN"
bar.x_axis.title = "Categoría"
data = Reference(ws3, min_col=2, min_row=14, max_row=19)
cats = Reference(ws3, min_col=1, min_row=15, max_row=19)
bar.add_data(data, titles_from_data=True)
bar.set_categories(cats)
bar.height = 8
bar.width = 16
ws3.add_chart(bar, "D3")

# Pie chart: balance Louis (verde) vs gastos (rojo)
pie = PieChart()
pie.title = "Balance: Aportes Louis vs Mis Gastos"
pdata = Reference(ws3, min_col=2, min_row=23, max_row=25)
pcats = Reference(ws3, min_col=1, min_row=24, max_row=25)
pie.add_data(pdata, titles_from_data=True)
pie.set_categories(pcats)
pie.height = 8
pie.width = 16
pie.series[0].data_points = [
    DataPoint(idx=0, spPr=GraphicalProperties(solidFill="00B050")),  # Aportes Louis = verde
    DataPoint(idx=1, spPr=GraphicalProperties(solidFill="FF0000")),  # Mis Gastos = rojo
]
ws3.add_chart(pie, "D19")

wb.active = 0  # abrir en Registro
wb.save(OUT)
print("saved:", OUT)
