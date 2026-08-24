"""
Heuristic selector finder.

Scans a page's HTML for tags whose id/class/data-* attributes contain
given keywords (e.g. "price", "title") and prints each candidate's tag,
id, class, and a text preview — so you don't have to grep raw HTML by hand.

Two modes:
  --render     fetch the page with headless Selenium (JS-rendered DOM)
  (default)    fetch the page with requests (static HTML only)

Usage:
  python find_selectors.py <url> keyword1 keyword2 ...
  python find_selectors.py <url> --render keyword1 keyword2 ...

Example:
  python find_selectors.py https://www.amazon.in/dp/B0FJQWRBVH --render price title image description
"""

import sys

import requests
from bs4 import BeautifulSoup

DEFAULT_KEYWORDS = ["price", "title", "image", "img", "description", "desc"]


def fetch_static(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=10)
    return response.text


def fetch_rendered(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(url)
        driver.implicitly_wait(5)
        return driver.page_source
    finally:
        driver.quit()


def attr_matches(tag, keywords, attr_name):
    """Check whether `keywords` appear in one specific attribute (id, class, or data-*)."""
    if attr_name == "id":
        haystack = (tag.get("id") or "").lower()
    elif attr_name == "class":
        haystack = " ".join(tag.get("class") or []).lower()
    else:  # data-*
        haystack = " ".join(
            v for k, v in tag.attrs.items() if k.startswith("data-") and isinstance(v, str)
        ).lower()

    return [kw for kw in keywords if kw.lower() in haystack]


def find_candidates(html, keywords, max_text_len=120):
    """Returns (id_matches, other_matches) — id matches are the higher-confidence signal
    since ids are usually unique and purpose-named, unlike reused classes/data attrs."""
    soup = BeautifulSoup(html, "html.parser")
    id_matches, other_matches = [], []

    for tag in soup.find_all(True):
        id_hits = attr_matches(tag, keywords, "id")
        class_hits = attr_matches(tag, keywords, "class")
        data_hits = attr_matches(tag, keywords, "data-*")
        matched = id_hits or class_hits or data_hits
        if not matched:
            continue

        text = tag.get_text(strip=True)
        preview = (text[:max_text_len] + "...") if len(text) > max_text_len else text

        entry = {
            "matched_keywords": matched,
            "tag": tag.name,
            "id": tag.get("id"),
            "class": tag.get("class"),
            "src_or_href": tag.get("src") or tag.get("href"),
            "text_preview": preview,
        }

        (id_matches if id_hits else other_matches).append(entry)

    return id_matches, other_matches


def print_candidates(entries, limit):
    for c in entries[:limit]:
        print("-" * 70)
        print(f"matched:  {c['matched_keywords']}")
        print(f"tag:      <{c['tag']}>")
        print(f"id:       {c['id']}")
        print(f"class:    {c['class']}")
        if c["src_or_href"]:
            print(f"src/href: {c['src_or_href']}")
        if c["text_preview"]:
            print(f"text:     {c['text_preview']}")
    if len(entries) > limit:
        print(f"\n... {len(entries) - limit} more not shown (use --limit N to see more).")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python find_selectors.py <url> [--render] [--limit N] [keyword1 keyword2 ...]")
        sys.exit(1)

    url = args[0]
    rest = args[1:]

    render = "--render" in rest
    if render:
        rest.remove("--render")

    limit = 15
    if "--limit" in rest:
        idx = rest.index("--limit")
        limit = int(rest[idx + 1])
        rest = rest[:idx] + rest[idx + 2 :]

    keywords = rest or DEFAULT_KEYWORDS

    print(f"Fetching {url} ({'rendered' if render else 'static'})...")
    html = fetch_rendered(url) if render else fetch_static(url)

    print(f"Searching for keywords: {keywords}\n")
    id_matches, other_matches = find_candidates(html, keywords)

    print(f"=== High-confidence matches (id contains keyword) — {len(id_matches)} found ===")
    print_candidates(id_matches, limit)

    if not id_matches and not other_matches:
        print("\nNo matching elements found. Try different keywords, or use --render if the")
        print("data might be injected by JavaScript (not present in the static HTML).")
    elif other_matches:
        print(f"\n=== Lower-confidence matches (class/data-* only) — {len(other_matches)} found ===")
        print_candidates(other_matches, limit)
