import json
import logging
import os

import requests
from dotenv import load_dotenv

from Constants import LEN_ABUSE_RECORDS
from MongoDB import insert_abuse_collection, show_collection

load_dotenv()

AUTHKEY_ABUSE = os.getenv('AUTHKEY_ABUSE')
URL_ABUSE = os.getenv('URL_ABUSE')


async def get_abuses():
    data = {
        'query': 'get_iocs'
    }
    headers = {
        'Auth-Key': AUTHKEY_ABUSE,
        'Content-Type': 'application/json'
    }
    response = requests.post(URL_ABUSE, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()

        for record in result['data']:
            await insert_abuse_collection(record)

        logging.info(f'Записано {len(result)} записей в базу')
    else:
        logging.error(f"Ошибка API: {response.status_code}, {response.text}")

    await show_collection(LEN_ABUSE_RECORDS)
