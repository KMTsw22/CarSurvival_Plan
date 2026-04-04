"""
TB_SpellBook icon_key를 실제 스프라이트 파일명으로 수정 후 재익스포트

사용법: py fix_spellbook_icons.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

SPELL_TYPES = [str, str, str, float, str, int, bool, int, str]

ICON_FIX = {
    "HP Regen-removebg": "ico_hpregen",
    "EXP Boost-removebg": "ico_expboost",
    "Damage Shield-removebg": "ico_damageshield",
    "Magnet-removebg": "ico_magnet",
}

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
    ws = wb["TB_SpellBook"]

    icon_col = 9  # icon_key 컬럼 (1-based)
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None: break
        old_key = row[icon_col - 1].value
        if old_key in ICON_FIX:
            new_key = ICON_FIX[old_key]
            ws.cell(row=row_idx, column=icon_col, value=new_key)
            print(f"{row[0].value}: {old_key} → {new_key}")
        else:
            print(f"{row[0].value}: {old_key} (OK)")

    wb.save(XLSX_PATH)
    wb.close()
    print("\n엑셀 저장 완료!")

    # 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_SpellBook"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, SPELL_TYPES[i]) for i in range(len(SPELL_TYPES))])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, "TB_SpellBook.bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"TB_SpellBook.bytes: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
