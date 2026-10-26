"""AX Studio · Newsletter(메뉴 셸) 배포본: 셸 + 썸네일 도구 + 콘텐츠 이미지 편집기 + 라이브러리 + 폰트 + 샘플을 HTML 한 파일로 합친다.

폰트 · 라이브러리는 한 번만 넣고, 실행할 때 blob 주소로 만들어 두 도구(iframe)가 같이 쓴다 → 파일 크기를 줄임.
실행: python3 build.py  →  dist/gccare-insight-studio.html (이름 고정 · 인터넷 없이 동작)
"""
import base64, json, os, re

VERSION = '1.0'
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TH = os.path.join(ROOT, 'thumbnail'); ED = os.path.join(ROOT, 'editor')


def read(p, mode='r'):
    with open(p, mode, **({} if 'b' in mode else {'encoding': 'utf-8'})) as f:
        return f.read()


def sub1(pattern, repl, html, label):
    html, n = re.subn(pattern, lambda m: repl, html)
    assert n == 1, f'치환 실패({label}): {pattern}'
    return html


def tool(path, extra=(), h2c=True):
    h = read(path)
    h = sub1(r'<link rel="stylesheet" href="[^"]*pretendard[^"]*">', '<style>__NL_FONTFACE__</style>', h, path)
    h = re.sub(r'<link rel="stylesheet" href="[^"]*oswald\.css">\n?', '', h)   # 포인트 글꼴은 __NL_FONTFACE__에 들어 있음
    if h2c: h = sub1(r'<script src="[^"]*html2canvas[^"]*"></script>', '<script src="__NL_LIB_h2c__"></script>', h, path)
    h = sub1(r'<script src="[^"]*lucide[^"]*"></script>', '<script src="__NL_LIB_lucide__"></script>', h, path)
    h = sub1(r'<script src="[^"]*assets\.js"></script>', '<script src="__NL_LIB_assets__"></script>', h, path)
    for pat, key in extra: h = sub1(pat, f'<script src="__NL_LIB_{key}__"></script>', h, path)
    return h


tools = {
    'thumb': tool(os.path.join(TH, 'index.html'), [(r'<script src="refs\.js"></script>', 'refs')]),
    'image': tool(os.path.join(ED, 'index.html'), [(r'<script src="assets-editor\.js"></script>', 'assetsEd'), (r'<script src="[^"]*gifenc[^"]*"></script>', 'gifenc')]),   # gifenc: 콘텐츠 이미지 [GIF로 저장]
    'pdf': tool(os.path.join(ROOT, 'pdf', 'index.html'), [(r'<script src="styles\.js"></script>', 'pdfStyles'), (r'<script src="examples\.js"></script>', 'pdfEx'), (r'<script src="moods\.js"></script>', 'pdfMoods')]),   # html2canvas는 이번 호 화면의 작은 표지 미리보기용
}
libs = {
    'h2c': read(os.path.join(TH, 'vendor', 'html2canvas.min.js')),
    'lucide': read(os.path.join(TH, 'vendor', 'lucide.min.js')),
    'gifenc': read(os.path.join(TH, 'vendor', 'gifenc.js')),
    'assets': read(os.path.join(TH, 'assets.js')),
    'assetsEd': read(os.path.join(ED, 'assets-editor.js')),
    'refs': read(os.path.join(TH, 'refs.js')),   # 썸네일 참고 이미지 (썸네일 도구 · 에셋 › 배경 이미지)
    'samples': read(os.path.join(HERE, 'samples.js')),
    'pdfStyles': read(os.path.join(ROOT, 'pdf', 'styles.js')),   # 리드마그넷 그림체 샘플 (PDF 도구 · 에셋 › 배경 이미지)
    'pdfEx': read(os.path.join(ROOT, 'pdf', 'examples.js')),
    'pdfMoods': read(os.path.join(ROOT, 'pdf', 'moods.js')),     # 리드마그넷 분위기 보기 (pdf/make_moods.py)     # 리드마그넷 예시 · 표지 그림 (pdf/make_examples.py)
}
fonts = {w: base64.b64encode(read(os.path.join(TH, 'vendor', f'Pretendard-{n}.woff2'), 'rb')).decode() for w, n in [('400', 'Regular'), ('500', 'Medium'), ('600', 'SemiBold'), ('700', 'Bold'), ('800', 'ExtraBold'), ('900', 'Black')]}
fonts['oswald'] = base64.b64encode(read(os.path.join(TH, 'vendor', 'Oswald-Variable.woff2'), 'rb')).decode()   # 포인트 글꼴 (세로로 긴 숫자 · 영문, 2026-10-20)

