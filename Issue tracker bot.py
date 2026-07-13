import requests
import json
import os
from dotenv import load_dotenv
import argparse

load_dotenv()
token = os.environ.get('ISSUE_TOKEN')
REPO = "sirixhab/my-learning"


session = requests.Session()
session.headers.update({'Authorization':f'Bearer {token}'})
def create_issue(title,body):
    
    payload = {'title': title, 'body':body}

    r = session.post(f'https://api.github.com/repos/{REPO}/issues', json=payload)

    r.raise_for_status()

    if r.status_code == 201:
        issue= r.json()
        print(f'Create an issue with {issue['number']}:{issue['html_url']}')
        return issue
    
    else:
        print("failed")
        return None

def close_issue(issue_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}"
    payload = {"state": "closed"}

    
    response = session.patch(url, json=payload)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="GitHub issue bot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'create' command needs a title and a body
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("title")
    create_parser.add_argument("body")

    # 'close' command needs an issue number
    close_parser = subparsers.add_parser("close")
    close_parser.add_argument("issue_number")

    args = parser.parse_args()

    if args.command == "create":
        create_issue(args.title, args.body)
    elif args.command == "close":
        result = close_issue(args.issue_number)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()


# NOTE:A requests.Session lets you set the token and headers once, and reuse that same session object for every call. Two benefits:

# 1.Less repetition — no copy-pasting headers into every function
# 2.Faster — it reuses the same underlying network connection instead of opening a new one per request

# NOTE:A CLI (command-line interface) lets you to try or change by typing commands in the terminal, instead of calling th function everytime.
# So no code editing needed — you just pass arguments. Python's built-in argparse module handles this. 