import asyncio
import httpx
import threading
from datetime import datetime, timedelta, timezone
from datetime import timedelta

from collections import defaultdict
from typing import Dict, Tuple, Optional

from app import decorators 
from app.config import settings
from proxmox_api.utils.connection import aproxmox_get_auth_cookie

from logger.logger import get_logger

logger = get_logger(__name__)

class ProxmoxSessionManager:

    _instance = None
    _lock = threading.Lock()  # Use threading.Lock for sync operations
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
                cls._instance.__init__()
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_auth_cookies'):  # Prevent re-init
            self._auth_cookies: Dict[str, dict] = {}  # Stores cookies
            self._locks = defaultdict(asyncio.Lock)  # One lock by user
            self._proxmox_host = settings.PROXMOX_HOST

    def _store_cookie(
            self,
            username: str,
            realm: str,
            cookie: str,
            csrf: str
    ):
        """Create and store new auth cookie"""
        self._auth_cookies[f'{username}@{realm}'] = {
            "cookie": cookie,
            "csrf": csrf,
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=1, minutes=30)#below 2 hours which is the lifespan of these pve auth cookies 
        }
        logger.info("#######################")
        logger.info(f"New session created for user {username}")
        print(self._auth_cookies)
        logger.info("#######################")
        
        
    async def verify_credentials(
        self,
        username: str,
        password: str,
        realm: str = "",
    ) -> Tuple[bool, bool]: #first value indicates sucess, second indicates if privileged
        """Verify credentials with Proxmox server"""
        @decorators.with_retry(max_attempts=2, initial_delay=2, allowed_exceptions = (httpx.HTTPStatusError) )
        async def _attempt_auth_with_realm(realm: str) -> bool:
            logger.info(f"Attempting to login into realm {realm} with user {username}")
            async with self._locks[f"{username}@{realm}"]:
                try:
                    auth_result = await aproxmox_get_auth_cookie(
                        self._proxmox_host,
                        username,
                        password,
                        realm
                    )

                    if not auth_result or None in auth_result:  # Handle None return
                        logger.debug(f"Authentication failed for {username}@{realm}")
                        return False
                    
                    cookie, csrf = auth_result
                    if not all((cookie, csrf)):
                        logger.warning(f"Empty cookie/csrf for {username}@{realm}")
                        return False

                    self._store_cookie(username, realm, cookie, csrf)
                    logger.info(f"Sucessful authentication into realm {realm} with user {username}")
                    return True
                except Exception as e:
                    logger.error(f"Unexpected error during {username}@{realm} auth: {str(e)}")
                    return False
                
        if realm != "": 

            if await _attempt_auth_with_realm(realm): return True, True

        else:
                    
            if await _attempt_auth_with_realm(settings.LDAP_PRIVILEGED_REALM): return True, True

            if await _attempt_auth_with_realm(settings.LDAP_BASE_REALM): return True, False

        logger.info(f"Failed to login with user {username}")
        
        return False, False
    
    def get_session(
            self, 
            username: str, 
            realm: str
            ) -> Optional[httpx.AsyncClient]:
        """Retrieve an active session"""
        data = self._auth_cookies[f'{username}@{realm}']
        if not data or data["expires_at"] <= datetime.now(timezone.utc):
            return None
        
        session = httpx.AsyncClient(verify=False)
        session.cookies.set("PVEAuthCookie", data["cookie"])
        session.headers.update({"CSRFPreventionToken": data["csrf"]})  
        return session

