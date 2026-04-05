import requests
import os
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN is missing!")
if not TELEGRAM_CHAT_ID:
    raise Exception("TELEGRAM_CHAT_ID is missing!")
if not ANTHROPIC_API_KEY:
    raise Exception("ANTHROPIC_API_KEY is missing!")

def generate_morning_message():
    today = datetime.now().strftime("%A, %B %d")
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": f"Write a warm good morning message for {today}. Under 80 words. Include one motivational quote. Use 1-2 emojis."
            }
        ]
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=body
    )
    print("API status:", response.status_code)
    data = response.json()
    return data["content"][0]["text"]

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
