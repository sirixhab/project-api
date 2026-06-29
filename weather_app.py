import requests

def get_weather(lat, lon):
    r = requests.get('https://api.open-meteo.com/v1/forecast', params={"latitude": lat, "longitude": lon,
                         "current_weather": True})
    r.raise_for_status()
    return r.json()['current_weather']    


delhi   = get_weather(28.6, 77.2)
mumbai  = get_weather(19.0, 72.8)
london  = get_weather(51.5, -0.1)

print(mumbai)                
print(delhi)                
print(london)


#NOTE:
# how is it calculating weather using the lat and lon without any mathematical operations provided?
# ## You Are Not Calculating Anything

# Your Python code does **zero weather calculation**. You're just asking someone else's computer to do it.

# ```python
# requests.get("https://api.open-meteo.com/v1/forecast", params={
#     "latitude": 28.6,
#     "longitude": 77.2,
#     "current_weather": True
# })
# ```

# This is like making a **phone call**:

# ```
# You        →  "what's the weather at 28.6, 77.2?"
# Their server →  *looks it up* → "32.5°C, windspeed 12.3"
# You        →  receives the answer
# ```

# You're not doing the math. You're just sending a question and receiving an answer.

# ---

# ## What Open-Meteo Actually Does (On Their Side)

# On their servers they have:

# ```
# → thousands of weather sensors worldwide
# → satellite data
# → historical weather databases
# → complex meteorological models
# → code that maps coordinates to nearest weather station
# ```

# When you send `latitude=28.6, longitude=77.2` — their server:

# ```
# 1. receives your coordinates
# 2. finds the nearest weather station to that location
# 3. fetches current readings from their database
# 4. formats it as JSON
# 5. sends it back to you
# ```

# All of that happens **on their machine**, not yours.

# ---

# ## Your Code's Only Job

# ```python
# # your entire job is just 3 things:
# r = requests.get(url, params={...})   # 1. send the question
# r.raise_for_status()                  # 2. check you got an answer
# data = r.json()['current_weather']    # 3. read the answer
# ```

# You are a **consumer** of their calculation, not the calculator.

# ---

# ## This is the Whole Point of APIs

# ```
# WITHOUT API:
# You would need → weather satellites
#                → sensor networks
#                → meteorology models
#                → years of data
#                → complex math
#                → impossible for one person

# WITH API:
# You need       → 5 lines of Python ✅
# ```

# APIs let you use other people's powerful systems — weather engines, maps, payment processors, AI models — by just sending a request and reading the response.

# Your coordinates are just the **input** you hand to their system. The intelligence lives entirely on their side.

