# GC케어 뉴스레터 자동화

디자이너 대신 **운영자가 직접** 뉴스레터 이미지를 만들 수 있게 하는 도구 모음. 카드뉴스 편집기(`../cards/cardnews_editor_v1.0.html`) 구조를 응용한 단일 HTML 도구 + claude.ai 스킬.

> **현재 단계 (2026-10-01): 프로토타입 → 팀장 보고 → 상세 구축.** 통합본 `app/dist/newsletter-maker.html`이 최신 (**파일 이름 고정**, 버전은 왼쪽 아래 표시 · README 버전 표). 다음 할 일은 맨 아래 "진행 순서" 참고.

## 산출물 규격 (확정)

| 산출물 | 작업 크기 | 내보내기 | 비고 |
|---|---|---|---|
| PC 이미지 | 폭 900 | 2배 (1800px) | 메일 발송 시 약 660px로 축소(×0.73) → 본문 최소 18, 가장 작은 글자 14, 선 1.5px 이상 |
| 모바일 이미지 | 폭 350 | 3배 (1050px) | 타이틀 16·18 / 본문 14·16 |
| 썸네일 | 399×231 | 3배 (1197×693) | 파일명 `(N호)NN.제목.png` |
| PDF | A4 세로 900×1273 | 벡터 | 게시판 업로드·화면 열람용. 인쇄 대응은 후순위 |

- PC 타이포: 타이틀 22 / 본문 18·16 (본문 18은 DS 텍스트 스타일에 없어 글로벌 토큰 18/26 조합)
- 이미지 내보내기는 브라우저 html2canvas(카드뉴스 편집기와 동일), PDF는 브라우저 인쇄→PDF(실제 텍스트 유지)
- 파일 1MB 제한 대응 시 이미지 크기 축소 금지(2·3배 의미가 사라짐) → 색상 수 감소 압축 사용

## 호수 관리

- 한 호 = 콘텐츠 2~3개, 콘텐츠당 이미지 2~3장 (PC·모바일 각각)
- 10호=202605 … 14호=202609, **15호=202610 (2026-10-14 게시 마감)**
- 기존 폴더/파일 규칙 유지: `YYYYMM_contentsNN_pNN.png`(PC), `_mNN.png`(모바일)
- 입력: IPR팀 기획안(pptx/pdf/docx). 차트 수치도 기획안 안에 있음

## 디자인 원칙 (사용자 지정 — 바꾸지 말 것)

- **뉴스레터는 앱 위주가 아님.** B2B(HR·보건 담당자) 정보 콘텐츠 = 편집 디자인·인포그래픽 관점. 앱 UI 패턴/Mobbin 레퍼런스 X. DS는 토큰(컬러·타이포)만 사용
- **컬러:** 블루톤 기반 + 녹색(careGreen)은 포인트만. 기본은 DS 토큰, **단 Figma 13·14호 원본 재현이 DS 매핑보다 우선** (사용자 지정, 2026-10-01)
  - 13·14호 → DS 매핑(확정): 헤더 남색·진남색 careBlue/900, 강조 careBlue/700, 배지 careBlue/500, 연파랑 careBlue/100, 바탕 coolNeutral/50, 구분선 coolNeutral/100, 그린 careGreen/500·700·10 (일반 `blue/*` 대신 careBlue 우선) — `docs/컬러매핑_13-14호.html`
  - 예외 1: 썸네일 타이틀 색 `#002540` (**썸네일 전용**. 콘텐츠 이미지는 아님)
  - 예외 2: 그린 배경 `#20B977` (타이틀 흰색, 로고 남색, 강조 단어 `#002540`, 대비 안내 생략)
  - 예외 3: 표·순위 막대는 13호 Figma 원본 색 그대로 (`--nl-*` 변수, editor/index.html 맨 위)
