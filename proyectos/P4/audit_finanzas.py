#!/usr/bin/env python3
"""
Reconciliation audit for PlantillaFinanzas2026.xlsx.
Read-only analysis — never writes to the live file.
Usage: python3 audit_finanzas.py
"""

from openpyxl import load_workbook
from pathlib import Path
from markitdown import MarkItDown

EXCEL_PATH = Path.home() / "Codes/mi-criterio/proyectos/P4/PlantillaFinanzas2026.xlsx"


def structure_overview():
    """Quick markitdown pass — sheet/column overview, not used for numeric calc."""
    md = MarkItDown()
    result = md.convert(str(EXCEL_PATH))
    return result.text_content[:2000]

CUENTAS = ["BBVA", "Uala", "Nu", "Edenred", "Didi cuenta", "efectivo", "Bitso", "GBM"]


def load_data():
    wb = load_workbook(EXCEL_PATH, data_only=True)
    ws_trans = wb["Transacciones"]
    ws_cat = wb["Catalogos"]

    rows = []
    for row_idx in range(2, ws_trans.max_row + 1):
        monto = ws_trans[f"A{row_idx}"].value
        tarjeta = ws_trans[f"D{row_idx}"].value
        if monto is None or tarjeta is None:
            continue
        rows.append({
            'row': row_idx,
            'monto': monto,
            'tipo': ws_trans[f"B{row_idx}"].value,
            'categoria': ws_trans[f"C{row_idx}"].value,
            'tarjeta': tarjeta,
            'fecha': ws_trans[f"E{row_idx}"].value,
            'desc': ws_trans[f"F{row_idx}"].value,
        })

    return wb, ws_cat, rows


def reconcile(cuenta, real, si_val, rows):
    # Ingreso/Egreso: exact tarjeta match (avoids Nu matching Nu Turbo/Nu Cajita)
    exact_rows = [r for r in rows if str(r['tarjeta']).strip() == cuenta]
    ing = sum(r['monto'] for r in exact_rows if r['tipo'] == 'Ingreso')
    egr = sum(r['monto'] for r in exact_rows if r['tipo'] == 'Egreso')

    # Transferencia: match "cuenta->X" / "X->cuenta" over full rows (not exact-filtered)
    trans_rows = [r for r in rows if r['tipo'] == 'Transferencia' and '->' in str(r['tarjeta'])]
    trans_in = sum(r['monto'] for r in trans_rows if str(r['tarjeta']).split('->')[-1].strip() == cuenta)
    trans_out = sum(r['monto'] for r in trans_rows if str(r['tarjeta']).split('->')[0].strip() == cuenta)

    acct_rows = exact_rows + [r for r in trans_rows
                               if str(r['tarjeta']).split('->')[-1].strip() == cuenta
                               or str(r['tarjeta']).split('->')[0].strip() == cuenta]

    calc = si_val + ing - egr + trans_in - trans_out
    residual = real - calc

    return {
        'cuenta': cuenta, 'si': si_val, 'ing': ing, 'egr': egr,
        'trans_in': trans_in, 'trans_out': trans_out,
        'calc': calc, 'real': real, 'residual': residual,
        'n_rows': len(acct_rows), 'rows': acct_rows,
    }


def print_summary(result):
    r = result
    print(f"{r['cuenta']}:")
    print(f"  Calc: {r['si']} + {r['ing']} - {r['egr']} + {r['trans_in']} - {r['trans_out']} = {r['calc']}")
    print(f"  Real: {r['real']}")
    print(f"  Residual: {r['residual']}")
    print(f"  Rows: {r['n_rows']}\n")


def audit_inversiones(wb, rows):
    """Dump Inversiones sheet + locate all investment-instrument transactions."""
    print("\n" + "=" * 60)
    print("=== HOJA INVERSIONES (estado actual) ===")
    ws_inv = wb["Inversiones"]
    for row_idx in range(1, ws_inv.max_row + 1):
        vals = [ws_inv.cell(row=row_idx, column=c).value for c in range(1, 9)]
        if any(v is not None for v in vals):
            print(f"  r{row_idx}: {vals}")

    print("\n=== TRANSACCIONES POR INSTRUMENTO ===")
    instrumentos = ["Bitso", "GBM", "Nu Turbo", "Nu Cajita", "Didi cuenta", "Edenred"]
    for inst in instrumentos:
        hits = [r for r in rows if inst.lower() in str(r['tarjeta']).lower()]
        print(f"\n{inst} ({len(hits)} registros):")
        for r in sorted(hits, key=lambda x: (x['fecha'] or '')):
            f = r['fecha'].strftime('%Y-%m-%d') if hasattr(r['fecha'], 'strftime') else r['fecha']
            print(f"  r{r['row']:>3} | {f} | {r['tipo']:<14} | {r['monto']:>10} | {r['tarjeta']:<22} | {r['desc']}")


def main():
    wb, ws_cat, rows = load_data()

    cat_row_map = {'BBVA': 30, 'Uala': 31, 'Nu': 32, 'Edenred': 33,
                   'Didi cuenta': 34, 'efectivo': 35, 'Bitso': 36, 'GBM': 37}

    print("=== REAL BALANCES (Catalogos F30:F37) ===")
    for cuenta, cat_row in cat_row_map.items():
        real = ws_cat[f"F{cat_row}"].value
        print(f"{cuenta}: {real}")
    print(f"\nTotal transaction rows: {len(rows)}\n")

    for cuenta, cat_row in cat_row_map.items():
        real = ws_cat[f"F{cat_row}"].value
        si_val = ws_cat[f"D{cat_row}"].value or 0
        if real is None:
            continue
        result = reconcile(cuenta, real, si_val, rows)
        print_summary(result)

    audit_inversiones(wb, rows)
    wb.close()


if __name__ == "__main__":
    main()
