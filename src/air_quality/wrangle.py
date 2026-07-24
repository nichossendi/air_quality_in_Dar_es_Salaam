"""
    Data cleaning for Dar es Salaam PM2.5 sensor readings sourced from MongoDB.
"""

import pandas as pd
from pymongo.collection import Collection


def wrangle(collection: Collection, site: int = 11) -> pd.Series:
    """
    Query and clean PM2.5 readings for a single site.

    Cleaning steps:
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

    results = collection.find(
        {
            "metadata.site": site,
            "metadata.measurement": "P2"
        },
        projection = {
            "P2": 1,
            "timestamp": 1,
            "_id": 0
        },
    )

    # Read results into a DataFrame indexed by the timestamp
    df = pd.DataFrame(list(results)).set_index("timestamp")

    # Localize timezone to Dar es Salaam, Tanzania local time
    df.index = df.index.tz_localize("UTC").tz_convert("Africa/Dar_es_Salaam")

    # Remove outlier PM2.5 readings above 100
    df = df[df["P2"] < 100]

    # Resample to hourly frequency (mean) and forward fill any gaps
    resampled_series = df["P2"].resample("h").mean().ffill()

    # Return as a named Series
    resampled_series.name = "P2"

    return resampled_series


def get_site_reading_counts(collection: Collection) -> list[dict]:
    """
    Return the number of readings (any measurement type) per site.

    Useful for identifying which site has the most complete data before
    committing to a single site in wrangle().
    """
    
    # TODO: implement via an aggregation pipeline
    raise NotImplementedError
