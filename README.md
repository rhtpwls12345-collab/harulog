# 하루로그 Android 앱 (Capacitor)

웹 버전 하루로그를 그대로 감싸고, 앱에서만 되는 4가지 자동 기록을 붙인 Android 프로젝트예요.

| 연동 | 어디서 읽나 | 초안 카드에 나오는 것 |
|---|---|---|
| 실제 날씨 | 대략적 위치(약 1km) → Open-Meteo (API 키 필요 없음) | 날씨·기온 (최근 31일까지) |
| 워치·건강 앱 수면 | Health Connect `sleep` | 기상 시각, 취침 시각 + 수면 시간 |
| 워치·건강 앱 운동·걸음 | Health Connect `workouts`, `steps` | 운동(러닝·요가…) 시작 시각과 시간, 하루 걸음 수 4,000보 이상이면 걷기 |
| 휴대폰 사용으로 수면 추정 | 사용 정보 접근(화면 켜짐·꺼짐 시각만) | 워치 수면이 없을 때만 기상·취침 추정 |
| 캘린더 일정 | 휴대폰 캘린더(구글 캘린더 포함) | 그날 지난 일정 → 제목·시간으로 초안 (종류는 제목으로 추측, 하루 종일·거절한 일정 제외) |
| 이동 수단 감지 | 구글 활동 인식 Transition API (위치 안 씀) | 차량 이동 8분↑, 자전거 8분↑, 달리기 10분↑, 걷기 15분↑ |
| 사진 | 갤러리 사진의 찍은 시각 | 같은 시간대 일정·운동 초안에 사진 첨부, 아니면 “무엇을 했나요?” 초안 |

모든 항목은 **‘오늘 하루 초안’ 카드에 제안으로만** 나오고 ‘맞아요’를 눌러야 저장돼요. 기록은 휴대폰 안에만 저장돼요.

---

## 0. PC에서 바로 테스트 (설치 없이)

`pc-test.html`을 더블클릭해서 크롬/엣지로 열면 **앱 버전 화면을 PC에서 그대로** 써 볼 수 있어요.

- 휴대폰 권한(위치·Health Connect·사용 정보 접근)과 워치 데이터는 **가짜로 흉내** 내요. 버튼을 누르면 허용한 것으로 처리돼요.
- 날씨는 서울 기준 실제 날씨를 가져오고, 인터넷이 안 되면 가짜 날씨로 바뀌어요.
- 오른쪽 아래 **PC 테스트 모드** 버튼: 데이터 상황(워치 있음 / 휴대폰만 / 없음), Health Connect 미설치, 권한 초기화를 바꿔 볼 수 있어요.
- 휴대폰 크기로 보려면 `F12` → 왼쪽 위 휴대폰 아이콘(기기 툴바)을 켜세요.
- 기록은 PC 브라우저에만 저장되고 휴대폰 앱과는 별개예요.

`src/` 를 고친 뒤 `npm run build` 하면 `pc-test.html`도 함께 새로 만들어져요. (`pc-test.html`과 `src/pc-mock.js`는 휴대폰 앱에는 들어가지 않아요.)

## 1. 준비물 (처음 한 번)

1. **Node.js 20 이상** — https://nodejs.org (LTS)
2. **Android Studio** (최신 안정판) — https://developer.android.com/studio
   - 처음 실행 때 나오는 설정 마법사에서 *Standard* 선택 → Android SDK가 함께 설치돼요.
   - Android Studio 안에 JDK 21이 들어 있어서 따로 설치하지 않아도 돼요.
3. **테스트할 Android 휴대폰** (Android 8.0 이상, 권장 Android 14 이상)
   - 설정 › 휴대폰 정보 › 소프트웨어 정보 › *빌드번호*를 7번 눌러 개발자 모드 켜기
   - 설정 › 개발자 옵션 › *USB 디버깅* 켜기 → USB로 PC에 연결 → 휴대폰에 뜨는 ‘USB 디버깅 허용’ 확인

