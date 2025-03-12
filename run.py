import asyncio
import logging
from main import main

logging.basicConfig(level=logging.INFO)

async def main():
    logging.info('Запуск скрипта')
    await main()

if __name__ == "__main__":
    asyncio.run(main())
