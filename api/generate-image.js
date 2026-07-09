// Vercel 서버리스 함수 — 카드뉴스 편집기(04번)의 AI 이미지 생성 프록시
// 프롬프트 원문과 회사 공용 OpenAI API 키는 전부 환경변수(process.env)에만 있고,
// 이 코드가 올라간 깃허브 저장소에는 절대 값이 노출되지 않는다.

// 이미지 생성이 40초 정도 걸리므로 함수 실행 시간 제한을 늘려둠
// (Hobby 플랜에서는 이 값이 무시되고 여전히 짧게 제한될 수 있음 — 실제 배포 후 테스트 필요)
module.exports.config = { maxDuration: 60 };

async function callOpenAIImage({ apiKey, content, size }) {
  const resp = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'gpt-4o',
      input: [{ role: 'user', content }],
      tools: [{ type: 'image_generation', quality: 'low', size }]
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

    let content, size;
    if (kind === 'header') {
      content = buildHeaderContent(body);
      size = '1024x1024';
    } else if (kind === 'section') {
      content = buildSectionContent(body);
      size = '1536x1024';
    } else {
      res.status(400).json({ error: `알 수 없는 kind: ${kind}` });
      return;
    }

    const dataURL = await callOpenAIImage({ apiKey: effectiveKey, content, size });
    res.status(200).json({ dataURL });
  } catch (e) {
    // 디버그용: 어떤 키(개인/회사)가 쓰였는지 끝 4자리만 노출 (전체 키는 절대 노출 안 함)
    const usedKey = (req.body && req.body.apiKey && req.body.apiKey.trim())
      ? `개인 키 (...${req.body.apiKey.trim().slice(-4)})`
      : `회사 공용키 (...${(process.env.OPENAI_API_KEY || '').slice(-4)})`;
    const envKeys = (req.body && req.body.kind === 'header')
      ? ['HEADER_PROMPT_A', 'HEADER_PROMPT_B']
      : ['SECTION_STYLE', 'SECTION_PROMPT', 'SECTION_GUIDELINE_MALE', 'SECTION_GUIDELINE_FEMALE'];
    res.status(500).json({ error: `[사용된 키: ${usedKey}] [env 글자수(실제/기대): ${checkEnvLengths(envKeys)}] ` + (e.message || String(e)) });
  }
};
