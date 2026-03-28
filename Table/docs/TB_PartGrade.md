# TB_PartGrade (파츠 등급 배율 테이블)

> 파츠의 등급별 수치 배율과 UI 색상을 정의합니다.

## 컬럼 정의

| 컬럼명 | ��입 | 설명 |
|--------|------|------|
| `grade_id` | string **(PK)** | 등급 고유 ID. 형식: `GRADE_###` |
| `grade_name` | string | 등급 한글 표시 이��� |
| `grade_enum` | enum | 코드에서 사용하는 ��급 enum. 값: `Common` / `Rare` / `Epic` / `Legendary` / `Evolution` |
| `value_multiplier` | float | `TB_Part.base_value`에 곱하는 배율. 실제효과 = base_value × value_multiplier |
| `color_hex` | string | UI에서 등급 표시 색상 (HEX) |
| `sort_order` | int | 정렬 순서. 낮을수록 앞에 표시 |

## 참조 관계

- **이 테이블을 참���하는 곳:**
  - `TB_Level`의 등급 확률 (grade_common_pct ~ grade_legendary_pct)이 이 테이블의 등급 기준을 따름

## 등급별 배율 요약

| 등급 | 배율 | 색상 |
|------|------|------|
| 일반 (Common) | ×1.0 | ���색 #FFFFFF |
| 레어 (Rare) | ×1.3 | 파랑 #4FC3F7 |
| 에픽 (Epic) | ×1.6 | 보라 #CE93D8 |
| ��전더리 (Legendary) | ×2.0 | 금색 #FFD54F |
| 진화 (Evolution) | ×2.5 | 주황 #FF8A65 |

## 비고

- 등급 배율 변경 시 이 테이블만 수정하면 전체 파츠에 일괄 적용
