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

def get_prod_detail(url, csvwriter) :
	response = fetch_with_retry(url, headers=headers)
	if not response :
		sys.exit()

	print("Status code:", response.status_code)  # should print 200

	soup = BeautifulSoup(response.text, "html.parser")
 
	title = soup.find("div", id="titleSection")
	print(f"Title : \n{title.text.strip()}")
	price = soup.find()
    # return soup

url = "https://www.amazon.in/Logitech-Bluetooth-Connectivity-Spill-Resistant-Comfortable/dp/B0FJQWRBVH/?_encoding=UTF8&pd_rd_w=HE6jc&content-id=amzn1.sym.340182bc-8d5c-49c7-8b69-c0403f7ba3a7%3Aamzn1.symc.752cde0b-d2ce-4cce-9121-769ea438869e&pf_rd_p=340182bc-8d5c-49c7-8b69-c0403f7ba3a7&pf_rd_r=YVCZY40NAQD04VPK2JVE&pd_rd_wg=QykzZ&pd_rd_r=af35959c-d896-4e5a-b1d4-43806b2d3c16"
headers = {"User-Agent": "Mozilla/5.0 (educational scraping practice)"}

# rp = RobotFileParser()
# rp.set_url(url + "robots.txt")
# rp.read()
# can_check = robot_check(url, headers, rp)
# if not can_check :
# 	sys.exit()

# response = fetch_with_retry(url, headers)
# if not response :
# 	sys.exit()
response = requests.get(url, headers= headers)
soup = BeautifulSoup(response.text, "html.parser")
csvwriter = 0
get_prod_detail(url, csvwriter)

