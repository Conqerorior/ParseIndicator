import asyncio
import logging
import os

import aiohttp
import async_timeout
from dotenv import load_dotenv
from Constants import LEN_ABUSE_RECORDS
from MongoDB import insert_abuse_collection, show_collection, database, ABUSE_COLLECTION

load_dotenv()

AUTHKEY_ABUSE = os.getenv('AUTHKEY_ABUSE')
URL_ABUSE = os.getenv('URL_ABUSE')
abuse_collection = database.get_collection(ABUSE_COLLECTION)

async def fetch_abuses():
    data = {'query': 'get_iocs'}
    headers = {
        'Auth-Key': AUTHKEY_ABUSE,
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(URL_ABUSE, headers=headers, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f"Ошибка API: {response.status}, {await response.text()}")
                    return None
        except asyncio.TimeoutError:
            logging.error(f"Таймаут при запросе: {URL_ABUSE}")
            return None
        except Exception as e:
            logging.error(f"Ошибка при запросе: {e}")
            return None


async def get_abuses():
    result = await fetch_abuses()
    if not result:
        return

    records = result.get('data', [])

    tasks = [insert_abuse_collection(record) for record in records]
    await asyncio.gather(*tasks)

    # Для вывода всей обновлённой коллекции
    # await show_collection(abuse_collection, LEN_ABUSE_RECORDS)
