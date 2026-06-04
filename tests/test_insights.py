# tests/test_insights.py
"""
Test scaffolds for DATA-05 requirement.
Initially skipped - will pass after src/data/insights.py implementation.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


def test_detect_anomalies_with_outliers():
    """Task 1: Verify detect_anomalies finds outliers using IQR method."""
    from src.data.insights import detect_anomalies

    # Create data with clear outliers
    df = pd.DataFrame({'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]})

    result = detect_anomalies(df, 'value')

    # Should detect outlier (100 is far outside IQR bounds)
    assert result is not None
    assert result['type'] == 'anomaly'
    assert 'value' in result['message']
    assert '异常值' in result['message']
    assert 'outlier_count' in result['statistics']
    assert result['statistics']['outlier_count'] == 1
    assert 'bounds' in result['statistics']


def test_detect_anomalies_no_outliers():
    """Task 1: Verify detect_anomalies returns None when outliers < 5%."""
    from src.data.insights import detect_anomalies

    # Create data with no significant outliers
    df = pd.DataFrame({'value': list(range(1, 101))})

    result = detect_anomalies(df, 'value')

    # Should return None (no outliers > 5%)
    assert result is None


def test_detect_anomalies_insufficient_data():
    """Task 1: Verify detect_anomalies returns None for small datasets."""
    from src.data.insights import detect_anomalies

    # Create small dataset (< 10 rows)
    df = pd.DataFrame({'value': [1, 2, 3, 4, 5]})

    result = detect_anomalies(df, 'value')

    # Should return None (insufficient data)
    assert result is None


@pytest.mark.skip(reason="Waiting for Task 4: generate_initial_insights")
def test_generate_insights():
    """DATA-05: Verify generation of 1-2 insights (trends or anomalies)."""
    pass


@pytest.mark.skip(reason="Waiting for Task 4: generate_initial_insights")
def test_no_mental_math():
    """DATA-05: Verify all statistics computed via code execution (PITFALL-01: no LLM mental math)."""
    pass