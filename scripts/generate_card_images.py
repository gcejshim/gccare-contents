"""
간기능개선 카드뉴스 이미지 자동생성 (Gemini API)
card02, card03, card04 전용 (card01은 건드리지 않음)

실행:
  python3 generate_card_images.py           # 카드 2, 3, 4 전부
  python3 generate_card_images.py --card 2  # 특정 카드만

출력:
  images/card02/header.png  + sec_01.png ~ sec_06.png
  images/card03/...
  images/card04/...
"""

import os
import sys
import time
import base64
import argparse
import requests
from io import BytesIO
from pathlib import Path
from PIL import Image

# ====================================================================
# 설정
# ====================================================================

GEMINI_API_KEY = "AIzaSyCJHM9kLbO3T6GPa2Gg40OsvnSWhi49SIw"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.5-flash-image:generateContent?key={GEMINI_API_KEY}"
)

OPENAI_API_KEY = "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"

BASE_DIR     = Path(__file__).parent.parent
IMAGES_DIR   = BASE_DIR / "images"
REF_DIR      = IMAGES_DIR / "ref-images"
REF_HEADLINE = REF_DIR / "headline"
REF_SEC_MALE = REF_DIR / "section_male"
REF_SEC_FEM  = REF_DIR / "section_female"

# ====================================================================
# 카드 데이터 (엑셀 기획서 기반)
# ====================================================================

