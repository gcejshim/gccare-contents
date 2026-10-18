# GC케어 뉴스레터 콘텐츠 이미지 만들기

운영자가 올린 기획안을 **이미지 한 장 = 블록 하나**로 나누고, 편집기에 넣을 JSON을 만든다.

## 작업 방향

- **템플릿은 디자인 참고용**이다. 이미지는 **기획서를 기준으로** Claude가 만든다.
- **타이틀 · 컬러는 기본 디자인 시스템**에서, **레이아웃은 기획서를 최대한 참조**한다.
- 기획서에 스타일이 없으면(텍스트 · 기본 표만 있으면) 디자인 시스템을 지키고 템플릿을 참고해 알아서 디자인한다.
- 결과물은 **편집기에서 상세 수정이 가능한 구조**로 만든다. 템플릿으로 되는 모양은 꼭 템플릿으로(숫자를 바꾸면 막대까지 다시 계산됨), `html`이면 data- 표시를 빠짐없이 단다. 그래서 가능한 한 편집기 템플릿(`type`)과 옵션으로 표현하고, 편집기에 새로 생긴 템플릿 · 옵션을 우선 쓴다. `html`은 템플릿으로 도저히 안 될 때만.
- 기본 타이틀 크기 · 스타일과 폰트 크기 정책(아래 "글자" 표)은 **항상** 지킨다. 템플릿을 쓰면 편집기가 지켜 주고, `html`이면 직접 지킨다.

## 우선순위 (부딪히면 위가 이긴다)

1. **기획안 내용** — 문구 · 수치 · 강조가 정확할 것. 임의로 바꾸지 않는다. 줄바꿈 · 강조만 정한다. 수치가 없으면 지어내지 말고 빈칸으로 두고 알린다.
2. **기획서의 형태 · 시각 요소** — 표면 표, 막대면 막대, 순서 · 묶음 · 강조 위치
3. **템플릿 · 디자인 시스템 스타일** — 제목 스타일, 폰트 크기 정책, 색 토큰

## 진행 방식

1. 기획안에서 **호수**와 콘텐츠(01 메인, 02 · 03 서브), 콘텐츠별 **이미지 순서**를 찾아 목록으로 먼저 보여 준다. 기획안에 "이미지 1/2/3"이 표시돼 있으면 그대로 따른다. 참고: 15호 = 2026년 10월.
2. **템플릿으로 못 넣는 요소**(기획서에 있는데 편집기 템플릿 · 옵션에 없는 모양)가 있으면 **만들기 전에 먼저 알리고** 어떻게 할지 확인받는다. (예: "말풍선 강조는 템플릿에 없어요. ① 빼고 굵게 강조 ② html로 만들기 중 어떻게 할까요?")
3. **이미지 한 장씩** 진행한다.
   - **미리보기**: 그 이미지가 어떻게 보일지 보여 준다(가능하면 HTML 미리보기, 아니면 구성 설명). 어떤 템플릿을 왜 골랐는지 한 줄. 어울리는 템플릿이 둘 이상이면 **추천안 + 다른 안 1개**를 한 줄씩 비교해 주고 "다른 안으로 볼까요?"라고 묻는다(사용자는 어떤 게 좋은지 모를 수 있으니 추천안은 반드시 정해 준다).
   - 사용자가 **OK**하면 그 이미지의 **소스(JSON)**를 준다. 고쳐 달라고 하면 고쳐서 다시 미리보기.
   - 결과마다 한 줄 표기: **"스킬 기준대로"** 또는 **"벗어난 부분: …"**(기획서를 따르느라 템플릿 · 정책에서 벗어난 점).
   - 사용자가 "한꺼번에 줘"라고 하면 남은 이미지를 `nl-blocks` 하나로 묶어 준다.
4. 소스는 **파일이 아니라 채팅에 코드 블록**으로 준다. 한 장이면 `nl-block`, 여러 장이면 `nl-blocks`.
5. 넣는 방법 안내 (소스와 함께 매번 짧게):
   "편집기 ② 만드는 방법에서 **[Claude 스킬로 만들기]**를 고르고, 칸에 붙여 넣은 뒤 [넣기]를 눌러 주세요. 넣기 전에 들어올 이미지 목록이 보이고, 이미 있는 번호는 '바뀜'으로 표시돼요. 화면 캡처 · 사진은 블록에서 직접 넣어 주세요."

