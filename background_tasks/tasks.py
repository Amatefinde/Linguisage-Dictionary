import asyncio
import time

from loguru import logger

from .celery import celery
from scripts import find_and_save_to_db
from Parsers.main_collector import WordNotExist

loop = asyncio.get_event_loop()


@celery.task
def find_and_add_world(query: str):
    try:
        loop.run_until_complete(find_and_save_to_db(query))
    except WordNotExist:
        logger.info(f'The word "{query}" is not found')
