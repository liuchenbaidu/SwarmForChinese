import json
import requests

from swarm import Agent


def get_weather(location, time="now"):
    """Get the current weather in a given location. Location MUST be a city."""
    # OpenWeatherMap API 配置
    API_KEY = "624004d0b118966014a55bed0810abde"  # 替换为你的 API key
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        # 发送 API 请求
        params = {
            "q": location,
            "appid": API_KEY,
            "units": "metric"  # 使用摄氏度
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        print("一次请求")
        
        weather_data = response.json()
        
        # 提取需要的天气信息
        return json.dumps({
            "location": location,
            "temperature": str(round(weather_data["main"]["temp"])),
            "description": weather_data["weather"][0]["description"],
            "humidity": str(weather_data["main"]["humidity"]),
            "time": time
        })
    except requests.RequestException as e:
        return json.dumps({
            "error": f"Failed to get weather data: {str(e)}",
            "location": location,
            "time": time
        })


def send_email(recipient, subject, body):
    print("Sending email...")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return "Sent!"


weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a helpful agent.",
    functions=[get_weather, send_email],
)
