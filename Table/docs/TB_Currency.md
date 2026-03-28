# TB_Currency (재화 테이블)

> 게임 내 사용되는 모든 재화를 정의합니다.

## 컬럼 정의

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `currency_id` | string **(PK)** | 재화 고유 ID. 형식: `CUR_###` |
| `currency_name` | string | 재화 표시 이름 |
| `currency_desc` | string | 재화 용도 설명 (UI 툴팁용) |
| `daily_cap` | int | 하루 최대 획득 가능량. 0 = 무제한 |
| `icon_key` | string | UI 아이콘 리소스 키 |

## 참조 관계

- **이 테이블을 참조하는 곳:**
  - `TB_Car.unlock_currency_id` → `currency_id`
  - `TB_Reward.currency_id` → `currency_id`
  - `TB_Shop.price_currency_id` → `currency_id`
  - `TB_Shop.reward_target_id` → `currency_id` (reward_type = Currency일 때)

## 비고

- 현재 골드(CUR_001), 스크랩(CUR_002) 2종
- 신규 재화 추가 시 이 테이블에 행 추가 후, 관련 테이블에서 ID 참조
