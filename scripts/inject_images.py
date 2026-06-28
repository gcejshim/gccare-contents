"""
생성된 이미지 + 섹션 내용(DEFAULTS)을 card HTML 파일에 삽입
Usage:
  python3 inject_images.py --card 2
  python3 inject_images.py --card 3
  python3 inject_images.py        # 2, 3, 4 전체
"""

import re
import json
import base64
import argparse
from pathlib import Path

BASE_DIR   = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images"
HTML_DIR   = BASE_DIR / "cards"

# ── 카드별 헤더 타이틀/서브타이틀 ──────────────────────────────────────
CARD_HEADER = {
    2: {"title": "AST·ALT·γ-GTP\n쉽게 이해하기",    "subtitle": "건강검진 수치, 이렇게 읽으세요"},
    3: {"title": "지방간이란\n무엇인가",               "subtitle": "술 안 마셔도 생길 수 있어요"},
    4: {"title": "내 간수치\n상승 원인 {찾기}",        "subtitle": "일상 속 습관을 점검하세요"},
    5: {"title": "술만의 {문제가} 아닙니다",           "subtitle": "지방간은 술 때문만이 아니라 원인에 따라 종류와 관리법이 달라져요."},
    6:  {"title": "지방간을\n{방치하면?}",               "subtitle": "초기에 관리할수록 회복 가능성이 높아요"},
    7:  {"title": "지방간 개선의\n{핵심 3가지}",         "subtitle": "생활습관 개선만으로도 충분히 좋아질 수 있어요"},
    8:  {"title": "체중 {5%} 감량이\n간에 미치는 효과", "subtitle": "작은 변화가 간 건강에 큰 변화를 만들어요"},
    9:  {"title": "금주·절주\n{실천 가이드}",            "subtitle": "간을 위한 음주 습관 점검"},
    10: {"title": "하루 {7,000보}\n걷기 챌린지",         "subtitle": "작은 걸음이 간 건강을 바꿉니다"},
    11: {"title": "지방간 관리의\n{탄수화물 줄이기}",    "subtitle": "술보다 위험할 수도 있어요"},
    12: {"title": "단백질 중심\n식단 {시작하기}",        "subtitle": "간 건강을 위한 단백질 식습관"},
    13: {"title": "야식이\n{지방간을 만드는 이유}",      "subtitle": "밤에 먹는 습관이 간을 힘들게 해요"},
    14: {"title": "간에 좋은\n식사 패턴 {만들기}",       "subtitle": "간 건강은 습관에서 시작됩니다"},
}

