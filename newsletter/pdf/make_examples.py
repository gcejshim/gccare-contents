"""리드마그넷(PDF) 예시 · 표지 그림: 완성한 호 작업 파일(issues/NN/work/*_전체.json)의 PDF를 꺼내 examples.js로 만든다.

- window.PDF_EXAMPLES: [예시 보기]에 뜨는 문서 (블록이 하나도 없는 PDF는 빼고)
- window.PDF_COVERS: 표지 그림이 있는 PDF 전부 (통합본 에셋 › 배경 이미지 › 리드마그넷 표지)
실행: python3 make_examples.py [작업 파일]  — 기본은 app/build.py의 DEFAULT_ISSUE와 같은 15호. 새 호로 예시를 바꾸면 경로만 바꿔 다시 실행
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'issues', '15', 'work', '202610_뉴스레터_15호_전체.json')

with open(SRC, encoding='utf-8') as f: issue = json.load(f)
items = (issue.get('pdf') or {}).get('items') or {}
no = issue.get('issue')
examples, covers = [], []
for k in sorted(items):
    d = items[k]
    d = {x: d[x] for x in d if x not in ('no', 'origin')}   # 작업 기록(넣은 기획서 · 시각)은 예시에 안 넣음
    title = (d.get('title') or '').split('\n')[0]
    if any(pg.get('blocks') for pg in d.get('pages', [])): examples.append({'name': title, 'issue': no, 'doc': d})
    if (d.get('img') or {}).get('src'): covers.append({'name': title, 'issue': no, 'theme': d.get('theme'), 'src': d['img']['src']})

out = os.path.join(HERE, 'examples.js')
with open(out, 'w', encoding='utf-8') as f:
    f.write(f'// make_examples.py로 만듦 ({os.path.relpath(SRC, ROOT)}) — 직접 고치지 말고 작업 파일을 고쳐 다시 실행\n')
    f.write('window.PDF_EXAMPLES=' + json.dumps(examples, ensure_ascii=False) + ';\n')
    f.write('window.PDF_COVERS=' + json.dumps(covers, ensure_ascii=False) + ';\n')
print(f'{out}  예시 {len(examples)}개 · 표지 {len(covers)}장 ({os.path.getsize(out) // 1024} KB)')
