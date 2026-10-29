/**
 * 요청 받기 — 통합본 오른쪽 아래 [요청 보내기]로 쓴 글을 '뉴스레터 요청' 탭에 한 줄씩 (2026-10-26 은진님 요청)
 *
 * 탭은 도구마다 따로: 뉴스레터 → '뉴스레터 요청' (카드뉴스에 달면 '카드뉴스 요청').
 * 접속 · 사용 기록(AccessLog · UsageLog)은 지금처럼 함께 쌓임 → 통계는 카드뉴스 · 뉴스레터 합쳐서도, tool 칸으로 나눠서도 볼 수 있음.
 *
 * 붙이는 법 (처음 한 번):
 *   1. 기록 시트를 열고 [확장 프로그램 › Apps Script]
 *   2. 왼쪽 [파일 +] › [스크립트] → 이름 '요청받기' → 이 파일 내용을 전부 붙여 넣고 저장
 *   3. 원래 있던 doPost 함수를 찾아서, 함수 첫 줄에 아래 한 줄을 넣고 저장
 *        var rq = handleRequestPost_(e); if (rq) return rq;
 *   4. 위쪽 함수 고르기에서 testRequest 를 고르고 [실행] → 권한 허용 (메일 보내기 · Drive 권한 포함)
 *      → '뉴스레터 요청' 탭에 시험 줄이 생기고 메일이 오면 성공 (시험 줄은 지워도 됨)
 *   5. [배포 › 배포 관리] → 지금 쓰는 배포의 연필 → 버전 '새 버전' → [배포]
 *      (새 배포를 만들면 주소가 바뀌어서 안 됨 — 꼭 기존 배포를 새 버전으로)
 *
 * 첨부 (2026-10-27 추가): 요청에 붙인 파일(캡처 등, 3개 · 합쳐 10MB까지)은 내 Drive '뉴스레터 요청 첨부' 폴더에 저장되고
 * 시트 맨 끝 '첨부' 칸에 링크가 들어감. 이 파일로 바꿨으면 위 4 · 5번(권한 허용 · 새 버전 배포)을 한 번 더.
 * 파일은 공유하지 않음(스크립트 주인만 열림) — 다른 사람도 봐야 하면 폴더를 그 사람에게 공유
 *
 * 뉴스레터 사용자 명단 (2026-10-27 추가): 통합본 사용자 확인 창에는 명단 탭의 '뉴스레터' 칸에 O(아무 글자나)를 적은 사람만 보임.
 *   1. 기존 명단 탭(회사 · 팀 · 이름이 있는 탭) 첫 줄 오른쪽 빈칸에 '뉴스레터'라고 적고, 보여 줄 사람 줄에 O
 *   2. 원래 있던 doGet 함수 첫 줄에 아래 한 줄을 넣고 저장 → 위 5번처럼 기존 배포를 새 버전으로
 *        var nu = handleUsersGet_(e); if (nu) return nu;
 *   - 탭 이름은 몰라도 됨: 첫 줄에 '뉴스레터'와 '이름'이 함께 있는 탭을 찾음. '뉴스레터' 칸이 없으면 예전처럼 전체 명단
 *   - 카드뉴스 편집기는 ?tool=뉴스레터 를 안 붙이므로 지금처럼 전체 명단
 *
 * Teams 알림 (2026-10-29 추가 — 회사 Outlook이 Google에서 보낸 메일을 막아서 메일 대신 Teams 채널로):
 *   1. Teams 채널 이름 옆 [… › 워크플로] → '웹후크 요청이 수신되면 채널에 게시' → 팀 · 채널 고르고 [워크플로 추가] → 나온 주소(URL) 복사
 *   2. Apps Script 왼쪽 [⚙ 프로젝트 설정] › 맨 아래 [스크립트 속성 추가] → 속성 TEAMS_WEBHOOK, 값에 1번 주소 → 저장
 *      (주소는 코드에 적지 않음 — 공개 저장소라서. 주소를 아는 사람은 누구나 그 채널에 글을 올릴 수 있음)
 *   3. 함수 고르기에서 testTeams 를 고르고 [실행] → 권한 허용(외부 서비스 연결) → Teams 채널에 시험 카드가 오면 성공
 *   4. 위 5번처럼 기존 배포를 새 버전으로
 */

const REQUEST_FOLDER = '뉴스레터 요청 첨부';   // 첨부를 저장할 내 Drive 폴더 이름 (없으면 만듦)
const REQUEST_NOTIFY = '';   // 알림 메일 받을 주소. 비워 두면 스크립트 주인(시트 주인) 계정으로 감 — 공개 저장소라 주소는 여기 적지 않음. 여러 명이면 'a@…,b@…'
const REQUEST_MAIL = false;   // 메일 알림 (회사 Outlook에서 막혀 2026-10-29 끔 → Teams 알림 사용). true면 메일도 보냄

