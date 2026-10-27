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
 *   4. 위쪽 함수 고르기에서 testRequest_ 를 고르고 [실행] → 권한 허용 (메일 보내기 · Drive 권한 포함)
 *      → '뉴스레터 요청' 탭에 시험 줄이 생기고 메일이 오면 성공 (시험 줄은 지워도 됨)
 *   5. [배포 › 배포 관리] → 지금 쓰는 배포의 연필 → 버전 '새 버전' → [배포]
 *      (새 배포를 만들면 주소가 바뀌어서 안 됨 — 꼭 기존 배포를 새 버전으로)
 *
 * 첨부 (2026-10-27 추가): 요청에 붙인 파일(캡처 등, 3개 · 합쳐 10MB까지)은 내 Drive '뉴스레터 요청 첨부' 폴더에 저장되고
 * 시트 맨 끝 '첨부' 칸에 링크가 들어감. 이 파일로 바꿨으면 위 4 · 5번(권한 허용 · 새 버전 배포)을 한 번 더.
 * 파일은 공유하지 않음(스크립트 주인만 열림) — 다른 사람도 봐야 하면 폴더를 그 사람에게 공유
 */

const REQUEST_FOLDER = '뉴스레터 요청 첨부';   // 첨부를 저장할 내 Drive 폴더 이름 (없으면 만듦)
const REQUEST_NOTIFY = '';   // 알림 메일 받을 주소. 비워 두면 스크립트 주인(시트 주인) 계정으로 감 — 공개 저장소라 주소는 여기 적지 않음. 여러 명이면 'a@…,b@…'
const REQUEST_MAIL = true;   // false면 메일 없이 시트에만

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
  list.forEach(f => {
    try {
      const name = `${stamp}_${who}_${String(f.name || 'file').replace(/[\\/:*?"<>|]/g, '_').slice(0, 80)}`;
      const blob = Utilities.newBlob(Utilities.base64Decode(f.data), f.type || 'application/octet-stream', name);
      const file = folder.createFile(blob);
      file.setDescription(`${tool} 요청 · ${d.n || ''} · ${d.screen || ''}`);
      out.push({ name: f.name || name, url: file.getUrl() });
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

function testRequest_() {
  saveRequest_({ tool: '뉴스레터', c: 'GC케어', t: 'UX팀', n: '시험', screen: '이용 가이드', text: '요청 보내기 시험이에요. 이 줄은 지워도 돼요.', ver: '',
    files: [{ name: '시험.txt', type: 'text/plain', data: Utilities.base64Encode('첨부 시험이에요. 지워도 돼요.', Utilities.Charset.UTF_8) }] });
}
