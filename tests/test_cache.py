from datetime import datetime
from pathlib import Path

import pytest

from slackcat.cache import Cache


@pytest.fixture
def cache(tmpdir):
    file = Path(tmpdir) / "cache.db"
    file.touch()
    return Cache(file)


def test_set_sync_get(cache):
    date = datetime(year=2020, month=1, day=5)
    value = "Hello world"
    cache.set(date, value)
    assert cache.get(date) == value
    cache.sync()
    assert cache.get(date) == value


def test_get_in_range(cache):
    for day in range(1, 20):
        date = datetime(year=2020, month=1, day=day)
        value = f"Hello world {day}"
        cache.set(date, value)
    cache.sync()
    from_date = datetime(year=2020, month=1, day=5)
    to_date = datetime(year=2020, month=1, day=9)
    assert cache.get_in_range(from_date, to_date) == [
        f"Hello world {i}" for i in range(5, 10)
    ]
