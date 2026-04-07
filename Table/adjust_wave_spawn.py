"""
TB_Wave: spawn_count 절반, spawn_interval 절반 후 재익스포트

사용법: py adjust_wave_spawn.py
"""
import os, sys, io, math, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

WAVE_TYPES = [str, int, str, int, float, int, float, str]

def cast(val, t):
    if val is None:
        return "" if t == str else 0 if t == int else 0.0 if t == float else False
    if t == int: return int(float(val)) if val else 0
    if t == float: return float(val) if val else 0.0
    if t == str: return str(val) if val else ""
    return val

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Wave"]

    # col 4 = spawn_count, col 5 = spawn_interval
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None: break

        old_spawn = row[3].value or 0
        old_interval = row[4].value or 0

        new_spawn = max(1, math.ceil(old_spawn / 2))
        new_interval = round(old_interval / 2, 2)

        ws.cell(row=row_idx, column=4, value=new_spawn)
        ws.cell(row=row_idx, column=5, value=new_interval)
        print(f"{row[0].value} w{row[1].value}: spawn {old_spawn}→{new_spawn}, interval {old_interval}→{new_interval}")

    wb.save(XLSX_PATH)
    wb.close()
    print("\n엑셀 저장 완료!")

    # 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_Wave"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, WAVE_TYPES[i]) for i in range(len(WAVE_TYPES))])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Wave.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Wave.bytes: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
