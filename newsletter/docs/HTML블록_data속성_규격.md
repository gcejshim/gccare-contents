# 직접 만든 블록(HTML) — 편집용 data- 속성 규격

`gc-ax-insight` 스킬(콘텐츠 이미지)이 `html` 블록을 만들 때 이 규격대로 표시를 달면, AX Studio · Insight › 콘텐츠 이미지 생성 편집기에서 운영자가 **코드를 열지 않고** 미리보기에서 글자 · 숫자 · 막대 · 색을 고칠 수 있다.

- 적용: 편집기 2026-10-05 이후 (`editor/index.html`의 `hkRender` · `hkApply`)
- 스크립트(`<script>`)는 쓰지 않는다. 편집기가 속성만 읽는다.
- 고친 값은 블록 데이터의 `html` · `htmlMo` 코드에 그대로 반영된다 → 작업 파일 저장 · 불러오기 후에도 유지.
- 표시가 없는 예전 HTML 블록은 지금처럼 그린다 (하위 호환).
- ③ 상세 편집에는 코드 칸 대신 **글자 · 세로축 · 숫자 · 색 입력칸**이 자동으로 생긴다 (PC · 모바일 하나로). HTML 코드는 운영자 화면에 보이지 않는다.

## 1. 속성

| 속성 | 붙는 곳 | 편집기 동작 |
|---|---|---|
| `data-key="m-20-now"` | 고칠 수 있는 모든 요소 | PC(`html`)와 모바일(`htmlMo`)에서 **같은 key끼리 연결**. 한쪽을 고치면 양쪽 코드가 같이 바뀐다. 한 HTML 안에서도 같은 key 요소는 모두 같이 바뀐다 |
| `data-edit="text"` | 글자 (제목 · 말풍선 · 라벨 · 띠 · 범례) | 미리보기에서 클릭 → 인라인 수정 (Enter 확인 · Shift+Enter 줄바꿈 · Esc 취소). [굵게] · 글자 색 도구 사용 가능 |
| `data-edit="value"` | 숫자 라벨 | 인라인 수정 (숫자만). 같은 key의 `data-bar`도 같이 바뀌어 막대 높이가 다시 계산된다 |
| `data-bar="32.1"` | 막대 요소 | 높이 = 값 ÷ 최대값 × 100% 로 그린다 (편집기가 `style.height`를 넣음) |
| `data-max="80"` | 막대 요소 | 그 막대의 최대값 (축과 연결하지 않을 때) |
| `data-axis="axis"` | 막대 · 눈금 요소 | 아래 `data-max-key`로 정한 축의 최대값을 쓴다 (`data-max`보다 우선) |
| `data-max-key="axis"` | 세로축 최대값을 보여 주는 글자 요소 (예: 맨 위 눈금 "80") | 이 글자가 그 축의 최대값. 클릭해서 고치면 `data-axis="axis"` 막대 · 눈금 · 따라가는 요소가 모두 다시 계산된다 |
| `data-tick="0.5"` | 눈금 글자 | 글자 = 축 최대값 × 비율 (0 · 0.25 · 0.5 · 0.75 …). 위치는 CSS로 고정 (`bottom:50%` 등) |
| `data-follow="m-20-now"` | 말풍선 등 막대를 따라가는 요소 | 연결한 막대 높이에 맞춰 `style.bottom`을 넣는다. `position:absolute`, 막대와 같은 높이 기준 상자 안에 둔다 |
| `data-gap="8"` | `data-follow` 요소 | 막대 끝에서 띄울 거리(px). 결과: `bottom: calc(높이% + 8px)` |
| `data-label="남자 20대"` | 고칠 수 있는 모든 요소 (권장) | ③ 상세 편집 입력칸 이름. 없으면 `data-key`가 이름으로 보임 |
| `data-color="--careBlue-700"` | 색을 바꿀 수 있는 요소 (막대 · 띠 · 배지 · 보조 값 칸) | 편집기가 `background: var(토큰)`을 넣는다. `data-key`가 있으면 미리보기에서 눌러 색 고르기 → 같은 key 요소 모두 바뀜 |

### 주의
- `data-key`에는 영문 · 숫자 · `-`만 쓴다 (예: `m-20-now`, `f-30-note`, `axis`). `:` 쓰지 않기.
- 막대 높이를 CSS(`height:40%`)로 직접 쓰지 않는다. 편집기가 `data-bar`로 계산한다.
- 글자 요소 안에 다른 표시 요소를 넣지 않는다 (글자만, 굵게 `<b>` · 색 `<span class="tc-red">`는 가능).
- 숫자 라벨이 막대 안에 있으면 라벨을 누르면 숫자 수정, 막대의 빈 곳을 누르면 색 고르기.
- 색 글자는 편집기 글자 색 클래스를 쓴다: `tc-blue` · `tc-green` · `tc-red` · `tc-orange` · `tc-gray`.

