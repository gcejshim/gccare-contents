// GC Care 카드뉴스 편집기 - AI 이미지 생성 프롬프트
// 이 파일은 편집기에서만 로드됩니다. 내보낸 HTML에는 포함되지 않습니다.

// __AI_START__
let refGuidelinesMale   = (function(){try{var b=atob('Q0hBUkFDVEVSOiDsnbQg7Lm065Oc7J2YIOyjvOyduOqzteydgCAzMOuMgCDtlZzqta3snbgg64Ko7ISxIDHsnbjsnbTri6QuIOyDgeydmCDsmLfsg4nsnYAg67CY65Oc7IucICNCQUQwRjEgKOyXsO2VnCDruJTro6gp66W8IOyCrOyaqe2VnOuLpC4g66qo65OgIOyEueyFmOyXkOyEnCDrj5nsnbztlZwg7J2466y87J20IOuTseyepe2VnOuLpC4gKOuLqCwg7J6l66m07JeQIOuUsOudvCDrkZAg7IKs656M7J20IO2VqOq7mCDrk7HsnqXtlaAg7IiYIOyeiOuLpC4pOw=='),c=new Uint8Array(b.length);for(var i=0;i<b.length;i++)c[i]=b.charCodeAt(i);return new TextDecoder().decode(c);}catch(e){return '';}})();
let refGuidelinesFemale = (function(){try{var b=atob('4pqg77iPIENSSVRJQ0FMIOKAlCBDSEFSQUNURVIgTVVTVCBCRSBGRU1BTEU6IOydtCDsubTrk5zsnZgg7KO87J246rO17J2AIOuwmOuTnOyLnCAzMOuMgCDtlZzqta3snbgg7Jes7ISxIDHsnbjsnbTri6QuIOygiOuMgCDrgqjshLEg7LqQ66at7YSw66W8IOq3uOumrOyngCDrp4jrnbwuIOyDgeydmCDsmLfsg4nsnYAg67CY65Oc7IucICNGRUVBQjAgKOyXsO2VnCDsmJDroZzsmrAp66W8IOyCrOyaqe2VnOuLpC4g66qo65OgIOyEueyFmOyXkOyEnCDrj5nsnbztlZwg7Jes7ISxIOyduOusvOydtCDrk7HsnqXtlZzri6QuICjri6gsIOyepeuptOyXkCDrlLDrnbwg65GQIOyCrOuejOydtCDtlajqu5gg65Ox7J6l7ZWgIOyImCDsnojri6QuKTs='),c=new Uint8Array(b.length);for(var i=0;i<b.length;i++)c[i]=b.charCodeAt(i);return new TextDecoder().decode(c);}catch(e){return '';}})();
// __AI_END__

