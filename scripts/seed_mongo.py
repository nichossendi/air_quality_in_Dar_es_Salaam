"""Seed a local MongoDB instance with synthetic Dar es Salaam air quality data.

Prerequisites:
    - A MongoDB server running locally on port 27017. Easiest way, via Docker:
        docker run -d -p 27017:27017 --name aq-mongo mongo:6
    - pymongo installed: pip install pymongo

Usage:
    python scripts/seed_mongo.py
"""

import json
from datetime import datetime
from pathlib import Path

from pymongo import MongoClient

DATA_FILE = Path(__file__).parent.parent / "data" / "dar-es-salaam.json"


def main():
    client = MongoClient(host="localhost", port=27017)
    db = client["air-quality"]
    collection = db["dar-es-salaam"]

    existing = collection.count_documents({})
    if existing > 0:
        print(f"Collection already has {existing} documents. Dropping and reseeding.")
        collection.drop()

    with open(DATA_FILE) as f:
        docs = json.load(f)

    # convert ISO timestamp strings to real datetime objects for Mongo
    for doc in docs:
        doc["timestamp"] = datetime.strptime(doc["timestamp"], "%Y-%m-%dT%H:%M:%SZ")

    result = collection.insert_many(docs)
    print(f"Inserted {len(result.inserted_ids)} documents into air-quality.dar-es-salaam")

    # quick sanity check, mirrors what the assignment asks you to verify
    sites = collection.distinct("metadata.site")
    print("Sites in collection:", sites)


if __name__ == "__main__":
    main()
