"""
BOOK_ATKUP 삭제 + BOOK_002의 icon_key를 ico_atkup으로 변경 후 재익스포트

사용법: py fix_spellbook_atkup.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

SPELL_TYPES = [str, str, str, float, str, int, bool, int, str]
LANG_TYPES = [str, str, str]

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

def delete_row_by_id(ws, item_id, id_col=0):
    """item_id가 일치하는 행 삭제"""
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[id_col].value == item_id:
            ws.delete_rows(row_idx)
            return True
    return False

def export_sheet(wb, sheet_name, types, out_name):
    ws = wb[sheet_name]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, types[i]) for i in range(len(types))])
    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, out_name + ".bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"{out_name}.bytes: {len(rows)} rows, {len(packed)} bytes")

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)

    # 1) BOOK_002의 icon_key를 ico_atkup으로 변경
    ws = wb["TB_SpellBook"]
    for row in ws.iter_rows(min_row=2):
        if row[0].value == "BOOK_002":
            old_icon = row[8].value
            row[8].value = "ico_atkup"
            print(f"BOOK_002 icon_key: '{old_icon}' → 'ico_atkup'")
            break

    # 2) BOOK_ATKUP 삭제
    if delete_row_by_id(ws, "BOOK_ATKUP"):
        print("BOOK_ATKUP 삭제 완료 (TB_SpellBook)")

    # 3) 언어 테이블에서도 BOOK_ATKUP 삭제
    if delete_row_by_id(wb["TB_LangLevelUpSelect_name"], "BOOK_ATKUP"):
        print("BOOK_ATKUP 삭제 완료 (Lang_name)")
    if delete_row_by_id(wb["TB_LangLevelUpSelect_des"], "BOOK_ATKUP"):
        print("BOOK_ATKUP 삭제 완료 (Lang_des)")

    wb.save(XLSX_PATH)
    wb.close()

    # 4) 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    export_sheet(wb, "TB_SpellBook", SPELL_TYPES, "TB_SpellBook")
    export_sheet(wb, "TB_LangLevelUpSelect_name", LANG_TYPES, "TB_LangLevelUpSelect_name")
    export_sheet(wb, "TB_LangLevelUpSelect_des", LANG_TYPES, "TB_LangLevelUpSelect_des")
    wb.close()

    print("\nDone!")

if __name__ == "__main__":
    main()