CARDS = {
    2: {
        "title":    "AST·ALT·γ-GTP\n쉽게 이해하기",
        "subtitle": "건강검진 수치, 이렇게 읽으세요",
        "sections": [
            {
                "no": "01", "title": "간수치 해석법",
                "scene": "Korean person sitting at desk intently reading a medical checkup report, focused analytical expression, documents spread on desk"
            },
            {
                "no": "02", "title": "헷갈리는 영문",
                "scene": "Korean person looking confused and puzzled at a medical document, multiple question marks floating around their head, tilting head in confusion"
            },
            {
                "no": "03", "title": "AST 의미",
                "scene": "Korean male character doing weight training or push-ups, flexing muscles, energetic and athletic pose, sweat drops"
            },
            {
                "no": "04", "title": "ALT 특징",
                "scene": "Korean character with a worried expression holding their side (liver area), sensitive and slightly uncomfortable pose, hand on abdomen"
            },
            {
                "no": "05", "title": "γ-GTP 신호",
                "scene": "Korean male character sitting at a drinking table with alcohol glass, warning or caution symbol appearing above, slightly unsteady expression"
            },
            {
                "no": "06", "title": "함께 봐야 합니다",
                "scene": "Korean character looking at three separate items together with a thoughtful and wise expression, comparing and connecting multiple things"
            },
        ],
    },
    3: {
        "title":    "지방간이란\n무엇인가",
        "subtitle": "술 안 마셔도 생길 수 있어요",
        "sections": [
            {
                "no": "01", "title": "지방간 경고",
                "scene": "Korean character eating fast food or junk food late at night, red warning sign or alarm symbol nearby, guilty expression"
            },
            {
                "no": "02", "title": "증상이 없습니다",
                "scene": "Korean character appearing cheerful and healthy on the outside, but looking slightly unaware, calm and unsuspecting expression"
            },
            {
                "no": "03", "title": "지방간이란?",
                "scene": "Korean character with a large round belly, holding stomach area, showing excess fat accumulation, pudgy friendly appearance"
            },
            {
                "no": "04", "title": "왜 생길까?",
                "scene": "Korean character eating sugary sweets and snacks while sitting idle on a couch, sedentary unhealthy lifestyle scene"
            },
            {
                "no": "05", "title": "방치하면 위험",
                "scene": "Korean character looking scared at a small problem growing bigger, alarmed expression, danger signal growing larger"
            },
            {
                "no": "06", "title": "지금 시작하세요!",
                "scene": "Korean character putting on sneakers getting ready to walk or jog, motivated bright expression, first step of healthy habit"
            },
        ],
    },
    14: {
        "title":    "간에 좋은\n식사 패턴 만들기",
        "subtitle": "간 건강은 습관에서 시작됩니다",
        "sections": [
            {
                "no": "01", "title": "식사 패턴이 중요합니다",
                "scene": "Korean female character sitting at a nicely set dining table with a balanced healthy meal, calm and content expression, peaceful mealtime atmosphere"
            },
            {
                "no": "02", "title": "끼니 거르지 않기",
                "scene": "Korean female character looking very hungry with an empty stomach, holding her stomach with an exaggerated starving expression, a clock showing it is past mealtime visible nearby"
            },
            {
                "no": "03", "title": "아침 먹는 습관",
                "scene": "Korean female character sitting at a breakfast table in bright morning light eating a simple healthy breakfast, refreshed and energetic morning expression"
            },
            {
                "no": "04", "title": "식사 순서 바꾸기",
                "scene": "Object-only composition, no human character. An extremely large divided plate that fills the entire frame edge to edge. Left half packed with colorful 3D clay vegetables and protein foods (broccoli, carrots, chicken, tofu). Right half holds a mound of white rice. One large bold blue arrow pointing toward the vegetables side, one bold red arrow pointing toward the rice side. Ultra close-up view — the plate occupies 90% of image height, almost no empty space around it. Clean 3D clay style."
            },
            {
                "no": "05", "title": "가공식품 줄이기",
                "scene": "Object-only composition, no human character. A red warning or X symbol placed over 3D clay processed food items: instant ramen, chips bag, and canned goods. Clean cautionary composition on white background."
            },
            {
                "no": "06", "title": "작은 변화부터 시작",
                "scene": "Korean female character holding a monthly calendar and cheerfully checking off completed healthy meal habit days with a pen, satisfied and motivated expression, suggesting consistent small daily progress"
            },
        ],
    },
    12: {
        "title":    "단백질 중심\n식단 시작하기",
        "subtitle": "간 건강을 위한 단백질 식습관",
        "sections": [
            {
                "no": "01", "title": "단백질이 중요합니다",
                "scene": "Korean female character confidently holding a plate full of colorful protein foods (egg, chicken, tofu, fish), proud and cheerful expression, wellness educator pose"
            },
            {
                "no": "02", "title": "왜 단백질이 필요할까?",
                "scene": "Korean female character lightly flexing arm muscle with a curious and energetic expression, suggesting protein builds strength, simple and expressive pose"
            },
            {
                "no": "03", "title": "포만감 유지 효과",
                "scene": "Korean female character sitting at a table looking satisfied and content after eating, hands gently on stomach, relaxed full expression"
            },
            {
                "no": "04", "title": "좋은 단백질 고르기",
                "scene": "Object-only composition, no human character. Beautiful 3D clay flat-lay of protein foods: chicken breast, salmon fillet, tofu block, and eggs arranged neatly together on white background."
            },
            {
                "no": "05", "title": "피해야 할 단백질도 있다",
                "scene": "Korean female character making a cautious stop gesture toward a plate of bacon strips and fatty pork belly, concerned warning expression"
            },
            {
                "no": "06", "title": "한 끼씩 바꿔보세요!",
                "scene": "Korean female character at a dining table thoughtfully swapping a bowl of white rice for a protein-rich meal with chicken and vegetables, small decisive gesture, motivated expression"
            },
        ],
    },
    4: {
        "title":    "내 간수치\n상승 원인 찾기",
        "subtitle": "일상 속 습관을 점검하세요",
        "sections": [
            {
                "no": "01", "title": "간수치 원인 찾기",
                "scene": "Korean detective character holding a magnifying glass searching for hidden clues, investigative curious expression"
            },
            {
                "no": "02", "title": "숨은 원인",
                "scene": "Korean character surrounded by small hidden bad habits floating around them (late night snacking, sitting too long), surprised discovery expression"
            },
            {
                "no": "03", "title": "음주 패턴 체크",
                "scene": "Object-only composition, no human character. A glass of beer or soju bottle placed next to a monthly calendar with several dates circled or marked in red, suggesting frequent drinking pattern. Clean minimal arrangement on white background."
            },
            {
                "no": "04", "title": "체중·식습관 확인",
                "scene": "Korean character standing on a weighing scale looking down at the number, unhealthy snacks visible nearby, worried expression"
            },
            {
                "no": "05", "title": "운동·수면 점검",
                "scene": "Korean female character looking tired with dark circles, sitting slouched beside a bed, holding an alarm clock and looking at it with a weary expression. A pair of unused running shoes visible nearby. The character conveys the feeling of poor sleep and lack of exercise."
            },
            {
                "no": "06", "title": "원인을 찾아보세요!",
                "scene": "Korean character holding a checklist and pen, thoughtfully checking off lifestyle habits, confident determined expression"
            },
        ],
    },
    5: {
        "title":    "지방간의 종류와\n관리법 알기",
        "subtitle": "술만의 문제가 아닙니다",
        "sections": [
            {
                "no": "01", "title": "술만의 문제가 아닙니다",
                "scene": "Korean male character looking surprised and concerned, holding an alcohol glass in one hand while the other hand points to unhealthy food items nearby, realizing fatty liver is not only caused by alcohol. Puzzled yet eye-opening expression."
            },
            {
                "no": "02", "title": "지방간도 종류가 있다",
                "scene": "Object-only composition, no human character. Two distinct groups of 3D clay objects side by side: left group has a soju or beer bottle representing alcoholic fatty liver; right group has unhealthy snacks and a burger representing non-alcoholic fatty liver. A clean visual divider between the two groups. Pure white background."
            },
            {
                "no": "03", "title": "알코올성 지방간",
                "scene": "Korean male character sitting at a table with multiple drinks in front of him, looking slightly dazed and unhealthy, holding a glass of alcohol with a cautious warning expression. One or two bottles visible. Slightly unsteady but aware expression suggesting liver strain from alcohol."
            },
            {
                "no": "04", "title": "비알코올성 지방간",
                "scene": "Korean male character sitting on a couch eating unhealthy snacks, looking sedentary and slightly overweight, surrounded by junk food. Relaxed but unhealthy lifestyle scene suggesting diet and lack of exercise as fatty liver causes."
            },
            {
                "no": "05", "title": "마른 사람도 위험",
                "scene": "Korean male character who is visibly slim and thin, looking shocked and alarmed at a health checkup result showing a fatty liver warning. Unexpected surprised expression — the character clearly looks healthy on the outside but the report says otherwise."
            },
            {
                "no": "06", "title": "관리법은 다릅니다",
                "scene": "Object-only composition, no human character. Split composition: left side shows a no-alcohol symbol (crossed-out drink bottle in 3D clay), right side shows healthy food items and a small exercise icon (vegetables, water bottle, sneakers). Clean dividing line between two distinct management approaches. Pure white background."
            },
        ],
    },
    6: {
        "title":    "지방간을 방치하면\n어떻게 될까?",
        "subtitle": "초기에 관리할수록 회복 가능성이 높아요",
        "sections": [
            {
                "no": "01", "title": "방치하면 위험합니다",
                "scene": "Korean female character looking dismissive, waving off a health warning sheet with a carefree shrug while a clock behind her shows time passing. Slightly worried undertone despite dismissive gesture."
            },
            {
                "no": "02", "title": "1단계, 단순 지방간",
                "scene": "Object-only composition, no human character. A 3D clay liver organ with a few small yellow fat droplets on its surface. Mild, early-stage look. Soft green glow suggesting it is still recoverable. Pure white background."
            },
            {
                "no": "03", "title": "2단계, 지방간염",
                "scene": "Object-only composition, no human character. A 3D clay liver with more fat deposits and red inflammation spots on its surface. A small red warning triangle nearby. More troubled appearance than stage 1. Pure white background."
            },
            {
                "no": "04", "title": "증상이 없을 수도 있다",
                "scene": "Korean female character smiling and looking outwardly healthy, but holding a health report in hand showing concerning liver values. Contrast between normal outward appearance and hidden health concern inside."
            },
            {
                "no": "05", "title": "섬유화·간경변 위험",
                "scene": "Object-only composition, no human character. A 3D clay liver with hardened cracked fibrous texture, rigid and stiff looking. Dark warning coloring. Cracked surface showing liver fibrosis and cirrhosis progression. Pure white background."
            },
            {
                "no": "06", "title": "중요한 건 조기 관리",
                "scene": "Korean female character looking proactive and decisive, holding a lifestyle checklist with checkmarks, smiling confidently. A healthy green plant or small calendar nearby suggesting ongoing daily management."
            },
        ],
    },
    7: {
        "title":    "지방간 개선의\n핵심 3가지",
        "subtitle": "생활습관 개선만으로도 충분히 좋아질 수 있어요",
        "sections": [
            {
                "no": "01", "title": "생활습관이 핵심",
                "scene": "Korean male character standing confidently in action pose, surrounded by healthy lifestyle items — a running shoe, a vegetable, and a water bottle arranged nearby. Determined, action-ready expression."
            },
            {
                "no": "02", "title": "체중 감량 시작하기",
                "scene": "Korean male character standing on a weight scale looking pleasantly surprised and pleased, giving a thumbs up. Happy expression at the result."
            },
            {
                "no": "03", "title": "복부비만 관리",
                "scene": "Korean male character wrapping a measuring tape around their waist, looking focused and satisfied. Confident expression showing active self-management."
            },
            {
                "no": "04", "title": "식습관 바꾸기",
                "scene": "Korean male character sitting at a table, pushing aside unhealthy junk food and pulling toward a healthy plate of vegetables and grilled chicken. Deliberate positive food choice expression."
            },
            {
                "no": "05", "title": "꾸준한 운동 습관",
                "scene": "Korean male character walking briskly, wearing comfortable workout clothes, looking energetic and happy. A fitness watch on wrist. Active outdoor walking scene."
            },
            {
                "no": "06", "title": "중요한 건 꾸준함",
                "scene": "Korean male character looking at a habit tracker calendar with multiple consecutive checkmarks on daily boxes, looking satisfied and proud of maintaining healthy habits."
            },
        ],
    },
    8: {
        "title":    "체중 5% 감량이\n간에 미치는 효과",
        "subtitle": "작은 변화가 간 건강에 큰 변화를 만들어요",
        "sections": [
            {
                "no": "01", "title": "5% 감량의 힘",
                "scene": "Korean female character looking amazed and happy, holding a health improvement chart showing positive liver changes after weight loss. Pleasantly surprised, encouraged expression."
            },
            {
                "no": "02", "title": "간 지방 감소 시작",
                "scene": "Object-only composition, no human character. A 3D clay liver with fat droplets visibly melting away and decreasing in number, showing early recovery. A gentle green healing glow beginning to appear. Pure white background."
            },
            {
                "no": "03", "title": "생각보다 작은 목표",
                "scene": "Object-only composition, no human character. A 3D clay balance scale with a large weight block on one side and a small weight block on the other, a checkmark symbol showing the small goal is achievable. Pure white background."
            },
            {
                "no": "04", "title": "천천히 줄이기",
                "scene": "Korean female character walking steadily at a calm, unhurried pace looking relaxed and patient. A slow and steady expression. A gentle upward slope visible ahead suggesting gradual progress."
            },
            {
                "no": "05", "title": "작은 습관 변화",
                "scene": "Korean female character choosing a water bottle over a sugary drink with one hand, while putting on walking shoes with the other. Two small healthy choices happening simultaneously. Positive motivated expression."
            },
            {
                "no": "06", "title": "중요한 건 꾸준함",
                "scene": "Korean female character looking at a habit calendar with consistent daily checkmarks across many days, looking calm and satisfied. Long-term healthy routine theme."
            },
        ],
    },
    9: {
        "title":    "금주·절주\n실천 가이드",
        "subtitle": "간을 위한 음주 습관 점검",
        "sections": [
            {
                "no": "01", "title": "술이 간을 지칩니다",
                "scene": "Korean male character looking tired and fatigued, slumped at a table surrounded by several empty drink glasses. Weary, worn-out expression showing the toll of frequent drinking."
            },
            {
                "no": "02", "title": "금주 효과가 빠른 이유",
                "scene": "Object-only composition, no human character. A 3D clay bar chart showing liver enzyme bars decreasing from left to right with a green downward trend arrow. Visual of rapidly improving liver values after stopping alcohol. Pure white background."
            },
            {
                "no": "03", "title": "절주부터 시작하기",
                "scene": "Korean male character carefully holding just one small glass of alcohol, with a 'no' or crossed-out symbol gesture toward a larger bottle nearby. Controlled, intentional expression showing moderation and restraint."
            },
            {
                "no": "04", "title": "회식 전 전략 세우기",
                "scene": "Korean male character at a dinner table deliberately choosing protein foods and vegetable side dishes, looking strategic and prepared. Planning expression, deliberate healthy food selection before drinking."
            },
            {
                "no": "05", "title": "술자리 습관 바꾸기",
                "scene": "Korean male character drinking a glass of water between alcoholic drinks at a social setting, eating food slowly, looking relaxed and in control. Water glass is prominent in the scene."
            },
            {
                "no": "06", "title": "간 회복도 중요합니다",
                "scene": "Korean male character drinking a large glass of water and resting peacefully on a couch, looking calm and nurturing. Recovery and rest after drinking theme."
            },
        ],
    },
    10: {
        "title":    "하루 7,000보\n걷기 챌린지",
        "subtitle": "작은 걸음이 간 건강을 바꿉니다",
        "sections": [
            {
                "no": "01", "title": "걷기부터 시작하세요",
                "scene": "Korean female character walking energetically with a big smile, arms swinging naturally, wearing comfortable shoes. A fitness tracker on wrist. Active, positive walking expression."
            },
            {
                "no": "02", "title": "왜 걷기가 중요할까?",
                "scene": "Object-only composition, no human character. A 3D clay walking shoe with a heart symbol and a small flame icon representing fat burning placed nearby. Simple clean representation of walking as aerobic exercise. Pure white background."
            },
            {
                "no": "03", "title": "복부비만 감소 효과",
                "scene": "Korean female character measuring their waist with a measuring tape, looking pleasantly surprised at a smaller measurement than expected. Happy, encouraged expression."
            },
            {
                "no": "04", "title": "왜 7,000보일까?",
                "scene": "Object-only composition, no human character. A row of seven 3D clay footprint shapes leading toward a large heart symbol, representing the daily step goal as a path to heart and liver health. Clean, symbolic visualization. Pure white background."
            },
            {
                "no": "05", "title": "일상 속 걷기 습관",
                "scene": "Korean female character choosing to take the stairs instead of the elevator, carrying a bag, looking active and motivated. Daily life scene showing habitual walking as natural choice."
            },
            {
                "no": "06", "title": "중요한 건 꾸준함",
                "scene": "Korean female character wearing comfortable walking shoes, looking at a calendar with checkmarks on consecutive daily boxes, looking satisfied and content. Long-term walking streak theme."
            },
        ],
    },
    11: {
        "title":    "지방간 관리의\n탄수화물 줄이기",
        "subtitle": "술보다 위험할 수도 있어요",
        "sections": [
            {
                "no": "01", "title": "술보다 위험할 수 있습니다",
                "scene": "Korean male character looking alarmed, holding a large bowl of white rice and a sugary drink, with an expression of surprise realizing these are more dangerous than expected for his liver."
            },
            {
                "no": "02", "title": "왜 탄수화물이 문제일까?",
                "scene": "Object-only composition, no human character. A 3D clay liver with sugar cubes and bread rolls being transformed into fat droplets piling onto it, showing carbohydrates converting to liver fat. Pure white background."
            },
            {
                "no": "03", "title": "혈당을 빠르게 올리는 음식",
                "scene": "Object-only composition, no human character. A cluster of 3D clay high-glycemic foods grouped tightly together: white rice bowl, bread slice, ramen noodles, and a sugary drink can. Warning visual composition. Pure white background."
            },
            {
                "no": "04", "title": "먼저 줄여야 할 음식",
                "scene": "Korean male character pushing away a plate of snacks and instant noodles with a determined expression. A clear rejection gesture toward unhealthy carbohydrate snacks."
            },
            {
                "no": "05", "title": "중요한 건 바꾸기",
                "scene": "Object-only composition, no human character. Split composition: left side shows white rice and a sugary drink (crossed out); right side shows a multigrain rice bowl and a water bottle (approved). Simple swap visualization. Pure white background."
            },
            {
                "no": "06", "title": "작은 변화가 시작입니다",
                "scene": "Korean male character looking satisfied and confident, eating a bowl of multigrain rice with vegetables. A positive, healthy meal choice with an encouraging expression."
            },
        ],
    },
    13: {
        "title":    "야식이\n지방간을 만드는 이유",
        "subtitle": "밤에 먹는 습관이 간을 힘들게 해요",
        "sections": [
            {
                "no": "01", "title": "밤에 먹는 습관",
                "scene": "Korean male character sitting on a couch late at night eating snacks, with a dark window showing nighttime outside. Relaxed but unhealthy late-night eating habit scene."
            },
            {
                "no": "02", "title": "왜 밤에 먹으면 안 될까?",
                "scene": "Object-only composition, no human character. A 3D clay clock showing late night time next to a liver with fat droplets accumulating on it, symbolizing reduced metabolism at night leads to fat storage. Pure white background."
            },
            {
                "no": "03", "title": "밤에 더 위험한 이유",
                "scene": "Object-only composition, no human character. Two identical 3D clay food portions side by side — one labeled 'day' (minimal fat) and one labeled 'night' (more fat on liver). Same food, different outcome visualization. Pure white background."
            },
            {
                "no": "04", "title": "야식이 만드는 변화",
                "scene": "Object-only composition, no human character. A 3D clay spread of typical late-night foods clustered together: ramen cup, fried chicken piece, beer can. Warning visual representing unhealthy liver impact. Pure white background."
            },
            {
                "no": "05", "title": "수면까지 방해합니다",
                "scene": "Korean male character lying in bed unable to sleep, looking uncomfortable with a full stomach, clock showing late hour. Late eating disrupting sleep quality scene."
            },
            {
                "no": "06", "title": "잠들기 전 3시간",
                "scene": "Object-only composition, no human character. A 3D clay clock showing the recommended cutoff time, with a crossed-out food plate nearby and a pillow/moon icon symbolizing healthy sleep preparation. Pure white background."
            },
        ],
    },
}

