from bazaar.lib.hashable_pydantic import HashableBaseModel

from .proxmox_settings import ProxmoxSettings


class Configuration(HashableBaseModel):
    proxmox_settings: ProxmoxSettings