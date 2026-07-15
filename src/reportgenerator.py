"""
summarizes and persists cleaned weather data across multiple cities
"""

import os
from datetime import datetime

import pandas as pd

from src.logger_config import get_logger
logger = get_logger(__name__)

class ReportGenerator:
    def __init__(self, output_dir:str = "reports") -> None:
        """
        Args:
            output_dir: Folder where CSV reports are saved. Created if missing.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_summary(self, df: pd.DataFrame) -> str:
        """
        Build a human-readable text summary of weather across multiple cities.

        Args:
            df: A DataFrame with one row per city (from DataCleaner.clean,
                concatenated across cities).

        Returns:
            A formatted summary string. 
        """
        if df.empty:
            logger.warning("generate_summary called with an empty DataFrame")
            return "No data available to summarize."
        
        num_cities = len(df)
        avg_temp = df["temperature"].mean()
        min_row = df.loc[df["temperature"].idxmin()]
        max_row = df.loc[df["temperature"].idxmax()] 

        # Groupby breakdown: how many cities per weather condition
        conditions_count = df.groupby("condition")["city"].count()

        lines = [
            f"Weather Summary — {num_cities} city(ies)",
            "=" * 40,
            f"Average temperature: {avg_temp:.1f}°C",
            f"Hottest: {max_row['city']} ({max_row['temperature']:.1f}°C)",
            f"Coldest: {min_row['city']} ({min_row['temperature']:.1f}°C)",
            "",
            "Conditions breakdown:",
        ]

        for condition, count in conditions_count.items():
            lines.append(f" {condition}: {count} city(ies)")

        summary = "\n".join(lines)
        logger.info(f"Generated summary for {num_cities} cities")
        return summary
    
    def save_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """
        Save the DataFrame to a timestamped CSV file in output_dir.

        Args:
            df: The DataFrame to save.
            filename: Base filename (without extension), e.g. "weather_report".

        Returns:
            The full path to the saved CSV file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{filename}_{timestamp}.csv"
        filepath = os.path.join(self.output_dir,full_filename)

        df.to_csv(filepath, index=False)
        logger.info(f"Saved report to {filepath}")
        return filepath