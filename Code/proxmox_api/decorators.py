import httpx
from functools import wraps

from logger.logger import get_logger

from typing import Callable, TypeVar, Optional, Awaitable

logger = get_logger(__name__)

T = TypeVar('T')

def handle_network_errors(func: Callable[..., Awaitable[bool]]) -> Callable[..., Awaitable[bool]]:
    """Handles network-related errors for async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> bool:
        try:
            return await func(*args, **kwargs)
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            logger.error(f"Network connection error: {err}")
            return False
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                logger.info(f"Resource not found: {err.request.url}")
                raise
            logger.error(f"HTTP error: {err}")
            raise
        except httpx.RequestError as err:
            logger.error(f"Request error: {err}")
            raise
    return wrapper