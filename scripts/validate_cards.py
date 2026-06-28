"""
카드뉴스 데이터 일관성 검증기
사용법:
  python validate_cards.py                          # generate_card_images.py 검증
  python validate_cards.py --file generate_card_images.py
  python validate_cards.py --show-rules             # 규칙 목록만 출력
"""

import sys
import argparse
import importlib.util
from pathlib import Path

# ────────────────────────────────────────────────────────────
# 규칙 정의
# ────────────────────────────────────────────────────────────

RULES = {
    "odd_male_clothing":  "#BAD0F1",   # 홀수 카드 남성 상의
    "even_female_clothing": "#FEEAB0", # 짝수 카드 여성 상의
    "odd_character":      "남성",
    "even_character":     "여성",
    "required_section_count": 6,
    "required_section_nos": [f"{i:02d}" for i in range(1, 7)],  # "01"~"06"
}

ERRORS = []
WARNINGS = []

def err(msg): ERRORS.append(msg)
def warn(msg): WARNINGS.append(msg)


# ────────────────────────────────────────────────────────────
# 검증 함수들
# ────────────────────────────────────────────────────────────

def check_parity(card_no: int, is_odd_actual: bool):
    """카드 번호와 홀짝 결과 일치 확인"""
    expected = (card_no % 2 == 1)
    if is_odd_actual != expected:
        err(f"  카드 {card_no:02d}: is_odd={is_odd_actual} 인데 {card_no}%2={card_no%2} → "
            f"{'홀수' if expected else '짝수'}이어야 함")


def check_sections(card_no: int, sections: list):
    """섹션 개수와 번호 검증"""
    count = len(sections)
    if count != RULES["required_section_count"]:
        err(f"  카드 {card_no:02d}: 섹션 {count}개 (6개여야 함)")

    nos = [s.get("no") for s in sections]
    expected = RULES["required_section_nos"]
    for exp_no in expected:
        if exp_no not in nos:
            err(f"  카드 {card_no:02d}: 섹션 번호 '{exp_no}' 없음 (있는 것: {nos})")

    for sec in sections:
        if not sec.get("title"):
            err(f"  카드 {card_no:02d} 섹션 {sec.get('no')}: title 비어있음")
        if not sec.get("scene"):
            warn(f"  카드 {card_no:02d} 섹션 {sec.get('no')}: scene 없음")


def check_clothing_in_script(card_no: int, script_source: str):
    """생성 스크립트 내부의 옷 색상 코드가 홀짝에 맞는지 확인"""
    is_odd = (card_no % 2 == 1)
    correct_color  = RULES["odd_male_clothing"] if is_odd else RULES["even_female_clothing"]
    wrong_color    = RULES["even_female_clothing"] if is_odd else RULES["odd_male_clothing"]
    correct_gender = RULES["odd_character"] if is_odd else RULES["even_character"]
    wrong_gender   = RULES["even_character"] if is_odd else RULES["odd_character"]

    # 스크립트에서 해당 카드 번호 주변 코드 추출 (간단히 전체 검색)
    # generate_card_images.py는 런타임에 f-string으로 생성하므로
    # 소스에서 직접 확인 불가 → CARDS dict의 scene으로 간접 확인
    return correct_color, correct_gender  # 호출자가 활용


def check_cross_consistency(cards: dict, card_defaults: dict, card_header: dict):
    """CARDS / CARD_DEFAULTS / CARD_HEADER 키 일치 확인"""
    cards_keys    = set(cards.keys())
    defaults_keys = set(card_defaults.keys()) if card_defaults else set()
    header_keys   = set(card_header.keys()) if card_header else set()

    # CARDS에는 있는데 CARD_DEFAULTS에 없는 것
    missing_defaults = cards_keys - defaults_keys
    if missing_defaults:
        for k in sorted(missing_defaults):
            warn(f"  카드 {k:02d}: CARDS에 있으나 CARD_DEFAULTS 없음")

    # CARDS에는 있는데 CARD_HEADER에 없는 것
    missing_header = cards_keys - header_keys
    if missing_header:
        for k in sorted(missing_header):
            warn(f"  카드 {k:02d}: CARDS에 있으나 CARD_HEADER 없음")

    # 반대 방향
    extra_defaults = defaults_keys - cards_keys
    for k in sorted(extra_defaults):
        warn(f"  카드 {k:02d}: CARD_DEFAULTS에 있으나 CARDS 없음")