- **콘텐츠 이미지 글자:** 모든 기본 텍스트(제목·헤드라인·항목명·일반 값) **`#111111`(neutral/900)**. coolNeutral/900(#1b1b1b) 쓰지 않기. 색은 강조값(표 강조 열, 순위 %, 비교 수치, 그린 강조)에만
  - 13호 본문 = Pretendard Medium 18 / 줄 22.5 / 자간 -0.2px, 헤드라인 Bold 28, 블록 제목 Bold 22
  - **어두운 바탕 위 흰 제목(카드 헤더, 표 머리글)은 굵기 600** — Figma는 700이지만 저장 PNG(html2canvas는 font-smoothing 미적용)가 두꺼워 보여 사용자가 600으로 결정
  - **차트는 이미지 금지, 전부 HTML** (꺾은선 = 회전한 div, 도넛 = 1도 조각 div 360개). 꺾은선 기본색 careGreen/500
- **아이콘:** Lucide 라인이 기본, 채움은 강조 시에만(Lucide는 라인 전용 → 닫힌 도형 fill 또는 Tabler filled 보완)
- **로고:** 썸네일은 14호 단색 영문 로고 78×19. 콘텐츠 이미지(히어로·단계별 화면)는 **한글 GC케어** 남색. 도구 상단 바는 공식 CI **한글** 컬러 심볼 + 흰 글자(`thumbnail/assets/logo_ci_color_whitetext_ko.png`)
  - 공식 CI 원본: `~/Documents/gccare/GCCI/GC CI Download_2022/1. GC CI (png)/Color/GC케어_kor.png` · `_eng.png` (회사 PC)
- **AI 이미지에는 글자를 넣지 않는다.** 글자는 항상 HTML로. 인물 사진은 회사 보유 사진만
- **영업 PDF:** 토스 콘텐츠(앱 화면 X) 벤치마킹 — 한 페이지 한 메시지, 큰 숫자·도식, 본문 최소화. 9월 운영자 제작 PDF는 불만족 → 내용만 참고
- 요청하지 않은 산출물을 늘리지 않는다(예: 게시판 썸네일/요약문은 제외됨)

## 폴더

```
newsletter/
├─ thumbnail/          썸네일 도구
│  ├─ index.html       개발본 (여기서 수정)
│  ├─ build.py         python3 build.py → dist/thumbnail.html (이름 고정, 단일 파일, 오프라인 동작.)
│  ├─ assets.js        로고·예시 이미지(base64). assets/ 원본에서 생성
│  └─ vendor/          html2canvas 1.4.1, lucide 0.460.0, Pretendard woff2
│     └─ vendor/Pretendard-Medium.woff2  (npm pretendard@1.3.9 경로. gh 경로는 404) — 빌드 3종 모두 500 = Medium
├─ editor/             콘텐츠 이미지(PC 900→2배 · 모바일 350→3배) 블록 편집기
│  ├─ index.html       개발본. 블록 정의는 BLOCKS (list·rank·hbar·table·hero·steps·vbar·stack·line·donut·html·raw·compare)
│  ├─ assets-editor.js 한글 로고(logoKoBlue/White) · 상단 바 한글 CI(logoTopKo)
│  └─ build.py         → dist/image-editor.html (이름 고정 · thumbnail/vendor · assets.js 공유)
├─ app/                통합본 "뉴스레터 만들기" (메뉴 셸: 이번 호 · 썸네일 · 콘텐츠 이미지 · PDF 준비 중 · 에셋 · 가이드)
│  ├─ index.html       개발본. 두 도구를 iframe으로 띄우고 postMessage로 호수 공유 · 저장 기록 · 호 전체 저장/열기
│  ├─ make_samples.py  10~14호 완성 이미지 → samples.js (에셋 › 샘플 모아보기). 회사 PC의 월별 폴더가 있어야 다시 만들 수 있음
│  └─ build.py         → dist/newsletter-maker.html (이름 고정 · 폰트·라이브러리는 한 번만 넣고 blob URL로 두 도구가 공유, 약 5.8MB)
├─ skills/gc-newsletter-thumbnail/   claude.ai 스킬 (기획안 → 썸네일 JSON). 수정 후 zip 다시 만들기
├─ skills/gc-newsletter-block/       claude.ai 스킬 (기획안 → 콘텐츠 블록 nl-block JSON, 블록에 없으면 html 블록). 편집기에 Ctrl+V
├─ docs/               GPT 지침(ChatGPT 배경 이미지), 컬러 매핑, 13·14호 원본 대비 비교 이미지
├─ issues/14/          14호 참고자료(기획안·PDF 4종)와 결과물
├─ docs/chart-guide.md 기존 차트(Chart.js TYPE A/B/C) 제작 가이드 — 캡처 규격 1012/350은 옛 값, 실제는 PC 920·모바일 390 스크립트
└─ scripts/screenshot_ipr.py  기존 Playwright 캡처 스크립트
```

## 썸네일 도구 구조 메모

- 상태 `S` = `{v:1, issue, no, title, titleSize(26|22), preset, customBg, layout(scene|object|photo), image, img{scale,x,y}, chipsOn, chips[3]}` → 이 형식이 스킬 JSON과 동일
- 프리셋: lightBlue, white, navy, blue, lightGreen, green + `custom`(스포이트)
- 장면형: 이미지가 배경 → 글자색은 이미지 밝기로 자동, 프리셋 클릭 시 사진형으로 전환
- 사진형 페이드는 CSS 그라데이션 대신 canvas 이미지(html2canvas 경계선 버그 회피)
- 자동 점검: 한 줄 형식(제목 → 해결법, 이유는 hover). 대비는 WCAG 2.1 큰 글씨 3:1 기준값을 함께 표시. 이미지 겹침 경고는 사용자 요청으로 제거
- 붙여넣기: 이미지는 커서 위치와 무관하게 받음, JSON 텍스트는 입력칸 밖에서만
- 자동저장 localStorage `gc-nl-thumb-v1` (이미지가 크면 제외)

## 콘텐츠 이미지 편집기 · 통합본 메모

- 상태 `S` = `{v:1, kind:'nl-image', issue, ym, items:[{id, type, contents, no, bg(gray|white|none), fmt(png|jpg), data}], sel, fold}`. 자동저장 `gc-nl-image-v1`, 셸은 `gc-nl-hub-v1`
- 저장: html2canvas, 흰 배경(투명 영역 없음). 형식 PNG 기본 · JPG(품질 90)는 사진 많을 때. PNG 1MB 초과 시 [JPG로 저장] 버튼
- 미리보기: PC·모바일 둘 다 기본 표시, PC는 칸에 맞춰 자동 축소, PC 제목줄의 "메일 크기로 보기"(660px) 옵션, 화면별 ▾ 접기 (사용자 지정: 설명 문구는 최소로)
- 블록에 없는 형태 대응(사용자 승인): ① 가까운 블록 옵션 → ② `html` 블록(스킬이 만든 HTML, `<style>` 자동 범위 한정 · script 제거 · `data-icon`→Lucide · 토큰 외 색 점검) → ③ 두세 번 반복되면 정식 블록으로 승격 → ④ `raw`(외부 제작 이미지 그대로, PC 1800 / 모바일 1050 권장)
- 붙여넣기: `{kind:'nl-block'|'nl-blocks'}` JSON → 블록 추가, 이미지 → 현재 블록의 빈 이미지 칸(목록 안 이미지 칸 포함)
- 검증 사례: 14호 서브 콘텐츠 2장(단계별 화면 + 목업 히어로) 재현 → `docs/데모_14호_서브콘텐츠_원본비교.jpg`
- AI 이미지: 지금은 에셋 › AI로 그리기(ChatGPT 프롬프트 생성, `docs/ChatGPT_뉴스레터이미지_GPT지침.md`). 계획: 별도 메뉴 "AI 이미지"로 분리 + 도구 이미지 칸 옆 [AI로 그리기] 버튼(용도·주제 자동 채움) → 공용 키 프록시(카드뉴스와 **함수 분리** `api/newsletter-image.js`, 뉴스레터 전용 OpenAI 프로젝트 키, 개인 키 미허용) → 에셋에 생성 이미지 보관. 사용 기록은 카드뉴스 UsageLog 시트에 `도구`·`호·카드` 열을 더해 합계 통계. 비용 기준 장당 약 ₩35
- 남은 디테일: 순위 막대 "형태가 이상함"(행 높이·배지 정렬, 13호 `2387-2550` 재대조) — 사용자가 나중에 잡기로 함. 다른 블록은 원본 맞춤 보류

## Figma

- 뉴스레터 13·14호: 파일 `i8zSUqXOiTr7xsrPknMPc7` (13호 `2387-1986`, 14호 `2478-1878`, 썸네일 에셋 `2095-1957`)
  - 프레임 이름 = 납품 파일명(`202608_contents01_p01` 등). 15호도 같은 구조(`02.GC뉴스레터_통이미지_PC|MO_15호_Main01|Sub01`)
  - `2478-2651`(Html → Body, 건강검진 Q&A)은 사용자가 만든 **PDF 시도 샘플**(긴 세로형) — 뉴스레터 결과물 아님. PDF는 A4 다페이지로 나눠야 함
- 디자인 시스템 Foundation: `ai8JLld3k0Zg9blRCq2H4C` (Color `1482-6366`, Typography `1482-11943`, Global Token `1482-12335`)
- Component(앱 UI 키트): `bbgOzhogvrC0RW47XdbDsR`

## 진행 순서

> 작업 방식: 이미지 생성·PDF 골격은 **초안을 먼저 넓게 잡고 점점 좁혀 간다.** 처음부터 디테일하게 만들지 않는다 (사용자 지정).


1. ✅ 썸네일 도구 + claude.ai 스킬 (v1.1)
2. ✅ 콘텐츠 이미지 편집기 블록 13종 + 통합본(메뉴 셸) 프로토타입 + 블록 스킬 (편집기 v1.3 · 통합본 v1.1 · 썸네일 v1.2)
   - 배포 규칙: dist 파일 이름은 고정, 고칠 때 build.py의 VERSION만 올리고 README 버전 표에 한 줄 추가
3. ⏭ 팀장 보고 자료: 프로토타입, 14호 재현 비교, 방향 판단(10~14호 콘텐츠 이미지 32장 중 약 78%가 블록으로 가능), AI 이미지 메뉴 계획, 비용
4. 15호(2026-10-14 마감) 기획안으로 실제 제작 — 맞는 블록 없으면 html 블록 → 반복되면 정식 블록
5. AI 이미지 메뉴 분리 · 도구 내 버튼 → 공용 키 프록시
6. PDF 템플릿 (블록 재사용, A4 세로 다페이지)