## 블록 고르기 (위에서부터 맞는 것)

| 기획안 내용 | 블록 `type` |
|---|---|
| 확인 항목 · 체크리스트 · 수칙 (아이콘 + 한 줄) | `list` |
| 설문 결과 (응답 + %) | `rank` |
| 항목별 비율 · 건수 비교 (가로 막대) | `hbar` |
| 기준표 · 방식 비교 · 과태료 등 칸으로 된 내용 | `table` |
| 전후 비교 · 그룹 비교 (세로 막대) | `vbar` |
| 구성비 (정상/전단계/유병 등 100%) | `stack` |
| 구성비 막대 + 오른쪽 평균 · 점수 칸 (예: 5점 평균 3.48) | `stack` + `side` · `sideRows` (html로 만들지 않기) |
| 연도 · 월별 추이 | `line` |
| 업종별 · 유형별 구성비 (원형) | `donut` |
| 두 사업장 · 두 방식 비교 카드 | `compare` |
| 서비스 · 관리자 화면 소개 (헤드라인 + 캡처 1장) | `hero` |
| 앱 화면 2~4개를 단계로 소개 | `steps` |
| 설명 + 진행 단계 박스(→) (상담 · 운영 흐름) | `flow` |
| 핵심 수치 한두 개 강조 (33% · 42% + 설명) | `bigstat` |
| 프로그램 · 서비스 소개 카드 2개 (배지 + 제목 + 설명 + 이미지) | `cards2` |
| 과태료 · 요금처럼 "항목 | 값" 카드 2개 | `kv` |
| 참여자 · 고객 후기 말풍선 (+ 담당자 인용 상자) | `quote` |
| 기획자 · 담당자 한마디 (프로필 + 긴 인용) | `voice` |
| 신청 · 안내 배너 (로고 + 헤드라인 + 화면) | `cta` |
| 판정 코드표 (A · C1 · D1 같은 색 배지) | `table` + `"badge":true` |
| 서로 다른 그래프 2개를 한 장에 비교 (꺾은선 + 파이 등) | `pair` (왼쪽 · 오른쪽 그래프를 안에 직접 담기) |
| **위 어디에도 안 맞음** (특수 인포그래픽, 캘린더, 차트 2개 나란히 등) | `html` |

`raw`(이미지 그대로)는 디자이너가 따로 만든 이미지를 넣는 블록이라 이 스킬에서는 만들지 않는다.

## JSON 형식

```json
{"kind":"nl-blocks","items":[
  {"kind":"nl-block","type":"table","contents":"01","no":1,"bg":"white","data":{ … }}
]}
```

