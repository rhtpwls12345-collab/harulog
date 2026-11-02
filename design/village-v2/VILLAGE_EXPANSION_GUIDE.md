# 하루로그 마을 확장 가이드 — 테마 장면 · 움직이는 요소 · 가구 카탈로그

Claude Design에서 새로 디자인한 요소를 일상기록 앱 **하루로그**에 넣기 위한 적용 문서입니다.
앞서 전달한 `claude-design-result/HANDOFF.md`(일러스트 리디자인)를 이어서 확장하는 내용입니다.

> **Claude에게 (적용 작업 시 먼저 읽을 것)**
> 1. **기존 저장 데이터는 그대로 읽혀야 합니다.** 아래의 새 필드는 모두 선택 사항이고, 값이 없으면 지금 화면과 같게 그려지게 하세요.
> 2. 그림의 정답은 `generator/*.py`(SVG를 만드는 Python 코드)입니다. 좌표가 앱의 논리 단위와 1:1이라서 도형을 그대로 캔버스 함수로 옮기면 됩니다. 옮기기 어려운 것은 `furniture/**.svg`, `scenery/**.svg`를 이미지로 캐시해서 `drawImage` 해도 됩니다.
> 3. 키, 라벨, 크기, 통과 여부, 활동 자리는 `catalog.json` 하나에 모두 들어 있습니다. 하드코딩하지 말고 이 파일을 읽어서 쓰세요.
> 4. 작업은 아래 '적용 순서'대로 하나씩 진행하고, 단계마다 기존 마을이 깨지지 않는지 확인하세요.

---

## 1. 들어 있는 파일

| 경로 | 내용 |
|---|---|
| `catalog.json` | 가구 84종과 배경 요소 63종의 목록. key, 라벨, 크기(footprint), 실제 그림 범위(bbox), 통과 불가 여부(solid), 활동 자리(spot), SVG 경로 |
| `furniture/{home,work,cafe,dining,gym,park}/{key}.svg` | 장소별 가구·기구. **(0,0) = 바닥 자리의 왼쪽 위**(건물 로컬 좌표) |
| `scenery/{city,forest,coast,village}/{key}.svg` | 테마 배경 요소. 기준점은 `catalog.json`의 `anchor`를 따름(대부분 아래쪽 가운데 = 땅에 닿는 점) |
| `scenes/{theme}.svg` | 테마별 확장 장면 완성본(보통 3×2 지도 + 위·아래 배경 띠). 앱 화면과 비교할 기준 |
| `rooms/{kind}.svg` | 새 가구로 꾸민 방 예시(크게 320×172 칸) |
| `generator/` | `art.py`(기본 도형·건물), `world.py`(지도), `furniture.py`, `scenery.py`, `scenes.py`, `rooms.py` |

## 2. 데이터 확장 (하위 호환)

```js
profile.world = {
  theme, size, slots, props,                 // ← 기존 그대로
  scenery: true,                             // 새 필드(선택): 위·아래 배경 띠와 움직이는 요소 켜기. 없으면 true
  slots: [
    { kind:'gym', size:'l', color:'sky', style:'modern',
      items: [ { k:'treadmill', x:14, y:14 }, { k:'pool', x:16, y:74 } ] }   // 새 필드(선택): 칸 안의 가구
  ],
  props: { forest: [ { k:'fox', x:220, y:110 } ] }   // 기존 소품 배열에 새 key 사용 가능
}
```

- **`slots[i].items`**
  - 없으면 지금처럼 `KINDS[kind]`의 기본 가구를 그립니다.
  - 있으면 **기본 가구 대신** 이 목록을 그립니다.
  - 좌표 기준은 건물 로컬입니다. (0,0) = 뒷벽 왼쪽 위이고, 바닥은 y ≥ 36 입니다.
  - 칸 크기별 바닥 범위: 작게 224×140, 보통 272×156, 크게 320×172.
  - 공원(`park`)은 칸 전체(320×176)가 로컬 좌표입니다.
- **최대 개수:** 칸당 16개. 카페·식당·체육관 등 장소 종류와 맞는 가구만 고를 수 있게 하세요(`catalog.json → furniture[kind]`). 집은 `home`, 작업실은 `work` 목록을 씁니다.
- **겹침 검사:** `solid:true`인 가구끼리는 footprint 사각형이 겹치지 않게 하세요. 2단위 격자에 맞추면 됩니다.
- **소품:** `props[theme]` 최대 60개는 그대로입니다. 아래 '사용자가 놓을 수 있는 소품'을 각 테마 PROPS에 추가합니다.

## 3. 장소별 가구 카탈로그 (84종)

