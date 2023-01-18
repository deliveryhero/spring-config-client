from unittest.mock import patch

import pytest

from spring_config_client.conf.settings import Settings


def test_settings_initialization_without_auth():
    settings = Settings()

    with pytest.raises(ValueError) as exc:
        settings.KEY

    assert 'Authentication username or password is not configured!' in str(exc)


@patch('spring_config_client.conf.settings.ConfigClient')
def test_settings_get(mock_config_client, auth):
    mock_config_client().config = {}

    settings = Settings()

    assert settings.KEY is None


@pytest.mark.parametrize(
    "config, expected_value",
    [
        ({'KEY': 'value'}, 'value'),
        ({'KEY': None}, None),
        ({'KEY': 2}, 2),
        ({'KEY': 2.2}, 2.2),
    ]
)
@patch('spring_config_client.conf.settings.ConfigClient')
def test_settings_get_key(mock_config_client, auth, config, expected_value):
    mock_config_client().config = config

    settings = Settings()

    assert settings.KEY == expected_value


@pytest.mark.parametrize(
    "environ,config,expected_value",
    [
        ({'LOCAL_KEY': 'local_value'}, {'KEY': '${LOCAL_KEY}'}, 'local_value'),
        ({'LOCAL_KEY': 'local_value'}, {'KEY': '${LOCAL_KEY:default}'}, 'local_value'),
        ({}, {'KEY': '${LOCAL_KEY:secure-internal-api-key}'}, 'secure-internal-api-key'),
        ({}, {'KEY': '${LOCAL_KEY:test}'}, 'test'),
        ({}, {'KEY': '${LOCAL_KEY}'}, None),
        ({'LOCAL_KEY': 'local_value'}, {}, None),
        ({'LOCAL_KEY': 'http://someurl{}"'}, {'KEY': '${LOCAL_KEY}'}, 'http://someurl{}"'),
        (
            {},
            {'KEY': "${SALEOR_URL:https://saleor-asia-uat.wegotwe.com/graphql/}"},
            "https://saleor-asia-uat.wegotwe.com/graphql/"
        )
    ]
)
@patch('spring_config_client.conf.settings.ConfigClient')
@patch('spring_config_client.conf.resolver.os')
def test_settings_get_key_from_environ(
    mock_os, mock_config_client, auth, config, environ, expected_value
):
    mock_os.environ = environ
    mock_config_client().config = config

    settings = Settings()

    assert settings.KEY == expected_value


@pytest.mark.parametrize(
    "environ,config,expected_value",
    [
        ({'LOCAL_KEY': '1'}, {'KEY': {"KEY": '${LOCAL_KEY}'}}, '1'),
        ({}, {'KEY': {"KEY": '${LOCAL_KEY:1}'}}, '1'),
        ({}, {'KEY': {"KEY": "${KEY:{'hello':'world','1':'1'}}"}}, "{'hello':'world','1':'1'}"),
        ({}, {'KEY': {"KEY": "${KEY:[]}"}}, "[]"),
    ]
)
@patch('spring_config_client.conf.settings.ConfigClient')
@patch('spring_config_client.conf.resolver.os')
def test_settings_get_key_from_nested_environ(
    mock_os, mock_config_client, auth, config, environ, expected_value
):
    mock_os.environ = environ
    mock_config_client().config = config

    settings = Settings()

    assert settings.KEY.KEY == expected_value


@pytest.mark.parametrize(
    "environ,config,expected_value",
    [
        ({}, {'KEY': {"KEY": {"KEY": '${LOCAL_KEY:1}'}}}, '1'),
    ]
)
@patch('spring_config_client.conf.settings.ConfigClient')
@patch('spring_config_client.conf.resolver.os')
def test_settings_get_key_from_extra_nested_environ(
    mock_os, mock_config_client, auth, config, environ, expected_value
):
    mock_os.environ = environ
    mock_config_client().config = config

    settings = Settings()

    assert settings.KEY.KEY.KEY == expected_value


@pytest.mark.parametrize(
    "config,expected_value",
    [
        ({'REDIS': {'key': 'value', 'key2': 2}}, 'local_value'),
    ]
)
@patch('spring_config_client.conf.settings.ConfigClient')
@patch('spring_config_client.conf.resolver.os')
def test_nested_settings(
    mock_os, mock_config_client, auth, config, expected_value
):
    mock_os.environ = {}
    mock_config_client().config = config

    settings = Settings()
    assert settings.REDIS.hello is None
    assert settings.REDIS.key2 == 2
    assert settings.REDIS.key == 'value'
