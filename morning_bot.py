import requests
import os
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN is missing!")
if not TELEGRAM_CHAT_ID:
    raise Exception("TELEGRAM_CHAT_ID is missing!")
if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY is missing!")

def generate_morning_message():
    today = datetime.now().strftime("%A, %B %d")
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": f"Write a warm good morning message for {today}. Under 80 words. Include one motivational quote. Use 1-2 emojis."
            }
        ],
        "max_tokens": 200
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body
    )
    print("Groq API status:", response.status_code)
    print("Groq response:", response.text)
    data = response.json()
    return data["choices"][0]["message"]["content"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    r = requests.post(url, json=payload)
    print("Telegram status:", r.status_code)
    print("Telegram response:", r.text)

print("Starting bot...")
message = generate_morning_message()
print("Generated message:", message)
send_telegram_message(message)
print("Done!")
