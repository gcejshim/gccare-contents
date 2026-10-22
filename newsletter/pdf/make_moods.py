"""리드마그넷 분위기 보기: 주제 · 표지 색 · 그림체가 다른 완성 표지(pdf/moods/)를 moods.js로 만든다.

- moods/meta.json: [{id, name, theme, style, desc}] — 순서대로 보여 줌
- moods/{id}_cover.webp: 패널에 작게 보이는 완성 표지 (폭 240)
- moods/{id}_big.webp: 마우스를 올리면 패널 옆에 크게 보이는 완성 표지 (폭 1200)
- moods/{id}_art.webp: 누르면 표지에 미리 얹히는 그림 원본
실행: python3 make_moods.py  →  moods.js (그다음 app/build.py)
"""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'moods')
b64 = lambda f: 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(D, f), 'rb').read()).decode()

with open(os.path.join(D, 'meta.json'), encoding='utf-8') as f: meta = json.load(f)
moods = [dict(m, cover=b64(m['id'] + '_cover.webp'), big=b64(m['id'] + '_big.webp'), art=b64(m['id'] + '_art.webp')) for m in meta]
out = os.path.join(HERE, 'moods.js')
with open(out, 'w', encoding='utf-8') as f:
    f.write('// make_moods.py로 만듦 (pdf/moods/) — 직접 고치지 말고 moods 폴더를 고쳐 다시 실행\n')
    f.write('window.PDF_MOODS=' + json.dumps(moods, ensure_ascii=False) + ';\n')
print(f'{out}  분위기 {len(moods)}개 ({os.path.getsize(out) // 1024} KB)')