- `contents`: "01" · "02" · "03", `no`: 그 콘텐츠 안의 이미지 번호(1부터)
- 글자 색: 글자 안에 `{블루:글자}` · `{그린:글자}` · `{빨강:글자}` (기획안에 강조 표시가 있을 때만, 이미지 한 장에 3곳 · 2색 이하). 강조 그린은 지금처럼 `[대괄호]`
- 세로축 (`vbar` · `line`): `yMax`(최대값) · `yStep`(눈금 간격) · `yLines`(기준선 개수 `"3"`~`"8"`, 맨 아래 선 포함). 기획안에 축 범위 · 눈금이 정해져 있을 때만 넣고, 없으면 비움(자동)
- 가로축 (`hbar`): `xMin`(시작값) · `xMax`(최대값) · `xStep`(눈금 간격) · `xLines`(세로 기준선 개수 `"3"`~`"8"`). 기획안에 정해져 있을 때만
- 그래프 색 `cols` (`rank`·`hbar`·`vbar`·`stack`·`line`·`donut`): 계열(도넛은 항목, 가로 막대는 [막대, 1위 막대]) 순서의 DS 토큰 배열, 예: `"cols":[null,null,"--careRed-400"]`. 기획안에 위험 · 주의 구간 표시가 있을 때만 쓰고, 나머지는 넣지 않음(자동). 쓸 수 있는 토큰: careBlue 900·700·500·400·300·200·100·50, careGreen 700·600·500·300·100·50, coolNeutral 600·400·300·200·100, careRed 600·500·400·300·200·100, careOrange 600·500·400·300·200·100, careYellow 500·300·200·100
- `bg`: `gray`(회색 바탕, 기본) · `white`(흰 바탕) · `none`(여백 없음). `hero` · `steps`는 쓰지 않음
- `logo`: `top`(상단 · 제목 줄 오른쪽) · `bottom`(하단 오른쪽). 기본은 넣지 않음(로고 없음). 기획서 · 참고 이미지에 GC Care 로고가 있으면 그 위치대로 넣는다(원본 로고 그림은 옮기지 않고 이 설정으로). `hero` · `cta` · `steps` · `raw`는 쓰지 않음. `html`에 `top`을 쓰면 로고는 블록 맨 위 오른쪽 한 줄에 들어가므로(PC · 모바일 모두) 제목 줄을 따로 비울 필요 없다
- `logoStyle`: 로고를 넣을 때 `color`(컬러 · 기본, CI 심볼 + 남색 글자) · `mono`(원톤 남색). 원본 로고가 컬러면 넣지 않음(기본 컬러), 단색이면 `"logoStyle":"mono"`
- `data`는 아래 블록별 형식. 빠진 칸은 편집기 예시 값으로 채워지므로 **필요한 칸만** 써도 된다.
- 강조할 단어는 `[대괄호]`, 한 줄 입력칸 안 줄바꿈은 `//`

### 블록별 `data`

