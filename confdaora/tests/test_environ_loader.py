import pytest
from dictdaora import DictDaora

import confdaora.confdaora
from confdaora.confdaora import confdaora_env


@pytest.fixture
def fake_os(mocker):
    return mocker.patch.object(confdaora.confdaora, 'os')


def test_should_set_variables_from_os_environ(fake_os):
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
