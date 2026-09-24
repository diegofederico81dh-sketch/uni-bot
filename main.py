import requests, time, os, threading
from flask import Flask

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
UNI_HIGH = 9.0
UNI_LOW = 8.5

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot UNI activo"

def check_price():
    while True:
        try:
            r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=UNIUSDT").json()
            price = float(r['price'])
            print(f"UNI: {price}")
            if TOKEN and CHAT_ID:
                if price >= UNI_HIGH:
                    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚀 UNI en ${price} - VENDE!")
                if price <= UNI_LOW:
                    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=📉 UNI en ${price} - COMPRA!")
        except Exception as e:
            print(e)
        time.sleep(60)

threading.Thread(target=check_price, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
