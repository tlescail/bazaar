from ..api import api
from . import proxmox


api.include_router(proxmox.router)
