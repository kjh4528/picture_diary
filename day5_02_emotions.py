"""
day5_02_emoticons.py — 이모티콘 캐릭터 도메인 응용

역할:
    APPEARANCE 공통 외모 단서와 EMOTIONS 감정 딕셔너리를 사용해
    이모티콘 캐릭터 이미지 프롬프트를 생성하고, 이미지를 일괄 저장합니다.

핵심 변수:
    APPEARANCE: str          ← 캐릭터 공통 외모 단서
    EMOTIONS: dict[str, str] ← 감정별 표현 딕셔너리
"""

from pathlib import Path

from agents.image import generate_image

# ---------------------------------------------------------------------------
# 캐릭터 공통 외모 단서 — 채점 필수 변수
# ---------------------------------------------------------------------------
APPEARANCE: str = (
    "cute round character, simple face, white body, minimalist style, "
    "flat illustration, clean white background"
)

# ---------------------------------------------------------------------------
# 감정별 표현 딕셔너리 — 채점 필수 변수 (6개 초과 필요)
# ---------------------------------------------------------------------------
EMOTIONS: dict[str, str] = {
    "happy":       "big smile, rosy cheeks, sparkling eyes",
    "sad":         "teary eyes, drooping mouth, slumped shoulders",
    "angry":       "furrowed brows, red face, clenched fists",
    "surprised":   "wide eyes, open mouth, raised eyebrows",
    "excited":     "jumping, arms raised, huge grin",
    "tired":       "half-closed eyes, slouching, yawning",
    "wink":        "one eye closed, playful smile, thumbs up",
    "embarrassed": "blushing cheeks, nervous smile, hands on face",
}


# ---------------------------------------------------------------------------
# 프롬프트 생성 함수
# ---------------------------------------------------------------------------

def build_emoji_prompt(emotion: str) -> str:
    """
    감정 키를 받아 이모티콘 이미지 생성 프롬프트를 반환합니다.

    Args:
        emotion: EMOTIONS 딕셔너리의 키 (예: "happy")

    Returns:
        이미지 생성용 영문 프롬프트 문자열
    """
    expression = EMOTIONS.get(emotion, "neutral expression")
    return (
        f"{APPEARANCE}, {expression}, "
        "emoji sticker style, no text, no watermark, sharp focus"
    )


# ---------------------------------------------------------------------------
# 단독 실행
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    for emotion, expression in EMOTIONS.items():
        prompt = build_emoji_prompt(emotion)
        out_path = f"outputs/emoji_{emotion}.png"

        print(f"\n[생성] {emotion}")
        print(f"  프롬프트: {prompt[:80]}...")

        saved = generate_image(prompt=prompt, output_path=out_path, model="dalle")
        print(f"  저장: {saved}")
