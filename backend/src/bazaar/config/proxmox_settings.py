from bazaar.lib.hashable_pydantic import HashableBaseModel

from pydantic import Field


class ProxmoxSettings(HashableBaseModel):
    api_host: str
    
    api_username: str
    api_password: str
    
    verify_ssl: bool = Field(False)
    