> 휴대폰이 없으면 Android Studio의 에뮬레이터(Device Manager › Create device, API 34 이상)로도 화면과 날씨는 확인할 수 있어요. 수면·운동은 실제 데이터가 없어서 비어 보여요.

## 2. 프로젝트 열기

이 폴더(`harulog-app`)에서 터미널(Windows는 PowerShell)을 열고:

```bash
npm install          # node_modules 설치 (처음 한 번)
npm run sync         # 웹 화면 빌드 → android 프로젝트로 복사
npm run open         # Android Studio로 열기
```

`npm run open`이 Android Studio를 못 찾으면, Android Studio에서 **File › Open** → `harulog-app/android` 폴더를 직접 열어도 돼요.

## 3. 휴대폰에 설치해서 실행

1. Android Studio 아래쪽에 *Gradle sync*가 끝날 때까지 기다려요 (처음엔 몇 분 걸려요).
2. 위쪽 기기 목록에서 연결한 휴대폰을 고르고 ▶ **Run 'app'** 클릭.
3. 휴대폰에 ‘하루로그’가 설치되고 바로 열려요.

APK 파일만 만들고 싶으면: **Build › Build App Bundle(s) / APK(s) › Build APK(s)** → 완료 알림의 *locate*를 누르면 `android/app/build/outputs/apk/debug/app-debug.apk`가 있어요. 이 파일을 휴대폰으로 옮겨 설치할 수도 있어요(출처를 알 수 없는 앱 허용 필요).

## 4. 앱에서 연동 켜기

앱 › **설정 › 자동 기록 연결** (오늘 화면 초안 카드의 *연결 설정* 버튼으로도 갈 수 있어요)

1. **날씨 자동 입력 › 위치 허용** → ‘대략적인 위치’로 허용하면 충분해요.
2. **워치·건강 앱 › 연결하기** → Health Connect 권한 화면에서 *수면, 걸음 수, 운동* 허용.
   - Android 13 이하는 Play 스토어에서 **Health Connect** 앱을 먼저 설치해야 해요 (버튼이 *Health Connect 설치·열기*로 바뀌어 있어요).
   - 워치 데이터가 Health Connect에 들어오도록 연결해 두세요. 예: **삼성 헬스 › 설정 › Health Connect**에서 수면·운동·걸음 수 공유 켜기. Fitbit, Google Fit 등도 각 앱 설정에서 Health Connect 연결.
3. **휴대폰 사용으로 수면 추정 › 사용 정보 접근 허용** → 설정 화면에서 ‘하루로그’ 찾아 허용 → 뒤로 가기. 앱으로 돌아오면 상태가 자동으로 갱신돼요.
4. **캘린더 일정 › 캘린더 허용**. 구글 캘린더 일정이 안 보이면 휴대폰 *구글 캘린더 앱 › 설정*에서 해당 계정 동기화가 켜져 있는지 확인하세요.
5. **이동 수단 감지 › 신체 활동 허용** → 자동으로 감지가 시작돼요. **켠 뒤부터** 기록되니 하루 정도 지나야 초안이 나와요. (구글 플레이 서비스가 있는 휴대폰만 지원)
6. **사진 › 사진 허용** → ‘모두 허용’ 또는 ‘일부 사진 선택’(Android 14+) 중 고를 수 있어요. 일부만 허용하면 고른 사진만 보여요.

기록 추가·수정 화면의 **사진** 칸에서도 갤러리 사진을 직접 고를 수 있어요(최대 6장). 사진은 1280px로 줄여 앱 안에만 저장되고, 하루 영상 카드에도 나와요. 백업 파일에는 사진이 들어가지 않아요.

오늘 화면으로 돌아가면 초안 카드에 ‘워치·건강’, ‘날씨’, ‘휴대폰 사용’ 표시가 붙은 제안이 나와요. 안 보이면 초안 카드의 **다시 읽기**를 눌러 보세요.

## 5. 화면(웹) 수정하는 방법

