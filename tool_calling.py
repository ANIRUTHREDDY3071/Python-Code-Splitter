import requests
import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
  api_key=os.getenv("GROQ_API_KEY")
)

def get_weather(location):
   """Get weather for any city"""
   api_key = "8e7e6be936642d0c8454f4ba99a1d8d9"
   url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"

   response = requests.get(url)
   data = response.json()

   if data["cod"] == 200:
       return {
           "location": location,
           "temperature": data["main"]["temp"],
           "description": data["weather"][0]["description"]
       }
   else:
       return {"error": "City not found"}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name like Mumbai, London"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
messages = [
    {
        "role": "system",
        "content": "You are a weather assistant. Use get_weather function when asked about weather."
    },
    {
        "role": "user",
        "content": "What's the weather in Hyd?"
    }
]
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools,
    tool_choice="auto"   
)
print(response)
response_message = response.choices[0].message

if response_message.tool_calls:
    print("Model wants to use a tool!")
else:
    print("Model answered directly")

if response_message.tool_calls:
    tool_call = response_message.tool_calls[0]

    arguments = json.loads(tool_call.function.arguments)
    location = arguments["location"]
    print(f"LLM wants weather for: {location}")

    weather_data = get_weather(location)
    print(f"Weather data: {weather_data}")
    messages.append(response_message)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(weather_data)
    })
final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

print(final_response.choices[0].message.content)