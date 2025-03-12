import asyncio
import logging
import os

import aiohttp
from dotenv import load_dotenv

from MongoDB import insert_circl_collection

load_dotenv()


URL_CIRCL = os.getenv('URL_CIRCL')
URL_CIRCL_UID = os.getenv('URL_CIRCL_UID')


async def fetch_json(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f'Ошибка {response.status} при запросе {url}')
                return None
    except Exception as e:
        logging.error(f'Ошибка запроса {url}: {e}')
        return None


async def process_circl_entry(session, key):
    response_uid = await fetch_json(session, f'{URL_CIRCL_UID}{key}.json')
    if response_uid:
        try:
            await insert_circl_collection(response_uid['Event'])
        except Exception as e:
            logging.error(f'Ошибка сохранения в БД {key}: {e}')


async def get_circl():
    async with aiohttp.ClientSession() as session:
        response = await fetch_json(session, URL_CIRCL)
        if not response:
            return

        tasks = [process_circl_entry(session, key) for key in response.keys()]

        await asyncio.gather(*tasks)

        logging.info('Все записи обработаны.')
