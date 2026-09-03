import requests
from lxml import html

def news_data(tree):
    heading = tree.xpath('//*[@id="app"]/main/article/div[2]/div[1]/div[1]/div[1]/h1/text()')

    timestamp = tree.xpath('//*[@id="app"]/main/article/div[2]/div[1]/div[5]/div[1]/div[1]/p/text()')

    text = tree.xpath('//div/p[@data-testid="article-paragraph-annotation-test-id"]/text()')
    text_data = ' '.join(text).strip()

    images = tree.xpath('//img')
    img_url = [images[i].get('src') for i in range(1,len(images)-1)]

        

    news = {
        'Heading' : heading[0],
        'Publish Date' : timestamp[2],
        'News' : text_data,
        'Image Url' : img_url
    }
    print(news)
    return None


url = 'https://www.straitstimes.com/asia/east-asia/china-penalises-10-people-for-misinformation-over-deadly-mudslide?ref=top-stories'
response = requests.get(url)
tree = html.fromstring(response.text)

news_data(tree)




# url_with_1_img = 'https://www.straitstimes.com/asia/south-asia/who-are-the-foreign-tourists-missing-in-nepals-flash-floods?ref=top-stories'

# url_with_multiple_img = 'https://www.straitstimes.com/asia/south-asia/nepal-buries-dead-as-rescuers-seek-thousands-missing?ref=top-stories'