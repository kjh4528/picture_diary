"""
agents/video.py — 이미지 → 영상 생성 (fal.ai image-to-video)

역할:
    image.py가 저장한 이미지 파일을 입력으로 받아
    fal.ai의 image-to-video 모델로 짧은 영상(.mp4)을 생성합니다.

    영상 생성은 이미지 생성보다 훨씬 오래 걸리기 때문에(30초~수분)
    fal_client.subscribe()를 사용해 완료될 때까지 내부적으로 폴링합니다.

사용 함수:
    generate_video(image_path, output_path) → str
"""

import os
import time
from pathlib import Path

import fal_client
import httpx
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# 모델 설정
# ---------------------------------------------------------------------------
# kling-video v2 master: 이미지 한 장 → 5초 영상, 실사·카메라무브 품질 우수
# 비용 ~$1.00/영상 (fal.ai 기준)
VIDEO_MODEL_ID = "fal-ai/kling-video/v2/master/image-to-video"


# ---------------------------------------------------------------------------
# 핵심 함수
# ---------------------------------------------------------------------------

def generate_video(image_path: str, output_path: str) -> str:
    """
    이미지 파일을 받아 fal.ai image-to-video 모델로 영상을 생성하고 저장합니다.

    Args:
        image_path:  입력 이미지 파일 경로 (예: "outputs/scene_1.png")
        output_path: 저장할 영상 파일 경로 (예: "outputs/scene_1.mp4")
                     반드시 .mp4 확장자여야 합니다.

    Returns:
        저장된 영상 파일의 경로 문자열

    Raises:
        FileNotFoundError: image_path 파일이 존재하지 않을 때
        RuntimeError:      FAL_KEY 누락, API 호출 실패, 영상 URL이 없을 때
        httpx.HTTPError:   영상 다운로드 실패 시

    Notes:
        fal_client.subscribe()는 내부적으로 폴링을 처리합니다.
        영상 생성은 보통 30초~3분 소요됩니다.
    """
    load_dotenv()

    # FAL_KEY 확인
    if not os.getenv("FAL_KEY"):
        raise RuntimeError(
            "FAL_KEY 환경 변수가 설정되지 않았습니다. "
            ".env 파일에 FAL_KEY=your_key_here 를 추가하세요."
        )

    # 입력 이미지 존재 확인
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"입력 이미지를 찾을 수 없습니다: {image_path}")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 1단계: 로컬 이미지를 fal CDN에 업로드 → 임시 URL 획득
    #         fal.ai 모델은 URL을 입력으로 받으므로 로컬 파일을 먼저 업로드합니다.
    print(f"[업로드] {image_path} → fal CDN")
    image_url = fal_client.upload_file(str(image_path))
    print(f"[업로드 완료] {image_url}")

    # 2단계: 영상 생성 요청 + 폴링
    #         subscribe()는 job을 제출하고 완료될 때까지 내부적으로 상태를 주기적으로
    #         확인(폴링)하다가 완료되면 결과를 반환합니다. (run()은 폴링 없이 즉시 반환)
    print(f"[생성 중] 모델: {VIDEO_MODEL_ID}  (30초~3분 소요)")
    start = time.time()

    result = fal_client.subscribe(
        VIDEO_MODEL_ID,
        arguments={
            "image_url": image_url,
            "prompt": "gentle camera movement, cinematic, smooth motion",
            "duration": "5",          # 5초 (기본값, "10"으로 변경 시 $2.80)
            "aspect_ratio": "16:9",
            "negative_prompt": "blur, distort, low quality",
            "cfg_scale": 0.5,
        },
        with_logs=False,
    )

    elapsed = time.time() - start
    print(f"[생성 완료] {elapsed:.0f}초 소요")

    # 3단계: 결과에서 영상 URL 추출
    video = result.get("video")
    if not video:
        raise RuntimeError(f"영상 URL이 응답에 없습니다. 응답: {result}")

    video_url = video.get("url")
    if not video_url:
        raise RuntimeError(f"video.url이 없습니다. 응답: {result}")

    # 4단계: URL에서 .mp4 다운로드 후 저장
    with httpx.Client(timeout=120) as client:
        response = client.get(video_url)
        response.raise_for_status()
        output_path.write_bytes(response.content)

    print(f"[저장 완료] {output_path}  ({len(response.content) // 1024} KB)")
    return str(output_path)


# ---------------------------------------------------------------------------
# 단독 실행 (테스트용)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json

    # scene_extracted.json + outputs/scene_1.* 이 있으면 첫 번째 장면으로 테스트
    scene_file = Path("scene_extracted.json")
    test_image = None

    # outputs/ 에서 첫 번째 이미지 탐색
    for ext in ("png", "jpg", "jpeg"):
        candidate = Path("outputs") / f"scene_1.{ext}"
        if candidate.exists():
            test_image = candidate
            break

    if test_image:
        print(f"[테스트] 입력 이미지: {test_image}")
        video_path = generate_video(
            image_path=str(test_image),
            output_path="outputs/scene_1.mp4",
        )
        print(f"[테스트 완료] {video_path}")
    else:
        print("[오류] outputs/scene_1.png(또는 .jpg) 파일이 없습니다.")
        print("먼저 agents/image.py를 실행해 이미지를 생성해 주세요.")
        raise SystemExit(1)
