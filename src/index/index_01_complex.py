from typing import List, TypedDict

from confdaora import confdaora_env


class DBConfig(TypedDict):
    __prefix__ = 'db'
    port: int = 3306
    host: str


KeyConfig = TypedDict('KeyConfig', {'name': str, 'values': List[int]})
KeyConfig.__prefix__ = 'keys'


class AppConfig(TypedDict):
    port: int = 8080
    host: str
    db: DBConfig
    keys: List[KeyConfig]


config = confdaora_env(AppConfig)

print(config)
