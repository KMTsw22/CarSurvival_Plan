"""
화염방사기 기본값 엑셀 반영 + TB_Car/TB_Weapon 재익스포트

사용법: py update_flame_defaults.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

CAR_TYPES = [str, str, str, float, float, float, float, float, str, float, str, int, str, bool, str, float]
WPN_TYPES = [str, str, str, float, str, str, str, float, float, int, int, str, float, float, float, float, float, float]

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

    # ── TB_Car: flame_offset = 4 ──
    ws_car = wb["TB_Car"]
    for row_idx, row in enumerate(ws_car.iter_rows(min_row=2), start=2):
        if row[0].value is None: break
        ws_car.cell(row=row_idx, column=16, value=4.0)
        print(f"TB_Car {row[0].value}: flame_offset = 4.0")

    # ── TB_Weapon: Flamethrower etc 값 설정 ──
    ws_wpn = wb["TB_Weapon"]
    for row in ws_wpn.iter_rows(min_row=2):
        if row[0].value is None: break
        if row[6].value == "Flamethrower":
            row[12].value = 3.0   # etc_value1: 화상 데미지
            row[13].value = 2.0   # etc_value2: 기본 반경
            # etc_value3(레벨당 반경 증가)는 기존값 유지
            row[15].value = 3.0   # etc_value4: 화상 지속시간
            print(f"{row[0].value}: etc1=3(화상DMG), etc2=2(반경), etc4=3(지속시간)")

    wb.save(XLSX_PATH)
    wb.close()
    print("\n엑셀 저장 완료!")

    # ── 재익스포트 ──
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)

    # TB_Car
    ws = wb["TB_Car"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, CAR_TYPES[i]) for i in range(len(CAR_TYPES))])
    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Car.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Car.bytes: {len(rows)} rows, {len(packed)} bytes")

    # TB_Weapon
    ws = wb["TB_Weapon"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, WPN_TYPES[i]) for i in range(len(WPN_TYPES))])
    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Weapon.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Weapon.bytes: {len(rows)} rows, {len(packed)} bytes")

    wb.close()

if __name__ == "__main__":
    main()
