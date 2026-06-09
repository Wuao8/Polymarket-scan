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

    opportunities = []

    for m in markets:
        try:
            name = m.get("question", "no-name")
            price = float(m.get("lastTradePrice", 0))
            volume = float(m.get("volume", 0))

            if volume > 0 and (price >= 0.95 or price <= 0.05):
                opportunities.append(f"{name} | price: {price} | vol: {volume}")

        except:
            continue

    if not opportunities:
        send_message("🔎 Nessuna opportunità trovata al momento")
    else:
        msg = "🚨 OPPORTUNITÀ POLYMARKET:\n\n" + "\n\n".join(opportunities[:5])
        send_message(msg)
