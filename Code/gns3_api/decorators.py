from functools import wraps
import httpx

from typing import Callable, TypeVar, Optional, Awaitable

from logger.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')

def handle_network_errors(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[Optional[T]]]:
    """Handles network-related errors for async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Optional[T]:
        try:
            return await func(*args, **kwargs)
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            logger.error(f"Network connection error: {err}")
            return None
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                logger.info(f"Resource not found: {err.request.url}")
                return None
            logger.error(f"HTTP error: {err}")
            raise
        except httpx.RequestError as err:
            logger.error(f"Request error: {err}")
            raise
    return wrapper