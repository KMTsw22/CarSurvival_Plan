"""TB_Monster 공룡 몬스터의 sprite_key를 실제 ch_1 파일명으로 업데이트"""
import sys, io, openpyxl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

wb = openpyxl.load_workbook('TableAsset/TB_Monster.xlsx')
ws = wb['TB_Monster']

# sprite_key 매핑: MON_ID -> ch_1/실제파일명 (확장자 제외)
sprite_map = {
    'MON_COMPY':   'ch_1/Compsognathus',
    'MON_RAPTOR':  'ch_1/Raptor',
    'MON_DILOPHO': 'ch_1/Dilophosaurus',
    'MON_STEGO':   'ch_1/Stegosaurus',
    'MON_TRIKE':   'ch_1/Triceratops',
    'MON_CARNO':   'ch_1/Carnotaurus',
    'MON_PTERO':   'ch_1/Pteranodon',
    'MON_ANKYLO':  'ch_1/Ankylosaurus',
    'MON_SPINO':   'ch_1/Spinosaurus',
    'MON_TREX':    'ch_1/T-Rex',
}

# 컬럼 인덱스: mon_id=1, sprite_key=11
updated = 0
for row in ws.iter_rows(min_row=2):
    mon_id = row[0].value
    if mon_id in sprite_map:
        old_key = row[10].value
        row[10].value = sprite_map[mon_id]
        print(f"  {mon_id:<16} {old_key:<20} -> {sprite_map[mon_id]}")
        updated += 1

wb.save('TableAsset/TB_Monster.xlsx')
print(f"\n{updated} sprite_keys updated")
