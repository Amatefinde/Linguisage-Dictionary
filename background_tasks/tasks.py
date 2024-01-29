import asyncio
import time

from loguru import logger

from .celery import celery
from scripts import find_and_save_to_db
from Parsers import SeleniumImgCollector
from Parsers.main_collector import WordNotExist


@celery.task
def find_and_add_world(query: str):
    image_collector = SeleniumImgCollector()
    with image_collector:
        try:
            asyncio.run(find_and_save_to_db(query, image_collector))
        except WordNotExist:
            logger.info(f'The word "{query}" is not found')
