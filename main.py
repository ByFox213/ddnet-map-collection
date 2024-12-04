import asyncio
import logging
import os

from ddapi import DDStatsDB

from db import DB
from dotenv import load_dotenv

from model import Postresql

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

load_dotenv()
dd = DDStatsDB()
db = DB(str(Postresql(**{k.lower(): e for k, e in os.environ.items()})))


async def main():
    await db.check_new_map(dd)


if __name__ == "__main__":
    asyncio.run(main())
