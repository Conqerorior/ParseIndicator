import os

import requests
from dotenv import load_dotenv

from MongoDB import insert_circl_collection

load_dotenv()


URL_CIRCL = os.getenv('URL_CIRCL')
URL_CIRCL_UID = os.getenv('URL_CIRCL_UID')


async def get_circl():
    response = requests.get(URL_CIRCL)
    if response.status_code == 200:
        result = response.json()
        for key, val in result.items():
            response_uid = requests.get(URL_CIRCL_UID + key + '.json')
            if response_uid.status_code == 200:
                await insert_circl_collection(response_uid.json()['Event'])