## 2. 예시 (남자 20대 막대 · 말풍선 · 축)

```html
<style>
.ch{position:relative;height:240px;display:flex;align-items:flex-end;gap:24px;border-bottom:1px solid var(--coolNeutral-200)}
.ax{position:absolute;left:-36px;font-size:14px;color:var(--coolNeutral-600)}
.g{position:relative;flex:1;height:100%;display:flex;align-items:flex-end;justify-content:center;gap:4px}
.b{width:22px;border-radius:4px 4px 0 0;position:relative}
.v{position:absolute;top:-22px;left:50%;transform:translateX(-50%);font-size:14px;font-weight:700;color:var(--careBlue-700)}
.co{position:absolute;left:50%;transform:translateX(-50%);padding:4px 8px;border:1.5px solid var(--careRed-500);border-radius:6px;background:#fff;color:var(--careRed-500);font-size:14px;font-weight:700;white-space:nowrap}
</style>
<div class="ch">
  <span class="ax" style="top:0" data-max-key="axis" data-key="axis">80</span>
  <span class="ax" style="bottom:50%" data-tick="0.5" data-axis="axis">40</span>
  <div class="g">
    <div class="co" data-key="m-20-note" data-edit="text" data-follow="m-20-now" data-gap="30">4.0%p 증가 ▲</div>
    <div class="b" data-key="m-20-prev" data-bar="28.1" data-axis="axis" data-color="--coolNeutral-200"></div>
    <div class="b" data-key="m-20-now" data-bar="32.1" data-axis="axis" data-color="--careBlue-700">
      <span class="v" data-key="m-20-now" data-edit="value">32.1</span>
    </div>
  </div>
</div>
```
- 32.1 → 35.0으로 고치면: PC · 모바일 막대 높이와 말풍선 위치가 같이 바뀜
- 맨 위 눈금 80 → 100으로 고치면: 모든 막대 · 가운데 눈금(40 → 50) · 말풍선이 다시 계산됨
- 파란 막대를 눌러 `careRed-500`을 고르면: PC · 모바일 둘 다 바뀜

## 3. 허용 색 토큰 (편집기에 정의된 전체)

`var(--이름)` · `data-color`에 쓸 수 있는 이름. 이 밖의 이름을 쓰면 색이 안 나오고, 자동 점검에 "편집기에 없는 색 토큰" 경고가 뜬다.

| 계열 | 단계 |
|---|---|
| careBlue | 10 · 50 · 100 · 200 · 300 · 400 · 500 · 600 · 700 · 800 · 900 |
| careGreen | 10 · 50 · 100 · 300 · 400 · 500 · 600 · 700 · 800 |
| careRed | 50 · 100 · 200 · 300 · 400 · 500 · 600 |
| careOrange | 50 · 100 · 200 · 300 · 400 · 500 · 600 |
| careYellow | 100 · 200 · 300 · 500 |
| coolNeutral | 50 · 100 · 200 · 300 · 400 · 500 · 600 · 800 |
| neutral | 0 · 100 · 500 · 600 · 700 · 900 |

- 흰색 `#fff`, 그림자 `rgba(3,21,82,.06)`은 써도 됨. 그 밖의 hex는 쓰지 않는다 (자동 점검 안내).
- 미리보기에서 막대를 눌러 여는 색 고르기 창은 그래프 블록 색 지정(`cols`)과 같은 목록이다.

## 4. 폰트 크기 정책 (변경 없음)

| | PC | 모바일 |
|---|---|---|
| 헤드라인 | 28 Bold | 20~22 Bold |
| 블록 제목 | 22 Bold | 18 Bold |
| 본문 | 18 · 16 Medium | 16 · 14 Medium |
| 가장 작은 글자 | 14 | 12 |

## 5. 그 밖에 함께 바뀐 것

- **같은 번호 교체**: Ctrl+V · [Claude 스킬 결과 넣기] 모두, 같은 콘텐츠 · 이미지 번호가 있으면 "덮어쓸까요?" → 예: 그 이미지를 교체 / 취소: 아무것도 넣지 않음. (빈 새 이미지는 묻지 않고 교체)
- **그래프 2개 나란히**: `"left":{"type":"vbar","data":{…}},"right":{…}`로 그래프를 직접 담으면 이 이미지 전용 그래프로 들어간다 (`type`: line · donut · vbar · hbar · stack).
- **100% 누적 막대 보조 값**: `"side":"5점 평균(점)","sideRows":"3.48\n3.40"` → 막대 오른쪽에 값 칸 (비우면 없음). 미리보기에서 클릭해 고칠 수 있음.
- (참고) `texts` · `nums` · `colors` · `sizes` + `{{이름}}` 방식도 계속 동작한다. 새로 만들 때는 위 data- 속성 방식을 쓴다.
