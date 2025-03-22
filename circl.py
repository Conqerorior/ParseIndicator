import asyncio
import json
import logging
import os
import aiohttp
import async_timeout
from dotenv import load_dotenv
from Constants import LEN_CICLE_RECORDS, TIMEOUT
from MongoDB import insert_circl_collection_if_exist, show_collection, database, CIRCL_COLLECTION

load_dotenv()

URL_CIRCL = os.getenv('URL_CIRCL')
URL_CIRCL_UID = os.getenv('URL_CIRCL_UID')
circl_collection = database.get_collection(CIRCL_COLLECTION)

async def fetch_json(session, url):
    try:
        async with session.get(url) as response:
            async with async_timeout.timeout(TIMEOUT):
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f'Ошибка {response.status} при запросе {url}')
                    return None
    except Exception as e:
        logging.error(f'Ошибка запроса {url}: {e}')
        return None


async def process_circl_entry(session, key):
    existing = await circl_collection.find_one({'_id': key}) # для ускорения работы, вначале смотрим, есть ли в БД значение с тами ключом
    # В данном случае, из-за гигантских размеров ответа, это очень существенно ускоряет парсинг
    if not existing:
        response_uid = await fetch_json(session, f'{URL_CIRCL_UID}{key}.json')
        if response_uid and len(json.dumps(response_uid)) < 16777000:
            try:
                await insert_circl_collection_if_exist(response_uid['Event'])
            except Exception as e:
                logging.error(f'Ошибка сохранения в БД {key}: {e}')
    else:
        logging.info(f'Запись {key} уже существует')


async def get_circl():
    async with aiohttp.ClientSession() as session:
        response = await fetch_json(session, URL_CIRCL)
        if not response:
            return
        tasks = [process_circl_entry(session, key) for key in response.keys()]
        await asyncio.gather(*tasks)

    # Для вывода всей обновлённой коллекции
    # await show_collection(circl_collection, LEN_CICLE_RECORDS)
