---
name: gc-newsletter-block
description: GC케어 뉴스레터 기획안(PDF·PPT·문서·붙여넣은 텍스트)이나 참고 이미지를 받아 '뉴스레터 만들기 › 콘텐츠 이미지 생성' 편집기에 바로 붙여넣을 블록(JSON)을 만든다. 기존 블록(리스트·순위·표·차트 등)에 내용을 채우거나, 맞는 블록이 없으면 '직접 만든 블록(HTML)'을 만든다. 사용자가 뉴스레터 콘텐츠 이미지, PC·모바일 이미지, 15호 이미지, 블록 만들기, 표·차트 이미지, 블록에 없는 형태를 요청하면 사용한다.
---

# GC케어 뉴스레터 콘텐츠 블록 만들기

운영자가 올린 기획안을 **이미지 한 장 = 블록 하나**로 나누고, 편집기에 붙여넣을 JSON을 만든다. 디자인(색·글꼴·크기·2·3배 저장)은 편집기가 책임지므로, 여기서는 **블록 종류와 내용**을 정한다.

## 진행 순서

1. 기획안에서 **호수**와 콘텐츠(01 메인, 02 서브 …), 콘텐츠별 **이미지 순서**를 찾는다. 기획안에 "이미지 1/2/3"이 표시돼 있으면 그대로 따른다. 참고: 15호 = 2026년 10월.
2. 이미지마다 아래 **블록 고르기** 순서로 블록을 정한다.
3. 결과는 **JSON 코드 블록 하나**로 준다(여러 장이면 `nl-blocks`로 묶음). 블록마다 한 줄로 "어떤 블록을 왜 골랐는지"를 덧붙인다.
4. 마지막 안내 한 줄: "편집기(콘텐츠 이미지 생성) 화면 빈 곳을 누르고 Ctrl+V 하면 블록이 추가돼요. 화면 캡처·사진은 블록에서 직접 넣어 주세요."

기획안 문구와 수치를 **임의로 바꾸지 않는다.** 줄바꿈·강조만 정한다. 수치가 기획안에 없으면 지어내지 말고 빈칸으로 두고 알려 준다.

## 블록 고르기 (위에서부터 맞는 것)

| 기획안 내용 | 블록 `type` |
|---|---|
| 확인 항목 · 체크리스트 · 수칙 (아이콘 + 한 줄) | `list` |
| 설문 결과 (응답 + %) | `rank` |
| 항목별 비율 · 건수 비교 (가로 막대) | `hbar` |
| 기준표 · 방식 비교 · 과태료 등 칸으로 된 내용 | `table` |
| 전후 비교 · 그룹 비교 (세로 막대) | `vbar` |
| 구성비 (정상/전단계/유병 등 100%) | `stack` |
| 연도 · 월별 추이 | `line` |
| 업종별 · 유형별 구성비 (원형) | `donut` |
| 두 사업장 · 두 방식 비교 카드 | `compare` |
| 서비스 · 관리자 화면 소개 (헤드라인 + 캡처 1장) | `hero` |
| 앱 화면 2~4개를 단계로 소개 | `steps` |
| **위 어디에도 안 맞음** (인터뷰 말풍선, 단계 흐름, 인용, 특수 인포그래픽 등) | `html` |

`raw`(이미지 그대로)는 디자이너가 따로 만든 이미지를 넣는 블록이라 이 스킬에서는 만들지 않는다.

## JSON 형식

```json
{"kind":"nl-blocks","items":[
  {"kind":"nl-block","type":"table","contents":"01","no":1,"bg":"white","data":{ … }}
]}
```

- `contents`: "01" · "02" · "03", `no`: 그 콘텐츠 안의 이미지 번호(1부터)
- `bg`: `gray`(회색 바탕, 기본) · `white`(흰 바탕) · `none`(여백 없음). `hero` · `steps`는 쓰지 않음
- `data`는 아래 블록별 형식. 빠진 칸은 편집기 예시 값으로 채워지므로 **필요한 칸만** 써도 된다.
- 강조할 단어는 `[대괄호]`, 한 줄 입력칸 안 줄바꿈은 `//`

### 블록별 `data`

