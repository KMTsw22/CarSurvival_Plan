"""
MON_007, MON_033 (stoplight) special_ability를 TrafficLight로 수정 후 재익스포트

사용법: py fix_trafficlight.py
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

TARGETS = {"MON_007", "MON_033"}

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Monster"]

    # special_ability = col 10 (1-based)
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None: break
        if row[0].value in TARGETS:
            old = row[9].value
            ws.cell(row=row_idx, column=10, value="TrafficLight")
            print(f"{row[0].value}: special '{old}' → 'TrafficLight'")

    wb.save(XLSX_PATH)
    wb.close()
    print("\n엑셀 저장 완료!")

    # 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_Monster"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, MON_TYPES[i]) for i in range(len(MON_TYPES))])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Monster.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Monster.bytes: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
