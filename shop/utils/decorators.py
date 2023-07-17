import logging
import time

logger = logging.getLogger(__name__)



def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"Executed {func.__name__} in {execution_time} seconds")
        return result
    return wrapper

