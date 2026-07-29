# not just reading one API and printing it; you're translating one API's data model into another API's data model
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


# ---- Config ----
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "sirixhab/hello-world"   

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")

STATE_FILE = "synced_issues.json"

def load_synced_issues():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_synced_issues(synced_ids):
    with open(STATE_FILE, "w") as f:
        json.dump(list(synced_ids), f)

# GitHub side
def get_github_session():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    })
    return session


def fetch_open_issues(session, repo):
    """Fetch all open issues, handling pagination."""
    issues = []
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {"state": "open", "per_page": 30, "page": 1}

    while True:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        page_data = response.json()

        if not page_data:
            break  # no more pages
        #GitHub returns results 30-at-a-time by default. This loop keeps requesting page=1, page=2, page=3... until
        # a page comes back empty, meaning you've reached the end.
        # GitHub's issues endpoint also returns pull requests — filter those out
        real_issues = [issue for issue in page_data if "pull_request" not in issue]
        issues.extend(real_issues)

        params["page"] += 1

    return issues

# Trello side
def get_notion_session():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",   # Notion requires this version header
        "Content-Type": "application/json",
    })
    return session


def create_trello_card(session, list_id, name, desc):
    url = "https://api.trello.com/1/cards"
    payload = {
        "idList": list_id,
        "name": name,
        "desc": desc,
    }
    response = session.post(url, params=payload, timeout=10)
    response.raise_for_status()
    return response.json()


# Schema mapping — the core "translation" logic
def map_issue_to_card(issue):
    """Convert a GitHub issue's schema into the fields Trello's API expects."""
    labels = [label["name"] for label in issue.get("labels", [])]
    label_text = f"Labels: {', '.join(labels)}\n\n" if labels else ""

    name = f"#{issue['number']} — {issue['title']}"
    desc = (
        f"{label_text}"
        f"{issue.get('body') or '(no description)'}\n\n"
        f"Reported by: {issue['user']['login']}\n"
        f"Link: {issue['html_url']}"
    )

    return {"name": name, "desc": desc}

# Main sync logic
def sync_github_to_trello():
    github_session = get_github_session()
    trello_session = get_trello_session()
    
    # Without this check, running the script twice would create duplicate Trello cards for the same issue every time.
    # This state file makes the sync idempotent — safe to re-run without side effects. 
    synced_ids = load_synced_issues()

    print(f"Fetching open issues from {GITHUB_REPO}...")
    issues = fetch_open_issues(github_session, GITHUB_REPO)
    print(f"Found {len(issues)} open issues.")

    new_syncs = 0

    for issue in issues:
        issue_id = issue["id"]

        if issue_id in synced_ids:
            continue  # already synced this issue before, skip it

        card_data = map_issue_to_card(issue)

        try:
            card = create_trello_card(
                trello_session,
                TRELLO_LIST_ID,
                card_data["name"],
                card_data["desc"],
            )
            print(f"Created Trello card: {card['name']}")
            synced_ids.add(issue_id)
            new_syncs += 1

        except requests.RequestException as e:
            print(f"Failed to create card for issue #{issue['number']}: {e}")

    save_synced_issues(synced_ids)
    print(f"Sync complete. {new_syncs} new card(s) created.")


if __name__ == "__main__":
    sync_github_to_trello()


# NOTE:
# -> it introduces schema mapping -- GitHub's issue JSON and Trello's card JSON look nothing alike, 
#    even though they represent similar ideas ("a thing that needs to be tracked").
# -> This translation layer — deciding how one system's fields map to another's, and 
#    handling fields that don't have a direct equivalent — is the actual skill this project teaches. 
#    It's exactly what you'd do connecting a CRM to a support ticketing system, or a payment provider to an internal ledger.
# -> You'll want a separate Session for each service, since headers/auth differ
# ->GitHub wants a Bearer token in the header. Trello wants key/token as query parameters on every request. Setting session.params means
#   every request made with trello_session automatically includes those two params — similar to how session.headers works, but for query strings instead.
# ->with GitHub's API: the issues endpoint also returns pull requests, because internally GitHub treats PRs as a type of issue. If an item has a "pull_request" key, 
#    it's actually a PR, not a real issue — so you filter those out.
# -> def map_issue_to_card(issue): Keeping the schema translation in its own function, separate from the fetch/create logic, means if Trello's card format changes, 
#   or you want to sync to Notion instead, you only touch this one function — not the whole sync pipeline.
