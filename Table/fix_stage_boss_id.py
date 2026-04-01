"""
TB_Stage의 boss_mon_id를 실제 보스 ID(MON_BOSS_001)로 수정

사용법: py fix_stage_boss_id.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

TYPES = [str, str, int, str, str, int, str, str]

def cast(val, t):
    if val is None:
        return "" if t == str else 0 if t == int else 0.0 if t == float else False
    if t == int: return int(float(val)) if val else 0
    if t == str: return str(val) if val else ""
    return val

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Stage"]

    # boss_mon_id 열(index 3, 1-based col 4)을 MON_BOSS_001로 수정
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None:
            break
        old = row[3].value
        row[3].value = "MON_BOSS_001"
        print(f"행 {row_idx}: boss_mon_id '{old}' → 'MON_BOSS_001'")

    wb.save(XLSX_PATH)
    wb.close()

    # 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_Stage"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, TYPES[i]) for i in range(len(TYPES))])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, "TB_Stage.bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"TB_Stage.bytes 재생성: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
