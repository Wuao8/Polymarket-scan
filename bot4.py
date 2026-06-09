import requests
import os
from datetime import datetime

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
    now = datetime.utcnow()

    for m in markets:
        try:
            name = m.get("question", "no-name")
            price = float(m.get("lastTradePrice", 0))
            volume = float(m.get("volume", 0))

            end_date = m.get("endDate") or m.get("end_date")
            if not end_date:
                continue

            end = datetime.fromisoformat(end_date.replace("Z", ""))

            days_left = (end - now).days

            if volume > 0 and days_left <= 7 and (price >= 0.95 or price <= 0.05):
                opportunities.append(
                    f"{name}\nprice: {price} | vol: {volume} | days_left: {days_left}"
                )

        except:
            continue

    if not opportunities:
        send_message("🔎 Nessuna opportunità ad alta probabilità (7 giorni)")
    else:
        msg = "🚨 POLYMARKET EDGE (<7d):\n\n" + "\n\n".join(opportunities[:5])
        send_message(msg)
