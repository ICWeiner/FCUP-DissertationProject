import time
import asyncio
import httpx

from proxmox_api.utils.connection import aproxmox_get_auth_cookie

from logger.logger import get_logger

logger = get_logger(__name__)

_proxmox_auth_cache = {
    "cookie": None,
    "csrf": None,
    "expires_at": 0,
}

_auth_lock = asyncio.Lock()

def _build_session(cookie,csrf):
    session = httpx.AsyncClient(verify=False)

    session.cookies.set("PVEAuthCookie", cookie)

    session.headers.update({"CSRFPreventionToken": csrf})  
    
    return session

async def aget_proxmox_session(proxmox_host, username, password):
    now = time.time()
    if _proxmox_auth_cache["cookie"] and _proxmox_auth_cache["expires_at"] > now:
        return _build_session(_proxmox_auth_cache["cookie"], _proxmox_auth_cache["csrf"])
    #TODO: test lock here instead of above
    async with _auth_lock:#lock for thread safety on credential update
        # If expired or missing, use the provided function to fetch new tokens
        cookie, csrf = await aproxmox_get_auth_cookie(proxmox_host, username, password)
        logger.info("#######################")
        logger.info("New session created")
        logger.info("#######################")
        _proxmox_auth_cache.update({
            "cookie": cookie,
            "csrf": csrf,
            "expires_at": now + 2 * 3500,
        })
        return _build_session(cookie, csrf)