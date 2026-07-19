# Teaches webhooks — different from polling, since you push data to a service instead of just reading from one.

import requests
import os 
import time
import schedule
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
CITY = "Bengaluru"
UNITS = "metric"                # metric = Celsius, imperial = Fahrenheit


def get_weather(session, city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": UNITS,
    }
    response = session.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def build_discord_payload(weather_data, city):         #This just pulls specific values out of the big nested dictionary returned by OpenWeatherMap. 
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    description = weather_data["weather"][0]["description"].title()
    wind_speed = weather_data["wind"]["speed"]

    embed = {
        "title": f"Weather Update — {city}",
        "description": description,
        "color": 3447003,  # a blue accent color
        "fields": [
            {"name": "Temperature", "value": f"{temp}°C", "inline": True},
            {"name": "Feels Like", "value": f"{feels_like}°C", "inline": True},
            {"name": "Humidity", "value": f"{humidity}%", "inline": True},
            {"name": "Wind Speed", "value": f"{wind_speed} m/s", "inline": True},
        ],

        "footer": {"text": "Weather Notifier Bot"},
    }

    return {"embeds": [embed]}

def send_discord_alert(session, payload):

    response = session.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()
    print(f"[{datetime.now()}] Weather update sent to Discord.")

def job():                            #This is the function that actually gets called on a schedule. 
    session = requests.Session()
    try:
        weather_data = get_weather(session, CITY)
        payload = build_discord_payload(weather_data, CITY)
        send_discord_alert(session, payload)
    except requests.RequestException as e:
        print(f"[{datetime.now()}] Error during weather job: {e}")


def main():
    job()

    # this registers a rule with the schedule library. Important: this line does not run the job — it just adds it to an internal list of scheduled tasks.
    schedule.every().day.at("08:00").do(job)

    print("Weather notifier scheduled. Waiting for next run...")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()




# NOTE: Why webhooks over polling?
# POLLING : Here, You repeatedly ask an API "anything new?", It is  initiated by your code, on a timer 
#        Refreshing your email inbox every 60 seconds, Wastes requests when nothing changed.
# WEBHOOKS : Here, You push data to a service whenever something happens, It is initiated by your code, on an event/trigger,
#         Getting a Discord DM, Requires a URL that accepts the push.

# IMPORTANT:
# In this project, you're not receiving a webhook — you're sending TO one. Discord and Slack give you a special URL (a webhook URL) 
# that you POST a JSON payload to, and it automatically appears as a message in a channel. No login, no OAuth, no bot token needed — just a POST request.
# This is the simplest possible way to get "push notifications" working, which is why it's a great teaching project before you move to more complex auth-based APIs.

# No Authorization header is needed here — the webhook URL itself is the secret/credential. 
              # Anyone who has that URL can post messages to that Discord channel, 
            # which is why you should never commit it to a public GitHub repo.






# NOTE: 
# embed{}-- This builds a dictionary matching exactly the structure Discord expects for a rich "embed" message.
#The API only understands this specific shape.
# "color": 3447003 — Discord wants colors as a decimal integer, not a hex code like #3498db.
# "inline": True — makes fields sit side-by-side instead of stacked.
# The whole embed is wrapped in {"embeds": [embed]} because Discord's API technically supports sending multiple embeds in one message — hence the list.