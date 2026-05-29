"""
pipeline.py — 그림일기 멀티 LLM 파이프라인 진입점

흐름:
    일기 텍스트
        │
        ▼
    [1] extract_scenes()   → scenes: list[dict]
        │
        ▼
    [2] generate_image()   → images: list[str]   (4장 일괄)
        │
        ▼
    [3] generate_video()   → videos: list[str]   (선택)
        │
        ▼
    반환: {"scenes": [...], "images": [...], "videos": [...]}

사용 함수:
    picture_diary_pipeline(diary_text, image_model, generate_videos) → dict
"""

from pathlib import Path

from agents.image import generate_image
from agents.scene import extract_scenes
from agents.video import generate_video

OUTPUT_DIR = Path("outputs")


def picture_diary_pipeline(
    diary_text: str,
    image_model: str = "dalle",
    generate_videos: bool = False,
) -> dict:
    """
    일기 텍스트를 받아 장면 추출 → 이미지 생성 → (선택) 영상 생성을 순서대로 실행합니다.

    Args:
        diary_text:      일기 원문 문자열
        image_model:     이미지 생성 모델 — "dalle" (기본값) 또는 "flux"
        generate_videos: True이면 각 이미지에 대해 영상도 생성합니다 (선택)

    Returns:
        {
            "scenes": list[dict],   # 추출된 장면 리스트 (scene_kr, prompt_en)
            "images": list[str],    # 생성된 이미지 파일 경로 리스트
            "videos": list[str],    # 생성된 영상 파일 경로 리스트 (generate_videos=False 시 빈 리스트)
        }
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    # ── 1단계: 일기 텍스트 → 4개 장면 추출 ────────────────────────────────
    print("\n══ [1/3] 장면 추출 ══════════════════════════════")
    scenes = extract_scenes(diary_text)
    print(f"  추출 완료: {len(scenes)}개 장면")

    # ── 2단계: 장면 프롬프트 → 이미지 생성 ────────────────────────────────
    print(f"\n══ [2/3] 이미지 생성 (model={image_model}) ═══════")
    ext = "png" if image_model == "dalle" else "jpeg"
    images: list[str] = []

    for i, scene in enumerate(scenes, 1):
        print(f"\n  [장면 {i}/{len(scenes)}] {scene['scene_kr']}")
        output_path = str(OUTPUT_DIR / f"scene_{i}.{ext}")
        image_path = generate_image(
            prompt=scene["prompt_en"],
            output_path=output_path,
            model=image_model,
        )
        images.append(image_path)

    print(f"\n  이미지 생성 완료: {len(images)}장")

    # ── 3단계: 이미지 → 영상 생성 (선택) ──────────────────────────────────
    videos: list[str] = []

    if generate_videos:
        print(f"\n══ [3/3] 영상 생성 ════════════════════════════")
        for i, image_path in enumerate(images, 1):
            print(f"\n  [장면 {i}/{len(images)}]")
            video_path = generate_video(
                image_path=image_path,
                output_path=str(OUTPUT_DIR / f"scene_{i}.mp4"),
            )
            videos.append(video_path)
        print(f"\n  영상 생성 완료: {len(videos)}개")
    else:
        print("\n══ [3/3] 영상 생성 건너뜀 (generate_videos=False) ═")

    print("\n══ 파이프라인 완료 ════════════════════════════════")
    return {"scenes": scenes, "images": images, "videos": videos}


# ---------------------------------------------------------------------------
# 단독 실행
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    diary_path = Path("diary.md")
    if not diary_path.exists():
        print("[오류] diary.md 파일이 없습니다. 프로젝트 루트에서 실행해 주세요.")
        raise SystemExit(1)

    diary_text = diary_path.read_text(encoding="utf-8")
    print(f"[일기 로드] {len(diary_text)}자")

    result = picture_diary_pipeline(
        diary_text=diary_text,
        image_model="flux",      # "dalle" 또는 "flux"
        generate_videos=False,   # True로 바꾸면 영상까지 생성
    )

    print(f"\n장면 수  : {len(result['scenes'])}")
    print(f"이미지   : {result['images']}")
    print(f"영상     : {result['videos']}")
