# TB_Car (차량 테이블)

> 플레이어가 선택할 수 있는 차량의 기본 정보와 스��을 정의합니다.

## ��럼 정의

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `car_id` | string **(PK)** | 차량 고�� ID. 형식: `CAR_###` |
| `car_name` | string | 차량 표시 이름 |
| `car_type` | enum | 차량 타입. 값: `SportsCar` / `SUV` / `Truck` |
| `base_hp` | float | 기본 체력 (HP). 파츠에 의해 증감 |
| `base_speed` | float | ���본 이동속도 (units/sec) |
| `base_atk_speed` | float | 기본 공격속도 (shots/sec). 높을수록 빠름 |
| `base_damage` | float | 기�� 투사체 1회 데미지 |
| `collision_damage` | float | ���과 충돌 시 적에게 가하는 데미지 |
| `passive_type` | enum | 고유 패시브 종류. 값: `CooldownReduce` / `DefenseUp` / `CollisionReflect` |
| `passive_value` | float | 패시브 수치 (% 또는 고정값). passive_type에 따라 해석 다름 |
| `passive_desc` | string | 패시브 설명 (UI 표시용) |
| `unlock_cost` | int | 해금 비용. 0 = 무료(기본 차량) |
| `unlock_currency_id` | string **(FK)** | 해금에 사용하는 재화 ID. → `TB_Currency.currency_id` |
| `unlocked_by_default` | bool | `true` = 처음부터 사용 가능 |
| `sprite_key` | string | 차량 스프라이트 리소스 키 |

## 참조 관계

- **이 테이블이 참조하는 곳:**
  - `unlock_currency_id` → `TB_Currency.currency_id`
- **이 테이블을 ��조하는 곳:**
  - `TB_Shop.reward_target_id` → `car_id` (reward_type = Car일 때)

## 비고

- 현재 3종: 스포츠카(기본), SUV(골드 500), 트럭(골드 1500)
- 차량 추가 시 이 테이블에 행 추가 + TB_Shop에 해금 상품 추가
