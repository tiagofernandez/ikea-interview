import pytest

from warehouse import config


@pytest.fixture
def app():
    return config.app
