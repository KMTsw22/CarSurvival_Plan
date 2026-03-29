# TB_Map (맵 테이블)

> 게임에서 선택 가능한 맵(배경)의 정보를 정의합니다.

## 컬럼 정의

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `map_id` | string **(PK)** | 맵 고유 ID. 형식: `MAP_###` |
| `map_name` | string | 맵 표시 이름 |
| `map_desc` | string | 맵 설명 (UI 표시용) |
| `bg_sprite_key` | string | 배경 스프라이트 리소스 키. Resources 폴더 기준 |
| `tile_size` | float | 배경 타일 크기. 0 = 스프라이트 원본 크기 사용 |
| `grid_size` | int | 배경 타일링 반복 횟수 (중심 기준 ±N). 4 = 9x9 그리드 |
| `special_effect` | string | 맵 고유 효과. `None` / `Sandstorm` / `IceSlip` / `Rain` 등 |
| `unlock_cost` | int | 해금 비용. 0 = 무료(기본 맵) |
| `unlock_currency_id` | string **(FK)** | 해금 재화 ID. → `TB_Currency.currency_id` |
| `unlocked_by_default` | bool | `true` = 처음부터 사용 가능 |
| `release_phase` | enum | 출시 단계. 값: `MVP` / `v1.5` / `v2` |

## 참조 관계

- **이 테이블이 참조하는 곳:**
  - `unlock_currency_id` → `TB_Currency.currency_id`

## 맵 목록

| ID | 이름 | 효과 | 해금 | 출시 |
|----|------|------|------|------|
| MAP_001 | 야간 도시 고속도로 | 없음 | 무료 | MVP |
| MAP_002 | 사막 하이웨이 | 모래 폭풍 | 골드 1,000 | v2 |
| MAP_003 | 눈덮인 산악도로 | 빙판 미끄러짐 | 골드 2,000 | v2 |

## 비고

- MVP에서는 MAP_001만 사용
- `special_effect`는 코드에서 맵별 고유 로직으로 처리 (모래폭풍=시야 감소, 빙판=조작감 변경 등)
- `tile_size=0`이면 스프라이트의 `bounds.size`를 자동 사용
