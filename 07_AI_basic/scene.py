import os
import base64
import requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import json
import fal_client

load_dotenv()
client = OpenAI() #fal_client

# 기본 프롬프트
APPEARANCE = (
    '젊은 여성 AI 비서 아리아, 짧은 검은 머리, 따뜻한 갈색 눈,'
    '파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소, 상반신 샷,'
    '50mm 렌즈, 눈높이, 영화 같은 조명, 사실적인 표현'
)

# 프롬프트 조합 함수
def build_prompt(scene: dict) -> str:
    parts = [
        APPEARANCE,
        f"{scene['shot']} shot",
        scene['angle'],
        scene['light'],
        f"{scene['lens']} lens",
        scene['composition']
        ]
    return ','.join(parts)

# 장면 설정 json
sample_scene = {
    'scene_id': 1,
    'scene_kr': 'Aria의 집중된 표정 클로즈업',
    'shot': 'CU',
    'angle': 'eye_level',
    'light': 'key light',
    'lens': '85mm tight',
    'composition': 'centered'
}

prompt = build_prompt(sample_scene)
print(prompt)

