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
 *   4. 위쪽 함수 고르기에서 testRequest_ 를 고르고 [실행] → 권한 허용 (메일 보내기 권한 포함)
 *      → '뉴스레터 요청' 탭에 시험 줄이 생기고 메일이 오면 성공 (시험 줄은 지워도 됨)
 *   5. [배포 › 배포 관리] → 지금 쓰는 배포의 연필 → 버전 '새 버전' → [배포]
 *      (새 배포를 만들면 주소가 바뀌어서 안 됨 — 꼭 기존 배포를 새 버전으로)
 */

const REQUEST_NOTIFY = '';   // 요청이 오면 알림 메일 받을 주소를 붙여 넣을 때 적어요 (예: 'name@gccorp.com'). 비워 두면 메일 없이 시트에만 (공개 저장소라 주소는 여기 적어 두지 않음)

function handleRequestPost_(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return null; }
  if (!d || d.action !== 'request') return null;   // 요청이 아니면 원래 doPost가 그대로 처리
  saveRequest_(d);
  return ContentService.createTextOutput(JSON.stringify({ ok: true, saved: 'request' })).setMimeType(ContentService.MimeType.JSON);
}

function saveRequest_(d) {
  const tool = String(d.tool || '뉴스레터').replace(/[\[\]*?:\/\\]/g, '');
  const name = tool + ' 요청';
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(['날짜', '회사', '팀', '이름', '화면', '요청 내용', '버전', '상태', '메모']);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, 9).setFontWeight('bold').setBackground('#f0f8ff');
    sh.setColumnWidth(6, 420);
  }
  const clean = s => String(s || '').slice(0, 2000);
  sh.appendRow([new Date(), clean(d.c), clean(d.t), clean(d.n), clean(d.screen), clean(d.text), clean(d.ver), '접수', '']);
  sh.getRange(sh.getLastRow(), 6).setWrap(true);

  if (REQUEST_NOTIFY) {
    try {
      MailApp.sendEmail(REQUEST_NOTIFY, `[${tool} 요청] ${clean(d.n)} · ${clean(d.screen)}`,
        `${clean(d.c)} ${clean(d.t)} ${clean(d.n)}님이 요청을 보냈어요.\n\n화면: ${clean(d.screen)}\n\n${clean(d.text)}\n\n— 시트 '${name}' 탭에 기록됨`);
    } catch (err) { console.warn('알림 메일 실패(기록은 됨): ' + err); }
  }
}

function testRequest_() {
  saveRequest_({ tool: '뉴스레터', c: 'GC케어', t: 'UX팀', n: '시험', screen: '이용 가이드', text: '요청 보내기 시험이에요. 이 줄은 지워도 돼요.', ver: '' });
}
