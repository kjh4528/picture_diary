from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
response = client.messages.create(   #client.chat.completions.create
    model='claude-haiku-4-5-20251001', #'gpt-5.4-nano'
    max_tokens= 300,
    system= '당신은 친절한 한국어 ai 면접 코치입니다.',
    messages=[
        {'role':'user', 'content':'백엔드 개발자 면접 준비를 시작하는 사람에게 첫 조언을 3문장으로 해줘.'}
    ]
)

print(response)

