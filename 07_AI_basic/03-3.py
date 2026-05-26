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

REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "prompt_en"]
SYSTEM_PROMPT = """
너는 그림일기 장면 추출 담당자입니다. 
반드시 JSON 개체로만 답합니다. 
최상위 키는 scenes입니다. 
각 장면은 scene_kr, prompt_en, shot, angle, light을 포함합니다. 
prompt_en은 영어 이미지 프롬프트입니다. 
장면은 최대 3개입니다."""

def validate_scenes(scene: list[dict]) -> None:
    missing = REQUIRED_FIELDS - set(scene)
    if missing:
        print(f"없는 필드: ", missing)

def extract_scenes(text: str) -> list[dict]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ]
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    scenes = data.get('scenes',[])[:3]

    for scene in scenes:
        validate_scenes(scenes)

    return scenes

if __name__ == "__main__":
    diary = '아리아는 비 오는 오후 카페 창가에서 낡은 지도를 발견했다.'
    for item in extract_scenes(diary):
        print(item['scene_kr'])
        print(item['prompt_en'])
