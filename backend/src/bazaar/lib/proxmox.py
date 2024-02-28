from functools import lru_cache
from typing_extensions import Annotated
from fastapi import Depends
from proxmoxer import ProxmoxAPI
import urllib3

from bazaar.config.settings import Settings, settings
from bazaar.config.proxmox_settings import ProxmoxSettings


@lru_cache
def proxmox_settings(settings: Annotated[Settings, Depends(settings)] = settings()) -> ProxmoxSettings:
    return settings.configuration.proxmox_settings


@lru_cache
def proxmox(settings: Annotated[ProxmoxSettings, Depends(proxmox_settings)] = proxmox_settings()) -> ProxmoxAPI:
    urllib3.disable_warnings()
    return ProxmoxAPI(
        host=settings.api_host,
        user=settings.api_username,
        password=settings.api_password,
        verify_ssl=settings.verify_ssl
    )