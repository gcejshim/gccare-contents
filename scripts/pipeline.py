"""
카드뉴스 자동화 파이프라인
사용: python3 pipeline.py --cards 17 18 19 20
      python3 pipeline.py --cards 15-20
      python3 pipeline.py --cards 17-20 --review-only  # 검수만 실행
"""
import argparse, subprocess, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR  = Path(__file__).parent.parent
HTML_DIR  = BASE_DIR / "cards"
IMG_DIR   = BASE_DIR / "images"

def run(cmd, desc):
    print(f"\n[{desc}]")
    r = subprocess.run(cmd, shell=True, cwd=str(BASE_DIR),
                       capture_output=True, text=True)
    if r.stdout: print(r.stdout.strip())
    if r.returncode != 0:
        print(f"❌ 오류: {r.stderr.strip()}")
        return False
    return True

def has_all_images(card_no):
    d = IMG_DIR / f"card{card_no:02d}"
    if not d.exists(): return False
    headline = d / f"card{card_no:02d}_01_headline.webp"
    sections = [d / f"card{card_no:02d}_{i:02d}.webp" for i in range(1, 7)]
    return headline.exists() and all(s.exists() for s in sections)

def generate_jpg(card_no):
    html_path = HTML_DIR / f"card{card_no:02d}.html"
    jpg_path  = HTML_DIR / f"card{card_no:02d}.jpg"
    if not html_path.exists():
        print(f"  ❌ {html_path.name} 없음")
        return False

    print(f"\n[JPG 생성] card{card_no:02d}.jpg")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900}, device_scale_factor=3)
        page.goto(f"file://{html_path.resolve()}")
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)

        page.evaluate("""() => {
            const panel = document.querySelector('.preview-panel');
            if (panel) { panel.style.height = 'auto'; panel.style.overflow = 'visible'; }
            const wrap = document.querySelector('.card-wrap');
            if (wrap) { wrap.style.overflow = 'visible'; }
        }""")
        time.sleep(0.5)

        el = page.query_selector("#preview")
        if not el:
            print("  ❌ #preview 요소 없음")
            browser.close()
            return False

        box = el.bounding_box()
        page.set_viewport_size({"width": 1400, "height": int(box["height"]) + 100})
        time.sleep(0.3)
        el.screenshot(path=str(jpg_path), type="jpeg", quality=92)
        browser.close()
    print(f"  저장: {jpg_path.name} ({jpg_path.stat().st_size // 1024}KB)")
    return True


# ── 문구 검수 ─────────────────────────────────────────────────────────────

