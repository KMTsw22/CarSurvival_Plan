"""
TB_LangLevelUpSelect_des 설명을 능력치 위주로 업데이트 후 재익스포트

사용법: py update_desc_stats.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

LANG_TYPES = [str, str, str]

# item_id → (한국어 설명, 영어 설명)
DESC_UPDATES = {
    "WPN_001": ("DMG 15\nCD 0.3s", "DMG 15\nCD 0.3s"),
    "WPN_002": ("DMG 8/s\nDUR 5s\n감속 50%", "DMG 8/s\nDUR 5s\nSlow 50%"),
    "WPN_003": ("DMG 7\n회전 180°/s", "DMG 7\nSpin 180°/s"),
}

def cast(val, t):
    if val is None:
        return "" if t == str else 0
    return str(val) if val else ""

def main():
    # 1) 먼저 TB_Weapon에서 실제 수치 읽기
    wb_read = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws_wpn = wb_read["TB_Weapon"]

    weapons = {}
    for row in ws_wpn.iter_rows(min_row=2, values_only=True):
        if row[0] is None: break
        weapon_id = str(row[0])
        weapons[weapon_id] = {
            "damage": float(row[3]) if row[3] else 0,
            "weapon_type": str(row[6]) if row[6] else "",
            "cooldown": float(row[7]) if row[7] else 0,
            "duration": float(row[8]) if row[8] else 0,
            "etc1": float(row[12]) if row[12] else 0,
            "etc2": float(row[13]) if row[13] else 0,
            "etc3": float(row[14]) if row[14] else 0,
        }
    wb_read.close()

    # 실제 수치로 설명 생성
    desc_map = {}
    for wid, w in weapons.items():
        ko_lines = []
        en_lines = []

        if w["weapon_type"] == "MachineGun":
            ko_lines.append(f"DMG {w['damage']:.0f}")
            ko_lines.append(f"CD {w['cooldown']:.1f}s")
            en_lines = ko_lines.copy()
        elif w["weapon_type"] == "OilSlick":
            ko_lines.append(f"DMG {w['damage']:.0f}/s")
            if w["duration"] > 0: ko_lines.append(f"DUR {w['duration']:.0f}s")
            if w["etc1"] > 0: ko_lines.append(f"감속 {w['etc1']:.0f}%")
            en_lines.append(f"DMG {w['damage']:.0f}/s")
            if w["duration"] > 0: en_lines.append(f"DUR {w['duration']:.0f}s")
            if w["etc1"] > 0: en_lines.append(f"Slow {w['etc1']:.0f}%")
        elif w["weapon_type"] == "SawBlade":
            ko_lines.append(f"DMG {w['damage']:.0f}")
            if w["etc1"] > 0: ko_lines.append(f"회전 {w['etc1']:.0f}°/s")
            en_lines.append(f"DMG {w['damage']:.0f}")
            if w["etc1"] > 0: en_lines.append(f"Spin {w['etc1']:.0f}°/s")

        if ko_lines:
            desc_map[wid] = ("\n".join(ko_lines), "\n".join(en_lines))

    # 스펠북도
    ws_spell = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)["TB_SpellBook"]
    for row in ws_spell.iter_rows(min_row=2, values_only=True):
        if row[0] is None: break
        book_id = str(row[0])
        effect_type = str(row[2]) if row[2] else ""
        base_value = float(row[3]) if row[3] else 0

        if effect_type == "DamageUp":
            desc_map[book_id] = (f"ATK +{base_value:.0f}%", f"ATK +{base_value:.0f}%")
        elif effect_type == "SpeedUp":
            desc_map[book_id] = (f"SPD +{base_value:.0f}%", f"SPD +{base_value:.0f}%")
        elif effect_type == "HpUp":
            desc_map[book_id] = (f"HP +{base_value:.0f}%", f"HP +{base_value:.0f}%")

    print("생성된 설명:")
    for k, v in desc_map.items():
        print(f"  {k}: {v[0].replace(chr(10), ' | ')}")

    # 2) 엑셀 업데이트
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws_des = wb["TB_LangLevelUpSelect_des"]

    updated = 0
    for row in ws_des.iter_rows(min_row=2):
        item_id = row[0].value
        if item_id and item_id in desc_map:
            ko, en = desc_map[item_id]
            row[1].value = ko
            row[2].value = en
            updated += 1
            print(f"  업데이트: {item_id}")

    wb.save(XLSX_PATH)
    wb.close()
    print(f"\n{updated}개 설명 업데이트 완료")

    # 3) 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_LangLevelUpSelect_des"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, str) for i in range(3)])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, "TB_LangLevelUpSelect_des.bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"TB_LangLevelUpSelect_des.bytes: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
