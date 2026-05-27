"""
agents/scene.py — 일기 텍스트 → 장면 JSON 자동 추출

역할:
    OpenAI Chat API (JSON 모드)를 사용해 일기 텍스트를 분석하고,
    그림으로 그릴 수 있는 4개의 장면을 JSON 형태로 추출합니다.

사용 함수:
    extract_scenes(diary_text) → list[dict]
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# 시스템 프롬프트 — JSON 스키마와 제약 조건을 명시합니다
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a visual scene extractor for an illustrated diary project.

Read the diary text and extract exactly 4 scenes that can be drawn as illustrations.

Return a JSON object with the following structure:
{
  "scenes": [
    {
      "scene_kr": "장면을 한국어로 한 문장으로 설명",
      "prompt_en": "English image generation prompt with shot/angle/lighting/style"
    }
  ]
}

Rules:
- "scenes" array must contain EXACTLY 4 items.
- "scene_kr" must be written in Korean.
- "prompt_en" must be written in English and include: shot type (wide shot / close-up / medium shot), lighting condition, and visual style.
- Always append ", watercolor diary illustration" at the end of every "prompt_en".
- Do NOT include any explanation or text outside the JSON object.
"""


def extract_scenes(diary_text: str) -> list[dict]:
    """
    일기 텍스트를 분석해 4개의 장면을 추출합니다.

    Args:
        diary_text: 일기 원문 문자열 (300~500자)

    Returns:
        list[dict]: 장면 딕셔너리 리스트.
                    각 딕셔너리에는 'scene_kr'(한국어 설명)과
                    'prompt_en'(영문 이미지 프롬프트)이 포함됩니다.

    Raises:
        ValueError: API 응답에 'scenes' 키가 없거나 장면 수가 4개가 아닐 때
        KeyError:   각 장면에 필수 키가 없을 때
    """
    load_dotenv()
    client = OpenAI()  # OPENAI_API_KEY를 환경 변수에서 자동 탐지

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diary_text},
        ],
        response_format={"type": "json_object"},  # JSON 모드: 반드시 유효한 JSON 반환
        temperature=0.7,
        max_tokens=1500,
    )

    raw = json.loads(response.choices[0].message.content)

    # 최상위 키 검증
    if "scenes" not in raw:
        raise ValueError(f"'scenes' 키가 응답에 없습니다. 받은 키: {list(raw.keys())}")

    scenes = raw["scenes"]

    # 장면 수 검증
    if len(scenes) != 4:
        raise ValueError(f"장면이 4개여야 합니다. 현재: {len(scenes)}개")

    # 각 장면 필수 키 검증
    for i, scene in enumerate(scenes):
        for key in ("scene_kr", "prompt_en"):
            if key not in scene:
                raise KeyError(f"장면 {i+1}에 '{key}' 키가 없습니다.")

    return scenes


def save_scenes(scenes: list[dict], out_path: Path) -> None:
    """
    추출된 장면 리스트를 JSON 파일로 저장합니다.

    Args:
        scenes:   extract_scenes()가 반환한 장면 리스트
        out_path: 저장할 파일 경로 (예: Path("scene_extracted.json"))
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({"scenes": scenes}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[저장 완료] {out_path}")


# ---------------------------------------------------------------------------
# 단독 실행 (테스트용)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    diary_path = Path("diary.md")
    if not diary_path.exists():
        print("[오류] diary.md 파일이 없습니다. 프로젝트 루트에서 실행해 주세요.")
        raise SystemExit(1)

    diary_text = diary_path.read_text(encoding="utf-8")
    print(f"[일기 로드] {len(diary_text)}자")

    scenes = extract_scenes(diary_text)
    print(f"[추출 완료] 장면 {len(scenes)}개\n")

    for i, scene in enumerate(scenes, 1):
        print(f"── 장면 {i} ──")
        print(f"  KR: {scene['scene_kr']}")
        print(f"  EN: {scene['prompt_en']}")

    save_scenes(scenes, Path("scene_extracted.json"))
