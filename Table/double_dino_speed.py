"""TB_Monster 공룡 몬스터 속도 2배"""
import sys, io, openpyxl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

wb = openpyxl.load_workbook('TableAsset/TB_Monster.xlsx')
ws = wb['TB_Monster']

dino_ids = {
    'MON_COMPY', 'MON_RAPTOR', 'MON_DILOPHO', 'MON_STEGO', 'MON_TRIKE',
    'MON_CARNO', 'MON_PTERO', 'MON_ANKYLO', 'MON_SPINO', 'MON_TREX',
}

# col: mon_id=1, base_speed=5
for row in ws.iter_rows(min_row=2):
    mon_id = row[0].value
    if mon_id in dino_ids:
        old_spd = row[4].value
        row[4].value = old_spd * 2
        print(f"  {mon_id:<16} {old_spd} -> {row[4].value}")

wb.save('TableAsset/TB_Monster.xlsx')
print("done")
