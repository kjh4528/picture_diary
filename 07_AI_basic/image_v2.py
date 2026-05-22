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
BASE_PROMPT = (
    '한국인 여성 20대 중반 아리아, 은은한 하이라이트가 들어간 짧은 검은 머리, 따뜻한 갈색 눈,'
    '파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소,'
    '사실적인 표현'
)

# 6종 샷 사이즈 레퍼런스 
SHOT_SIZES = {
    'ECU': ('extreme close-up', '감정 미세 변화, 눈빛 강조'),
    'CU': ('close-up', '얼굴 중심, SNS 프로필'),
    'BS': ('bust shot', '표준 포트레이트, 캐릭터 가드 기준'),
    'MS': ('medium shot', '제스처, 옷차림 포함'),
    'FS': ('full shot', '전신, 의상 카탈로그'),
    'WS': ('wide shot', '환경, 세계관 등 강조')
}

# 앵글 3종
ANGLES = ['eye_level', 'low angle', 'high angle'] # 기본, 올려보기, 내려보기 

# 조명 3종
LIGHTING_SETUPS = ['key light','fill light', 'back light'] # 주광, 보조광, 후면광 

# 렌즈 
LENSES = ['24mm wide', '50mm portrait', '85mm tight', '200mm', '400mm'] # 광각, 표준, 망원 ...

# 심도
DEPTHS = ['shallow depth of field', 'bokeh background', 'deep focus, sharp background']

# 구도
COMPOSITIONS = ['rule of thirds','centered composition', 'negative space, minimalist']

# 최종 프롬프트 
prompt = f'{BASE_PROMPT}, {SHOT_SIZES["BS"][0]}, {ANGLES[2]}, {LIGHTING_SETUPS[0]}, {LENSES[2]}, {DEPTHS[0]}, {COMPOSITIONS[0]}' 
print('최종 프롬프트: ', prompt) 


print('gpt-image-1.5 호출 시작 = 약 5 ~ 15초 소요 예상...')

response = client.images.generate(
    model="gpt-image-1.5",
    prompt=prompt,
    size="1024x1024",
    quality='low',
    n=1,
    output_format= 'png' # gpt-image 모델은 항상 base64 반환
)

# Base64 디코딩 후 저장 
image_b64 = response.data[0].b64_json
image_bytes = base64.b64decode(image_b64)

# 출력 경로 
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# 이미지 저장 
output_path = output_dir / "aria_v2.png"
output_path.write_bytes(image_bytes)

print(f"[저장완료] {output_path}")
