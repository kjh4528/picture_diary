import os
import base64
import requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import json

# API KEY 로드 확인
load_dotenv()
api_key : str|None = os.getenv('OPENAI_API_KEY')
print(f'[환경확인] OPENAI_API_KEY: {"loaded" if api_key else "키 없음"}')

# OpenAI 클라이언트 생성
client = OpenAI()

def json_mode():
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        response_format={'type':'json_object'}, # 모델 응답이 일반 문장이 아니라 json 객체 형식(문법)이 되도록 강제
        # 모델에게 보내는 내용
        messages=[
            {'role':'system',  # 모델의 역할과 출력 규칙
            'content': (
            '당신은 한 줄 문장을 json 객체로 변환하는 도우미입니다.'
            '반드시 다음 형식으로만 답하세요:'
            '{"title":"제목 한 줄", "word_count":"단어수(정수)"}')
            },
            {'role':'user',  # 실제 요청 
            'content':'아리아가 도서관에서 책을 읽고 있습니다.'
            }
        ]
    )

    # 응답 객체에서 실제 텍스트(str)만 꺼내 python 객체(dict)로 변환(json.loads())
    result = json.loads(response.choices[0].message.content) 

    print(result)
    print(type(result)) # class 'dict'

def no_json_mode():
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        # response_format={'type':'json_object'}
        messages=[
            {
            'role':'system',
            'content': (
            '당신은 한 줄 문장을 json 객체로 변환하는 도우미입니다.'
            '반드시 다음 형식으로만 답하세요:'
            '{"title":"제목 한 줄", "word_count":"단어수(정수)"}'
            )
            },
            {
            'role':'user',
            'content':'아리아가 도서관에서 책을 읽고 있습니다.'
            }
        ]
    )

    result = response.choices[0].message.content # openAI API 응답 기본적으로 문자열(str)

    print(result)
    print(type(result))


if __name__ == '__main__':
    # print('--- JSON MODE ---')
    json_mode()

    # print('--- NO JSON MODE ---')
    # no_json_mode()