모든 가구는 `furniture.py`에 그림 함수로 있고, 행 하나 = `(key, 라벨, w, h, 그리는 함수, solid)` 입니다.
`spot`은 그 가구를 쓰는 활동을 할 때 캐릭터가 서는 자리로, 가구 왼쪽 위 기준 `(w/2, h+6)`(가구 앞 가운데)입니다.

| 장소 | 가구 (key) |
|---|---|
| **집 15** | TV와 TV장 `tv` · 옷장 `wardrobe` · 냉장고 `fridge` · 싱크대·가스레인지 `kitchen` · 2인 식탁 `dinette` · 공부 책상 `desk` · 1인 소파 `armchair` · 어항 `aquarium` · 업라이트 피아노 `piano` · 좌식 테이블 `floorsit` · 행거 `clothes` · 세탁기 `washer` · 욕조 `bathtub` · 몬스테라 화분 `monstera` · 화장대 `dresser` |
| **작업실·사무실 14** | 듀얼 모니터 책상 `pcdesk` · 파티션 자리 `partition` · 화이트보드 `whiteboard` · 복합기 `printer` · 정수기 `cooler` · 서류 캐비닛 `cabinet` · 회의 테이블 `meeting` · 사무용 의자 `officechair` · 커피 스테이션 `coffee` · 프로젝터 스크린 `projector` · 라운지 소파 `lounge` · 스탠딩 책상 `standing` · 우편함 선반 `mailshelf` · 탁구대 `pingpong` |
| **카페 13** | 에스프레소 바 `espresso` · 디저트 쇼케이스 `pastry` · 원형 테이블 세트 `roundset` · 창가 바 테이블 `barstools` · 원두 자루 `beans` · 콜드브루 디스펜서 `coldbrew` · 계산대 `pos` · 부스 좌석 `booth` · 케이크 스탠드 `cakestand` · 식물 선반 `plantshelf` · 동네 게시판 `board` · 테이크아웃 창구 `takeout` · 1인 소파 `armchair` |
| **식당 14** | 원형 테이블(3인) `roundtable` · 주방 화구 `stove` · 숯불 그릴 `grill` · 초밥 바 `sushibar` · 와인 랙 `winerack` · 샐러드 바 `saladbar` · 바 카운터 `bar` · 아기 의자 `highchair` · 디저트 카트 `dessertcart` · 수족관 `fishtank` · 안내 데스크 `host` · 주방 픽업대 `kitchenpass` · 뷔페 워머 `buffet` · 부스 좌석 `booth` |
| **체육관 14** | 러닝머신 `treadmill` · 수영장(레인 3) `pool` · 달리기 트랙 `track` · 실내 자전거 `bike` · 로잉 머신 `rowing` · 요가 매트 `yoga` · 케틀벨 랙 `kettle` · 사물함 `lockers` · 벤치프레스 `benchpress` · 철봉 `pullup` · 복싱 링 `ring` · 수건 선반 `towels` · 점수판 `scoreboard` · 공 거치대 `ballrack` |
| **공원 14** | 미끄럼틀 `slide` · 그네 `swing` · 시소 `seesaw` · 모래놀이터 `sandbox` · 피크닉 테이블 `picnic` · 정자 `gazebo` · 꽃 아치 `arch` · 자전거 거치대 `bikerack` · 아이스크림 카트 `icecream` · 음수대 `drinking` · 분리수거함 `trash` · 이정표 `signpost` · 정글짐 `junglegym` · 오리 연못 `duckpond` |

**통과 가능한 가구:** 좌식 테이블, 사무용 의자, 케이크 스탠드, 달리기 트랙, 요가 매트, 모래놀이터, 꽃 아치. 나머지는 모두 `solid`라서 footprint를 길찾기 장애물로 등록합니다.

**활동 연결 예시**(`spot.activity` 참고):

| 장소 | 활동 → 가구 |
|---|---|
| 체육관 | 달리기 → `treadmill`·`track`, 수영 → `pool`, 요가 → `yoga`, 근력 → `benchpress`·`kettle`·`pullup` |
| 집 | 요리 → `kitchen`, 식사 → `dinette`, 휴식 → `tv`, 공부·일기 → `desk`, 목욕 → `bathtub`, 빨래 → `washer`, 악기 → `piano` |
| 작업실 | 업무 → `pcdesk`·`partition`·`standing`, 회의 → `meeting`·`whiteboard`, 발표 → `projector` |
| 카페 | 친구 만남 → `booth`·`roundset`, 혼자 커피 → `barstools` |
| 식당 | 모임 → `roundtable`, 외식 → `sushibar`·`booth` |
| 공원 | 피크닉 → `picnic`, 산책 쉬기 → `gazebo`, 놀이 → `slide`·`swing` |

