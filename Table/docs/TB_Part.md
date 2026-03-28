# TB_Part (파츠 테이���)

> 게임 내 모든 파츠(기본 15종 + 진화 5종)의 정보를 정의합니다.

## 컬럼 정의

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `part_id` | string **(PK)** | 파츠 고유 ID. 형식: `PART_###` |
| `part_name` | string | 파츠 표시 이름 |
| `category` | enum | 파츠 카테고리. 값: `Engine` / `Weapon` / `Defense` / `Special` |
| `base_value` | float | 일반(Common) 등급 기준 효과 수치. 등급별 실제값 = base_value × `TB_PartGrade.value_multiplier` |
| `effect_type` | enum | 효과 종류. 값: `SpeedUp` / `AtkSpeedUp` / `DamageUp` / `HpUp` / `DefenseUp` / `HpRegen` / `CollisionReflect` / `ActiveSkill` |
| `effect_desc` | string | 효과 설명 (UI 카드 표시용) |
| `has_active` | bool | `true` = 액티브 스킬 보유. cooldown/duration 필드 사용 |
| `weapon_type` | enum | 무기 카테고리 파츠의 발사 타입. 값: `None` / `MachineGun` / `Missile` / `EMP` / `OilSlick` / `Mine` |
| `cooldown` | float | 액티브 스킬 재사용 대기시간 (초). has_active=false면 0 |
| `duration` | float | 액티브 ��킬 지속시간 (초). has_active=false면 0 |
| `max_level` | int | 파츠 최대 레벨. 일반=3, 진화=5 |
| `stackable` | bool | `true` = 같은 파츠 중복 장착 가능 |
| `drop_weight` | int | 레벨업 시 등장 가중치. 높을수록 자주 등장. 진화 파츠=0 (드랍 불가) |
| `is_evolution_result` | bool | `true` = 진화로만 획득 가능한 파츠. 드랍/상점 불가 |
| `icon_key` | string | ���츠 아이콘 리소��� 키 |

## 참조 관���

- **이 테이블을 참조하�� 곳:**
  - `TB_Evolution.material_a_id` → `part_id`
  - `TB_Evolution.material_b_id` → `part_id`
  - `TB_Evolution.result_part_id` → `part_id`
  - `TB_MonsterDrop.special_drop_id` → `part_id`
  - `TB_Shop.reward_target_id` → `part_id` (reward_type = Part일 때)

## 파츠 구성 요약

| 카테고리 | 기본 파츠 | 진화 파츠 |
|----------|----------|----------|
| Engine | 터보차저, 슈퍼차저, NOS 부스터, 경량화 섀시 | 트윈터보 |
| Weapon | 기관총, 미사일 런처, EMP 펄스, 오일 슬릭, 지뢰 투하 | 유도 EMP 미사일, 화염 기관총 |
| Defense | 런플랫 타이어, 강화 차체, 사이드 램 | 불도저 모드 |
| Special | 드래프팅, 자동 수리 킷, 레이더 | 슬립스트림 폭발 |

## 비고

- `is_evolution_result=true`인 파츠는 `drop_weight=0`이어야 함 (레벨업 선택지에 등장하면 안 됨)
- 등급별 실제 수치 계산: `base_value × TB_PartGrade.value_multiplier`
- 레벨별 수치 스케일링은 코드에서 처리 (base_value × level)
