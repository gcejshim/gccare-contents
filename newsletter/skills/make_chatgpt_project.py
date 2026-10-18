"""ChatGPT 프로젝트용 파일 만들기: gc-ax-insight 스킬 → chatgpt-project/

ChatGPT 프로젝트 = 지침(Instructions) + 파일. 스킬과 내용은 같고, 지침만 '프로젝트의 모든 대화에서 따르기'로 바꾼다.
스킬(SKILL.md · references)을 고친 뒤 실행하면 같이 맞춰진다.

실행: py make_chatgpt_project.py  →  chatgpt-project/ (프로젝트_지침.txt + content.md · design-system.md · thumbnail.md)
"""
import os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, 'gc-ax-insight')
OUT = os.path.join(HERE, 'chatgpt-project')
os.makedirs(OUT, exist_ok=True)

body = open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read()
body = re.sub(r'^---\n.*?\n---\n\n?', '', body, count=1, flags=re.S)   # 스킬 머리말(name · description) 빼기
body = body.replace('`references/', '`')                               # 프로젝트에서는 파일이 한 곳에

head = """이 프로젝트는 GC케어 뉴스레터 제작 도구 'GC AX Studio · Insight'용이다. 이 프로젝트의 모든 대화에서 아래 지침을 따른다.
기획안(PDF · PPT · 엑셀 · 문서 · 붙여넣은 글)이나 이미지를 받으면, 프로젝트 파일 thumbnail.md · content.md · design-system.md를 읽고 그 규칙대로 결과를 만든다. 답은 한국어로 한다.
**썸네일**을 요청하면 썸네일 JSON을 준 뒤, thumbnail-image.md 규칙대로 **그림도 이미지 생성으로 바로 만든다**(콘텐츠마다 한 장씩, 그림에는 타이틀 · 칩 · 로고를 넣지 않음).

"""
open(os.path.join(OUT, '프로젝트_지침.txt'), 'w', encoding='utf-8').write(head + body)

for f in ('content.md', 'design-system.md', 'thumbnail.md'):
    shutil.copyfile(os.path.join(SKILL, 'references', f), os.path.join(OUT, f))
# ChatGPT 프로젝트에만 있는 파일 (Claude 스킬은 그림을 못 그림): 썸네일 그림 규칙
shutil.copyfile(os.path.join(HERE, 'chatgpt-extra', 'thumbnail-image.md'), os.path.join(OUT, 'thumbnail-image.md'))

# 참고 이미지 (도구는 19장을 자동 추천해 같이 보냄 → 프로젝트에는 배경색 · 그림체별 대표 11장, 파일 이름에 배경색 · 그림체)
from PIL import Image
REFS_DIR = os.path.join(HERE, '..', 'thumbnail', 'assets', 'refs')
meta = {}
for m in re.finditer(r"\('([^']+)', '([^']+)', \[([^\]]*)\], '(\w+)',\s*'([^']*)'\)", open(os.path.join(HERE, '..', 'thumbnail', 'make_refs.py'), encoding='utf-8').read()):
    meta[m.group(1)] = (m.group(2), [x.strip(" '") for x in m.group(3).split(',')], m.group(4), m.group(5))
PICK = ['13_01_하반기건강검진', '10_01_데이터리포트', '12_02_폭염', '12_01_당떨어지는기분', '14_02_걷기챌린지', '14_01_검진결과',
        '13_02_담당자고민', '11_03_과태료', '자료실_건강증진', '자료실_응급처치', '11_01_KB국민은행']
TYPE = {'obj3d': '3D', 'scene3d': '3D', 'mockup': '3D', 'flat': '3D', 'photo': '실사'}
RD = os.path.join(OUT, '참고이미지'); os.makedirs(RD, exist_ok=True)
for f in os.listdir(RD): os.remove(os.path.join(RD, f))
rows = []
for fid in PICK:
    name, bg, typ, desc = meta[fid]
    fn = f"참고_{bg[0]}_{TYPE.get(typ, '3D')}_{name.replace(' ', '').replace('·', '')}.jpg"
    Image.open(os.path.join(REFS_DIR, fid + '.png')).convert('RGB').save(os.path.join(RD, fn), 'JPEG', quality=86)
    rows.append(f"| {fn} | {', '.join(bg)} | {TYPE.get(typ, '3D')} | {desc} |")
img_md = open(os.path.join(OUT, 'thumbnail-image.md'), encoding='utf-8').read()
img_md += """
## 참고 이미지 (프로젝트 파일 '참고_….jpg')
그림을 만들 때 **썸네일 배경색(preset) · 그림체에 맞는 참고 이미지 1장**을 골라 함께 참고한다(파일 이름 = 참고_배경색_그림체_주제). 어느 것을 골랐는지 한 줄로 알려 준다.
- 참고 이미지에서는 **배치 · 구도 · 색 분위기만** 따른다. 재질 · 조명은 위 '그림체'(스튜디오 프리미엄 3D)를 따르고, 물건 · 글자는 따라 그리지 않는다.
- 사용자가 대화에 이미지를 첨부하면 **첨부 이미지가 우선**이다(위 '참고 이미지를 첨부했을 때').

| 파일 | 어울리는 배경 | 그림체 | 모습 |
|---|---|---|---|
""" + '\n'.join(rows) + '\n'
open(os.path.join(OUT, 'thumbnail-image.md'), 'w', encoding='utf-8').write(img_md)

n = len(head + body)
print(f'chatgpt-project/  지침 {n}자 + 파일 4개 + 참고 이미지 {len(PICK)}장')
