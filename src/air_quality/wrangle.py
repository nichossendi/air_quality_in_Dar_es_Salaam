"""Data cleaning for Dar es Salaam PM2.5 sensor readings, sourced from MongoDB.

Kept out of the notebook so it's importable, testable, and reusable, same
pattern as Projects 1 and 2.
"""

import pandas as pd
from pymongo.collection import Collection


def wrangle(collection: Collection, site: int = 11) -> pd.Series:
    """Query and clean PM2.5 readings for a single site.

    Cleaning steps (to implement):
        1. Query the collection for the given site's P2 (PM2.5) readings.
        2. Read results into a DataFrame indexed by timestamp.
        3. Localize timestamps to Africa/Dar_es_Salaam.
        4. Remove outlier PM2.5 readings above 100.
        5. Resample to hourly frequency (mean), forward-fill any gaps.
        6. Return a Series named "P2".

    Parameters
    ----------
    collection : pymongo.collection.Collection
        The MongoDB collection to query (e.g. db["dar-es-salaam"]).
    site : int
        Which sensor site to pull readings for. Default 11 (the site with
        the most complete readings in this dataset).

    Returns
    -------
    pd.Series
        Hourly PM2.5 readings, cleaned and gap-filled.
    """
    # TODO: implement cleaning steps above (Monday session)
    raise NotImplementedError


def get_site_reading_counts(collection: Collection) -> list[dict]:
    """Return the number of readings (any measurement type) per site.

    Useful for identifying which site has the most complete data before
    committing to a single site in wrangle().
    """
    # TODO: implement via an aggregation pipeline
    raise NotImplementedError
