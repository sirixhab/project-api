import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()  #call the .env file

def get_news(topic):
    api_key = os.environ.get("NEWS_API_KEY")

    r = requests.get("https://newsapi.org/v2/everything", params={
        "q": topic, 
        "pageSize":1,  
        "from": "2026-06-01",         
        "to": "2026-06-15",          
        "domains": "bbc.com,cnn.com",      
        "apiKey": api_key     #this proves you're an authorized user
        })

    r.raise_for_status()
    data = r.json()                    # NOTE: the keys are within nested list i.e in the list articles

    article = data['articles'][0]      # so get first article from the list
    return {
        'name': article['source']['name'],         # source name is nested
        'title': article['title'],
        'published on': article['publishedAt'],
        'about': article['description'],
        'url': article['url']

    }

news = get_news("technology")
print(json.dumps(news, indent=2))        #json.dumps() converts a Python object (dict/list) into a JSON-formatted string. 
                                            #It's the opposite of json.loads() (which converts a JSON string into a Python object).




# Skills: API keys, pagination, filtering

# 1. install dotenv in terminal --> pip install python-dotenv
# 2. create a .env file and copy the api key there after getting the key from website
# 3. by getting a api proves who you are to the server before it gives you data.
# 4. pagination: APIs don't send you ALL results at once — they split results into "pages," like a book.Eg:"page": 1 ← which page of results,"pageSize": 10← how many results per page
# 5. filtering: by using parameters, narrowing to what is required