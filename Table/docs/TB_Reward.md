# TB_Reward (보상 테이��)

> 런 완료, 보스 처치, 광고 시청, 일일 접속 등 이벤트별 보���을 정의합니다.

## 컬럼 정의

| 컬���명 | 타입 | 설명 |
|--------|------|------|
| `reward_id` | string **(PK)** | 보상 고유 ID. 형식: `RWD_###` |
| `reward_trigger` | enum | 보상 발동 조건. 값: `RunComplete` / `BossClear` / `AdWatch` / `DailyLogin` |
| `currency_id` | string **(FK)** | 지급할 재화 ID. → `TB_Currency.currency_id` |
| `amount` | int | 기본 지급 수량 |
| `bonus_multiplier` | float | 보너스 배율. 1.0 = 기본. 광고 시청 등으로 2.0 적용 가능 |
| `note` | string | ��고 |

## 참조 관계

- **이 테���블이 참��하는 곳:**
  - `currency_id` → `TB_Currency.currency_id`

## 보상 요약

| 트리거 | 골드 | 스크랩 | 비고 |
|--------|------|--------|------|
| RunComplete | 100 | 20 | 런 완료 기본 보상 |
| BossClear | 200 | 50 | 보스 처치 추가 보상 |
| AdWatch | 200 (×2.0) | - | 광고 시청 시 골드 2배 |
| DailyLogin | 50 | 10 | 일일 접속 보상 |

## 데이터 구조 참고

- 한 트리거에 여러 재화를 지급하면 행을 나눔
  - 예: RunComplete → RWD_001 (골드 100) + RWD_002 (스���랩 20) = 2행

## 비고

- `bonus_multiplier`는 실제 지급량에 곱해짐: 실제 지급 = amount × bonus_multiplier
- 일일 획득량은 `TB_Currency.daily_cap`에 의해 제한됨
