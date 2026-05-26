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


prompt = "Aria sitting by the cafe window on a rainy afternoon, examing an old map"
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
output_path = output_dir / "day3-4.png"
output_path.write_bytes(image_bytes)

print(f"[저장완료] {output_path}")