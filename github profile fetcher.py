import requests

def profile_fetcher(username):
    r = requests.get(f"https://api.github.com/users/{username}", headers={'user-agent':'my-app/1.0'})

    r.raise_for_status               #headers={'user-agent':'my-app/1.0'} --> not necessary, can be ignored 
    data = r.json()
    
    return {
        'name': data['name'],
        'user type': data['user_view_type'],
        'company': data['company'],
        'location': data['location'],
        'followers': data['followers'],
        'following': data['following'],
        'created on':data['created_at']
    }


print(profile_fetcher("torvalds"))
print(profile_fetcher("gvanrossum"))

