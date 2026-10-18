// Vercel 서버리스 함수 — 카드뉴스 편집기(04번)의 AI 이미지 생성 프록시
// 프롬프트 원문과 회사 공용 OpenAI API 키는 전부 환경변수(process.env)에만 있고,
// 이 코드가 올라간 깃허브 저장소에는 절대 값이 노출되지 않는다.

// 이미지 생성이 40초 정도 걸리므로 함수 실행 시간 제한을 늘려둠
// (Hobby 플랜에서는 이 값이 무시되고 여전히 짧게 제한될 수 있음 — 실제 배포 후 테스트 필요)
module.exports.config = { maxDuration: 60 };

const IMAGE_MODEL = 'gpt-image-2';

async function callOpenAIImage({ apiKey, content, size, background, quality = 'low' }) {
  const resp = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'gpt-4o',
      input: [{ role: 'user', content }],
      // 이미지 모델은 직접 지정 (gpt-image-1은 2026-10-23 종료 → gpt-image-2. 투명 배경은 gpt-image-2 미리보기 기능)
      // 투명 배경은 gpt-image-2에서 'not supported' (2026-10-18 시험) → 썸네일 오브젝트형(투명)은 도구에서 뺌
      tools: [{ type: 'image_generation', model: IMAGE_MODEL, quality, size, ...(background ? { background } : {}) }]
    })
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err?.error?.message || `OpenAI 호출 실패 (${resp.status})`);
  }

  const data = await resp.json();
  const imgItem = (data.output || []).find((o) => o.type === 'image_generation_call');
  if (!imgItem) {
    // 디버그용: 실제 응답에 어떤 항목이 왔는지 보여줌 (프롬프트 원문은 응답에 없으므로 노출 안 됨)
    const types = (data.output || []).map((o) => o.type + (o.status ? `(${o.status})` : ''));
    const refusal = (data.output || []).find((o) => o.type === 'message')
      ?.content?.map((c) => c.text || c.refusal).filter(Boolean).join(' | ');
    throw new Error(`OpenAI 응답에 이미지가 없습니다. output types: [${types.join(', ')}]${refusal ? ' / message: ' + refusal : ''}`);
  }
  return `data:image/png;base64,${imgItem.result}`;
}

// 진단용 — Vercel 복호화 시 실제 확인된 글자 수 (실제 값은 노출 안 함, 길이만 비교)
const EXPECTED_LEN = {
  SECTION_STYLE: 2025,
  SECTION_PROMPT: 840,
  SECTION_GUIDELINE_MALE: 126,
  SECTION_GUIDELINE_FEMALE: 182,
  HEADER_PROMPT_A: 535,
  HEADER_PROMPT_B: 788
};
function checkEnvLengths(keys) {
  return keys.map((k) => `${k}=${(process.env[k] || '').length}/${EXPECTED_LEN[k]}`).join(', ');
}

function buildSectionContent({ prompt, gender, styleRefImages, refImageDataURL }) {
  const guideline = gender === 'female'
    ? process.env.SECTION_GUIDELINE_FEMALE || ''
    : process.env.SECTION_GUIDELINE_MALE || '';
  const guidelineText = (process.env.SECTION_STYLE || '') + (guideline.trim() ? '\n\n' + guideline : '');
  const fullPrompt = (process.env.SECTION_PROMPT || '')
    .replace('__GUIDELINE__', guidelineText)
    .replace('__PROMPT__', prompt);

  const content = [];
  if (refImageDataURL) content.push({ type: 'input_image', image_url: refImageDataURL });
  for (const ref of (styleRefImages || [])) content.push({ type: 'input_image', image_url: ref });
  if (content.length > 0) {
    content.push({ type: 'input_text', text: 'These are reference images. Match this exact illustration style.' });
  }
  content.push({ type: 'input_text', text: fullPrompt });
  return content;
}

function buildHeaderContent({ prompt, activeHeaderStyle, headerRefImages }) {
  // A1 스타일도 HEADER_PROMPT_A를 재사용 (원본 로직: activeHeaderStyle !== 'B' → A)
  const template = activeHeaderStyle === 'B'
    ? (process.env.HEADER_PROMPT_B || '')
    : (process.env.HEADER_PROMPT_A || '');
  const headerPromptText = template.replace('__PROMPT__', prompt);

  const content = [];
  for (const ref of (headerRefImages || [])) content.push({ type: 'input_image', image_url: ref });
  content.push({ type: 'input_text', text: headerPromptText });
  return content;
}

