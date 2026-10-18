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

"""
open(os.path.join(OUT, '프로젝트_지침.txt'), 'w', encoding='utf-8').write(head + body)

for f in ('content.md', 'design-system.md', 'thumbnail.md'):
    shutil.copyfile(os.path.join(SKILL, 'references', f), os.path.join(OUT, f))

n = len(head + body)
print(f'chatgpt-project/  지침 {n}자 + 파일 3개')
