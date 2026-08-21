import requests, csv, time, sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

def robot_check(url, headers, rp):
	can_fetch = rp.can_fetch(headers['User-Agent'], url)
	return can_fetch  # True or False

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

def get_books(url, csvwriter) :
	global x
	response = fetch_with_retry(url, headers=headers)
	if not response :
		sys.exit()

	print("Status code:", response.status_code)  # should print 200

	soup = BeautifulSoup(response.text, "html.parser")
 
	books = soup.find_all("article", class_="product_pod")
	x +=1
	print(f"Found {len(books)} books on the page [{x}]")
	
	for book in books:
		title = book.h3.a["title"]
		availability = book.find("p", class_="instock availability").text.strip()
		price = book.find("p", class_="price_color").text
		f = [title, price, availability]
		csvwriter.writerow(f)

	return soup

x = 0
no_of_pg = int(input("enter number of pages you want to scrape: "))

url = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (educational scraping practice)"}

rp = RobotFileParser()
rp.set_url(url + "robots.txt")
rp.read()
can_check = robot_check(url, headers, rp)
if not can_check :
	sys.exit()

response = fetch_with_retry(url, headers)
if not response :
	sys.exit()

soup = BeautifulSoup(response.text, "html.parser")

f = ['Title', 'Price', 'Availability']

with open("Books_scraped.csv", 'w', newline = '', encoding="utf-8-sig") as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(f)
	get_books(url, csvwriter)
	url_temp = url
	for i in range(1, no_of_pg):
		next_link = soup.find("li", class_="next")
		if not next_link :
			print('no more pages found')
			break
		url_temp = urljoin(url_temp, next_link.a["href"])
		if not robot_check(url_temp, headers, rp):
			print(f"Disallowed by robots.txt : {url_temp}")
			break
		soup = get_books(url_temp, csvwriter)		
		