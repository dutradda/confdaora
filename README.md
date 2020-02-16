# confdaora

<p align="center" style="margin: 3em">
  <a href="">
    <img src="https://dutradda.github.io/confdaora/confdaora.svg" alt="confdaora" width="300"/>
  </a>
</p>

<p align="center">
    <em>Configurations using python annotations</em>
</p>

---

**Documentation**: <a href="https://dutradda.github.io/confdaora/" target="_blank">https://dutradda.github.io/confdaora</a>

**Source Code**: <a href="https://github.com/dutradda/confdaora" target="_blank">https://github.com/dutradda/confdaora</a>

---


## Key Features

- Generate a `DictDaora` with values parsed from environment variables.


## Requirements

 - Python 3.8+
 - dictdaora
 - jsondaora


## Instalation
```
$ pip install confdaora
```


## Basic example

```python
from typing import TypedDict

from confdaora import confdaora_env


class AppConfig(TypedDict):
    port: int
    host: str


config = confdaora_env(AppConfig)

print(config)

```

Suposing your file calls `myconf.py`:
```
PORT=8080 HOST=localhost python myconf.py

```

```
{'port': 8080, 'host': 'localhost'}

```


## Complex example

```python
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

```

Suposing your file calls `myconf.py`:
```
HOST=localhost \
DB_HOST=localhost \
KEYS_0_NAME=test \
KEYS_0_VALUES=10,20 \
KEYS_1_NAME=test2 \
KEYS_1_VALUES=30,40 \
python myconf.py

```

```
{'db': {'host': 'localhost', 'port': 3306}, 'keys': [{'name': 'test', 'values': [10, 20]}, {'name': 'test2', 'values': [30, 40]}], 'host': 'localhost', 'port': 8080}

```
