# GC케어 뉴스레터 자동화

운영자가 디자이너 없이 뉴스레터 이미지를 만들 수 있게 돕는 도구입니다.

## 썸네일 만들기

**바로 열기:** https://gcejshim.github.io/gccare-contents/newsletter/thumbnail/dist/thumbnail-v1.1.html

크롬이나 엣지에서 열면 됩니다. 파일로 받아 두면 인터넷 없이도 동작합니다.

1. 호수·콘텐츠 번호 확인
2. 타이틀 입력 (엔터로 줄바꿈, 3줄 이내, 강조는 `[대괄호]`)
3. 배경 색상 선택 (필요할 때만 [색 찍기])
4. 이미지 넣기 — 끌어다 놓기 · 클릭 · Ctrl+V
5. 자동 점검 확인 → **[완성 이미지 저장 (PNG)]** (1197×693)
6. 나중에 고치려면 **[편집 원본 저장]** (.json) → **[편집 원본 열기]**

### claude.ai 스킬로 더 빠르게

`skills/gc-newsletter-thumbnail.zip`을 claude.ai의 설정 → 기능 → 스킬에 올려 두면, 기획안 PDF를 올리고 "15호 썸네일 작업 내용 만들어줘"라고 하면 됩니다. Claude가 준 내용을 복사해 도구 화면에 Ctrl+V로 붙여넣으면 타이틀·배경·칩이 채워집니다.

## 도구 수정하기 (개발)

```bash
cd newsletter/thumbnail
# index.html 수정 후
python3 build.py        # → dist/thumbnail-vX.html 생성 (build.py의 VERSION 올리기)
```

## 버전

| 버전 | 내용 |
|---|---|
| v1.1 | 이미지 붙여넣기·끌어다 놓기 수정, 공식 CI 상단 바 |
| v1.0 | 자동 점검 한 줄 형식, WCAG 대비 기준 표시 |
| v0.6~0.9 | 영문 로고, 그린 배경, 편집 원본 저장/열기 |
| v0.1~0.5 | 썸네일 템플릿, 배경 프리셋, 레이아웃 3종, 스킬 연동, 색 찍기 |
