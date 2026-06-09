import requests
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

GAMMA_URL = "https://gamma-api.polymarket.com/markets"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def get_markets():
    r = requests.get(GAMMA_URL)
    return r.json()

if __name__ == "__main__":
    markets = get_markets()

    send_message(f"📊 Mercati trovati: {len(markets)}")
