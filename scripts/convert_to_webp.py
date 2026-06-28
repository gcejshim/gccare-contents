"""
HTML 파일 안에 박힌 base64 PNG 이미지를 WebP로 변환
Usage:
  python3 convert_to_webp.py --card 2
  python3 convert_to_webp.py           # 모든 card HTML 처리
"""
import re
import base64
import argparse
from pathlib import Path
from io import BytesIO
from PIL import Image

BASE_DIR = Path(__file__).parent.parent
CARDS_DIR = BASE_DIR / "cards"


def png_b64_to_webp_b64(b64_str: str, quality: int = 85) -> str:
    raw = base64.b64decode(b64_str)
    img = Image.open(BytesIO(raw))
    buf = BytesIO()
    img.save(buf, "WEBP", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def convert_html(html_path: Path):
    print(f"\n처리 중: {html_path.name}  ({html_path.stat().st_size / 1024 / 1024:.1f} MB)")
    html = html_path.read_text(encoding="utf-8")

    pattern = re.compile(r'data:image/png;base64,([A-Za-z0-9+/=]+)')
    matches = pattern.findall(html)

    if not matches:
        print("  PNG base64 없음, 건너뜀")
        return

    print(f"  PNG 이미지 {len(matches)}개 발견 → WebP 변환 중...")
    count = 0
    def replacer(m):
        nonlocal count
        count += 1
        print(f"    [{count}/{len(matches)}] 변환 중...", end="\r")
        webp = png_b64_to_webp_b64(m.group(1))
        return f"data:image/webp;base64,{webp}"

    html_new = pattern.sub(replacer, html)
    print()

    html_path.write_text(html_new, encoding="utf-8")
    new_size = html_path.stat().st_size / 1024 / 1024
    print(f"  완료: {new_size:.1f} MB")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", type=int, help="카드 번호 (없으면 전체)")
    args = parser.parse_args()

    if args.card:
        targets = [CARDS_DIR / f"card{args.card:02d}.html"]
    else:
        targets = sorted(CARDS_DIR.glob("card*.html"))

    for p in targets:
        if p.exists():
            convert_html(p)

    print("\n✅ 완료!")


if __name__ == "__main__":
    main()