BOOT = r"""
(function(){
  const D = window.__NL_DATA; const urls = {};
  const blob = (s, type) => URL.createObjectURL(new Blob([s], {type}));
  const bin = b64 => { const s = atob(b64), a = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; };
  const font = {}; Object.keys(D.fonts).forEach(w => { font[w] = URL.createObjectURL(new Blob([bin(D.fonts[w])], {type: 'font/woff2'})); });
  Object.keys(D.libs).forEach(k => { urls[k] = blob(D.libs[k], 'text/javascript'); });
  const faces = [[400, '400'], [500, '500'], [600, '600'], [700, '700'], [800, '800'], [900, '900']].map(([w, f]) => `@font-face{font-family:Pretendard;font-weight:${w};font-display:block;src:url(${font[f]}) format('woff2')}`).join('')
    + `@font-face{font-family:Oswald;font-weight:200 700;font-display:block;src:url(${font.oswald}) format('woff2')}`;
  const load = src => new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); });
  window.NL_PACK = {
    version: D.version,
    toolHTML(k){ return D.tools[k].replace('__NL_FONTFACE__', faces).replace(/__NL_LIB_(\w+)__/g, (_, n) => urls[n]); },
    async boot(){
      const st = document.createElement('style'); st.textContent = faces; document.head.appendChild(st);
      for (const k of ['lucide', 'assets', 'assetsEd', 'samples', 'refs', 'pdfStyles', 'pdfEx', 'pdfMoods']) await load(urls[k]);
      try { await document.fonts.load('700 16px Pretendard'); } catch(e){}
    }
  };
})();
"""

shell = read(os.path.join(HERE, 'index.html'))
shell = sub1(r'<link rel="stylesheet" href="[^"]*pretendard[^"]*">\n', '', shell, 'shell font')
for pat in [r'<script src="[^"]*lucide[^"]*"></script>\n', r'<script src="\.\./thumbnail/assets\.js"></script>\n', r'<script src="\.\./editor/assets-editor\.js"></script>\n', r'<script src="\.\./thumbnail/refs\.js"></script>\n',r'<script src="samples\.js"></script>\n', r'<script src="\.\./pdf/styles\.js"></script>\n', r'<script src="\.\./pdf/examples\.js"></script>\n', r'<script src="\.\./pdf/moods\.js"></script>\n']:
    shell = sub1(pat, '', shell, 'shell lib')
data = json.dumps({'version': VERSION, 'tools': tools, 'libs': libs, 'fonts': fonts}, ensure_ascii=False).replace('<', '\\u003c')
# 기본 호: 처음 여는 브라우저에 채워 줄 최신 완성 호 (issues/NN/work/*_전체.json)
DEFAULT_ISSUE = os.path.join(ROOT, 'issues', '15', 'work', '202610_뉴스레터_15호_전체.json')
default_issue = read(DEFAULT_ISSUE).replace('<', '\\u003c')
pack = '<script>window.__NL_DATA=' + data + ';</script>\n<script>window.NL_DEFAULT_ISSUE=' + default_issue + ';</script>\n<script>' + BOOT + '</script>\n'
shell = shell.replace('</head>', pack + '</head>', 1)
shell = shell.replace('<title>AX Studio · Newsletter</title>', f'<title>AX Studio · Newsletter v{VERSION}</title>')
os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
out = os.path.join(HERE, 'dist', 'gccare-insight-studio.html')   # 이름 고정 (버전은 파일 안 · README에서 관리)
with open(out, 'w', encoding='utf-8') as f: f.write(shell)
print(f'{out}  ({os.path.getsize(out) // 1024} KB)')
