from dataclasses import dataclass
from typing import List

from confdaora import confdaora_env


@dataclass
class DBConfig:
    __prefix__ = 'db'
    host: str
    port: int = 3306


@dataclass
class KeyConfig:
    __prefix__ = 'keys'
    name: str
    values: List[int]


@dataclass
class AppConfig:
    db: DBConfig
    keys: List[KeyConfig]
    host: str
    port: int = 8080


config = confdaora_env(AppConfig)

print(config)
