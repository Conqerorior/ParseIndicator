import logging
import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_NAME = os.getenv('MONGODB_NAME')
ABUSE_COLLECTION = os.getenv('ABUSE_COLLECTION')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
database = client.get_database(MONGODB_NAME)
abuse_collection = database.get_collection(ABUSE_COLLECTION)


async def start_mongodb():
    logging.warning('Подключение к базе данных успешно установлено')


async def insert_abuse_collection(record):
    record['_id'] = record.pop('id')
    existing = await abuse_collection.find_one({'_id': record['_id']})
    if not existing:
        await abuse_collection.insert_one(record)
        logging.info(f'Добавлена новая запись: {record['_id']}')
    else:
        logging.info(f'Запись {record['_id']} уже существует')


async def show_collection(length):
    cursor = abuse_collection.find({})
    docs = await cursor.to_list(length=length)
    for doc in docs:
        print(doc)