| 파일 | 내용 |
|---|---|
| `src/harulog.html` | 앱 화면 전체 (웹 아티팩트 버전과 같은 원본) |
| `src/native.js` | 앱 전용 연동: 날씨, Health Connect, 휴대폰 수면 추정, 설정 카드 |
| `src/pc-mock.js` | PC 테스트용 가짜 플러그인과 테스트 패널 (`pc-test.html`에만 들어감) |
| `src/privacypolicy.html` | 개인정보 처리방침 (Health Connect 권한 화면에서 열려요) |
| `scripts/build-www.mjs` | 위 파일들을 `www/`의 완전한 HTML로 묶는 스크립트 |
| `android/app/src/main/java/com/harulog/app/PhoneSignalsPlugin.java` | 화면 켜짐·꺼짐 시각을 읽는 자체 플러그인 |
| `android/.../DayDataPlugin.java` | 캘린더 일정, 갤러리 사진 목록·축소본, 이동 감지 켜기/끄기·기록 읽기 |
| `android/.../TransitionTracker.java`, `TransitionReceiver.java`, `BootReceiver.java` | 활동 인식 등록, 전환 기록 저장(14일), 재부팅 후 다시 등록 |
| `android/app/src/main/AndroidManifest.xml` | 권한 (대략적 위치, 사용 정보 접근, Health Connect 읽기 3종, 캘린더, 사진, 신체 활동, 부팅 완료) |

`src/`를 고친 뒤에는 항상:

```bash
npm run sync
```

그리고 Android Studio에서 ▶ Run을 다시 누르면 돼요. (`www/`와 `android/app/src/main/assets/public/`은 자동 생성되니 직접 고치지 마세요.)

### 휴대폰 화면을 PC에서 디버깅
PC 크롬 주소창에 `chrome://inspect` → 휴대폰의 하루로그 WebView 아래 *inspect* → 콘솔에서 오류와 `[harulog]` 경고를 볼 수 있어요.

## 마을 확장 그림(v2) 고치기

마을의 가구 84종, 테마 배경 띠, 움직이는 차·배·동물 그림은 `design/village-v2/`(Claude Design 결과물)에서 만들어져요.

| 파일 | 내용 |
|---|---|
| `design/village-v2/catalog.json` | 가구·배경 요소 목록(라벨, 크기, 통과 여부, 활동 자리) |
| `design/village-v2/furniture/`, `scenery/` | 가구·배경 요소 SVG |
| `design/village-v2/generator/` | 그림을 만든 Python 코드 |
| `scripts/build-village-assets.py` | 위 파일들을 앱이 바로 그리는 '그리기 명령'으로 바꿔 `src/harulog.html`에 넣음 |

디자인 파일을 바꿨다면:

```bash
python3 scripts/build-village-assets.py   # Python 3 필요
npm run sync
```

## 기록 → 장면 그림 고치기 (반려동물 · 운동 소품 · 효과)

기록 내용에 맞춰 캐릭터가 움직이는 장면의 그림은 `design/scene`(Claude Design 결과물)에 있어요.

| 폴더 | 내용 |
|---|---|
| `design/scene/pets/` | 강아지·고양이 8종 × 걷기 4프레임·앉기·엎드리기 SVG, `anchors.json`(목줄 고리 좌표) |
| `design/scene/props/` | 운동 소품 22개 (바벨, 러닝머신, 수영 물결, 요가 매트, 스피닝·자전거, 샌드백, 글러브 …) |
| `design/scene/fx/` | 효과 5개 (하트, 반짝임, 손 흔들기, 음표, z) |
| `design/scene/ui/` | 말풍선·장면 칸·반려동물 카드 시안 (앱 CSS에 반영됨) |

SVG를 고친 뒤에는 이렇게 다시 만들어요.

```
python3 scripts/build-scene-assets.py   # SVG → 그리기 명령, src/harulog.html 의 sceneAssets 블록 갱신
node scripts/build-www.mjs              # 웹·PC 테스트 파일 다시 만들기
```

