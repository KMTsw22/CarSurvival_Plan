"""
TableAsset/TB_Monster.xlsx에서 MON_TRAFFIC, MON_BOSS_SLAVE_0, MON_BOSS_SLAVE_1을
메인 car_survivor_tables.xlsx TB_Monster에 추가 후 재익스포트

사용법: py add_traffic_monster.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
ASSET_PATH = os.path.join(SCRIPT_DIR, "TableAsset", "TB_Monster.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

MON_TYPES = [str, str, bool, float, float, float, float, int, int, str, str, float, float, float]
TARGETS = {"MON_TRAFFIC", "MON_BOSS_SLAVE_0", "MON_BOSS_SLAVE_1"}

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
    # TableAsset에서 대상 행 읽기
    awb = openpyxl.load_workbook(ASSET_PATH, read_only=True, data_only=True)
    aws = awb.active
    new_rows = []
    for row in aws.iter_rows(min_row=2, values_only=True):
        if row[0] is None: break
        if row[0] in TARGETS:
            new_rows.append(list(row))
            print(f"TableAsset에서 읽음: {row[0]} (special={row[9]})")
    awb.close()

    # 메인 테이블에 추가
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Monster"]

    # 이미 있는지 확인
    existing = set()
    for row in ws.iter_rows(min_row=2):
        if row[0].value is None: break
        existing.add(row[0].value)

    # 마지막 행 찾기
    last_row = 1
    for row in ws.iter_rows(min_row=2):
        if row[0].value is None: break
        last_row = row[0].row

    for data in new_rows:
        mon_id = data[0]
        if mon_id in existing:
            print(f"{mon_id}: 이미 존재 → 건너뜀")
            continue
        last_row += 1
        for col_idx, val in enumerate(data, start=1):
            if col_idx <= len(MON_TYPES):
                ws.cell(row=last_row, column=col_idx, value=val)
        print(f"Row {last_row}: {mon_id} 추가")

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
