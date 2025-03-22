import asyncio
import logging

from abuse import get_abuses
from circl import get_circl
from MongoDB import start_mongodb
from rss_feeds import get_rss_feeds


async def main():
    await start_mongodb()
    logging.warning("Приложение запущено")
    await get_abuses()
    await get_rss_feeds()
    await get_circl()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
