import dataclasses
import os
from typing import Any, Type

from jsondaora import as_typed_dict, asdataclass, jsondaora


def confdaora(conf_type: Type[Any]) -> Any:
    conf_args = {}
    conf_type = jsondaora(conf_type)

    for name, type_ in conf_type.__annotations__.items():
        prefix = getattr(conf_type, '__prefix__', None)

        if prefix:
            key = f'{prefix}_{name}'
        else:
            key = name

        if issubclass(type_, dict) or dataclasses.is_dataclass(type_):
            conf_args[name] = confdaora(type_)
        else:
            value: Any = os.environ.get(key.upper())
            value = value.split(',')
            value = (
                [v.strip(' ') for v in value] if len(value) > 1 else value[0]
            )
            conf_args[name] = value

    if issubclass(conf_type, dict):
        return as_typed_dict(conf_args, conf_type)

    return asdataclass(conf_args, conf_type)