# ── 카드별 섹션 콘텐츠 (엑셀 기획서 기반) ──────────────────────────────
CARD_DEFAULTS = {
    2: [
        {"no": "01", "title": "간수치 {해석법}",    "body": "AST·ALT·γ-GTP는 건강검진에서 간 상태를 확인할 때 중요한 수치예요."},
        {"no": "02", "title": "헷갈리는 {영문}",    "body": "결과지 속 영문 수치는 간 건강 상태와 간 부담 여부를 보여주는 신호예요."},
        {"no": "03", "title": "AST {의미}",          "body": "AST는 간뿐 아니라 근육에도 있어 운동 후에도 일시적으로 상승할 수 있어요."},
        {"no": "04", "title": "ALT {특징}",          "body": "ALT는 간 손상에 민감하게 반응해 지방간이나 간염에서 높아지기 쉬워요."},
        {"no": "05", "title": "γ-GTP {신호}",        "body": "γ-GTP는 음주·약물 영향에 민감해 생활습관 변화에 따라 빠르게 변할 수 있어요."},
        {"no": "06", "title": "함께 봐야 {합니다}",  "body": "수치는 하나보다 함께 보는 것이 중요하며 반복되는 변화 확인이 필요해요."},
    ],
    3: [
        {"no": "01", "title": "지방간 {경고}",        "body": "술을 마시지 않아도 지방간이 생길 수 있어 생활습관 관리가 중요해요."},
        {"no": "02", "title": "증상이 {없습니다}",    "body": "지방간은 초기 증상이 거의 없어 건강검진에서 우연히 발견되는 경우가 많아요."},
        {"no": "03", "title": "지방간이란?",           "body": "지방간은 간세포 안에 지방이 과도하게 쌓여 간 부담이 커진 상태를 말해요."},
        {"no": "04", "title": "왜 {생길까?}",         "body": "과식·단 음식·운동 부족은 간에 지방이 쌓이게 만드는 주요 원인이 될 수 있어요."},
        {"no": "05", "title": "방치하면 {위험}",      "body": "지방간을 방치하면 지방간염·간섬유화 등으로 진행될 수 있어 주의가 필요해요."},
        {"no": "06", "title": "지금 {시작하세요!}",   "body": "야식 줄이기와 걷기 같은 작은 습관 변화가 지방간 관리에 도움이 될 수 있어요."},
    ],
    14: [
        {"no": "01", "title": "식사 패턴이 {중요합니다}", "body": "간 건강은 특정 음식보다 평소 식사 습관의 영향을 더 크게 받아요."},
        {"no": "02", "title": "끼니 {거르지 않기}",       "body": "식사를 거르면 폭식하기 쉬워 간에 지방이 쌓일 가능성이 높아져요."},
        {"no": "03", "title": "아침 먹는 {습관}",         "body": "아침 식사는 하루 식사 흐름을 안정시키는 데 도움이 될 수 있어요."},
        {"no": "04", "title": "식사 순서 {바꾸기}",       "body": "채소와 단백질을 먼저 먹으면 혈당 상승을 천천히 만들 수 있어요."},
        {"no": "05", "title": "가공식품 {줄이기}",         "body": "가공식품과 첨가물이 많은 음식은 간에 부담을 줄 수 있어요."},
        {"no": "06", "title": "작은 변화부터 {시작}",     "body": "식사 습관은 한 번에 바꾸기보다 조금씩 실천하는 것이 중요해요."},
    ],
    12: [
        {"no": "01", "title": "단백질이 {중요합니다}",   "body": "지방간 관리에서는 단백질을 충분히 먹는 식습관도 중요해요."},
        {"no": "02", "title": "왜 {필요할까?}",          "body": "단백질은 근육 유지와 신진대사에 도움을 줄 수 있어요."},
        {"no": "03", "title": "포만감 유지 {효과}",       "body": "단백질은 혈당 변동을 줄이고 식사 후 포만감 유지에 도움이 돼요."},
        {"no": "04", "title": "좋은 단백질 {고르기}",    "body": "닭가슴살·생선·두부·달걀 같은 단백질 식품을 선택해보세요."},
        {"no": "05", "title": "피해야 할 {단백질}",       "body": "베이컨·삼겹살처럼 포화지방이 많은 음식은 줄이는 게 좋아요."},
        {"no": "06", "title": "한 끼씩 {바꿔보세요!}",  "body": "탄수화물 대신 단백질 비중을 조금씩 늘리는 것부터 시작해보세요."},
    ],
    4: [
        {"no": "01", "title": "간수치 원인 {찾기}",     "body": "간수치 상승 원인은 술뿐 아니라 일상 속 생활습관에 숨어 있을 수 있어요."},
        {"no": "02", "title": "숨은 {원인}",          "body": "간수치 변화는 작은 습관의 영향일 수 있어 생활습관 점검이 중요해요."},
        {"no": "03", "title": "음주 패턴 {체크}",     "body": "잦은 음주와 폭음은 γ-GTP 상승에 영향을 줄 수 있어 확인이 필요해요."},
        {"no": "04", "title": "체중·식습관 {확인}",   "body": "야식·단 음료·체중 증가는 지방간과 간수치 상승 위험을 높일 수 있어요."},
        {"no": "05", "title": "운동·수면 {점검}",     "body": "활동량 부족과 수면 부족은 간 회복을 늦추고 지방 부담을 키울 수 있어요."},
        {"no": "06", "title": "원인을 {찾아보세요!}", "body": "음주·식습관·수면 중 흔들린 습관부터 바꾸는 것이 간 관리의 시작이에요."},
    ],
    5: [
        {"no": "01", "title": "술만의 {문제가} 아닙니다", "body": "지방간은 술 때문만이 아니라 원인에 따라 종류와 관리법이 달라져요."},
        {"no": "02", "title": "지방간도 {종류가} 있다",   "body": "최근에는 술을 거의 마시지 않아도 지방간 진단을 받는 경우가 늘고 있어요."},
        {"no": "03", "title": "알코올성 {지방간}",         "body": "반복되는 음주와 폭음은 간에 지방을 쌓이게 만들 수 있어 주의가 필요해요."},
        {"no": "04", "title": "비알코올성 {지방간}",       "body": "식습관·비만·운동 부족은 비알코올성 지방간의 대표 원인이 될 수 있어요."},
        {"no": "05", "title": "마른 사람도 {위험}",        "body": "체형과 관계없이 지방간이 생길 수 있어 정기 검진과 관리가 중요해요."},
        {"no": "06", "title": "관리법은 {다릅니다}",       "body": "알코올성은 절주, 비알코올성은 체중·식단 관리가 핵심이에요."},
    ],
    6: [
        {"no": "01", "title": "방치하면 {위험합니다}",    "body": "지방간은 증상이 없어 보여도 방치하면 간 손상으로 이어질 수 있어요."},
        {"no": "02", "title": "1단계, {단순 지방간}",     "body": "초기 지방간은 생활습관 교정만으로도 충분히 회복될 가능성이 높아요."},
        {"no": "03", "title": "2단계, {지방간염}",         "body": "지방 축적이 계속되면 간에 염증이 생기고 간수치도 높아질 수 있어요."},
        {"no": "04", "title": "증상이 {없을 수도}",        "body": "지방간염 단계에서도 증상이 없는 경우가 많아 정기 검진이 중요해요."},
        {"no": "05", "title": "섬유화·{간경변} 위험",     "body": "염증이 오래 지속되면 간이 딱딱해지고 간경변으로 진행될 수 있어요."},
        {"no": "06", "title": "중요한 건 {조기 관리}",    "body": "지방간은 초기에 관리할수록 회복 가능성이 높아 생활습관 관리가 중요해요."},
    ],
    7: [
        {"no": "01", "title": "생활습관이 {핵심}",         "body": "초기 지방간은 생활습관 개선만으로도 충분히 좋아질 가능성이 높아요."},
        {"no": "02", "title": "체중 감량 {시작하기}",      "body": "체중의 5~10% 감량만으로도 간에 쌓인 지방 감소에 도움이 될 수 있어요."},
        {"no": "03", "title": "복부비만 {관리}",            "body": "허리둘레와 복부비만 관리는 지방간 개선에 중요한 관리 포인트예요."},
        {"no": "04", "title": "식습관 {바꾸기}",            "body": "단 음식·가공식품을 줄이고 채소·단백질 위주 식사가 도움이 돼요."},
        {"no": "05", "title": "꾸준한 {운동 습관}",         "body": "하루 30분 걷기 같은 가벼운 운동도 지방간 개선에 도움이 될 수 있어요."},
        {"no": "06", "title": "중요한 건 {꾸준함}",         "body": "무리한 방법보다 꾸준히 실천 가능한 생활습관을 만드는 것이 중요해요."},
    ],
    8: [
        {"no": "01", "title": "5% {감량의 힘}",             "body": "체중의 5%만 줄여도 간 건강에는 생각보다 큰 변화가 나타날 수 있어요."},
        {"no": "02", "title": "간 지방 {감소 시작}",        "body": "체중을 5% 감량하면 간에 쌓인 지방 감소가 시작될 수 있어요."},
        {"no": "03", "title": "생각보다 {작은 목표}",       "body": "70kg 기준 3.5kg 정도로 충분히 도전 가능한 현실적인 목표예요."},
        {"no": "04", "title": "천천히 {줄이기}",             "body": "급격한 단식보다 천천히 꾸준히 감량하는 것이 간 건강에 더 중요해요."},
        {"no": "05", "title": "작은 {습관 변화}",            "body": "단 음료 줄이기와 식후 걷기 같은 작은 습관 변화가 도움이 될 수 있어요."},
        {"no": "06", "title": "중요한 건 {꾸준함}",          "body": "무리한 감량보다 꾸준한 생활습관 변화가 안전하고 효과적인 방법이에요."},
    ],
    9: [
        {"no": "01", "title": "술이 {간을 지칩니다}",       "body": "잦은 음주는 지방간과 간수치 상승의 원인이 될 수 있어요."},
        {"no": "02", "title": "금주 효과가 {빠른 이유}",    "body": "γ-GTP는 알코올에 민감해 금주만으로도 수치 변화가 나타날 수 있어요."},
        {"no": "03", "title": "절주부터 {시작하기}",         "body": "금주가 어렵다면 음주량과 횟수를 줄이는 것부터 시작해보세요."},
        {"no": "04", "title": "회식 전 {전략 세우기}",      "body": "빈속 음주를 피하고 단백질·채소 위주 안주를 선택하는 게 좋아요."},
        {"no": "05", "title": "술자리 습관 {바꾸기}",       "body": "물을 함께 마시고 천천히 마시면 자연스럽게 음주량을 줄일 수 있어요."},
        {"no": "06", "title": "간 회복도 {중요합니다}",     "body": "음주 후 충분한 수분 섭취와 휴식은 간 회복에 도움이 될 수 있어요."},
    ],
    10: [
        {"no": "01", "title": "걷기부터 {시작하세요}",      "body": "하루 7,000보 걷기만으로도 간 건강에 긍정적인 변화를 만들 수 있어요."},
        {"no": "02", "title": "왜 걷기가 {중요할까?}",      "body": "걷기는 혈당 조절과 지방 연소에 도움이 되는 대표적인 유산소 운동이에요."},
        {"no": "03", "title": "복부비만 {감소 효과}",        "body": "꾸준히 걸으면 복부비만 감소와 지방간 개선에도 도움이 될 수 있어요."},
        {"no": "04", "title": "왜 {7,000보}일까?",          "body": "하루 7,000보는 체중 관리와 만성질환 예방에 효과적인 활동량이에요."},
        {"no": "05", "title": "일상 속 {걷기 습관}",         "body": "계단 이용과 식후 산책 같은 작은 습관만으로도 걸음 수를 늘릴 수 있어요."},
        {"no": "06", "title": "중요한 건 {꾸준함}",          "body": "무리하게 걷기보다 매일 꾸준히 실천하는 것이 더 중요해요."},
    ],
    11: [
        {"no": "01", "title": "술보다 {위험할 수} 있습니다", "body": "탄수화물 과잉 섭취는 지방간을 만드는 주요 원인 중 하나일 수 있어요."},
        {"no": "02", "title": "왜 탄수화물이 {문제일까?}",   "body": "남은 당분은 간에서 지방으로 저장돼 지방간 위험을 높일 수 있어요."},
        {"no": "03", "title": "혈당을 {빠르게} 올리는 음식", "body": "흰쌀밥·빵·면·달달한 음료는 간에 지방이 쌓이기 쉬운 음식이에요."},
        {"no": "04", "title": "먼저 줄여야 할 {음식}",        "body": "과자·라면·야식 같은 탄수화물 간식부터 줄여보는 것이 좋아요."},
        {"no": "05", "title": "중요한 건 {바꾸기}",           "body": "흰쌀 대신 잡곡, 단 음료 대신 물로 바꾸는 습관이 중요해요."},
        {"no": "06", "title": "작은 변화가 {시작입니다}",    "body": "식습관을 조금씩 바꾸는 것만으로도 간 건강에 도움이 될 수 있어요."},
    ],
    13: [
        {"no": "01", "title": "밤에 {먹는 습관}",             "body": "늦은 밤 야식은 간이 쉬어야 할 시간을 방해할 수 있어요."},
        {"no": "02", "title": "왜 밤에 {먹으면 안 될까?}",   "body": "밤에는 활동량과 대사 기능이 줄어 지방 저장이 쉬워질 수 있어요."},
        {"no": "03", "title": "밤에 더 {위험한 이유}",        "body": "같은 음식도 밤에 먹으면 지방으로 저장될 가능성이 높아질 수 있어요."},
        {"no": "04", "title": "야식이 {만드는 변화}",          "body": "라면·치킨·맥주 같은 야식은 간 지방과 간수치 상승에 영향을 줄 수 있어요."},
        {"no": "05", "title": "수면까지 {방해합니다}",         "body": "늦은 식사는 수면의 질을 떨어뜨려 간 회복을 방해할 수 있어요."},
        {"no": "06", "title": "잠들기 전 {3시간}",             "body": "가능하면 잠들기 3시간 전에는 식사를 마무리하는 것이 좋아요."},
    ],
}


