import openai
from dotenv import load_dotenv
import os

## 금지
# client = openai.OpenAI(api_key='skXXXXXX')

# 프로젝트 폴더(root)에서 .env 파일 찾아서 로드 
load_dotenv()

api_key : str|None = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)


# .gitignore .env 추가 여부 확인
gitignore_path = '.gitignore'
try:
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if '.env' in content:
            print(".env is listed in .gitignore")
        else:
            print(".env is NOT listed in .gitignore")
except FileNotFoundError:
    print('.gitignore 파일 없음')