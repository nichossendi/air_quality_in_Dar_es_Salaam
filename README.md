# Air Quality in Dar es Salaam

Predicticting PM2.5 air quality readings using an autoregressive (AR) time series model, sourced from MongoDB.

## Problem

Given hourly PM2.5 sensor readings from multiple sites in Dar es Salaam,
identify the site with the most complete data, clean and resample the readings and
build/evaluate an AR model with walk-forward validation.

## Project Structure

```
├── data/                   # raw JSON export (gitignored), used only to seed Mongo
├── scripts/
│   └── seed_mongo.py       # loads data/dar-es-salaam.json into local MongoDB
├── notebooks/
├── src/air_quality/
│   ├── wrangle.py          # MongoDB query + cleaning logic
│   └── model.py            # AR model selection, walk-forward validation
├── tests/
└── reports/
```

## Setup

1. Start a local MongoDB instance (Docker is easiest):
   ```bash
   docker run -d -p 27017:27017 --name aq-mongo mongo:6
   ```
2. Install dependencies:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Seed the database:
   ```bash
   python scripts/seed_mongo.py
   ```
4. Confirm it worked:
   ```bash
   python -c "from pymongo import MongoClient; print(MongoClient()['air-quality']['dar-es-salaam'].count_documents({}))"
   ```

## Data

`data/dar-es-salaam.json` contains synthetic hourly PM2.5 (`P2`) and PM10
(`P1`) readings for 3 sensor sites (11, 23, 29) across 2018, with realistic
autoregressive structure, daily/weekly seasonality, missing-data gaps, and
outlier spikes >100 (by design, to be filtered during cleaning). Site 11 has
the most complete readings, matching the assignment's expected finding.

## Running Tests

```bash
pytest
```

## Status

🚧 In progress — see `reports/findings.md`.
