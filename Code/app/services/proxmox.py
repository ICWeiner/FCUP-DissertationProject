import random
import httpx
import asyncio
import logging
import proxmox_api.proxmox_vm_actions as proxmox_vm_actions 
import proxmox_api.proxmox_vm_firewall as proxmox_vm_firewall
import proxmox_api.utils.proxmox_vm_ip_fetcher as proxmox_vm_ip_fetcher
import functools
from . import proxmox_session
from time import sleep #this should probably be asyncio sleep not time sleep, but weird things happens when i change

from ..config import settings

CONCURRENT_LIMIT = settings.CONCURRENT_LIMIT

class SemaphoreManager:
    _semaphore = None

    @classmethod
    def get_semaphore(cls):
        if cls._semaphore is None:
            #loop = asyncio.get_running_loop()  # Ensure we're using the correct event loop
            cls._semaphore = asyncio.Semaphore(1)
        return cls._semaphore
    
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

def with_proxmox_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        #async with SemaphoreManager.get_semaphore():
        session = await proxmox_session.aget_proxmox_session( *_get_proxmox_host_and_credentials() )
        try:
            return await func(session, *args, **kwargs)
        except httpx.RequestError as err:
            logging.error(f"Error in {func.__name__}: {err}")
            return False
        finally:
            await session.aclose()
    return wrapper

def _get_proxmox_host():
    return settings.PROXMOX_HOST

def _get_proxmox_credentials():
    return settings.PROXMOX_USER, settings.PROXMOX_PASSWORD

def _get_proxmox_host_and_credentials():
    return _get_proxmox_host(), *_get_proxmox_credentials()

@with_proxmox_session
async def adestroy_vm(session, vm_proxmox_id):
    return await proxmox_vm_actions.adestroy( _get_proxmox_host(), session, vm_proxmox_id)


@with_proxmox_session
async def aclone_vm(session, template_proxmox_id, hostname):
    clone_id = None

    while clone_id is None:
        id = random.randint(100, 999999999)
        if await proxmox_vm_actions.acheck_free_id( _get_proxmox_host(), session, id): clone_id = id

    await proxmox_vm_actions.acreate( _get_proxmox_host(), session, template_proxmox_id, clone_id, hostname)

    return clone_id

@with_proxmox_session
async def aset_vm_status(session, vm_proxmox_id, desired_status, max_retries=10, interval=5):
    action = ""
    if desired_status == True:
        await proxmox_vm_actions.astart( _get_proxmox_host(), session, vm_proxmox_id)
        action = "Power on"
    else:
        await proxmox_vm_actions.astop( _get_proxmox_host(), session, vm_proxmox_id)
        action = "Power off"
    
    for _ in range(max_retries): 
        if await proxmox_vm_actions.acheck_vm_status( _get_proxmox_host(), session, vm_proxmox_id) == desired_status:
            return True
        sleep(interval)

    logging.warning(f"Timeout reached while waiting for VM {vm_proxmox_id} to {action}.")
    raise TimeoutError(f"VM {vm_proxmox_id} failed to {action}.")

@with_proxmox_session
async def atemplate_vm(session, vm_proxmox_id, max_retries=10, interval=5):
    if await proxmox_vm_actions.atemplate( _get_proxmox_host(), session, vm_proxmox_id):
        for _ in range(max_retries):
            if await proxmox_vm_actions.acheck_vm_is_template( _get_proxmox_host(), session, vm_proxmox_id):
                return True
            sleep(interval)
        raise TimeoutError(f"VM {vm_proxmox_id} failed to become a template.")

@with_proxmox_session
async def aget_vm_ip(session, vm_proxmox_id):
    return await proxmox_vm_ip_fetcher.get_ip( _get_proxmox_host(), session, vm_proxmox_id)

@with_proxmox_session
async def acreate_firewall_rules(session, vm_proxmox_id, teacher_vm_proxmox_id):
    teacher_vm_ip = await proxmox_vm_ip_fetcher.get_ip( _get_proxmox_host(), session, teacher_vm_proxmox_id)
    return await proxmox_vm_firewall.acreate_proxmox_vm_isolation_rules( _get_proxmox_host(), session, vm_proxmox_id, teacher_vm_ip)

@with_proxmox_session
async def adestroy_firewall_rules(session, vm_proxmox_id):
    return await proxmox_vm_firewall.adelete_proxmox_vm_isolation_rules( _get_proxmox_host(), session, vm_proxmox_id)
