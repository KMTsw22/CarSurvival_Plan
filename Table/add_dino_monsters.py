"""TB_Monster에 ch_1 공룡 몬스터 추가"""
import sys, io, openpyxl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

wb = openpyxl.load_workbook('TableAsset/TB_Monster.xlsx')
ws = wb['TB_Monster']

# 기존 마지막 행 찾기
last_row = ws.max_row

# 공룡 몬스터 데이터
# (mon_id, mon_name, is_boss, base_hp, base_speed, contact_damage, scale,
#  chapter, spawn_weight, special_ability, sprite_key,
#  bounce_speed, bounce_height, bounce_squash)
#
# 역할 매핑 (기존 몬스터 참고):
#   MON_COMPY   ≈ MON_001 타이어 괴물 (기본 졸개)      HP50  spd1.75 dmg20
#   MON_RAPTOR  ≈ MON_002 오일 슬라임 (빠른형)          HP80  spd2.8  dmg20
#   MON_DILOPHO ≈ MON_006 Cone Head (기본+특수)         HP50  spd1.75 dmg20
#   MON_STEGO   ≈ MON_003 메탈 크러셔 (느린 탱커)       HP200 spd1.05 dmg30
#   MON_TRIKE   ≈ MON_005 Billboard Golem (돌진 탱커)   HP250 spd0.7  dmg20
#   MON_CARNO   ≈ MON_004 스파크 러너 (빠른 공격형)     HP50  spd3.5  dmg30
#   MON_PTERO   ≈ MON_002 오일 슬라임 (빠름+회피)       HP80  spd2.8  dmg20
#   MON_ANKYLO  ≈ MON_008 Wrecker Crawler (중장갑)      HP300 spd1.05 dmg30
#   MON_SPINO   ≈ MON_009 Wrench Goblin (대형 고데미지) HP500 spd0.7  dmg40
#   MON_TREX    ≈ MON_BOSS_001 워로드 트럭 (보스)       HP20000

dinos = [
    # 기본 졸개 - 콤프소그나투스 (소형, 빠름, 약함)
    ('MON_COMPY', 'Compsognathus', False, 50, 2.0, 15, 0.4,
     1, 10, 'None', 'spr_mon_compy', 0.5, 0.15, 0.1),

    # 빠른 돌격 - 랩터 (빠르고 공격적)
    ('MON_RAPTOR', 'Raptor', False, 70, 3.0, 25, 0.55,
     1, 8, 'None', 'spr_mon_raptor', 0.5, 0.1, 0.1),

    # 독 공격형 - 딜로포사우루스 (중간, 특수능력)
    ('MON_DILOPHO', 'Dilophosaurus', False, 60, 2.2, 20, 0.55,
     1, 8, 'None', 'spr_mon_dilopho', 0.5, 0.15, 0.1),

    # 느린 탱커 - 스테고사우루스 (높은HP, 느림)
    ('MON_STEGO', 'Stegosaurus', False, 200, 1.0, 30, 0.75,
     1, 5, 'None', 'spr_mon_stego', 0.5, 0.3, 0.15),

    # 돌진형 - 트리케라톱스 (중장갑, 돌진)
    ('MON_TRIKE', 'Triceratops', False, 250, 1.4, 35, 0.7,
     1, 5, 'None', 'spr_mon_trike', 0.5, 0.25, 0.15),

    # 공격형 중형 - 카르노타우루스 (빠르고 강함)
    ('MON_CARNO', 'Carnotaurus', False, 80, 3.2, 30, 0.6,
     1, 6, 'FlameTrail', 'spr_mon_carno', 0.5, 0.1, 0.05),

    # 비행 기습 - 프테라노돈 (빠름, 회피형, 낮은HP)
    ('MON_PTERO', 'Pteranodon', False, 40, 3.5, 15, 0.5,
     1, 7, 'None', 'spr_mon_ptero', 0.5, 0.1, 0.05),

    # 중장갑 탱커 - 안킬로사우루스 (매우 높은HP, 매우 느림)
    ('MON_ANKYLO', 'Ankylosaurus', False, 350, 0.7, 25, 0.8,
     1, 4, 'None', 'spr_mon_ankylo', 0.5, 0.25, 0.15),

    # 대형 위협 - 스피노사우루스 (높은HP, 고데미지)
    ('MON_SPINO', 'Spinosaurus', False, 500, 0.8, 40, 0.9,
     1, 3, 'None', 'spr_mon_spino', 0.5, 0.2, 0.1),

    # 보스 - 티렉스
    ('MON_TREX', 'T-Rex', True, 20000, 1.0, 50, 0.9,
     1, 1, 'ThreePhase', 'spr_mon_trex', 1.0, 0.01, 0.03),
]

for i, d in enumerate(dinos):
    r = last_row + 1 + i
    for c, val in enumerate(d):
        ws.cell(r, c + 1).value = val

wb.save('TableAsset/TB_Monster.xlsx')
print(f"TB_Monster: {len(dinos)} dino rows added (row {last_row+1}~{last_row+len(dinos)})")
print()
print(f"{'MON_ID':<16} {'이름':<20} {'HP':>6} {'속도':>5} {'데미지':>6} {'크기':>5} {'능력'}")
print("-" * 85)
for d in dinos:
    boss = " [BOSS]" if d[2] else ""
    print(f"{d[0]:<16} {d[1]:<20} {d[3]:>6.0f} {d[4]:>5.1f} {d[5]:>6.0f} {d[6]:>5.2f} {d[9]}{boss}")
