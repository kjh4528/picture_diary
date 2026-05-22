import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client

# API KEY 로드 확인
load_dotenv()
api_key : str|None = os.getenv('FAL_KEY')
print(f'[환경확인] FAL_KEY: {"loaded" if api_key else "키 없음"}')

# 캐릭터 생성 프롬프트
ARIA_BS_PROMPT = (
    '젊은 여성 AI 비서 아리아, 짧은 검은 머리, 따뜻한 갈색 눈,'
    '파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소, 상반신 샷,'
    '50mm 렌즈, 눈높이, 영화 같은 조명, 사실적인 표현'
)

print('fal.ai FLUX-schnell 호출 시작 = 약 5 ~ 15초 소요 예상...')

# fal_client 비동기 호출 - 응답이 올 때까지 기다릴 필요 없음. 큐 등록 -> 완료 대기 -> 결과 반환 처리
# 지금은 동기방식 호출
result = fal_client.subscribe(
    'fal-ai/flux/schnell',
    arguments= {
        'prompt': ARIA_BS_PROMPT,
        'image_size':'landscape_4_3',
        'num_inference_steps': 4,     # 해당 모델 기준 4스텝 충분 
        'num_images': 1
    }
)

# 응답 구조 확인
fal_image_url = result["images"][0]["url"]
print(f'[응답구조] result["images"][0]["url"] = {fal_image_url}')


# URL에서 png 이미지를 다운로드해서 로컬에 저장
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
image_bytes = requests.get(fal_image_url).content


# 이미지 저장 
output_path = output_dir / "aria_fal.png"
output_path.write_bytes(image_bytes)

print(f"[저장완료] {output_path}")
