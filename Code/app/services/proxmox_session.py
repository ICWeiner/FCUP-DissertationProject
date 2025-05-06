import time
import asyncio
import httpx

from collections import defaultdict
from typing import Dict, Tuple

from proxmox_api.utils.connection import aproxmox_get_auth_cookie_ldap

from logger.logger import get_logger

logger = get_logger(__name__)

_proxmox_auth_caches: Dict[str, Dict] = defaultdict(lambda: {
    "cookie": None,
    "csrf": None,
    "expires_at": 0,
})

_auth_locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

def _build_session(cookie,csrf):
    session = httpx.AsyncClient(verify=False)
    session.cookies.set("PVEAuthCookie", cookie)
    session.headers.update({"CSRFPreventionToken": csrf})  
    return session

async def aget_proxmox_session(proxmox_host: str, username: str, password: str) -> httpx.AsyncClient:
    now = time.time()

    user_cache = _proxmox_auth_caches[username]

    if user_cache["cookie"] and user_cache["expires_at"] > now:
        return _build_session(user_cache["cookie"], user_cache["csrf"])
    
    async with _auth_locks[username]:#lock for thread safety on credential update
        # If expired or missing, use the provided function to fetch new tokens
        cookie, csrf = await aproxmox_get_auth_cookie_ldap(proxmox_host, username, password)

        logger.info("#######################")
        logger.info(f"New session created for user {username}")
        logger.info("#######################")

        user_cache.update({
            "cookie": cookie,
            "csrf": csrf,
            "expires_at": now + 2 * 3500,
        })
        return _build_session(cookie, csrf)