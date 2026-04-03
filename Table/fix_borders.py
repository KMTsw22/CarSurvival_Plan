"""
TB_Weapon 데이터 행에 얇은(thin) 테두리 적용

사용법: py fix_borders.py
주의: 엑셀 파일을 먼저 닫고 실행하세요!
"""
import os, sys, io, openpyxl
from openpyxl.styles import Border, Side

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Weapon"]

    hair = Side(style='hair')
    hair_border = Border(left=hair, right=hair, top=hair, bottom=hair)

    # 헤더 포함 전체 데이터 영역에 hair 테두리 적용
    for row in ws.iter_rows(min_row=1):
        cell_id = row[0].value
        if row[0].row > 1 and (cell_id is None or str(cell_id).startswith("[")):
            break
        for cell in row:
            if cell.value is not None or cell.column <= 18:
                cell.border = hair_border

    print("hair 테두리 적용 완료")
    wb.save(XLSX_PATH)
    wb.close()
    print(f"저장: {XLSX_PATH}")

if __name__ == "__main__":
    main()
