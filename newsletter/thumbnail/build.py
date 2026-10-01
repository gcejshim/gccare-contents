"""썸네일 도구 배포본 만들기: index.html + assets.js + 라이브러리 + 폰트를 HTML 한 파일로 합친다.

실행: python3 build.py  →  dist/thumbnail.html (이름 고정)
"""
import base64
import os
import re

VERSION = '1.2'
HERE = os.path.dirname(os.path.abspath(__file__))


def read(path, mode='r'):
    with open(os.path.join(HERE, path), mode, **({} if 'b' in mode else {'encoding': 'utf-8'})) as f:
        return f.read()


def inline_script(code):
    return '<script>' + code.replace('</script', '<\\/script') + '</script>'


html = read('index.html')

faces = ''.join(
    "@font-face{font-family:Pretendard;font-weight:%d;font-display:block;"
    "src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, base64.b64encode(read(f'vendor/Pretendard-{n}.woff2', 'rb')).decode())
    for w, n in [(400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold')]
)
replacements = [
    (r'<link rel="stylesheet" href="[^"]*pretendard[^"]*">', '<style>' + faces + '</style>'),
    (r'<script src="[^"]*html2canvas[^"]*"></script>', inline_script(read('vendor/html2canvas.min.js'))),
    (r'<script src="[^"]*lucide[^"]*"></script>', inline_script(read('vendor/lucide.min.js'))),
    (r'<script src="assets.js"></script>', inline_script(read('assets.js'))),
]
for pattern, repl in replacements:
    html, n = re.subn(pattern, lambda m: repl, html)
    assert n == 1, f'치환 실패: {pattern}'

html = html.replace('<title>뉴스레터 썸네일 만들기</title>', f'<title>뉴스레터 썸네일 만들기 v{VERSION}</title>')
os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
out = os.path.join(HERE, 'dist', 'thumbnail.html')   # 이름 고정
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'{out}  ({os.path.getsize(out) // 1024} KB)')
