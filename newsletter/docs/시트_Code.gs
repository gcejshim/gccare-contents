/**
 * 기록 시트(gccare-cardnews-log) Apps Script의 Code.gs 사본 — 2026-10-27 배포본 (카드뉴스 · 뉴스레터 함께 씀)
 * 시트에서 고치면 여기도 같이 맞춰 둘 것. 요청 · 명단 처리는 시트_요청받기.gs
 *
 * 탭: 명단 ApprovedUsers(회사 · 팀명 · 이름 · 뉴스레터), 카드뉴스 AccessLog · UsageLog, 뉴스레터 '뉴스레터 접속' · '뉴스레터 사용' · '뉴스레터 요청'
 */
function doGet(e) {
  var nu = handleUsersGet_(e); if (nu) return nu;
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('ApprovedUsers');
  var rows = sheet.getDataRange().getValues();
  var users = [];
  for (var i = 1; i < rows.length; i++) {
    var c = rows[i][0], t = rows[i][1], n = rows[i][2];
    if (c && t && n) users.push({ c: String(c), t: String(t), n: String(n) });
  }
  return ContentService.createTextOutput(JSON.stringify(users))
    .setMimeType(ContentService.MimeType.JSON);
}

// 도구별 탭: 카드뉴스 = AccessLog · UsageLog, 뉴스레터 = 뉴스레터 접속 · 뉴스레터 사용 (없으면 머리글과 함께 만듦)
function logSheet_(ss, name, head) {
  var sh = ss.getSheetByName(name);
  if (!sh) { sh = ss.insertSheet(name); sh.appendRow(head); sh.setFrozenRows(1); }
  return sh;
}

function doPost(e) {
  var rq = handleRequestPost_(e); if (rq) return rq;
  var data = JSON.parse(e.postData.contents);
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ts = Utilities.formatDate(new Date(), "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");
  var nl = data.tool === '뉴스레터';

  if (data.action === 'usage') {
    var usageSheet = logSheet_(ss, nl ? '뉴스레터 사용' : 'UsageLog', ['시간', '회사', '팀명', '이름', '종류']);
    usageSheet.appendRow([ts, data.c, data.t, data.n, nl ? String(data.kind || '').replace(/^뉴스레터 · /, '') : data.kind]);
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  var sheet = logSheet_(ss, nl ? '뉴스레터 접속' : 'AccessLog', ['시간', '회사', '팀명', '이름']);
  sheet.appendRow([ts, data.c, data.t, data.n]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
