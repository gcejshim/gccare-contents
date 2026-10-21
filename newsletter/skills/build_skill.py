"""스킬 zip 만들기: gc-ax-newsletter 폴더 → gc-ax-newsletter.zip (claude.ai에 올리는 파일)

PDF 규칙(references/pdf.md)은 도구 자동 만들기와 같은 규칙서(api/_pdf-rules.js)에서 만든다 → 규칙은 그 파일 하나만 고치기.
실행: py build_skill.py
"""
import os, subprocess, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKILL = os.path.join(HERE, 'gc-ax-newsletter')

rules = subprocess.run(['node', '-e', "process.stdout.write(require(process.argv[1]).PDF_RULES)", os.path.join(ROOT, 'api', '_pdf-rules.js')],
                       capture_output=True, check=True).stdout.decode('utf-8')

HEAD = """# PDF (보건관리 자료실 · 실무 자료)

기획서(PPT · PDF · Word · 붙여넣은 글)를 AX Studio · Newsletter **PDF 메뉴**에 넣을 작업 내용(JSON, `kind: nl-pdf`)으로 만든다.
도구 안 [자동 만들기]와 **같은 규칙서**다(`api/_pdf-rules.js`에서 만듦 — 이 파일을 직접 고치지 않는다).

## 진행
1. 기획서 쪽마다 무엇이 들어갈지 **한 줄씩 먼저 보여 준다** (예: "2쪽 누가 · 언제 · 어떻게 → 타임라인 · 숫자 카드 · 단계 흐름"). 표지 · 마지막 구독 안내 쪽도 표시.
2. 확인받으면 아래 규칙대로 JSON **하나**를 만든다. 길어서 채팅이 끊기므로 **아티팩트(코드 · JSON)**로 주고, 다운로드 파일은 만들지 않는다.
3. 넣는 방법 한 줄: "[복사] → AX Studio · Newsletter **아무 화면에서 Ctrl+V** 하면 맞는 메뉴로 가서 들어가요. 표지 그림은 PDF 메뉴 ③ 표지 그림 › [이미지 만들기]로 만들어요."
4. 고쳐 달라고 하면 그 쪽 · 블록만 바꾼 **전체 JSON**을 다시 준다.
5. 한 호에 PDF가 여러 개면(호수 안에서 PDF01 · PDF02 …) JSON에 `"no":"02"`처럼 번호를 넣는다. 붙여 넣으면 그 번호 자리로 들어간다(없으면 도구에서 지금 고른 번호). 파일 이름은 도구가 `(15호)PDF02.문서 이름.pdf`로 붙인다.

(아래 규칙서의 '출력: JSON 하나만'은 JSON 모양 이야기다. 대화에서는 위 1번처럼 먼저 쪽 구성을 보여 주고 확인받는다.)

## 규칙서
"""

with open(os.path.join(SKILL, 'references', 'pdf.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(HEAD + rules.strip() + '\n')
out = os.path.join(HERE, 'gc-ax-newsletter.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('gc-ax-newsletter/', '')
    z.writestr('gc-ax-newsletter/references/', '')
    for name in sorted(os.listdir(os.path.join(SKILL, 'references'))):
        z.write(os.path.join(SKILL, 'references', name), f'gc-ax-newsletter/references/{name}')
    z.write(os.path.join(SKILL, 'SKILL.md'), 'gc-ax-newsletter/SKILL.md')
print(out, os.path.getsize(out) // 1024, 'KB')
