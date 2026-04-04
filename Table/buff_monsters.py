"""
TB_Monster: base_hp x10
TB_Wave: spawn_count x5, max_enemies x5
후 재익스포트

사용법: py buff_monsters.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

MON_TYPES = [str, str, bool, float, float, float, float, int, int, str, str, float, float, float]
WAVE_TYPES = [str, int, str, int, float, int, float, str]

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

    # ── TB_Monster: base_hp (col 4) x10 ──
    ws = wb["TB_Monster"]
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None: break
        old_hp = row[3].value or 0
        new_hp = old_hp * 10
        ws.cell(row=row_idx, column=4, value=new_hp)
        print(f"TB_Monster {row[0].value}: base_hp {old_hp} → {new_hp}")

    # ── TB_Wave: spawn_count (col 4) x5, max_enemies (col 6) x5 ──
    ws = wb["TB_Wave"]
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None: break
        old_spawn = row[3].value or 0
        old_max = row[5].value or 0
        new_spawn = old_spawn * 5
        new_max = old_max * 5
        ws.cell(row=row_idx, column=4, value=new_spawn)
        ws.cell(row=row_idx, column=6, value=new_max)
        print(f"TB_Wave {row[0].value} w{row[1].value}: spawn {old_spawn}→{new_spawn}, max {old_max}→{new_max}")

    wb.save(XLSX_PATH)
    wb.close()
    print("\n엑셀 저장 완료!")

    # ── 재익스포트 ──
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)

    # TB_Monster
    ws = wb["TB_Monster"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, MON_TYPES[i]) for i in range(len(MON_TYPES))])
    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Monster.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Monster.bytes: {len(rows)} rows, {len(packed)} bytes")

    # TB_Wave
    ws = wb["TB_Wave"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, WAVE_TYPES[i]) for i in range(len(WAVE_TYPES))])
    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Wave.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Wave.bytes: {len(rows)} rows, {len(packed)} bytes")

    wb.close()

if __name__ == "__main__":
    main()