- 털 색이 바뀌는 면은 `var(--fur,…)`, `var(--fur-dark,…)`, 장비 색은 `var(--gear,…)` 로 표시해 두면 자동으로 바꿔 끼워져요.
- 목줄/하네스는 각각 `<g class="gear-collar">`, `<g class="gear-harness">` 묶음이에요.
- 확인용 테스트: `test/scene.test.js`(반려동물 등록·동행·말풍선), `test/scene-motions.test.js`(동작별 소품 스크린샷 `test/mo-*.png`)

## 팝업 장소

기록 제목·메모에 아래 말이 있으면, 그 활동 동안만 마을에 임시 가게가 생겨요(운동·수면·기상·이동 기록은 제외).

| 가게 | 키워드 예 |
|---|---|
| 병원 | 병원, 치과, 약국, 검진, 예방접종 |
| 영화관 | 영화, 극장, CGV, 메가박스 |
| 도서관 | 도서관, 책 빌림, 반납 |
| 마트 | 마트, 장보기, 편의점, 다이소, 시장 |
| 미용실 | 미용실, 커트, 펌, 염색, 네일 |
| 은행·관공서 | 은행, 주민센터, 우체국, 민원 |
| 노래방·공연 | 노래방, 콘서트, 뮤지컬, 연극 |

- 자리: 집에서 가까운 **빈 땅 → 광장 → 작은 숲** 칸에 보통 크기(272×156) 건물이 실내 가구까지 갖춰 잠깐 서요. 셋 다 없으면 **집 앞 도로에 팝업 트럭**이 들어와요.
- 연출: 공사 가림막 → ‘뿅!’ → 개업 리본·풍선, 활동이 끝나 캐릭터가 나오면 접혀서 원래 칸으로 돌아가요.
- 그림 원본은 `design/popup`(Claude Design 결과물)이에요. 고친 뒤 `python3 scripts/build-popup-assets.py` → `node scripts/build-www.mjs` 로 다시 만들어요.
- 기록 입력 창의 ‘장면 → 장소’에서 직접 고르거나 ‘원래 장소’로 끌 수 있어요(`activity.scene.p`).
- 키워드는 `src/harulog.html`의 `POPUPS` 표에서 고쳐요. 확인용 테스트는 `test/popup.test.js`예요.

## 서버 백업·로그인 켜기 (Supabase, 무료)
1. https://supabase.com 에서 가입 → **New project** (지역은 Northeast Asia (Seoul) 추천).
2. 왼쪽 **SQL Editor** → `supabase/schema.sql` 내용을 붙여 넣고 **Run**.
3. **Authentication → Sign In / Providers → Email**: 켜기, 비밀번호 최소 8자.
4. **Authentication → URL Configuration**: Site URL 에 배포 주소(`https://rhtpwls12345-collab.github.io/2---/`) 넣기.
5. **Project Settings → API** 에서 `Project URL` 과 `anon public` 키를 `src/config.js` 에 넣고 `npm run build`.
   - ⚠ `service_role` 키는 절대 넣지 마세요.
6. 앱 설정 → ‘계정과 서버 백업’에서 회원가입 → 로그인 → ‘지금 서버에 백업’.

## 웹 배포 (GitHub Pages, 무료)
1. 이 폴더를 GitHub 저장소에 올리기 (GitHub Desktop: File → Add local repository → Publish/Push).
2. 저장소 **Settings → Pages → Source: GitHub Actions**.
3. `main` 에 올릴 때마다 `.github/workflows/pages.yml` 이 자동으로 빌드·배포해요. 주소는 Actions 실행 결과에 나와요.

보안 점검 결과는 `SECURITY.md` 에 있어요.

## 6. 동작 원리 (요약)

