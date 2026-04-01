"""
TB_Monster, TB_MonsterDrop의 빈 행 제거 후 재익스포트

사용법: py fix_monster_rows.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

MON_TYPES = [str, str, bool, float, float, float, float, int, int, str, str, float, float, float]
DROP_TYPES = [str, str, int, int, int]

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

def compact_sheet(ws, id_col=0):
    """빈 행을 제거하고 데이터를 연속으로 만듦"""
    data_rows = []
    headers = []
    for col_idx, cell in enumerate(ws[1]):
        headers.append(cell.value)

    for row in ws.iter_rows(min_row=2, values_only=True):
        val = row[id_col]
        if val is None: continue
        s = str(val).strip()
        if s == "" or s.startswith("[") or s.startswith("─"): continue
        # ID 형식 체크 (MON_, DROP_, WPN_ 등으로 시작)
        if not any(s.startswith(p) for p in ("MON_", "DROP_", "WPN_", "BOOK_", "STG_", "MAP_")): continue
        data_rows.append(list(row))

    # 기존 데이터 삭제 (헤더 제외)
    ws.delete_rows(2, ws.max_row)

    # 다시 쓰기
    for r_idx, row_data in enumerate(data_rows, start=2):
        for c_idx, val in enumerate(row_data, start=1):
            ws.cell(row=r_idx, column=c_idx, value=val)

    return len(data_rows)

def export_sheet(xlsx_path, sheet_name, types, out_name):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb[sheet_name]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None: continue
        s = str(row[0]).strip()
        if s == "" or s.startswith("[") or s.startswith("─"): continue
        if not any(s.startswith(p) for p in ("MON_", "DROP_", "WPN_", "BOOK_", "STG_", "MAP_")): continue
        rows.append([cast(row[j] if j < len(row) else None, types[j]) for j in range(len(types))])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, out_name + ".bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"{out_name}.bytes: {len(rows)} rows, {len(packed)} bytes")

def main():
    # 1) 엑셀 빈 행 정리
    wb = openpyxl.load_workbook(XLSX_PATH)

    count = compact_sheet(wb["TB_Monster"])
    print(f"TB_Monster: {count}행 (빈 행 제거)")

    count = compact_sheet(wb["TB_MonsterDrop"])
    print(f"TB_MonsterDrop: {count}행 (빈 행 제거)")

    wb.save(XLSX_PATH)
    wb.close()

    # 2) 재익스포트
    export_sheet(XLSX_PATH, "TB_Monster", MON_TYPES, "TB_Monster")
    export_sheet(XLSX_PATH, "TB_MonsterDrop", DROP_TYPES, "TB_MonsterDrop")

    print("\nDone!")

if __name__ == "__main__":
    main()
