from functools import lru_cache
from pydantic_settings import SettingsConfigDict
from pydantic import Field, FilePath

from bazaar.lib.hashable_pydantic import HashableBaseSettings
from .configuration import Configuration


class Settings(HashableBaseSettings):
    
    config_file: FilePath = Field("config.json")
    
    __config__: Configuration | None = None
    
    model_config = SettingsConfigDict(
        env_prefix="bazaar_",
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
    @property
    def configuration(self) -> Configuration:
        if self.__config__ is None:
            self.__config__ = Configuration.model_validate_json(self.config_file.read_text())
            
        return self.__config__

@lru_cache
def settings() -> Settings:
    return Settings()