# ====================================================================
# 스타일 프롬프트
# ====================================================================

SECTION_STYLE = """
🚫 ABSOLUTE RULES — NEVER VIOLATE UNDER ANY CIRCUMSTANCES:
1. ZERO TEXT. No letters, no words, no numbers, no Korean, no English, no symbols, no labels, no captions, no watermarks, no signs, no writing of any kind anywhere in the image. If ANY text appears, the image is rejected.
2. PURE WHITE BACKGROUND (#FFFFFF) ONLY. The background must be completely solid pure white with zero gradients, zero color tints, zero floor shadows, zero reflections, zero patterns, zero textures. Nothing but #FFFFFF.

## 이미지 생성 스타일
- 부드러운 파스텔 기반의 미니멀 3D 클레이 일러스트
- 30대 한국인 성인 인물
- 귀엽지만 너무 어려 보이지 않는 분위기
- 눈모양: 흰자위가 보이는 눈매에 검은 동공, 살짝 처진 눈매
- 둥글고 말랑한 형태감
- 차분하고 편안한 웰니스 무드
- 깔끔한 모바일 앱 일러스트 스타일
- 전체적으로 맑고 깨끗한 쿨톤 무드
- 따뜻한 베이지/노란 조명 느낌 제거
- 형태와 실루엣이 부드럽지만 명확하게 보이도록 표현
- 과하게 흐릿하지 않은 정돈된 렌더링

## 컬러
- 전체 컬러는 밝고 부드러운 비비드 파스텔 계열을 기본으로 한다.
- soft clean pastel colors — avoid dull, muddy, or washed-out colors
- 전체 색감은 뉴트럴~쿨톤 기반으로 유지한다.
- 회색끼와 누런끼 없이 깨끗하고 산뜻한 톤으로 표현한다.
- 아이보리, 크림빛, 노란 베이지 계열 사용 최소화
- 화이트는 깨끗한 쿨 화이트 느낌으로 표현
- 블루, 민트계열의 은은한 쿨톤 기운을 아주 미세하게 활용
- #4BD48C와 유사한 녹색을 오브젝트 한 곳에만 은은한 포인트 컬러로 사용한다.
- 남자 캐릭터 상의 옷색 #BAD0F1, 여자 캐릭터 상의 옷색 #FEEAB0 컬러를 기본으로 사용
- 포인트 녹색은 전체를 지배하지 않도록 작고 자연스럽게 배치한다.
- 사물은 본연의 컬러를 기본적으로 유지한다.

## 조명과 질감
- 은은한 하이라이팅과 밝은 명도를 더한다.
- 부드러운 조명과 은은한 그림자를 사용한다.
- 강한 명암 대비는 피한다.
- 전체 조명은 깨끗하고 맑은 자연광 느낌의 쿨 화이트 톤
- 노란 조명, 텅스텐 느낌, 웜톤 그림자 금지
- 실사 느낌 없이 단순하고 정돈된 3D 클레이 질감으로 표현한다.
- 질감 표현은 너무 흐리지 않게, 표면 경계와 입체감을 살짝 더 명확하게 표현
- 흐릿하거나 뿌연 느낌 없이 깨끗하고 선명한 렌더링
- soft ambient lighting with clean highlights, clear but soft shape definition

## 배경과 구성
- 배경은 항상 순수한 #FFFFFF (그라데이션, 바닥 반사, 그림자 없음)
- 이미지 비율은 항상 14:9 (가로형 와이드 포맷)
- 오브젝트/인물이 프레임을 가득 채우도록 크게 배치한다. 상하좌우 여백을 최소화하여 빈 공간이 없게 한다.
- 주요 오브젝트는 이미지 높이의 85~95%를 차지하도록 크게 그린다.
- 오브젝트는 인물을 포함해 최대 4개까지만 사용한다.
- 여러 오브젝트를 쓸 때는 서로 가깝게 모아서 배치한다. 오브젝트를 캔버스에 넓게 분산하지 말고, 중앙에 밀집시켜 빈 공간이 생기지 않도록 한다.
- 메인 오브젝트 1~2개는 크고 굵게, 나머지는 곁에 붙여 보조로 배치한다.
- 배경 그림자와 바닥 반사는 최소화하여 더 깨끗한 인상 유지

## 금지 사항
- ⛔ 텍스트/글자/한글/영문/숫자/기호 삽입 절대 금지 — 단 하나의 글자도 허용 안 됨
- ⛔ 배경은 반드시 순수 흰색(#FFFFFF)만 — 그라데이션·색조·바닥·그림자·텍스처 일절 금지
- 복잡한 배경 금지
- 실사 느낌 금지
- 과한 디테일 금지
- 강한 명암 대비 금지
- 선명한 원색 금지
- 애니메이션/픽사 스타일 금지
- 어린아이처럼 보이는 얼굴 금지
- 복잡한 소품 추가 금지
- 노란끼 도는 피부톤 금지
- 웜톤 필터 느낌 금지
- 과하게 뿌옇거나 흐린 표현 금지
- muddy colors 금지 / washed-out colors 금지

## 일관성
- 처음 생성된 캐릭터의 얼굴형, 비율, 피부 톤, 헤어 스타일, 전체 조형감, 색감, 조명 스타일을 이후 이미지에서도 최대한 동일하게 유지한다.
- 이후 생성 이미지에서도 동일한 쿨톤 화이트 밸런스와 밝은 렌더링 유지

## 인물 구성
- 모든 섹션에 사람이 등장할 필요는 없다.
- 장면의 내용이 개념 설명이나 사물로 더 잘 전달된다면 인물 없이 오브젝트/아이콘만으로 구성한다.
- 6개 섹션 중 약 2개는 인물 없이 사물 중심 구성으로 표현한다.
- NOTE: Not every scene requires a human character. If the scene is better expressed with objects or concepts alone, illustrate it without a person. Across the 6 sections, approximately 2 should be object-only compositions.
"""

