import time
from loguru import logger


def async_timer(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        logger.info(f"Время выполнения функции {func.__name__}: {end - start} секунд")
        return result

    return wrapper


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"Время выполнения функции {func.__name__}: {end - start} секунд")
        return result

    return wrapper