function handleRequestPost_(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return null; }
  if (!d || d.action !== 'request') return null;   // 요청이 아니면 원래 doPost가 그대로 처리
  const n = saveRequest_(d);
  return ContentService.createTextOutput(JSON.stringify({ ok: true, saved: 'request', files: n })).setMimeType(ContentService.MimeType.JSON);
}

function saveRequest_(d) {
  const tool = String(d.tool || '뉴스레터').replace(/[\[\]*?:\/\\]/g, '');
  const name = tool + ' 요청';
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(['날짜', '회사', '팀', '이름', '화면', '요청 내용', '버전', '상태', '메모', '첨부']);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground('#f0f8ff');
    sh.setColumnWidth(6, 420);
  }
  if (!sh.getRange(1, 10).getValue()) sh.getRange(1, 10).setValue('첨부').setFontWeight('bold').setBackground('#f0f8ff');   // 예전에 만든 탭에 칸 더하기
  const clean = s => String(s || '').slice(0, 2000);
  const links = saveFiles_(d, tool);
  sh.appendRow([new Date(), clean(d.c), clean(d.t), clean(d.n), clean(d.screen), clean(d.text), clean(d.ver), '접수', '', links.map(f => f.url).join('\n')]);
  sh.getRange(sh.getLastRow(), 6).setWrap(true);
  if (links.length) sh.getRange(sh.getLastRow(), 10).setRichTextValue(richLinks_(links));

  sendTeams_(d, tool, name, links);   // Teams 채널 알림 (스크립트 속성 TEAMS_WEBHOOK이 있을 때만)
  const to = REQUEST_NOTIFY || Session.getEffectiveUser().getEmail();   // 웹 앱은 '나로 실행'이라 주인 주소
  if (REQUEST_MAIL && to) {
    try {
      MailApp.sendEmail(to, `[${tool} 요청] ${clean(d.n)} · ${clean(d.screen)}`,
        `${clean(d.c)} ${clean(d.t)} ${clean(d.n)}님이 요청을 보냈어요.\n\n화면: ${clean(d.screen)}\n\n${clean(d.text)}\n\n${links.map(f => '첨부: ' + f.name + ' ' + f.url).join('\n')}${links.length ? '\n\n' : ''}— 시트 '${name}' 탭에 기록됨`);
    } catch (err) { console.warn('알림 메일 실패(기록은 됨): ' + err); }
  }
  return links.length;
}

