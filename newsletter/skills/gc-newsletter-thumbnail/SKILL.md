---
name: gc-newsletter-thumbnail
description: GC케어 뉴스레터 기획안(PDF·PPT·문서 또는 붙여넣은 텍스트)을 받아 '뉴스레터 썸네일 만들기' 도구에서 바로 불러올 수 있는 작업 내용(JSON)으로 변환하고, 썸네일 이미지 생성 프롬프트를 제안한다. 사용자가 뉴스레터 썸네일, 호수(예: 15호) 썸네일, 기획안 변환, 썸네일 작업 파일을 요청하면 사용한다.
---

# GC케어 뉴스레터 썸네일 작업 내용 만들기

운영자가 올린 기획안에서 콘텐츠별 썸네일 정보를 뽑아, 썸네일 도구(`뉴스레터_썸네일_vX.html`)에 붙여넣을 JSON을 만든다. 디자인은 도구가 책임지므로, 여기서는 **내용과 선택지**만 정한다.

## 진행 순서

1. 기획안에서 **호수**(예: 15호)와 콘텐츠 목록(01 메인, 02 서브, 03…)을 찾는다. 호수가 없으면 물어본다. 참고: 14호=2026년 9월, 15호=2026년 10월, 이후 한 달에 한 호씩.
2. 콘텐츠마다 아래 규칙으로 JSON을 하나씩 만든다.
3. 콘텐츠마다 **JSON 코드 블록 하나**와 **이미지 프롬프트**를 준다. 파일을 만들 수 있으면 `(15호)01.작업.json`처럼 파일로도 준다.
4. 마지막에 사용 방법 한 줄을 붙인다: "썸네일 도구를 열고 JSON을 복사해 Ctrl+V로 붙여넣은 뒤, 이미지를 넣고 [PNG 저장]을 누르세요."

기획안의 문구를 임의로 바꾸지 않는다. 줄바꿈과 강조만 정하고, 3줄에 도저히 안 들어가면 줄이기 전에 원문과 줄인 안을 함께 보여주고 고르게 한다.

## JSON 형식 (이 형식 그대로)

```json
{
  "v": 1,
  "issue": 15,
  "no": "01",
  "title": "검진결과가\n나왔습니다.\n무엇을 해야 할까요?",
  "titleSize": 26,
  "preset": "lightBlue",
  "layout": "scene",
  "image": null,
  "img": {"scale": 100, "x": 0, "y": 0},
  "chipsOn": true,
  "chips": [
    {"icon": "User", "label": "결과 확인"},
    {"icon": "MessageCircle", "label": "사후관리"},
    {"icon": "TrendingUp", "label": "건강관리 계획"}
  ]
}
```

- `v`: 항상 1
- `issue`: 호수 숫자, `no`: "01" · "02" · "03"
- `image`: 항상 `null` (이미지는 운영자가 도구에서 넣는다)
- `img`: 항상 `{"scale":100,"x":0,"y":0}`

## 타이틀 규칙

- `\n`으로 줄을 나눈다. **3줄 이내**, 한 줄은 **한글 약 9자 이내**(26px 기준. 공백·문장부호 포함 11자까지 허용).
- 의미 단위로 끊는다. 조사·어미 앞에서 끊지 않고, 한 글자만 남는 줄을 만들지 않는다.
- 강조할 단어는 `[대괄호]`로 감싼다. **한 타이틀에 한 곳, 2~6자**만. 숫자·핵심 키워드가 좋다. 강조가 꼭 필요하지 않으면 쓰지 않는다.
- 4줄이 꼭 필요하면 `"titleSize": 22`로 하고 이유를 한 줄로 알려준다. 기본은 26.

## 배경 프리셋 (`preset`)

