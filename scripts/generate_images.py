import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GREEN = (10, 194, 98)
NAVY  = (30, 45, 74)
NAVY_DARK = (13, 31, 60)
WHITE = (255, 255, 255)
LIGHT = (200, 216, 240)

CARDS = {
    1: {
        "dir": "card01",
        "header": {
            "title": "간수치가 높다는 신호",
            "subtitle": "무엇이 문제일까?",
        },
        "sections": [
            {"no": "01", "title": "간수치 경고등", "keyword": "피로·무기력"},
            {"no": "02", "title": "침묵의 장기",   "keyword": "자각증상 無"},
            {"no": "03", "title": "간수치 의미",   "keyword": "AST · ALT"},
            {"no": "04", "title": "의외의 원인",   "keyword": "야식·비만·수면"},
            {"no": "05", "title": "확인 포인트",   "keyword": "음주·체중·약물"},
            {"no": "06", "title": "중요한 건 흐름", "keyword": "지속 관찰"},
        ],
    }
}

def try_font(size):
    paths = [
        str(Path(__file__).parent.parent / "assets" / "Jalnan.ttf"),
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_header(out_path, title, subtitle):
    W, H = 390, 220
    img = Image.new("RGB", (W, H), NAVY_DARK)
    draw = ImageDraw.Draw(img)

    # 배경 장식 원
    for cx, cy, r, alpha in [(320, 40, 80, 40), (60, 180, 60, 30), (350, 180, 50, 25)]:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*GREEN, alpha))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)

    # 하단 그린 바
    draw.rectangle([0, H-6, W, H], fill=GREEN)

    # 텍스트
    f_sub  = try_font(15)
    f_main = try_font(26)

    draw.text((24, 60), subtitle, font=f_sub, fill=LIGHT)
    draw.text((24, 88), title,   font=f_main, fill=WHITE)

    # GC Care 로고 텍스트
    f_logo = try_font(12)
    draw.text((24, H-28), "GC Care", font=f_logo, fill=GREEN)

    img.save(out_path)
    print(f"  저장: {out_path}")

def draw_section(out_path, no, title, keyword):
    W, H = 215, 160
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # 상단 컬러 바
    draw.rectangle([0, 0, W, 44], fill=NAVY)

    # 번호 뱃지
    f_no   = try_font(13)
    f_kw   = try_font(20)
    f_title = try_font(12)

    draw.rounded_rectangle([12, 10, 46, 30], radius=5, fill=GREEN)
    draw.text((16, 12), no, font=f_no, fill=WHITE)

    draw.text((54, 12), title, font=f_title, fill=LIGHT)

    # 키워드 중앙 표시
    bbox = draw.textbbox((0, 0), keyword, font=f_kw)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 65), keyword, font=f_kw, fill=NAVY)

    # 하단 그린 라인
    draw.rectangle([0, H-4, W, H], fill=GREEN)

    # 테두리
    draw.rectangle([0, 0, W-1, H-1], outline=(*GREEN, 255), width=1)

    img.save(out_path)
    print(f"  저장: {out_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", type=int, required=True)
    args = parser.parse_args()

    card = CARDS.get(args.card)
    if not card:
        print(f"카드 {args.card}번 데이터가 없습니다.")
        return

    out_dir = os.path.join("images", card["dir"])
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n[카드 {args.card}] 이미지 생성 중...")

    draw_header(
        os.path.join(out_dir, "header.png"),
        card["header"]["title"],
        card["header"]["subtitle"],
    )

    for sec in card["sections"]:
        fname = f"sec_{sec['no']}.png"
        draw_section(
            os.path.join(out_dir, fname),
            sec["no"], sec["title"], sec["keyword"],
        )

    print(f"\n완료! {out_dir}/ 에 {1 + len(card['sections'])}개 파일 생성됨.\n")

if __name__ == "__main__":
    main()