- 활동에 맞는 가구가 칸에 없으면 지금처럼 기본 자리(또는 집·길)에서 재현합니다.
- 방 예시 배치(크게 칸)는 `catalog.json → rooms`에 `{k,x,y}` 목록으로 들어 있어서, '추천 배치'나 '기본값으로' 버튼에 그대로 쓸 수 있습니다.

## 4. 테마 장면 확장 (배경 띠)

`scenery !== false`이면 지도 위·아래에 테마 배경 띠를 붙입니다.

| 테마 | 위 띠 T | 아래 띠 B | 위 띠 내용 | 아래 띠 내용 |
|---|---|---|---|---|
| city | 150 | 80 | 고층빌딩 스카이라인과 인도 | 왕복 대로(버스·택시·트럭·승용차)와 인도 |
| forest | 120 | 70 | 계곡 물줄기(y 40–76), 폭포, 나무 다리, 꽃밭, 텐트와 모닥불, 동물 | 침엽수 숲, 산딸기, 반딧불이 |
| coast | 80 | 150 | 모래언덕, 비치 오두막, 비치발리볼, 수산 가판 | 넓은 바다, 부두, 고기잡이 배, 돛단배, 부표, 카약, 등대 |
| village | 140 | 74 | 배추·당근·밀밭, 헛간, 풍차, 젖소·양·닭, 호박, 벌통, 트랙터 | 개울과 징검다리, 빨랫줄, 장독대, 우체통, 감나무 |

- **지도 크기:** `WH = 기존 WH + T + B`. 지도 전체를 `OY += T`만큼 내려 그리면 기존 좌표를 바꿀 필요가 없습니다.
- **카메라:** 이동 범위를 새 WH에 맞춰 넓힙니다.
- **길찾기:** 배경 띠는 걷지 못하는 곳으로 둡니다. 도시의 인도(위 띠 맨 아래 22단위, 아래 띠 위 4단위)만 NPC 전용으로 씁니다.
- **고정 배경 배치:** 위치는 `scenes.py → scene(theme)`의 `sprites` 목록이 정답입니다. 모든 x는 지도 폭 WW 기준이라, 작게(2×2)·크게(4×2) 맵에서는 `x * WW / 1056`으로 비례 배치하거나 `range(…, WW, 간격)`처럼 반복 배치하세요.
- **그리는 순서:** 바탕 → 띠 바닥(계곡·바다·대로) → 지도 → y 기준으로 정렬한 스프라이트(건물 앞 나무, 소품, 차, NPC, 동물). 앱에서 이미 쓰는 y 정렬과 같은 규칙입니다.

## 5. 움직이는 요소 (애니메이션)

| 요소 | 그림 | 움직임 규칙(권장) |
|---|---|---|
| 승용차·택시·버스·트럭 (가로 도로) | `car_side(color, facing, kind)` | 차선 2개: 도로 위 y+10은 왼쪽으로, y+22는 오른쪽으로 갑니다. 속도 40–60u/s. 화면 끝을 넘으면 반대편에서 다시 나옵니다. 횡단보도 앞 8u에서 0.8초 멈춤(선택) |
| 차 (세로 도로) | `car_front(color)` / `car_front(color, back=True)` | 세로 도로 가운데 x+10. 아래로 갈 때 앞모습, 위로 갈 때 뒷모습. 속도 35u/s |
| 대로 차량 (도시 아래 띠) | 위와 같음 | 차선 y = 띠 시작 +30(왼쪽) / +56(오른쪽). 버스 1대, 택시 1–2대 |
| NPC 행인 | Haru Avatar Kit `createWalker(randomAvatar())` | 인도·도로 가장자리를 따라 18u/s. 방향에 맞춰 `direction`을 바꿉니다. 도시 6–10명, 다른 테마 2–3명. 3–8초마다 잠깐 멈춤(idle) |
| 고기잡이 배·돛단배 | `fishboat()`, `sailboat()` | 위아래로 ±1.5u 출렁임(3초 주기), 좌우로 천천히 이동(5u/s) |
| 부표 | `buoy()` | ±1u 출렁임, 꼭대기 불빛이 1초마다 깜빡 |
| 갈매기 | `p_gull` | 하늘을 사인 곡선으로 날기. 가끔 부두에 앉음 |
| 풍차 | `windmill(t)` | `t` = 각도(도). 초당 30° 회전 |
| 오리 가족 | `ducks()` | 계곡·개울을 따라 4u/s, 물결 선이 뒤따라감 |
| 나비·반딧불이 | `butterflies()`, `fireflies()` | 작은 원을 그리며 떠다님. 반딧불이는 노을·밤에만 표시하고 투명도를 깜빡임 |
| 모닥불 | `campfire()` | 불꽃 높이를 0.9–1.1배로 0.3초마다 흔들기. 밤에는 주변 빛 원을 2배로 |
| 동물 (여우·곰·사슴·토끼·닭·양) | 각 함수 | 제자리에서 1–2초 걷고 쉬기를 반복(반경 20u). 좌우 반전은 `scale(-1,1)` |
| 고층빌딩 창문 | `tower(..., seed)` | 밤에는 켜진 창 비율을 20%에서 60%로 |

