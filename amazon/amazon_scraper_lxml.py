import requests, csv
from lxml import html

def get_data(tree, path):

    data = tree.xpath(path)
    if len(data) > 0:
        return data[0].strip()
    else :
        return None

headers = {"User-Agent": "Mozilla/5.0(educational scrapingoorac)"}

all_products = []

x = int(input('Enter no of URLs you will enter : '))

for i in range(x) :
    url = input('Enter URL :').strip()
    response = requests.get(url, headers=headers)
    print("Status : ", response.status_code)

    tree = html.fromstring(response.text)

    title = get_data(tree, '//*[@id="productTitle"]/text()')
    price = get_data(tree, '//*[@id="corePriceDisplay_desktop_feature_div"]/div/div[1]/span[3]/span[2]/span[2]/text()')
    max_price = get_data(tree, '//*[@id="corePriceDisplay_desktop_feature_div"]/div/div[2]/span/span/span[1]/span[2]/span[2]/span[1]/text()')
    rating = get_data(tree, '//*[@id="acrPopover"]/span/a/span/text()')
    review_count = get_data(tree, '//*[@id="acrCustomerReviewText"]/text()').strip('()')

    product = {'Title' : title,
            'Price' : price,
            'Max_Price' : max_price,
            'Rating' : rating,
            'Review_Count' : review_count,
            'URL' : url,}
    all_products.append(product)

with open("Product_Details.csv", 'w', newline='',encoding="utf-8-sig") as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=all_products[0].keys())
    csvwriter.writeheader()
    csvwriter.writerows(all_products)