HEADLINE_STYLE_ODD = """
Bold modern health infographic card cover. Dark navy background (#0D1F3C).
Bright green (#0AC262) accent. Health/medical 3D icon (liver or stethoscope). Square format.

Display this Korean text EXACTLY with perfect character accuracy:
제목 (크고 굵게): {title}
부제목 (작게): {subtitle}
"""

HEADLINE_STYLE_EVEN = """
Bold modern health infographic card cover. Bright vivid green (#0AC262) background.
White and dark text. Health/medical 3D illustration element. Square format. Clean and energetic.

Display this Korean text EXACTLY with perfect character accuracy:
제목 (크고 굵게): {title}
부제목 (작게): {subtitle}
"""

# ====================================================================
# 헬퍼: 이미지 → base64
# ====================================================================

def load_ref_images(folder: Path, max_count: int = 3, max_px: int = 768) -> list[str]:
    """참조 이미지 로드 — PNG/JPG/WEBP 모두 지원, 큰 이미지는 max_px 기준 리사이즈"""
    exts = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.PNG", "*.JPG", "*.WEBP")
    files = []
    for ext in exts:
        files.extend(folder.glob(ext))
    files = sorted(set(files))[:max_count]
    result = []
    for p in files:
        img = Image.open(p).convert("RGB")
        if max(img.size) > max_px:
            img.thumbnail((max_px, max_px), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        result.append(base64.b64encode(buf.getvalue()).decode())
    return result


# ====================================================================
# Gemini 이미지 생성
# ====================================================================

CARD_HEADLINE_BOTTOM = {
    5: """MATCH THE REFERENCE IMAGE EXACTLY — same style, same quality:
- Background: deep dark navy blue (#0D1F3C) with large semi-transparent decorative circles in corners, diagonal accent shapes — identical to reference
- NO subtitle text, NO banner ribbon, NO badge. Title text ONLY.
- ⚠️ CRITICAL — TITLE TEXT MUST BE EXACTLY: 지방간의 종류와 관리법 알기
  Do NOT change, rephrase, or rewrite this title. Render these exact Korean characters, nothing else.
  Display across 3 lines: "지방간의" / "종류와 관리법" / "알기"
  First line in bright green (#0AC262), second and third lines in white.
  Bold, slightly glossy 3D-style font — same as reference. NOT flat cartoon. NOT deeply extruded.
- BOTTOM ILLUSTRATION (lower 30%, EXACTLY 2 objects — no more, no less):
  - Left: unhealthy fatty liver character (yellowish-brown bumpy texture, worried sweating face — same 3D clay cartoon style as reference liver)
  - Right: Korean male character (30s, light blue polo shirt, raising one index finger — exact same style and quality as reference character)
  - ABSOLUTELY NO other objects: no bottles, no food, no props, no additional characters""",
}

CARD_HEADLINE_CUSTOM_PROMPT = {}

# 부제목을 헤드라인에 표시하지 않을 카드 번호
CARD_HEADLINE_NO_SUBTITLE = {5}

# 카드별 레이아웃/일러스트 추가 지시 (제목은 항상 CARDS dict에서 자동 사용)
CARD_HEADLINE_BOTTOM.update({
    4: """LAYOUT NOTES:
- Same green gradient style as reference (do NOT use purple/blue background)
- Same decorative elements: circles, X marks, dashes
- TOP BADGE text (small, above title): "내 간수치 왜 올랐을까?"
- LEFT SPEECH BUBBLE: "원인이\n뭘까?"
- RIGHT SPEECH BUBBLE: "지금\n점검!" """,

    6: """LAYOUT NOTES:
- Same green gradient style as reference (do NOT use purple/blue background)
- Same decorative elements: circles, X marks, dashes
- TOP BADGE text (small, above title): "지방간의 진행 단계를 알아보세요"
- LEFT SPEECH BUBBLE: "방치하면\n어떻게?"
- RIGHT SPEECH BUBBLE: "단계별\n확인!" """,

    8: """LAYOUT NOTES:
- Same green gradient style as reference (do NOT use purple/blue background)
- Same decorative elements: circles, X marks, dashes
- TOP BADGE text (small, above title): "작은 감량, 큰 간 변화!"
- LEFT SPEECH BUBBLE: "왜 5%\n감량?"
- RIGHT SPEECH BUBBLE: "효과\n확인!" """,

    10: """LAYOUT NOTES:
- Same green gradient style as reference (do NOT use purple/blue background)
- Same decorative elements: circles, X marks, dashes
- TOP BADGE text (small, above title): "걸으면 간이 좋아져요!"
- LEFT SPEECH BUBBLE: "왜 7,000\n보일까?"
- RIGHT SPEECH BUBBLE: "지금\n도전!" """,

    12: """LAYOUT NOTES:
- Same green gradient style as reference (do NOT use purple/blue background)
- Same decorative elements: circles, X marks, dashes
- TOP BADGE text (small, above title): "간 건강의 핵심, 단백질 식단!"
- LEFT SPEECH BUBBLE: "왜 단백질\n이 좋을까?"
- RIGHT SPEECH BUBBLE: "식단\n바꾸기!" """,

    14: """LAYOUT NOTES:
- Same green gradient style as reference (do NOT use purple/blue background)
- Same decorative elements: circles, X marks, dashes
- TOP BADGE text (small, above title): "간 건강의 시작, 식습관부터!"
- LEFT SPEECH BUBBLE: "습관이\n핵심!"
- RIGHT SPEECH BUBBLE: "지금\n시작!"
- NO characters or food images at the bottom. NO subtitle below the title.""",
})


def generate_headline_gpt(title: str, subtitle: str, is_odd: bool, ref_head: list[str] = None, retries: int = 3, card_no: int = None) -> bytes:
    """GPT-image-1으로 헤드라인 이미지 생성 — 참고 이미지 스타일 반영"""
    from openai import OpenAI
    import base64 as _b64

    client = OpenAI(api_key=OPENAI_API_KEY)

    # 기본 프롬프트: 제목은 항상 CARDS dict에서 그대로 사용
    show_subtitle = card_no not in CARD_HEADLINE_NO_SUBTITLE if card_no else True
    if show_subtitle:
        base_prompt = (
            f"참고 이미지와 완전히 동일한 스타일, 색상, 레이아웃으로 헬스 카드뉴스 표지를 생성해줘.\n\n"
            f"아래 한글 텍스트를 글자 획 하나도 틀리지 않게 정확히 표시해줘:\n"
            f"- 제목 (크고 굵게): {title.replace(chr(10), ' ')}\n"
            f"- 부제목 (작게): {subtitle}\n\n"
            f"텍스트는 절대 임의로 변형하지 마. 그대로 정확하게 렌더링."
        )
    else:
        base_prompt = (
            f"참고 이미지와 완전히 동일한 스타일, 색상, 레이아웃으로 헬스 카드뉴스 표지를 생성해줘.\n\n"
            f"아래 한글 텍스트를 글자 획 하나도 틀리지 않게 정확히 표시해줘:\n"
            f"- 제목 (크고 굵게): {title.replace(chr(10), ' ')}\n\n"
            f"텍스트는 절대 임의로 변형하지 마. 그대로 정확하게 렌더링. 부제목은 이미지에 표시하지 마."
        )

    # 카드별 완전 커스텀 프롬프트가 있으면 사용 (제목 포함 전체 지정)
    if card_no and card_no in CARD_HEADLINE_CUSTOM_PROMPT:
        prompt_text = CARD_HEADLINE_CUSTOM_PROMPT[card_no]
    # 하단 일러스트만 커스텀이 있으면 기본 제목 프롬프트에 추가
    elif card_no and card_no in CARD_HEADLINE_BOTTOM:
        prompt_text = base_prompt + "\n\n" + CARD_HEADLINE_BOTTOM[card_no]
    else:
        prompt_text = base_prompt

    content = []
    for img_data in ref_head:
        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{img_data}"
        })
    content.append({"type": "input_text", "text": prompt_text})

    for attempt in range(retries):
        try:
            response = client.responses.create(
                model="gpt-4o",
                input=[{"role": "user", "content": content}],
                tools=[{"type": "image_generation", "quality": "low", "size": "1024x1024"}],
            )
            for item in response.output:
                if item.type == "image_generation_call":
                    return _b64.b64decode(item.result)
            raise ValueError("응답에 이미지 없음")
        except Exception as e:
            if attempt < retries - 1:
                wait = 15 * (attempt + 1)
                print(f"    GPT 에러 → {wait}초 후 재시도 ({attempt+1}/{retries}): {e}")
                time.sleep(wait)
            else:
                raise


