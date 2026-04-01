"""
새 몬스터 이미지를 Sprites/Monsters에 복사 + TB_Monster/TB_MonsterDrop 테이블에 추가

사용법: py add_new_monsters.py
"""
import os, sys, io, shutil, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")
SRC_DIR = os.path.join(SCRIPT_DIR, "..", "ImgData", "mvp", "monster", "remove_bg_new")
DST_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Sprites", "Monsters")

# 이미지 → (sprite_key, mon_name_ko, mon_name_en)
MONSTER_MAP = [
    ("Air Filter Slime-removebg.png",       "spr_mon_airfilter",    "에어필터 슬라임",      "Air Filter Slime"),
    ("Battery Bolt-removebg.png",           "spr_mon_battery",      "배터리 볼트",          "Battery Bolt"),
    ("Billboard Golem-remove.png",          "spr_mon_billboard",    "빌보드 골렘",          "Billboard Golem"),
    ("Bolt Swarm-removebg.png",             "spr_mon_boltswarm",    "볼트 스웜",            "Bolt Swarm"),
    ("Brake Pad-removebg.png",              "spr_mon_brakepad",     "브레이크 패드",        "Brake Pad"),
    ("Caliper Crab-removebg.png",           "spr_mon_caliper",      "캘리퍼 크랩",          "Caliper Crab"),
    ("Checker Ghost-removebg.png",          "spr_mon_checker",      "체커 고스트",          "Checker Ghost"),
    ("Cone Head-remove.png",                "spr_mon_conehead",     "콘 헤드",              "Cone Head"),
    ("DRS Drone-removebg.png",              "spr_mon_drs",          "DRS 드론",             "DRS Drone"),
    ("Drill Mole-removebg.png",             "spr_mon_drill",        "드릴 몰",              "Drill Mole"),
    ("Grandstand Rusher-removebg.png",      "spr_mon_grandstand",   "관람석 러셔",          "Grandstand Rusher"),
    ("Helmet Header-removebg.png",          "spr_mon_helmet",       "헬멧 헤더",            "Helmet Header"),
    ("Jack Stand Walker-removebg.png",      "spr_mon_jackstand",    "잭 스탠드 워커",       "Jack Stand Walker"),
    ("Oil_Drum_Roller-removebg.png",        "spr_mon_oildrum",      "오일드럼 롤러",        "Oil Drum Roller"),
    ("Pit Crew Zombie-removebg.png",        "spr_mon_pitcrew",      "피트크루 좀비",        "Pit Crew Zombie"),
    ("Safety Car Goblin-removebg.png",      "spr_mon_safetycar",    "세이프티카 고블린",    "Safety Car Goblin"),
    ("Spark Plug-removebg.png",             "spr_mon_sparkplug",    "스파크 플러그",        "Spark Plug"),
    ("Stoplight Striker-remove.png",        "spr_mon_stoplight",    "신호등 스트라이커",    "Stoplight Striker"),
    ("Tire Stacker-removebg.png",           "spr_mon_tirestacker",  "타이어 스태커",        "Tire Stacker"),
    ("Turbo Fan-romvebg.png",               "spr_mon_turbofan",     "터보 팬",              "Turbo Fan"),
    ("Wrecker Crawler-remove.png",          "spr_mon_wrecker",      "레커 크롤러",          "Wrecker Crawler"),
    ("Wrench Goblin-removebg.png",          "spr_mon_wrench",       "렌치 고블린",          "Wrench Goblin"),
]

# 몬스터 테이블 타입
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

def main():
    # 1) 이미지 복사
    os.makedirs(DST_DIR, exist_ok=True)
    copied = 0
    for src_name, sprite_key, _, _ in MONSTER_MAP:
        src = os.path.join(SRC_DIR, src_name)
        dst = os.path.join(DST_DIR, sprite_key + ".png")
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied += 1
        else:
            print(f"  WARNING: {src_name} not found!")
    print(f"{copied}개 이미지 복사 완료 → {DST_DIR}")

    # 2) 엑셀에 몬스터 추가
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws_mon = wb["TB_Monster"]
    ws_drop = wb["TB_MonsterDrop"]

    # 기존 mon_id 수집
    existing_ids = set()
    for row in ws_mon.iter_rows(min_row=2, values_only=True):
        if row[0] is None: break
        existing_ids.add(str(row[0]))

    start_idx = len(existing_ids) + 1  # 기존 개수 다음부터
    added = 0

    for i, (src_name, sprite_key, name_ko, name_en) in enumerate(MONSTER_MAP):
        mon_id = f"MON_{start_idx + i:03d}"

        if mon_id in existing_ids:
            continue

        # TB_Monster 행 추가
        # mon_id, mon_name, is_boss, base_hp, base_speed, contact_damage, scale, chapter, spawn_weight, special_ability, sprite_key, bounce_speed, bounce_height, bounce_squash
        row_num = ws_mon.max_row + 1
        data = [
            mon_id,         # mon_id
            name_en,        # mon_name (영어)
            False,          # is_boss
            30.0,           # base_hp (임시)
            1.5,            # base_speed (임시)
            5.0,            # contact_damage (임시)
            0.7,            # scale (임시)
            1,              # chapter
            10,             # spawn_weight (임시)
            "",             # special_ability
            sprite_key,     # sprite_key
            12.0,           # bounce_speed (임시)
            0.25,           # bounce_height (임시)
            0.15,           # bounce_squash (임시)
        ]
        for col_idx, val in enumerate(data, 1):
            ws_mon.cell(row=row_num, column=col_idx, value=val)

        # TB_MonsterDrop 행 추가
        # drop_id, mon_id, exp_amount, gold_amount, screw_amount
        drop_row = ws_drop.max_row + 1
        drop_data = [f"DROP_{start_idx + i:03d}", mon_id, 3, 5, 0]
        for col_idx, val in enumerate(drop_data, 1):
            ws_drop.cell(row=drop_row, column=col_idx, value=val)

        print(f"  추가: {mon_id} - {name_ko} ({name_en}) → {sprite_key}")
        added += 1

    wb.save(XLSX_PATH)
    wb.close()
    print(f"\n{added}개 몬스터 추가")

    # 3) 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)

    # TB_Monster
    ws = wb["TB_Monster"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[j] if j < len(row) else None, MON_TYPES[j]) for j in range(len(MON_TYPES))])

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_Monster.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_Monster.bytes: {len(rows)} rows")

    # TB_MonsterDrop
    ws = wb["TB_MonsterDrop"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[j] if j < len(row) else None, DROP_TYPES[j]) for j in range(len(DROP_TYPES))])

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    with open(os.path.join(OUTPUT_DIR, "TB_MonsterDrop.bytes"), "wb") as f:
        f.write(packed)
    print(f"TB_MonsterDrop.bytes: {len(rows)} rows")

    wb.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
