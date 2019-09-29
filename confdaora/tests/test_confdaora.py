from dataclasses import asdict

import pytest
from dictdaora import DictDaora

from confdaora.confdaora import confdaora, os


@pytest.fixture
def fake_environ(mocker):
    return mocker.patch.object(os, 'environ')


def test_should_set_env_vars_with_different_types(fake_environ):
    class FakeConfig(DictDaora):
        fake_int: int
        fake_str: str
        fake_float: float

    fake_environ.get = {
        'FAKE_INT': '10',
        'FAKE_STR': 'string',
        'FAKE_FLOAT': '.1',
    }.get
    expected_config = {'fake_int': 10, 'fake_str': 'string', 'fake_float': 0.1}

    assert confdaora(FakeConfig) == expected_config


def test_should_set_env_vars_with_prefix(fake_environ):
    class FakeConfig(DictDaora):
        __prefix__ = 'fake'
        integer: int

    fake_environ.get = {'FAKE_INTEGER': '10'}.get
    expected_config = {'integer': 10}

    assert confdaora(FakeConfig) == expected_config


def test_should_set_env_vars_on_dataclass(fake_environ):
    class FakeConfig:
        integer: int

    fake_environ.get = {'INTEGER': '10'}.get
    expected_config = {'integer': 10}

    assert asdict(confdaora(FakeConfig)) == expected_config


def test_should_set_env_vars_with_nested_config(fake_environ):
    class FakeConfig3(DictDaora):
        __prefix__ = 'fake3'
        number: float

    class FakeConfig2(DictDaora):
        __prefix__ = 'fake2'
        string: str
        fake3: FakeConfig3

    class FakeConfig(DictDaora):
        __prefix__ = 'fake'
        integer: int
        fake2: FakeConfig2

    fake_environ.get = {
        'FAKE_INTEGER': '10',
        'FAKE2_STRING': 'str',
        'FAKE3_NUMBER': '.1',
    }.get
    expected_config = {
        'integer': 10,
        'fake2': {'string': 'str', 'fake3': {'number': 0.1}},
    }

    assert confdaora(FakeConfig) == expected_config