- **날씨**: 위치를 소수점 2자리로 줄여 `api.open-meteo.com`에 최근 31일 + 오늘 일별 날씨를 한 번에 요청해 30분 캐시. 날씨 코드 → 맑음/흐림/비/눈/안개, 풍속 30km/h 이상이면 바람. 평균 기온 25°↑ 더움, 16°↑ 포근, 6°↑ 선선, 그 밑은 추움.
- **수면(Health Connect)**: 전날 18시~다음날 6시 사이 수면 기록을 1시간 이내 간격끼리 한 세션으로 묶고, ‘깨어 있음’ 구간은 수면 시간에서 빼요. 그날 3~14시에 끝난 가장 긴 세션 → 기상, 그날 19시~다음날 5시에 시작해 이미 끝난 세션 → 취침.
- **휴대폰 수면 추정**: 화면이 꺼져 있던 구간 중 3분 미만으로 잠깐 켠 것(시계 확인 등)은 이어 붙이고, 3시간 이상인 가장 긴 구간을 잠으로 봐요. 건강 앱 수면이 있으면 그걸 우선해요.
- **운동/걸음**: 그날 운동 기록은 종류별 한국어 이름으로, 걸음은 시간별 합계로 가장 많이 걸은 시간대를 골라요.

## 7. 스토어에 올리기 전에 꼭

- [ ] `src/privacypolicy.html`의 운영자·연락처 채우고, 가능하면 웹에도 올려서 Play Console에 URL 등록
- [ ] **Health Connect 권한 신청**: Play Console › 앱 콘텐츠 › *Health apps* 선언 + Health Connect 권한 사용 이유 작성 (수면·걸음·운동 읽기만 사용)
- [ ] **사용 정보 접근(PACKAGE_USAGE_STATS)**: Play 정책상 핵심 기능일 때만 허용돼요. 심사에서 문제가 되면 이 기능만 끄는 버전을 준비하세요 (`AndroidManifest.xml`에서 해당 권한 삭제 + 설정 카드 항목이 ‘미허용’으로 남을 뿐 앱은 정상 동작).
- [ ] Play Console › 앱 콘텐츠 › *데이터 보안*에 캘린더·사진·신체 활동 ‘기기 안에서만 처리’로 기재
- [ ] 앱 아이콘: Android Studio › `app` 우클릭 › New › Image Asset
- [ ] 릴리스 서명: Build › Generate Signed App Bundle → `.aab` 업로드
- [ ] `android/app/build.gradle`의 `versionCode` / `versionName` 올리기

## 8. 자주 막히는 곳

| 증상 | 해결 |
|---|---|
| `npm run open` 후 Android Studio가 안 열림 | Android Studio에서 `harulog-app/android` 폴더를 직접 열기 |
| Gradle sync 실패 `SDK location not found` | Android Studio로 열면 `local.properties`가 자동 생성돼요. 터미널 빌드라면 `ANDROID_HOME` 환경변수 설정 |
| 기기가 목록에 안 보임 | USB 케이블(데이터용)·USB 디버깅 허용 확인, Windows는 제조사 USB 드라이버(삼성: Samsung USB Driver) 설치 |
| 위치 허용했는데 날씨가 안 나옴 | 휴대폰의 위치(GPS) 자체가 꺼져 있는지 확인, 인터넷 연결 확인 후 *다시 읽기* |
| 워치 연결됨인데 수면이 안 나옴 | 삼성 헬스 등에서 Health Connect로 수면 공유가 켜져 있는지, 어젯밤 수면이 실제로 기록됐는지 확인 |
| 이동 감지가 계속 비어 있음 | 켠 뒤부터만 기록돼요. 배터리 최적화가 심한 기종은 설정 › 앱 › 하루로그 › 배터리 › ‘제한 없음’으로 바꿔 보세요 |
| 휴대폰 수면 추정이 이상함 | 밤에 음악·충전 화면 등으로 화면이 자주 켜지면 짧게 잘려요. 워치 수면이 있으면 그걸 우선 써요 |

## 9. 버전

Capacitor 8.5.3 · @capacitor/geolocation 8.2.4 · @capgo/capacitor-health 8.11.12 · play-services-location 21.3.0 · minSdk 26 · targetSdk 36

`test/native-mock.test.js`는 가짜 플러그인으로 연동 레이어를 브라우저에서 검증하는 Playwright 스크립트예요 (선택).
