import os
import base64
import requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# API KEY 로드 확인
load_dotenv()
api_key : str|None = os.getenv('OPENAI_API_KEY')
print(f'[환경확인] OPENAI_API_KEY: {"loaded" if api_key else "키 없음"}')

# OpenAI 클라이언트 초기화(키 자동 탐지)
client = OpenAI()

# 캐릭터 생성 프롬프트
ARIA_BS_PROMPT = (
    '젊은 여성 AI 비서 아리아, 짧은 검은 머리, 따뜻한 갈색 눈,'
    '파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소, 상반신 샷,'
    '50mm 렌즈, 눈높이, 영화 같은 조명, 사실적인 표현'
)

print('gpt-image-1 호출 시작 = 약 5 ~ 15초 소요 예상...')

# DALL-E 3 동기 호출 - 응답이 올 때까지 기다림
response = client.images.generate(
    model="gpt-image-1",
    prompt=ARIA_BS_PROMPT,
    size="1024x1024",
    quality='low',
    n=1,
    output_format= 'png' # gpt-image 모델은 항상 base64 반환
)

# 응답 구조 확인: b64_json 구조
image_b64 = response.data[0].b64_json
print(f'[응답구조] response.data[0].b64_json={image_b64[:60]}...')

# Base64 디코딩 후 저장 
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
image_bytes = base64.b64decode(image_b64)


# 이미지 저장 
output_path = output_dir / "aria_v1.png"
output_path.write_bytes(image_bytes)

print(f"[저장완료] {output_path}")
