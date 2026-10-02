"""10~14호 완성 이미지를 미리보기(WebP)로 줄여 samples.js로 만든다. 에셋 › 샘플 모아보기에서 사용.

실행 (둘 중 하나)
  python3 make_samples.py                 회사 PC의 월별 폴더(YYYYMM_뉴스레터)에서 납품 PNG를 읽음
  python3 make_samples.py --figma DIR     Figma 내보내기(2배 PNG, 파일명 = 노드 ID '2387-2550.png')를 읽음
                                          FIGMA에 없는 이미지와 DIR에 없는 이미지는 지금 samples.js 것을 그대로 둠
새 호가 끝나면 TYPES(와 FIGMA)에 추가하고 다시 실행.

인코딩: WebP (cwebp -sharp_yuv, 없으면 Pillow). 콘텐츠 폭 1200 · q60, 썸네일 798 · q70 (2배)
  → 폭 600(1배)은 크게 보기에서 글자가 깨져 2배로 저장. 해상도가 높아 q60이어도 글자가 선명함
"""
import argparse, base64, io, json, os, re, shutil, subprocess, tempfile, unicodedata
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))   # 뉴스레터/
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples.js')
W, Q = 1200, 60             # 콘텐츠 이미지 (크게 보기 창 약 1000px에서도 선명하도록 2배)
TW, TQ = 798, 70            # 썸네일 2배 (399×231 → 798×462)

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

# 샘플 이름 → Figma 노드 (파일 i8zSUqXOiTr7xsrPknMPc7, 페이지 'GC뉴스레터 산출물 2026'). 2026-10-02 확인
# 빠진 것: 202606_contents01_p03(납품본은 Chart.js 캡처라 Figma에 없음, 같은 이름 프레임은 KB 사진),
#          202606_contents02_p01(Figma는 이후 수정된 디자인이라 납품본과 다름)
FIGMA = {
    '(10호)01.데이터 리포트.png': '2190:7982', '(10호)02.보건이지 솔루션 소개.png': '2190:8014',
    '202605_contents01_p01.png': '2201:2987', '202605_contents01_p02.png': '2228:1883', '202605_contents01_p03.png': '2228:1884',
    '202605_contents02_p01.png': '2182:4831', '202605_contents02_p02.png': '2182:5826', '202605_contents02_p03.png': '2184:6687', '202605_contents02_p04.png': '2185:7253',
    '(11호)01.kb국민은행.png': '2268:1878', '(11호)02.임직원 건강관리잘하는기업은.png': '2270:1955', '(11호)03.임직원건강관리안반으면.png': '2270:1923',
    '202606_contents01_p01.png': '2243:7794', '202606_contents01_p02.png': '2243:8292',
    '202606_contents01_p04.png': '2242:7789', '202606_contents01_p05.png': '2242:7302', '202606_contents01_p06.png': '2242:7791',
    '202606_contents02_p02.png': '2249:1977', '202606_contents02_p03.png': '2248:1920',
    '202606_contents03_p01.png': '2265:2331', '202606_contents03_p02.png': '2265:2343', '202606_contents03_p03.png': '2266:1878',
    '(12호)01.오후마다 당 떨어지는 기분, 진짜 이유는.png': '2323:1937', '(12호)02.데이터 리포트.png': '2323:1986',
    '202607_contents01_p01.png': '2310:1881', '202607_contents01_p02.png': '2328:2261', '202607_contents01_p03.png': '2326:1878',
    '202607_contents02_p01.png': '2308:3065', '202607_contents02_p02.png': '2308:3068',
    '(13호)01.하반기 건강검진, 운영 현황부터 점검하세요.png': '2427:2531', '(13호)02.건강검진 담당자들은지금 무엇을고민하고 있을까요.png': '2428:2562',
    '202608_contents01_p01.png': '2395:3748', '202608_contents01_p02.png': '2413:2545', '202608_contents01_p03.png': '2414:2147',
    '202608_contents02_p01.png': '2390:2781', '202608_contents02_p02.png': '2387:2550', '202608_contents02_p03.png': '2401:1878',
    '(14호)01.검진결과가 나왔습니다.무엇을 해야할까요.png': '2481:1903', '(14호)02.걷기 챌린지, 더오래 참여하고 더 쉽게 운영하려면.png': '2495:1888',
    '(14호)02_1.걷기 챌린지, 더오래 참여하고 더 쉽게 운영하려면.png': '2525:1881',
    '202609_contents02_p01.png': '2504:2062', '202609_contents02_p02.png': '2495:1900',
}


def webp(im, q):
    if shutil.which('cwebp'):   # -sharp_yuv: 글자 · 선 주변 색 번짐을 줄임 (Pillow에는 없는 옵션)
        with tempfile.TemporaryDirectory() as t:
            src, out = os.path.join(t, 's.png'), os.path.join(t, 'o.webp')
            im.save(src)
            subprocess.run(['cwebp', '-quiet', '-q', str(q), '-m', '6', '-sharp_yuv', '-metadata', 'none', src, '-o', out], check=True)
            with open(out, 'rb') as f: return f.read()
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=q, method=6); return buf.getvalue()


def thumb(path, w=W, q=Q):
    im = Image.open(path)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3]); im = bg
    else:
        im = im.convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    return 'data:image/webp;base64,' + base64.b64encode(webp(im, q)).decode(), im.size, im0size(path)


def im0size(path):
    with Image.open(path) as im: return im.size


def from_folders():
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
                src, size, orig = thumb(p, TW, TQ)
                items.append({'issue': int(m.group(1)), 'ym': ym, 'name': f, 'type': 'thumb', 'title': m.group(3), 'w': orig[0], 'h': orig[1], 'src': src})
    return items


def from_figma(d):
    """지금 samples.js의 목록 · 분류 · 원본 크기는 그대로 두고 그림만 Figma 내보내기로 바꾼다."""
    with open(OUT, encoding='utf-8') as fp: s = fp.read()
    items = json.loads(s[s.index('['):s.rindex(']') + 1]); n = 0
    for it in items:
        nid = FIGMA.get(it['name']); p = nid and os.path.join(d, nid.replace(':', '-') + '.png')
        if not p or not os.path.exists(p): print('  유지', it['name']); continue
        it['src'] = thumb(p, TW, TQ)[0] if it['type'] == 'thumb' else thumb(p)[0]; n += 1
    print(f'Figma에서 {n}장 교체')
    return items


ap = argparse.ArgumentParser(); ap.add_argument('--figma', metavar='DIR'); a = ap.parse_args()
items = from_figma(a.figma) if a.figma else from_folders()
with open(OUT, 'w', encoding='utf-8') as fp:
    fp.write('window.NL_SAMPLES = ' + json.dumps(items, ensure_ascii=False) + ';\n')
print(f'{OUT}  {len(items)}장  {os.path.getsize(OUT) // 1024} KB')
from collections import Counter; print(Counter(i['type'] for i in items))
