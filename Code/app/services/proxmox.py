import random
import httpx
import asyncio
import functools
import ipaddress

import proxmox_api.proxmox_vm_actions as proxmox_vm_actions 
import proxmox_api.proxmox_vm_firewall as proxmox_vm_firewall
import proxmox_api.utils.proxmox_vm_ip_fetcher as proxmox_vm_ip_fetcher

from app import decorators 
from app.config import settings
from app.services import proxmox_session
from logger.logger import get_logger


logger = get_logger(__name__)

class SemaphoreManager:
    _semaphore = None

    @classmethod
    def get_semaphore(cls):
        if cls._semaphore is None:
            cls._semaphore = asyncio.Semaphore(settings.CONCURRENT_LIMIT)
        return cls._semaphore
    

def with_proxmox_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with SemaphoreManager.get_semaphore():
            session = await proxmox_session.aget_proxmox_session( *_get_proxmox_host_and_credentials() )
            try:
                return await func(session, *args, **kwargs)
            except httpx.RequestError as err:
                logger.error(f"Error in {func.__name__}: {err}")
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
@decorators.with_retry
async def adestroy_vm(session, vm_proxmox_id):
    return await proxmox_vm_actions.adestroy( _get_proxmox_host(), session, vm_proxmox_id)


@with_proxmox_session
@decorators.with_retry
async def aclone_vm(session, template_proxmox_id, hostname):
    clone_id = None

    while clone_id is None:
        id = random.randint(100, 999999999)
        if await proxmox_vm_actions.acheck_free_id( _get_proxmox_host(), session, id): clone_id = id

    await proxmox_vm_actions.acreate( _get_proxmox_host(), session, template_proxmox_id, clone_id, hostname)

    return clone_id

@with_proxmox_session
@decorators.with_retry
async def aset_vm_status(session, vm_proxmox_id, desired_status):
    if desired_status == True:
        await proxmox_vm_actions.astart( _get_proxmox_host(), session, vm_proxmox_id)
    else:
        await proxmox_vm_actions.astop( _get_proxmox_host(), session, vm_proxmox_id)

    if await proxmox_vm_actions.acheck_vm_status( _get_proxmox_host(), session, vm_proxmox_id) == desired_status:
        return True


@with_proxmox_session
@decorators.poll_until_complete(max_retries=10, interval=5)
async def atemplate_vm(session, vm_proxmox_id) -> bool:
    # First attempt the templating operation
    if not await proxmox_vm_actions.atemplate(_get_proxmox_host(), session, vm_proxmox_id):
        return False
    
    # Then check completion status
    return await proxmox_vm_actions.acheck_vm_is_template(
        _get_proxmox_host(), session, vm_proxmox_id
    )

@with_proxmox_session
@decorators.with_retry(allowed_exceptions=(ValueError,) )
async def aget_vm_ip(session, vm_proxmox_id) -> str:
    ip = await proxmox_vm_ip_fetcher.get_ip(_get_proxmox_host(), session, vm_proxmox_id)
    
    # This will raise ValueError for invalid IPs, triggering retry
    if ipaddress.ip_address(ip).version == 4:
        logger.info(f"Successfully acquired IPv4 address for VM {vm_proxmox_id}")
        return ip
    
    logger.info("Returned address is not valid IPv4")
    raise ValueError("Invalid IPv4 address")  # Triggers retry


@with_proxmox_session
@decorators.with_retry
async def aget_vm_hostname(session, vm_proxmox_id) -> str:
    return await proxmox_vm_ip_fetcher.get_hostname( _get_proxmox_host(), session, vm_proxmox_id)

@with_proxmox_session
@decorators.with_retry
async def acreate_firewall_rules(session, vm_proxmox_id, teacher_vm_proxmox_id) -> bool:
    teacher_vm_ip = await proxmox_vm_ip_fetcher.get_ip( _get_proxmox_host(), session, teacher_vm_proxmox_id)
    return await proxmox_vm_firewall.acreate_proxmox_vm_isolation_rules( _get_proxmox_host(), session, vm_proxmox_id, teacher_vm_ip)

@with_proxmox_session
@decorators.with_retry
async def adestroy_firewall_rules(session, vm_proxmox_id) -> bool:
    return await proxmox_vm_firewall.adelete_proxmox_vm_isolation_rules( _get_proxmox_host(), session, vm_proxmox_id)
