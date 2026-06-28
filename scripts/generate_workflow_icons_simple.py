import re
import requests
from pathlib import Path

API_KEY = "AIzaSyCJHM9kLbO3T6GPa2Gg40OsvnSWhi49SIw"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"
OUT_DIR = Path('images/workflow_icons')
OUT_DIR.mkdir(exist_ok=True)

steps = [
    ("open", "파일 열기 / 폴더 열기 아이콘"),
    ("edit", "텍스트 수정 / 펜 아이콘"),
    ("image", "이미지 생성 / 사진 아이콘"),
    ("apply", "이미지 적용 / 업로드 아이콘"),
    ("save", "저장 / 다운로드 아이콘"),
]

for name, desc in steps:
    prompt = f"""
    Generate one clean outline SVG icon for a workflow UI.
    Theme: modern app icon, minimal, rounded, 24x24 viewBox, stroke only, no fill, stroke-width 1.8, linecap round, linejoin round, currentColor friendly.
    Use this concept: {desc}.
    Return only one valid <svg>...</svg> block, nothing else.
    """

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "topP": 0.9, "maxOutputTokens": 300},
    }
    r = requests.post(URL, json=payload, timeout=120)
    r.raise_for_status()
    text = r.json()['candidates'][0]['content']['parts'][0]['text']
    match = re.search(r"<svg[^>]*>(.*?)</svg>", text, flags=re.S)
    svg = match.group(0) if match else text
    (OUT_DIR / f"{name}.svg").write_text(svg, encoding='utf-8')
    print(name, 'OK', len(svg))
