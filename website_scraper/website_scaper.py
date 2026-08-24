#https://en.wikipedia.org/wiki/Special:Random
import csv, requests
from bs4 import BeautifulSoup

def get_website(x, url, headers):
    
	response = requests.get(url, headers = headers)
	print("Status Code : ", response.status_code, url)
	soup = BeautifulSoup(response.text, "html.parser")
	title = soup.find("span", class_ = "mw-page-title-main")
	if not title:
		print('Coult not find title, moving to next page...')
	else:
		print(title.text)


	content_div = soup.find("div", id= "mw-content-text")



url = "https://en.wikipedia.org/wiki/Special:Random"
headers = {"User-Agent": "Mozilla/5.0 (educational scraping practice)"}


x = int(input('Enter no of times you want to scrape wikipedia : '))

for i in range(x):
	get_website(x, url, headers)