// 첨부를 Drive 폴더에 저장 → [{name, url}]. 한 개가 실패해도 요청 글과 나머지 파일은 저장
function saveFiles_(d, tool) {
  const list = Array.isArray(d.files) ? d.files.slice(0, 3) : [];
  if (!list.length) return [];
  const it = DriveApp.getFoldersByName(REQUEST_FOLDER);
  const folder = it.hasNext() ? it.next() : DriveApp.createFolder(REQUEST_FOLDER);
  const stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd_HHmmss');
  const who = String(d.n || '').replace(/[\\/:*?"<>|]/g, '').slice(0, 20);
  const out = [];
  list.forEach((f, i) => {
    try {
      const name = `${stamp}_${who}_${String(f.name || 'file').replace(/[\\/:*?"<>|]/g, '_').slice(0, 80)}`;
      const blob = Utilities.newBlob(Utilities.base64Decode(f.data), f.type || 'application/octet-stream', name);
      const file = folder.createFile(blob);
      file.setDescription(`${tool} 요청 · ${d.n || ''} · ${d.screen || ''}`);
      out.push({ i, name: f.name || name, url: file.getUrl() });
    } catch (err) { console.warn('첨부 저장 실패: ' + err); }
  });
  return out;
}

function richLinks_(links) {
  const text = links.map(f => f.name).join('\n');
  const b = SpreadsheetApp.newRichTextValue().setText(text);
  let at = 0;
  links.forEach(f => { b.setLinkUrl(at, at + f.name.length, f.url); at += f.name.length + 1; });
  return b.build();
}

// Teams 채널에 의견 카드 올리기. 첨부는 Drive 링크 대신 개수만 (회사 보안에서 Google Drive 링크가 막힐 수 있어서) — 실패해도 시트 기록은 그대로
// 이미지 첨부는 통합본이 만든 작은 미리보기(d.thumbs [{i, d}], 폭 600 JPG data URI · 합쳐 170KB 안)를 카드에 바로 넣음 (2026-10-29).
// 미리보기를 누르면 원본(Drive)이 열림 — Drive 파일은 공유하지 않아 스크립트 주인만 열림
function sendTeams_(d, tool, name, links) {
  const url = PropertiesService.getScriptProperties().getProperty('TEAMS_WEBHOOK');
  if (!url) return;
  const clean = s => String(s || '').slice(0, 1500);
  const who = [clean(d.c), clean(d.t), clean(d.n)].filter(Boolean).join(' · ');
  const thumbs = (Array.isArray(d.thumbs) ? d.thumbs : []).map(t => typeof t === 'string' ? { d: t } : t || {})
    .filter(t => /^data:image\/jpeg;base64,/.test(String(t.d))).slice(0, 3);
  const image = t => {
    const f = links.find(l => l.i === t.i);
    return Object.assign({ type: 'Image', url: t.d, size: 'Stretch', spacing: 'Medium' },
      f ? { selectAction: { type: 'Action.OpenUrl', url: f.url, title: '원본 보기' } } : {});
  };
  const card = {
    type: 'AdaptiveCard', $schema: 'http://adaptivecards.io/schemas/adaptive-card.json', version: '1.4',
    body: [
      { type: 'TextBlock', text: `${tool} 의견이 들어왔습니다`, weight: 'Bolder', size: 'Medium', wrap: true },
      { type: 'FactSet', facts: [
        { title: '보낸 사람', value: who || '-' },
        { title: '화면', value: clean(d.screen) || '-' },
        { title: '버전', value: clean(d.ver) || '-' },
        { title: '첨부', value: links.length ? `${links.length}개 · ${thumbs.length ? '아래 미리보기를 누르면 원본, ' : ''}시트 '${name}' 탭에도 있음` : '없음' }
      ] },
      { type: 'TextBlock', text: clean(d.text) || '(내용 없음)', wrap: true, spacing: 'Medium' }
    ].concat(thumbs.map(image))
  };
  try {
    UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      payload: JSON.stringify({ type: 'message', attachments: [{ contentType: 'application/vnd.microsoft.card.adaptive', contentUrl: null, content: card }] }) });
  } catch (err) { console.warn('Teams 알림 실패(기록은 됨): ' + err); }
}

function testTeams() {
  if (!PropertiesService.getScriptProperties().getProperty('TEAMS_WEBHOOK')) throw new Error('스크립트 속성 TEAMS_WEBHOOK이 없어요 (위 Teams 알림 2번)');
  sendTeams_({ c: '시험', t: 'AX팀', n: '심은진', screen: '콘텐츠 이미지', ver: 'v1.0', text: 'Teams 알림 시험입니다. 이 카드가 보이면 성공이에요.' }, '뉴스레터', '뉴스레터 요청', []);
}

function testRequest() {
  saveRequest_({ tool: '뉴스레터', c: 'GC케어', t: 'UX팀', n: '시험', screen: '이용 가이드', text: '요청 보내기 시험이에요. 이 줄은 지워도 돼요.', ver: '',
    files: [{ name: '시험.txt', type: 'text/plain', data: Utilities.base64Encode('첨부 시험이에요. 지워도 돼요.', Utilities.Charset.UTF_8) }] });
}

// 뉴스레터 사용자 명단 — 통합본이 ?tool=뉴스레터 로 부르면 '뉴스레터' 칸에 표시한 사람만 [{c, t, n}]
function handleUsersGet_(e) {
  if (!e || !e.parameter || e.parameter.tool !== '뉴스레터') return null;
  const list = newsletterUsers_();
  if (!list) return null;   // '뉴스레터' 칸이 아직 없으면 원래 doGet이 전체 명단을 줌
  return ContentService.createTextOutput(JSON.stringify(list)).setMimeType(ContentService.MimeType.JSON);
}

function newsletterUsers_() {
  for (const sh of SpreadsheetApp.getActiveSpreadsheet().getSheets()) {
    if (sh.getLastRow() < 1 || sh.getLastColumn() < 1) continue;
    const head = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0].map(v => String(v).trim());
    const mark = head.indexOf('뉴스레터'), name = head.findIndex(v => v.includes('이름'));
    if (mark < 0 || name < 0) continue;
    const co = head.findIndex(v => v.includes('회사')), team = head.findIndex(v => v.includes('팀') || v.includes('부서'));
    if (sh.getLastRow() < 2) return [];
    return sh.getRange(2, 1, sh.getLastRow() - 1, head.length).getValues()
      .filter(r => String(r[mark]).trim() && String(r[name]).trim())
      .map(r => ({ c: co >= 0 ? String(r[co]).trim() : '', t: team >= 0 ? String(r[team]).trim() : '', n: String(r[name]).trim() }));
  }
  return null;
}
