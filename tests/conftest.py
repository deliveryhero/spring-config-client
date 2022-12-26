import os

import pytest


@pytest.fixture
def auth():
    os.environ['CONFIGSERVER_AUTH_USERNAME'] = 'user'
    os.environ['CONFIGSERVER_AUTH_PASSWORD'] = 'pass'
