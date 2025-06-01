## error in this file


from dotenv import load_dotenv
import os 

import requests
import json


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OpenRouterApiKey")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

response = requests.post(
  url=f"{BASE_URL}/chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
  },
  data=json.dumps({
    "model": MODEL,
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

print(response.json())