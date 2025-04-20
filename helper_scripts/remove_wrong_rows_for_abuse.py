import re
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_NAME = os.getenv('MONGODB_NAME')
ABUSE_COLLECTION = os.getenv('ABUSE_COLLECTION')

client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]
collection = db[ABUSE_COLLECTION]

uuid_pattern = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
    re.IGNORECASE
)
uuid_no_hyphens = re.compile(
    r'^[0-9a-f]+$',
    re.IGNORECASE
)

query = {
    "$or": [
        {"ioc": {"$regex": r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', "$options": "i"}},
        {"ioc": {"$regex": r'^[0-9a-f]+$', "$options": "i"}}
    ]
}

# Получаем список документов, которые будут удалены
docs_to_delete = list(collection.find(query))

print(f"Найдено {len(docs_to_delete)} записей для удаления:")
for doc in docs_to_delete:
    print(doc)

if docs_to_delete:
    result = collection.delete_many(query)
    print(f"Удалено {result.deleted_count} записей")