| 값 | 이름 | 어울리는 주제 |
|---|---|---|
| `lightBlue` | 라이트 블루 (기본) | 대부분의 콘텐츠 |
| `white` | 화이트 | 데이터 리포트, 설문 결과 |
| `navy` | 네이비 | 담당자용, 제도·법령 등 무게감 있는 주제 |
| `blue` | 블루 | 서비스 소개, 공지 |
| `lightGreen` | 라이트 그린 | 챌린지, 생활습관 (녹색이 어울리는 주제) |
| `green` | 그린 (#20B977) | 챌린지·캠페인처럼 밝고 활동적인 주제. 타이틀 흰색, 강조 단어는 남색 |

뉴스레터는 블루톤이 기본이고 녹색은 포인트다. 한 호 안에서 메인·서브가 같은 프리셋이어도 괜찮다.

## 레이아웃 (`layout`)

- `scene` (장면형, 기본): 배경까지 그려진 이미지가 썸네일 전체를 채운다. 14호 방식.
- `object` (오브젝트형): 배경이 투명한 3D 오브젝트 PNG를 오른쪽에 둔다.
- `photo` (사진형): 오른쪽 절반에 실사진. 인물 사진은 회사 보유 사진만 쓴다고 안내한다.

## 키워드 칩 (`chips`)

- 기획안에 콘텐츠의 **핵심 단계·키워드 3개**가 분명할 때만 `chipsOn: true`. 아니면 `false`로 두고 `label`은 빈 문자열.
- `label`은 **7자 이내**의 명사형(예: "결과 확인", "사후관리").
- `icon`은 아래 목록의 값만 쓴다(Lucide 라인 아이콘):
  `User` 사람 · `Users` 사람들 · `FileText` 문서 · `ClipboardCheck` 체크리스트 · `HeartPulse` 건강 · `Stethoscope` 진료 · `Hospital` 병원 · `CalendarCheck` 일정 · `ShieldCheck` 안전 · `Activity` 활동 · `TrendingUp` 상승 · `ChartColumn` 차트 · `MessageCircle` 상담 · `Building2` 회사 · `Footprints` 걷기 · `Pill` 약 · `Bell` 알림 · `CircleCheck` 완료 · `Search` 확인 · `Smartphone` 앱 · `Clock` 시간 · `Target` 목표
- `chips` 배열은 항상 3개를 채운다(안 쓰는 칸은 label을 빈 문자열로).

## 이미지 프롬프트 제안

콘텐츠마다 이미지 생성용 프롬프트를 **영문 1개 + 한글 설명 1줄**로 준다. 레이아웃에 맞춰 쓴다.

- 공통: `soft 3D clay style, blue tone palette with one small green accent, soft studio lighting, clean, no text, no letters, no numbers, no logos`
- `scene`: 뒤에 `wide 16:9 composition, main object on the right third, empty soft light-blue background on the left two-thirds for text` 추가
- `object`: 뒤에 `single object, isolated, transparent background` 추가
- `photo`: 사물·공간 위주로 쓰고, 인물 사진은 생성하지 말고 회사 사진을 쓰라고 안내한다.

**이미지에는 절대 글자를 넣지 않는다.** 글자는 도구가 올린다.

## 예시 (14호, 실제 발행본)

```json
{"v":1,"issue":14,"no":"01","title":"검진결과가\n나왔습니다.\n무엇을 해야 할까요?","titleSize":26,"preset":"lightBlue","layout":"scene","image":null,"img":{"scale":100,"x":0,"y":0},"chipsOn":true,"chips":[{"icon":"User","label":"결과 확인"},{"icon":"MessageCircle","label":"사후관리"},{"icon":"TrendingUp","label":"건강관리 계획"}]}
```

```json
{"v":1,"issue":14,"no":"02","title":"걷기 챌린지,\n더 오래 참여하고\n더 쉽게 운영하려면?","titleSize":26,"preset":"lightBlue","layout":"scene","image":null,"img":{"scale":100,"x":0,"y":0},"chipsOn":false,"chips":[{"icon":"Footprints","label":""},{"icon":"Smartphone","label":""},{"icon":"TrendingUp","label":""}]}
```
