import requests
import json
import time

def track_price(target_price):
    session = requests.Session()
    session.headers.update({"User-Agent": "price-tracker/1.0"})

    while True:
        r = session.get("https://api.coingecko.com/api/v3/simple/price",
        params = {"ids": "bitcoin", "vs_currencies": "usd"})
        price = r.json()["bitcoin"]["usd"]

        if price < target_price:
            print(f"Alert! Bitcoin dropped to {price}")
            # send email via Mailgun API here
            break

        time.sleep(60)   # check every minute

result=track_price(40000)
print(json.dumps(result,indent=2))