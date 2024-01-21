from timeit import default_timer
from loguru import logger


def async_timer(func):
    async def wrapper(*args, **kwargs):
        start = default_timer()
        result = await func(*args, **kwargs)
        end = default_timer()
        logger.info(f"Время выполнения функции {func.__name__}: {end - start} секунд")
        return result

    return wrapper


def timer(func):
    def wrapper(*args, **kwargs):
        start = default_timer()
        result = func(*args, **kwargs)
        end = default_timer()
        logger.info(f"Время выполнения функции {func.__name__}: {end - start} секунд")
        return result

    return wrapper