- `list`: `{"title":"지금 다시 확인할 변동 사항","headIcon":"SquareCheckBig","items":[{"icon":"Users","text":"…"}]}` (항목 3~7개)
- `rank`: `{"title":"질문","tag":"복수 응답","items":[{"text":"응답","value":75}]}` (값 큰 순서로 자동 정렬, 같은 값은 공동 순위). 헤더 색 `hc`: `navy`(기본) · `blue` · `light` · `green` — 기획안에 색 지정이 없으면 넣지 않음
- `hbar`: `{"title":"…","sub":"(*설명)","unit":"%","top":true,"items":[{"label":"항목","value":25.4}]}`
- `table`: `{"title":"…","head":"구분 | 직접 운영 | 위탁 운영","rows":"대상자 관리 | 내용//둘째 줄 | 내용\n…","firstCol":true,"icons":"Users\nCalendarDays","hl":"last"}` — 칸은 `|`, 행은 `\n`, 빨간 경고 글씨는 `!!글자!!`, `hl:"last"`면 마지막 열 강조. 행 간격 `rowH`: `m`(보통, 기본) · `s`(좁게 — 한 줄짜리 내용이 많을 때) · `l`(넓게 — 칸 안 두 줄이 많을 때). **내용을 보고 고른다**: 칸 안 줄바꿈(`//`)이 있는 행이 절반 이상이면 `l`, 7행 이상이고 모든 칸이 20자 안팎 한 줄이면 `s`, 그 밖엔 `m`(넣지 않으면 도구가 같은 기준으로 자동). **표 모양**: 열이 **3개 이상**(비교표)이면 강조형(`hc:"navy"` · `firstCol:true`, 행마다 맞는 `icons`), **2개**(구분 | 내용)면 기본형(`hc:"light"` · `firstCol:false` · 아이콘 없음). 기획안에 다른 강조가 분명히 있을 때만 바꾸고, 보통은 `hc` · `firstCol`을 넣지 않는다(도구가 열 개수로 자동). **본문 정렬** `align`: `auto`(기본 · 넣지 않음 — 긴 글이 많은 열은 왼쪽, 짧은 값 열은 가운데) · `center` · `left`. 보통은 넣지 않는다. 머리글 색 `hc`: `navy`(기본) · `blue` · `light` · `green` (색 지정 없으면 넣지 않음). 아이콘 스타일 `iconStyle`: `line`(기본) · `emoji` (`list`도 같음)
- `vbar`: `{"title":"…","sub":"(N=83)","unit":"","series":"참여 전 | 참여 후","rows":"수축기 혈압 | 143 | 125","accent":"last","delta":"pct","good":"down","ref":"120 | 정상 기준"}` — 계열 1~5개. `accent`: `none`·`last`(마지막 계열 그린)·`row`(`acRow` 번째 항목만, 나머지 회색)·`bar`(`acRow`·`acSer` 막대 하나). `delta`: `none`·`pct`(변화율)·`diff`(차이), 첫 계열→마지막 계열, `good`: `down`·`up`·`none`. `ref`: 기준선 "값 | 이름". `palette`: `blue`·`mute`(회색+강조), `labels`: `all`·`accent`·`none`, `dec`: `auto`·`0`·`1`·`2`
- `stack`: `{"title":"…","series":"정상 | 전단계 | 유병","rows":"참여 전 | 6 | 0 | 90","show":"value","unit":"명","accent":2}` — 오른쪽 보조 값 칸: `"side":"5점 평균(점)","sideRows":"3.48
3.40"` (막대 순서대로, 비우면 없음)
- `line`: `{"title":"…","sub":"('21~'25년)","unit":"명","series":"계열명","rows":"2021년 | 25\n2022년 | 29","labels":true}` (기본 그린, 파랑이면 `"green":false`)
- `donut`: `{"title":"…","unit":"%","center":"건설업\n46.5%","accent":true,"items":[{"label":"건설업","value":46.5}]}` (6개 넘으면 "기타"로 묶기)
- `compare`: `{"aName":"A 사업장","aMetrics":"수검률 | 40%\n예약률 | 75%","aStatus":"…","aStatusIcon":"CalendarCheck","aCheck":"…","aCheckIcon":"Target","bName":"B 사업장", … ,"statusTitle":"현재 상태","checkTitle":"확인할 사항"}`
- `flow`: `{"head":"GC케어 유소견자 의료진 상담","title":"검진결과 C, D등급 임직원에게 간호사가 직접 1:1 상담 진행","desc":"설명 (**굵게**)","steps":"임직원 검진결과 등록\n대상자 자동 분류\n맞춤 콘텐츠 발송"}` (단계 4개 이하 권장, 머리 이미지 `avatar`는 운영자가 넣음)
- `bigstat`: `{"items":[{"value":"33","unit":"%","text":"설명 [(96명 중 32명)]"}]}` (카드 3개 이하)
- `cards2`: `{"items":[{"badge":"걷기 캠페인","title":"제목","text":"설명","image":""}]}` (이미지는 운영자가 넣음)
- `kv`: `{"items":[{"title":"사업주 과태료 (일반건강진단 기준)","rows":"1차 위반 (1인당) | 10만 원\n2차 위반 (1인당) | 20만 원"}]}`
- `quote`: `{"badge":"참여자 인터뷰","title":"설문 응답자 중 [64%] **건강습관 형성에 도움이 된다**고 응답","items":[{"image":"","text":"후기","who":"제조업 임직원 A"}],"note":"담당자 인용 (선택)","noteBy":"- 금융업 A사 담당자 인터뷰"}`
- 강조색 `tone` (`flow` · `bigstat` · `cards2` · `kv` · `quote` · `voice` · `cta` · `hero`): `green`(기본) · `blue` — 블록 안의 그린을 블루로 한꺼번에 바꿈
- 배지 배경색 `badgeBg` (`quote` · `cards2`): `--careGreen-600`(기본) · `--careGreen-700` · `--careGreen-50` · `--careBlue-500` · `--careBlue-900` · `--careBlue-100` · `--careOrange-600` · `--coolNeutral-600`. 기획안에 색 지정이 없으면 넣지 않음
- `voice`: `{"head":"기획자의 한 마디","body":"“인용 **굵게**”","by":"- 검진 PI팀 OOO 기획자"}`
- `cta`: `{"logo":"en","title":"기업 보건관리의 모든 업무,\n[보건이지] 하나로 EASY하게!","sub":"지금 사전 신청하면,\n출시 후 6개월 **무료 이용 혜택**"}` (화면 이미지는 운영자가 넣음)
- 표 배지: `"firstCol":true,"badge":true,"badges":"그린\n연그린\n노랑\n빨강"` (행마다 그린 · 연그린 · 노랑 · 빨강 · 파랑 · 회색)
- 가로 막대 축 시작값 `xMin` (예: 배수면 `1`), 꺾은선 기준선 `ref` (`"140 | 정상"`)
- 굵게: 글자 안 `**굵게**` (모든 블록). 원본 글에서 굵게 강조된 문구는 그대로 굵게 (편집기 미리보기의 [굵게] 버튼으로 운영자가 켜고 끌 수 있음)
- `pair`: `{"left":{"type":"line","data":{…}},"right":{"type":"donut","data":{…}}}` — 왼쪽 · 오른쪽 그래프를 **안에 직접** 담는다. `type`은 `line` · `donut` · `vbar` · `hbar` · `stack`만, `data`는 그 블록 형식 그대로. 그래프를 따로 블록으로 만들지 않는다(따로 만들면 별도 이미지로 저장됨). 편집기에서는 [왼쪽 그래프] · [오른쪽 그래프] 탭에서 고친다.
- 꺾은선 간단 스타일 `"simple":true`(세로축 · 눈금 숨김), 도넛 파이 `"pie":true`(조각 안 이름 · 값)
- `hero`: `{"title":"우리 회사에 맞게 설정하고, [반복 업무는 줄이고]","frame":true,"winTitle":"어떠케어 - 내부 관리자"}` (캡처는 운영자가 넣음). 배경 `bgStyle`: `flat`(연파랑, 기본) · `grad` · `white` · `gray` · `navy`(글씨 · 로고 흰색)
- `steps`: `{"title":"","items":[{"title":"걸음 수 추이 확인"},{"title":"나만의 캐릭터와 닉네임"}]}` (캡처는 운영자가 넣음)
- `html`: 아래 "직접 만든 블록" 참고 → `{"note":"인터뷰 말풍선 3개","html":"…","htmlMo":"…"}` (고칠 곳은 data- 표시)

