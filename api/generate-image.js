// Vercel 서버리스 함수 — 카드뉴스 편집기(04번)의 AI 이미지 생성 프록시
// 프롬프트 원문과 회사 공용 OpenAI API 키는 전부 환경변수(process.env)에만 있고,
// 이 코드가 올라간 깃허브 저장소에는 절대 값이 노출되지 않는다.

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
  if (!imgItem) throw new Error('OpenAI 응답에 이미지가 없습니다.');
  return `data:image/png;base64,${imgItem.result}`;
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
    res.status(500).json({ error: e.message || String(e) });
  }
};
