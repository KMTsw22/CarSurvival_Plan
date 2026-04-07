"""
TB_Weapon에 etc_comment1~5 컬럼 추가 — etc_value1~5 용도 설명을 텍스트 컬럼으로 저장

사용법: py add_etc_comment_columns.py
주의: 엑셀 파일을 먼저 닫고 실행하세요!
"""
import os, sys, io, openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(SCRIPT_DIR, "TableAsset", "TB_Weapon.xlsx")

# 무기별 etc_value1~5 용도 설명
# key = weapon_id, value = [etc1설명, etc2설명, etc3설명, etc4설명, etc5설명]
ETC_COMMENTS = {
    "WPN_001": [
        "(미사용)",
        "(미사용)",
        "(미사용)",
        "레벨당 데미지 증가",
        "(미사용)",
    ],
    "WPN_002": [
        "감속 비율 (50=50%)",
        "감속 지속시간 (초)",
        "기본 웅덩이 반경",
        "레벨당 반경 증가량",
        "(미사용)",
    ],
    "WPN_003": [
        "회전 속도 (도/초)",
        "궤도 반경",
        "타격 간격 (초)",
        "(미사용, 개수=레벨)",
        "(미사용)",
    ],
    "WPN_004": [
        "기본 타격 인원수",
        "레벨당 추가 인원 (+1)",
        "(미사용)",
        "(미사용)",
        "(미사용)",
    ],
    "WPN_005": [
        "기본 스턴 지속시간 (초)",
        "기본 반경",
        "레벨당 반경 증가량",
        "(미사용)",
        "(미사용)",
    ],
    "WPN_006": [
        "기본 화염 지속시간 (초)",
        "기본 화염 반경",
        "레벨당 반경 증가량",
        "화염 오프셋 Y",
        "(미사용)",
    ],
    "WPN_007": [
        "기본 레이저 줄기 수",
        "레벨당 레이저 추가 (+1)",
        "(미사용)",
        "(미사용)",
        "(미사용)",
    ],
    "WPN_008": [
        "기본 미사일 수",
        "레벨당 미사일 추가 (+1)",
        "(미사용)",
        "(미사용)",
        "(미사용)",
    ],
}


def main():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["TB_Weapon"]

    headers = [cell.value for cell in ws[1]]
    print(f"현재 컬럼 수: {len(headers)}")
    print(f"현재 헤더: {headers}")

    # etc_comment1~5 이미 있는지 확인
    if "etc_comment1" in headers:
        print("\netc_comment 컬럼이 이미 존재합니다. 값만 업데이트합니다.")
        comment_start_col = headers.index("etc_comment1") + 1  # 1-based
    else:
        # damage_per_level 뒤에 etc_comment1~5 삽입
        # damage_per_level = col 18, 그 뒤에 5개 컬럼 추가
        insert_col = 19  # col 19부터 삽입
        for i in range(5):
            ws.insert_cols(insert_col + i)
        # 헤더 작성
        for i in range(5):
            ws.cell(row=1, column=insert_col + i, value=f"etc_comment{i+1}")
        comment_start_col = insert_col
        print(f"\netc_comment1~5 컬럼 삽입 완료 (col {insert_col}~{insert_col+4})")

    # 데이터 행에 주석 텍스트 채우기
    count = 0
    for row in ws.iter_rows(min_row=2):
        wid = row[0].value
        if wid is None:
            break
        if wid not in ETC_COMMENTS:
            print(f"  [SKIP] {wid}: 주석 정의 없음")
            continue

        comments = ETC_COMMENTS[wid]
        for i, text in enumerate(comments):
            ws.cell(row=row[0].row, column=comment_start_col + i, value=text)
        count += 1
        print(f"  [OK] {wid}: 주석 5개 입력")

    print(f"\n총 {count}개 무기 주석 입력 완료")

    wb.save(XLSX_PATH)
    wb.close()
    print(f"저장 완료: {XLSX_PATH}")


if __name__ == "__main__":
    main()
