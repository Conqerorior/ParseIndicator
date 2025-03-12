import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from Constants import LEN_RSS_RECORDS, RSS_FEEDS_URLS
from MongoDB import insert_rss_collection, show_collection


async def get_rss_feeds():
    for rss_feed_url in RSS_FEEDS_URLS:
        articles = await get_rss_feed_by_url(rss_feed_url)
        for article in articles:
            await insert_rss_collection(article)
        await show_collection(LEN_RSS_RECORDS)


async def get_rss_feed_by_url(feed_url):
    response = requests.get(feed_url)
    if response.status_code != 200:
        logging.error(f'Ошибка API: {response.status_code}, {response.text}')
    soup = BeautifulSoup(response.content, 'lxml-xml')

    # Парсинг статей
    articles = []
    for item in soup.find_all('item'):
        article = {
            'title': item.title.text if item.title else None,
            'link': item.link.text if item.link else None,
            'description': item.description.text if item.description else None,
            'published': item.pubDate.text if item.pubDate else None,
            'source': feed_url,
            'parsed_at': datetime.now()
        }
        articles.append(article)

    return articles
