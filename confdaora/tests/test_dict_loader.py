from typing import List, TypedDict

import pytest
from dictdaora import DictDaora

from confdaora.confdaora import from_dict
from confdaora.exceptions import ValidationError


def test_should_set_dict_with_different_types():
    class FakeConfig(DictDaora):
        fake_int: int
        fake_str: str
        fake_float: float

    config = {
        'FAKE_INT': '10',
        'FAKE_STR': 'string',
        'FAKE_FLOAT': '.1',
    }
    expected_config = {'fake_int': 10, 'fake_str': 'string', 'fake_float': 0.1}

    assert from_dict(FakeConfig, config) == expected_config


def test_should_set_variables_with_prefix():
    class FakeConfig(DictDaora):
        __prefix__ = 'fake'
        integer: int

    config = {'FAKE_INTEGER': '10'}
    expected_config = {'integer': 10}

    assert from_dict(FakeConfig, config) == expected_config


def test_should_set_variables_on_dataclass():
    class FakeConfig:
        integer: int

    config = {'INTEGER': '10'}
    expected_config = {'integer': 10}

    assert from_dict(FakeConfig, config) == expected_config


def test_should_set_variables_with_nested_config():
    class FakeConfig3(DictDaora):
        __prefix__ = 'fake3'
        numbers: List[float]

    class FakeConfig2(DictDaora):
        __prefix__ = 'fake2'
        string: str
        fake3: FakeConfig3

    class FakeConfig(DictDaora):
        __prefix__ = 'fake'
        integer: int
        fake2: FakeConfig2

    config = {
        'FAKE_INTEGER': '10',
        'FAKE2_STRING': 'str',
        'FAKE3_NUMBERS': '.1,.2,.3',
    }
    expected_config = {
        'integer': 10,
        'fake2': {'string': 'str', 'fake3': {'numbers': [0.1, 0.2, 0.3]}},
    }

    assert from_dict(FakeConfig, config) == expected_config


def test_should_set_variables_with_list_user_type():
    class FakeConfig2(TypedDict):
        __prefix__ = 'fake2'
        string: str
        numbers: List[float]

    class FakeConfig(TypedDict):
        __prefix__ = 'fake'
        integer: int
        fake2: List[FakeConfig2]

    config = {
        'FAKE_INTEGER': '10',
        'FAKE2_0_STRING': 'str0',
        'FAKE2_0_NUMBERS': '.1,.2,.3',
        'FAKE2_1_STRING': 'str1',
        'FAKE2_1_NUMBERS': '.4,.5,.6',
    }
    expected_fake2 = [
        {'string': 'str0', 'numbers': [0.1, 0.2, 0.3]},
        {'string': 'str1', 'numbers': [0.4, 0.5, 0.6]},
    ]
    expected_config = {'integer': 10, 'fake2': expected_fake2}

    assert from_dict(FakeConfig, config) == expected_config


def test_should_raise_validation_error_for_required_field():
    class FakeConfig(TypedDict):
        __prefix__ = 'fake'
        integer: int

    with pytest.raises(ValidationError) as exc_info:
        from_dict(FakeConfig, {})

    assert exc_info.value.args == ('required field: name=integer',)


def test_should_use_default_value():
    class FakeConfig(TypedDict):
        __prefix__ = 'fake'
        integer: int = 10

    assert from_dict(FakeConfig, {}) == {'integer': 10}
