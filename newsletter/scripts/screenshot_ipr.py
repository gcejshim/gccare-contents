from playwright.sync_api import sync_playwright
from PIL import Image
import os

MAX_BYTES = 1 * 1024 * 1024  # 1MB

def optimize_png(path):
    size = os.path.getsize(path)
    if size <= MAX_BYTES:
        return
    # 1단계: Pillow 무손실 최대 압축
    img = Image.open(path)
    img.save(path, optimize=True, compress_level=9)
    size = os.path.getsize(path)
    if size <= MAX_BYTES:
        return
    # 2단계: 여전히 초과면 이미지 크기를 단계적으로 축소
    scale = 0.85
    while size > MAX_BYTES and scale > 0.5:
        w = int(img.width * scale)
        h = int(img.height * scale)
        resized = img.resize((w, h), Image.LANCZOS)
        resized.save(path, optimize=True, compress_level=9)
        size = os.path.getsize(path)
        scale -= 0.05

FOLDER = '202607_뉴스레터'
ROOT   = '/Users/ejshim/Documents/gccare/콘텐츠통합/뉴스레터'
OUTPUT = f'{ROOT}/{FOLDER}'
BASE   = f'file://{ROOT}/{FOLDER}/html'

# (html파일명, 출력 prefix, 번호)
# 출력 파일명: {prefix}_{버전}{번호}.png  →  예: 202607_contents02_p01.png
charts = [
    ('202607_contents02_pc01.html', '202607_contents02', '01'),
    ('202607_contents02_pc02.html', '202607_contents02', '02'),
    ('202607_contents01_pc03.html', '202607_contents01', '03'),
]

VIEWPORTS = [
    ('p', 920, 900, 2),   # PC·메일 공용 900px
    ('m', 390, 844, 3),   # 모바일 390px
]

with sync_playwright() as p:
    browser = p.chromium.launch()

    for html_file, prefix, num in charts:
        url = f'{BASE}/{html_file}'

        for suffix, width, height, dpr in VIEWPORTS:
            page = browser.new_page(
                viewport={'width': width, 'height': height},
                device_scale_factor=dpr,
            )
            page.goto(url, wait_until='networkidle')
            page.wait_for_timeout(500)

            el = page.query_selector('.wrap')
            out_name = f'{prefix}_{suffix}{num}.png'
            out_path = os.path.join(OUTPUT, out_name)
            el.screenshot(path=out_path)
            optimize_png(out_path)
            size_kb = os.path.getsize(out_path) // 1024
            print(f'✅ {out_name} 저장 완료 ({size_kb}KB)')
            page.close()

    browser.close()
