import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


driver = webdriver.Chrome()
driver.get('https://quotes.toscrape.com/js')
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "quote" )))

for a in range(4):
    if a !=0 :
        # Find the "Next" link
        next_link = driver.find_element(By.CSS_SELECTOR, "li.next a")
        next_url = next_link.get_attribute("href")
        print("before changing url")
        print(next_url)  # e.g. "https://example.com/page/2"  
        print("end") 
        driver.get(next_url)
    # print(f"Page {a+1} ----------------------------")
    quote = driver.find_elements(By.CLASS_NAME, "quote")
    # for i in range(10):
    #     text = quote[i].find_element(By.CLASS_NAME, "text")
    #     author = quote[i].find_element(By.CLASS_NAME, "author")
    #     print(text.text)
    #     print(author.text)
    print(len(quote))
driver.quit()