// __AI_START__
const SECTION_STYLE = (function(){try{var b=atob('8J+aqyBBQlNPTFVURSBSVUxFUyDigJQgTkVWRVIgVklPTEFURToKMS4gWkVSTyBURVhULiBObyBsZXR0ZXJzLCBubyB3b3Jkcywgbm8gbnVtYmVycywgbm8gS29yZWFuLCBubyBFbmdsaXNoLCBubyBzeW1ib2xzIGFueXdoZXJlLiBJbWFnZSBpcyByZWplY3RlZCBpZiBBTlkgdGV4dCBhcHBlYXJzLgoyLiBQVVJFIFdISVRFIEJBQ0tHUk9VTkQgKCNGRkZGRkYpIE9OTFkuIE5vIGdyYWRpZW50cywgbm8gZmxvb3Igc2hhZG93cywgbm8gcmVmbGVjdGlvbnMsIG5vIHRleHR1cmVzLgoKIyMgSWxsdXN0cmF0aW9uIFN0eWxlCi0gU29mdCBwYXN0ZWwtYmFzZWQgbWluaW1hbCAzRCBjbGF5IGlsbHVzdHJhdGlvbgotIEtvcmVhbiBhZHVsdCBjaGFyYWN0ZXIgaW4gdGhlaXIgMzBzICh3aGVuIGEgcGVyc29uIGFwcGVhcnMpCi0gVXNlIGEgdW5pcXVlLCBkeW5hbWljIGFjdGlvbiBwb3NlIOKAlCB2YXJ5IGFjcm9zcyBpbWFnZXM6IHNpdHRpbmcsIGNyb3VjaGluZywgcmVhY2hpbmcsIHBvaW50aW5nLCBleGFtaW5pbmcsIGx5aW5nLCBzdHJldGNoaW5nLCBldGMuIE5FVkVSIHVzZSBhIHBsYWluIHN0YW5kaW5nL2ZhY2luZy1mb3J3YXJkIHBvc2UKLSBDdXRlIGJ1dCBub3QgY2hpbGRpc2gg4oCUIGNhbG0sIG1hdHVyZSB3ZWxsbmVzcyBtb29kCi0gRXllczogdmlzaWJsZSB3aGl0ZXMgd2l0aCBkYXJrIHB1cGlscywgc2xpZ2h0bHkgZHJvb3BpbmcgZXllbGlkcwotIFJvdW5kIGFuZCBzb2Z0IGZvcm1zLCBzZXJlbmUgYW5kIGNvbWZvcnRhYmxlIHdlbGxuZXNzIGF0bW9zcGhlcmUKLSBDbGVhbiBtb2JpbGUgYXBwIGlsbHVzdHJhdGlvbiBzdHlsZSwgb3ZlcmFsbCBicmlnaHQgYW5kIGNvb2wtdG9uZWQKCiMjIENvbG9yCi0gQnJpZ2h0LCBzb2Z0IHZpdmlkIHBhc3RlbCBwYWxldHRlIGFzIGJhc2UKLSBOZXV0cmFsIHRvIGNvb2wtdG9uZSBiYXNlZDsgbWluaW1pemUgaXZvcnkvY3JlYW0vd2FybSBiZWlnZQotIFVzZSBhIHN1YnRsZSAjNEJENDhDLWxpa2UgZ3JlZW4gYXMgYW4gYWNjZW50IG9uIG9uZSBvYmplY3Qgb25seQotIE1hbGUgY2hhcmFjdGVyIHRvcDogI0JBRDBGMSAvIEZlbWFsZSBjaGFyYWN0ZXIgdG9wOiAjRkVFQUIwCgojIyBMaWdodGluZyAmIFRleHR1cmUKLSBTdWJ0bGUgaGlnaGxpZ2h0cywgc29mdCBsaWdodGluZywgY29vbCB3aGl0ZSBuYXR1cmFsIGxpZ2h0IGZlZWwKLSBObyB5ZWxsb3cgbGlnaHRpbmcsIHR1bmdzdGVuLCBvciB3YXJtLXRvbmVkIHNoYWRvd3Mg4oCUIDNEIGNsYXkgdGV4dHVyZSBvbmx5LCBubyBwaG90b3JlYWxpc20KCiMjIENvbXBvc2l0aW9uICYgTGF5b3V0Ci0gQmFja2dyb3VuZDogcHVyZSAjRkZGRkZGIG9ubHkgKG5vIGdyYWRpZW50cywgbm8gZmxvb3IsIG5vIHNoYWRvd3MpCi0gQXNwZWN0IHJhdGlvOiAxNDo5IHdpZGUgbGFuZHNjYXBlCi0gT2JqZWN0cy9jaGFyYWN0ZXJzIG11c3QgZmlsbCB0aGUgZnJhbWUg4oCUIG1pbmltaXplIGVtcHR5IHNwYWNlIG9uIGFsbCBzaWRlcwotIE1haW4gb2JqZWN0cyBvY2N1cHkgODXigJM5NSUgb2YgdGhlIGltYWdlIGhlaWdodAotIE1BWElNVU0gNCBvYmplY3RzIHRvdGFsIGluY2x1ZGluZyBhbnkgY2hhcmFjdGVycyDigJQgTk8gRVhDRVBUSU9OUwotIFdoZW4gdXNpbmcgbXVsdGlwbGUgb2JqZWN0cywgY2x1c3RlciB0aGVtIHRpZ2h0bHkgaW4gdGhlIGNlbnRlciDigJQgZG8gTk9UIHNwcmVhZCBhY3Jvc3MgdGhlIGNhbnZhcwotIDHigJMyIG1haW4gb2JqZWN0cyBsYXJnZSBhbmQgZG9taW5hbnQ7IGFueSBhZGRpdGlvbmFsIG9iamVjdCBwbGFjZWQgY2xvc2UgYXMgYSBzbWFsbCBhY2NlbnQgb25seQoKIyMgUHJvaGliaXRlZAotIOKblCBOTyB0ZXh0LCBsZXR0ZXJzLCBudW1iZXJzLCBvciBzeW1ib2xzIG9mIGFueSBraW5kCi0g4puUIEJhY2tncm91bmQgbXVzdCBiZSBwdXJlIHdoaXRlICgjRkZGRkZGKSBvbmx5IOKAlCBubyBleGNlcHRpb25zCi0gTm8gcGhvdG9yZWFsaXNtLCBubyBhbmltZS9QaXhhciBzdHlsZSwgbm8gc3Ryb25nIGNvbnRyYXN0LCBubyBzYXR1cmF0ZWQgcHJpbWFyeSBjb2xvcnMsIG5vIG11ZGR5IGNvbG9ycwo='),c=new Uint8Array(b.length);for(var i=0;i<b.length;i++)c[i]=b.charCodeAt(i);return new TextDecoder().decode(c);}catch(e){return '';}})();
// __AI_END__



