from openai import OpenAI

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你好，你是谁？"},
        {"role": "user", "content": "写段python代码，计算1+2+...+100的和"},
    ],
    stream=False
)

print(response.choices[0].message.content)