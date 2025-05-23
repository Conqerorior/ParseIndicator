import logging
import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_NAME = os.getenv('MONGODB_NAME')
ABUSE_COLLECTION = os.getenv('ABUSE_COLLECTION')
CIRCL_COLLECTION = os.getenv('CIRCL_COLLECTION')
RSS_COLLECTION = os.getenv('RSS_COLLECTION')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
database = client.get_database(MONGODB_NAME)
abuse_collection = database.get_collection(ABUSE_COLLECTION)
circl_collection = database.get_collection(CIRCL_COLLECTION)
rss_collection = database.get_collection(RSS_COLLECTION)


async def start_mongodb():
    logging.warning('Подключение к базе данных успешно установлено')


async def insert_abuse_collection(record):
    record['_id'] = record.pop('id')
    existing = await abuse_collection.find_one({'_id': record['_id']})
    if not existing:
        await abuse_collection.insert_one(record)
        logging.info(f'Добавлена новая запись: {record["_id"]}')
    else:
        logging.info(f'Запись {record["_id"]} уже существует')


async def insert_circl_collection_if_exist(record):
    record['_id'] = record.pop('uuid')
    existing = await circl_collection.find_one({'_id': record['_id']})
    if not existing:
        await circl_collection.insert_one(record)
        logging.info(f'Добавлена новая запись: {record["_id"]}')


async def insert_rss_collection(article):
    existing = await rss_collection.find_one({'title': article['title'], 'link': article['link'],
                                              'published': article['published']})
    if not existing:
        await rss_collection.insert_one(article)
        logging.info(f'Добавлена новая запись: {article["title"]}')
    else:
        logging.info(f'Запись {article["title"]} уже существует')


async def show_collection(collection, length):
    cursor = collection.find({})
    docs = await cursor.to_list(length=length)
    for doc in docs:
        print(doc)
