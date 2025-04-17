import httpx
from .proxmox_base_uri_generator import proxmox_base_uri

from logger.logger import get_logger

logger = get_logger(__name__)

async def aproxmox_get_auth_cookie(proxmox_host, username, password):#Fetches cookie and csrf tokens
    uri = f'{proxmox_base_uri(proxmox_host)}/access/ticket'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_data = {"username": username, "password": password}
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(uri, headers=headers, data=auth_data)
    except Exception as err:
        logger.error("Failure during ticket request", err)
        exit(1)

    response.raise_for_status()

    try:
        response_data = response.json()
    except ValueError:
        logger.error("Failure during JSON parsing")
        exit(1)

    cookie = response_data["data"]["ticket"]
    csrf = response_data["data"]["CSRFPreventionToken"]

    return cookie, csrf