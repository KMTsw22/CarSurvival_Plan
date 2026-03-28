# TB_MonsterDrop (�� 드랍 보상 테이블)

> 적 처치 시 드랍하는 경험치, 골드, 특수 아이템을 정��합니다.

## 컬럼 정의

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `drop_id` | string **(PK)** | 드랍 고유 ID. 형식: `DROP_###` |
| `mon_id` | string **(FK)** | 이 드랍을 가진 적 ID. → `TB_Monster.mon_id` |
| `exp_amount` | int | 처치 시 드랍하는 경험치(파편) 수량 |
| `gold_amount` | int | 처치 시 드랍하는 골드 수량 |
| `special_drop_id` | string **(FK, nullable)** | 특수 드랍 파츠 ID. → `TB_Part.part_id`. 없으면 null |
| `special_drop_rate` | float | 특수 드��� 확률 (%). 0 = 특수 드랍 없음 |

## 참조 관계

- **이 테이블이 참조하��� 곳:**
  - `mon_id` → `TB_Monster.mon_id`
  - `special_drop_id` → `TB_Part.part_id`

## 드랍 요약

| 적 | 경험치 | 골드 | 특수 드랍 |
|----|--------|------|----------|
| 러스티 세단 | 3 | 5 | - |
| 스파이크 바이크 | 2 | 3 | - |
| 장갑 픽업 | 5 | 8 | - |
| 불꽃 버�� | 4 | 6 | - |
| 워로드 탱크���럭 (보스) | 50 | 200 | - |

## 비고

- `TB_Monster`와 1:1 관계 (적 1종당 드랍 1행)
- 특수 드랍은 향후 확장용. 현재 모든 적의 special_drop_id = null
- 보스 처치 보상은 이 테이블 + `TB_Reward`(BossClear) 합산
