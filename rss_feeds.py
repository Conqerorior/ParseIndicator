import asyncio
import logging
from datetime import datetime
import aiohttp
import async_timeout
from bs4 import BeautifulSoup
from Constants import RSS_FEEDS_URLS, LEN_RSS_RECORDS
from MongoDB import insert_rss_collection, show_collection, rss_collection


async def process_rss_feed_by_url(session, rss_feed_url):
    try:
        async with session.get(rss_feed_url) as response:
            if response.status == 200:
                content = b''  # Создаем пустой bytes объект
                async for chunk in response.content:  # Читаем данные по частям
                    content += chunk
                soup = BeautifulSoup(content, 'lxml-xml')
                for item in soup.find_all('item'):
                    article = {
                        'title': item.title.text if item.title else None,
                        'link': item.link.text if item.link else None,
                        'description': item.description.text if item.description else None,
                        'published': item.pubDate.text if item.pubDate else None,
                        'source': rss_feed_url,
                        'parsed_at': datetime.now()
                    }

                    await insert_rss_collection(article)
            else:
                logging.error(f'Ошибка API: {response.status_code}, {response.text}')
                return None
    except asyncio.TimeoutError:
        logging.error(f"Таймаут при запросе: {rss_feed_url}")
        return None
    except Exception as e:
        logging.error(f'Ошибка запроса {rss_feed_url}: {e}')
        return None


async def get_rss_feeds():
    async with aiohttp.ClientSession() as session:
        tasks = [process_rss_feed_by_url(session, rss_feed_url) for rss_feed_url in RSS_FEEDS_URLS]
        await asyncio.gather(*tasks)

    # Вывод всей обновлённой коллекции
    # await show_collection(rss_collection, LEN_RSS_RECORDS)