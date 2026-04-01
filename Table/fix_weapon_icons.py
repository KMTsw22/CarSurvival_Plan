"""
TB_Weapon icon_key 일괄 업데이트 후 재익스포트

사용법: py fix_weapon_icons.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

ICON_MAP = {
    "ico_machinegun": "weapon_machinegun",
    "ico_oilslick": "weapon_oilslick",
    "ico_spinblade": "weapon_spinblade",
    "ico_sawblade": "weapon_spinblade",
}

TYPES = [str, str, str, float, str, str, str, float, float, int, int, str, float, float, float, float, float]

def cast(val, t):
    if val is None:
        return "" if t == str else 0 if t == int else 0.0 if t == float else False
    if t == int: return int(float(val)) if val else 0
    if t == float: return float(val) if val else 0.0
    if t == str: return str(val) if val else ""
    return val

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Weapon"]

    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        icon_cell = row[11]  # icon_key (col index 11)
        old_val = icon_cell.value
        if old_val and old_val in ICON_MAP:
            icon_cell.value = ICON_MAP[old_val]
            print(f"행 {row_idx}: '{old_val}' → '{ICON_MAP[old_val]}'")

    wb.save(XLSX_PATH)
    wb.close()
    print("엑셀 저장 완료")

    # 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_Weapon"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, TYPES[i]) for i in range(len(TYPES))])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, "TB_Weapon.bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"TB_Weapon.bytes 재생성: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