아이콘 이름(Lucide): `SquareCheckBig` `CircleCheck` `ListChecks` `ClipboardCheck` `ClipboardList` `Users` `UserCheck` `UserPlus` `UserX` `ContactRound` `IdCard` `Building2` `Hospital` `FileCheck` `FileText` `ShieldPlus` `ShieldCheck` `CalendarCheck` `CalendarDays` `Clock` `Search` `Target` `TrendingUp` `ChartColumn` `HeartPulse` `Heart` `Stethoscope` `Activity` `Pill` `Brain` `Footprints` `Thermometer` `Bell` `Megaphone` `Mail` `Smartphone` `Monitor` `MessageCircle` `Lightbulb` `Award` `Settings` `RefreshCw` `Info` `CircleAlert` `TriangleAlert` (표 첫 칸 · HTML 블록은 다른 Lucide 이름도 가능, 예: `ArrowLeftRight`)

## 직접 만든 블록 (`html`) 규칙

맞는 블록이 없을 때만 쓴다. 편집기가 이 코드를 PC(폭 900) · 모바일(폭 350)에 그려 2·3배 PNG로 저장한다.

**디자인**
- **가장 가까운 템플릿의 스타일을 그대로** 따른다: 제목(블록 제목 22 Bold, 남색 헤더 등), 카드(흰 바탕 · 둥근 모서리 16 · 그림자), 표 선, 그래프 막대 모양 · 축 · 숫자 위치, 아이콘 원.
- 템플릿에 **없는 스타일은 Claude가 디자인 시스템 안에서 임의로** 만든다(말풍선, 이름 띠, 보조 값 칸 등). 색은 토큰만, 글자 크기는 아래 표 안에서.
- 기획서에 참고 이미지가 있으면 배치 · 순서 · 강조 위치를 따르되, 색 · 글꼴은 디자인 시스템으로 바꾼다.

