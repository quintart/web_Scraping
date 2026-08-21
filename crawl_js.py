from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://quotes.toscrape.com/js/")  # a JS-rendered version of a practice site

wait = WebDriverWait(driver, 10)  # wait up to 10 seconds
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

quotes = driver.find_elements(By.CLASS_NAME, "quote")
print(f"Found {len(quotes)} quotes")
f = ['Quote', 'Author']
with open('Quote.csv', 'w',newline = '', encoding="utf-8-sig") as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(f)
	for q in quotes:
		text = q.find_element(By.CLASS_NAME, "text").text
		author = q.find_element(By.CLASS_NAME, "author").text
		print(f"{text} — {author}")
		f = [text, author]
		csvwriter.writerow(f)

	driver.quit()  # always close the browser when done