from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量初始化 AzureOpenAI 客户端
client = AzureOpenAI(
    api_key=os.getenv('AZURE_API_KEY'),      # API密钥
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),   # Azure端点
    api_version=os.getenv('AZURE_API_VERSION')    # API版本
)

try:
    # 使用客户端进行操作
    response = client.chat.completions.create(
        model=os.getenv('AZURE_DEPLOYMENT_NAME'),  # 部署名称
        messages=[
            {"role": "user", "content": "树上3只鸟，地上3只鸟，打了一枪还有几只"}
        ]
    )
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"Error occurred: {str(e)}")
