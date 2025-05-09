import httpx
from .proxmox_base_uri_generator import proxmox_base_uri

from logger.logger import get_logger

logger = get_logger(__name__)

async def aproxmox_get_auth_cookie(
        proxmox_host: str,
        username: str, 
        password: str, 
        realm: str
        )-> tuple[str, str] | tuple[None, None]:#Fetches cookie and csrf tokens
    
    uri = f'{proxmox_base_uri(proxmox_host)}/access/ticket'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_data = {"username": username, "password": password, "realm":realm}
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(uri, headers=headers, data=auth_data)

        if response.status_code == 200:

            response_data = response.json()

            cookie = response_data["data"]["ticket"]
            csrf = response_data["data"]["CSRFPreventionToken"]

            return cookie, csrf
        
        elif response.status_code == 401: return None, None #Invalid credentials
        
        else: response.raise_for_status()
    
    except httpx.RequestError as err:
        logger.error(f"Connection error fetching Proxmox ticket: {err}")
        raise
    except httpx.HTTPStatusError as err:
        logger.error(f"Proxmox API returned {err.response.status_code}: {err}")
    except (ValueError, KeyError) as err:
        logger.error(f"Malformed Proxmox API response: {err}")