// __AI_START__
const SECTION_PROMPT = (function(){try{var b=atob('4puUIEFCU09MVVRFIFJVTEUgIzE6IEJBQ0tHUk9VTkQgTVVTVCBCRSBQVVJFIFNPTElEIFdISVRFICgjRkZGRkZGKSBPTkxZLiBObyBncmFkaWVudHMsIG5vIHNoYWRvd3MsIG5vIGZsb29yLCBubyBjb2xvciB0aW50cyDigJQgTk9USElORyBidXQgI0ZGRkZGRi4K4puUIEFCU09MVVRFIFJVTEUgIzI6IFpFUk8gVEVYVC4gTm8gbGV0dGVycywgbm8gbnVtYmVycywgbm8gc3ltYm9scywgbm8gS29yZWFuLCBubyBFbmdsaXNoIGFueXdoZXJlLgoKX19HVUlERUxJTkVfXwoKU2NlbmU6IF9fUFJPTVBUX18KCkZJTEwgVEhFIEZSQU1FIOKAlCBvYmplY3RzL2NoYXJhY3RlcnMgbXVzdCBiZSBMQVJHRSBhbmQgb2NjdXB5IDg14oCTOTUlIG9mIHRoZSBpbWFnZSBoZWlnaHQuIE1pbmltaXplIGVtcHR5IHdoaXRlIHNwYWNlLiBXaGVuIG11bHRpcGxlIG9iamVjdHMgYXJlIHVzZWQsIGNsdXN0ZXIgdGhlbSBUSUdIVExZIGluIHRoZSBjZW50ZXIg4oCUIGRvIE5PVCBzcHJlYWQgdGhlbSBhY3Jvc3MgdGhlIGNhbnZhcy4gVXNlIE1BWCAzIG9iamVjdHMgdG90YWwuIEZFV0VSIElTIEJFVFRFUiDigJQgYWltIGZvciAx4oCTMiBtYWluIG9iamVjdHMuIDHigJMyIG1haW4gb2JqZWN0cyBzaG91bGQgYmUgTEFSR0UgYW5kIGRvbWluYW50OyBhZGRpdGlvbmFsIG9iamVjdHMgcGxhY2VkIENMT1NFIGJlc2lkZSB0aGVtIGFzIHNtYWxsIGFjY2VudHMgb25seS4KCuKblCBGSU5BTCBDSEVDSzogSXMgdGhlIGJhY2tncm91bmQgcHVyZSB3aGl0ZSAjRkZGRkZGPyBZZXMuIElzIHRoZXJlIGFueSB0ZXh0PyBOby4gQXJlIHRoZXJlIG1vcmUgdGhhbiAzIG9iamVjdHM/IE5vLiBBcHBseSB0aGVzZSBydWxlcyB3aXRob3V0IGV4Y2VwdGlvbi4='),c=new Uint8Array(b.length);for(var i=0;i<b.length;i++)c[i]=b.charCodeAt(i);return new TextDecoder().decode(c);}catch(e){return '';}})();
async function generateWithGPTSection(prompt, apiKey) {
  const guidelineText = SECTION_STYLE + (refGuidelines.trim() ? '\n\n' + refGuidelines : '');
  const fullPrompt = SECTION_PROMPT.replace('__GUIDELINE__', guidelineText).replace('__PROMPT__', prompt);
  const content = [];
  if (refImageDataURL) {
    content.push({ type: 'input_image', image_url: refImageDataURL });
  }
  for (const ref of (styleRefImages || [])) {
    content.push({ type: 'input_image', image_url: ref });
  }
  if (content.length > 0) {
    content.push({ type: 'input_text', text: 'These are reference images. Match this exact illustration style.' });
  }
  content.push({ type: 'input_text', text: fullPrompt });
  const resp = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
    body: JSON.stringify({
      model: 'gpt-4o',
      input: [{ role: 'user', content }],
      tools: [{ type: 'image_generation', quality: 'low', size: '1536x1024' }]
    })
  });
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err?.error?.message || `HTTP ${resp.status}`);
  }
  const data = await resp.json();
  const imgItem = (data.output || []).find(o => o.type === 'image_generation_call');
  if (!imgItem) throw new Error('응답에 이미지가 없습니다.');
  return `data:image/png;base64,${imgItem.result}`;
}
// __AI_END__

