import json
import re
import requests
from pathlib import Path

API_KEY = "AIzaSyCJHM9kLbO3T6GPa2Gg40OsvnSWhi49SIw"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

OUT_DIR = Path("images/workflow_icons")
OUT_DIR.mkdir(exist_ok=True)

PROMPT = """
당신은 UI/UX용 SVG 아이콘 디자이너입니다.
아래 5개의 워크플로우 단계에 맞는 선형 SVG 아이콘을 만들어 주세요.
조건:
- 각 아이콘은 24x24 viewBox
- stroke만 사용, fill 없음
- stroke-width 1.8
- stroke-linecap=round, stroke-linejoin=round
- currentColor 스타일에 맞게 단색으로 작성
- 너무 장식적이지 않고 실제 앱 아이콘처럼 깔끔한 모양
- 각 아이콘은 하나의 <svg>...</svg> 문자열만 포함
- 출력은 반드시 JSON 형식: {"icons":[{"name":"open","svg":"<svg ...>...</svg>"}, ...]}

단계:
1. open: 파일 열기 / 폴더 열기
2. edit: 텍스트 수정 / 펜/메모
3. image: 이미지 생성 / 사진/캔버스
4. apply: 이미지 적용 / 업로드/붙여넣기
5. save: 저장 / 다운로드
"""

payload = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": PROMPT}],
        }
    ],
    "generationConfig": {
        "temperature": 0.2,
        "topP": 0.9,
        "maxOutputTokens": 1200,
    },
}

response = requests.post(URL, json=payload, timeout=120)
response.raise_for_status()
obj = response.json()
text = obj["candidates"][0]["content"]["parts"][0]["text"]
(OUT_DIR.parent / "gemini_response.txt").write_text(text, encoding="utf-8")
print("WROTE", OUT_DIR.parent / "gemini_response.txt")

match = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.S)
if not match:
    match = re.search(r"(\{\s*\"icons\"\s*:\s*\[.*\]\s*\})", text, flags=re.S)
if not match:
    raise ValueError("Gemini response did not contain JSON.")
json_text = match.group(1)
icons = json.loads(json_text)["icons"]

for item in icons:
    name = item["name"]
    svg = item["svg"]
    (OUT_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(f"wrote {OUT_DIR / f'{name}.svg'}")
