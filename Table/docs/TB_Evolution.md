# TB_Evolution (파츠 진��� 테이블)

> 두 파츠를 조합하여 상위 파츠로 진화시키는 레시피를 정의합니다.

## ���럼 정의

| ��럼명 | 타입 | 설명 |
|--------|------|------|
| `evo_id` | string **(PK)** | 진화 레���피 고유 ID. 형식: `EVO_###` |
| `evo_name` | string | 진화 결과 파츠 이름 (표시용) |
| `material_a_id` | string **(FK)** | 재료 A 파�� ID. → `TB_Part.part_id` |
| `material_a_level` | int | 재료 A가 도달해야 하는 최소 레벨 |
| `material_b_id` | string **(FK)** | ��료 B 파��� ID. → `TB_Part.part_id` |
| `material_b_level` | int | 재�� B가 도달해야 하는 최소 레벨 |
| `result_part_id` | string **(FK)** | 진화 결과 파츠 ID. → `TB_Part.part_id` (is_evolution_result=true인 파츠) |
| `visual_desc` | string | 진화 시 차량 외형 변화 설명. 아트팀 전달용 |
| `priority` | enum | 개발 우선순위. 값: `P0` (MVP 필수) / `P1` (중요) / `P2` (후순위) |

## 참조 관계

- **이 테이블이 참조하�� 곳:**
  - `material_a_id` → `TB_Part.part_id`
  - `material_b_id` → `TB_Part.part_id`
  - `result_part_id` �� `TB_Part.part_id`

## 진화 레시피 요약

| 결과 | 재료 A (레벨) | 재료 B (레벨) | 우선순위 |
|------|-------------|-------------|---------|
| 트윈터보 | ��보차저 (Lv3) | 슈퍼차저 (Lv1) | P0 |
| 유도 EMP 미사일 | 미사�� 런처 (Lv3) | EMP 펄스 (Lv1) | P0 |
| 화염 기관총 | 오일 슬릭 (Lv2) | 기관총 (Lv2) | P0 |
| 불도저 모드 | 강화 차�� (Lv3) | 사이드 램 (Lv1) | P1 |
| 슬립스트림 폭발 | NOS 부스터 (Lv1) | 드래프팅 (Lv1) | P1 |

## 비고

- 진화 조건 충족 시 자동으로 진화 선택지가 제공됨
- 진화하면 재료 A, B는 소멸되고 결과 파츠로 교체
- `result_part_id`는 반드시 `TB_Part`에서 `is_evolution_result=true`인 파츠여야 함
