from pydantic import BaseModel
from pydantic_settings import BaseSettings


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash( (type(self),) + tuple(self.__dict__.values()) )


class HashableBaseSettings(BaseSettings):
    def __hash__(self):
        return hash( (type(self),) + tuple(self.__dict__.values()) )