def generate_image(prompt: str, ref_images: list[str], retries: int = 3) -> bytes:
    parts = []
    for img_data in ref_images:
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_data}})
    parts.append({"text": prompt})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    for attempt in range(retries):
        try:
            resp = requests.post(GEMINI_URL, json=payload, timeout=120)
            resp.raise_for_status()
            for part in resp.json()["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    return base64.b64decode(part["inlineData"]["data"])
            raise ValueError("응답에 이미지 없음")
        except requests.HTTPError as e:
            if resp.status_code in (500, 429) and attempt < retries - 1:
                wait = 15 * (attempt + 1)
                print(f"    {resp.status_code} 에러 → {wait}초 후 재시도 ({attempt+1}/{retries})")
                time.sleep(wait)
            else:
                raise


# ====================================================================
# 카드 처리
# ====================================================================

def process_card(card_no: int, skip_headline: bool = False):
    card = CARDS[card_no]
    out_dir = IMAGES_DIR / f"card{card_no:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*55}")
    print(f"  카드 {card_no:02d}: {card['title'].replace(chr(10), ' ')}")
    print(f"{'='*55}")

    # 참고 이미지 로드 (홀수=card01+card03스타일/남자, 짝수=card02스타일/여자)
    is_odd = (card_no % 2 == 1)
    odd_keywords = {"card01", "card03"}
    head_files = sorted([f for f in REF_HEADLINE.iterdir()
                         if not f.name.startswith('.')
                         and (any(k in f.stem for k in odd_keywords) if is_odd else "card02" in f.stem)])[:2]
    ref_head = []
    for f in head_files:
        img = Image.open(f).convert("RGB")
        if max(img.size) > 768:
            img.thumbnail((768, 768), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        ref_head.append(base64.b64encode(buf.getvalue()).decode())

    # card14는 card04 헤드라인을 스타일 참조로 사용
    if card_no == 14:
        card04_head = IMAGES_DIR / "card04" / "card04_01_headline.webp"
        if card04_head.exists():
            img = Image.open(card04_head).convert("RGB")
            if max(img.size) > 768:
                img.thumbnail((768, 768), Image.LANCZOS)
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=85)
            ref_head = [base64.b64encode(buf.getvalue()).decode()]

    ref_sec_dir = REF_SEC_MALE if is_odd else REF_SEC_FEM
    ref_sec = load_ref_images(ref_sec_dir, 3)
    print(f"  참고이미지 — headline: {len(ref_head)}장 ({'홀수' if is_odd else '짝수'}호 스타일), section: {len(ref_sec)}장 ({'male' if is_odd else 'female'})")

    def save_as_webp(img_bytes: bytes, out_path: Path, quality: int = 85):
        """Gemini 응답 이미지를 WebP로 변환 저장"""
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        buf = BytesIO()
        img.save(buf, format="WEBP", quality=quality)
        out_path.write_bytes(buf.getvalue())

    # ── headline ──────────────────────────────────────────────────
    if not skip_headline:
        head_out = out_dir / f"card{card_no:02d}_01_headline.webp"
        if head_out.exists():
            print(f"\n  [헤드라인] 스킵 (이미 존재)")
        else:
            print(f"\n  [헤드라인] GPT-image-1 생성 중... (참고이미지 {len(ref_head)}장)")
            try:
                img_bytes = generate_headline_gpt(card["title"], card["subtitle"], is_odd, ref_head, card_no=card_no)
                save_as_webp(img_bytes, head_out)
                print(f"    저장: {head_out} ({head_out.stat().st_size//1024}KB)")
            except Exception as e:
                print(f"    실패: {e}")

    # ── sections ─────────────────────────────────────────────────
    for sec in card["sections"]:
        out_path = out_dir / f"card{card_no:02d}_{sec['no']}.webp"
        if out_path.exists():
            print(f"\n  [{sec['no']}] {sec['title']} — 스킵")
            continue
        print(f"\n  [{sec['no']}] {sec['title']}")
        gender_ko = "30대 한국인 남성" if card_no % 2 == 1 else "30대 한국인 여성"
        clothing = "#BAD0F1 (연한 블루)" if card_no % 2 == 1 else "#FEEAB0 (연한 옐로우)"
        prompt = (
            f"⛔ CRITICAL: NO TEXT OF ANY KIND. NO LETTERS. NO WORDS. NO NUMBERS. ZERO TEXT ANYWHERE. "
            f"⛔ CRITICAL: BACKGROUND MUST BE PURE SOLID WHITE (#FFFFFF) ONLY. NO GRADIENTS. NO SHADOWS. NO FLOOR.\n\n"
            f"Generate a new illustration in EXACTLY the same 3D clay render style as the reference images above. "
            f"Copy the rendering style, material feel, lighting, and color palette precisely.\n\n"
            f"{SECTION_STYLE}\n\n"
            f"CHARACTER: 이 카드의 주인공은 {gender_ko} 1인이다. 상의 옷색은 반드시 {clothing}를 사용한다. "
            f"모든 섹션에서 동일한 인물이 등장한다. (단, 장면에 따라 두 사람이 함께 등장할 수 있다.)\n\n"
            f"IMPORTANT: Output must be WIDE 14:9 LANDSCAPE format. Horizontal composition. "
            f"FILL THE FRAME — objects/characters must be LARGE and occupy 85–95% of the image height. "
            f"Minimize empty white space on all sides. The illustration should feel full and bold, not floating in empty space. "
            f"When multiple objects are used, cluster them tightly together in the center — do NOT spread them across the canvas. "
            f"1–2 main objects should be large and dominant; additional objects are placed close beside them as accents.\n\n"
            f"Scene to illustrate: {sec['scene']}\n\n"
            f"⛔ FINAL REMINDER: ABSOLUTELY NO TEXT, NO LETTERS, NO SYMBOLS ANYWHERE IN THE IMAGE. "
            f"BACKGROUND IS PURE WHITE (#FFFFFF) ONLY — NO EXCEPTIONS."
        )
        try:
            img_bytes = generate_image(prompt, ref_sec)
            save_as_webp(img_bytes, out_path)
            print(f"    저장: {out_path} ({out_path.stat().st_size//1024}KB)")
        except Exception as e:
            print(f"    실패: {e}")

    total = 1 + len(card["sections"])
    print(f"\n  완료: {out_dir}/ ({total}개 파일)")


# ====================================================================
# 메인
# ====================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", type=int, choices=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                        help="특정 카드만 생성")
    parser.add_argument("--no-headline", action="store_true",
                        help="헤드라인 이미지 생성 건너뜀")
    args = parser.parse_args()

    target_cards = [args.card] if args.card else [2, 3, 4]

    print("🚀 간기능개선 카드뉴스 이미지 생성 시작")
    print(f"   대상 카드: {target_cards}")

    for card_no in target_cards:
        process_card(card_no, skip_headline=args.no_headline)

    print(f"\n{'='*55}")
    print("✅ 완료!")


if __name__ == "__main__":
    main()
