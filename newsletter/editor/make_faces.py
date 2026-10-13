"""인터뷰 얼굴(얼굴 고르기) 추가: assets/faces/*.png → assets-editor.js 의 face 키

ChatGPT로 만든 얼굴(흰 바탕 + 민트 동그라미)은 동그라미 바깥 흰색을 투명하게 지우고(머리카락이 동그라미 밖으로 나와도 그대로),
가장자리에 맞춰 자른 뒤 폭 360px로 줄여 WebP로 넣는다. 이미 투명한 PNG는 그대로 줄이기만 한다.
11호 얼굴(face11a~c)은 기존 값을 그대로 둔다.

새 얼굴 추가: assets/faces에 PNG 저장 → 아래 FACES에 한 줄 → index.html FACES에도 같은 키 · 이름 → 실행
실행: py make_faces.py  →  assets-editor.js  (그다음 build.py)
"""
import base64, io, json, os, re
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'assets', 'faces')
JS = os.path.join(HERE, 'assets-editor.js')

FACES = [   # (파일, 키)
    ('face_d_woman20.png', 'faceWoman20'),
    ('face_f_woman40.png', 'faceWoman40'),
    ('face_j_doctor.png', 'faceDoctor'),
    ('face_k_nurse.png', 'faceNurse'),
]


def cutout(im):
    """흰 바탕 중 이미지 테두리와 이어진 부분만 투명하게 (얼굴 · 옷의 흰색은 남김)"""
    a = np.array(im.convert('RGB'))
    white = (a.min(axis=2) > 232).astype(np.uint8)
    n, lab = cv2.connectedComponents(white, connectivity=4)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge)) & (white > 0)
    # 흰 옷(가운 등)이 바깥 흰색과 이어져도 지워지지 않게: 민트 동그라미를 찾아 그 안쪽은 남김
    r, g, b = [a[:, :, i].astype(int) for i in range(3)]
    mint = (g - r > 12) & (g > 200) & (b > 200)
    if mint.sum() > 1000:
        (cx, cy), rad = cv2.minEnclosingCircle(np.column_stack(np.nonzero(mint)[::-1]).astype(np.float32))
        yy, xx = np.mgrid[:a.shape[0], :a.shape[1]]
        bg &= (xx - cx) ** 2 + (yy - cy) ** 2 > (rad - 1) ** 2
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)   # 가장자리 부드럽게
    return Image.fromarray(np.dstack([a, alpha]))


def prep(path):
    im = Image.open(path)
    if im.mode != 'RGBA' or im.getpixel((0, 0))[3] > 0:
        im = cutout(im)
    im = im.crop(im.getbbox())
    w = 360
    if im.width == w:   # 이미 다듬은 파일 → 다시 줄이지 않음
        return im
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


src = open(JS, encoding='utf-8').read()
m = re.search(r'(window\.NL_ASSETS = Object\.assign\(window\.NL_ASSETS \|\| \{\}, )(\{.*\})(\);\s*)$', src, re.S)
assert m, 'assets-editor.js 형식을 못 읽었어요'
data = json.loads(m.group(2))
for fn, key in FACES:
    im = prep(os.path.join(SRC, fn))
    im.save(os.path.join(SRC, fn))   # 다듬은 결과로 저장 (다시 돌려도 같음)
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=88, method=6)
    data[key] = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    print(f'{key:12s} {fn}  {im.size[0]}×{im.size[1]}  {len(buf.getvalue()) // 1024} KB')
with open(JS, 'w', encoding='utf-8') as f:
    f.write(src[:m.start()] + m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3))
