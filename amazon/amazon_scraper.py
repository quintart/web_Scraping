import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
    )
    return driver


def get_text(driver, by, value):
    try:
        # textContent (not .text) so hidden/offscreen elements are still read
        return driver.find_element(by, value).get_attribute("textContent").strip()
    except NoSuchElementException:
        return None


def get_attr(driver, by, value, attr):
    try:
        return driver.find_element(by, value).get_attribute(attr)
    except NoSuchElementException:
        return None


def parse_product(driver):
    title = get_text(driver, By.ID, "productTitle")

    price = None
    for by, value in [
        (By.CSS_SELECTOR, "#corePriceDisplay_desktop_feature_div span.a-price span.a-offscreen"),
        (By.CSS_SELECTOR, "#corePrice_feature_div span.a-price span.a-offscreen"),
        (By.CSS_SELECTOR, "span.a-price span.a-offscreen"),
        (By.ID, "priceblock_ourprice"),
        (By.ID, "priceblock_dealprice"),
    ]:
        price = get_text(driver, by, value)
        if price:
            break

    image_url = get_attr(driver, By.ID, "landingImage", "src")

    description = None
    try:
        bullets = driver.find_elements(
            By.CSS_SELECTOR, "#feature-bullets ul li span.a-list-item"
        )
        if bullets:
            description = " | ".join(b.text.strip() for b in bullets if b.text.strip())
    except NoSuchElementException:
        pass
    if not description:
        description = get_text(driver, By.ID, "productDescription")

    return {
        "title": title,
        "price": price,
        "image_url": image_url,
        "description": description,
    }


def scrape_amazon_product(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.presence_of_element_located((By.ID, "productTitle")))
    except TimeoutException:
        print(f"Timed out waiting for product page to load: {url}")
    return parse_product(driver)


if __name__ == "__main__":
    urls = [
        u.strip()
        for u in input("Enter one or more Amazon product URLs (comma-separated): ").split(",")
        if u.strip()
    ]

    driver = build_driver()
    fieldnames = ["title", "price", "image_url", "description"]
    try:
        with open("amazon_products.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for url in urls:
                print(f"Scraping: {url}")
                product = scrape_amazon_product(driver, url)
                print(product)
                writer.writerow(product)
                time.sleep(2)  # be polite between requests
    finally:
        driver.quit()
