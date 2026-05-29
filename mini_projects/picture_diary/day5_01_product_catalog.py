"""
day5_01_product_catalog.py — 제품 카탈로그 도메인 응용

역할:
    domains/product_prompts.json의 제품 장면 데이터를 읽어
    카탈로그 스타일 이미지 프롬프트를 생성하고, 이미지를 일괄 저장합니다.

핵심 함수:
    build_product_prompt(desc, background) → str
"""

import json
from pathlib import Path

from agents.image import generate_image

# ---------------------------------------------------------------------------
# 제품 목록 (list[dict]) — 채점 필수 변수
# ---------------------------------------------------------------------------
products: list[dict] = [
    {
        "name": "wireless earbuds",
        "desc": "compact wireless earbuds with charging case",
        "size": "small",
        "shape": "round",
    },
    {
        "name": "desk clock",
        "desc": "minimalist wooden desk clock with clean dial",
        "size": "small",
        "shape": "round",
    },
    {
        "name": "insulated tumbler",
        "desc": "sleek stainless steel insulated tumbler",
        "size": "medium",
        "shape": "cylindrical",
    },
]

# ---------------------------------------------------------------------------
# 보너스: shot_map / angle_map (선택 +2점) — 제품 특성 → 시각 어휘 매핑
# ---------------------------------------------------------------------------
shot_map: dict[str, str] = {
    "small":  "close-up shot",
    "medium": "medium shot",
    "large":  "wide shot",
}

angle_map: dict[str, str] = {
    "round":       "eye-level angle",
    "cylindrical": "slight low angle",
    "flat":        "top-down angle",
}


# ---------------------------------------------------------------------------
# 핵심 함수
# ---------------------------------------------------------------------------

def build_product_prompt(desc: str, background: str = "clean white background") -> str:
    """
    제품 설명 문자열을 받아 카탈로그 스타일 이미지 생성 프롬프트를 반환합니다.

    Args:
        desc:       제품 설명 문자열 (예: "compact wireless earbuds with charging case")
        background: 배경 설명 문자열 (기본값: "clean white background") — 보너스 파라미터

    Returns:
        이미지 생성용 영문 프롬프트 문자열
    """
    return (
        f"close-up product photography of {desc}, "
        f"{background}, studio lighting, 50mm macro lens, "
        "soft shadows, clean and professional look, "
        "no text, no watermark, sharp focus"
    )


# ---------------------------------------------------------------------------
# 단독 실행
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # domains/product_prompts.json 로드
    prompts_path = Path("domains/product_prompts.json")
    data = json.loads(prompts_path.read_text(encoding="utf-8"))
    print(f"[로드] {prompts_path}  도메인: {data['domain']}")

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # 제품 목록 순회 → 프롬프트 생성 → 이미지 저장
    for product in products:
        shot  = shot_map.get(product["size"], "medium shot")
        angle = angle_map.get(product["shape"], "eye-level angle")

        prompt = build_product_prompt(
            desc=f"{product['desc']}, {shot}, {angle}",
            background="clean white background",
        )

        out_path = f"outputs/product_{product['name'].replace(' ', '_')}.png"
        print(f"\n[생성] {product['name']}")
        print(f"  프롬프트: {prompt[:80]}...")

        saved = generate_image(prompt=prompt, output_path=out_path, model="dalle")
        print(f"  저장: {saved}")
