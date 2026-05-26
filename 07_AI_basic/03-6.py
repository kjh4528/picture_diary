import os
import base64
import requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import json
import fal_client
from module0305 import get_client

if __name__ == "__main__":
    client = get_client()
    print(isinstance(client, OpenAI))