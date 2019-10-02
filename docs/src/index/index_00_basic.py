from typing import TypedDict

from confdaora import confdaora_env


class AppConfig(TypedDict):
    port: int
    host: str


config = confdaora_env(AppConfig)

print(config)
