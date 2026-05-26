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

# 기본 호출 방법
response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages= [
        {'role': 'system', 'content': '짧고 친절하게 답하세요,'},
        {'role': 'user', 'content': '장면 추출이 무엇인지 한 문장으로 설명하세요.'}
    ]
)

print(response.choices[0].message.content)