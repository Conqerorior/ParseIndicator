import asyncio
import logging
from MongoDB import start_mongodb
from abuse import get_abuses


async def main():
    await start_mongodb()
    logging.warning("Приложение запущено")
    await get_abuses()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
