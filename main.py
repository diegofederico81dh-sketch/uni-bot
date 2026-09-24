import os, time, requests
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot UNI activo"

def check_uni():
    while True:
        try:
            # Precio de UNI
            r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=UNIUSDT", timeout=10)
            price = float(r.json()['price'])
            print(f"UNI: {price}")
            
            if price <= 9.25:
                msg = f"🔴 UNI = ${price} - VENDE!"
                requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
            
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(60)

threading.Thread(target=check_uni, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
