# TB_Shop (상점 테이블)

> 인앱 구매(IAP) 상품과 인게임 재화 구매 상품을 정의합니다.

## 컬럼 ��의

| 컬럼명 | 타입 | ���명 |
|--------|------|------|
| `shop_id` | string **(PK)** | 상품 고유 ID. 형식: `SHOP_###` |
| `shop_name` | string | 상품 표시 이름 |
| `shop_type` | enum | 상��� 종류. 값: `IAP` (실제 결제) / `InGame` (인게임 재화) / `Ad` (광고 보상) |
| `price_type` | enum | 결제 수단. 값: `RealMoney` (원화) / `Gold` / `Scrap` |
| `price_amount` | int | 가격. RealMoney일 때 원(KRW) 단위 |
| `price_currency_id` | string **(FK, nullable)** | 인게임 재화 결제 시 재화 ID. → `TB_Currency.currency_id`. IAP면 null |
| `reward_type` | enum | 보상 종류. 값: `Currency` / `Part` / `Car` / `Cosmetic` / `System` |
| `reward_target_id` | string **(FK)** | 보상 대상 ID. reward_type에 따라 참조 테이블이 다름 |
| `reward_amount` | int | 보상 수량 |
| `is_one_time` | bool | `true` = 1회 구매 제한. `false` = 반복 구��� 가능 |
| `release_phase` | enum | 출시 단계. 값: `MVP` / `v1.5` / `v2` |
| `note` | string | 비고 |

## 참조 관계

- **이 테이블이 참조���는 곳:**
  - `price_currency_id` ��� `TB_Currency.currency_id`
  - `reward_target_id` → reward_type에 따라:
    - `Currency` → `TB_Currency.currency_id`
    - `Car` → `TB_Car.car_id`
    - `Part` → `TB_Part.part_id`
    - `Cosmetic` → 커스텀 ID (향후 테이블 확장)
    - `System` → 시스템 기능 ID (광고 제거 등)

## 상품 요약

| 상품 | 타입 | 가격 | 보상 | 출시 |
|------|------|------|------|------|
| 스타터 패키지 | IAP | ₩1,900 | 골드 1,000 + 레어 파츠 3개 | MVP |
| 프리미엄 도색 팩 | IAP | ₩2,900 | 메탈릭/크롬 색상 10종 | MVP |
| 프리미엄 휠 ��� | IAP | ₩2,900 | 특수 휠 5종 | MVP |
| 광고 제거 | IAP | ₩4,900 | 전면 광고 제거 | MVP |
| 월정액 카드 | IAP | ₩4,900 | 매일 골드 200 + 스크랩 50 | v1.5 |
| 시즌 번들 | IAP | ��9,900 | 한정 도색 + 휠 + 바디킷 | v2 |
| SUV 언락 | InGame | 골드 500 | SUV 차량 | MVP |
| 트럭 언락 | InGame | 골드 1,500 | 트럭 차량 | MVP |

## 비고

- IAP 상품의 `price_currency_id`는 null (실제 화폐 결제)
- InGame 상품은 `price_currency_id`로 사용할 재화를 지정
- `Cosmetic`, `System` reward_type은 현재 전용 테이블 없이 하드코딩 ID 사용 (향후 확장 시 별도 테이블 추가)
