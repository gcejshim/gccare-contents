// GC케어 서비스 규칙 — 썸네일 도구 · 통합본 AI로 그리기 공용 (2026-10-30). 고치면 두 곳 다 반영됨 (빌드 필요)
// 주제 표(OBJ_MAP): [주제 낱말, 기본 물건, 표면 무늬(한글), 표면 무늬(영어)] · OBJ_EN: 물건 이름 영어 병기(CGM은 실제 기기 모양) · editSend: [수정하기] 문장에 붙이기
(function(){
  // 2026-10-29 사용자: 표현이 한정적 → 금융 · 헬스케어 3D 아이콘 세트(모니모 · Pinterest)에서 '무엇을 그렸는지'만 가져와 주제를 늘림 (모양 · 색은 따라가지 않음, 그림체는 지금 규칙 그대로)
  // [주제 낱말, 기본 물건, 물건 표면 아이콘(한글), 같은 아이콘(영어 핵심 규칙용)]. 한 글자 낱말(목 · 위 · 술 · 간)은 '목표 · 기술 · 시간'에 걸려서 쓰지 않음
  const OBJ_MAP = [
    [/스트레스|마음|정신|번아웃|우울|치매|인지/, '뇌 모양 조형, 두 손으로 감싼 하트, 말풍선, 따뜻한 차, 쿠션', '마음 게이지, 잔잔한 물결 선', 'a calm mood gauge, soft wave lines'],
    [/폭염|온열|더위|한랭|추위|혹한/, '온도계, 물병, 선풍기 또는 담요, 해 또는 눈송이', '온도계 눈금, 물방울, 해 · 눈송이', 'a thermometer scale, water drops, a sun or snowflake'],
    [/응급|구급|심폐|CPR|AED/i, '구급함, 붕대, 반창고, 심장 모양 AED', '심박 선, 십자', 'a heartbeat line, a plus sign'],
    [/비만|체중|BMI|체성분|뱃살|허리둘레/i, '체중계, 줄자, 게이지(계기판), 건강 식단 도시락', '체성분 게이지, 줄자 눈금, 체중 추이 선', 'a body composition gauge, tape-measure marks, a weight trend line'],
    [/식단|영양|식습관|식사|점심|음식|나트륨|당류/, '도시락, 샌드위치와 커피, 샐러드 볼, 주방 저울, 물병', '식단 접시 그림, 영양 원그래프, 물방울', 'a balanced-plate diagram, a nutrition pie chart, water drops'],
    [/수면|잠|피로|불면/, '베개, 달, 수면 그래프가 뜬 휴대폰, 알람 시계', '초승달, 수면 물결 그래프', 'a crescent moon, a sleep wave graph'],
    [/금연|흡연|담배|호흡기|폐/, '폐 모양 조형, 물방울, 금연 표시', '폐 모양, 숨결 선, 금연 표시', 'a lungs shape, breath lines, a no-smoking sign'],
    [/절주|음주|과음|술자리|알코올/, '물잔, 금지 표시, 게이지(계기판)', '물잔, 게이지, 금지 표시', 'a water glass, a gauge, a no-alcohol sign'],
    [/운동|걷기|걷는|걸음|만\s?보|챌린지|다이어트|신체활동/, '운동화, 덤벨, 걸음 수가 뜬 스마트워치, 과녁과 다트', '걸음 수 링 그래프, 발자국, 과녁', 'a step-count ring, footprints, a target'],
    [/근골격|자세|허리|거북목|어깨|척추|스트레칭/, '척추 모양 조형, 사무용 의자, 스트레칭 밴드, 폼롤러', '척추 선, 바른 자세 실루엣', 'a spine line, a good-posture silhouette'],
    // 10/30 사용자: GC케어 혈당 서비스는 CGM(연속혈당측정) 모니터링 — 실제 앱 화면(docs/서비스자료/CGM앱_혈당그래프.png): 파란 그라데이션 · 흰 곡선 · 솟은 부분 빨강 · 식사 아이콘. 실제 기기(docs/서비스자료/CGM센서_부착.png): 흰 타원 패치 위 연회색 · 하늘빛 알약 모양 센서, 위팔 뒤쪽 — 로고만 없이. 목록 첫 번째는 앱 휴대폰(주인공감, 센서가 주인공이면 팔을 원통으로 그림) → 손가락 채혈 혈당 측정기가 아니라 팔에 붙이는 원형 센서 + 앱의 연속 그래프
    [/혈당|당뇨|CGM|연속혈당|당 떨어|스파이크/i, '혈당 앱 화면이 뜬 휴대폰(CGM 앱), 흰 타원 패치 위 연회색 타원형 CGM 센서, 커피잔, 간식', '파란 그라데이션 화면 위 흰 연속 혈당 곡선(목표선 위로 솟은 부분만 빨강), 식사 아이콘', 'a white continuous glucose curve on a blue gradient screen whose high part above the dotted target line is clearly bright red, a small meal icon'],
    [/혈압|뇌심|심혈관|만성|고혈압|콜레스테롤|심장/, '심장 모양 조형과 심박 선, 혈압계, 심박이 뜬 스마트워치', '심박 선, 혈압 게이지, 혈당 방울', 'a heartbeat line, a blood-pressure gauge, a blood-sugar drop'],
    [/구강|치아|치과|잇몸/, '치아 모양 조형, 칫솔, 치실', '치아 모양, 칫솔', 'a tooth shape, a toothbrush'],
    [/위내시경|대장|내시경|소화|위장|장 건강/, '위 · 장 모양 조형, 하트 표시 클립보드, 달력', '위 모양, 달력 표시', 'a stomach shape, a calendar mark'],
    [/감염|감염병|독감|코로나|위생|방역|바이러스/, '둥근 바이러스 조형, 마스크, 손 소독제, 체온계', '물방울, 손 모양, 둥근 바이러스 무늬', 'water drops, a hand shape, a simple round virus shape'],
    [/공시|법령|법률|법적|개정|제도|의무|규정|과태료/, '공시 책자 또는 서류 파일, 원통 막대그래프, 도장, 달력', '심박 선이 있는 서류 칸, 건강 지표 막대그래프', 'document sections with a heartbeat line, a health-indicator bar chart'],
    [/예방|보장|보험|안전보건|안전|보호|산재/, '십자 배지가 있는 둥근 방패, 두 손으로 감싼 하트, 하트 표시 클립보드', '십자', 'a plus sign'],
    [/검진|결과지|수검|재검/, '하트 표시 클립보드(검진표), 입체 탁상 달력, 돋보기, 결과 문서, 혈압계, 결과 리포트가 뜬 휴대폰', '심박 선, 결과 막대그래프, 달력 표시', 'a heartbeat line, a result bar chart, a calendar mark'],
    [/데이터|리포트|통계|분석|설문|결과\s?보고|비율|증가|감소|추이/, '원통 막대그래프와 위 · 아래 화살표, 원그래프 조각, 게이지(계기판), 돋보기', '막대 · 원그래프, 증감 화살표', 'a cylinder bar chart, a pie chart, one up or down arrow'],
    [/상담|비대면|원격|코칭/, '화면에 하트가 뜬 노트북, 헤드셋, 입체 말풍선 조형, 휴대폰', '말풍선, 영상 통화 화면', 'a speech bubble, a video-call screen'],
    [/정보|팁|Q&A|궁금|방법|알아보/i, '입체 전구, 펼친 안내 책자, 입체 말풍선 조형, 완료 화면이 뜬 휴대폰', '전구, 말풍선', 'a light bulb, a speech bubble'],
  ];
  // 건강검진 · 건강관리 (병원 · 진료 도구 말고 기업 건강관리)
  const OBJ_DEFAULT = [null, '건강관리 앱 화면 휴대폰, 하트 표시 클립보드, 원통 막대그래프, 게이지(계기판), 달력', '심박 선, 단순한 사람 실루엣, 걸음 · 수면 · 체중 같은 생활 지표 아이콘', 'a heartbeat (ECG) line, a simple human body silhouette, step / sleep / weight icons'];
  const topicFor = text => OBJ_MAP.find(([re]) => re.test(String(text || ''))) || OBJ_DEFAULT;
  function objectsFor(title){ return topicFor(title)[1]; }
  // 물건 이름 영어 병기 (짧은 프롬프트 · [수정하기] 공통). 10/30: '뉴스페이퍼'를 책자로 그림 → 영어를 괄호로, CGM은 실제 기기 모양
  const OBJ_EN = {'뉴스페이퍼':'a folded newspaper','신문':'a folded newspaper','책자':'a booklet','휴대폰':'a smartphone','스마트폰':'a smartphone','노트북':'a laptop','모니터':'a monitor','달력':'a desk calendar','리포트':'a report document','결과지':'a result sheet','클립보드':'a clipboard','체중계':'a bathroom scale','혈압계':'a blood pressure monitor','운동화':'sneakers','방패':'a shield','돋보기':'a magnifying glass','CGM 센서':'an oval, pill-shaped light gray-blue continuous glucose monitor (CGM) sensor on a slightly larger white oval adhesive patch, no logo','CGM':'an oval, pill-shaped light gray-blue continuous glucose monitor (CGM) sensor on a slightly larger white oval adhesive patch, no logo','연속혈당측정기':'an oval, pill-shaped light gray-blue continuous glucose monitor (CGM) sensor on a slightly larger white oval adhesive patch, no logo','혈당 센서':'an oval, pill-shaped light gray-blue continuous glucose monitor (CGM) sensor on a slightly larger white oval adhesive patch, no logo','커피잔':'a coffee cup','초콜릿':'a chocolate bar'};
  const EN_RE = new RegExp(Object.keys(OBJ_EN).sort((a, b) => b.length - a.length).map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'g');
  const withEn = t => t.replace(EN_RE, m => `${m}(${OBJ_EN[m]})`);
  // [수정하기] 문장에도 서비스 규칙: 물건 이름 영어 병기 + 혈당 화면을 고칠 땐 우리 앱 특징 (10/30 사용자)
  const editSend = what => withEn(what) + (/혈당|CGM/i.test(what) && /그래프|곡선|화면|앱/.test(what) ? ' (Glucose app screen: a white continuous curve on a blue gradient, only the part above the dotted target line in bright red.)' : '');
  window.GC_SVC = {OBJ_MAP, OBJ_DEFAULT, topicFor, objectsFor, OBJ_EN, withEn, editSend};
})();
