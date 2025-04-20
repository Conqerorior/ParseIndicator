import asyncio
import logging
import os
import re
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

    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    uuid_no_hyphens = re.compile(
        r'^[0-9a-f]+$',
        re.IGNORECASE
    )
    tasks = []
    for record in records:
        ioc = record.get('ioc')
        # Отсеиваем ioc с uid-ами
        if not (bool(uuid_pattern.match(ioc)) or bool(uuid_no_hyphens.match(ioc))):
            tasks.append(insert_abuse_collection(record))
    await asyncio.gather(*tasks)

    # Для вывода всей обновлённой коллекции
    # await show_collection(abuse_collection, LEN_ABUSE_RECORDS)
