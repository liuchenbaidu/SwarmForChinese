from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import json

# 加载 .env 文件中的环境变量
load_dotenv()

# 定义工具函数
def get_current_weather(location, unit="celsius"):
    """获取指定位置的当前天气"""
    # 这里用模拟数据代替实际的天气API调用
    weather_info = {
        "location": location,
        "temperature": "22",
        "unit": unit,
        "forecast": ["sunny", "windy"]
    }
    return json.dumps(weather_info)

# 从环境变量初始化 AzureOpenAI 客户端
client = AzureOpenAI(
    api_key=os.getenv('AZURE_API_KEY'),      
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),   
    api_version=os.getenv('AZURE_API_VERSION')    
)

# 定义可用的工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定位置的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如 '北京'、'上海'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

def process_tool_calls(assistant_message, messages):
    """处理工具调用并返回更新后的消息列表"""
    if not assistant_message.tool_calls:
        return False

    # 首先添加 assistant 的工具调用消息
    messages.append({
        "role": "assistant",
        "content": None,
        "tool_calls": assistant_message.tool_calls
    })

    # 然后处理所有工具调用并添加响应
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # 调用相应的函数
        if function_name == "get_current_weather":
            function_response = get_current_weather(
                location=function_args.get("location"),
                unit=function_args.get("unit", "celsius")
            )
            
            # 添加工具响应
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": function_response
            })
    
    return True

try:
    # 发送带有工具的请求
    messages = [{"role": "user", "content": "北京，上海今天天气怎么样？"}]
    
    response = client.chat.completions.create(
        model=os.getenv('AZURE_DEPLOYMENT_NAME'),
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    # 处理响应
    assistant_message = response.choices[0].message
    
    print(assistant_message,"\n",type(assistant_message),"\n",assistant_message.tool_calls)
    # 检查是否需要调用工具
    if process_tool_calls(assistant_message, messages):
        # 发送第二次请求以获取最终调用工具的归纳总结
        second_response = client.chat.completions.create(
            model=os.getenv('AZURE_DEPLOYMENT_NAME'),
            messages=messages
        )
        
        print(second_response.choices[0].message.content)
    else:
        print(assistant_message.content)
    
except Exception as e:
    print(f"Error occurred: {str(e)}")
