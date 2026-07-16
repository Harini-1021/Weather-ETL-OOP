# Weather ETL OOP

A class-based rebuild of a weather ETL (Extract, Transform, Load) pipeline, using
OpenWeatherMap's API. This is a follow-up to [Weather-ETL](https://github.com/Harini-1021/Weather-ETL),
reimplementing the same core logic with an object-oriented design, decorators,
logging, and automated tests.

## What it does

Fetches current weather for one or more cities, cleans and flattens the data,
and generates a summary report (console + CSV) — all via a single CLI command.

```bash
python -m src.main --cities London Tokyo "New York" --units metric
```

Example output:
```
Weather Summary — 3 city(ies)
========================================
Average temperature: 25.8°C
Hottest: Tokyo (31.5°C)
Coldest: London (17.6°C)

Conditions breakdown:
  Clear: 1 city(ies)
  Clouds: 2 city(ies)

Saved to: reports/weather_report_20260715_195544.csv
```

If a city fails to fetch (bad name, API error), it's logged and skipped —
the rest of the run continues normally.

## Architecture

| Class | Responsibility |
|---|---|
| `DataFetcher` | Fetches raw weather JSON from OpenWeatherMap, with automatic retries |
| `DataCleaner` | Flattens raw JSON into a clean pandas DataFrame |
| `ReportGenerator` | Aggregates multi-city data into a summary + saves CSV reports |

Orchestrated end-to-end by `src/main.py`, a CLI entry point built with `argparse`.

## Concepts demonstrated

- **OOP design** — three single-responsibility classes, composed together in `main.py`
- **Decorators** — `@timer` (measures execution time) and `@retry` (retries transient
  API failures with configurable attempts/delay), both built from scratch in
  `src/decorators.py`
- **Logging** — centralized logger configuration (`src/logger_config.py`), writing
  to both console and `pipeline.log`, replacing ad-hoc `print()` debugging
- **pandas** — flattening nested JSON, `groupby` aggregation, `idxmin`/`idxmax`
  for identifying hottest/coldest cities
- **Error handling** — per-city failure isolation in the CLI loop, narrow exception
  handling in `@retry` (only retries `RequestException`, not logic errors)
- **Testing** — 17 automated `pytest` tests covering `DataCleaner`, `ReportGenerator`,
  and both decorators, using fixtures, `tmp_path`, and simulated failures
  (no live API calls in tests)

## Setup

```bash
git clone https://github.com/Harini-1021/Weather-ETL-OOP.git
cd Weather-ETL-OOP

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the project root with your OpenWeatherMap API key:
```
OWM_API_KEY=your_api_key_here
```

## Usage

```bash
python -m src.main --cities London Tokyo --units metric
```

Options:
- `--cities` — one or more city names (required)
- `--units` — `metric`, `imperial`, or `standard` (default: `metric`)

## Running tests

```bash
pytest -v
```

## Project structure

```
Weather-ETL-OOP/
├── src/
│   ├── fetcher.py           # DataFetcher
│   ├── datacleaning.py      # DataCleaner
│   ├── reportgenerator.py   # ReportGenerator
│   ├── decorators.py        # @timer, @retry
│   ├── logger_config.py     # centralized logging setup
│   └── main.py               # CLI entry point
├── tests/
│   ├── test_datacleaning.py
│   ├── test_reportgenerator.py
│   └── test_decorators.py
├── requirements.txt
└── README.md
```

## Related

- [Weather-ETL](https://github.com/Harini-1021/Weather-ETL) — the original
  function-based version this project rebuilds using OOP