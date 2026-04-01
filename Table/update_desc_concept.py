"""
TB_LangLevelUpSelect_des 설명을 레벨업 컨셉에 맞게 업데이트

머신건: 데미지 증가
오일슬럭: 범위 증가
회전톱날: 개수 추가

사용법: py update_desc_concept.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

def cast(val, t):
    if val is None: return ""
    return str(val) if val else ""

def main():
    # 1) TB_Weapon에서 실제 수치 읽기
    wb_read = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws_wpn = wb_read["TB_Weapon"]

    weapons = {}
    for row in ws_wpn.iter_rows(min_row=2, values_only=True):
        if row[0] is None: break
        weapons[str(row[0])] = {
            "damage": float(row[3]) if row[3] else 0,
            "weapon_type": str(row[6]) if row[6] else "",
            "cooldown": float(row[7]) if row[7] else 0,
            "duration": float(row[8]) if row[8] else 0,
            "etc1": float(row[12]) if row[12] else 0,  # 오일:감속%, 톱날:회전속도
            "etc2": float(row[13]) if row[13] else 0,  # 오일:감속시간, 톱날:궤도반경
            "etc3": float(row[14]) if row[14] else 0,  # 오일:기본반경, 톱날:타격간격
        }

    # 스펠북 읽기
    ws_spell = wb_read["TB_SpellBook"]
    spellbooks = {}
    for row in ws_spell.iter_rows(min_row=2, values_only=True):
        if row[0] is None: break
        spellbooks[str(row[0])] = {
            "effect_type": str(row[2]) if row[2] else "",
            "base_value": float(row[3]) if row[3] else 0,
        }
    wb_read.close()

    # 2) 설명 생성
    desc_map = {}
    for wid, w in weapons.items():
        if w["weapon_type"] == "MachineGun":
            ko = f"DMG +{w['damage']:.0f}/Lv\nCD {w['cooldown']:.1f}s"
            en = f"DMG +{w['damage']:.0f}/Lv\nCD {w['cooldown']:.1f}s"
        elif w["weapon_type"] == "OilSlick":
            ko = f"범위 +0.2/Lv\n감속 {w['etc1']:.0f}%\nDUR {w['duration']:.0f}s"
            en = f"Range +0.2/Lv\nSlow {w['etc1']:.0f}%\nDUR {w['duration']:.0f}s"
        elif w["weapon_type"] == "SawBlade":
            ko = f"톱날 +1/Lv\nDMG {w['damage']:.0f}"
            en = f"Blade +1/Lv\nDMG {w['damage']:.0f}"
        else:
            continue
        desc_map[wid] = (ko, en)

    for bid, b in spellbooks.items():
        v = b["base_value"]
        if b["effect_type"] == "DamageUp":
            desc_map[bid] = (f"ATK +{v:.0f}%/Lv", f"ATK +{v:.0f}%/Lv")
        elif b["effect_type"] == "SpeedUp":
            desc_map[bid] = (f"SPD +{v:.0f}%/Lv", f"SPD +{v:.0f}%/Lv")
        elif b["effect_type"] == "HpUp":
            desc_map[bid] = (f"HP +{v:.0f}%/Lv", f"HP +{v:.0f}%/Lv")

    print("설명:")
    for k, v in desc_map.items():
        print(f"  {k}: {v[0].replace(chr(10), ' | ')}")

    # 3) 엑셀 업데이트
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

    wb.save(XLSX_PATH)
    wb.close()
    print(f"\n{updated}개 업데이트")

    # 4) 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_LangLevelUpSelect_des"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i], str) for i in range(3)])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, "TB_LangLevelUpSelect_des.bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"TB_LangLevelUpSelect_des.bytes: {len(rows)} rows")

if __name__ == "__main__":
    main()