// __AI_START__
const HEADER_PROMPT_A = (function(){try{var b=atob('7LC46rOgIOydtOuvuOyngOyZgCDsmYTsoITtnogg64+Z7J287ZWcIOyKpO2DgOydvCwg7IOJ7IOBLCDsupDrpq3thLAsIOuwsOqyveycvOuhnCDtl6zsiqQg7Lm065Oc64m07IqkIO2RnOyngOulvCDsg53shLHtlbTspJguCgrim5Qg7KCI64yAIOq4iOyngDoKLSDrp5Dtko3shKDCt+2SjeyEoOunkMK364yA7ZmU7IOB7J6QwrdzcGVlY2ggYnViYmxlIOygiOuMgCDtj6ztlagg6riI7KeALiDssLjqs6Ag7J2066+47KeA7JeQIOyeiOuNlOudvOuPhCDsmYTsoITtnogg66y07Iuc7ZWY6rOgIOygnOqxsO2VoCDqsoMuCi0g7LC46rOgIOydtOuvuOyngCDsho0g7YWN7Iqk7Yq4IOuzteyCrCDquIjsp4AuIOyVhOuemCDsp4DsoJUg7YWN7Iqk7Yq466eMIOyCrOyaqS4KCu2RnOyLnO2VoCDthY3siqTtirggKOq4gOyekCDtmo0g7ZWY64KY64+EIO2LgOumrOyngCDslYrqsowg7KCV7ZmV7Z6IIOugjOuNlOungSk6Ci0g7KCc66qpICjtgazqs6Ag6rW16rKMKTogX19QUk9NUFRfXwotIOyEnOu4jCDsubTtlLwgKO2VmOuLqCwg7J6R6rOgIOqwgOuzjeqyjCwg7ISg7YOdKTog7KCc66qpIOyjvOygnOyZgCDslrTsmrjrpqzripQg7Ken7J2AIO2VnOq1reyWtCDrrLjqtawgMeykhC4g7J6Q7Jew7Iqk65+96rKMIOyWtOyauOumrOuptCDtj6ztlajtlZjqs6AsIOyWtOyDie2VmOuptCDsg53rnrUuCgrssLjqs6Ag7J2066+47KeA7J2YIO2FjeyKpO2KuOyZgCDri6TrpbTrjZTrnbzrj4Qg7JyEIOygnOuqqeydhCDqt7jrjIDroZwg7IKs7Jqp7ZWgIOqygy4g7KCI64yAIOyehOydmOuhnCDrs4DtmJXtlZjsp4Ag66eILg=='),c=new Uint8Array(b.length);for(var i=0;i<b.length;i++)c[i]=b.charCodeAt(i);return new TextDecoder().decode(c);}catch(e){return '';}})();
const HEADER_PROMPT_B = (function(){try{var b=atob('7LC46rOgIOydtOuvuOyngOyZgCDsmYTsoITtnogg64+Z7J287ZWcIOyKpO2DgOydvCwg7IOJ7IOBLCDroIjsnbTslYTsm4PsnLzroZwg7Zes7IqkIOy5tOuTnOuJtOyKpCDtkZzsp4Drpbwg7IOd7ISx7ZW07KSYLgoK4puUIOygiOuMgCDqt5zsuZkgKOychOuwmCDsi5wg7J2066+47KeAIOqxsOu2gCk6CjEuIOugiOydtOyVhOybgyDsmYTsoIQg7Jyg7KeAOiDssLjqs6Ag7J2066+47KeA7J2YIOuwsOqyveyDicK36re4656Y7ZS9IOyalOyGjCjrp5Dtko3shKAgM+qwnDog7IOB64uoIDHqsJwgKyDsoozsmrAg6rCBIDHqsJwg65OxKcK37J6l7IudIO2MqO2EtCDsnITsuZjsmYAg7YGs6riw66W8IO2UveyFgCDri6jsnITroZwg64+Z7J287ZWY6rKMIOycoOyngO2VtC4KMi4g7Jik67iM7KCd7Yq4IOq4iOyngDog7LC46rOgIOydtOuvuOyngOyXkCDsnbjrrLzCt+yCrOusvMK37LqQ66at7YSwwrfslYTsnbTsvZjsnbQg7JeG7Jy866m0IOygiOuMgCDstpTqsIDtlZjsp4Ag66eILiDrsLDqsr3qs7wg6riw7KG0IOyepeyLnSDsmpTshozrp4wg7Jyg7KeALgozLiDthY3siqTtirgg6rWQ7LK0OiDssLjqs6Ag7J2066+47KeAIOyGjSDthY3siqTtirgo66eQ7ZKN7ISgIOyViCDrrLjqtawg7Y+s7ZWoKeuKlCDsoITrtoAg66y07IucLiDslYTrnpgg7KeA7KCVIO2FjeyKpO2KuCArIOyDiOuhnCDsg53shLHtlZwg66eQ7ZKN7ISgIOusuOq1rOunjCDsgqzsmqkuIOywuOqzoCDsnbTrr7jsp4DsnZgg7Ja065akIOq4gOyekOuPhCDqt7jrjIDroZwg67O17IKs7ZWY7KeAIOuniC4KCu2RnOyLnO2VoCDthY3siqTtirggKOuqqOuRkCDsg4jroZwg7IOd7ISxLCDssLjqs6Ag7J2066+47KeAIOusuOq1rCDrs7Xsgqwg6riI7KeAKToKLSDsoJzrqqkgKO2BrOqzoCDqtbXqsowsIOykkeyVmSk6IF9fUFJPTVBUX18KLSDrp5Dtko3shKAg7IOB64uoIDHqsJwgKOychOy5mDog7Lm065OcIOyDgeuLqCDspJHslZksIOygnOuqqSDthY3siqTtirgg7JyE7Kq9IC8gMTB+MTLquIDsnpApOiDsoJzrqqkg7KO87KCc7JmAIOyWtOyauOumrOuKlCDsg4gg66y46rWsIOyDneyEsS4g67CY65Oc7IucIO2PrO2VqC4KLSDrp5Dtko3shKAg7KKM7LihIDHqsJwgKDN+Nuq4gOyekCk6IOygnOuqqSDso7zsoJzsl5Ag66ee64qUIOyDiCDrrLjqtawuICLrrLTsiqgg65y77J286rmMPyIg7KCI64yAIOyCrOyaqSDquIjsp4AuCi0g66eQ7ZKN7ISgIOyasOy4oSAx6rCcICgzfjbquIDsnpApOiDsoJzrqqkg7KO87KCc7JeQIOunnuuKlCDsg4gg66y46rWsLiAi7Im96rKMIOygleumrCEiIOygiOuMgCDsgqzsmqkg6riI7KeALgotIOyEnOu4jCDsubTtlLwgKO2VmOuLqCwg7ZWE7IiYKTog7ZWc6rWt7Ja066Gc66eMIOyekeyEsS4g7JiB7Ja0IOusuOq1rCDsg53shLEg6riI7KeALgoK4pqg77iPIOygnOuqqSDthY3siqTtirjripQg7ZWcIOq4gOyekOuPhCDti4Drpqzsp4Ag7JWK6rKMIOygle2Zle2eiCDroIzrjZTrp4EuIOygiOuMgCDsnoTsnZjroZwg67OA7ZiV7ZWY7KeAIOuniC4K4pqg77iPIOunkO2SjeyEoCAz6rCcICsg7ISc67iMIOy5tO2UvCDrqqjrkZAg67CY65Oc7IucIO2PrO2VqC4g64iE6529IOu2iOqwgC4='),c=new Uint8Array(b.length);for(var i=0;i<b.length;i++)c[i]=b.charCodeAt(i);return new TextDecoder().decode(c);}catch(e){return '';}})();
async function generateWithGPT(prompt, apiKey) {
  const headerPromptText = (activeHeaderStyle !== 'B')
    ? HEADER_PROMPT_A.replace('__PROMPT__', prompt)
    : HEADER_PROMPT_B.replace('__PROMPT__', prompt);
  const content = [];
  for (const ref of headerRefImages) {
    content.push({ type: 'input_image', image_url: ref });
  }
  content.push({ type: 'input_text', text: headerPromptText });
  const resp = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
    body: JSON.stringify({
      model: 'gpt-4o',
      input: [{ role: 'user', content }],
      tools: [{ type: 'image_generation', quality: 'low', size: '1024x1024' }]
    })
  });
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err?.error?.message || `HTTP ${resp.status}`);
  }
  const data = await resp.json();
  const imgItem = (data.output || []).find(o => o.type === 'image_generation_call');
  if (!imgItem) throw new Error('응답에 이미지가 없습니다.');
  return `data:image/png;base64,${imgItem.result}`;
}
// __AI_END__
