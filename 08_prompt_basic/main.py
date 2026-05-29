import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

def is_loaded(name):
    return bool(os.getenv(name))

def main():
    print("Hello from 08-prompt-basic!")


if __name__ == "__main__":
    main()
    