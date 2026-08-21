from urllib.robotparser import RobotFileParser
import time
import requests


def fetch_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response
            print(f"Got status {response.status_code}, retrying...")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        wait = 2 ** attempt  # 1s, 2s, 4s...
        print(f"Retrying in {wait}s...")
        time.sleep(wait)
    
    print("Max retries reached — giving up on this URL.")
    return None



rp = RobotFileParser()
rp.set_url("https://en.wikipedia.org/robots.txt")
rp.read()
headers = {"User-Agent": "Mozilla/5.0 (educational scraping practice)"}
url = "https://books.toscrape.com/"


# can_fetch = rp.can_fetch(headers, url)
# print(can_fetch)  # True or False

fetch_with_retry(url, headers)