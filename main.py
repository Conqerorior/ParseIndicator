import asyncio
import logging

from abuse import get_abuses
from MongoDB import start_mongodb


async def main():
    await start_mongodb()
    logging.warning("Приложение запущено")
    await get_abuses()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
