# GC케어 뉴스레터 자동화

디자이너 대신 **운영자가 직접** 뉴스레터 이미지를 만들 수 있게 하는 도구 모음. 카드뉴스 편집기(`../cards/cardnews_editor_v1.0.html`) 구조를 응용한 단일 HTML 도구 + claude.ai 스킬.

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
- **컬러:** DS 토큰 사용, 블루톤 기반 + 녹색(careGreen)은 포인트만
  - 예외 1: 타이틀 색 `#002540` (14호 원본 유지)
  - 예외 2: 그린 배경 `#20B977` (타이틀 흰색, 로고 남색, 강조 단어 `#002540`, 대비 안내 생략)
- **아이콘:** Lucide 라인이 기본, 채움은 강조 시에만(Lucide는 라인 전용 → 닫힌 도형 fill 또는 Tabler filled 보완)
- **로고:** 썸네일은 14호 단색 영문 로고 78×19. 도구 상단 바는 공식 CI 컬러 심볼 + 흰 글자
  - 공식 CI 원본: `~/Documents/gccare/GCCI/GC CI Download_2022/1. GC CI (png)/Color/GC케어_eng.png` (회사 PC)
- **AI 이미지에는 글자를 넣지 않는다.** 글자는 항상 HTML로. 인물 사진은 회사 보유 사진만
- **영업 PDF:** 토스 콘텐츠(앱 화면 X) 벤치마킹 — 한 페이지 한 메시지, 큰 숫자·도식, 본문 최소화. 9월 운영자 제작 PDF는 불만족 → 내용만 참고
- 요청하지 않은 산출물을 늘리지 않는다(예: 게시판 썸네일/요약문은 제외됨)

## 폴더

```
newsletter/
├─ thumbnail/          썸네일 도구
│  ├─ index.html       개발본 (여기서 수정)
│  ├─ build.py         python3 build.py → dist/thumbnail-vX.html (단일 파일, 오프라인 동작)
│  ├─ assets.js        로고·예시 이미지(base64). assets/ 원본에서 생성
│  └─ vendor/          html2canvas 1.4.1, lucide 0.460.0, Pretendard woff2
├─ skills/gc-newsletter-thumbnail/   claude.ai 스킬 (기획안 → 도구 입력 JSON). 수정 후 zip 다시 만들기
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

## Figma

- 뉴스레터 13·14호: 파일 `i8zSUqXOiTr7xsrPknMPc7` (13호 `2387-1986`, 14호 `2478-1878`, 썸네일 에셋 `2095-1957`)
- 디자인 시스템 Foundation: `ai8JLld3k0Zg9blRCq2H4C` (Color `1482-6366`, Typography `1482-11943`, Global Token `1482-12335`)
- Component(앱 UI 키트): `bbgOzhogvrC0RW47XdbDsR`

## 진행 순서

> 작업 방식: 이미지 생성·PDF 골격은 **초안을 먼저 넓게 잡고 점점 좁혀 간다.** 처음부터 디테일하게 만들지 않는다 (사용자 지정).


1. ✅ 썸네일 도구 + claude.ai 스킬 (v1.1)
2. ⏭ 15호 PC·모바일 이미지 — 실제 기획안으로 필요한 블록만 만들며 블록 라이브러리 구축
3. PDF 템플릿 (2번 블록 재사용, A4 세로)
4. 편집기 통합(16호 이후): 블록 입력·실시간 미리보기·자동저장·에셋 라이브러리·AI 이미지 생성(카드뉴스 편집기 프록시 재사용)
