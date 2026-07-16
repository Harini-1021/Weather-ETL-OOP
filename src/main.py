"""
CLI entry point for the Weather ETL OOP pipeline
""" 

import argparse

import pandas as pd

from src.fetcher import DataFetcher
from src.datacleaning import DataCleaner
from src.reportgenerator import ReportGenerator
from src.logger_config import get_logger

logger = get_logger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description= "Fetch, clean, and report on weather data for one or more cities"

    )
    parser.add_argument(
        "--cities",
        nargs="+",
        required=True,
        help= "One or more city names, e.g. --cities London Tokyo \"New York\"",
    )
    parser.add_argument(
        "--units",
        choices = ["metric","imperial","standard"],
        default="metric",
        help= "Units for temperature (default: metric)",
    )
    return parser.parse_args()

def run_pipeline(cities: list[str], units: str)-> pd.DataFrame:
    fetcher = DataFetcher()
    cleaner = DataCleaner()

    cleaned_frames = []
    for city in cities:
        try:
            raw = fetcher.fetch_current_weather(city, units=units)
            df = cleaner.clean(raw)
            cleaned_frames.append(df)
        except Exception as e:
            logger.error(f"Skipping '{city} due to error: {e}")
            continue
    if not cleaned_frames:
        logger.warning("No cities were successfully fetched.")
        return pd.DataFrame() 
    
    return pd.concat(cleaned_frames, ignore_index=True)
    
def main() -> None:
    args = parse_args()

    logger.info(f"Starting pipeline for cities: {args.cities} (units={args.units})")

    combined_df = run_pipeline(args.cities, args.units)

    if combined_df.empty:
        print("No data available - all city fetches failed.")
        return
    
    reporter = ReportGenerator()
    summary = reporter.generate_summary(combined_df)
    print(summary)

    filepath = reporter.save_to_csv(combined_df, "weather_report")
    print(f"\nSaved to: {filepath}")


if __name__ == "__main__":
    main()