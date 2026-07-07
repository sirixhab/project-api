# creating an actual resource on some other's platform(creating git reops) by using json data and proper authentication.
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
def create_repo(name, private=False):
    token = os.environ.get("NEW_GIT_TOKEN")

    r = requests.post("https://api.github.com/user/repos",headers={"Authorization": f"Bearer {token}", "Accept":"application/vnd.github+json"},
    json={  "name": name,"private": private,"description": "Created via Python API"})
    
# "Accept" is an HTTP header that tells server what format you want back(i.e is json, html or xml)
# application/json  → generic JSON (works with most APIs)
# vnd.github+json   → GitHub's specific JSON format
                    # vnd = vendor (company-specific)
                    # github = that vendor is GitHub
                    # +json = it's JSON underneath

    r.raise_for_status
    return r.json()

# To delete the created repo
def delete_repo(owner, repo_name):
    token = os.environ.get("NEW_GIT_TOKEN")

    r=requests.delete(f"https://api.github.com/repos/{owner}/{repo_name}", headers={"Authorization": f"Bearer {token}"})

    r.raise_for_status()
    return print(f"deleted repo: {repo_name}")


result=create_repo('my_repo')
print(json.dumps(result,indent=2))
print("\n")
delete_repo("sirixhab","my_repo")

#NOTE: this displays the repos present 
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# token = os.environ.get("NEW_GIT_TOKEN")

# r = requests.get(
#     "https://api.github.com/user/repos",
#     headers={"Authorization": f"Bearer {token}"}
# )

# repos = r.json()
# for repo in repos:
#     print(repo['name'])   # see your actual repo names

# NOTE: 
# 1. data--> sends form-encoded text — wrong format for GitHub's API, Content-Type: application/x-www-form-urlencoded,body: name=test --> github expects json, it will reject this.
# 2. json-->sends proper JSON — what GitHub's API expects,Content-Type: application/json,body: {"name": "test".
# 3. why bearer token instead of 'apikey' param:
            # NewsAPI — key in URL params
            #params={"apiKey": api_key}

            # GitHub — token in Authorization header
           # headers={"Authorization": f"Bearer {token}"}

    #Bearer tokens are: (tokens are generated from this link:https://github.com/settings/tokens)
      # --> more secure (not visible in URL/logs)
      #--> standard for OAuth-based APIs
      #--> used by most modern professional APIs (GitHub, Stripe, Twitter, etc.)