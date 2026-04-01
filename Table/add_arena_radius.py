"""
TB_Stage에 arena_radius 컬럼 추가 후 재익스포트

사용법: py add_arena_radius.py
"""
import os, sys, io, msgpack, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "car_survivor_tables.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "CarSurvior", "Assets", "Resources", "Tables")

TYPES = [str, str, int, str, str, int, str, str, float]

def cast(val, t):
    if val is None:
        return "" if t == str else 0 if t == int else 0.0 if t == float else False
    if t == int: return int(float(val)) if val else 0
    if t == float: return float(val) if val else 0.0
    if t == str: return str(val) if val else ""
    return val

def main():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Stage"]

    # 헤더에 arena_radius 추가
    ws.cell(row=1, column=9, value="arena_radius")

    # 각 행에 기본값 설정
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row[0].value is None:
            break
        stage_no = row[2].value
        # 스테이지가 높을수록 아레나 넓게
        radius = 8.0 + (stage_no - 1) * 2.0
        ws.cell(row=row_idx, column=9, value=radius)
        print(f"행 {row_idx} (stage {stage_no}): arena_radius = {radius}")

    wb.save(XLSX_PATH)
    wb.close()

    # 재익스포트
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    ws = wb["TB_Stage"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None or str(row[0]).startswith("["): break
        rows.append([cast(row[i] if i < len(row) else None, TYPES[i]) for i in range(len(TYPES))])
    wb.close()

    packed = msgpack.packb(rows, use_bin_type=True, use_single_float=True)
    out_path = os.path.join(OUTPUT_DIR, "TB_Stage.bytes")
    with open(out_path, "wb") as f:
        f.write(packed)
    print(f"TB_Stage.bytes 재생성: {len(rows)} rows, {len(packed)} bytes")

if __name__ == "__main__":
    main()
