import logging
import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
database = client.get_database(os.getenv('MONGODB_NAME'))
collection = database.get_collection(os.getenv('MONGODB_COLLECTION'))

async def start_mongodb():
    logging.warning('Подключение к базе данных успешно установлено')