- `list`: `{"title":"지금 다시 확인할 변동 사항","headIcon":"SquareCheckBig","items":[{"icon":"Users","text":"…"}]}` (항목 3~7개)
- `rank`: `{"title":"질문","tag":"복수 응답","items":[{"text":"응답","value":75}]}` (값 큰 순서로 자동 정렬, 같은 값은 공동 순위)
- `hbar`: `{"title":"…","sub":"(*설명)","unit":"%","top":true,"items":[{"label":"항목","value":25.4}]}`
- `table`: `{"title":"…","head":"구분 | 직접 운영 | 위탁 운영","rows":"대상자 관리 | 내용//둘째 줄 | 내용\n…","firstCol":true,"icons":"Users\nCalendarDays","hl":"last"}` — 칸은 `|`, 행은 `\n`, 빨간 경고 글씨는 `!!글자!!`, `hl:"last"`면 마지막 열 강조
- `vbar`: `{"title":"…","sub":"(N=83)","unit":"","series":"참여 전 | 참여 후","rows":"수축기 혈압 | 143 | 125","hl":true}`
- `stack`: `{"title":"…","series":"정상 | 전단계 | 유병","rows":"참여 전 | 6 | 0 | 90","show":"value","unit":"명","accent":2}`
- `line`: `{"title":"…","sub":"('21~'25년)","unit":"명","series":"계열명","rows":"2021년 | 25\n2022년 | 29","labels":true}` (기본 그린, 파랑이면 `"green":false`)
- `donut`: `{"title":"…","unit":"%","center":"건설업\n46.5%","accent":true,"items":[{"label":"건설업","value":46.5}]}` (6개 넘으면 "기타"로 묶기)
- `compare`: `{"aName":"A 사업장","aMetrics":"수검률 | 40%\n예약률 | 75%","aStatus":"…","aStatusIcon":"CalendarCheck","aCheck":"…","aCheckIcon":"Target","bName":"B 사업장", … ,"statusTitle":"현재 상태","checkTitle":"확인할 사항"}`
- `hero`: `{"title":"우리 회사에 맞게 설정하고, [반복 업무는 줄이고]","frame":true,"winTitle":"어떠케어 - 내부 관리자"}` (캡처는 운영자가 넣음)
- `steps`: `{"title":"","items":[{"title":"걸음 수 추이 확인"},{"title":"나만의 캐릭터와 닉네임"}]}` (캡처는 운영자가 넣음)
- `html`: 아래 "직접 만든 블록" 참고 → `{"note":"인터뷰 말풍선 3개","html":"…","htmlMo":"…"}`

아이콘 이름(Lucide): `SquareCheckBig` `CircleCheck` `ListChecks` `ClipboardCheck` `ClipboardList` `Users` `UserCheck` `UserPlus` `UserX` `ContactRound` `IdCard` `Building2` `Hospital` `FileCheck` `FileText` `ShieldPlus` `ShieldCheck` `CalendarCheck` `CalendarDays` `Clock` `Search` `Target` `TrendingUp` `ChartColumn` `HeartPulse` `Heart` `Stethoscope` `Activity` `Pill` `Brain` `Footprints` `Thermometer` `Bell` `Megaphone` `Mail` `Smartphone` `Monitor` `MessageCircle` `Lightbulb` `Award` `Settings` `RefreshCw` `Info` `CircleAlert` `TriangleAlert` (표 첫 칸 · HTML 블록은 다른 Lucide 이름도 가능, 예: `ArrowLeftRight`)

## 직접 만든 블록 (`html`) 규칙

맞는 블록이 없을 때만 쓴다. 편집기가 이 코드를 PC(폭 900) · 모바일(폭 350)에 그려 2·3배 PNG로 저장한다.

**구조**
- `html`(PC)과 `htmlMo`(모바일)를 **따로** 만든다. 모바일은 위아래로 쌓고 글자를 줄인다.
- 맨 앞에 `<style>` 하나, 그 뒤에 내용. `<style>`의 선택자는 편집기가 이 블록 안으로 자동 한정하니 짧은 클래스 이름(`.q`, `.row`)을 써도 된다.
- 바깥 폭은 지정하지 않는다(블록 폭에 맞춰짐). `width:100%`, flex · grid로 배치한다. 고정 px 폭은 칸 하나 정도만.
- 바탕은 블록 설정(`bg`)이 깔아 주므로, 카드가 필요하면 `background:#fff;border-radius:16px;padding:28px 32px`처럼 안에서 만든다.

**글자 (Pretendard는 편집기가 넣어 줌 — `font-family` 쓰지 않기)**
| | PC | 모바일 |
|---|---|---|
| 큰 헤드라인 | 28 Bold | 20~22 Bold |
| 블록 제목 | 22 Bold | 18 Bold |
| 본문 | 18 · 16 Medium(500) | 16 · 14 Medium |
| 가장 작은 글자 | 14 | 12 |
- 기본 글자색은 `#111111`(따로 지정하지 않으면 됨). 회색 보조 글자는 `var(--coolNeutral-600)`.
- 줄 간격 1.5~1.65, `word-break:keep-all`은 편집기가 이미 적용.

