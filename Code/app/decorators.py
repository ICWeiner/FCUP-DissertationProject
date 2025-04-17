import asyncio
from functools import wraps
from typing import Callable, Awaitable, Type

from logger.logger import get_logger

logger = get_logger(__name__)

def with_retry(
    max_attempts: int = 5, 
    initial_delay: float = 3.0,
    backoff_factor: float = 2.0,
    allowed_exceptions: tuple = (Exception,)
):
    """
    Decorator that retries a function upon failure.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = initial_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except allowed_exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"Final attempt {attempt} failed: {str(e)}")
                        raise
                    logger.warning(f"Attempt {attempt} failed, retrying in {current_delay}s...")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff_factor
        return wrapper
    return decorator

def poll_until_complete(
    max_retries: int = 10,
    interval: float = 5.0,
    timeout_exception: Type[Exception] = TimeoutError
):
    """
    Decorator that polls until a successful result or timeout.
    """
    def decorator(func: Callable[..., Awaitable[bool]]) -> Callable[..., Awaitable[bool]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> bool:
            for attempt in range(1, max_retries + 1):
                result = await func(*args, **kwargs)
                if result:
                    return True
                if attempt < max_retries:
                    await asyncio.sleep(interval)
            
            raise timeout_exception(
                f"Operation timed out after {max_retries} attempts "
                f"(interval: {interval}s)"
            )
        return wrapper
    return decorator