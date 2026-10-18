"""ChatGPT 프로젝트용 파일 만들기 (콘텐츠 이미지 전용, 2026-10-18 사용자 결정 — 썸네일은 도구에 있으므로 뺌)

ChatGPT 프로젝트 = 지침(Instructions) + 파일.
- 지침: chatgpt-extra/project-instructions.md (콘텐츠 이미지 전용으로 따로 씀)
- 파일: 스킬 gc-ax-insight/references 의 content.md · design-system.md (스킬과 같은 내용)
스킬(references)을 고친 뒤 실행하면 같이 맞춰진다.
썸네일까지 넣던 예전 구성(thumbnail.md · thumbnail-image.md · 참고 이미지 11장)은 chatgpt-extra/thumbnail-image.md에 규칙만 남겨 둠.

실행: py make_chatgpt_project.py  →  chatgpt-project/ (프로젝트_지침.txt + content.md · design-system.md)
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, 'gc-ax-insight')
OUT = os.path.join(HERE, 'chatgpt-project')
if os.path.isdir(OUT): shutil.rmtree(OUT)   # 예전 썸네일 파일 · 참고 이미지까지 정리
os.makedirs(OUT)

inst = open(os.path.join(HERE, 'chatgpt-extra', 'project-instructions.md'), encoding='utf-8').read()
open(os.path.join(OUT, '프로젝트_지침.txt'), 'w', encoding='utf-8').write(inst)
for f in ('content.md', 'design-system.md'):
    shutil.copyfile(os.path.join(SKILL, 'references', f), os.path.join(OUT, f))
print(f'chatgpt-project/  지침 {len(inst)}자 + 파일 2개 (콘텐츠 이미지 전용)')
