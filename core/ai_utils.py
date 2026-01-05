import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

def chatgpt_generate(prompt, model="gpt-4.1", temperature=0.7, max_tokens=512):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for product data entry."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