def load_inject_data():
    import importlib.util
    spec = importlib.util.spec_from_file_location("inject", BASE_DIR / "scripts" / "inject_images.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CARD_HEADER, mod.CARD_DEFAULTS

def check_html_text(card_no, card_header, card_defaults):
    html_path = HTML_DIR / f"card{card_no:02d}.html"
    if not html_path.exists():
        return False, [f"HTML 파일 없음"]

    html = html_path.read_text(encoding="utf-8")
    issues = []

    # 제목 확인
    header = card_header.get(card_no, {})
    title_words = header.get("title", "").replace("{", "").replace("}", "").replace("\n", " ").split()
    for word in title_words:
        if word and word not in html:
            issues.append(f"제목 누락: '{word}'")

    # 섹션 제목·본문 확인 (HTML에는 중괄호 그대로 저장됨)
    for sec in card_defaults.get(card_no, []):
        sec_title_raw = sec["title"]  # 중괄호 포함 그대로 비교
        body_snippet = sec["body"][:15]
        if sec_title_raw not in html:
            issues.append(f"[{sec['no']}] 섹션제목 누락: '{sec_title_raw}'")
        if body_snippet not in html:
            issues.append(f"[{sec['no']}] 본문 누락: '{body_snippet}...'")

    return len(issues) == 0, issues

def check_image_orientation(img_path: Path):
    """PIL로 이미지 방향 확인 — 가로(landscape) 여부 반환"""
    try:
        from PIL import Image
        with Image.open(img_path) as img:
            w, h = img.size
        return w > h, w, h
    except Exception as e:
        return None, 0, 0

def review_card(card_no, card_header, card_defaults):
    is_odd = (card_no % 2 == 1)
    gender = "홀수(남)" if is_odd else "짝수(여)"
    html_ok, issues = check_html_text(card_no, card_header, card_defaults)

    card_dir = IMG_DIR / f"card{card_no:02d}"
    img_files = [card_dir / f"card{card_no:02d}_01_headline.webp"] + \
                [card_dir / f"card{card_no:02d}_{i:02d}.webp" for i in range(1, 7)]
    missing_imgs = [f.name for f in img_files if not f.exists()]

    # 방향 검수: 섹션 이미지(01~06)만 가로(landscape) 확인 — 표지(headline)는 1024×1024 정사각 정상
    orientation_issues = []
    section_files = [card_dir / f"card{card_no:02d}_{i:02d}.webp" for i in range(1, 7)]
    for f in section_files:
        if not f.exists():
            continue
        is_landscape, w, h = check_image_orientation(f)
        if is_landscape is False:
            orientation_issues.append(f"{f.name} 정사각/세로 ({w}×{h}) — 가로(landscape) 여야 함")

    jpg_path = HTML_DIR / f"card{card_no:02d}.jpg"
    jpg_ok = jpg_path.exists()

    all_ok = html_ok and not missing_imgs and not orientation_issues and jpg_ok
    return {
        "card": card_no,
        "gender": gender,
        "html_ok": html_ok,
        "html_issues": issues,
        "missing_imgs": missing_imgs,
        "orientation_issues": orientation_issues,
        "jpg_ok": jpg_ok,
        "jpg_size": jpg_path.stat().st_size // 1024 if jpg_ok else 0,
        "pass": all_ok,
    }


# ── 메인 ─────────────────────────────────────────────────────────────────

def process_card(card_no):
    print(f"\n{'='*50}")
    print(f"  카드 {card_no:02d} 처리 시작")
    print(f"{'='*50}")

    if has_all_images(card_no):
        print(f"\n[이미지 생성] 스킵 (이미 존재)")
    else:
        ok = run(f"python3 scripts/generate_card_images.py --card {card_no}", "이미지 생성")
        if not ok: return False

    ok = run(f"python3 scripts/inject_images.py --card {card_no}", "HTML 주입")
    if not ok: return False

    ok = generate_jpg(card_no)
    if not ok: return False

    print(f"\n✅ card{card_no:02d} 생성 완료")
    return True

def parse_cards(args):
    cards = []
    for a in args:
        if '-' in a:
            s, e = a.split('-')
            cards.extend(range(int(s), int(e)+1))
        else:
            cards.append(int(a))
    return sorted(set(cards))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cards", nargs="+", required=True)
    parser.add_argument("--review-only", action="store_true",
                        help="생성 없이 검수만 실행")
    args = parser.parse_args()
    cards = parse_cards(args.cards)

    print(f"🚀 파이프라인 시작: 카드 {cards}")

    gen_results = {}
    if not args.review_only:
        for c in cards:
            gen_results[c] = process_card(c)
    else:
        gen_results = {c: True for c in cards}

    # 검수
    print(f"\n\n{'='*50}")
    print("🔍 문구·파일 검수")
    print(f"{'='*50}")
    card_header, card_defaults = load_inject_data()

    review_results = {}
    for c in cards:
        rev = review_card(c, card_header, card_defaults)
        review_results[c] = rev

    # 최종 리포트
    print(f"\n\n{'='*50}")
    print("📋 최종 검수 리포트")
    print(f"{'='*50}")
    all_pass = True
    for c in cards:
        rev = review_results[c]
        gen_ok = gen_results.get(c, True)
        status = "✅" if (gen_ok and rev["pass"]) else "❌"
        if not (gen_ok and rev["pass"]): all_pass = False

        line = f"  card{c:02d} [{rev['gender']}]  {status}"
        if rev["jpg_ok"]:
            line += f"  JPG {rev['jpg_size']}KB"
        print(line)

        if not rev["html_ok"]:
            for issue in rev["html_issues"]:
                print(f"         ⚠ {issue}")
        if rev["missing_imgs"]:
            print(f"         ⚠ 이미지 누락: {', '.join(rev['missing_imgs'])}")
        if rev["orientation_issues"]:
            for oi in rev["orientation_issues"]:
                print(f"         ⚠ 방향오류: {oi}")

    print(f"\n  {'✅ 전체 통과' if all_pass else '❌ 일부 요주의'}")
    print(f"\n📁 {HTML_DIR}")
    for c in cards:
        jpg = HTML_DIR / f"card{c:02d}.jpg"
        if jpg.exists():
            print(f"  {jpg.name}  {jpg.stat().st_size // 1024}KB")

if __name__ == "__main__":
    main()
