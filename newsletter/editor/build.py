"""뉴스레터 이미지 편집기 배포본 만들기: index.html + 썸네일 도구의 라이브러리·폰트·로고를 HTML 한 파일로 합친다.

실행: python3 build.py  →  dist/image-editor.html (이름 고정 · 인터넷 없이 동작)
"""
import base64
import os
import re

VERSION = '1.5'
HERE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.join(HERE, '..', 'thumbnail')


def read(path, mode='r'):
    with open(path, mode, **({} if 'b' in mode else {'encoding': 'utf-8'})) as f:
        return f.read()


def inline_script(code):
    return '<script>' + code.replace('</script', '<\\/script') + '</script>'


html = read(os.path.join(HERE, 'index.html'))

faces = ''.join(
    "@font-face{font-family:Pretendard;font-weight:%d;font-display:block;"
    "src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, base64.b64encode(read(os.path.join(SHARED, 'vendor', f'Pretendard-{n}.woff2'), 'rb')).decode())
    for w, n in [(400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold')]
)
replacements = [
    (r'<link rel="stylesheet" href="[^"]*pretendard[^"]*">', '<style>' + faces + '</style>'),
    (r'<script src="[^"]*html2canvas[^"]*"></script>', inline_script(read(os.path.join(SHARED, 'vendor', 'html2canvas.min.js')))),
    (r'<script src="[^"]*lucide[^"]*"></script>', inline_script(read(os.path.join(SHARED, 'vendor', 'lucide.min.js')))),
    (r'<script src="\.\./thumbnail/assets\.js"></script>', inline_script(read(os.path.join(SHARED, 'assets.js')))),
    (r'<script src="assets-editor\.js"></script>', inline_script(read(os.path.join(HERE, 'assets-editor.js')))),
]
for pattern, repl in replacements:
    html, n = re.subn(pattern, lambda m: repl, html)
    assert n == 1, f'치환 실패: {pattern}'

html = html.replace('<title>뉴스레터 이미지 만들기</title>', f'<title>뉴스레터 이미지 만들기 v{VERSION}</title>')
os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
out = os.path.join(HERE, 'dist', 'image-editor.html')   # 이름 고정
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'{out}  ({os.path.getsize(out) // 1024} KB)')
