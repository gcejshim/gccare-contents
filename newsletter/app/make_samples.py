"""10~14호 완성 이미지를 작은 미리보기(JPG)로 줄여 samples.js로 만든다. 에셋 › 샘플 모아보기에서 사용.

실행: python3 make_samples.py  (새 호가 끝나면 TYPES에 분류를 추가하고 다시 실행)
"""
import base64, io, json, os, re, unicodedata
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))   # 뉴스레터/
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples.js')
W = 480

# 블록 유형 분류 (뉴스레터 이미지 패턴 분석 결과). 키: 'YYYYMM_contentsNN_pNN'
TYPES = {
    '202605_contents01_p01': 'hbar', '202605_contents01_p02': 'stack', '202605_contents01_p03': 'hbar',
    '202605_contents02_p01': 'hero', '202605_contents02_p02': 'quote', '202605_contents02_p03': 'hero', '202605_contents02_p04': 'hero',
    '202606_contents01_p01': 'vbar', '202606_contents01_p02': 'vbar', '202606_contents01_p03': 'hbar',
    '202606_contents01_p04': 'photo', '202606_contents01_p05': 'photo', '202606_contents01_p06': 'photo',
    '202606_contents02_p01': 'flow', '202606_contents02_p02': 'quote', '202606_contents02_p03': 'table',
    '202606_contents03_p01': 'table', '202606_contents03_p02': 'table', '202606_contents03_p03': 'table',
    '202607_contents01_p01': 'illust', '202607_contents01_p02': 'line', '202607_contents01_p03': 'list',
    '202607_contents02_p01': 'line', '202607_contents02_p02': 'list',
    '202608_contents01_p01': 'list', '202608_contents01_p02': 'compare', '202608_contents01_p03': 'table',
    '202608_contents02_p01': 'rank', '202608_contents02_p02': 'rank', '202608_contents02_p03': 'rank',
    '202609_contents02_p01': 'steps', '202609_contents02_p02': 'hero',
}
ISSUE = {'202605': 10, '202606': 11, '202607': 12, '202608': 13, '202609': 14}


def thumb(path, w=W):
    im = Image.open(path)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3]); im = bg
    else:
        im = im.convert('RGB')
    h = round(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=70, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode(), im.size, im0size(path)


def im0size(path):
    with Image.open(path) as im: return im.size


items = []
for ym, issue in ISSUE.items():
    d = os.path.join(ROOT, f'{ym}_뉴스레터')
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        f = unicodedata.normalize('NFC', f)
        p = os.path.join(d, f) if os.path.exists(os.path.join(d, f)) else os.path.join(d, unicodedata.normalize('NFD', f))
        m = re.match(r'^(\d{6}_contents\d\d_p\d\d)\.png$', f)
        if m and m.group(1) in TYPES:
            src, size, orig = thumb(p)
            items.append({'issue': issue, 'ym': ym, 'name': f, 'type': TYPES[m.group(1)], 'w': orig[0], 'h': orig[1], 'src': src})
            continue
        m = re.match(r'^\((\d+)호\)(\d\d)(?:_\d)?\.(.+)\.png$', f)
        if m:
            src, size, orig = thumb(p, 400)
            items.append({'issue': int(m.group(1)), 'ym': ym, 'name': f, 'type': 'thumb', 'title': m.group(3), 'w': orig[0], 'h': orig[1], 'src': src})

with open(OUT, 'w', encoding='utf-8') as fp:
    fp.write('window.NL_SAMPLES = ' + json.dumps(items, ensure_ascii=False) + ';\n')
print(f'{OUT}  {len(items)}장  {os.path.getsize(OUT) // 1024} KB')
from collections import Counter; print(Counter(i['type'] for i in items))
