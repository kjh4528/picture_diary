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

SCENE_SCHEMA_HINT = '''
반드시 JSON 객체로 답하세요.
최상위 키는 scenes입니다. 
각 장면은 scene_kr, prompt_en, shot, angle, light을 포함합니다. 
prompt_en은 영어 이미지 프롬프트입니다. '''

diary_text = '아리아는 비 오는 오후에 작은 카페 창가에서 낡은 지도를 발견했다.'

# 기본 호출 방법
response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages= [
        {'role': 'system', 'content': SCENE_SCHEMA_HINT},
        {'role': 'user', 'content': diary_text}
    ],
    response_format= {'type':'json_object'}
)

print(response.choices[0].message.content)