def img_to_b64(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode()
    mime = "image/webp" if path.suffix.lower() == ".webp" else "image/png"
    return f"data:{mime};base64,{data}"


def replace_between(html: str, start_marker: str, end_pattern: str, replacement: str) -> str:
    """start_marker 이후 end_pattern 첫 등장까지를 replacement로 교체"""
    idx = html.find(start_marker)
    if idx == -1:
        return html
    after = html[idx + len(start_marker):]
    m = re.search(end_pattern, after)
    if not m:
        return html
    end_idx = idx + len(start_marker) + m.end()
    return html[:idx] + replacement + html[end_idx:]


def inject(card_no: int, skip_headline: bool = False):
    html_path = HTML_DIR / f"card{card_no:02d}.html"
    img_dir   = IMAGES_DIR / f"card{card_no:02d}"

    if not html_path.exists():
        print(f"  [card{card_no:02d}] HTML 파일 없음: {html_path}")
        return

    has_images = img_dir.exists()
    print(f"\n[card{card_no:02d}] 삽입 중... {'(이미지 포함)' if has_images else '(텍스트만)'}")

    # ── 이미지 로드 (있을 때만) ────────────────────────────────────
    header_b64 = None
    section_images = {}

    if has_images:
        # 헤드라인 이미지 처리
        if skip_headline:
            print(f"  헤드라인 이미지 생략 (--no-headline)")
        else:
            headline_path = img_dir / f"card{card_no:02d}_01_headline.webp"
            if not headline_path.exists():
                headline_path = img_dir / f"card{card_no:02d}_01_headline.png"
            if not headline_path.exists():
                print(f"  헤드라인 이미지 없음, 헤드라인 생략")
            else:
                header_b64 = img_to_b64(headline_path)
                print(f"  헤드라인: {headline_path.name}")

        # 섹션 이미지 로드 (없는 것은 슬롯 빈칸으로 유지)
        for i in range(6):
            sec_path = img_dir / f"card{card_no:02d}_{i+1:02d}.webp"
            if not sec_path.exists():
                sec_path = img_dir / f"card{card_no:02d}_{i+1:02d}.png"
            if not sec_path.exists():
                print(f"  섹션 {i+1}: 없음 (슬롯 유지)")
                continue
            section_images[str(i)] = img_to_b64(sec_path)
            print(f"  섹션 {i+1}: {sec_path.name}")
        if not section_images and not header_b64:
            has_images = False

    print("  HTML 읽는 중...")
    html = html_path.read_text(encoding="utf-8")

    # ── DEFAULTS 교체 (JS 변수) ────────────────────────────────────
    if card_no in CARD_DEFAULTS:
        new_defaults = f"let DEFAULTS = {json.dumps(CARD_DEFAULTS[card_no], ensure_ascii=False, indent=2)};"
        html = replace_between(html, "let DEFAULTS = ", r"\];", new_defaults)
        print("  DEFAULTS 업데이트 완료")

    # ── 헤더 타이틀/서브타이틀 교체 ──────────────────────────────────
    if card_no in CARD_HEADER:
        hdr = CARD_HEADER[card_no]
        title_val = hdr["title"]
        html = re.sub(
            r'(id="f-title"[^>]*>)[^<]*(</textarea>)',
            lambda m, v=title_val: m.group(1) + v + m.group(2),
            html, count=1, flags=re.DOTALL
        )
        if "subtitle" in hdr:
            sub_val = hdr["subtitle"]
            html = re.sub(
                r'(id="f-subtitle"[^>]*>)[^<]*(</textarea>)',
                lambda m, v=sub_val: m.group(1) + v + m.group(2),
                html, count=1, flags=re.DOTALL
            )
        print("  헤더 타이틀 교체 완료")

    # ── 폼 HTML 교체 (s-title-X, s-body-X) ────────────────────────
    if card_no in CARD_DEFAULTS:
        secs = CARD_DEFAULTS[card_no]
        for i, sec in enumerate(secs):
            # input value 교체 (lambda로 replacement string 이스케이프 문제 회피)
            title_val = sec["title"]
            html = re.sub(
                rf'(id="s-title-{i}"\s+value=")[^"]*(")',
                lambda m, v=title_val: m.group(1) + v + m.group(2),
                html, count=1
            )
            body_val = sec["body"]
            html = re.sub(
                rf'(id="s-body-{i}"[^>]*>)[^<]*(</textarea>)',
                lambda m, v=body_val: m.group(1) + v + m.group(2),
                html, count=1
            )
        # 카드 뱃지 input value 교체
        badge_text = f"간 건강 관리 · {card_no:02d}"
        html = re.sub(
            r'(id="f-badge"[^>]*value=")[^"]*(")',
            lambda m: m.group(1) + badge_text + m.group(2),
            html, count=1
        )
        html = re.sub(
            r'(<div class="c-header-badge"[^>]*>)[^<]*(</div>)',
            lambda m: m.group(1) + badge_text + m.group(2),
            html, count=1
        )
        print("  폼 HTML 교체 완료")

    # ── 초기화 블록 전체 교체 ──────────────────────────────────────────
    # 가능한 기존 패턴들
    old_init_variants = [
        "buildSectionForms();\nbuildPreviewSections();\napplyInitImages();\nupdate();",
        "buildSectionForms();\nbuildPreviewSections();\nupdate();",
        "buildSectionForms();\nbuildPreviewSections();\nloadFromStorage();",
    ]
    old_init = next((v for v in old_init_variants if v in html), None)

    if has_images:
        new_init = (
            "buildSectionForms();\n"
            "(function(){\n"
            "  var h='';\n"
            "  DEFAULTS.forEach(function(d,i){\n"
            "    var url=sectionImages[String(i)]||sectionImages[i]||'';\n"
            "    var imgHTML=url?'<img src=\"'+url+'\" style=\"width:100%;height:100%;object-fit:cover;border-radius:14px;display:block;\">':imgSlot(null);\n"
            "    h+='<div class=\"c-section-card\" id=\"p-card-'+i+'\">'\n"
            "      +'<span class=\"c-badge\">'+d.no+'</span>'\n"
            "      +'<h2 class=\"c-section-title\" id=\"p-stitle-'+i+'\"></h2>'\n"
            "      +'<div class=\"c-section-img-wrap\"><div class=\"c-section-img'+(url?' has-image':'')+'\" id=\"p-simg-'+i+'\" style=\"'+(url?'border:none;background:transparent;':'')+'\">'+imgHTML+'</div></div>'\n"
            "      +'<p class=\"c-section-body\" id=\"p-sbody-'+i+'\"></p>'\n"
            "      +'</div>';\n"
            "    if(url){\n"
            "      (function(idx,imgUrl){setBarImage('paste-zone-sec-'+idx,imgUrl,function(){removeSectionImg(idx);});})(i,url);\n"
            "    }\n"
            "  });\n"
            "  document.getElementById('p-sections').innerHTML=h;\n"
            "  if(headerImageURL){\n"
            "    var hs=document.getElementById('p-header-img');\n"
            "    if(hs)hs.innerHTML='<img src=\"'+headerImageURL+'\" alt=\"\" style=\"width:100%;height:100%;object-fit:cover;display:block;\">';\n"
            "    setBarImage('upload-bar-header',headerImageURL,function(){removeHeaderImg();});\n"
            "  }\n"
            "})();\n"
            "update();"
        )
    else:
        new_init = (
            "buildSectionForms();\n"
            "buildPreviewSections();\n"
            "update();"
        )

    if old_init:
        html = html.replace(old_init, new_init, 1)
        print("  초기화 블록 교체 완료")
    else:
        # IIFE 패턴(이미지 포함)이 이미 있는 경우 → 교체
        old_iife_start = "buildSectionForms();\n(function(){"
        if old_iife_start in html:
            iife_block_start = html.find(old_iife_start)
            update_marker = "update();"
            update_pos = html.find(update_marker, iife_block_start)
            if update_pos != -1:
                html = html[:iife_block_start] + new_init + html[update_pos + len(update_marker):]
                print("  초기화 블록 교체 완료 (IIFE→new)")
        else:
            print("  ⚠ 초기화 블록 미발견, 건너뜀")

    if has_images:
        # ── headerImageURL 교체 (줄 단위 교체 — regex는 긴 base64에서 오작동) ──
        header_js = json.dumps(header_b64)
        new_header_line = f"let headerImageURL = {header_js};"
        lines = html.split('\n')
        replaced_header = False
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r'let headerImageURL\s*=', stripped) and 'html.replace' not in line and 'html =' not in line:
                lines[idx] = new_header_line
                replaced_header = True
                break
        if replaced_header:
            html = '\n'.join(lines)
            print("  headerImageURL 교체 완료")
        else:
            print("  ⚠ headerImageURL 미발견")

        # ── sectionImages 교체 (줄 단위 교체) ──────────────────────
        new_sec_line = f'const sectionImages = {json.dumps(section_images, ensure_ascii=False)};'
        lines = html.split('\n')
        replaced_sec = False
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r'const sectionImages\s*=\s*\{', stripped) and 'html.replace' not in line and 'html =' not in line:
                lines[idx] = new_sec_line
                replaced_sec = True
                break
        if replaced_sec:
            html = '\n'.join(lines)
            print("  sectionImages 교체 완료")
        else:
            print("  ⚠ sectionImages 미발견")

    print("  HTML 저장 중...")
    html_path.write_text(html, encoding="utf-8")
    print(f"  완료: {html_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", type=int, choices=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    parser.add_argument("--no-headline", action="store_true",
                        help="헤드라인 이미지 주입 건너뜀")
    args = parser.parse_args()

    cards = [args.card] if args.card else [2, 3, 4, 12]
    for c in cards:
        inject(c, skip_headline=args.no_headline)
    print("\n✅ 완료!")


if __name__ == "__main__":
    main()
