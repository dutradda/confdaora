# confdaora

<p align="center" style="margin: 3em">
  <a href="">
    <img src="python.svg" alt="confdaora" width="300"/>
  </a>
</p>

<p align="center">
    <em>Configurations using python annotations</em>
</p>

---

**Documentation**: <a href="#" target="_blank"></a>

**Source Code**: <a href="#" target="_blank"></a>

---


## Key Features

- Generate a `DictDaora` with values parsed from environment variables.


## Requirements

 - Python 3.6+
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
{'port': 8080, 'host': 'localhost', 'db': {'port': 3306, 'host': 'localhost'}, 'keys': [{'name': 'test', 'values': [10, 20]}, {'name': 'test2', 'values': [30, 40]}]}

```
