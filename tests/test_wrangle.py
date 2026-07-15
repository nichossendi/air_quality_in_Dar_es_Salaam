"""Unit tests for air_quality.wrangle.

Requires a local MongoDB seeded via scripts/seed_mongo.py before running.
"""

import pytest
from pymongo import MongoClient

from air_quality.wrangle import wrangle


@pytest.fixture(scope="module")
def collection():
    client = MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=2000)
    try:
        client.admin.command("ping")
    except Exception:
        pytest.skip("No local MongoDB running on localhost:27017 — start it and reseed first.")
    return client["air-quality"]["dar-es-salaam"]


@pytest.fixture
def y(collection):
    return wrangle(collection, site=11)


def test_no_outliers_above_100(y):
    # TODO: assert (y < 100).all()
    pass


def test_no_missing_values(y):
    # TODO: assert y.isna().sum() == 0
    pass


def test_hourly_frequency(y):
    # TODO: assert y.index.freq is not None (or check consistent hourly spacing)
    pass


def test_series_name(y):
    # TODO: assert y.name == "P2"
    pass
