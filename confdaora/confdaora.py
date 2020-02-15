import dataclasses
import os
import re
from typing import Any, Dict, Mapping, Type, _GenericAlias  # type: ignore

from dictdaora import DictDaora
from jsondaora.deserializers import deserialize_field

from confdaora.exceptions import ValidationError


def confdaora_env(conf_type: Type[Any]) -> DictDaora:
    return from_dict(conf_type, os.environ)


def is_user_type(type_: Type[Any]) -> bool:
    return isinstance(type_, type) and (
        issubclass(type_, dict) or dataclasses.is_dataclass(type_)
    )


def from_dict(conf_type: Type[Any], mapping: Mapping[str, Any]) -> DictDaora:
    conf = DictDaora()

    for name, type_ in conf_type.__annotations__.items():
        prefix = getattr(conf_type, '__prefix__', None)
        value: Any

        if prefix:
            key = f'{prefix}_{name}'
        else:
            key = name

        if is_user_type(type_):
            conf[name] = from_dict(type_, mapping)
            continue

        if (
            isinstance(type_, _GenericAlias)
            and type_._name == 'List'
            and is_user_type(type_.__args__[0])
        ):
            type_ = type_.__args__[0]
            prefix = getattr(type_, '__prefix__', '').upper()
            keys = [
                k
                for k in mapping
                for f in type_.__annotations__.keys()
                if k.startswith(prefix) and k.endswith(f.upper())
            ]
            values = []

            for k in keys:
                match = re.match(f"{prefix}_.*(\\d+)_(.*)", k)
                if match:
                    value = mapping.get(k.upper())
                    index, attr_name = match.groups()
                    values.append((int(index), attr_name.lower(), value))

            values = sorted(values, key=lambda v: v[0])
            dyn_types: Dict[int, Type[Any]] = {}

            for index, attr_name, value in values:  # type: ignore
                type_index = dyn_types.get(index)  # type: ignore

                if not type_index:
                    type_index = type(
                        f'{type_.__name__}{index}',
                        (type_,),
                        {
                            '__prefix__': f'{prefix}_{index}'
                            if prefix
                            else str(index)
                        },
                    )
                    dyn_types[index] = type_index  # type: ignore

            conf_values = [
                from_dict(dtype, mapping) for dtype in dyn_types.values()
            ]
            conf[name] = conf_values
            continue

        else:
            value = mapping.get(key.upper())

        if value:
            value = value.split(',')
            value = (
                [v.strip(' ') for v in value] if len(value) > 1 else value[0]
            )

        elif hasattr(conf_type, name):
            value = getattr(conf_type, name)

        else:
            raise ValidationError(f'required field: name={name}')

        if value is not None:
            conf[name] = deserialize_field(name, type_, value)

    return conf
