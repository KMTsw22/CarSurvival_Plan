"""
TB_Monster: scale -0.05 (최소 0.05)
후 재익스포트

사용법: py reduce_monster_scale.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

MON_TYPES = [str, str, bool, float, float, float, float, int, int, str, str, float, float, float]

def cast(val, t):
    if val is None:
        return "" if t == str else 0 if t == int else 0.0 if t == float else False
    if t == bool:
        if isinstance(val, bool): return val
        if isinstance(val, str): return val.lower() in ("true", "1", "yes")
        return bool(val)
    if t == int: return int(float(val)) if val else 0
    if t == float: return float(val) if val else 0.0
    if t == str: return str(val) if val else ""
    return val

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)

    # ── TB_Monster: scale (col 7, index 6) -0.05, 최소 0.05 ──
    ws = wb["TB_Monster"]
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None:
            break
        old_scale = row[6].value or 0.0
        new_scale = round(max(old_scale - 0.05, 0.05), 4)
        ws.cell(row=row_idx, column=7, value=new_scale)
        print(f"TB_Monster {row[0].value}: scale {old_scale} → {new_scale}")

    wb.save(XLSX_PATH)
    wb.close()
    print("\n엑셀 저장 완료!")

    # ── 재익스포트 ──
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)

    ws = wb["TB_Monster"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["):
            break
        rows.append([cast(row[i] if i < len(row) else None, MON_TYPES[i]) for i in range(len(MON_TYPES))])
    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Monster.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Monster.bytes: {len(rows)} rows, {len(packed)} bytes")

    wb.close()

if __name__ == "__main__":
    main()
