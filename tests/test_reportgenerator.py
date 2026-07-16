""" 
Tests for ReportGenerator
"""

import pandas as pd
import pytest

from src.reportgenerator import ReportGenerator

@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame([
        {"city": "London", "country": "GB", "temperature": 18.0, "condition": "Clouds"},
        {"city": "Tokyo", "country": "JP", "temperature": 30.0, "condition": "Clear"},
        {"city": "New York", "country": "US", "temperature": 25.0, "condition": "Clear"},
    ])

def test_generate_summary_contains_average(sample_df):
    """Summary should report the correct average temperature."""
    reporter = ReportGenerator()
    summary = reporter.generate_summary(sample_df)
    expected_avg = (18.0 + 30.0 + 25.0) / 3  # 24.333...
    assert f"{expected_avg:.1f}" in summary

def test_generate_summary_identifies_hottest(sample_df):
    """Summary should correctly identify Tokyo as hottest."""
    reporter = ReportGenerator()
    summary = reporter.generate_summary(sample_df)
    assert "Tokyo" in summary
    assert "Hottest" in summary

def test_generate_summary_identifies_coldest(sample_df):
    """Summary should correctly identify London as coldest."""
    reporter = ReportGenerator()
    summary = reporter.generate_summary(sample_df)
    assert "London" in summary
    assert "Coldest" in summary

def test_generate_summary_condition_breakdown(sample_df):
    """Summary should correctly count cities per condition (2 Clear, 1 Clouds)."""
    reporter = ReportGenerator()
    summary = reporter.generate_summary(sample_df)
    assert "Clear: 2" in summary
    assert "Clouds: 1" in summary

def test_generate_summary_empty_dataframe():
    """Summary should handle an empty DataFrame gracefully, not crash."""
    reporter = ReportGenerator()
    summary = reporter.generate_summary(pd.DataFrame())
    assert "No data available" in summary

def test_save_to_csv_creates_file(sample_df, tmp_path):
    """save_to_csv() should create a real CSV file at the returned path."""
    reporter = ReportGenerator(output_dir=str(tmp_path))
    filepath = reporter.save_to_csv(sample_df, "test_report")

    import os
    assert os.path.exists(filepath)
    assert filepath.endswith(".csv")

def test_save_to_csv_content_matches(sample_df, tmp_path):
    """The saved CSV should contain the same data as the original DataFrame."""
    reporter = ReportGenerator(output_dir=str(tmp_path))
    filepath = reporter.save_to_csv(sample_df, "test_report")

    reloaded = pd.read_csv(filepath)
    assert len(reloaded) == len(sample_df)
    assert list(reloaded["city"]) == list(sample_df["city"])

    