// 뉴스레터 썸네일 [바로 만들기] — 프롬프트는 썸네일 도구가 짜서 화면에 보여 주고(ChatGPT 복사용과 같은 내용) 그대로 받는다.
// charRefs: 프롬프트에 '첨부한 캐릭터'로 적힌 카드뉴스 편집기 캐릭터 이미지 (최대 2장)
const isSmallImage = (u) => /^data:image\/(webp|png|jpeg);base64,/.test(u || '') && u.length < 500000;
// styleRef: 프롬프트에 '첨부한 참고 이미지'로 적힌 지난 호 썸네일 배경 (글자 뺀 것, 1장) — 그림체 · 배치만 참고
// styleRefMine: 사용자가 직접 넣은 참고 이미지 → 그릴 대상이 그 안에 있으면 모양까지 참고 허용 (2026-10-18)
function buildThumbContent({ prompt, charRefs, styleRef, styleRefMine }) {
  const chars = (Array.isArray(charRefs) ? charRefs : []).filter(isSmallImage).slice(0, 2);
  const ref = isSmallImage(styleRef) ? styleRef : '';
  const content = [];
  if (ref) content.push({ type: 'input_image', image_url: ref });
  chars.forEach((u) => content.push({ type: 'input_image', image_url: u }));
  let note = '';
  if (ref) note += styleRefMine
    ? '\n\n(The first attached image is the reference the user attached, referred to as "첨부한 참고 이미지" above. Follow its rendering style, materials, lighting and composition. If the requested subject appears in it, you may follow its shape. Do not copy its logos or text.)'
    : '\n\n(The first attached image is the style reference referred to as "첨부한 참고 이미지" above. Use it for composition, layout and color mood only — follow the rendering style described in the prompt (premium studio-shot 3D), and do not copy its objects, people or text.)';
  if (chars.length) note += `\n\n(The ${ref ? 'next' : 'attached'} image(s) are our brand characters referred to as "첨부한 캐릭터" above, in the same order. Use only their faces and hairstyles.)`;
  // 2026-10-18: 신문 · 머그컵 등에 영어가 자꾸 나옴 → 적은 글자 말고는 글자 금지, 특히 영어
  note += '\n\n(TEXT RULE: Render no text except the exact words the prompt explicitly asks for, written exactly as given — Korean stays Korean Hangul. Never invent English or any Latin-letter headlines, labels or body text on newspapers, documents, mugs or signs; draw gray lines instead.)';
  content.push({ type: 'input_text', text: prompt + note });
  return content;
}

// 썸네일 · AI로 그리기 [고치기] — 지금 이미지를 그대로 두고 적은 부분만 바꿈 (2026-10-18)
// image: 고칠 이미지(data URL, 도구에서 긴 쪽 1536px로 줄여 보냄), prompt: 바꿀 점 한 줄
const isEditImage = (u) => /^data:image\/(webp|png|jpeg);base64,/.test(u || '') && u.length < 4000000;
// ref: 수정할 때 같이 붙인 참고 이미지(선택)
function buildEditContent({ prompt, image, ref }) {
  const hasRef = isEditImage(ref);
  return [
    { type: 'input_image', image_url: image },
    ...(hasRef ? [{ type: 'input_image', image_url: ref }] : []),
    { type: 'input_text', text:
      `Edit the first attached image. Change only this: ${prompt}\n\n` +
      (hasRef ? 'The second attached image is a reference the user attached for this change ("참고 이미지"). Use it only for what the request asks (shape, color, style or layout). Do not copy its logos or text.\n\n' : '') +
      'Keep everything else exactly the same — composition, camera angle, object positions and sizes, colors, lighting, rendering style and the background color. ' +
      'Any changed or newly added object must match the main object: same camera angle and perspective, proportional size (supporting objects about 30-50% of the main object), same lighting direction, and sit on the same floor with a soft contact shadow — the result must look like one coherent scene, not stickers. ' +
      'Keep the left side empty for a headline. Do not add new text; keep any existing Korean text exactly as it is unless the request says otherwise. Never add English or Latin-letter text unless the request explicitly asks for those exact words. ' +
      'Output the full edited image at the same aspect ratio.' }
  ];
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'POST만 허용됩니다.' });
    return;
  }

  try {
    const body = req.body || {};
    const { kind, prompt, apiKey } = body;
    if (!prompt || !prompt.trim()) {
      res.status(400).json({ error: '프롬프트가 비어있습니다.' });
      return;
    }

    const effectiveKey = (apiKey && apiKey.trim()) ? apiKey.trim() : process.env.OPENAI_API_KEY;
    if (!effectiveKey) {
      res.status(500).json({ error: '서버에 OpenAI API 키가 설정되어 있지 않습니다.' });
      return;
    }

    let content, size, background, quality;
    if (kind === 'thumb') {
      content = buildThumbContent(body);
      quality = 'medium';   // 2026-10-18 사용자: 세련되게 — low는 재질이 뭉개짐 (가로형 장당 약 $0.041)
      size = body.layout === 'object' ? '1024x1024' : '1536x1024';
      if (body.layout === 'object') background = 'transparent';
    } else if (kind === 'edit') {
      if (!isEditImage(body.image)) {
        res.status(400).json({ error: '고칠 이미지가 없거나 너무 커요.' });
        return;
      }
      content = buildEditContent(body);
      quality = 'medium';   // 썸네일과 같은 품질
      size = '1536x1024';
    } else if (kind === 'header') {
      content = buildHeaderContent(body);
      size = '1024x1024';
    } else if (kind === 'section') {
      content = buildSectionContent(body);
      size = '1536x1024';
    } else {
      res.status(400).json({ error: `알 수 없는 kind: ${kind}` });
      return;
    }

    const dataURL = await callOpenAIImage({ apiKey: effectiveKey, content, size, background, quality });
    res.status(200).json({ dataURL });
  } catch (e) {
    // 디버그용: 어떤 키(개인/회사)가 쓰였는지 끝 4자리만 노출 (전체 키는 절대 노출 안 함)
    const usedKey = (req.body && req.body.apiKey && req.body.apiKey.trim())
      ? `개인 키 (...${req.body.apiKey.trim().slice(-4)})`
      : `회사 공용키 (...${(process.env.OPENAI_API_KEY || '').slice(-4)})`;
    const kind = req.body && req.body.kind;
    const envKeys = kind === 'header'
      ? ['HEADER_PROMPT_A', 'HEADER_PROMPT_B']
      : ['SECTION_STYLE', 'SECTION_PROMPT', 'SECTION_GUIDELINE_MALE', 'SECTION_GUIDELINE_FEMALE'];
    const envInfo = kind === 'thumb' || kind === 'edit' ? '' : ` [env 글자수(실제/기대): ${checkEnvLengths(envKeys)}]`;
    res.status(500).json({ error: `[사용된 키: ${usedKey}]${envInfo} ` + (e.message || String(e)) });
  }
};