# ────────────────────────────────────────────────────────────
# 메인 검증 루프
# ────────────────────────────────────────────────────────────

def validate(module):
    cards = getattr(module, "CARDS", None)
    card_defaults = getattr(module, "CARD_DEFAULTS", None)
    card_header   = getattr(module, "CARD_HEADER", None)

    if cards is None:
        err("CARDS dict를 찾을 수 없음")
        return

    print(f"\n검증 대상 카드: {sorted(cards.keys())}")
    print(f"총 {len(cards)}개 카드\n")

    for card_no, card in sorted(cards.items()):
        is_odd = (card_no % 2 == 1)
        parity_str = f"{'홀수(남)' if is_odd else '짝수(여)'}"
        print(f"  카드 {card_no:02d} [{parity_str}] — {card.get('title','').replace(chr(10),' ')}")

        # 1) 홀짝 계산 자체는 항상 card_no % 2로 보장됨 (코드 리뷰 목적)
        check_parity(card_no, is_odd)

        # 2) 섹션 검증
        sections = card.get("sections", [])
        check_sections(card_no, sections)

        # 3) scene 안에 잘못된 성별/색상이 들어갔는지 확인
        correct_color, correct_gender = check_clothing_in_script(card_no, "")
        wrong_color   = RULES["even_female_clothing"] if is_odd else RULES["odd_male_clothing"]
        wrong_gender  = RULES["even_character"] if is_odd else RULES["odd_character"]

        for sec in sections:
            scene = sec.get("scene", "")
            if wrong_color.lower() in scene.lower():
                err(f"  카드 {card_no:02d} 섹션 {sec.get('no')}: "
                    f"잘못된 옷 색상 {wrong_color} (올바른 색: {correct_color})")
            if wrong_gender in scene:
                err(f"  카드 {card_no:02d} 섹션 {sec.get('no')}: "
                    f"잘못된 성별 '{wrong_gender}' (올바른 성별: '{correct_gender}')")

    # 4) 교차 일관성
    if card_defaults or card_header:
        check_cross_consistency(cards, card_defaults or {}, card_header or {})

    # ────────── 결과 출력 ──────────
    print("\n" + "="*55)
    if not ERRORS and not WARNINGS:
        print("✅ 검증 통과 — 오류 없음")
    else:
        if ERRORS:
            print(f"❌ 오류 {len(ERRORS)}건:")
            for e in ERRORS:
                print(e)
        if WARNINGS:
            print(f"\n⚠️  경고 {len(WARNINGS)}건:")
            for w in WARNINGS:
                print(w)
        if ERRORS:
            print("\n→ 위 오류를 수정한 후 다시 실행하세요.")
            sys.exit(1)
    print("="*55)


# ────────────────────────────────────────────────────────────
# 진입점
# ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="generate_card_images.py",
                        help="검증할 Python 파일 (기본값: generate_card_images.py)")
    parser.add_argument("--show-rules", action="store_true",
                        help="적용 중인 검증 규칙 출력")
    args = parser.parse_args()

    if args.show_rules:
        print("적용 규칙:")
        for k, v in RULES.items():
            print(f"  {k}: {v}")
        return

    target = Path(args.file)
    if not target.exists():
        print(f"파일 없음: {target}")
        sys.exit(1)

    # 동적 모듈 로드
    spec = importlib.util.spec_from_file_location("target_module", target)
    mod  = importlib.util.module_from_spec(spec)

    # API 키 등 외부 의존성 무시
    import unittest.mock as mock
    with mock.patch.dict("sys.modules", {
        "requests": mock.MagicMock(),
        "PIL": mock.MagicMock(),
        "PIL.Image": mock.MagicMock(),
        "openai": mock.MagicMock(),
    }):
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"모듈 로드 실패: {e}")
            sys.exit(1)

    print(f"파일 로드: {target}")
    validate(mod)


if __name__ == "__main__":
    main()
