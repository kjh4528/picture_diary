"""
agents/image.py — 장면 프롬프트 → 이미지 생성 (gpt-image-1-mini / fal.ai FLUX)

역할:
    gpt-image-1-mini(OpenAI) 또는 fal-client(FLUX)를 사용해
    scene.py가 추출한 영문 프롬프트를 이미지로 변환하고, 로컬에 저장합니다.

    model="dalle" → gpt-image-1-mini (DALL-E 후속, ~$0.005/장)
    model="flux"  → fal-ai/flux/schnell (~$0.003/장)

사용 함수:
    generate_image(prompt, output_path, model) → str  (단일 장면)
    generate_images(scenes, out_dir, model)   → list[str]  (4장면 일괄)
"""

import os
import time
from pathlib import Path

import fal_client
import httpx
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# FLUX 모델 설정
# ---------------------------------------------------------------------------
FLUX_MODEL_ID = "fal-ai/flux/schnell"  # 빠른 추론 FLUX 모델 (무료 티어 가능)
# 필요 시 "fal-ai/flux/dev" 또는 "fal-ai/flux-pro" 로 교체

IMAGE_SIZE = "landscape_4_3"      # 4:3 가로 비율 — 그림일기에 적합
NUM_INFERENCE_STEPS = 4           # schnell 권장값 (4~8)
OUTPUT_FORMAT = "jpeg"


# ---------------------------------------------------------------------------
# 핵심 함수
# ---------------------------------------------------------------------------

def generate_image(prompt: str, output_path: str, model: str = "dalle") -> str:
    """
    영문 프롬프트 한 개를 받아 이미지를 생성하고 파일로 저장합니다.

    Args:
        prompt:      이미지 생성 영문 프롬프트 (scene.py의 'prompt_en' 값)
        output_path: 저장할 파일 경로 (예: "outputs/scene_1.jpg")
        model:       사용할 모델 — "dalle" (기본값) 또는 "flux"

    Returns:
        저장된 파일의 경로 문자열

    Raises:
        ValueError:       model 값이 "dalle" / "flux" 이외일 때
        RuntimeError:     API 호출 실패 또는 이미지 URL이 없을 때
        httpx.HTTPError:  이미지 다운로드 실패 시
    """
    load_dotenv()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if model == "dalle":
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다. "
                ".env 파일에 OPENAI_API_KEY=your_key_here 를 추가하세요."
            )
        # gpt-image-1-mini: DALL-E 3 후속 모델, low 품질로 FLUX schnell과 비용 근접 (~$0.005/장)
        # 응답이 base64로 오므로 URL 다운로드 없이 직접 디코딩하여 저장
        import base64
        client = OpenAI()
        gpt_response = client.images.generate(
            model="gpt-image-1-mini",
            prompt=prompt,
            size="1536x1024",   # 가로 비율 landscape (gpt-image-1 계열 지원 사이즈)
            quality="low",      # low = 가장 저렴, FLUX schnell과 비용 유사
            n=1,
        )
        image_bytes = base64.b64decode(gpt_response.data[0].b64_json)
        output_path.write_bytes(image_bytes)
        print(f"[저장 완료] {output_path}  ({len(image_bytes) // 1024} KB)")
        return str(output_path)

    elif model == "flux":
        if not os.getenv("FAL_KEY"):
            raise RuntimeError(
                "FAL_KEY 환경 변수가 설정되지 않았습니다. "
                ".env 파일에 FAL_KEY=your_key_here 를 추가하세요."
            )
        result = fal_client.run(
            FLUX_MODEL_ID,
            arguments={
                "prompt": prompt,
                "image_size": IMAGE_SIZE,
                "num_inference_steps": NUM_INFERENCE_STEPS,
                "num_images": 1,
                "output_format": OUTPUT_FORMAT,
                "enable_safety_checker": False,
            },
        )
        images = result.get("images")
        if not images:
            raise RuntimeError(f"이미지 URL이 응답에 없습니다. 응답: {result}")
        image_url = images[0]["url"]

    else:
        raise ValueError(f"지원하지 않는 model: '{model}'. 'dalle' 또는 'flux'를 사용하세요.")

    # URL에서 파일 다운로드 (flux는 url 응답)
    with httpx.Client(timeout=60) as client:
        response = client.get(image_url)
        response.raise_for_status()
        output_path.write_bytes(response.content)

    print(f"[저장 완료] {output_path}  ({len(response.content) // 1024} KB)")
    return str(output_path)


def generate_images(
    scenes: list[dict],
    out_dir: Path,
    model: str = "dalle",
) -> list[str]:
    """
    scene.py가 반환한 4개 장면 리스트를 받아 이미지를 일괄 생성합니다.

    Args:
        scenes:  extract_scenes()가 반환한 list[dict] (scene_kr, prompt_en 포함)
        out_dir: 이미지를 저장할 디렉터리
        model:   사용할 모델 — "dalle" (기본값) 또는 "flux"

    Returns:
        생성된 이미지 파일 경로 문자열 리스트 (장면 순서 유지)

    Notes:
        요청 간 1초 대기로 레이트 리밋을 방지합니다.
    """
    out_dir = Path(out_dir)
    ext = "png" if model == "dalle" else OUTPUT_FORMAT  # gpt-image-1-mini는 PNG 반환
    paths = []

    for i, scene in enumerate(scenes, 1):
        prompt = scene["prompt_en"]
        print(f"\n[장면 {i}/{len(scenes)}] 생성 중... (model={model})")
        print(f"  프롬프트: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

        output_path = out_dir / f"scene_{i}.{ext}"
        saved = generate_image(prompt, output_path, model=model)
        paths.append(saved)

        if i < len(scenes):
            time.sleep(1)

    print(f"\n[완료] {len(paths)}개 이미지 생성됨 → {out_dir}")
    return paths


# ---------------------------------------------------------------------------
# 단독 실행 (테스트용)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json

    # 테스트할 모델 선택: "dalle" 또는 "flux"
    TEST_MODEL = "flux"

    sample_prompt = (
        "wide shot, early morning alley, soft orange sunlight filtering through "
        "old buildings, wet pavement with fallen autumn leaves, no people, "
        "quiet atmosphere, watercolor diary illustration"
    )

    scene_file = Path("scene_extracted.json")

    if scene_file.exists():
        scenes = json.loads(scene_file.read_text(encoding="utf-8"))["scenes"]
        print(f"[불러오기] scene_extracted.json → 장면 {len(scenes)}개")
        paths = generate_images(scenes, Path("outputs"), model=TEST_MODEL)
        for p in paths:
            print(f"  {p}")
    else:
        print(f"[테스트] scene_extracted.json 없음 → 샘플 프롬프트로 단일 이미지 테스트 (model={TEST_MODEL})")
        ext = "png" if TEST_MODEL == "dalle" else OUTPUT_FORMAT
        path = generate_image(sample_prompt, Path(f"outputs/test_scene.{ext}"), model=TEST_MODEL)
        print(f"[테스트 완료] {path}")