**운영자가 고칠 수 있게 (꼭 지키기)** — 바뀔 만한 글자 · 숫자 · 막대 · 색에 `data-` 표시를 단다. 편집기가 읽어서 미리보기에서 바로 고치게 해 준다(코드 안 열어도 됨). PC(`html`)와 모바일(`htmlMo`)에 **같은 `data-key`**를 쓰면 한쪽을 고칠 때 둘 다 바뀐다.
| 속성 | 붙는 곳 | 하는 일 |
|---|---|---|
| `data-key="m-20-now"` | 고칠 수 있는 모든 요소 | PC · 모바일 연결 이름 (영문 · 숫자 · `-`만) |
| `data-edit="text"` | 글자 (제목 · 말풍선 · 라벨 · 띠 · 범례) | 클릭해서 글자 수정 |
| `data-edit="value"` | 숫자 라벨 | 숫자 수정 → 같은 key 막대 높이도 다시 계산 |
| `data-bar="32.1"` + `data-max="80"` | 막대 | 높이 = 값 ÷ 최대값 (CSS로 높이를 직접 쓰지 않기) |
| `data-axis="axis"` | 막대 · 눈금 | 아래 축 최대값을 씀 (`data-max`보다 우선) |
| `data-max-key="axis"` | 세로축 맨 위 숫자 글자 | 이 숫자를 고치면 그 축의 막대 · 눈금이 다시 계산 |
| `data-tick="0.5"` | 눈금 글자 | 글자 = 축 최대값 × 비율 |
| `data-follow="m-20-now"` + `data-gap="30"` | 말풍선 등 (`position:absolute`) | 막대 높이를 따라 위치 이동 |
| `data-label="남자 20대"` | 고칠 수 있는 모든 요소 | ③ 상세 편집 입력칸 이름 (꼭 달기, 운영자가 보는 이름) |
| `data-color="--careBlue-700"` | 막대 · 띠 · 배지 · 값 칸 | 배경색. 미리보기에서 눌러 색 바꾸기 (토큰만) |
- 운영자는 코드를 보지 않는다. ③ 상세 편집에 data- 표시로 만든 입력칸만 보이므로, 바뀔 수 있는 건 빠짐없이 표시한다.
- 그래프는 막대마다 `data-key` + `data-bar` + `data-axis` + `data-color`, 숫자 라벨은 같은 key로 `data-edit="value"`.
- 글자 색은 `<span class="tc-red">`(tc-blue · tc-green · tc-red · tc-orange · tc-gray), 굵게는 `<b>`.
- 그래프 예시는 맨 아래 "예시" 참고.

**구조**
- `html`(PC)과 `htmlMo`(모바일)를 **따로** 만든다. 모바일은 위아래로 쌓고 글자를 줄인다. **PC에서 옆으로 나란히 둔 것(그래프 2개 · 카드 2개)은 모바일에서 반드시 위아래로** 쌓고 각각 폭 100%로 한다(350폭에 나란히 두면 숫자 · 글자가 겹침).
- **제목 옆 부제목**(회색 작은 글씨 등)은 PC에서는 제목 옆, **모바일에서는 제목 아래 줄**(`display:block`)로 내린다. 문장 중간에서 끊기지 않게. 부제목 글자에 `-` · `·` 같은 앞 기호를 넣지 않는다(PC에서 띄우는 건 `margin-left`로).
- 맨 앞에 `<style>` 하나, 그 뒤에 내용. `<style>`의 선택자는 편집기가 이 블록 안으로 자동 한정하니 짧은 클래스 이름(`.q`, `.row`)을 써도 된다.
- 바깥 폭은 지정하지 않는다(블록 폭에 맞춰짐). `width:100%`, flex · grid로 배치한다. 고정 px 폭은 칸 하나 정도만.
- 바탕은 블록 설정(`bg`)이 깔아 주므로, 카드가 필요하면 **`class="box"`**를 쓴다(편집기가 흰 바탕 · 모서리 PC 16 · 모바일 14 · 그림자를 맞춤, 안 여백만 `padding:28px 32px`처럼 준다). 카드 안의 작은 칸에도 모서리를 꼭 준다(design-system.md '모양').

