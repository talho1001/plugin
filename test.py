import requests

def check_test_route():
    url = "https://dummyjson.com/test"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("response:", response.json())
    except Exception as e:
        print("failed:", e)

check_test_route()
