import pytest

from warehouse import config


@pytest.fixture
def app():
    return config.app


@pytest.fixture(autouse=True)
def run_around_tests():
    clear_data()
    yield


def clear_data():
    db = config.db
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
