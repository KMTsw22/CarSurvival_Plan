# TB_Monster (적 테이블)

> 게임에 등장하는 모든 적(일반 몬스터 + 보스)의 기본 스탯을 정의합���다.

## 컬럼 정의

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `mon_id` | string **(PK)** | 적 고유 ID. 형식: `MON_###` |
| `mon_name` | string | 적 표시 이름 |
| `is_boss` | bool | `true` = ���스 몬스터. 보스는 TB_Wave에서 단독 등장 |
| `base_hp` | float | ��본 체력. `TB_Wave.difficulty_scale`에 의해 스케일링됨 |
| `base_speed` | float | 이동속도 (units/sec). 난이도 배율 적용됨 |
| `contact_damage` | float | 플레이어와 충돌 시 프레임당 데미지 |
| `scale` | float | 스프라��트 크기 배율. 1.0 = 기본 크기 |
| `spawn_start_min` | int | 이 적이 처음 등장하�� 시간 (분). 0 = 게임 시작부터 |
| `spawn_weight` | int | 스폰 가중치. 높을수록 해당 시간대에 자주 스폰 |
| `special_ability` | string | 특수 능력. `None` = 없음 / `FlameTrail` = 화염 궤적 / `ThreePhase` = 3페이즈 보스 |
| `tint_color` | string | 스프라이트 색조 (HEX). 시각적 구분용 |
| `sprite_key` | string | 스프라이트 리소스 키 |

## 참조 관계

- **�� 테이블을 참조하는 곳:**
  - `TB_MonsterDrop.mon_id` → `mon_id`
  - `TB_Wave.mon_id` → `mon_id`

## 적 종류 요약

| 이름 | 보스 | HP | 속도 | 등장 시점 | 특징 |
|------|------|-----|------|----------|------|
| 러스티 세단 | - | 60 | 2 | 0분 | 기본 적, 항상 스폰 |
| 스파이크 바이크 | - | 30 | 5 | 2분 | 빠름, 측면 기습 |
| 장갑 픽업 | - | 150 | 1.5 | 4분 | 느리지만 체력 높음 |
| 불꽃 버기 | - | 50 | 4.5 | 7분 | 화염 궤적 남김 |
| 워로드 탱크트럭 | ★ | 2000 | 1 | 12분 | 런 종료 보스, 3페이즈 |

## 비고

- 난이도 스케일링: 실제 HP = `base_hp × TB_Wave.difficulty_scale`
- 보스는 `spawn_weight=1`로 고정, TB_Wave에서 직접 스폰 시점 지정
