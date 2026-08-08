"""
Unit tests for air_quality.wrangle.
Requires a local MongoDB seeded via scripts/seed_mongo.py before running.
"""

import pytest
from pymongo import MongoClient

from air_quality.wrangle import wrangle

@pytest.fixture(scope="module")
def collection():
    client = MongoClient(host = "localhost", port = 27017, serverSelectionTimeoutMS = 2000)

    try:
        client.admin.command("ping")
    except Exception:
        pytest.skip("No local MongoDB running on localhost:27017. Start it and reseed first.")

    col = client["air-quality"]["dar-es-salaam"]
    
    # Flush container database state
    col.delete_many({})
    
    # Inject isolated test data directly so tests pass without external files
    col.insert_many([
        {"timestamp": pd.Timestamp("2026-08-01 00:00:00"), "P2": 12.5, "metadata": {"site": 11, "measurement": "P2"}},
        {"timestamp": pd.Timestamp("2026-08-01 01:00:00"), "P2": 14.2, "metadata": {"site": 11, "measurement": "P2"}},
        {"timestamp": pd.Timestamp("2026-08-01 02:00:00"), "P2": 150.0, "metadata": {"site": 11, "measurement": "P2"}}, # Outlier
        {"timestamp": pd.Timestamp("2026-08-01 03:00:00"), "P2": 18.1, "metadata": {"site": 11, "measurement": "P2"}},
    ])

    yield col

    # Clean up the test database state
    col.delete_many({})


@pytest.fixture
def y(collection):
    return wrangle(collection, site = 11)

def test_no_outliers_above_100(y):
    assert (y < 100).all()

def test_no_missing_values(y):
    assert y.isna().sum() == 0

def test_hourly_frequency(y):
    assert y.index.freq is not None

def test_series_name(y):
    assert y.name == "P2"