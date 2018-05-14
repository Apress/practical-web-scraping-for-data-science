import requests
import json
import re
from bs4 import BeautifulSoup
import dataset

db = dataset.connect('sqlite:///reviews.db')

review_url = 'https://www.amazon.com/ss/customer-reviews/ajax/reviews/get/'
product_id = '1449355730'

session = requests.Session()
session.headers.update({
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    })

session.get('https://www.amazon.com/product-reviews/{}/'.format(product_id))

def parse_reviews(reply):
    reviews = []
    for fragment in reply.split('&&&'):
        if not fragment.strip():
            continue
        json_fragment = json.loads(fragment)
        if json_fragment[0] != 'append':
            continue
        html_soup = BeautifulSoup(json_fragment[2], 'html.parser')
        div = html_soup.find('div', class_='review')
        if not div:
            continue
        review_id = div.get('id')
        review_classes = ' '.join(html_soup.find(class_='review-rating').get('class'))
        rating = re.search('a-star-(\d+)', review_classes).group(1)
        title = html_soup.find(class_='review-title').get_text(strip=True)
        review = html_soup.find(class_='review-text').get_text(strip=True)
        reviews.append({'review_id': review_id,
                        'rating': rating,
                        'title': title,
                        'review': review})
    return reviews

def get_reviews(product_id, page):
    data = {
        'sortBy':'',
        'reviewerType':'all_reviews',
        'formatType':'',
        'mediaType':'',
        'filterByStar':'all_stars',
        'pageNumber':page,
        'filterByKeyword':'',
        'shouldAppend':'undefined',
        'deviceType':'desktop',
        'reftag':'cm_cr_getr_d_paging_btm_{}'.format(page),
        'pageSize':10,
        'asin':product_id,
        'scope':'reviewsAjax1'
        }
    r = session.post(review_url + 'ref=' + data['reftag'], data=data)
    reviews = parse_reviews(r.text)
    return reviews

page = 1
while True:
    print('Scraping page', page)
    reviews = get_reviews(product_id, page)
    if not reviews:
        break
    for review in reviews:
        print('  -', review['rating'], review['title'])
        db['reviews'].upsert(review, ['review_id'])
    page += 1