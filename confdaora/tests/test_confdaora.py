from typing import List, TypedDict

import pytest
from dictdaora import DictDaora

import confdaora.confdaora
from confdaora.confdaora import confdaora_env
from confdaora.exceptions import ValidationError


@pytest.fixture
def fake_os(mocker):
    return mocker.patch.object(confdaora.confdaora, 'os')


def test_should_set_env_vars_with_different_types(fake_os):
    class FakeConfig(DictDaora):
        fake_int: int
        fake_str: str
        fake_float: float

    fake_os.environ = {
        'FAKE_INT': '10',
        'FAKE_STR': 'string',
        'FAKE_FLOAT': '.1',
    }
    expected_config = {'fake_int': 10, 'fake_str': 'string', 'fake_float': 0.1}

    assert confdaora_env(FakeConfig) == expected_config


def test_should_set_env_vars_with_prefix(fake_os):
    class FakeConfig(DictDaora):
        __prefix__ = 'fake'
        integer: int

    fake_os.environ = {'FAKE_INTEGER': '10'}
    expected_config = {'integer': 10}

    assert confdaora_env(FakeConfig) == expected_config


def test_should_set_env_vars_on_dataclass(fake_os):
    class FakeConfig:
        integer: int

    fake_os.environ = {'INTEGER': '10'}
    expected_config = {'integer': 10}

    assert confdaora_env(FakeConfig) == expected_config


def test_should_set_env_vars_with_nested_config(fake_os):
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

    fake_os.environ = {
        'FAKE_INTEGER': '10',
        'FAKE2_STRING': 'str',
        'FAKE3_NUMBERS': '.1,.2,.3',
    }
    expected_config = {
        'integer': 10,
        'fake2': {'string': 'str', 'fake3': {'numbers': [0.1, 0.2, 0.3]}},
    }

    assert confdaora_env(FakeConfig) == expected_config


def test_should_set_env_vars_with_list_user_type(fake_os):
    class FakeConfig2(TypedDict):
        __prefix__ = 'fake2'
        string: str
        numbers: List[float]

    class FakeConfig(TypedDict):
        __prefix__ = 'fake'
        integer: int
        fake2: List[FakeConfig2]

    fake_os.environ = {
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

    assert confdaora_env(FakeConfig) == expected_config


def test_should_raise_validation_error_required_field(fake_os):
    class FakeConfig(TypedDict):
        __prefix__ = 'fake'
        integer: int

    fake_os.environ = {}

    with pytest.raises(ValidationError) as exc_info:
        confdaora_env(FakeConfig)

    assert exc_info.value.args == ('required field: name=integer',)


def test_should_use_default_value(fake_os):
    class FakeConfig(TypedDict):
        __prefix__ = 'fake'
        integer: int = 10

    fake_os.environ = {}

    assert confdaora_env(FakeConfig) == {'integer': 10}
