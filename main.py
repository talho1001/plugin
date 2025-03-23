import requests
import sys

API = "https://dummyjson.com"
LOGIN = f"{API}/auth/login"
ME = f"{API}/auth/me"
POSTS = f"{API}/posts"
COMMENTS = lambda post_id: f"{API}/posts/{post_id}/comments"


def safe_req(method, url, headers=None, json=None, params=None):
    try:
        response = requests.request(method, url, headers=headers, json=json, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e} - {getattr(e.response, 'text', '')}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
    return None


# CON TEST

def authenticate(username: str, password: str) -> str:
    payload = {"username":username, "password":password}
    data = safe_req("POST", LOGIN, json=payload)
    if data and "token" in data:
        print("Login successful")
        return data["token"]
    print("Login failed")
    return None


# EV1
  
def get_user_details(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    return safe_req("GET", ME, headers=headers)

# EV2 

def get_posts(limit=60):
    return safe_req("GET", POSTS, params={"limit": limit})

def get_post_comments(post_id):
    return safe_req("GET", COMMENTS(post_id))


# EV3 

def get_posts_with_comments(limit=60):
    posts_data = get_posts(limit)
    if not posts_data:
        return None

    posts = posts_data.get("posts", [])
    for post in posts:
        comments = get_post_comments(post["id"])
        post["comments"] = comments.get("comments") if comments else []
    return posts


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <username> <password>")
        return

    username, password = sys.argv[1], sys.argv[2]
    print("Running connectivity test...")
    token = authenticate(username, password)
    if not token:
        return

    print("\n Evidence E1: Authenticated User Info")
    user = get_user_details(token)
    print(user)

    print("\n Evidence E2: 60 Posts")
    posts = get_posts()
    print(posts)

    print("\n Evidence E3: 60 Posts with Comments")
    posts_with_comments = get_posts_with_comments()
    print(posts_with_comments)

if __name__ == "__main__":
    main()