**색 (토큰만 · `var(--이름)`으로 쓰기)**
- 블루 기본: `--careBlue-900`(남색 헤더·강조) `--careBlue-700` `--careBlue-500`(배지·아이콘) `--careBlue-400` `--careBlue-200` `--careBlue-100`(연파랑 배경) `--careBlue-50` `--careBlue-10`
- 그린은 포인트만: `--careGreen-500`(강조 숫자·단어) `--careGreen-700` `--careGreen-10`
- 뉴트럴: `--coolNeutral-50`(바탕) `--coolNeutral-100`(구분선) `--coolNeutral-600`(보조 글자) `--neutral-100`(#e6e6e6 표 선)
- 경고: `--careRed-500`, 주의 배경 `--careOrange-50`
- 흰색 `#fff`, 그림자 `rgba(3,21,82,.06)`은 써도 됨. 그 밖의 hex는 쓰지 않는다.
- 어두운 바탕 위 흰 제목은 `font-weight:600`.

**아이콘**: `<i data-icon="Users" data-color="--careBlue-500" data-size="22"></i>` → 편집기가 Lucide 아이콘으로 바꿔 줌. 원 안 아이콘이면 바깥 `span`에 배경·크기를 준다.

**쓰지 않는 것 (저장 PNG에서 깨지거나 막힘)**
- `<script>`, `on…=` 속성, `<iframe>`, 외부 링크 · 외부 이미지(`http…`) — 이미지가 필요하면 그 자리를 비우고 "이 이미지는 목업 히어로/이미지 그대로 블록으로 넣어 주세요"라고 안내
- `conic-gradient`, `backdrop-filter`, `filter`, `mix-blend-mode`, `clip-path`, `position:fixed`, `vw/vh` 단위, 웹폰트·`font-family`
- 원형 차트가 필요하면 `donut` 블록을 쓰고, HTML로 그리지 않는다.
- 이미지 안 글자 금지 원칙은 그대로: 글자는 모두 HTML 텍스트로.

## 예시 (10호 "기획자의 한 마디" → 맞는 블록이 없어 html)

```json
{"kind":"nl-block","type":"html","contents":"02","no":2,"bg":"gray","data":{"note":"기획자 한마디 인용","html":"<style>.q{background:#fff;border-radius:16px;padding:28px 32px}.q .who{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:700;margin-bottom:14px}.q .who span{width:36px;height:36px;border-radius:50%;background:var(--careBlue-50);display:flex;align-items:center;justify-content:center}.q p{margin:0;font-size:18px;font-weight:500;line-height:1.65}.q b{color:var(--careBlue-700)}.q .by{margin-top:12px;font-size:16px;color:var(--coolNeutral-600)}</style><div class=\"q\"><div class=\"who\"><span><i data-icon=\"MessageCircle\" data-size=\"20\"></i></span>기획자의 한 마디</div><p>“현장의 소리를 들어보니 <b>검진·건강평가·사후관리 데이터가 수기로 제각각 관리</b>되어, 보건관리자가 단순 정리에 매달리고 있었습니다.”</p><div class=\"by\">- 검진 PI팀 기획자</div></div>","htmlMo":"<style>.q{background:#fff;border-radius:14px;padding:20px 18px}.q .who{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:700;margin-bottom:10px}.q .who span{width:30px;height:30px;border-radius:50%;background:var(--careBlue-50);display:flex;align-items:center;justify-content:center}.q p{margin:0;font-size:15px;font-weight:500;line-height:1.6}.q b{color:var(--careBlue-700)}.q .by{margin-top:10px;font-size:13px;color:var(--coolNeutral-600)}</style><div class=\"q\"><div class=\"who\"><span><i data-icon=\"MessageCircle\" data-size=\"16\"></i></span>기획자의 한 마디</div><p>“현장의 소리를 들어보니 <b>검진·건강평가·사후관리 데이터가 수기로 제각각 관리</b>되어, 보건관리자가 단순 정리에 매달리고 있었습니다.”</p><div class=\"by\">- 검진 PI팀 기획자</div></div>"}}
```

같은 형태의 `html` 블록이 **두세 호 연속** 나오면 "정식 블록으로 만들면 좋겠다"고 운영자에게 알린다(담당자가 편집기 블록으로 승격).
