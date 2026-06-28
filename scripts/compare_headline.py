"""
헤드라인 모델 비교: Gemini vs GPT
card01, card02 헤드라인을 Gemini로 생성 → 기존 GPT 결과와 나란히 저장

출력:
  images/comparison/card01_gpt.webp     ← GPT 원본 복사
  images/comparison/card01_gemini.webp  ← Gemini 생성
  images/comparison/card02_gpt.webp
  images/comparison/card02_gemini.webp

실행:
  python3 compare_headline.py
"""

import sys
import shutil
import base64
from io import BytesIO
from pathlib import Path
from PIL import Image

# generate_card_images.py의 함수/상수를 그대로 재사용
sys.path.insert(0, str(Path(__file__).parent))
from generate_card_images import (
    generate_image,   # Gemini 이미지 생성 함수 (섹션에서 쓰는 그대로)
    IMAGES_DIR,
    REF_HEADLINE,
)

OUT_DIR = IMAGES_DIR / "comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ── 비교 대상 카드 정의 ──────────────────────────────────────────────────
CARDS = {
    1: {
        "title":       "간수치가 높다는 신호, 무엇이 문제일까?",
        "subtitle":    "건강검진 수치를 제대로 이해해보세요",
        "is_odd":      True,
        "ref_keyword": ["card01", "card03"],   # 홀수 참고이미지
        "gpt_src":     IMAGES_DIR / "card01" / "card01_01_headline.webp",
    },
    2: {
        "title":       "AST·ALT·γ-GTP 쉽게 이해하기",
        "subtitle":    "건강검진 수치, 이렇게 읽으세요",
        "is_odd":      False,
        "ref_keyword": ["card02"],             # 짝수 참고이미지
        "gpt_src":     IMAGES_DIR / "card02" / "card02_01_headline.webp",
    },
}


def load_headline_refs(keywords: list[str], max_count: int = 2) -> list[str]:
    """참고이미지 폴더에서 키워드 매칭 파일 로드 (generate_card_images.py 방식 동일)"""
    files = sorted([
        f for f in REF_HEADLINE.iterdir()
        if not f.name.startswith('.')
        and any(k in f.stem for k in keywords)
    ])[:max_count]
    result = []
    for f in files:
        img = Image.open(f).convert("RGB")
        if max(img.size) > 768:
            img.thumbnail((768, 768), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        result.append(base64.b64encode(buf.getvalue()).decode())
    print(f"  참고이미지 {len(result)}장 로드: {[f.name for f in files]}")
    return result


def build_headline_prompt(title: str, subtitle: str, is_odd: bool) -> str:
    gender = "30대 한국인 남성" if is_odd else "30대 한국인 여성"
    clothing = "#BAD0F1 (연한 블루)" if is_odd else "#FEEAB0 (연한 옐로우)"
    return (
        f"참고 이미지와 완전히 동일한 스타일, 색상, 레이아웃으로 헬스 카드뉴스 표지를 생성해줘.\n\n"
        f"아래 한글 텍스트를 글자 획 하나도 틀리지 않게 정확히 표시해줘:\n"
        f"- 제목 (크고 굵게): {title}\n"
        f"- 부제목 (작게): {subtitle}\n\n"
        f"캐릭터: {gender}, 상의 색상 {clothing}, 3D 클레이 일러스트 스타일\n"
        f"텍스트는 절대 임의로 변형하지 마. 그대로 정확하게 렌더링."
    )


def main():
    print("\n" + "="*55)
    print("  헤드라인 모델 비교: Gemini vs GPT")
    print("="*55)

    for card_no, info in CARDS.items():
        print(f"\n── card{card_no:02d}: {info['title']} ──")

        # GPT 원본 복사
        gpt_out = OUT_DIR / f"card{card_no:02d}_gpt.webp"
        if info["gpt_src"].exists():
            shutil.copy2(info["gpt_src"], gpt_out)
            print(f"  GPT 원본 복사 → {gpt_out.name}")
        else:
            print(f"  ⚠ GPT 원본 없음: {info['gpt_src']}")

        # Gemini 생성 (generate_card_images.py의 generate_image() 그대로 사용)
        gemini_out = OUT_DIR / f"card{card_no:02d}_gemini.webp"
        print(f"  Gemini 생성 중...")
        ref = load_headline_refs(info["ref_keyword"])
        prompt = build_headline_prompt(info["title"], info["subtitle"], info["is_odd"])
        img_bytes = generate_image(prompt, ref)
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=85)
        gemini_out.write_bytes(buf.getvalue())
        print(f"  저장 완료 → {gemini_out.name} ({gemini_out.stat().st_size//1024}KB)")

    print(f"\n✅ 완료! 결과: {OUT_DIR}")
    for f in sorted(OUT_DIR.iterdir()):
        print(f"   {f.name}  ({f.stat().st_size//1024}KB)")


if __name__ == "__main__":
    main()