- 날씨와 시간대: 기존 하늘·땅 색 로직을 그대로 적용합니다.
- 눈이 오면 밭, 꽃밭, 지붕 윗면(헛간·오두막·등대 지붕)에 흰색을 덧칠합니다.
- 비가 오면 배와 차의 움직임을 0.7배로 줄입니다.

## 6. 사용자가 놓을 수 있는 소품 (PROPS 추가)

기존 소품에 아래 key를 더합니다. 크고 고정된 것(빌딩, 계곡, 밭, 부두, 등대, 헛간, 풍차)은 장면 고정 배경이라 제외했습니다.

| 테마 | 추가 소품 key |
|---|---|
| city | `hydrant`, `trashcan`, `cone`, `pigeons`, `phonebooth`, `kiosk`, `billboard`, `foodtruck` |
| forest | `fox`, `bearcub`, `owl`, `ducks`, `butterflies`, `hedgehog`, `tent`, `campfire`, `fireflies`, `birdhouse`, `berrybush`, `meadow` |
| coast | `crab`, `shells`, `towel`, `lifeguard`, `volleyball`, `beachhut`, `fishcrates`, `fishstall`, `kayak`, `buoy` |
| village | `chicken`, `cow`, `sheep`, `pumpkins`, `jangdok`, `beehive`, `tractor`, `laundry`, `mailbox`, `persimmon`, `stepstones` |

- `solid` 크기는 `catalog.json`의 bbox 폭 ×0.6, 높이 3–4u 정도로 잡으면 자연스럽습니다.
- 소품 팔레트 썸네일은 `scenery/{theme}/{key}.svg`를 그대로 쓰면 됩니다.

## 7. 꾸미기 화면 추가 UI

- **칸 편집에 '가구' 탭 추가**
  - 장소에 맞는 가구 그림 타일을 보여 줍니다(7열 PC / 3열 모바일).
  - 타일을 누르면 미리보기 위 그 칸 가운데에 놓이고, 끌어서 옮깁니다. 위치는 2u 격자에 맞춥니다.
  - 놓인 가구를 다시 누르면 '삭제' 버튼이 나옵니다.
  - 버튼: '추천 배치'(`catalog.rooms`), '가구 모두 치우기'(기본 가구로 되돌림).
- **소품 팔레트:** 테마마다 소품 수가 늘었으니 가로 스크롤 대신 접이식 그리드로 바꿉니다(처음 2줄만 보이고 '더 보기').
- **장면 토글:** '배경 장면 보기' 스위치를 둡니다(`scenery`). 저사양 기기는 끈 상태로 시작해도 됩니다.
- 모든 버튼은 40px 이상, 선택 상태는 `aria-pressed`로 표시합니다.

## 8. 성능 메모

- 고정 배경(빌딩, 밭, 계곡, 바다)은 테마와 맵 크기가 바뀔 때만 **오프스크린 캔버스에 한 번 그려 캐시**합니다.
- 움직이는 요소(차, NPC, 배, 동물)만 매 프레임 다시 그립니다.
- SVG를 이미지로 쓸 때는 줌 단계별로 `devicePixelRatio`에 맞춘 비트맵을 캐시하세요.
- NPC는 화면 밖에 있으면 위치만 갱신하고 그리지 않습니다.

## 9. 적용 순서 (권장)

1. **`catalog.json` 로드 + 가구 그리기 함수 이식.** `slots[i].items`가 없을 때 기존과 똑같이 보이는지 확인합니다.
2. **`slots[i].items` 렌더 + solid 등록 + spot 활동 연결.** 방 예시(`rooms`)로 체육관·작업실을 꾸며서 확인합니다.
3. **꾸미기 화면 '가구' 탭.**
4. **테마 배경 띠(고정).** 캐시로 그립니다.
5. **움직이는 요소.** 차 → NPC → 배·동물 순서로 넣습니다.
6. **PROPS 확장 + 소품 팔레트 정리.**
