# GC케어 뉴스레터 차트 제작 가이드

## 폴더 구조
- 작업 폴더: `/Users/ejshim/Documents/gccare/콘텐츠통합/뉴스레터/`
- 월별 폴더: `YYYYMM_뉴스레터/` (예: `202606_뉴스레터`)
- HTML 소스: `YYYYMM_뉴스레터/html/` 안에 저장
- 완성 이미지: `YYYYMM_뉴스레터/` 루트에 저장

### 파일 네이밍 규칙
| 구분 | 패턴 | 예시 |
|------|------|------|
| HTML | `YYYYMM_contentsNN_pcNN.html` | `202605_contents01_pc01.html` |
| PC 이미지 | `YYYYMM_contentsNN_pNN.png` | `202605_contents01_p01.png` |
| 모바일 이미지 | `YYYYMM_contentsNN_mNN.png` | `202605_contents01_m01.png` |

---

## 공통 디자인 스펙

| 항목 | PC | 모바일 |
|------|-----|--------|
| 컨테이너 | 100% width, border 1px #e6e6e6 | 동일 |
| 패딩 | 32px | 20px 16px |
| 폰트 | Pretendard CDN | 동일 |
| 가이드선 | 점선 [2,2], #E2E5E8, 1.2px | 동일 |
| 기준선(0) | 실선 | 동일 |
| 가이드선 방식 | Chart.js 커스텀 플러그인 (beforeDatasetsDraw) | 동일 |

### 가이드선 플러그인 (수직 - 가로막대 차트용)
```javascript
const dashedVGrid = {
  id: 'dashedVGrid',
  beforeDatasetsDraw(chart) {
    const { ctx, chartArea: { top, bottom }, scales: { x } } = chart;
    ctx.save();
    ctx.strokeStyle = '#E2E5E8';
    ctx.lineWidth = 1.2;
    x.ticks.forEach((tick, i) => {
      if (Math.abs((tick.value - baselineValue) % stepSize) > 0.001) return;
      const xPos = x.getPixelForTick(i);
      ctx.setLineDash(tick.value === baselineValue ? [] : [2, 2]);
      ctx.beginPath();
      ctx.moveTo(xPos, top);
      ctx.lineTo(xPos, bottom);
      ctx.stroke();
    });
    ctx.restore();
  }
};
```

### 가이드선 플러그인 (수평 - 세로막대/스택 차트용)
```javascript
const dashedHGrid = {
  id: 'dashedHGrid',
  beforeDatasetsDraw(chart) {
    const { ctx, chartArea: { left, right }, scales: { y } } = chart;
    ctx.save();
    ctx.strokeStyle = '#E2E5E8';
    ctx.lineWidth = 1.2;
    y.ticks.forEach((tick, i) => {
      const yPos = y.getPixelForTick(i);
      ctx.setLineDash(tick.value === 0 ? [] : [2, 2]);
      ctx.beginPath();
      ctx.moveTo(left, yPos);
      ctx.lineTo(right, yPos);
      ctx.stroke();
    });
    ctx.restore();
  }
};
```

---

## 차트 유형별 스펙

### TYPE A — 가로 막대 (배수/비율 비교)
예: 라이프스타일 관련 검사 (01번)

- barThickness: 20, 막대 간격 12px → chart height = bars × 32 + 40
- 막대 색상: #0AC262
- floating bar: `data: values.map(v => [1.0, v])`
- x축 stepSize: 0.5, 기준선 1.0x
- 타이틀: left, 24px bold + `.sub` span 13px #888
- max: 최댓값 + 0.15 (여백)
- 모바일 height: bars × 40 + 40

### TYPE B — 세로 스택 막대 (100% 구성)
예: 지원금 구간별 추가 결제 검사 구성 (02번)

- 색상 팔레트 (GC케어 그린):
  - 소화기·내시경: #1B5E35
  - 심뇌혈관·뇌: #0AC262
  - 여성암(유방): #67E69C
  - 여성건강(부인과): #3D7A6C
  - 갑상선: #8BC4BE
  - 기타: #BFC9CE
- datalabels: `v >= 5 ? v.toFixed(1)+'%' : ''`, 기타 세그먼트는 #666 텍스트
- 모바일 datalabels: size 9, weight normal
- 범례: bottom, center, boxWidth/Height 7
- PC height: 280px, 모바일 height: 340px

### TYPE C — 가로 막대 (절대값 + 라벨)
예: 추가 검사 건수 Top10 (03번)

- barThickness: 20, chart height = bars × 32 + 40
- 1위 항목 색상: #0AC262, 나머지: #A9F5C3
- datalabels: anchor end, align right, clip false
- layout.padding.right: 55 (모바일: 38)
- x축 stepSize: 1000, maxRotation: 0
- 모바일: stepSize 2000, font 9px, height = bars × 34 + 40

---

## 스크린샷 자동화

### 스크립트 위치
`/Users/ejshim/Downloads/screenshot_ipr.py`

### 실행
```bash
python3 /Users/ejshim/Downloads/screenshot_ipr.py
```

### 스펙
| 버전 | 뷰포트 | DPR | 캡처 방식 |
|------|--------|-----|----------|
| PC | 1012px | 2x | `.wrap` 요소 |
| 모바일 | 350px | 3x | `.wrap` 요소 |

### 새 달 작업 시 스크립트 수정
```python
FOLDER = 'YYYYMM_뉴스레터'  # ← 여기만 수정
charts = [
    ('YYYYMM_contents01_pc01.html', 'YYYYMM_contents01', '01'),
    ('YYYYMM_contents01_pc02.html', 'YYYYMM_contents01', '02'),
    ('YYYYMM_contents01_pc03.html', 'YYYYMM_contents01', '03'),
]
```

---

## 다음 호 작업 순서
1. 월별 폴더 생성: `YYYYMM_뉴스레터/` + `YYYYMM_뉴스레터/html/`
2. `202605_뉴스레터/html/` 의 HTML 파일 복사 후 파일명의 `202605` → 새 월로 변경
3. 데이터 수치 업데이트
4. `screenshot_ipr.py`의 `FOLDER` 변수만 새 월로 수정 (예: `'202606_뉴스레터'`)
5. `python3 /Users/ejshim/Downloads/screenshot_ipr.py` 실행
6. 완성 이미지 확인 후 납품
