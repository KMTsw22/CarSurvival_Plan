"""
TB_Weapon의 etc_value4에 레벨당 증가량 설정 후 재익스포트

MachineGun: etc4 = 레벨당 추가 데미지 (기존 data.damage 사용하던 것)
OilSlick: etc4 = 레벨당 범위 증가
SawBlade: etc4 = 0 (개수=레벨, 코드로 처리)

사용법: py add_etc4_perlevel.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

TYPES = [str, str, str, float, str, str, str, float, float, int, int, str, float, float, float, float, float]

PER_LEVEL = {
    "MachineGun": 20.0,   # 레벨당 DMG +20
    "OilSlick": 0.2,      # 레벨당 범위 +0.2
    "SawBlade": 0.0,      # 개수=레벨 (코드 내부)
}

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

    for row in ws.iter_rows(min_row=2):
        if row[0].value is None: break
        weapon_type = row[6].value  # weapon_type col
        if weapon_type in PER_LEVEL:
            row[15].value = PER_LEVEL[weapon_type]  # etc_value4 (0-indexed col 15)
            print(f"{row[0].value} ({weapon_type}): etc_value4 = {PER_LEVEL[weapon_type]}")

    wb.save(XLSX_PATH)
    wb.close()

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
    print(f"\nTB_Weapon.bytes: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
