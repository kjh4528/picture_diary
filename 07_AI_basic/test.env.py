from dotenv import load_dotenv
import os


# Load variables from .env
load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY")

def mask_key(key):
    return key[:15]

if open_ai_key is None:
    print("OPENAI_API_KEY not found in .env")
else:
    print("OPENAI_API_KEY loaded")
    print("Masked Key:", mask_key(open_ai_key))