**글자 · 색 · 모양은 `references/design-system.md`를 따른다.** HTML에서 지킬 것만:
- `font-family`는 쓰지 않는다(Pretendard는 편집기가 넣어 줌). 기본 글자색은 지정하지 않으면 `#111111`.
- 색은 `var(--이름)`(예: `var(--careBlue-900)`)으로만 쓴다. 토큰 밖 hex는 흰색 `#fff`와 그림자 `rgba(3,21,82,.06)`만.
- 줄 간격 1.5~1.65, `word-break:keep-all`은 편집기가 이미 적용.

**아이콘**: `<i data-icon="Users" data-color="--careBlue-500" data-size="22"></i>` → 편집기가 Lucide 아이콘으로 바꿔 줌. 원 안 아이콘이면 바깥 `span`에 배경·크기를 준다.

**쓰지 않는 것 (저장 PNG에서 깨지거나 막힘)**
- `<script>`, `on…=` 속성, `<iframe>`, 외부 링크 · 외부 이미지(`http…`) — 이미지가 필요하면 그 자리를 비우고 "이 이미지는 목업 히어로/이미지 그대로 블록으로 넣어 주세요"라고 안내
- `conic-gradient`, `backdrop-filter`, `filter`, `mix-blend-mode`, `clip-path`, `position:fixed`, `vw/vh` 단위, 웹폰트·`font-family`
- 원형 차트가 필요하면 `donut` 블록을 쓰고, HTML로 그리지 않는다.
- 이미지 안 글자 금지 원칙은 그대로: 글자는 모두 HTML 텍스트로.

## 예시 (10호 "기획자의 한 마디" → 맞는 블록이 없어 html · 글자마다 data- 표시)

```json
{"kind": "nl-block", "type": "html", "contents": "02", "no": 2, "bg": "gray", "data": {"note": "기획자 한마디 인용", "html": "<style>.q{background:#fff;border-radius:16px;padding:28px 32px}.q .who{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:700;margin-bottom:14px}.q .who span{width:36px;height:36px;border-radius:50%;background:var(--careBlue-50);display:flex;align-items:center;justify-content:center}.q p{margin:0;font-size:18px;font-weight:500;line-height:1.65}.q b{color:var(--careBlue-700)}.q .by{margin-top:12px;font-size:16px;color:var(--coolNeutral-600)}</style><div class=\"q\"><div class=\"who\"><span><i data-icon=\"MessageCircle\" data-size=\"20\"></i></span><span data-key=\"head\" data-edit=\"text\">기획자의 한 마디</span></div><p data-key=\"quote\" data-edit=\"text\">“현장의 소리를 들어보니 <b>검진·건강평가·사후관리 데이터가 수기로 제각각 관리</b>되어, 보건관리자가 단순 정리에 매달리고 있었습니다.”</p><div class=\"by\" data-key=\"by\" data-edit=\"text\">- 검진 PI팀 기획자</div></div>", "htmlMo": "<style>.q{background:#fff;border-radius:14px;padding:20px 18px}.q .who{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:700;margin-bottom:10px}.q .who span{width:30px;height:30px;border-radius:50%;background:var(--careBlue-50);display:flex;align-items:center;justify-content:center}.q p{margin:0;font-size:15px;font-weight:500;line-height:1.6}.q b{color:var(--careBlue-700)}.q .by{margin-top:10px;font-size:13px;color:var(--coolNeutral-600)}</style><div class=\"q\"><div class=\"who\"><span><i data-icon=\"MessageCircle\" data-size=\"16\"></i></span><span data-key=\"head\" data-edit=\"text\">기획자의 한 마디</span></div><p data-key=\"quote\" data-edit=\"text\">“현장의 소리를 들어보니 <b>검진·건강평가·사후관리 데이터가 수기로 제각각 관리</b>되어, 보건관리자가 단순 정리에 매달리고 있었습니다.”</p><div class=\"by\" data-key=\"by\" data-edit=\"text\">- 검진 PI팀 기획자</div></div>"}}
```

그래프 예시 (막대 · 말풍선 · 축 — 32.1을 고치면 막대와 말풍선이, 맨 위 80을 고치면 모든 막대와 눈금이 다시 계산됨):

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

같은 형태의 `html` 블록이 **두세 호 연속** 나오면 "정식 블록으로 만들면 좋겠다"고 운영자에게 알린다(담당자가 편집기 블록으로 승격).
