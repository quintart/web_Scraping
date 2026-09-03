import requests, csv, time, random
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
    try :
        response = requests.get(url=url, headers=headers)
    except requests.exceptions.RequestException as e:
        print('Something went wrong:')
        continue

    if response.status_code != 200:
        print("Failed to retrieve the page. Status code:", response.status_code)
        continue

    time.sleep(random.uniform(2,5))
    print("Status : ", response.status_code)

    tree = html.fromstring(response.text)

    title = get_data(tree, '//*[@id="productTitle"]/text()')
    price = get_data(tree, '//*[@id="corePriceDisplay_desktop_feature_div"]/div/div[1]/span[3]/span[2]/span[2]/text()')
    if not price:
        price = 'N/A'
    max_price = get_data(tree, '//*[@id="corePriceDisplay_desktop_feature_div"]/div/div[2]/span/span/span[1]/span[2]/span[2]/span[1]/text()') 
    if not max_price:
        max_price = 'N/A'
    in_stock = get_data(tree, '//*[@id="availability"]/span/text()')
    if not in_stock :
        in_stock = 'Out of Stock'
    rating = get_data(tree, '//*[@id="acrPopover"]/span/a/span/text()')
    review_count = get_data(tree, '//*[@id="acrCustomerReviewText"]/text()')
    review_count = review_count.strip('()') if review_count else 0

    product = {'Title' : title,
            'Price' : price,
            'Max_Price' : max_price,
            'Availability' : in_stock,
            'Rating' : rating,
            'Review_Count' : review_count,
            'URL' : url,}
    all_products.append(product)
    print(product)
if all_products:
    with open("Product_Details.csv", 'w', newline='',encoding="utf-8-sig") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=all_products[0].keys())
        csvwriter.writeheader()
        print("Data written to Product_Details.csv successfully.")
        csvwriter.writerows(all_products)
        